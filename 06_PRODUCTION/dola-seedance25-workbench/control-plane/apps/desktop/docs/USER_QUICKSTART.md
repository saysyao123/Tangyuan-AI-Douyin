# Dola Seedance Portable V1 — Quick Start

1. 解压 ZIP 到一个普通可写目录，例如 `D:\AI\DolaWorkbench`。不要直接在 ZIP 里运行。
2. 双击 `Dola-Seedance-Workbench-Portable-*.exe`。
3. 首次运行会自动建立并解锁本地保险库，预设密码为 `Tangyuan-Portable-2026!`。这是公开的首次启动便利密码，不是长期安全密码。
4. 点击“+ 添加 Dola 账号”，选择该账号后，在中间可见 Dola 页面里由你本人完成登录。程序不会收集 Google 密码、TOTP、短信验证码，也不会自动注册账号。
5. 第一次确认登录态可正常恢复后，建议点右上角“修改保险库密码”，换成你自己的独立密码。旧预设密码随后失效。
6. 右侧选择时长/比例，输入 Prompt，点“加入任务队列”。然后点“开始下一个排队任务”。任务会交给本机 Portable Worker；默认最多 3 个账号并发，同一账号同时只允许 1 个生成任务。
7. 如果任务进入 `observation_wait`，程序会先自动做一次“只恢复观察、不重新提交”的恢复；仍未拿到媒体时可点“恢复等待中的任务”。这一步不会再次点击 Dola 的生成按钮。
8. 成功解析并下载的 MP4 保存到程序旁的 `data\outputs\`。调试/证据文件在 `data\debug\`，项目/任务元数据在 `data\projects\` 和现有任务数据中。
9. 5s/10s 是正常测试目标。只有当前登录的 Dola 页面/账号本身正常提供 30s 时才选择 30s；程序不会伪造 entitlement、绕过 quota、CAPTCHA、MFA、地区限制或服务端拒绝。
10. 正常关闭程序时，已打开账号的 Chromium 登录态会重新加密写入 `data\vault\`。如果 Windows 文件句柄导致明文 Profile 无法安全删除，程序会阻止“假装安全退出”并要求恢复/重试。

## 目录

- `runtime/`：临时控制与解密后的运行态；程序运行时使用。
- `data/vault/`：加密后的账号 Profile。
- `data/accounts/`：非敏感账号元数据。
- `data/projects/`：项目/Job 状态。
- `data/outputs/`：生成后成功解析、下载并通过轻量 MP4 校验的文件。
- `data/logs/`、`data/debug/`、`data/backups/`：日志、调试证据和备份。

移动到另一台电脑前，先正常退出并备份整个 `data/`。跨机器登录态是否继续有效最终由 Dola/Google 的安全策略决定，必要时会要求重新登录。
