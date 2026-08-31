'use strict';

const accountsEl = document.getElementById('accounts');
const webviewsEl = document.getElementById('webviews');
const emptyEl = document.getElementById('empty');
const addButton = document.getElementById('addAccount');
const reloadButton = document.getElementById('reload');
const clearButton = document.getElementById('clearSession');
const lockButton = document.getElementById('lockVault');
const activeNameEl = document.getElementById('activeName');
const statusEl = document.getElementById('status');
const taskForm = document.getElementById('taskForm');
const providerEl = document.getElementById('provider');
const durationEl = document.getElementById('duration');
const ratioEl = document.getElementById('ratio');
const promptEl = document.getElementById('prompt');
const queueTaskButton = document.getElementById('queueTask');
const tasksEl = document.getElementById('tasks');
const taskCountEl = document.getElementById('taskCount');
const refreshTasksButton = document.getElementById('refreshTasks');

const vaultGate = document.getElementById('vaultGate');
const vaultForm = document.getElementById('vaultForm');
const vaultTitle = document.getElementById('vaultTitle');
const vaultDescription = document.getElementById('vaultDescription');
const vaultPassword = document.getElementById('vaultPassword');
const vaultConfirmRow = document.getElementById('vaultConfirmRow');
const vaultConfirm = document.getElementById('vaultConfirm');
const vaultSubmit = document.getElementById('vaultSubmit');
const vaultError = document.getElementById('vaultError');
const vaultRecovery = document.getElementById('vaultRecovery');

// The visible desktop UI is a manual-login/debug surface, not the worker pool.
// Keep at most one Dola renderer alive here. Account sessions are prepared from
// the encrypted profile vault before the webview is created.
const views = new Map();
let accounts = [];
let tasks = [];
let activeId = '';
let vaultStatus = null;
let workspaceStarted = false;
let accountSwitchSerial = 0;

function accountById(id) { return accounts.find(item => item.id === id) || null; }
function vaultIsUnlocked() { return ['UNLOCKED', 'RESEAL_REQUIRED'].includes(vaultStatus?.state); }

function destroyView(accountId) {
  const view = views.get(accountId);
  if (!view) return;
  try { view.wrapper.remove(); } catch (_) {}
  views.delete(accountId);
}

function destroyAllViews() {
  for (const accountId of [...views.keys()]) destroyView(accountId);
}

function destroyInactiveViews(keepId) {
  for (const accountId of [...views.keys()]) {
    if (accountId !== keepId) destroyView(accountId);
  }
}

function setControlsForVault() {
  const unlocked = vaultIsUnlocked();
  addButton.disabled = !unlocked;
  refreshTasksButton.disabled = !unlocked;
  lockButton.disabled = !unlocked;
  if (!unlocked) {
    reloadButton.disabled = true;
    clearButton.disabled = true;
    queueTaskButton.disabled = true;
  }
}

function showVaultGate(status) {
  vaultStatus = status;
  const unlocked = vaultIsUnlocked();
  vaultGate.hidden = unlocked;
  setControlsForVault();
  if (unlocked) {
    vaultError.textContent = '';
    vaultPassword.value = '';
    vaultConfirm.value = '';
    return;
  }

  const initializing = status?.initialized !== true;
  vaultTitle.textContent = initializing ? '首次设置 DolaWorkbench 保险库' : '解锁 DolaWorkbench';
  vaultSubmit.textContent = initializing ? '创建保险库并解锁' : '解锁';
  vaultConfirmRow.hidden = !initializing;
  vaultConfirm.required = initializing;
  vaultPassword.autocomplete = initializing ? 'new-password' : 'current-password';
  vaultDescription.textContent = initializing
    ? '请设置一个仅用于本机 Dola 账号登录态加密的主密码。程序不会保存这个密码；以后每次启动输入一次。'
    : '输入本机保险库主密码后，才会解密并打开 Dola 账号会话。密码不会通过 Codex Control Plane 暴露。';
  if (status?.recoveryRequired) {
    vaultRecovery.hidden = false;
    vaultRecovery.textContent = `检测到上次运行未完成安全回收。解锁后会优先保留运行目录中的较新账号会话，再重新加密；涉及账号：${(status.dirtyAccounts || []).join(', ') || '待检查'}`;
  } else {
    vaultRecovery.hidden = true;
    vaultRecovery.textContent = '';
  }
  setTimeout(() => vaultPassword.focus(), 0);
}

function ensureWebview(account) {
  if (views.has(account.id)) return views.get(account.id);
  const wrapper = document.createElement('div');
  wrapper.className = 'webview-wrapper';
  wrapper.dataset.accountId = account.id;
  const webview = document.createElement('webview');
  webview.src = 'https://www.dola.com/chat/';
  webview.partition = account.partition;
  webview.setAttribute('allowpopups', '');
  webview.setAttribute('webpreferences', 'contextIsolation=yes');
  webview.addEventListener('did-start-loading', () => { if (activeId === account.id) statusEl.textContent = 'Dola 页面加载中…'; });
  webview.addEventListener('did-stop-loading', () => { if (activeId === account.id) statusEl.textContent = 'Dola 会话已加载；请直接在页面内登录或使用。'; });
  webview.addEventListener('did-fail-load', (event) => {
    if (activeId === account.id && Number(event.errorCode) !== -3) statusEl.textContent = `Dola 页面加载失败：${event.errorDescription || event.errorCode}`;
  });
  const registerGuest = () => {
    if (typeof webview.getWebContentsId !== 'function') return;
    const guestId = Number(webview.getWebContentsId());
    if (Number.isInteger(guestId) && guestId > 0) {
      window.seedanceDesktop.registerWebview(account.id, guestId);
    }
  };
  webview.addEventListener('dom-ready', registerGuest, { once: true });
  webview.addEventListener('did-stop-loading', registerGuest, { once: true });
  wrapper.appendChild(webview);
  webviewsEl.appendChild(wrapper);
  views.set(account.id, { wrapper, webview });
  return views.get(account.id);
}

async function setActiveAccount(id) {
  const serial = ++accountSwitchSerial;
  if (!vaultIsUnlocked()) {
    showVaultGate(vaultStatus || await window.seedanceDesktop.getVaultStatus());
    return;
  }
  const account = accountById(id);
  activeId = account ? id : '';
  destroyInactiveViews(activeId);
  document.querySelectorAll('.account-card').forEach(el => el.classList.toggle('active', el.dataset.accountId === activeId));
  if (!account) {
    emptyEl.hidden = false;
    activeNameEl.textContent = '尚未选择账号';
    statusEl.textContent = '添加账号后即可在独立 Dola 会话中登录';
    reloadButton.disabled = true;
    clearButton.disabled = true;
    queueTaskButton.disabled = true;
    return;
  }

  emptyEl.hidden = false;
  activeNameEl.textContent = account.name;
  statusEl.textContent = '正在从加密保险库准备该账号会话…';
  reloadButton.disabled = true;
  clearButton.disabled = true;
  queueTaskButton.disabled = true;
  try {
    await window.seedanceDesktop.prepareAccountSession(account.id);
    if (serial !== accountSwitchSerial || activeId !== account.id) return;
    const view = ensureWebview(account);
    view.wrapper.classList.add('active');
    emptyEl.hidden = true;
    statusEl.textContent = '独立 Dola 会话已打开；当前只保留这一个可见调试 WebView。';
    reloadButton.disabled = false;
    clearButton.disabled = false;
    queueTaskButton.disabled = false;
  } catch (error) {
    if (serial !== accountSwitchSerial) return;
    emptyEl.hidden = false;
    statusEl.textContent = `账号会话准备失败：${error.message || error}`;
  }
}

async function renderAccounts() {
  accountsEl.replaceChildren();
  for (const account of accounts) {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'account-card';
    card.dataset.accountId = account.id;
    card.innerHTML = '<span class="dot"></span><span class="account-copy"><strong></strong><small>独立会话</small></span>';
    card.querySelector('strong').textContent = account.name;
    card.addEventListener('click', () => { setActiveAccount(account.id).catch(console.error); });
    accountsEl.appendChild(card);
  }
  if (activeId && accountById(activeId)) await setActiveAccount(activeId);
  else if (accounts[0]) await setActiveAccount(accounts[0].id);
  else await setActiveAccount('');
}

function renderTasks() {
  tasksEl.replaceChildren();
  taskCountEl.textContent = String(tasks.length);
  if (tasks.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'task-empty';
    empty.textContent = '还没有任务。可以从这里或 Codex CLI 加入队列。';
    tasksEl.appendChild(empty);
    return;
  }
  for (const task of tasks.slice(0, 100)) {
    const card = document.createElement('div');
    card.className = 'task-card';
    const top = document.createElement('div');
    top.className = 'task-card-top';
    const title = document.createElement('strong');
    const account = accountById(task.accountId);
    title.textContent = `${account ? account.name : task.accountId.slice(0, 8)} · ${task.duration}s · ${task.ratio}`;
    const state = document.createElement('span');
    state.className = 'task-state';
    state.textContent = task.state;
    top.append(title, state);
    const prompt = document.createElement('div');
    prompt.className = 'task-prompt';
    prompt.textContent = task.prompt;
    const meta = document.createElement('div');
    meta.className = 'task-meta';
    meta.textContent = `${task.provider} / ${task.model}${task.blockedReason ? ` / ${task.blockedReason}` : ''}`;
    const actions = document.createElement('div');
    actions.className = 'task-actions';
    const open = document.createElement('button');
    open.type = 'button';
    open.textContent = '打开账号';
    open.addEventListener('click', () => { setActiveAccount(task.accountId).catch(console.error); });
    actions.appendChild(open);
    if (!['success', 'failed', 'cancelled'].includes(task.state)) {
      const cancel = document.createElement('button');
      cancel.type = 'button';
      cancel.textContent = '取消';
      cancel.addEventListener('click', async () => { await window.seedanceDesktop.cancelTask(task.id); await refreshTasks(); });
      actions.appendChild(cancel);
    }
    card.append(top, prompt, meta, actions);
    tasksEl.appendChild(card);
  }
}

async function refreshAccounts() {
  accounts = await window.seedanceDesktop.listAccounts();
  await renderAccounts();
}
async function refreshTasks() {
  tasks = await window.seedanceDesktop.listTasks();
  renderTasks();
}

async function startUnlockedWorkspace() {
  if (!vaultIsUnlocked()) return;
  setControlsForVault();
  if (!workspaceStarted) {
    workspaceStarted = true;
    await Promise.all([refreshAccounts(), refreshTasks()]);
  } else {
    await refreshAccounts();
  }
}

vaultForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  vaultError.textContent = '';
  const password = vaultPassword.value;
  const initializing = vaultStatus?.initialized !== true;
  if (initializing && password !== vaultConfirm.value) {
    vaultError.textContent = '两次输入的主密码不一致。';
    vaultConfirm.focus();
    return;
  }
  vaultSubmit.disabled = true;
  try {
    const status = initializing
      ? await window.seedanceDesktop.initializeVault(password)
      : await window.seedanceDesktop.unlockVault(password);
    vaultPassword.value = '';
    vaultConfirm.value = '';
    showVaultGate(status);
    await startUnlockedWorkspace();
  } catch (error) {
    vaultPassword.value = '';
    vaultConfirm.value = '';
    vaultError.textContent = `无法解锁：${error.message || error}`;
    vaultPassword.focus();
  } finally {
    vaultSubmit.disabled = false;
  }
});

addButton.addEventListener('click', async () => {
  if (!vaultIsUnlocked()) return showVaultGate(vaultStatus || await window.seedanceDesktop.getVaultStatus());
  const suggested = `Dola ${accounts.length + 1}`;
  const name = window.prompt('给这个 Dola 账号起个名字：', suggested);
  if (name == null) return;
  const account = await window.seedanceDesktop.addAccount(name);
  await refreshAccounts();
  await setActiveAccount(account.id);
});

reloadButton.addEventListener('click', () => { const view = views.get(activeId); if (view) view.webview.reload(); });

clearButton.addEventListener('click', async () => {
  const account = accountById(activeId);
  if (!account) return;
  const confirmed = window.confirm(`确定清除“${account.name}”的本地 Dola 登录会话吗？\n\n不会删除其他账号。`);
  if (!confirmed) return;
  await window.seedanceDesktop.clearAccountSession(account.id);
  const view = views.get(account.id);
  if (view) view.webview.loadURL('https://www.dola.com/chat/');
  statusEl.textContent = '该账号本地会话已清除，请重新登录。';
});

lockButton.addEventListener('click', async () => {
  if (!vaultIsUnlocked()) return;
  const confirmed = window.confirm('锁定保险库会关闭当前可见的 Dola 页面，并把已打开的账号会话重新加密。继续吗？');
  if (!confirmed) return;
  ++accountSwitchSerial;
  destroyAllViews();
  activeId = '';
  reloadButton.disabled = true;
  clearButton.disabled = true;
  queueTaskButton.disabled = true;
  statusEl.textContent = '正在回收并加密账号会话…';
  await new Promise((resolve) => setTimeout(resolve, 250));
  try {
    const result = await window.seedanceDesktop.lockVault();
    vaultStatus = result.vault;
    workspaceStarted = false;
    accounts = [];
    tasks = [];
    accountsEl.replaceChildren();
    tasksEl.replaceChildren();
    taskCountEl.textContent = '0';
    activeNameEl.textContent = '保险库已锁定';
    statusEl.textContent = '输入主密码后才能再次打开 Dola 账号会话。';
    showVaultGate(vaultStatus);
  } catch (error) {
    statusEl.textContent = `保险库锁定失败：${error.message || error}`;
    vaultStatus = await window.seedanceDesktop.getVaultStatus();
    showVaultGate(vaultStatus);
    if (vaultIsUnlocked()) await startUnlockedWorkspace();
  }
});

taskForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const account = accountById(activeId);
  if (!account || !vaultIsUnlocked()) return;
  const prompt = promptEl.value.trim();
  if (!prompt) { promptEl.focus(); return; }
  try {
    await window.seedanceDesktop.createTask({ accountId: account.id, provider: providerEl.value, mode: 't2v', model: 'seedance-v2.5', duration: Number(durationEl.value), ratio: ratioEl.value, prompt });
    promptEl.value = '';
    await refreshTasks();
    statusEl.textContent = providerEl.value === 'dola-web-background'
      ? '任务已加入本地队列；后台 provider 需要通过 Codex 控制端显式 dispatch。'
      : '任务已加入本地队列；Dola 自动提交仍按真实页面能力与 Gate 执行。';
  } catch (error) {
    statusEl.textContent = `创建任务失败：${error.message || error}`;
  }
});

refreshTasksButton.addEventListener('click', () => {
  if (vaultIsUnlocked()) refreshTasks().catch(console.error);
});
window.seedanceDesktop.onActivateAccount((id) => {
  if (vaultIsUnlocked() && accountById(id)) setActiveAccount(id).catch(console.error);
});
window.seedanceDesktop.onAccountsChanged(async () => {
  if (vaultIsUnlocked()) await refreshAccounts();
});
window.seedanceDesktop.onTasksChanged(async () => {
  if (vaultIsUnlocked()) await refreshTasks();
});

(async () => {
  try {
    vaultStatus = await window.seedanceDesktop.getVaultStatus();
    showVaultGate(vaultStatus);
    if (vaultIsUnlocked()) await startUnlockedWorkspace();
  } catch (error) {
    console.error(error);
    statusEl.textContent = '初始化 DolaWorkbench 失败。';
    vaultGate.hidden = false;
    vaultError.textContent = error.message || String(error);
  }
})();
