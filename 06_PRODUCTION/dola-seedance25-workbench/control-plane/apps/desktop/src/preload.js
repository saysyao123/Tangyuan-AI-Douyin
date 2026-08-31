'use strict';

const { contextBridge, ipcRenderer } = require('electron');

function subscribe(channel, callback) {
  const listener = (_event, payload) => callback(payload);
  ipcRenderer.on(channel, listener);
  return () => ipcRenderer.removeListener(channel, listener);
}

contextBridge.exposeInMainWorld('seedanceDesktop', {
  getVaultStatus: () => ipcRenderer.invoke('vault:status'),
  initializeVault: (password) => ipcRenderer.invoke('vault:initialize', String(password || '')),
  unlockVault: (password) => ipcRenderer.invoke('vault:unlock', String(password || '')),
  changeVaultPassword: (currentPassword, newPassword) => ipcRenderer.invoke('vault:change-password', {
    currentPassword: String(currentPassword || ''),
    newPassword: String(newPassword || '')
  }),
  lockVault: () => ipcRenderer.invoke('vault:lock'),
  prepareAccountSession: (id) => ipcRenderer.invoke('profiles:prepare-account', String(id || '')),

  listAccounts: () => ipcRenderer.invoke('accounts:list'),
  addAccount: (name) => ipcRenderer.invoke('accounts:add', String(name || '')),
  removeAccount: (id, clearSession = false) => ipcRenderer.invoke('accounts:remove', String(id || ''), clearSession === true),
  clearAccountSession: (id) => ipcRenderer.invoke('accounts:clear-session', String(id || '')),
  activateAccount: (id) => ipcRenderer.invoke('accounts:activate', String(id || '')),
  registerWebview: (accountId, guestId) => ipcRenderer.send('webview:registered', { accountId: String(accountId || ''), guestId: Number(guestId) }),
  getAccountSessionStatus: (id) => ipcRenderer.invoke('accounts:session-status', String(id || '')),
  listProviders: () => ipcRenderer.invoke('providers:list'),
  listTasks: () => ipcRenderer.invoke('tasks:list'),
  createTask: (input) => ipcRenderer.invoke('tasks:create', input || {}),
  getTask: (id) => ipcRenderer.invoke('tasks:get', String(id || '')),
  cancelTask: (id) => ipcRenderer.invoke('tasks:cancel', String(id || '')),
  dispatchTask: (id) => ipcRenderer.invoke('tasks:dispatch', String(id || '')),
  onActivateAccount: (callback) => subscribe('control:activate-account', callback),
  onAccountsChanged: (callback) => subscribe('accounts:changed', callback),
  onTasksChanged: (callback) => subscribe('tasks:changed', callback)
});
