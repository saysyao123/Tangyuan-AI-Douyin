'use strict';

const { app } = require('electron');
const {
  LAYOUT_VERSION,
  resolvePortableRoot,
  buildPortableLayout,
  ensurePortableLayout
} = require('./core/portable-paths');
const { ProjectStore } = require('./core/project-store');
const { AccountRegistry } = require('./core/account-registry');
const { WorkerScheduler } = require('./core/worker-scheduler');
const { WorkerConfigStore } = require('./core/worker-config');
const { ProfileVault } = require('./core/vault');
const { ElectronProfileBridge } = require('./core/electron-profile-bridge');
const { installPortableRuntime } = require('./core/portable-runtime');
const { DEFAULT_INITIAL_VAULT_PASSWORD } = require('./core/defaults');

const root = resolvePortableRoot({
  env: process.env,
  execPath: process.execPath,
  isPackaged: app.isPackaged,
  moduleDir: __dirname
});
const layout = buildPortableLayout(root);
ensurePortableLayout(layout);

// Keep durable metadata separate from browser credentials. Electron userData
// remains the migration-compatible home for accounts/tasks/UI metadata, while
// Chromium session storage is redirected to the ephemeral vault-controlled
// runtime root before app ready. No Dola partition is opened until renderer or
// worker code explicitly prepares an account after vault unlock.
app.setPath('userData', layout.electronUserData);
app.setPath('sessionData', layout.sessionDataDir);

process.env.DOLA_WORKBENCH_ROOT = layout.root;
process.env.DOLA_WORKBENCH_DATA_ROOT = layout.dataDir;
process.env.DOLA_WORKBENCH_LAYOUT_VERSION = String(LAYOUT_VERSION);
process.env.SEEDANCE_STUDIO_CONTROL_DIR = layout.controlDir;
process.env.DOLA_ARTIFACT_ROOT = layout.debugCapturesDir;

const projectStore = new ProjectStore(layout);
const accountRegistry = new AccountRegistry(layout);
const workerConfig = new WorkerConfigStore(layout);
const workerSettings = workerConfig.load();
const workerScheduler = new WorkerScheduler(workerSettings);
const vault = new ProfileVault(layout);
const profileBridge = new ElectronProfileBridge(layout, vault);

// User-requested first-run convenience: initialize/unlock with the public
// bootstrap password. This is not treated as a security boundary; the desktop
// UI prominently recommends replacing it after first successful login.
let defaultPasswordActive = false;
try {
  if (!vault.isInitialized()) {
    vault.initialize(DEFAULT_INITIAL_VAULT_PASSWORD);
    defaultPasswordActive = true;
  } else if (!['UNLOCKED', 'RESEAL_REQUIRED'].includes(vault.status().state)) {
    try {
      vault.unlock(DEFAULT_INITIAL_VAULT_PASSWORD);
      defaultPasswordActive = true;
    } catch (_) {
      // A private replacement password has already been configured. Stay
      // locked and let the local desktop unlock Gate request it.
    }
  }
} catch (_) {
  // Fail closed. The renderer can still show the normal unlock/recovery Gate.
}

const portableRuntime = installPortableRuntime({
  layout,
  projectStore,
  accountRegistry,
  workerConfig,
  workerScheduler,
  vault,
  profileBridge,
  defaultPasswordActive
});

function activeVault() { return portableRuntime.vault; }
function activeBridge() { return portableRuntime.profileBridge; }
function vaultUnlocked() {
  return ['UNLOCKED', 'RESEAL_REQUIRED'].includes(activeVault().status().state);
}

function vaultLockedError() {
  const error = new Error('Dola profile vault is locked. Unlock it once in the desktop UI before opening or dispatching account sessions.');
  error.code = 'VAULT_LOCKED';
  error.statusCode = 423;
  return error;
}

const controlServer = require('./control-server');
const originalStartControlServer = controlServer.startControlServer;
controlServer.startControlServer = async function startPortableControlServer(legacyHandlers) {
  async function syncAccounts() {
    const legacy = typeof legacyHandlers.listAccounts === 'function'
      ? await legacyHandlers.listAccounts()
      : [];
    return accountRegistry.syncLegacy(legacy);
  }

  async function prepareAccount(id) {
    if (!vaultUnlocked()) throw vaultLockedError();
    await syncAccounts();
    const account = accountRegistry.get(id);
    if (!account) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    activeBridge().prepare(account);
    return account;
  }

  const handlers = {
    ...legacyHandlers,
    health: async () => {
      const legacyHealth = await legacyHandlers.health();
      await syncAccounts();
      const accountHealth = accountRegistry.healthSummary();
      return {
        ...legacyHealth,
        portable: {
          enabled: true,
          layoutVersion: LAYOUT_VERSION,
          projects: projectStore.listProjects().length,
          accounts: accountHealth.total,
          schedulableAccounts: accountHealth.schedulable,
          workers: workerScheduler.status(),
          vault: activeVault().status(),
          defaultPasswordActive: portableRuntime.defaultPasswordActive === true,
          profileRuntime: {
            sessionDataRootReserved: true,
            electronSessionDataRedirected: true,
            bridgeReady: true,
            runtimeBinding: 'F3-experimental-live'
          },
          f2RuntimeBinding: 'foundation-only'
        }
      };
    },

    listAccounts: async () => syncAccounts(),
    createAccount: async (name) => {
      const legacy = await legacyHandlers.createAccount(name);
      return accountRegistry.upsert({ ...legacy, source: 'legacy-poc' });
    },
    activateAccount: async (id) => {
      await prepareAccount(id);
      const activated = await legacyHandlers.activateAccount(id);
      accountRegistry.upsert({ ...activated, source: accountRegistry.get(id)?.source || 'legacy-poc' });
      return accountRegistry.get(id) || activated;
    },
    getAccountSession: async (id) => {
      await prepareAccount(id);
      const sessionState = await legacyHandlers.getAccountSession(id);
      if (accountRegistry.get(id)) {
        accountRegistry.recordHealth(id, {
          loginStatus: sessionState.loginStatus,
          pageLoaded: sessionState.pageLoaded,
          evidence: sessionState.evidence,
          pagePath: sessionState.pagePath,
          checkedAt: sessionState.checkedAt || Date.now()
        });
      }
      return sessionState;
    },
    accountHealthSummary: async () => {
      await syncAccounts();
      return accountRegistry.healthSummary();
    },
    pauseAccount: async (id, reason) => {
      await syncAccounts();
      return accountRegistry.pause(id, reason || 'MANUAL_PAUSE');
    },
    resumeAccount: async (id) => {
      await syncAccounts();
      return accountRegistry.resume(id);
    },
    debugAccount: async (id) => {
      const account = await prepareAccount(id);
      const worker = workerScheduler.promoteDebug(id);
      await legacyHandlers.activateAccount(id);
      return { account, debug: worker, workers: workerScheduler.status() };
    },
    dispatchTask: async (id) => {
      try {
        const task = await legacyHandlers.getTask(id);
        if (!task) return { ok: false, statusCode: 404, error: 'task_not_found' };
        await prepareAccount(task.accountId);
        return legacyHandlers.dispatchTask(id);
      } catch (error) {
        return {
          ok: false,
          statusCode: Number(error.statusCode) || 409,
          error: error.code || 'dispatch_blocked',
          message: error.message || String(error)
        };
      }
    },

    workerStatus: async () => ({
      ...workerScheduler.status(),
      runtimeBinding: 'foundation-only',
      note: 'F2 lease/worker policy is active as a control foundation. Real multi-worker Dola runtime binding lands in F4/F5.'
    }),
    configureWorkers: async (input) => {
      const saved = workerConfig.save(input || {});
      workerScheduler.configure(saved);
      return { settings: saved, workers: workerScheduler.status() };
    },
    sweepWorkers: async () => ({ evicted: workerScheduler.sweepIdle(), workers: workerScheduler.status() }),

    listProjects: async () => projectStore.listProjects(),
    createProject: async (input) => projectStore.createProject(input),
    getProject: async (id) => projectStore.getProject(id),
    listProjectJobs: async (id) => projectStore.listJobs(id),
    createProjectJob: async (input) => projectStore.createJob(input),
    createProjectJobRevision: async (input) => projectStore.createNewRevision(input),
    getProjectJob: async (id) => projectStore.getJob(id),
    getProjectResult: async (id) => projectStore.projectResult(id)
  };
  return originalStartControlServer(handlers);
};

// Vault credentials are accepted only over Electron IPC from the trusted local
// desktop preload. The loopback Codex Control Plane intentionally has no unlock
// endpoint and receives status only.
require('./portable-ipc').registerPortableIpc();
require('./main');
