# P1.2 External Chrome/Edge + CDP 验收记录（2026-08-30）

## 当前状态

P1.2 代码与自动化测试已完成；真实外部浏览器验收停在人工登录 Gate。当前没有把未启动的 CDP 或未登录页面当作 PASS。

```text
EXTERNAL_BROWSER_LAUNCH: MANUAL_GATE
CDP_READY: NOT_RUN_WITH_EXTERNAL_BROWSER
PLAYWRIGHT_CDP_CONNECT: NOT_RUN_WITH_EXTERNAL_BROWSER
DOLA_LOGIN_SESSION: MANUAL_REQUIRED
TARGET_CHAT_LOADED: NOT_RUN
CAPTURE_RESPONSE: NOT_RUN
CAPTURE_ENDPOINT: UNKNOWN
MATCHED_FIELDS: []
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

## 自动化验收

```text
python -m pytest
29 passed in 5.63s
python -m compileall -q app tests tools
PASS
python -m app.cli dola-cdp --help
PASS
```

`tools\check_cdp.py` 在外部浏览器尚未由用户启动时返回 `CDP_READY: NO`，这是人工 Gate 尚未执行，不是 CDP 代码失败。

## 用户人工 Gate

1. 双击 `tools\launch_dola_chrome_cdp.bat`；如果 Chrome 不可用则双击 `tools\launch_dola_edge_cdp.bat`。
2. 在专用浏览器中由用户本人完成 Dola 登录，不向程序提供密码或验证码。
3. 保持浏览器窗口打开，先运行 `tools\check_cdp.py`，确认 `CDP_READY: YES`。
4. 再运行：

```powershell
.venv\Scripts\python.exe -m app.cli dola-cdp --auto-download --discover-network --target-chat "https://www.dola.com/chat/00000000000000000"
```

5. 程序会自动刷新此前两条 15 秒视频所在历史对话，捕获 attach 之后的新响应并执行 Resolver、clean candidate 下载和 ffprobe。

完成首次登录后，也可以采用后台模式：关闭可见专用浏览器，双击 `tools\launch_dola_chrome_cdp_background.bat`（或 Edge 版本），再执行同一条 `dola-cdp` 命令。后台模式只能复用已经建立的专用 Profile，不能承担首次登录。

## 验收边界

只有 `CAPTURE_RESPONSE=PASS`、`FOUND_CLEAN_CANDIDATE=YES`、`DOWNLOAD_CLEAN_SOURCE=PASS` 和 `FFPROBE=PASS` 同时成立，才可判定下载链成立。分辨率必须以下载文件的 ffprobe 为准；`VISIBLE_DOLA_WATERMARK` 在没有代表性帧肉眼复核前保持 `UNVERIFIED`。

P1.2 不会启动或关闭用户的 Chrome/Edge，不会绕过登录、验证码、权限或 403，也不会把播放器预览或超分文件当成原生无水印源。
