# Xiaochai Session Host Bridge

这是 Dola 多账号的兼容路线：旧版小柴多开器负责保存每个账号自己的 Electron `persist:` 分区和页面会话；当前 Resolver 只通过本机 `127.0.0.1` Bridge 请求公开账号状态、读取该账号页面已经捕获的 Dola 响应，并要求旧软件使用同一分区完成媒体下载。

本路线不复制浏览器 Profile，不导入 Cookie，不保存密码、验证码、OAuth 或 Token，也不修改原始 EXE。构建产物位于 `runtime\xiaochai-bridge`，原始文件仍在分析目录中保持不变。

## 构建与启动

在项目根目录执行：

```powershell
.\tools\build_xiaochai_bridge.ps1
.\tools\launch_xiaochai_bridge.bat
```

Bridge 默认只监听：

```text
http://127.0.0.1:8766
```

启动克隆版小柴窗口后，由账号所有者在各个 Dola 账号分区内手动完成登录。Bridge 不会把旧软件的 `authStatus` 自动写成当前账号 `READY`；需要通过 session 检查并由用户确认后再标记。

## Resolver 接入

```powershell
.venv\Scripts\python.exe -m app.cli xiaochai-bridge health
.venv\Scripts\python.exe -m app.cli xiaochai-bridge accounts
.venv\Scripts\python.exe -m app.cli xiaochai-bridge accounts --sync
.venv\Scripts\python.exe -m app.cli xiaochai-bridge session A01
.venv\Scripts\python.exe -m app.cli xiaochai-bridge capture A01 --output captures\legacy-host\A01-latest.json
.venv\Scripts\python.exe -m app.cli xiaochai-bridge resolve-latest A01 --auto-download --report captures\legacy-host\A01.report.json
```

其中 `A01` 是 Resolver 注册表中的本地账号 ID，不一定等于旧软件内部的账号 ID。映射关系保存在 `runtime\accounts\accounts.json` 的 `session_host=xiaochai` 和 `host_account_id` 字段中。

## 验收门槛

```text
XIAOCHAI_BRIDGE_BUILD: PASS
XIAOCHAI_BRIDGE_LAUNCH: PASS
LOCAL_BRIDGE_HEALTH: PASS
ACCOUNT_SYNC: PASS
MANUAL_LOGIN: PENDING / PASS
SESSION_VERIFY: PENDING / PASS
CAPTURE: PENDING / PASS
DOWNLOAD_WITH_SAME_PARTITION: PENDING / PASS
FFPROBE: PENDING / PASS
VISIBLE_WATERMARK_QA: PENDING / PASS
REAL_MULTI_ACCOUNT_ROUND_ROBIN: PENDING / PASS
```

只有实际下载文件通过 FFprobe、完整性检查以及首/中/尾帧无可见水印检查，才能把某个候选源标记为 clean。Bridge 能连通、出现 URL 或旧软件界面显示“已登录”，都不能替代文件级验收。账号轮询也必须以真实 Job 成功记录为依据；单纯本地轮询模拟不代表 Dola 服务端额度。

## 安全边界

- 所有桥接请求都绑定 `127.0.0.1`，可选本机 token 只通过环境变量传递。
- `/v1/accounts` 只返回 Dola 账号的公开标识、显示名、站点和状态。
- 捕获响应只作为当前用户本机的短期解析输入，不进入账号/任务总账本。
- 下载只允许 HTTPS Dola/CDN 类域名，并复用原账号 Electron 分区的网络请求；403 或地区限制原样失败，不做绕过。
- 旧软件原始 EXE 不直接修改；后续升级应重新从原始 `app.asar` 构建克隆版并复验注入。
