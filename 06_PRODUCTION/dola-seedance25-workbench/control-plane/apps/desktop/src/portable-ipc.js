'use strict';

const { app, BrowserWindow, dialog, ipcMain, session } = require('electron');
const path = require('node:path');
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
  // The renderer closes its visible WebView before calling password change or
  // lock. Hidden workers must also release their account windows before a real
  // Windows rekey Gate; if they do not, bridge cleanup fails closed.
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
  resealForShutdown,
  closeAndResealActiveProfiles
};
