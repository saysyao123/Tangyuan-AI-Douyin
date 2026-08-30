'use strict';

const { app, BrowserWindow, ipcMain, session, webContents } = require('electron');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { startControlServer } = require('./control-server');
const { DolaBackgroundRunner } = require('./background-dola');

let mainWindow = null;
let controlRuntime = null;
let backgroundRunner = null;
const webviewTargets = new Map();
const backgroundMode = process.argv.includes('--background');
const experimentalBackground = process.argv.includes('--enable-experimental-dola')
  || process.env.DOLA_BACKGROUND_EXPERIMENTAL === '1';

function backgroundArtifactRoot() {
  return process.env.DOLA_ARTIFACT_ROOT
    || 'D:\\seedance2.5测试\\dola-original-resolver\\runtime\\desktop-captures';
}

function accountsPath() {
  return path.join(app.getPath('userData'), 'accounts.json');
}

function tasksPath() {
  return path.join(app.getPath('userData'), 'tasks.json');
}

function normalizeAccount(value) {
  if (!value || typeof value !== 'object') return null;
  const id = String(value.id || '').trim();
  if (!/^[a-zA-Z0-9_-]{6,80}$/.test(id)) return null;
  const name = String(value.name || 'Dola Account').replace(/[\r\n\t]/g, ' ').trim().slice(0, 80) || 'Dola Account';
  return {
    id,
    name,
    partition: `persist:dola_${id}`,
    createdAt: Number(value.createdAt) || Date.now(),
    status: String(value.status || 'UNKNOWN').toUpperCase().slice(0, 32),
    lastError: String(value.lastError || '').slice(0, 500),
    lastCheckedAt: Number(value.lastCheckedAt) || null
  };
}

function loadAccounts() {
  try {
    const parsed = JSON.parse(fs.readFileSync(accountsPath(), 'utf8'));
    if (!Array.isArray(parsed.accounts)) return [];
    return parsed.accounts.map(normalizeAccount).filter(Boolean);
  } catch (_) {
    return [];
  }
}

function saveAccounts(accounts) {
  const clean = accounts.map(normalizeAccount).filter(Boolean);
  fs.mkdirSync(path.dirname(accountsPath()), { recursive: true });
  fs.writeFileSync(accountsPath(), JSON.stringify({ accounts: clean }, null, 2), 'utf8');
  return clean;
}

function createAccount(name) {
  const accounts = loadAccounts();
  const account = normalizeAccount({
    id: crypto.randomUUID().replace(/-/g, ''),
    name,
    createdAt: Date.now(),
    status: 'NEEDS_LOGIN'
  });
  accounts.push(account);
  saveAccounts(accounts);
  emit('accounts:changed', accounts);
  return account;
}

async function clearAccountSession(accountId) {
  const account = loadAccounts().find(item => item.id === String(accountId || ''));
  if (!account) return false;
  const ses = session.fromPartition(account.partition);
  await ses.clearStorageData();
  await ses.clearCache();
  return true;
}

function deleteAccount(accountId) {
  const id = String(accountId || '');
  const before = loadAccounts();
  const account = before.find(item => item.id === id);
  const after = before.filter(item => item.id !== id);
  saveAccounts(after);
  emit('accounts:changed', after);
  return account || null;
}

function loadTasks() {
  try {
    const parsed = JSON.parse(fs.readFileSync(tasksPath(), 'utf8'));
    return Array.isArray(parsed.tasks) ? parsed.tasks.filter(Boolean) : [];
  } catch (_) {
    return [];
  }
}

function saveTasks(tasks) {
  fs.mkdirSync(path.dirname(tasksPath()), { recursive: true });
  fs.writeFileSync(tasksPath(), JSON.stringify({ tasks }, null, 2), 'utf8');
  emit('tasks:changed', tasks);
  return tasks;
}

function updateAccount(accountId, patch) {
  const id = String(accountId || '');
  const accounts = loadAccounts();
  const index = accounts.findIndex(item => item.id === id);
  if (index < 0) throw Object.assign(new Error('Unknown accountId.'), { statusCode: 404, code: 'account_not_found' });
  const allowed = {};
  if (patch && Object.prototype.hasOwnProperty.call(patch, 'status')) allowed.status = String(patch.status || 'UNKNOWN').toUpperCase().slice(0, 32);
  if (patch && Object.prototype.hasOwnProperty.call(patch, 'lastError')) allowed.lastError = String(patch.lastError || '').slice(0, 500);
  allowed.lastCheckedAt = Date.now();
  accounts[index] = normalizeAccount({ ...accounts[index], ...allowed });
  const saved = saveAccounts(accounts);
  emit('accounts:changed', saved);
  return saved[index];
}

function patchTask(taskId, patch) {
  const id = String(taskId || '');
  const tasks = loadTasks();
  const index = tasks.findIndex(item => item.id === id);
  if (index < 0) throw Object.assign(new Error('Unknown taskId.'), { statusCode: 404, code: 'task_not_found' });
  tasks[index] = { ...tasks[index], ...(patch || {}), updatedAt: Date.now() };
  saveTasks(tasks);
  return tasks[index];
}

function listProviders() {
  return [
    {
      id: 'dola-web',
      label: 'Dola Web',
      state: 'experimental',
      dispatchReady: false,
      gate: 'D2',
      capabilities: { t2v: true, i2v: 'unknown', durationSeconds: [10, 30] },
      note: 'Account/session control is ready. Automatic Seedance submission stays disabled until the real D2 request lifecycle is observed and verified.'
    },
    {
      id: 'dola-web-background',
      label: 'Dola Web · Hidden Background (Experimental)',
      state: experimentalBackground && backgroundMode ? 'experimental-ready' : 'experimental',
      dispatchReady: experimentalBackground && backgroundMode,
      gate: 'D2_BACKGROUND_OBSERVE',
      capabilities: { t2v: true, i2v: true, durationSeconds: [5, 10, 30] },
      note: 'Uses one hidden Electron BrowserWindow per account persistent partition. Each account needs a one-time manual login in the desktop manager; no passwords or tokens are stored.'
    },
    {
      id: 'byteplus-seedance',
      label: 'BytePlus Seedance',
      state: 'planned',
      dispatchReady: false,
      gate: 'provider-config',
      capabilities: { t2v: true, i2v: true, durationRangeSeconds: [4, 30] },
      note: 'Official provider adapter placeholder; API credential configuration is not implemented in this branch.'
    }
  ];
}

function badRequest(message) {
  return Object.assign(new Error(message), { statusCode: 400, code: 'bad_request' });
}

function normalizeTask(input) {
  if (!input || typeof input !== 'object') throw badRequest('Task body is required.');
  const accountId = String(input.accountId || '').trim();
  if (!loadAccounts().some(item => item.id === accountId)) throw badRequest('Unknown accountId.');
  const prompt = String(input.prompt || '').trim();
  if (!prompt || prompt.length > 20000) throw badRequest('prompt must contain 1-20000 characters.');
  const duration = Number(input.duration || 10);
  if (!Number.isInteger(duration) || duration < 4 || duration > 30) throw badRequest('duration must be an integer from 4 to 30 seconds.');
  const ratio = String(input.ratio || '9:16').trim();
  if (!/^\d{1,3}:\d{1,3}$/.test(ratio)) throw badRequest('ratio must look like 9:16 or 16:9.');
  const mode = String(input.mode || 't2v');
  if (!['t2v', 'i2v', 'multi'].includes(mode)) throw badRequest('mode must be t2v, i2v, or multi.');
  const provider = String(input.provider || 'dola-web');
  if (!listProviders().some(item => item.id === provider)) throw badRequest('Unknown provider.');
  const imagePath = String(input.imagePath || '').trim();
  if (imagePath && (!path.isAbsolute(imagePath) || imagePath.length > 2000)) throw badRequest('imagePath must be an absolute local path.');
  if (imagePath && !fs.existsSync(imagePath)) throw badRequest('imagePath does not exist.');
  if (mode === 'i2v' && !imagePath) throw badRequest('imagePath is required for i2v tasks.');
  const now = Date.now();
  return {
    id: crypto.randomUUID().replace(/-/g, ''),
    accountId,
    provider,
    mode,
    model: String(input.model || 'seedance-v2.5').slice(0, 120),
    duration,
    ratio,
    prompt,
    imagePath: imagePath || null,
    state: 'queued',
    blockedReason: provider === 'dola-web'
      ? 'D2_GATE_NOT_PASSED'
      : provider === 'dola-web-background' && experimentalBackground && backgroundMode
        ? null
        : provider === 'dola-web-background' ? 'BACKGROUND_PROVIDER_DISABLED' : 'PROVIDER_NOT_CONFIGURED',
    createdAt: now,
    updatedAt: now
  };
}

function createTask(input) {
  const tasks = loadTasks();
  const task = normalizeTask(input);
  tasks.unshift(task);
  saveTasks(tasks.slice(0, 1000));
  return task;
}

function getTask(id) {
  return loadTasks().find(item => item.id === String(id || '')) || null;
}

function cancelTask(id) {
  const tasks = loadTasks();
  const index = tasks.findIndex(item => item.id === String(id || ''));
  if (index < 0) return null;
  const task = tasks[index];
  if (['success', 'failed', 'cancelled'].includes(task.state)) return task;
  tasks[index] = { ...task, state: 'cancelled', blockedReason: null, updatedAt: Date.now() };
  saveTasks(tasks);
  return tasks[index];
}

async function dispatchTask(id) {
  const task = getTask(id);
  if (!task) return { ok: false, statusCode: 404, error: 'task_not_found' };
  const provider = listProviders().find(item => item.id === task.provider);
  if (task.provider === 'dola-web-background') {
    if (!provider || provider.dispatchReady !== true || !backgroundRunner) {
      return {
        ok: false,
        statusCode: 409,
        error: 'DOLA_BACKGROUND_DISABLED',
        message: 'Start the desktop control plane with --background --enable-experimental-dola before dispatching background tasks.',
        task
      };
    }
    if (['running', 'capture_armed', 'generation_running'].includes(task.state)) {
      return { ok: true, statusCode: 200, message: 'background task already running', task };
    }
    const account = loadAccounts().find(item => item.id === task.accountId);
    if (!account) return { ok: false, statusCode: 404, error: 'account_not_found', task };
    const running = patchTask(task.id, {
      state: 'running',
      blockedReason: null,
      startedAt: Date.now(),
      error: null
    });
    backgroundRunner.run(running, account).catch(async (error) => {
      const message = String(error.message || error).slice(0, 500);
      try { patchTask(running.id, { state: 'failed', error: message }); } catch (_) {}
      try { updateAccount(account.id, { status: 'READY', lastError: message }); } catch (_) {}
    });
    return { ok: true, statusCode: 202, message: 'background task accepted', task: running };
  }
  if (!provider || provider.dispatchReady !== true) {
    return {
      ok: false,
      statusCode: 409,
      error: task.provider === 'dola-web' ? 'D2_GATE_NOT_PASSED' : 'PROVIDER_NOT_CONFIGURED',
      message: task.provider === 'dola-web'
        ? 'Dola automatic submission is intentionally blocked until the D2 10s baseline lifecycle is observed and verified on the user session.'
        : 'This provider is not configured yet.',
      task
    };
  }
  return { ok: false, statusCode: 501, error: 'provider_dispatch_not_implemented', task };
}

function emit(channel, payload) {
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send(channel, payload);
}

function activateAccount(id) {
  const account = loadAccounts().find(item => item.id === String(id || ''));
  if (!account) throw Object.assign(new Error('Unknown accountId.'), { statusCode: 404, code: 'account_not_found' });
  emit('control:activate-account', account.id);
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.show();
  return account;
}

function registerWebview(accountId, guestId) {
  const account = loadAccounts().find(item => item.id === String(accountId || ''));
  const numericGuestId = Number(guestId);
  if (!account || !Number.isInteger(numericGuestId) || numericGuestId <= 0) return false;
  webviewTargets.set(account.id, { guestId: numericGuestId, registeredAt: Date.now() });
  return true;
}

async function sessionStatus(accountId) {
  const id = String(accountId || '');
  const account = loadAccounts().find(item => item.id === id);
  if (!account) throw Object.assign(new Error('Unknown accountId'), { statusCode: 404, code: 'account_not_found' });
  const target = webviewTargets.get(id);
  if (!target) {
    if (backgroundMode && backgroundRunner) {
      const status = await backgroundRunner.sessionStatus(account);
      if (status.loginStatus === 'logged_in') updateAccount(id, { status: 'READY', lastError: '' });
      if (status.loginStatus === 'logged_out') updateAccount(id, { status: 'NEEDS_LOGIN' });
      return { accountId: id, ...status, checkedAt: Date.now() };
    }
    return { accountId: id, loginStatus: 'unknown', pageLoaded: false, evidence: 'webview_not_registered' };
  }
  const guest = webContents.fromId(target.guestId);
  if (!guest || guest.isDestroyed()) {
    return { accountId: id, loginStatus: 'unknown', pageLoaded: false, evidence: 'webview_unavailable' };
  }
  const pageUrl = guest.getURL();
  try {
    const snapshot = await guest.executeJavaScript(`(() => {
      const text = String(document.body?.innerText || '').slice(0, 200000);
      const normalized = text.toLowerCase();
      const loginPath = /\\/(login|signin|sign-in)(\\/|$)/i.test(location.pathname);
      const logoutSignal = /(退出登录|退出账号|log out|logout|sign out|signout)/i.test(normalized);
      const loginSignal = /(登录|log in|signin|sign in)/i.test(normalized);
      let loginStatus = 'unknown';
      let evidence = 'ambiguous_page';
      if (logoutSignal) {
        loginStatus = 'logged_in';
        evidence = 'logout_action_present';
      } else if (loginPath || loginSignal) {
        loginStatus = 'logged_out';
        evidence = loginPath ? 'login_path' : 'login_action_present';
      }
      return {
        loginStatus,
        pageLoaded: document.readyState === 'complete',
        evidence,
        pagePath: location.origin + location.pathname
      };
    })()`, true);
    return {
      accountId: id,
      loginStatus: snapshot.loginStatus || 'unknown',
      pageLoaded: snapshot.pageLoaded === true,
      evidence: String(snapshot.evidence || 'unknown'),
      pagePath: String(snapshot.pagePath || '').slice(0, 500),
      checkedAt: Date.now()
    };
  } catch (_) {
    return {
      accountId: id,
      loginStatus: 'unknown',
      pageLoaded: false,
      evidence: 'page_inspection_failed',
      pagePath: `${pageUrl.split('?')[0].split('#')[0]}`.slice(0, 500),
      checkedAt: Date.now()
    };
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1560,
    height: 920,
    minWidth: 1180,
    minHeight: 700,
    title: 'Seedance Desktop Studio',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      webviewTag: true,
      sandbox: false
    }
  });
  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

function registerIpc() {
  ipcMain.handle('accounts:list', () => loadAccounts());
  ipcMain.handle('accounts:add', (_event, name) => createAccount(name));
  ipcMain.handle('accounts:remove', async (_event, id, clearSession) => {
    if (clearSession === true) await clearAccountSession(id);
    return deleteAccount(id);
  });
  ipcMain.handle('accounts:clear-session', (_event, id) => clearAccountSession(id));
  ipcMain.handle('accounts:activate', (_event, id) => activateAccount(id));
  ipcMain.on('webview:registered', (_event, payload) => {
    if (payload && typeof payload === 'object') registerWebview(payload.accountId, payload.guestId);
  });
  ipcMain.handle('accounts:session-status', (_event, id) => sessionStatus(id));
  ipcMain.handle('providers:list', () => listProviders());
  ipcMain.handle('tasks:list', () => loadTasks());
  ipcMain.handle('tasks:create', (_event, input) => createTask(input));
  ipcMain.handle('tasks:get', (_event, id) => getTask(id));
  ipcMain.handle('tasks:cancel', (_event, id) => cancelTask(id));
  ipcMain.handle('tasks:dispatch', (_event, id) => dispatchTask(id));
}

async function startCodexControlPlane() {
  controlRuntime = await startControlServer({
    health: async () => ({
      ok: true,
      service: 'seedance-desktop-studio',
      version: 1,
      pid: process.pid,
      gates: { D0: 'implemented-not-user-verified', D1: 'pending-user-test', D2: 'pending', D3: 'pending' }
    }),
    listAccounts: async () => loadAccounts(),
    getAccountSession: async (id) => sessionStatus(id),
    createAccount: async (name) => createAccount(name),
    activateAccount: async (id) => activateAccount(id),
    listProviders: async () => listProviders(),
    listTasks: async () => loadTasks(),
    createTask: async (input) => createTask(input),
    getTask: async (id) => getTask(id),
    cancelTask: async (id) => cancelTask(id),
    dispatchTask: async (id) => dispatchTask(id)
  });
  console.log(`[Seedance Desktop] Codex control plane: http://${controlRuntime.info.host}:${controlRuntime.info.port}`);
}

app.whenReady().then(async () => {
  registerIpc();
  if (!backgroundMode) createWindow();
  backgroundRunner = new DolaBackgroundRunner({
    outputRoot: backgroundArtifactRoot(),
    getAccount: (id) => loadAccounts().find(item => item.id === String(id || '')) || null,
    updateTask: patchTask,
    updateAccount
  });
  await startCodexControlPlane();
  app.on('activate', () => {
    if (!backgroundMode && BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('before-quit', () => {
  if (controlRuntime) controlRuntime.stop().catch(() => {});
  if (backgroundRunner) backgroundRunner.close().catch(() => {});
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
