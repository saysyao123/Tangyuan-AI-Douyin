# Dola 多账号 Session 恢复与切换说明

日期：2026-08-30

## 现象

在 Codex 内置 Dola 页面退出当前账号后，访问 `https://www.dola.com/chat/?from_logout=1`，再次点击登录仍回到原账号。当前页面原登录账号显示为 `BASELINE_ACCOUNT`。

## 原因判断

这不是 `A01/A02` 注册表或 Scheduler 的问题，而是同一个浏览器 Profile 中仍保留着原有 Dola/SSO 登录会话。登出 Dola 页面不等同于清空外部 SSO 的账号选择状态。当前已验证 Full CDP 可用，但 `Target.getBrowserContexts` 和 `Target.createBrowserContext` 不支持，因此 Codex 内置浏览器不能在一个 Process 中创建多个隔离登录 Context。

不读取 Cookie、Local Storage、密码、Profile 数据库或 Token，也不建议通过清理这些数据来解决。

## 迁移自之前多账号软件的可行方案

之前软件的稳定做法是：

```text
Account A → 独立 Profile A → 独立 Session/端口
Account B → 独立 Profile B → 独立 Session/端口
一次只启用一个热账号
任务显式绑定 account_id
```

Dola 项目现在提供同样的本地启动器：

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver
.\tools\dola_account_slot.ps1 -AccountId A01 -Mode Login
.\tools\dola_account_slot.ps1 -AccountId A02 -Mode Login
.\tools\dola_account_slot.ps1 -AccountId A03 -Mode Login
```

对应关系：

```text
A01 / S01 / http://127.0.0.1:9331 / runtime\dola-accounts\A01
A02 / S02 / http://127.0.0.1:9332 / runtime\dola-accounts\A02
A03 / S03 / http://127.0.0.1:9333 / runtime\dola-accounts\A03
```

第一次启动是可见模式，账号所有者手动完成登录；之后关闭可见窗口，用同一个 Slot 的 `-Mode Background` 复用。不要把一个 Profile 的登录态复制到另一个 Profile，也不要让同一个 Profile 同时被可见和后台实例占用。

## 验收边界

```text
SLOT_PROFILE_SEPARATION: LOCAL_PASS
CDP_ENDPOINT_SEPARATION: LOCAL_PASS
LOGIN_CREDENTIAL_AUTOMATION: NOT_USED
IN_APP_BROWSER_MULTI_CONTEXT: NOT_AVAILABLE
REAL_DOLA_MULTI_ACCOUNT: PENDING_MANUAL_LOGIN
```

真实多账号验收顺序：用户分别登录至少两个 Slot → 页面显示对应账号 → 手动标记对应账号 `READY` → 每个 Slot 生成至少一条测试 → 每条捕捉、Resolver、下载、FFprobe 和账本中的 `account_id/session_slot` 一致 → 切回下一个 Slot。遇到 quota、rate-limit、account restriction 或 country restriction 时停止该账号，不自动换号规避限制。
