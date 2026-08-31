'use strict';

const { app, BrowserWindow, dialog, ipcMain, session, webContents } = require('electron');
const path = require('node:path');
const fs = require('node:fs');
const { readJson } = require('./core/atomic-json');
const { requirePortableRuntime } = require('./core/portable-runtime');
const { rekeyVaultPassword } = require('./core/vault-rekey');

let registered = false;
let allowQuit = false;
let shutdownPromise = null;

function legacyAccounts(runtime) {
  const file = path.join(runtime.layout.electronUserData, 'accounts.json');
  const parsed = readJson(file, { accounts: [] }) || { accounts: [] };
  return Array.isArray(parsed.accounts) ? parsed.accounts.filter(Boolean) : [];
}

function legacyTasks(runtime) {
  const file = path.join(runtime.layout.electronUserData, 'tasks.json');
  const parsed = readJson(file, { tasks: [] }) || { tasks: [] };
  return Array.isArray(parsed.tasks) ? parsed.tasks.filter(Boolean) : [];
}

function syncAccountRegistry(runtime) {
  return runtime.accountRegistry.syncLegacy(legacyAccounts(runtime));
}

function accountById(runtime, id) {
  syncAccountRegistry(runtime);
  return runtime.accountRegistry.get(String(id || '')) || null;
}

function vaultPublicStatus(runtime) {
  const status = runtime.vault.status();
  return {
    ...status,
    desktopUnlockRequired: !['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state),
    profileRuntimeBinding: 'experimental-f3',
    codexCanUnlock: false,
    defaultPasswordActive: runtime.defaultPasswordActive === true
  };
}

async function flushAccountSessions(accounts) {
  const results = [];
  for (const account of accounts) {
    try {
      const ses = session.fromPartition(account.partition);
      if (typeof ses.flushStorageData === 'function') await ses.flushStorageData();
      results.push({ accountId: account.id, flushed: true });
    } catch (error) {
      results.push({ accountId: account.id, flushed: false, error: String(error.message || error).slice(0, 160) });
    }
  }
  return results;
}

function resealFailures(items) {
  return items.filter((item) => item.resealed === false && item.reason !== 'not-dirty');
}

async function resealForShutdown(runtime) {
  const status = runtime.vault.status();
  if (!['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state)) return { skipped: true, reason: 'vault-not-unlocked' };
  const accounts = syncAccountRegistry(runtime);
  const flushBefore = await flushAccountSessions(accounts);
  for (const win of BrowserWindow.getAllWindows()) {
    try { win.destroy(); } catch (_) {}
  }
  await new Promise((resolve) => setTimeout(resolve, 300));
  const flushAfter = await flushAccountSessions(accounts);
  const resealed = runtime.profileBridge.resealDirty(accounts);
  const failures = resealFailures(resealed);
  if (failures.length) {
    const error = new Error(`Could not reseal ${failures.length} account profile(s) before exit.`);
    error.code = 'PROFILE_RESEAL_FAILED';
    error.failures = failures;
    throw error;
  }
  const vault = runtime.vault.lock();
  return { skipped: false, flushBefore, flushAfter, resealed, vault };
}

async function closeAndResealActiveProfiles(runtime) {
  const accounts = syncAccountRegistry(runtime);
  const flushed = await flushAccountSessions(accounts);
  await new Promise((resolve) => setTimeout(resolve, 250));
  const resealed = runtime.profileBridge.resealDirty(accounts);
  const failures = resealFailures(resealed);
  if (failures.length) {
    const error = new Error('One or more account profiles could not be resealed. Close Dola worker/debug windows and retry.');
    error.code = 'PROFILE_RESEAL_FAILED';
    error.failures = failures;
    throw error;
  }
  return { accounts, flushed, resealed };
}

function controlDiscoveryFile(runtime) {
  return path.join(runtime.layout.controlDir, 'SeedanceDesktopStudio', 'control.json');
}

async function localControlRequest(runtime, method, route, body) {
  const file = controlDiscoveryFile(runtime);
  if (!fs.existsSync(file)) {
    const error = new Error('Local Control Plane is not ready yet.');
    error.code = 'CONTROL_PLANE_NOT_READY';
    throw error;
  }
  const discovery = JSON.parse(fs.readFileSync(file, 'utf8'));
  const response = await fetch(`http://127.0.0.1:${discovery.port}${route}`, {
    method,
    headers: {
      authorization: `Bearer ${discovery.token}`,
      ...(body === undefined ? {} : { 'content-type': 'application/json' })
    },
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok && response.status !== 202) {
    const error = new Error(payload.message || payload.error || `HTTP ${response.status}`);
    error.code = payload.error || 'LOCAL_CONTROL_ERROR';
    error.statusCode = response.status;
    throw error;
  }
  return payload;
}

function isDolaWebContents(item) {
  if (!item || item.isDestroyed()) return false;
  try {
    const url = new URL(item.getURL());
    return url.protocol === 'https:' && ['dola.com', 'www.dola.com'].includes(url.hostname.toLowerCase());
  } catch (_) {
    return false;
  }
}

function visibleDolaWebview(account) {
  const expectedSession = session.fromPartition(account.partition);
  const candidates = webContents.getAllWebContents()
    .filter((item) => {
      try {
        return item.getType() === 'webview'
          && item.session === expectedSession
          && isDolaWebContents(item);
      } catch (_) {
        return false;
      }
    })
    .sort((a, b) => Number(b.id || 0) - Number(a.id || 0));
  return candidates[0] || null;
}

async function inspectVisibleDolaLogin(page) {
  return page.executeJavaScript(`(() => {
    const body = String(document.body?.innerText || '').slice(0, 180000);
    const lower = body.toLowerCase();
    const pathname = String(location.pathname || '');
    const visible = (el) => !!el && !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    const hasEditor = Array.from(document.querySelectorAll('textarea:not([disabled]),[contenteditable],[role="textbox"],[aria-label="doc_editor"]')).some(visible);
    const logoutSignal = /(退出登录|退出账号|log out|logout|sign out|signout)/i.test(lower);
    const loginSignal = /(登录|log in|signin|sign in)/i.test(lower);
    const loginPath = /\\/(login|signin|sign-in)(\\/|$)/i.test(pathname);
    const loggedIn = hasEditor || logoutSignal;
    const loggedOut = !loggedIn && (loginPath || !!document.querySelector('input[type="password"]') || loginSignal);
    return {
      loginStatus: loggedIn ? 'logged_in' : loggedOut ? 'logged_out' : 'unknown',
      pageLoaded: document.readyState === 'complete',
      evidence: hasEditor ? 'visible_editor_present' : logoutSignal ? 'visible_logout_action_present' : loginPath ? 'visible_login_path' : loginSignal ? 'visible_login_action_present' : 'visible_page_ambiguous',
      pagePath: location.origin + pathname
    };
  })()`, true);
}

function externalVisibleSlot(account, page) {
  return {
    accountId: account.id,
    window: {
      isDestroyed: () => page.isDestroyed(),
      destroy: () => {}
    },
    page,
    childWindows: [],
    debugger: null,
    capture: null,
    externalVisibleWebview: true
  };
}

async function dispatchVisibleTask(runtime, taskId) {
  const id = String(taskId || '');
  const task = legacyTasks(runtime).find((item) => item.id === id) || null;
  if (!task) {
    const error = new Error('Task not found');
    error.code = 'TASK_NOT_FOUND';
    error.statusCode = 404;
    throw error;
  }
  if (task.state === 'success') return { ok: true, statusCode: 200, message: 'task already completed', task };
  if (task.state === 'cancelled') {
    const error = new Error('Task is cancelled');
    error.code = 'TASK_CANCELLED';
    error.statusCode = 409;
    throw error;
  }
  if (['running', 'capture_armed', 'generation_running', 'resolving'].includes(task.state) || runtime.workerScheduler.isJobLeased(task.id)) {
    return { ok: true, statusCode: 200, message: 'task already running', task };
  }

  let account = accountById(runtime, task.accountId);
  if (!account) {
    const error = new Error('Account not found');
    error.code = 'ACCOUNT_NOT_FOUND';
    error.statusCode = 404;
    throw error;
  }
  const page = visibleDolaWebview(account);
  if (!page) {
    const error = new Error('The selected account does not currently have a visible Dola page.');
    error.code = 'VISIBLE_DOLA_VIEW_NOT_READY';
    error.statusCode = 409;
    throw error;
  }

  const health = await inspectVisibleDolaLogin(page).catch(() => ({ loginStatus: 'unknown', pageLoaded: false, evidence: 'visible_login_inspection_failed', pagePath: '' }));
  runtime.accountRegistry.recordHealth(account.id, { ...health, checkedAt: Date.now() });
  account = runtime.accountRegistry.get(account.id);
  if (health.loginStatus === 'logged_out') {
    const error = new Error('The visible Dola page is logged out. Complete manual login in the center page first.');
    error.code = 'LOGIN_REQUIRED';
    error.statusCode = 409;
    throw error;
  }
  if (health.loginStatus !== 'logged_in') {
    const error = new Error('The visible Dola login state could not be confirmed. Use the center page or “检查登录” first.');
    error.code = 'LOGIN_STATE_UNKNOWN';
    error.statusCode = 409;
    throw error;
  }

  const runner = runtime.backgroundRunner;
  if (!runner || typeof runner.run !== 'function' || !runner.slots) {
    const error = new Error('Portable Dola runner is not ready yet.');
    error.code = 'PROVIDER_RUNTIME_NOT_READY';
    error.statusCode = 503;
    throw error;
  }

  const leaseResult = runtime.workerScheduler.acquire({ ...task, accountId: account.id }, [account]);
  const previousSlot = runner.slots.get(account.id) || null;
  const visibleSlot = externalVisibleSlot(account, page);
  runner.slots.set(account.id, visibleSlot);

  let runningTask = task;
  try {
    if (typeof runner.directUpdateTask === 'function') {
      runningTask = await runner.directUpdateTask(task.id, {
        state: 'running',
        blockedReason: null,
        startedAt: task.startedAt || Date.now(),
        executionSurface: 'visible-webview',
        error: null,
        updatedAt: Date.now()
      });
    }
  } catch (error) {
    runner.slots.delete(account.id);
    if (previousSlot) runner.slots.set(account.id, previousSlot);
    runtime.workerScheduler.release(leaseResult.lease.jobId);
    throw error;
  }

  Promise.resolve()
    .then(() => runner.run(runningTask, account))
    .catch(async (error) => {
      const message = String(error.message || error).slice(0, 500);
      try {
        if (typeof runner.directUpdateTask === 'function') {
          await runner.directUpdateTask(task.id, { state: 'failed', error: message, updatedAt: Date.now() });
        }
      } catch (_) {}
    })
    .finally(() => {
      const current = runner.slots.get(account.id);
      if (current === visibleSlot) {
        runner.slots.delete(account.id);
        try {
          if (previousSlot && !previousSlot.window.isDestroyed()) runner.slots.set(account.id, previousSlot);
        } catch (_) {}
      }
      runtime.workerScheduler.release(leaseResult.lease.jobId);
    });

  return {
    ok: true,
    statusCode: 202,
    message: '任务已交给中间可见 Dola 页面执行；你可以直接看到模型、时长、首帧、Prompt 与提交过程。',
    task: { ...runningTask, state: 'running', executionSurface: 'visible-webview' }
  };
}

function registerPortableIpc() {
  if (registered) return;
  registered = true;

  ipcMain.handle('vault:status', () => vaultPublicStatus(requirePortableRuntime()));
  ipcMain.handle('vault:initialize', (_event, password) => {
    const runtime = requirePortableRuntime();
    runtime.vault.initialize(String(password || ''));
    runtime.defaultPasswordActive = false;
    return vaultPublicStatus(runtime);
  });
  ipcMain.handle('vault:unlock', (_event, password) => {
    const runtime = requirePortableRuntime();
    runtime.vault.unlock(String(password || ''));
    return vaultPublicStatus(runtime);
  });
  ipcMain.handle('vault:change-password', async (_event, input) => {
    const runtime = requirePortableRuntime();
    const currentPassword = String(input?.currentPassword || '');
    const newPassword = String(input?.newPassword || '');
    await closeAndResealActiveProfiles(runtime);
    const result = rekeyVaultPassword(runtime.vault, runtime.layout, currentPassword, newPassword);
    runtime.defaultPasswordActive = false;
    return { ...result, vault: vaultPublicStatus(runtime) };
  });
  ipcMain.handle('profiles:prepare-account', (_event, accountId) => {
    const runtime = requirePortableRuntime();
    const account = accountById(runtime, accountId);
    if (!account) {
      const error = new Error('Account not found');
      error.code = 'ACCOUNT_NOT_FOUND';
      error.statusCode = 404;
      throw error;
    }
    const result = runtime.profileBridge.prepare(account);
    return { ...result, vault: vaultPublicStatus(runtime) };
  });
  ipcMain.handle('vault:lock', async () => {
    const runtime = requirePortableRuntime();
    const { resealed } = await closeAndResealActiveProfiles(runtime);
    runtime.vault.lock();
    return { vault: vaultPublicStatus(runtime), resealed };
  });

  // Renderer never receives the loopback bearer token. These local IPC calls
  // proxy into the same Portable Control Plane used by Codex so desktop and
  // automation cannot diverge on scheduling/recovery semantics. When the
  // desktop has the matching account visible, the primary submit action uses
  // that exact WebView first. This keeps G1 aligned with the page the user has
  // already verified manually, while Codex/API dispatch remains background.
  ipcMain.handle('portable:dispatch-task', async (_event, id) => {
    const runtime = requirePortableRuntime();
    try {
      return await dispatchVisibleTask(runtime, id);
    } catch (error) {
      if (error?.code !== 'VISIBLE_DOLA_VIEW_NOT_READY') throw error;
      return localControlRequest(runtime, 'POST', `/v1/tasks/${encodeURIComponent(String(id || ''))}/dispatch`, {});
    }
  });
  ipcMain.handle('portable:recover-task', (_event, id) => {
    const runtime = requirePortableRuntime();
    return localControlRequest(runtime, 'POST', `/v1/tasks/${encodeURIComponent(String(id || ''))}/recover`, {});
  });

  app.on('before-quit', (event) => {
    if (allowQuit) return;
    const runtime = requirePortableRuntime();
    const status = runtime.vault.status();
    if (!['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state)) return;

    event.preventDefault();
    if (shutdownPromise) return;
    shutdownPromise = resealForShutdown(runtime)
      .then(() => {
        allowQuit = true;
        app.quit();
      })
      .catch((error) => {
        shutdownPromise = null;
        const detail = Array.isArray(error.failures)
          ? `\n\n${error.failures.map((item) => `${item.accountId}: ${item.error || item.reason}`).join('\n')}`
          : '';
        dialog.showErrorBox(
          'DolaWorkbench 无法安全退出',
          `账号登录态加密回收失败。为了避免把未加密的会话误标为已安全保存，本次退出已被阻止。\n\n${error.message || error}${detail}`
        );
      });
  });
}

module.exports = {
  registerPortableIpc,
  vaultPublicStatus,
  legacyAccounts,
  legacyTasks,
  visibleDolaWebview,
  dispatchVisibleTask,
  resealForShutdown,
  closeAndResealActiveProfiles,
  localControlRequest
};
