# P1.3 Codex In-App Browser + Full CDP 验收记录（2026-08-30）

## Gate 结论

Full CDP 已在重启后的 Codex In-App Browser 中可用，Dola 登录态也可用。正确通过左侧历史会话链接进入 `雨夜巷道武术对决` 后，页面显示第一段（0-15 秒）和第二段（15-30 秒）。

本轮未取得这两段视频的无水印原始媒体元数据，因此**不能宣布 clean source 链路成立**。当前页面暴露的两个下载 URL 都明确带有 `lr=video_gen_watermark_dyn`，只能作为带水印预览/下载入口。

```text
CODEX_IN_APP_BROWSER: PASS
FULL_CDP_AVAILABLE: YES
NETWORK_DOMAIN: PASS
RUNTIME_DOMAIN: PASS
PAGE_DOMAIN: PASS
NETWORK_RESPONSE_BODY: PASS (命令可调用；部分刷新响应正文为空)
TARGET_CHAT_LOADED: PASS (通过侧栏历史会话链接进入)
DOLA_LOGIN_SESSION: PASS

CAPTURE_RESPONSE: PASS (Full CDP 与页面会话请求均可读取)
CAPTURE_ENDPOINT: /im/chain/single; /samantha/video/get_play_info discovered
MATCHED_FIELDS: media / messages / content_block (目标消息未出现 clean-media 字段)
FOUND_FALLBACK_API: NO
FOUND_VIDEO_LIST: NO
FOUND_QAAB: NO
FOUND_CLEAN_CANDIDATE: NO
HIGHEST_NATIVE_RESOLUTION: UNKNOWN (clean source unavailable)
HIGHEST_BITRATE: UNKNOWN (clean source unavailable)
DOWNLOAD_CLEAN_SOURCE: NOT_AVAILABLE
DOWNLOAD_METHOD: NONE
FFPROBE: NOT_RUN (clean source unavailable)
VISIBLE_DOLA_WATERMARK: YES (URL token indicates watermark; pixels not independently rechecked in this P1.3 run)
```

## 实机证据

目标对话：

```text
https://www.dola.com/chat/00000000000000000
```

关键 Full CDP 能力调用结果：

```text
Network.enable: PASS
Runtime.evaluate: PASS
Page.enable: PASS
Network.responseReceived/loadingFinished: PASS
Network.getResponseBody: PASS (可读；对目标刷新批次出现 0 字节正文的响应)
```

直接使用 URL 打开时，Dola 主区域仍停留在空白新对话状态；通过侧栏点击 `雨夜巷道武术对决` 后，目标内容才真正加载。这是本轮此前误判为“登录/捕获失败”的主要原因。

正确加载后的页面显示两条下载入口：

```text
点击下载第一段：v16-dola.dola.com，lr=video_gen_watermark_dyn
点击下载第二段：v16-dola.dola.com，lr=video_gen_watermark_dyn
```

页面 Router 数据与内嵌数据已递归检查：

```text
target video vid: NOT_FOUND
fallback_api: NOT_FOUND
video_list: NOT_FOUND
original_media_info: NOT_FOUND
key_seed: NOT_FOUND
```

当前版本前端静态模块确实包含：

```text
POST /samantha/video/get_play_info
参数：{ vid }
返回使用：data.play_infos[0].main 或 backup
```

但这条历史消息是普通文本下载链接，不是带 `vid` 的结构化视频块；页面中唯一匹配 `v...` 的字符串来自头像 URL，不能当作视频 ID 使用。未经有效 `vid`，不继续猜测或改写水印 URL。

## 已验证但不是目标视频的捕获

早先对页面历史列表响应的 Full CDP 捕获已成功交给本地桥接服务，证明“内置浏览器 → Full CDP → 本机 Resolver → 下载 → ffprobe”技术链可运行；但它选中了另一条 10.1 秒、720×1280 的视频，不属于本次两条 15 秒目标视频，故不计入目标验收。

相关目录：

```text
captures\\codex-cdp\\
```

该目录内报告明确保留了 `clean candidate` 与下载成功证据，但报告对应的 VID 不是目标会话的两条 15 秒视频。

## 结论与边界

本轮已证明：

1. 重启后 Full CDP 设置生效；
2. Codex In-App Browser 能复用当前 Dola 登录态；
3. 通过正确的会话选择动作可以加载目标历史对话；
4. Full CDP 能观察网络并调用正文读取接口；
5. 当前目标消息只暴露带水印链接，P1.3 尚未拿到两条 clean source。

本轮没有：

1. 读取 Cookie、密码、浏览器 Profile 或验证码；
2. 尝试 403 绕过、伪造签名或把 `watermark` 参数替换成其他值；
3. 把带水印 CDN 链接标记为无水印原片；
4. 把另一条 10.1 秒历史视频的成功结果冒充本次两条 15 秒目标。

下一步若继续，应从 Dola 的“我的创作/资源节点”或实际结构化视频生成消息中取得合法 `vid/node_id`，再调用当前版本的 `GetPlayInfo` 或 AISpace 下载信息接口；仅凭本条文本中的水印 CDN URL，无法可靠恢复无水印原片。
