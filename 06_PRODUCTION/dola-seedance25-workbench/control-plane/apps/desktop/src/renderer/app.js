'use strict';

const bridge = window.seedanceDesktop;

const accountsEl = document.getElementById('accounts');
const accountCountEl = document.getElementById('accountCount');
const webviewsEl = document.getElementById('webviews');
const emptyEl = document.getElementById('empty');
const addButton = document.getElementById('addAccount');
const emptyAddButton = document.getElementById('emptyAddAccount');
const reloadButton = document.getElementById('reload');
const clearButton = document.getElementById('clearSession');
const healthButton = document.getElementById('checkHealth');
const lockButton = document.getElementById('lockVault');
const changePasswordButton = document.getElementById('changeVaultPassword');
const defaultPasswordNotice = document.getElementById('defaultPasswordNotice');
const activeNameEl = document.getElementById('activeName');
const activeHealthEl = document.getElementById('activeHealth');
const statusEl = document.getElementById('status');
const taskForm = document.getElementById('taskForm');
const modeEl = document.getElementById('mode');
const durationEl = document.getElementById('duration');
const ratioEl = document.getElementById('ratio');
const promptEl = document.getElementById('prompt');
const createAndRunButton = document.getElementById('createAndRun');
const queueOnlyButton = document.getElementById('queueOnly');
const imageInputRow = document.getElementById('imageInputRow');
const pickImageButton = document.getElementById('pickImage');
const imagePathEl = document.getElementById('imagePath');
const tasksEl = document.getElementById('tasks');
const taskCountEl = document.getElementById('taskCount');
const refreshTasksButton = document.getElementById('refreshTasks');
const toastRegion = document.getElementById('toastRegion');

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

const addAccountModal = document.getElementById('addAccountModal');
const addAccountForm = document.getElementById('addAccountForm');
const accountNameInput = document.getElementById('accountNameInput');
const addAccountSubmit = document.getElementById('addAccountSubmit');
const addAccountError = document.getElementById('addAccountError');

const passwordModal = document.getElementById('passwordModal');
const passwordForm = document.getElementById('passwordForm');
const passwordDefaultHint = document.getElementById('passwordDefaultHint');
const currentPasswordRow = document.getElementById('currentPasswordRow');
const currentVaultPassword = document.getElementById('currentVaultPassword');
const newVaultPassword = document.getElementById('newVaultPassword');
const confirmNewVaultPassword = document.getElementById('confirmNewVaultPassword');
const passwordSubmit = document.getElementById('passwordSubmit');
const passwordError = document.getElementById('passwordError');

const confirmModal = document.getElementById('confirmModal');
const confirmTitle = document.getElementById('confirmTitle');
const confirmMessage = document.getElementById('confirmMessage');
const confirmCancel = document.getElementById('confirmCancel');
const confirmOk = document.getElementById('confirmOk');

const DEFAULT_PASSWORD = 'Tangyuan-Portable-2026!';
const views = new Map();
const sessionStates = new Map();
let accounts = [];
let tasks = [];
let activeId = '';
let vaultStatus = null;
let workspaceStarted = false;
let accountSwitchSerial = 0;
let selectedImagePath = '';
let confirmResolver = null;

function accountById(id) { return accounts.find((item) => item.id === id) || null; }
function vaultIsUnlocked() { return ['UNLOCKED', 'RESEAL_REQUIRED'].includes(vaultStatus?.state); }

function toast(message, type = '') {
  const item = document.createElement('div');
  item.className = `toast${type ? ` ${type}` : ''}`;
  item.textContent = String(message || '');
  toastRegion.appendChild(item);
  setTimeout(() => item.remove(), 4200);
}

function openModal(el) {
  if (!el) return;
  el.hidden = false;
}

function closeModal(el) {
  if (!el) return;
  el.hidden = true;
}

function confirmAction(title, message, dangerous = true) {
  if (confirmResolver) confirmResolver(false);
  confirmTitle.textContent = title;
  confirmMessage.textContent = message;
  confirmOk.classList.toggle('danger', dangerous);
  openModal(confirmModal);
  return new Promise((resolve) => { confirmResolver = resolve; });
}

function settleConfirm(value) {
  closeModal(confirmModal);
  const resolve = confirmResolver;
  confirmResolver = null;
  if (resolve) resolve(Boolean(value));
}

confirmCancel.addEventListener('click', () => settleConfirm(false));
confirmOk.addEventListener('click', () => settleConfirm(true));

document.querySelectorAll('[data-close-modal]').forEach((button) => {
  button.addEventListener('click', () => closeModal(document.getElementById(button.dataset.closeModal)));
});

function sessionLabel(account) {
  const status = sessionStates.get(account.id)?.loginStatus;
  if (status === 'logged_in') return { text: '已登录', dot: 'ready' };
  if (status === 'logged_out') return { text: '需登录', dot: 'warn' };
  if (String(account.status || '').toUpperCase() === 'PAUSED') return { text: '已暂停', dot: 'bad' };
  if (String(account.status || '').toUpperCase() === 'NEEDS_LOGIN') return { text: '待登录', dot: 'warn' };
  return { text: '未检查', dot: '' };
}

function setHealthPill(state) {
  const loginStatus = state?.loginStatus || 'unknown';
  activeHealthEl.className = 'health-pill neutral';
  if (loginStatus === 'logged_in') {
    activeHealthEl.className = 'health-pill ready';
    activeHealthEl.textContent = '已登录';
  } else if (loginStatus === 'logged_out') {
    activeHealthEl.className = 'health-pill warn';
    activeHealthEl.textContent = '需要登录';
  } else {
    activeHealthEl.className = 'health-pill neutral';
    activeHealthEl.textContent = '未确认';
  }
}

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
  for (const accountId of [...views.keys()]) if (accountId !== keepId) destroyView(accountId);
}

function updateTaskControls() {
  const enabled = vaultIsUnlocked() && Boolean(accountById(activeId));
  createAndRunButton.disabled = !enabled;
  queueOnlyButton.disabled = !enabled;
  pickImageButton.disabled = !enabled;
}

function setControlsForVault() {
  const unlocked = vaultIsUnlocked();
  addButton.disabled = !unlocked;
  emptyAddButton.disabled = !unlocked;
  refreshTasksButton.disabled = !unlocked;
  lockButton.disabled = !unlocked;
  changePasswordButton.disabled = !unlocked;
  defaultPasswordNotice.hidden = vaultStatus?.defaultPasswordActive !== true;
  if (!unlocked) {
    reloadButton.disabled = true;
    clearButton.disabled = true;
    healthButton.disabled = true;
  }
  updateTaskControls();
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
    vaultRecovery.textContent = `检测到上次运行未完成安全回收。涉及账号：${(status.dirtyAccounts || []).join(', ') || '待检查'}`;
  } else {
    vaultRecovery.hidden = true;
    vaultRecovery.textContent = '';
  }
  setTimeout(() => vaultPassword.focus(), 0);
}

async function refreshActiveHealth() {
  const account = accountById(activeId);
  if (!account || !bridge) return null;
  healthButton.disabled = true;
  try {
    const state = await bridge.getAccountSessionStatus(account.id);
    sessionStates.set(account.id, state || {});
    setHealthPill(state);
    await renderAccounts();
    if (state?.loginStatus === 'logged_in') statusEl.textContent = 'Dola 登录状态已确认，可以创建 Seedance 任务。';
    else if (state?.loginStatus === 'logged_out') statusEl.textContent = '当前账号尚未登录，请直接在中间 Dola 页面完成登录。';
    else statusEl.textContent = '登录状态暂未确认；如果页面已经登录，可稍后再次点击“检查登录”。';
    return state;
  } catch (error) {
    setHealthPill(null);
    statusEl.textContent = `登录状态检查失败：${error.message || error}`;
    return null;
  } finally {
    healthButton.disabled = false;
  }
}

function ensureWebview(account) {
  if (views.has(account.id)) return views.get(account.id);
  const wrapper = document.createElement('div');
  wrapper.className = 'webview-wrapper';
  wrapper.dataset.accountId = account.id;
  const webview = document.createElement('webview');
  webview.partition = account.partition;
  webview.setAttribute('allowpopups', '');
  webview.setAttribute('webpreferences', 'contextIsolation=yes');
  webview.src = 'https://www.dola.com/chat/';
  webview.addEventListener('did-start-loading', () => {
    if (activeId === account.id) statusEl.textContent = 'Dola 页面加载中…';
  });
  webview.addEventListener('did-stop-loading', () => {
    if (activeId === account.id) {
      statusEl.textContent = 'Dola 页面已加载。首次使用请在页面内完成登录。';
      setTimeout(() => refreshActiveHealth().catch(() => {}), 700);
    }
  });
  webview.addEventListener('did-fail-load', (event) => {
    if (activeId === account.id && Number(event.errorCode) !== -3) {
      statusEl.textContent = `Dola 页面加载失败：${event.errorDescription || event.errorCode}`;
    }
  });
  const registerGuest = () => {
    if (typeof webview.getWebContentsId !== 'function') return;
    const guestId = Number(webview.getWebContentsId());
    if (Number.isInteger(guestId) && guestId > 0) bridge.registerWebview(account.id, guestId);
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
    showVaultGate(vaultStatus || await bridge.getVaultStatus());
    return;
  }
  const account = accountById(id);
  activeId = account ? id : '';
  destroyInactiveViews(activeId);
  document.querySelectorAll('.account-card').forEach((el) => el.classList.toggle('active', el.dataset.accountId === activeId));
  if (!account) {
    emptyEl.hidden = false;
    activeNameEl.textContent = '尚未选择账号';
    statusEl.textContent = '添加账号后即可在独立 Dola 会话中登录';
    setHealthPill(null);
    reloadButton.disabled = true;
    clearButton.disabled = true;
    healthButton.disabled = true;
    updateTaskControls();
    return;
  }

  emptyEl.hidden = false;
  activeNameEl.textContent = account.name;
  statusEl.textContent = '正在从加密保险库准备该账号会话…';
  setHealthPill(sessionStates.get(account.id));
  reloadButton.disabled = true;
  clearButton.disabled = true;
  healthButton.disabled = true;
  updateTaskControls();
  try {
    await bridge.prepareAccountSession(account.id);
    if (serial !== accountSwitchSerial || activeId !== account.id) return;
    const view = ensureWebview(account);
    view.wrapper.classList.add('active');
    emptyEl.hidden = true;
    statusEl.textContent = '独立 Dola 会话已打开。首次使用请直接在页面内登录。';
    reloadButton.disabled = false;
    clearButton.disabled = false;
    healthButton.disabled = false;
    updateTaskControls();
  } catch (error) {
    if (serial !== accountSwitchSerial) return;
    emptyEl.hidden = false;
    statusEl.textContent = `账号会话准备失败：${error.message || error}`;
    toast(`账号会话准备失败：${error.message || error}`, 'error');
  }
}

async function renderAccounts() {
  accountsEl.replaceChildren();
  accountCountEl.textContent = String(accounts.length);
  for (const account of accounts) {
    const label = sessionLabel(account);
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'account-card';
    card.dataset.accountId = account.id;
    card.innerHTML = '<span class="dot"></span><span class="account-copy"><strong></strong><small>独立会话</small></span><span class="account-state"></span>';
    card.querySelector('.dot').className = `dot ${label.dot}`.trim();
    card.querySelector('strong').textContent = account.name;
    card.querySelector('.account-state').textContent = label.text;
    card.addEventListener('click', () => { setActiveAccount(account.id).catch((error) => toast(error.message || error, 'error')); });
    accountsEl.appendChild(card);
  }
  document.querySelectorAll('.account-card').forEach((el) => el.classList.toggle('active', el.dataset.accountId === activeId));
}

function renderTasks() {
  tasksEl.replaceChildren();
  taskCountEl.textContent = String(tasks.length);
  if (tasks.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'task-empty';
    empty.textContent = '还没有任务。登录 Dola 后，可以直接“创建并开始”。';
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
    title.textContent = `${account ? account.name : String(task.accountId || '').slice(0, 8)} · ${task.mode === 'i2v' ? 'I2V' : 'T2V'} · ${task.duration}s · ${task.ratio}`;
    const state = document.createElement('span');
    state.className = 'task-state';
    state.textContent = task.state;
    top.append(title, state);
    const prompt = document.createElement('div');
    prompt.className = 'task-prompt';
    prompt.textContent = task.prompt;
    const meta = document.createElement('div');
    meta.className = 'task-meta';
    const output = task.outputPath || task.downloadPath || task.resultPath || '';
    meta.textContent = `Seedance 2.5${task.blockedReason ? ` / ${task.blockedReason}` : ''}${output ? ` / ${output}` : ''}`;
    const actions = document.createElement('div');
    actions.className = 'task-actions';
    const open = document.createElement('button');
    open.type = 'button';
    open.textContent = '打开账号';
    open.addEventListener('click', () => { setActiveAccount(task.accountId).catch(() => {}); });
    actions.appendChild(open);
    if (!['success', 'failed', 'cancelled'].includes(task.state)) {
      const cancel = document.createElement('button');
      cancel.type = 'button';
      cancel.textContent = '取消';
      cancel.addEventListener('click', async () => { await bridge.cancelTask(task.id); await refreshTasks(); });
      actions.appendChild(cancel);
    }
    card.append(top, prompt, meta, actions);
    tasksEl.appendChild(card);
  }
}

async function refreshAccounts(options = {}) {
  accounts = await bridge.listAccounts();
  await renderAccounts();
  if (options.selectFirst && !activeId && accounts[0]) await setActiveAccount(accounts[0].id);
  if (!accounts.length) await setActiveAccount('');
}

async function refreshTasks() {
  tasks = await bridge.listTasks();
  renderTasks();
}

async function startUnlockedWorkspace() {
  if (!vaultIsUnlocked()) return;
  setControlsForVault();
  if (!workspaceStarted) {
    workspaceStarted = true;
    await Promise.all([refreshAccounts(), refreshTasks()]);
    if (accounts[0]) await setActiveAccount(activeId && accountById(activeId) ? activeId : accounts[0].id);
  } else {
    await refreshAccounts();
  }
}

function showAddAccountModal() {
  if (!vaultIsUnlocked()) return;
  accountNameInput.value = `Dola ${String(accounts.length + 1).padStart(2, '0')}`;
  addAccountError.textContent = '';
  openModal(addAccountModal);
  setTimeout(() => { accountNameInput.focus(); accountNameInput.select(); }, 0);
}

addButton.addEventListener('click', showAddAccountModal);
emptyAddButton.addEventListener('click', showAddAccountModal);

addAccountForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  addAccountError.textContent = '';
  const name = accountNameInput.value.trim();
  if (!name) return;
  addAccountSubmit.disabled = true;
  try {
    statusEl.textContent = '正在创建独立 Dola 账号会话…';
    const account = await bridge.addAccount(name);
    closeModal(addAccountModal);
    await refreshAccounts();
    await setActiveAccount(account.id);
    toast(`已创建 ${account.name}，请在中间页面完成登录。`, 'success');
  } catch (error) {
    addAccountError.textContent = error.message || String(error);
    toast(`添加账号失败：${error.message || error}`, 'error');
  } finally {
    addAccountSubmit.disabled = false;
  }
});

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
    const status = initializing ? await bridge.initializeVault(password) : await bridge.unlockVault(password);
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

changePasswordButton.addEventListener('click', async () => {
  if (!vaultIsUnlocked()) return;
  try { vaultStatus = await bridge.getVaultStatus(); } catch (_) {}
  const usingDefault = vaultStatus?.defaultPasswordActive === true;
  passwordDefaultHint.hidden = !usingDefault;
  currentPasswordRow.hidden = usingDefault;
  currentVaultPassword.required = !usingDefault;
  currentVaultPassword.value = '';
  newVaultPassword.value = '';
  confirmNewVaultPassword.value = '';
  passwordError.textContent = '';
  openModal(passwordModal);
  setTimeout(() => (usingDefault ? newVaultPassword : currentVaultPassword).focus(), 0);
});

passwordForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  passwordError.textContent = '';
  const usingDefault = vaultStatus?.defaultPasswordActive === true;
  const current = usingDefault ? DEFAULT_PASSWORD : currentVaultPassword.value;
  const next = newVaultPassword.value;
  if (next.length < 8) {
    passwordError.textContent = '新密码至少需要 8 位。';
    return;
  }
  if (next !== confirmNewVaultPassword.value) {
    passwordError.textContent = '两次输入的新密码不一致。';
    return;
  }
  passwordSubmit.disabled = true;
  const reopenId = activeId;
  try {
    statusEl.textContent = '正在关闭当前 Dola 页面并重新加密保险库…';
    ++accountSwitchSerial;
    destroyAllViews();
    await new Promise((resolve) => setTimeout(resolve, 900));
    const result = await bridge.changeVaultPassword(current, next);
    vaultStatus = result.vault || await bridge.getVaultStatus();
    closeModal(passwordModal);
    setControlsForVault();
    toast('保险库密码已修改，首次预设密码已失效。', 'success');
    statusEl.textContent = '保险库密码修改成功。';
    if (reopenId && accountById(reopenId)) await setActiveAccount(reopenId);
  } catch (error) {
    passwordError.textContent = error.message || String(error);
    statusEl.textContent = `修改保险库密码失败：${error.message || error}`;
    toast(`修改密码失败：${error.message || error}`, 'error');
    try {
      vaultStatus = await bridge.getVaultStatus();
      setControlsForVault();
      if (reopenId && accountById(reopenId) && vaultIsUnlocked()) await setActiveAccount(reopenId);
    } catch (_) {}
  } finally {
    passwordSubmit.disabled = false;
  }
});

reloadButton.addEventListener('click', () => {
  const view = views.get(activeId);
  if (view) view.webview.reload();
});

healthButton.addEventListener('click', () => refreshActiveHealth().catch(() => {}));

clearButton.addEventListener('click', async () => {
  const account = accountById(activeId);
  if (!account) return;
  const confirmed = await confirmAction('清除本账号会话', `确定清除“${account.name}”的本地 Dola 登录会话吗？其他账号不会受影响。`);
  if (!confirmed) return;
  try {
    await bridge.clearAccountSession(account.id);
    sessionStates.delete(account.id);
    const view = views.get(account.id);
    if (view) view.webview.loadURL('https://www.dola.com/chat/');
    setHealthPill({ loginStatus: 'logged_out' });
    statusEl.textContent = '该账号本地会话已清除，请重新登录。';
    await renderAccounts();
  } catch (error) {
    toast(`清除会话失败：${error.message || error}`, 'error');
  }
});

lockButton.addEventListener('click', async () => {
  if (!vaultIsUnlocked()) return;
  const confirmed = await confirmAction('锁定保险库', '锁定会关闭当前 Dola 页面，并尝试把已打开账号的会话重新加密。继续吗？', false);
  if (!confirmed) return;
  ++accountSwitchSerial;
  destroyAllViews();
  activeId = '';
  reloadButton.disabled = true;
  clearButton.disabled = true;
  healthButton.disabled = true;
  updateTaskControls();
  statusEl.textContent = '正在回收并加密账号会话…';
  await new Promise((resolve) => setTimeout(resolve, 900));
  try {
    const result = await bridge.lockVault();
    vaultStatus = result.vault;
    workspaceStarted = false;
    accounts = [];
    tasks = [];
    accountsEl.replaceChildren();
    tasksEl.replaceChildren();
    accountCountEl.textContent = '0';
    taskCountEl.textContent = '0';
    activeNameEl.textContent = '保险库已锁定';
    statusEl.textContent = '输入主密码后才能再次打开 Dola 账号会话。';
    showVaultGate(vaultStatus);
  } catch (error) {
    statusEl.textContent = `保险库锁定失败：${error.message || error}`;
    toast(`保险库锁定失败：${error.message || error}`, 'error');
    vaultStatus = await bridge.getVaultStatus();
    showVaultGate(vaultStatus);
    if (vaultIsUnlocked()) await startUnlockedWorkspace();
  }
});

modeEl.addEventListener('change', () => {
  imageInputRow.hidden = modeEl.value !== 'i2v';
});

pickImageButton.addEventListener('click', async () => {
  try {
    const chosen = await bridge.pickImage();
    if (!chosen) return;
    selectedImagePath = chosen;
    imagePathEl.textContent = chosen;
  } catch (error) {
    toast(`选择图片失败：${error.message || error}`, 'error');
  }
});

async function createTask({ dispatch }) {
  const account = accountById(activeId);
  if (!account || !vaultIsUnlocked()) return;
  const prompt = promptEl.value.trim();
  if (!prompt) {
    promptEl.focus();
    toast('请先输入 Prompt。', 'error');
    return;
  }
  if (modeEl.value === 'i2v' && !selectedImagePath) {
    toast('图生视频需要先选择首帧图片。', 'error');
    return;
  }
  createAndRunButton.disabled = true;
  queueOnlyButton.disabled = true;
  try {
    const task = await bridge.createTask({
      accountId: account.id,
      provider: 'dola-web',
      mode: modeEl.value,
      model: 'seedance-v2.5',
      duration: Number(durationEl.value),
      ratio: ratioEl.value,
      prompt,
      imagePath: modeEl.value === 'i2v' ? selectedImagePath : null
    });
    promptEl.value = '';
    if (dispatch) {
      statusEl.textContent = `任务 ${task.id.slice(0, 8)} 已创建，正在交给本地 Worker…`;
      const result = await bridge.dispatchTask(task.id);
      statusEl.textContent = result.message || '任务已开始。';
      toast('任务已创建并开始执行。', 'success');
    } else {
      statusEl.textContent = '任务已加入队列。';
      toast('任务已加入队列。', 'success');
    }
    await refreshTasks();
  } catch (error) {
    statusEl.textContent = `任务操作失败：${error.message || error}`;
    toast(`任务操作失败：${error.message || error}`, 'error');
    await refreshTasks().catch(() => {});
  } finally {
    updateTaskControls();
  }
}

taskForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  await createTask({ dispatch: true });
});

queueOnlyButton.addEventListener('click', () => createTask({ dispatch: false }));
refreshTasksButton.addEventListener('click', () => refreshTasks().catch((error) => toast(error.message || error, 'error')));

if (bridge) {
  bridge.onActivateAccount((id) => {
    if (vaultIsUnlocked() && accountById(id)) setActiveAccount(id).catch(() => {});
  });
  bridge.onAccountsChanged(async () => {
    if (vaultIsUnlocked()) await refreshAccounts();
  });
  bridge.onTasksChanged(async () => {
    if (vaultIsUnlocked()) await refreshTasks();
  });
}

(async () => {
  if (!bridge) {
    statusEl.textContent = '桌面桥接没有加载，当前构建不可用。';
    vaultGate.hidden = false;
    vaultError.textContent = 'seedanceDesktop preload bridge missing';
    return;
  }
  try {
    vaultStatus = await bridge.getVaultStatus();
    showVaultGate(vaultStatus);
    if (vaultIsUnlocked()) await startUnlockedWorkspace();
  } catch (error) {
    statusEl.textContent = '初始化 DolaWorkbench 失败。';
    vaultGate.hidden = false;
    vaultError.textContent = error.message || String(error);
  }
})();
