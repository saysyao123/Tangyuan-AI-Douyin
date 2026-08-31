'use strict';

(() => {
  const dispatchButton = document.getElementById('dispatchNext');
  const recoverButton = document.getElementById('recoverWaiting');
  const statusEl = document.getElementById('status');
  if (!dispatchButton || !recoverButton) return;

  const runningStates = new Set(['running', 'capture_armed', 'generation_running', 'resolving', 'recovery_required']);
  const recoverStates = new Set(['observation_wait', 'result_observed', 'recovery_required', 'login_required']);

  async function tasks() {
    const items = await window.seedanceDesktop.listTasks();
    return Array.isArray(items) ? items : [];
  }

  async function refreshButtons() {
    try {
      const items = await tasks();
      dispatchButton.disabled = !items.some((task) => task.state === 'queued');
      recoverButton.disabled = !items.some((task) => recoverStates.has(task.state));
    } catch (_) {
      dispatchButton.disabled = true;
      recoverButton.disabled = true;
    }
  }

  dispatchButton.addEventListener('click', async () => {
    dispatchButton.disabled = true;
    try {
      const items = await tasks();
      const task = items.find((item) => item.state === 'queued');
      if (!task) {
        statusEl.textContent = '没有排队中的任务。';
        return;
      }
      statusEl.textContent = `正在启动任务 ${task.id.slice(0, 8)}…`;
      const result = await window.seedanceDesktop.dispatchTask(task.id);
      statusEl.textContent = result.message || '任务已交给本地 Portable Worker；生成会在后台继续。';
    } catch (error) {
      statusEl.textContent = `启动任务失败：${error.message || error}`;
    } finally {
      setTimeout(refreshButtons, 800);
    }
  });

  recoverButton.addEventListener('click', async () => {
    recoverButton.disabled = true;
    try {
      const items = await tasks();
      const task = items.find((item) => recoverStates.has(item.state) && !runningStates.has(item.state));
      if (!task) {
        statusEl.textContent = '目前没有需要恢复观察的任务。';
        return;
      }
      statusEl.textContent = `正在恢复观察任务 ${task.id.slice(0, 8)}；不会重新提交生成…`;
      const result = await window.seedanceDesktop.recoverTask(task.id);
      statusEl.textContent = result.message || '恢复观察已启动；不会重复点击 Dola 生成。';
    } catch (error) {
      statusEl.textContent = `恢复任务失败：${error.message || error}`;
    } finally {
      setTimeout(refreshButtons, 800);
    }
  });

  window.seedanceDesktop.onTasksChanged(() => refreshButtons());
  setInterval(refreshButtons, 5000);
  refreshButtons();
})();
