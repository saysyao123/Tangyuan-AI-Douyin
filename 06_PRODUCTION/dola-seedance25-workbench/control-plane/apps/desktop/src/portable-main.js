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

const root = resolvePortableRoot({
  env: process.env,
  execPath: process.execPath,
  isPackaged: app.isPackaged,
  moduleDir: __dirname
});
const layout = buildPortableLayout(root);
ensurePortableLayout(layout);

// Keep the current POC implementation working while moving all runtime data
// under the portable root. F3 will replace the compatibility Chromium profile
// root with the encrypted vault lifecycle without changing account IDs.
app.setPath('userData', layout.electronUserData);

process.env.DOLA_WORKBENCH_ROOT = layout.root;
process.env.DOLA_WORKBENCH_DATA_ROOT = layout.dataDir;
process.env.DOLA_WORKBENCH_LAYOUT_VERSION = String(LAYOUT_VERSION);
process.env.SEEDANCE_STUDIO_CONTROL_DIR = layout.controlDir;
process.env.DOLA_ARTIFACT_ROOT = layout.debugCapturesDir;

// Portable V1 adds capabilities around the existing POC without forcing a
// high-risk rewrite of main.js. The legacy Electron account/session handlers
// remain the browser-session authority while durable metadata lives in the
// Portable registry and projects store.
const projectStore = new ProjectStore(layout);
const accountRegistry = new AccountRegistry(layout);
const workerConfig = new WorkerConfigStore(layout);
const workerSettings = workerConfig.load();
const workerScheduler = new WorkerScheduler(workerSettings);

const controlServer = require('./control-server');
const originalStartControlServer = controlServer.startControlServer;
controlServer.startControlServer = async function startPortableControlServer(legacyHandlers) {
  async function syncAccounts() {
    const legacy = typeof legacyHandlers.listAccounts === 'function'
      ? await legacyHandlers.listAccounts()
      : [];
    return accountRegistry.syncLegacy(legacy);
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
          f2RuntimeBinding: 'foundation-only'
        }
      };
    },

    // Account metadata is mirrored from the existing Electron session owner.
    // This avoids moving/deleting live Chromium profile data during F2 while
    // giving Codex a durable, dynamic registry for 20+ accounts.
    listAccounts: async () => syncAccounts(),
    createAccount: async (name) => {
      const legacy = await legacyHandlers.createAccount(name);
      return accountRegistry.upsert({ ...legacy, source: 'legacy-poc' });
    },
    activateAccount: async (id) => {
      const activated = await legacyHandlers.activateAccount(id);
      accountRegistry.upsert({ ...activated, source: accountRegistry.get(id)?.source || 'legacy-poc' });
      return accountRegistry.get(id) || activated;
    },
    getAccountSession: async (id) => {
      await syncAccounts();
      const session = await legacyHandlers.getAccountSession(id);
      if (accountRegistry.get(id)) {
        accountRegistry.recordHealth(id, {
          loginStatus: session.loginStatus,
          pageLoaded: session.pageLoaded,
          evidence: session.evidence,
          pagePath: session.pagePath,
          checkedAt: session.checkedAt || Date.now()
        });
      }
      return session;
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
      await syncAccounts();
      const account = accountRegistry.get(id);
      if (!account) {
        const error = new Error('Account not found');
        error.code = 'ACCOUNT_NOT_FOUND';
        error.statusCode = 404;
        throw error;
      }
      const worker = workerScheduler.promoteDebug(id);
      await legacyHandlers.activateAccount(id);
      return { account, debug: worker, workers: workerScheduler.status() };
    },

    workerStatus: async () => ({
      ...workerScheduler.status(),
      runtimeBinding: 'foundation-only',
      note: 'F2 lease/worker policy is active as a control foundation. Real Dola BrowserWindow wake/sleep binding lands in F4/F5.'
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

require('./main');
