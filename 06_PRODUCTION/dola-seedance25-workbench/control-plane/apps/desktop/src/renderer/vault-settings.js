'use strict';

(() => {
  const DEFAULT_PASSWORD = 'Tangyuan-Portable-2026!';
  const button = document.getElementById('changeVaultPassword');
  const notice = document.getElementById('defaultPasswordNotice');
  const webviews = document.getElementById('webviews');
  const statusEl = document.getElementById('status');
  if (!button || !notice) return;

  async function refresh() {
    try {
      const status = await window.seedanceDesktop.getVaultStatus();
      notice.hidden = status.defaultPasswordActive !== true;
      button.disabled = !['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state);
      return status;
    } catch (_) {
      button.disabled = true;
      return null;
    }
  }

  button.addEventListener('click', async () => {
    const status = await refresh();
    if (!status || !['UNLOCKED', 'RESEAL_REQUIRED'].includes(status.state)) return;
    const confirmed = window.confirm('修改保险库密码前会关闭当前可见的 Dola 页面并重新加密已保存账号登录态。建议在没有生成任务运行时操作。继续吗？');
    if (!confirmed) return;

    const currentPassword = status.defaultPasswordActive === true
      ? DEFAULT_PASSWORD
      : window.prompt('请输入当前保险库密码：', '');
    if (currentPassword == null || !String(currentPassword).length) return;

    const newPassword = window.prompt('请输入新的保险库密码（至少 8 位，建议使用独立强密码）：', '');
    if (newPassword == null) return;
    if (String(newPassword).length < 8) {
      window.alert('新密码至少需要 8 位。');
      return;
    }
    const confirmPassword = window.prompt('请再次输入新的保险库密码：', '');
    if (confirmPassword == null || newPassword !== confirmPassword) {
      window.alert('两次输入的新密码不一致。');
      return;
    }

    button.disabled = true;
    statusEl.textContent = '正在关闭 Dola 页面、回收会话并重新加密保险库…';
    try {
      webviews.replaceChildren();
      await new Promise((resolve) => setTimeout(resolve, 400));
      await window.seedanceDesktop.changeVaultPassword(currentPassword, newPassword);
      notice.hidden = true;
      window.alert('保险库密码已修改。旧的首次预设密码已失效。');
      window.location.reload();
    } catch (error) {
      statusEl.textContent = `修改保险库密码失败：${error.message || error}`;
      window.alert(`修改失败：${error.message || error}\n\n如果提示账号 Profile 无法回收，请确认没有后台生成/调试窗口占用该账号后重试。`);
      await refresh();
    }
  });

  refresh();
})();
