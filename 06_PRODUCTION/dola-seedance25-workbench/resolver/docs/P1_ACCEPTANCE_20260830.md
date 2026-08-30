# P1 Browser Capture 验收记录（2026-08-30）

## 实施结果

P1 接入代码已完成，离线桥接与自动化测试通过；真实浏览器捕获未通过，原因是当前可用浏览器只有 Codex 内置浏览器，没有 Chrome/Edge 扩展安装或 `chrome.debugger`/`Fetch` 能力，且没有已加载本扩展的用户标签页。

## 验收字段

```text
CAPTURE_CHAIN_SINGLE: FAIL
FOUND_FALLBACK_API: NO
FOUND_VIDEO_LIST: NO
FOUND_CLEAN_CANDIDATE: NO
HIGHEST_NATIVE_RESOLUTION: UNKNOWN
DOWNLOAD_CLEAN_SOURCE: NOT_AVAILABLE
VISIBLE_DOLA_WATERMARK: UNVERIFIED
```

这些值表示本次没有拿到真实 capture JSON，不表示真实 Dola 后端一定没有 clean candidate。

## 已通过的本地验收

```text
python -m pytest
12 passed in 4.17s

python -m app.cli capture-server --out output\bridge-smoke --no-fetch-fallback
GET http://127.0.0.1:8765/health
{"ok":true}
```

覆盖项目：bridge health、POST capture、非法 host、非法 endpoint、原始 JSON 保存、自动 resolve、无 clean candidate、403 失败关闭；同时扩展 JavaScript 语法和 manifest JSON 校验通过。

## 已接入能力

- `python -m app.cli capture-server` 默认监听 `127.0.0.1:8765`。
- 每次 capture 精确要求 HTTPS `dola.com`（含子域名）的 `/im/chain/single` 路径。
- 保存本地原始 JSON、脱敏 capture metadata 和 resolve report。
- 默认不自动下载；`--auto-download` 才会调用现有 clean candidate 下载和 ffprobe。
- 默认会尝试显式发现的 `fallback_api`；可用 `--no-fetch-fallback` 关闭。
- 403、无 clean candidate、下载失败均失败关闭，不绕过认证。
- report、日志不输出 URL 查询参数、token、`key_seed` 或 Cookie。
- 扩展仅向 `127.0.0.1:8765` 发送 `/im/chain/single` 响应体，不读取密码、验证码、Cookie 或浏览器存储。

## 当前阻塞与实机步骤

需要在真实 Chrome 或 Edge 中由用户手动加载：

```text
LOCAL_DOLA_PROJECT_ROOT\dola-original-resolver\browser-extension
```

然后启动：

```powershell
python -m app.cli capture-server --auto-download
```

最后用本人已登录 Dola 打开历史视频对话并刷新。出现 `captures\dola_chain_*.json` 后，再以该文件中的 report 和 MP4 进行最终实机验收。当前不把页面上已有的普通下载链接当成 chain/single 捕获证据。
