# P1.1 Playwright Persistent Browser 验收记录（2026-08-30）

## 最终结论

P1.1 实现：**PASS**。针对之前两条 15 秒视频所在历史对话的真实捕获：**未完成**，阻塞在当前执行环境禁止启动 headed Chromium GUI，且独立 profile 没有可复用的登录态；不是 Resolver 或捕获代码的测试失败。

## 实机字段

```text
PLAYWRIGHT_BROWSER_LAUNCH: FAIL
PERSISTENT_PROFILE: PASS
DOLA_LOGIN_SESSION: MANUAL_REQUIRED
CAPTURE_RESPONSE: FAIL
CAPTURE_ENDPOINT: UNKNOWN
FOUND_FALLBACK_API: NO
FOUND_VIDEO_LIST: NO
FOUND_QAAB: NO
FOUND_CLEAN_CANDIDATE: NO
HIGHEST_NATIVE_RESOLUTION: UNKNOWN
HIGHEST_BITRATE: UNKNOWN
DOWNLOAD_CLEAN_SOURCE: NOT_AVAILABLE
DOWNLOAD_METHOD: NONE
FFPROBE: NOT_RUN
VISIBLE_DOLA_WATERMARK: UNVERIFIED
```

测试目标对话：`https://www.dola.com/chat/00000000000000000`，用于承载此前两条 15 秒视频。headed 启动实际返回 `spawn UNKNOWN`；headless 使用同一独立 profile 等待 20 秒，未产生 `/im/chain/single` 捕获。没有代填登录，也没有把未登录页面当成历史视频捕获。

脱敏 Network Discovery 唯一命中：

```text
POST www.dola.com /samantha/user/ab/get 200 application/json
matched_fields: video_model
```

该响应不是视频元数据，不能据此推断 fallback_api、video_list 或 clean candidate 存在。原始响应正文未写入 Discovery 报告。

## 已完成实现

- `app/capture/browser_session.py`：独立 `runtime/dola-browser-profile`、headed/headless 参数、profile 占用错误处理、手动登录提示。
- `app/capture/playwright_browser.py`：P1.1 对外入口。
- `app/capture/response_capture.py`：`BrowserContext.on("response")`、Dola 精确 host/path、完整响应体读取、UTF-8/charset 处理、相关字段过滤、raw bytes debug、Network Discovery。
- `app/download/authenticated.py`：普通 HTTP 403 后仅使用同一 Playwright Context 的 `context.request`，不伪造 Authorization；仍 403 失败关闭。
- `app/cli.py`：`python -m app.cli dola-browser [--auto-download] [--discover-network]`。
- `browser-extension/`：原 P1 扩展方案保留为备用，不作为默认路径。

## 自动化验收

```text
python -m pytest
22 passed in 5.98s

node --check browser-extension/service-worker.js
PASS
```

覆盖了 persistent profile、Dola/non-Dola URL、相关响应过滤、中文 UTF-8、capture 保存、自动 resolve、Network Discovery 脱敏、Playwright Context 下载 fallback 和 403 fail-closed。

## 运行命令

headed 首次登录：

```powershell
cd LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver
.\.venv\Scripts\python.exe -m app.cli dola-browser --auto-download --discover-network
```

如果 headed 环境可启动，用户本人在窗口中登录 Dola，打开自己已完成的视频对话并刷新即可。原始响应会写入 `captures/`，报告和下载结果也写在同一输出目录。

## 安全边界

不读取或导出浏览器 Profile 文件、Cookie、密码、验证码、Passkey；不自动点击生成、不绕过 Google OAuth、付费、额度、权限或 403；不修改请求、不擦除水印、不把超分结果冒充原生分辨率。Profile 和 capture 输出目录已加入 Git 忽略。
