# P1.5 Generation-Time Capture 验收报告

日期：2026-08-30
项目：Dola Original Resolver
浏览器：Codex In-App Browser + Full CDP
测试范围：新生成的一条短视频；不恢复 P1.4 的两条旧视频，不使用外部 Chrome、9222、Playwright 或扩展。

## 结论

本次测试证明：同一账号新生成的视频，可以从完成后的 Dola chain 响应中恢复真实媒体身份，并通过现有 Resolver 找到 clean candidate，完成原文件下载和 FFprobe 验证。

最终结果：

```text
FULL_CDP: PASS
CAPTURE_ARMED_BEFORE_GENERATION: PASS
GENERATION_MEDIA_IDENTITY_CAPTURE: PASS
VID_FOUND: YES
FALLBACK_API_FOUND: YES
VIDEO_LIST_FOUND: YES
KEY_SEED_FOUND: YES
FOUND_CLEAN_CANDIDATE: YES
DOWNLOAD: PASS
FFPROBE: PASS
VISIBLE_DOLA_WATERMARK: NO (首帧/中帧/尾帧抽检)
```

## 本次生成

生成前已安装页面只读 fetch/XHR/SSE/WebSocket capture hook，并在提交前确认已 armed：

```text
armed_at: 2026-08-30T03:30:52.225Z
generation_started_at: 2026-08-30T03:32:51.824Z
completion_observed_at: 2026-08-30T03:40:07.465Z
conversation_id: 00000000000000000
```

实际提示词为：

```text
一只橙色小猫在雨后的城市窗台上抬起前爪轻轻挥手，固定中近景，柔和自然光，动作连贯，画面干净，无文字、无标志。
```

Dola 页面在提交后提示其将请求调整到 5 秒，但最终下载文件的 FFprobe 时长为 10.08 秒；验收以文件级 FFprobe 为准，没有用页面文案替代媒体事实。

## 媒体身份恢复

完成后的同一对话重新通过 Dola 自己的站内导航打开，Full CDP 捕获到：

```text
POST/response: /samantha/aispace/homepage
POST/response: /im/chain/single
HTTP status: 200
response body: successfully read by Network.getResponseBody
```

Resolver 从本次 bundle 中恢复：

```text
vid: v186a3gm000cda9qa0nog65niljl4vcg
message_id: FOUND
conversation_id: FOUND
media_key: FOUND
node_id: NOT_FOUND
fallback_api: FOUND
key_seed: FOUND
video_list: FOUND
original_media_info: NOT_FOUND
get_play_info: NOT_AVAILABLE
```

严格规则下，仅有 `video_model` 不会通过；本次是因为捕获到符合格式的显式 `vid`，并同时处在视频媒体响应结构中，所以身份门通过，没有猜测 vid。

## Resolver、下载与文件 QA

不请求 fallback 时，本次 chain 响应只有带水印/预览类候选，clean candidate 为 0。对捕获到的 `fallback_api` 做一次诊断请求后：

```text
resolver status: success
candidate_count: 75
clean_candidate_count: 1
highest clean resolution: 1280x720
highest clean bitrate: 5781161 bps
```

下载文件：

[generation_v186a3gm000cda9qa0nog65niljl4vcg_attempt2.mp4](../captures/generation/20260830_033051/downloads/generation_v186a3gm000cda9qa0nog65niljl4vcg_attempt2.mp4)

```text
bytes: 7,284,263
sha256: 2AFE159D8E1CCEFA4A898296997B39E580DD29486E850D7912C2BF3975FCA3C1
container: MP4
video: H.264, 1280x720, 24 fps, 5628954 bps
audio: AAC, 130647 bps
duration: 10.080000 s
format bitrate: 5781161 bps
reencoded: NO
```

抽取并检查了以下三个画面：

```text
captures/generation/20260830_033051/qa_frames/frame_000.jpg
captures/generation/20260830_033051/qa_frames/frame_005.jpg
captures/generation/20260830_033051/qa_frames/frame_last.jpg
```

三个抽检画面均未观察到 Dola AI 可见水印。该结论是视觉抽检结论，不把字段名 `unwatermarked` 当作唯一证明。

## 重要边界

本轮实时生成期间的 hook 已在提交前 armed，且在第一次轮询中观察到 fetch/XHR/SSE 活动；但浏览器连接在原始实时缓冲写盘前发生了后台重置。因此：

```text
GENERATION_TIME_CAPTURE_RAW_PERSISTED: PARTIAL
POST_COMPLETION_CHAIN_REFRESH: PASS
```

本地 bundle 保存的是同一条新生成视频完成后的 `/im/chain/single` 完整响应、媒体命中信息、Resolver 输入、下载文件和 FFprobe 结果；报告没有把这次补捕获冒充为完整的实时 SSE 原始归档。下一轮若要求完全实时归档，应在浏览器进程外增加持续落盘通道，再提交生成任务。

另外，clean candidate 本次来自捕获到的历史 fallback API 路由。由于 AISpace 资源枚举仍受当前 Dola 区域限制，不能把这次结果表述为 AISpace 官方生产路由已恢复；它证明的是：在当前账号/当前生成结果上，fallback 身份链可以实际导出一个通过文件级和视觉 QA 的 clean MP4。

## 证据目录

```text
captures/generation/20260830_033051/network-index.json
captures/generation/20260830_033051/xhr-events.jsonl
captures/generation/20260830_033051/raw-responses.jsonl
captures/generation/20260830_033051/identity-chain.json
captures/generation/20260830_033051/media-hits.json
captures/generation/20260830_033051/resolver-input.json
captures/generation/20260830_033051/generation-report.json
captures/generation/20260830_033051/downloads/ffprobe-report.json
```
