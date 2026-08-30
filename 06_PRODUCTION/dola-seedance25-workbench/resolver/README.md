# Dola Original Video Resolver

这是一个独立的、可审计的 Dola 原文件解析、下载与多账号任务编排工具。它只处理用户本人登录并有权使用的会话和媒体；不包含登录绕过、验证码绕过、Cookie 抽取、配额绕过或 403 绕过。多账号功能只负责非敏感账号标识、Session Slot 绑定、健康感知轮询和审计记录。

## P0 已实现

- 递归扫描普通 JSON、嵌套 JSON 字符串、`video_model`、`fallback_api`、`video_list`、VID、`key_seed` 与候选媒体字段。
- 解析明文 HTTP(S)、普通 Base64/Base64URL、`$ @ #` 变体，以及带 `key_seed` 的 qAAB AES-CBC URL。
- 对候选源按“明确无水印/原始证据 → 像素面积 → 码率 → 编码”排序；任何水印负证据优先级最高。
- fallback_api 仅按 `channel=no&codec_type=8&logo_type=unwatermarked` 构造请求。
- 流式下载到 `.part`，核对 `Content-Length`，完成后原子改名；不重新编码。
- MP4 `ftyp` 签名、SHA-256 与 ffprobe 技术 QA；报告自动脱敏 URL 查询串，不输出 `key_seed`、Cookie 或签名 token。
- P1.1 Playwright persistent browser：独立 profile、全 context response 捕获、Network Discovery、`_ROUTER_DATA` 兜底和合法 `BrowserContext.request` 下载 fallback。
- P1.2 External Chrome/Edge + CDP：由用户桌面启动独立非默认 profile，程序只用 `connect_over_cdp` 接入已登录 Context；高相关响应评分、CDP 脱敏索引和外部浏览器不关闭保护。
- P1.5 Generation-Time Capture：`app/capture/generation_hook.js` 在生成前只读旁路捕获 fetch/XHR/SSE/WebSocket 响应；`resolve-generation` 将生成 bundle 中的 task/message/video identity 交给现有 Resolver，并对 VID、node/key 和 watermark 证据 fail-closed。
- P2.1/P3 多账号生产底座：`app/production/` 提供非敏感 Account Registry、sticky Job binding、即时 `events.jsonl`、Job 状态机/恢复存档、单 Worker health-aware round robin、容量事实报告和 5 秒文件级 QA Gate。
- 既有自研登录器接入：`consumer-gateway` 连接 `D:\豆包Seedance本地生成方案\consumer_gateway` 的本机管理 API，只同步公开账号 ID/状态，不复制 Cookie、Profile 或 SQLite。

## 使用

在本目录执行：

```powershell
python -m app.cli resolve --metadata fixtures/fallback_api_sample.json
python -m app.cli download --metadata response.json --output output/test.mp4 --report output/test.report.json
python -m app.cli inspect output/test.mp4 --report output/test.inspect.json
```

`download` 只有在解析到明确无水印候选时才会继续。HTTP 403 会原样失败，不会尝试绕过权限。`--fetch-fallback` 是显式网络动作，默认关闭。

## P1.1 持久化浏览器

首次登录使用专用 headed Chromium，不要指定日常 Chrome Profile：

```powershell
python -m playwright install chromium
python -m app.cli dola-browser
```

浏览器启动后，由用户本人完成 Dola 登录，再打开本人已经生成的视频对话并刷新。登录态会保存在 `runtime/dola-browser-profile`，该目录已被 Git 忽略。自动下载必须显式开启：

```powershell
python -m app.cli dola-browser --auto-download --discover-network
```

程序只监听当前 Playwright Context 的 response，不拦截或修改页面请求；目标优先是本人会话中的 `dola.com` `/im/chain/single`。如果普通 HTTP 下载返回 403，仅使用同一 Playwright Context 的 `context.request` 重试；仍为 403 时失败关闭，不伪造 Authorization、不读取浏览器 Profile 文件。

扩展方案仍保留在 `browser-extension/`，但不是默认路径。

## P1.2 外部 Chrome/Edge + CDP

P1.2 不再由 Playwright 启动 GUI 浏览器。先由用户双击以下任一启动器：

```text
tools\launch_dola_chrome_cdp.bat
tools\launch_dola_edge_cdp.bat
```

启动器使用独立的 `runtime\dola-*-cdp-profile` 和 `127.0.0.1:9222`。首次运行由用户本人在该专用浏览器中完成 Dola 登录，之后保持浏览器打开。可先检查 CDP：

```powershell
.venv\Scripts\python.exe tools\check_cdp.py
```

然后运行真实捕获：

```powershell
.venv\Scripts\python.exe -m app.cli dola-cdp --auto-download --discover-network --target-chat "https://www.dola.com/chat/00000000000000000"
```

程序只监听 attach 之后的新 response，并自动刷新目标历史对话；不读取密码、Cookie、验证码或 Profile 文件，不调用 `browser.close()`/`context.close()`，不修改外部浏览器生命周期。Discovery 只有响应评分达到 8 才进入解析，单独的 `video_model` 不会被判定为视频元数据。

### 已完成一次登录后的后台模式

如果不希望保留可见浏览器窗口，先关闭可见的专用 Dola 浏览器，再双击：

```text
tools\launch_dola_chrome_cdp_background.bat
```

Chrome 不可用时使用：

```text
tools\launch_dola_edge_cdp_background.bat
```

这两个启动器使用同一个已登录专用 Profile，以 `--headless=new` 在后台开启 9222；首次登录不能在无头模式完成。后台浏览器启动后，仍使用上面的 `dola-cdp` 命令。可见/后台实例不能同时占用同一个 Profile 或 9222 端口。

## 测试

```powershell
python -m pytest
```

`fixtures/` 中的地址和 qAAB 仅用于单元测试，不是真实下载地址。当前已知 Dola 15 秒文件仍是带水印预览证据，因此不能把它们当作无水印源验收通过。

## 多账号 5 秒生产底座

账号注册表只保存账号标识和 Session Slot，不保存密码、Cookie、OAuth、Token、验证码或浏览器 Profile：

```powershell
.venv\Scripts\python.exe -m app.cli accounts --json
.venv\Scripts\python.exe -m app.cli account-add A01 --display-name Dola-01
.venv\Scripts\python.exe -m app.cli account-login A01
.venv\Scripts\python.exe -m app.cli account-set-status A01 READY
```

`account-login` 只显示人工登录 Gate，不自动读取凭据，也不会伪造 READY。只有用户本人确认该 Slot 的 Dola 页面已登录后，才可以显式设置 `READY`。

任务入队与本地轮询验收：

```powershell
.venv\Scripts\python.exe -m app.cli enqueue --prompt-file prompts\p01.md
.venv\Scripts\python.exe -m app.cli worker --dry-run
```

`worker --dry-run` 只验证 Job → account_id/session_slot 的轮询，不提交生成。真实 Worker 仍需要当前 Codex In-App Browser 的用户确认生成动作；在 Full CDP 不支持 BrowserContext 隔离时，不能宣称多个 Dola 账号已同时登录。

### Dola 多账号登录问题：不要在同一个 Profile 反复退出重登

如果退出后点击登录仍自动回到旧账号，这是同一个浏览器 Profile/SSO 会话被复用，不是账号注册表问题。当前 Codex In-App Browser 的 Full CDP 不支持创建独立 BrowserContext，因此多账号实机采用“每个账号一个独立 Profile、一个独立 CDP 端口、单 Worker 顺序切换”的降级方案：

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver

# 首次为每个账号打开独立可见 Profile，由账号所有者手动登录
.\tools\dola_account_slot.ps1 -AccountId A01 -Mode Login
.\tools\dola_account_slot.ps1 -AccountId A02 -Mode Login
.\tools\dola_account_slot.ps1 -AccountId A03 -Mode Login

# 登录完成并关闭可见窗口后，按需以后台模式启动某个 Slot
.\tools\dola_account_slot.ps1 -AccountId A02 -Mode Background
.venv\Scripts\python.exe -m app.cli dola-cdp --endpoint http://127.0.0.1:9332 --discover-network
```

Profile 目录分别为 `runtime\dola-accounts\A01`、`A02`、`A03`，不复制现有登录态，也不导出任何凭据。每个 Slot 可用 `-Mode Status` 检查 CDP 是否监听；CDP 监听不等于 Dola 已登录，仍需页面账号状态检查。`A01 → A02 → A03` 的自动任务分配只在各 Slot 已人工登录并标记 `READY` 后成立。

每个发现的媒体身份会立即追加到 `runtime/events.jsonl`，账号/任务摘要分别写入 `runtime/accounts/account-ledger.jsonl` 和 `runtime/jobs/job-ledger.jsonl`。签名 URL、key_seed 和凭证不会进入总账本。

### 旧小柴多开器作为 Session Host（兼容路线）

如果账号在同一个网页 Profile 中退出后仍自动回到旧账号，可使用隔离的旧软件 Session Host。构建时从原始 `app.asar` 复制并注入本机 Bridge，原始 EXE 不会被覆盖：

```powershell
.\tools\build_xiaochai_bridge.ps1
.\tools\launch_xiaochai_bridge.bat
.venv\Scripts\python.exe -m app.cli xiaochai-bridge health
.venv\Scripts\python.exe -m app.cli xiaochai-bridge accounts --sync
```

随后由账号所有者在克隆版小柴的各个 Dola 分区手动登录。Resolver 通过 `session_host=xiaochai`、`host_account_id` 绑定账号，捕获和下载均由旧软件在对应分区执行；不复制 Profile、不读取或输出 Cookie。完整流程和验收表见 [`docs/XIAOCHAI_SESSION_HOST_BRIDGE_20260830.md`](docs/XIAOCHAI_SESSION_HOST_BRIDGE_20260830.md)。

5 秒素材只接受 FFprobe 时长 4.0–6.5 秒、至少 1280×720，并且首/中/尾帧人工确认无可见水印；页面显示“5 秒”不能替代文件级验收。当前“每账号可生成几条”只有在服务端额度和单 Job 成本均由真实响应确认后才能计算，本地剩余计数不作为容量结论。

### 接入之前自研的多账号登录器

当前最适合复用的不是新建浏览器，而是之前已经验证过的本地消费者网关。它默认监听 `127.0.0.1:19090`，账号会话仍由 `D:\豆包Seedance本地生成方案\consumer_gateway` 管理；本项目只同步公开账号标识并建立 `A01/A02/... → host_account_id` 映射：

```powershell
.venv\Scripts\python.exe -m app.cli consumer-gateway health
.venv\Scripts\python.exe -m app.cli consumer-gateway accounts --sync
.venv\Scripts\python.exe -m app.cli consumer-gateway status A01
.venv\Scripts\python.exe -m app.cli consumer-gateway start A01
.venv\Scripts\python.exe -m app.cli consumer-gateway probe A01
```

`stopped` 只表示该账号当前没有占用热浏览器，不等于会话退出；`status` 返回 `logged_in=true` 后，当前项目才会将对应槽位标记为 `READY`。由于旧网关的实际站点是豆包 `doubao.com`，这条接入路线适用于我们之前的 Seedance 2.5 豆包生产链；它不能把豆包会话冒充成 `dola.com` 会话。详见 [`docs/CONSUMER_GATEWAY_SESSION_HOST_20260830.md`](docs/CONSUMER_GATEWAY_SESSION_HOST_20260830.md)。

## P1.5 生成时捕获

P1.5 必须在点击 Dola 生成按钮前，使用 Codex In-App Browser + Full CDP 开启 `Network/Page/Runtime`，并执行 `app/capture/generation_hook.js`。Hook 不读取 Cookie、Profile 或密码，不改写原始请求/响应，只将响应旁路放入页面内存缓冲区；URL 只记录 host/path，正文有单块 2 MB、总 64 MB 上限。

生成完成后将事件文件保存到：

```text
captures/generation/YYYYMMDD_HHMMSS/
```

然后运行：

```powershell
python -m app.cli resolve-generation captures/generation/YYYYMMDD_HHMMSS
```

该命令生成 `identity-chain.json`、`media-hits.json`、`resolver-input.json` 和 `generation-report.json`。单独的 `video_model`、普通 `key` 或不符合 VID 格式的 `v...` 字符串不会通过媒体身份 Gate。

## 实机边界

浏览器捕获必须在本人已登录会话内打开历史作品或手动刷新后观察请求。扩展版保留为备用方案，Playwright P1.1 是当前默认实现；是否拿到 clean source 仍需以真实响应、下载文件、ffprobe 和肉眼检查共同确认。

## Dola Desktop 多账号后台接入

当前项目可以连接用户自己运行的 `Dola Seedance Desktop Studio` 控制平面，同步其非敏感
账号槽位元数据，并通过 loopback API 激活指定账号。不会复制或导出 Cookie、密码、Token、
验证码或 Chromium Profile。

先启动 Dola 登录器：

```powershell
cd LOCAL_CONTROL_PLANE_ROOT\apps\desktop
npm start
```

再在本项目执行：

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver
.venv\Scripts\python.exe -m app.cli dola-desktop health
.venv\Scripts\python.exe -m app.cli dola-desktop accounts
.venv\Scripts\python.exe -m app.cli dola-desktop accounts --sync
.venv\Scripts\python.exe -m app.cli dola-desktop activate D01
```

`--sync` 使用独立的 `runtime/accounts/dola_accounts.json`，不会覆盖其他 Provider 的账号
注册表。同步只建立 `D01/D02` 到 Dola Desktop account id 的 sticky binding；由于账号列表
本身不能证明登录成功，后台不会自动把账号标成 `READY`。

如果账号所有者已经确认对应 Dola 页面登录成功，可由后台记录这一确认（不读取凭据）：

```powershell
.venv\Scripts\python.exe -m app.cli dola-desktop confirm-login D01
.venv\Scripts\python.exe -m app.cli dola-desktop confirm-login D02
```

该状态的 `readiness_basis` 会标记为 `user_confirmed`；它不是服务端额度证明，真实任务仍
必须以 Dola 返回和最终文件 QA 为准。

当前可确认范围：控制平面健康检查、Dola A/B/C 账号发现、独立 partition 绑定和后台激活。
Dola 网页自动提交仍需经过真实请求生命周期验证；服务端返回额度、权限或地区限制时必须
停止，不能用账号轮换规避。

当前三账号状态：`D01/D02=READY`（用户确认），`D03=NEEDS_LOGIN`。D03 是为历史第三账号
建立的新独立槽位，不能从已关闭的 Codex 内置浏览器会话复制登录态；账号所有者需要在
Dola C 页面完成一次正常登录后，再运行：

```powershell
.venv\Scripts\python.exe -m app.cli dola-desktop confirm-login D03
```
