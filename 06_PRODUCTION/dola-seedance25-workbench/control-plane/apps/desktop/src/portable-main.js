'use strict';

const { app } = require('electron');
const {
  LAYOUT_VERSION,
  resolvePortableRoot,
  buildPortableLayout,
  ensurePortableLayout
} = require('./core/portable-paths');
const { ProjectStore } = require('./core/project-store');

const root = resolvePortableRoot({
  env: process.env,
  execPath: process.execPath,
  isPackaged: app.isPackaged,
  moduleDir: __dirname
});
const layout = buildPortableLayout(root);
ensurePortableLayout(layout);

// Keep the current POC implementation working while moving all runtime data
// under the portable root. F1/F3 will split durable metadata from encrypted
// profile material without changing the public Control Plane contract.
app.setPath('userData', layout.electronUserData);

process.env.DOLA_WORKBENCH_ROOT = layout.root;
process.env.DOLA_WORKBENCH_DATA_ROOT = layout.dataDir;
process.env.DOLA_WORKBENCH_LAYOUT_VERSION = String(LAYOUT_VERSION);
process.env.SEEDANCE_STUDIO_CONTROL_DIR = layout.controlDir;
process.env.DOLA_ARTIFACT_ROOT = layout.debugCapturesDir;

// Portable V1 adds capabilities around the existing POC without forcing a
// high-risk rewrite of main.js in the first foundation Gate. Patch the cached
// control-server export before main.js imports it, so legacy task/account
// handlers stay intact while projects/jobs use the new durable store.
const projectStore = new ProjectStore(layout);
const controlServer = require('./control-server');
const originalStartControlServer = controlServer.startControlServer;
controlServer.startControlServer = async function startPortableControlServer(legacyHandlers) {
  const handlers = {
    ...legacyHandlers,
    health: async () => ({
      ...(await legacyHandlers.health()),
      portable: {
        enabled: true,
        layoutVersion: LAYOUT_VERSION,
        projects: projectStore.listProjects().length
      }
    }),
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
