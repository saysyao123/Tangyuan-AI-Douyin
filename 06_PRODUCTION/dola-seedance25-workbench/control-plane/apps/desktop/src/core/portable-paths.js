'use strict';

const fs = require('node:fs');
const path = require('node:path');

const LAYOUT_VERSION = 1;

function resolvePortableRoot(options = {}) {
  const env = options.env || process.env;
  const moduleDir = path.resolve(options.moduleDir || __dirname);
  const execPath = path.resolve(options.execPath || process.execPath);
  const isPackaged = options.isPackaged === true;

  if (env.DOLA_WORKBENCH_ROOT) return path.resolve(String(env.DOLA_WORKBENCH_ROOT));
  if (env.PORTABLE_EXECUTABLE_DIR) return path.resolve(String(env.PORTABLE_EXECUTABLE_DIR));
  if (isPackaged) return path.dirname(execPath);
  return path.resolve(moduleDir, '..', '..', '.portable-dev');
}

function buildPortableLayout(rootValue) {
  const root = path.resolve(rootValue);
  const appDir = path.join(root, 'app');
  const runtimeDir = path.join(root, 'runtime');
  const dataDir = path.join(root, 'data');
  const unlockedProfilesDir = path.join(runtimeDir, 'unlocked-profiles');

  return {
    version: LAYOUT_VERSION,
    root,
    appDir,
    runtimeDir,
    dataDir,
    controlDir: path.join(runtimeDir, 'control'),
    tempDir: path.join(runtimeDir, 'tmp'),
    unlockedProfilesDir,
    // Electron's live browser-session root is runtime-only but deliberately
    // separate from vault scratch space. Manual vault lock can wipe scratch
    // keys/workdirs without deleting the main window's default session while
    // the process is still alive. Per-account Partitions are resealed/deleted
    // by ElectronProfileBridge.
    sessionDataDir: path.join(runtimeDir, 'session-data'),
    vaultWorkingDir: path.join(unlockedProfilesDir, 'vault-work'),
    vaultDir: path.join(dataDir, 'vault'),
    profilesDir: path.join(dataDir, 'profiles'),
    electronUserData: path.join(dataDir, 'profiles', 'electron-user-data'),
    accountsDir: path.join(dataDir, 'accounts'),
    projectsDir: path.join(dataDir, 'projects'),
    outputsDir: path.join(dataDir, 'outputs'),
    stateDir: path.join(dataDir, 'state'),
    logsDir: path.join(dataDir, 'logs'),
    backupsDir: path.join(dataDir, 'backups'),
    debugDir: path.join(dataDir, 'debug'),
    debugCapturesDir: path.join(dataDir, 'debug', 'captures'),
    layoutMarker: path.join(dataDir, 'state', 'layout.json')
  };
}

function directoryList(layout) {
  return [
    layout.runtimeDir,
    layout.controlDir,
    layout.tempDir,
    layout.unlockedProfilesDir,
    layout.sessionDataDir,
    layout.vaultWorkingDir,
    layout.dataDir,
    layout.vaultDir,
    layout.profilesDir,
    layout.electronUserData,
    layout.accountsDir,
    layout.projectsDir,
    layout.outputsDir,
    layout.stateDir,
    layout.logsDir,
    layout.backupsDir,
    layout.debugDir,
    layout.debugCapturesDir
  ];
}

function ensurePortableLayout(layout) {
  for (const dir of directoryList(layout)) fs.mkdirSync(dir, { recursive: true });

  let current = null;
  try { current = JSON.parse(fs.readFileSync(layout.layoutMarker, 'utf8')); } catch (_) {}

  if (current && Number(current.version) > LAYOUT_VERSION) {
    const error = new Error(`Portable data layout v${current.version} is newer than this app supports (v${LAYOUT_VERSION}).`);
    error.code = 'PORTABLE_LAYOUT_TOO_NEW';
    throw error;
  }

  const marker = {
    version: LAYOUT_VERSION,
    rootKind: 'dola-workbench-portable',
    createdAt: Number(current?.createdAt) || Date.now(),
    updatedAt: Date.now()
  };
  const partial = `${layout.layoutMarker}.part`;
  fs.writeFileSync(partial, `${JSON.stringify(marker, null, 2)}\n`, 'utf8');
  fs.renameSync(partial, layout.layoutMarker);
  return marker;
}

module.exports = {
  LAYOUT_VERSION,
  resolvePortableRoot,
  buildPortableLayout,
  ensurePortableLayout
};
