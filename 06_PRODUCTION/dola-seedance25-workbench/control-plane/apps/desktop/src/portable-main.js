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

app.setPath('userData', layout.electronUserData);
app.setPath('sessionData', layout.sessionDataDir);

process.env.DOLA_WORKBENCH_ROOT = layout.root;
process.env.DOLA_WORKBENCH_DATA_ROOT = layout.dataDir;
process.env.DOLA_WORKBENCH_STATE_ROOT = layout.stateDir;
process.env.DOLA_WORKBENCH_OUTPUT_ROOT = layout.outputsDir;
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

let defaultPasswordActive = false;
try {
  if (!vault.isInitialized()) {
    vault.initialize(DEFAULT_INITIAL_VAULT_PASSWORD);
    defaultPasswordActive = true;
  } else if (!['UNLOCKED', 'RESEAL_REQUIRED'].includes(vault.status().state)) {
    try {
      vault.unlock(DEFAULT_INITIAL_VAULT_PASSWORD);
      defaultPasswordActive = true;
    } catch (_) {}
  }
} catch (_) {}

const portableRuntime = installPortableRuntime({
  layout,
  projectStore,
  accountRegistry,
  workerConfig,
  workerScheduler,
  vault,
  profileBridge,
  defaultPasswordActive,
  backgroundRunner: null
});

function sleep(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
function activeVault() { return portableRuntime.vault; }
function activeBridge() { return portableRuntime.profileBridge; }
function vaultUnlocked() { return ['UNLOCKED', 'RESEAL_REQUIRED'].includes(activeVault().status().state); }

function vaultLockedError() {
  const error = new Error('Dola profile vault is locked. Unlock it once in the desktop UI before opening or dispatching account sessions.');
  error.code = 'VAULT_LOCKED';
  error.statusCode = 423;
  return error;
}

function isDolaProvider(provider) {
  return ['dola-web', 'dola-web-background'].includes(String(provider || ''));
}

const controlServer = require('./control-server');
const originalStartControlServer = controlServer.startControlServer;
controlServer.startControlServer = async function startPortableControlServer(legacyHandlers) {
  async function syncAccounts() {
    const legacy = typeof legacyHandlers.listAccounts === 'function' ? await legacyHandlers.listAccounts() : [];
    return accountRegistry.syncLegacy(legacy);
  }

  async function getPortableAccount(id) {
    await syncAccounts();
    const account = accountRegistry.get(id);
    if (!account) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    return account;
  }

  async function prepareAccount(id) {
    if (!vaultUnlocked()) throw vaultLockedError();
    const account = await getPortableAccount(id);
    activeBridge().prepare(account);
    return account;
  }

  async function verifyRunnerLogin(account) {
    const runner = portableRuntime.backgroundRunner;
    if (!runner || typeof runner.sessionStatus !== 'function') {
      const error = new Error('Portable Dola runner is not ready yet.');
      error.code = 'PROVIDER_RUNTIME_NOT_READY';
      error.statusCode = 503;
      throw error;
    }
    const status = await runner.sessionStatus(account);
    accountRegistry.recordHealth(account.id, {
      loginStatus: status.loginStatus,
      pageLoaded: status.pageLoaded,
      evidence: status.evidence,
      pagePath: status.pagePath,
      checkedAt: Date.now()
    });
    if (status.loginStatus === 'logged_out') {
      const error = new Error('Dola session is logged out. Open this account in the desktop UI and complete manual login first.');
      error.code = 'LOGIN_REQUIRED';
      error.statusCode = 409;
      throw error;
    }
    if (status.loginStatus !== 'logged_in') {
      const error = new Error('Dola login state could not be confirmed. Open the account in the desktop UI and verify the page before dispatching.');
      error.code = 'LOGIN_STATE_UNKNOWN';
      error.statusCode = 409;
      throw error;
    }
    return accountRegistry.get(account.id);
  }

  async function acquireTaskLease(task, account) {
    const current = accountRegistry.get(account.id) || account;
    return workerScheduler.acquire({ ...task, accountId: account.id }, [current]);
  }

  async function runPortableTaskInBackground(task, account, mode = 'run') {
    const runner = portableRuntime.backgroundRunner;
    if (!runner) throw Object.assign(new Error('Portable Dola runner is unavailable.'), { code: 'PROVIDER_RUNTIME_NOT_READY', statusCode: 503 });
    const lease = await acquireTaskLease(task, account);
    try {
      if (mode === 'recover') {
        return await runner.recover(task, account, { waitMs: 90_000 });
      }
      await runner.directUpdateTask(task.id, {
        state: 'running',
        blockedReason: null,
        startedAt: task.startedAt || Date.now(),
        error: null,
        updatedAt: Date.now()
      });
      let result = await runner.run(task, account);
      // One automatic observation-only recovery pass. This never clicks submit
      // and therefore cannot duplicate a provider generation.
      if (result?.recoverable) {
        await sleep(5_000);
        const latest = await legacyHandlers.getTask(task.id) || task;
        result = await runner.recover(latest, account, { waitMs: 90_000 });
      }
      return result;
    } finally {
      workerScheduler.release(lease.lease.jobId);
    }
  }

  async function portableDispatch(id) {
    const task = await legacyHandlers.getTask(id);
    if (!task) return { ok: false, statusCode: 404, error: 'task_not_found' };
    if (!isDolaProvider(task.provider)) return legacyHandlers.dispatchTask(id);
    if (task.state === 'success') return { ok: true, statusCode: 200, message: 'task already completed', task };
    if (task.state === 'cancelled') return { ok: false, statusCode: 409, error: 'TASK_CANCELLED', task };
    if (task.state === 'failed') {
      return { ok: false, statusCode: 409, error: 'FAILED_TASK_REQUIRES_NEW_TASK', message: 'Create a new task/revision rather than blindly resubmitting a failed provider request.', task };
    }
    if (['running', 'capture_armed', 'generation_running', 'resolving'].includes(task.state) || workerScheduler.isJobLeased(task.id)) {
      return { ok: true, statusCode: 200, message: 'task already running', task };
    }

    let account = await prepareAccount(task.accountId);
    account = await verifyRunnerLogin(account);
    const recoveryOnly = ['observation_wait', 'result_observed', 'recovery_required', 'login_required'].includes(task.state);

    // Start asynchronously so the loopback API/UI remains responsive.
    runPortableTaskInBackground(task, account, recoveryOnly ? 'recover' : 'run').catch(async (error) => {
      try {
        const runner = portableRuntime.backgroundRunner;
        if (runner?.directUpdateTask && !recoveryOnly) {
          await runner.directUpdateTask(task.id, { state: 'failed', error: String(error.message || error).slice(0, 500), updatedAt: Date.now() });
        }
      } catch (_) {}
    });
    return {
      ok: true,
      statusCode: 202,
      message: recoveryOnly ? 'recovery accepted without resubmission' : 'portable Dola generation accepted',
      task: { ...task, state: recoveryOnly ? 'recovery_required' : 'running' }
    };
  }

  async function portableRecover(id) {
    const task = await legacyHandlers.getTask(id);
    if (!task) return { ok: false, statusCode: 404, error: 'task_not_found' };
    if (!isDolaProvider(task.provider)) return { ok: false, statusCode: 409, error: 'RECOVERY_NOT_SUPPORTED_FOR_PROVIDER' };
    if (task.state === 'success') return { ok: true, statusCode: 200, message: 'task already completed', task };
    if (workerScheduler.isJobLeased(task.id)) return { ok: false, statusCode: 409, error: 'TASK_BUSY' };
    let account = await prepareAccount(task.accountId);
    account = await verifyRunnerLogin(account);
    runPortableTaskInBackground(task, account, 'recover').catch(() => {});
    return { ok: false, statusCode: 202, recoverable: true, state: 'RECOVERY_REQUIRED', message: 'recovery accepted without provider resubmission' };
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
          providerLifecycle: {
            recoverWithoutResubmit: true,
            mediaResolver: 'in-process-candidate-ranking',
            runtimeBinding: 'F5-F6-experimental'
          }
        }
      };
    },
    listProviders: async () => {
      const providers = await legacyHandlers.listProviders();
      return providers.map((provider) => isDolaProvider(provider.id)
        ? { ...provider, state: 'portable-experimental', dispatchReady: true, gate: 'PORTABLE_G1', note: 'Portable runner available; real Dola behavior remains subject to account login, visible entitlement and Windows G1 evidence.' }
        : provider);
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
      const account = await prepareAccount(id);
      const runner = portableRuntime.backgroundRunner;
      const sessionState = runner ? await runner.sessionStatus(account) : await legacyHandlers.getAccountSession(id);
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
    accountHealthSummary: async () => { await syncAccounts(); return accountRegistry.healthSummary(); },
    pauseAccount: async (id, reason) => { await syncAccounts(); return accountRegistry.pause(id, reason || 'MANUAL_PAUSE'); },
    resumeAccount: async (id) => { await syncAccounts(); return accountRegistry.resume(id); },
    debugAccount: async (id) => {
      const account = await prepareAccount(id);
      const worker = workerScheduler.promoteDebug(id);
      await legacyHandlers.activateAccount(id);
      return { account, debug: worker, workers: workerScheduler.status() };
    },
    dispatchTask: portableDispatch,
    recoverTask: portableRecover,
    workerStatus: async () => ({
      ...workerScheduler.status(),
      runtimeBinding: 'portable-runner',
      note: 'Per-account leases and global worker cap are enforced locally. Real simultaneous Dola success still requires Windows G2 evidence.'
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

require('./portable-ipc').registerPortableIpc();

const backgroundModule = require('./background-dola');
const { PortableDolaBackgroundRunner } = require('./background-dola-portable');
backgroundModule.DolaBackgroundRunner = PortableDolaBackgroundRunner;

require('./main');
