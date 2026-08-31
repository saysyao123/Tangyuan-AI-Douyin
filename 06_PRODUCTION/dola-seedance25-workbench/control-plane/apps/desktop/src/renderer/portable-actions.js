'use strict';

(() => {
  const dispatchButton = document.getElementById('dispatchNext');
  const recoverButton = document.getElementById('recoverWaiting');
  const statusEl = document.getElementById('status');
  const studioPanel = document.querySelector('.studio-panel');
  if (!dispatchButton || !recoverButton) return;

  // RC3: the whole right-hand Seedance Studio is vertically scrollable.
  // I2V adds an image row and can otherwise push the task list below the
  // fixed-height window. Keep one obvious up/down scrollbar for the whole
  // panel instead of clipping the lower task area.
  const style = document.createElement('style');
  style.textContent = `
    .studio-panel {
      overflow-y: scroll !important;
      overflow-x: hidden !important;
      scrollbar-gutter: stable;
      overscroll-behavior: contain;
    }
    .studio-panel .task-form { flex: 0 0 auto; }
    .studio-panel .tasks {
      min-height: 180px !important;
      overflow: visible !important;
      flex: 0 0 auto;
      padding-bottom: 28px;
    }
    .studio-panel::-webkit-scrollbar { width: 11px; }
    .studio-panel::-webkit-scrollbar-track { background: rgba(255,255,255,.035); border-radius: 999px; }
    .studio-panel::-webkit-scrollbar-thumb { background: rgba(145,160,189,.42); border-radius: 999px; border: 2px solid transparent; background-clip: padding-box; }
    .studio-panel::-webkit-scrollbar-thumb:hover { background: rgba(145,160,189,.65); border: 2px solid transparent; background-clip: padding-box; }
    .task-runtime-detail {
      border-radius: 8px;
      padding: 8px 9px;
      font-size: 11px;
      line-height: 1.5;
      overflow-wrap: anywhere;
      background: #10192b;
      border: 1px solid #2a3855;
      color: #aebad1;
    }
    .task-runtime-detail.error {
      background: #2a171d;
      border-color: #693b46;
      color: #ffc6cd;
    }
    .task-runtime-detail.surface {
      background: #10261c;
      border-color: #315f46;
      color: #b9ebca;
    }
  `;
  document.head.appendChild(style);
  if (studioPanel) studioPanel.scrollTop = 0;

  const runningStates = new Set(['running', 'capture_armed', 'generation_running', 'resolving', 'recovery_required']);
  const recoverStates = new Set(['observation_wait', 'result_observed', 'recovery_required', 'login_required']);

  async function tasks() {
    const items = await window.seedanceDesktop.listTasks();
    return Array.isArray(items) ? items : [];
  }

  function decorateTaskCards(items) {
    const cards = Array.from(document.querySelectorAll('.task-card'));
    for (let index = 0; index < cards.length; index += 1) {
      const card = cards[index];
      const task = items[index];
      if (!task) continue;
      card.querySelectorAll('.task-runtime-detail').forEach((node) => node.remove());

      if (task.executionSurface === 'visible-webview') {
        const surface = document.createElement('div');
        surface.className = 'task-runtime-detail surface';
        surface.textContent = '执行位置：中间可见 Dola 网页（与当前人工登录/手动生成使用同一页面会话）';
        card.appendChild(surface);
      }

      const failure = String(task.error || '').trim();
      if (failure) {
        const detail = document.createElement('div');
        detail.className = 'task-runtime-detail error';
        detail.textContent = `失败原因：${failure}`;
        card.appendChild(detail);
      } else if (task.blockedReason && !['OBSERVATION_WAIT'].includes(task.blockedReason)) {
        const detail = document.createElement('div');
        detail.className = 'task-runtime-detail';
        detail.textContent = `状态详情：${task.blockedReason}`;
        card.appendChild(detail);
      }
    }
  }

  async function refreshUi() {
    try {
      const items = await tasks();
      dispatchButton.disabled = !items.some((task) => task.state === 'queued');
      recoverButton.disabled = !items.some((task) => recoverStates.has(task.state));
      decorateTaskCards(items);
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
      statusEl.textContent = result.message || '任务已交给本地 Portable Worker。';
    } catch (error) {
      statusEl.textContent = `启动任务失败：${error.message || error}`;
    } finally {
      setTimeout(refreshUi, 800);
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
      setTimeout(refreshUi, 800);
    }
  });

  window.seedanceDesktop.onTasksChanged(() => setTimeout(refreshUi, 60));
  setInterval(refreshUi, 5000);
  refreshUi();
})();
