# P1.4.5 Official Thread Share Recovery 验收报告

日期：2026-08-30
项目：Dola Original Resolver
目标会话：`雨夜巷道武术对决`
目标 Chat：`https://www.dola.com/chat/00000000000000000`

## 验收结论

官方 Thread 分享路线本身可用，但对这条旧历史会话没有恢复出 clean 媒体身份。Thread 页提供的是完整消息快照和两条原有 `video_gen_watermark_dyn` 下载链接，没有新增 `fallback_api`、`video_list`、`key_seed`、`vid` 或 `node_id`。

```text
OFFICIAL_SHARE_ACTION: PASS
DOLA_THREAD_URL_FOUND: YES
THREAD_PUBLICLY_LOADABLE: YES_IN_CURRENT_LOGIN_SESSION
ANONYMOUS_PUBLIC_ACCESS: UNVERIFIED

ROUTER_DATA_FOUND: YES
SHARE_INFO_FOUND: YES
MESSAGE_SNAPSHOT_FOUND: YES
TARGET_VIDEO_BLOCKS_FOUND: 2

THREAD_FALLBACK_API_FOUND: NO
THREAD_KEY_SEED_FOUND: NO
THREAD_VIDEO_LIST_FOUND: NO
THREAD_VID_FOUND: NO

RESOLVER_RUN: PASS
FOUND_CLEAN_CANDIDATE: NO
HIGHEST_NATIVE_RESOLUTION: UNKNOWN
HIGHEST_BITRATE: UNKNOWN

DOWNLOAD: NOT_AVAILABLE
FFPROBE: NOT_RUN
VISIBLE_DOLA_WATERMARK: UNVERIFIED
```

## 官方分享动作

已在目标 Chat 中通过右上角官方分享按钮创建分享，没有手工猜测 share-id。Dola 官方接口均返回成功：

```text
/im/message/share/share_token: HTTP 200
/im/message/share/save: HTTP 200
```

实际 Thread 链接已保存至：

[target-thread-url.txt](../captures/thread/target-thread-url.txt)

本次生成的 Thread：

`https://www.dola.com/thread/xnPflk9Q4BnZ2uQKQ`

## Thread 页面三路检查

使用 Codex In-App Browser + Full CDP 打开 Thread，并刷新后检查：

```text
window._ROUTER_DATA: FOUND
loaderData: FOUND
shareInfo: FOUND
Hydration mergeLoaderData script: FOUND
Hydration router-data script: FOUND
message_snapshot.message_list: FOUND
message_list length: 3
```

Thread Hydration 数据中包含：

```text
share_info
message_snapshot
message_snapshot.message_list
creation_block
```

但页面加载期间的 Dola Network JSON/HTML 数据没有出现 clean 媒体身份接口。网络上只观察到 Thread 文档自身，没有 `fallback_api`、`video_list`、`key_seed`、`get_play_info` 或 `get_download_info` 响应。

## 两段旧视频匹配结果

在官方 Thread 的 `message_snapshot.message_list` 中，递归扫描明确识别到 2 个目标视频块，分别对应原会话的：

```text
第一段：0-15 秒
第二段：15-30 秒
```

两段链接都明确带有：

```text
lr=video_gen_watermark_dyn
```

因此它们被记录为水印候选并拒绝进入 clean 下载流程。没有修改 URL、没有猜测 `vid`、没有跨区域请求，也没有把 `lr` 参数替换成其他值。

## P0 Resolver 结果

Thread payload 已交给现有 P0 Resolver：

```text
status: clean_source_not_available
candidate_count: 3
clean_candidate_count: 0
fallback_api_count: 0
video_list_count: 1 (由两个明确 Thread 文本链接组成的原始水印集合)
key_seed_present: false
selected clean source: none
```

P0 的 fail-closed 行为符合预期：Thread 中只有带水印链接时，不会自动下载并声称无水印。

## 为什么没有继续下载 A 侧

任务要求的 A 侧是 Chat/Thread 当前水印下载，B 侧是 Thread Resolver clean candidate。本轮 B 侧没有 clean candidate，因此没有用下载器主动下载水印源，也没有对水印文件做伪装成 clean 的 A/B 结论。两个链接已经被完整识别，且其 rendition 标记明确为 `watermark_dyn`。

## 最终判断

```text
P1.4.5 Official Thread URL: PASS
P1.4.5 Thread message recovery: PASS
P1.4.5 Two target video blocks: PASS
P1.4.5 Clean media identity recovery: FAIL
P1.4.5 Clean download: NOT_AVAILABLE
```

这说明官方 Thread 分享页绕过了 Chat 页的展示层，但没有绕过这两条旧视频已经被 Dola 扁平化为水印链接的事实；当前也没有通过 Thread 暴露更深的媒体身份。旧视频的 clean 恢复仍然受到当前账号/区域的 AISpace 限制，不是 P0 Resolver 或 Thread 解析代码故障。

相对地，P1.5 新生成测试已经证明“生成结果完成链路 → 显式 vid → fallback_api → clean candidate → 下载 → FFprobe → 视觉检查”可以成立。因此后续最可靠的生产路线仍是生成时捕获媒体身份，而不是继续从这两条旧水印 URL 反推。

## 证据目录

```text
captures/thread/target-thread-url.txt
captures/thread/share-actions.json
captures/thread/network-index.json
captures/thread/thread-http-response.html
captures/thread/router-data.json
captures/thread/router-hits.json
captures/thread/hydration-scripts.json
captures/thread/thread-router-args.json
captures/thread/share-info.json
captures/thread/message-snapshot.json
captures/thread/message-summary.json
captures/thread/thread-media-hits.json
captures/thread/resolver-input.json
captures/thread/resolver-report.json
```
