# P1.4 AISpace Node Recovery 验收记录（2026-08-30）

## Gate 结论

本轮已使用重启后仍有效的 Codex In-App Browser + Full CDP 和当前 Dola 登录态执行。目标历史会话可以正常加载，但 Dola 当前账号/区域的 AISpace 资源接口返回区域限制，无法合法枚举资源节点，因此本轮没有取得两条 15 秒视频的 `node_id + key/vid`，也没有继续猜测或调用媒体下载接口。

```text
AISPACE_UI_FOUND: NO
AISPACE_ENDPOINT_FOUND: YES
AISPACE_NODE_INFO: FAIL (HTTP 200, business code 710022003, country restricted)
TARGET_CONVERSATION_NODE_MATCH: FAIL

TARGET_NODE_COUNT: 0

SEGMENT_01_NODE_ID: NOT_FOUND
SEGMENT_01_KEY_VID: NOT_FOUND
SEGMENT_02_NODE_ID: NOT_FOUND
SEGMENT_02_KEY_VID: NOT_FOUND

DOLA_VIDEO_GET_PLAY_INFO: NOT_RUN (no valid node key/vid)
DOLA_MEDIA_GET_PLAY_INFO: NOT_RUN (not observed in current UI; no valid node)
AISPACE_GET_DOWNLOAD_INFO: NOT_RUN (no node_id; AISpace access restricted)

FOUND_ORIGINAL_MEDIA_INFO: NO
FOUND_CLEAN_CANDIDATE: NO
SEGMENT_01_NATIVE_RESOLUTION: UNKNOWN
SEGMENT_02_NATIVE_RESOLUTION: UNKNOWN
SEGMENT_01_VISIBLE_WATERMARK: YES (current text download URL contains video_gen_watermark_dyn)
SEGMENT_02_VISIBLE_WATERMARK: YES (current text download URL contains video_gen_watermark_dyn)
DOWNLOAD_SEGMENT_01: NOT_AVAILABLE
DOWNLOAD_SEGMENT_02: NOT_AVAILABLE
```

## 实机过程与证据

目标对话：

```text
https://www.dola.com/chat/00000000000000000
```

页面与登录态：

```text
CODEX_IN_APP_BROWSER: PASS
FULL_CDP: PASS
DOLA_LOGIN_SESSION: PASS
TARGET_CHAT_LOADED: PASS
```

目标会话通过左侧历史链接进入后，页面确实显示：

```text
第一段（0-15 秒）
第二段（15-30 秒）
```

两条页面下载入口均为 `v16-dola.dola.com`，并包含：

```text
lr=video_gen_watermark_dyn
```

因此它们只能标记为带水印预览/下载入口。

### UI 资源入口检查

已检查当前页面的：

```text
AI 创作
视频模式
账号菜单
项目菜单
```

没有出现：

```text
我的创作
作品
资源
文件
Space
AI Space
历史创作
```

### 真实 AISpace 接口探测

当前前端实际访问/暴露了以下接口路径：

```text
/samantha/aispace/homepage
/samantha/aispace/node_info
/samantha/collection/list
```

使用当前页面同源会话执行根节点和首页探测，未读取 Cookie、Profile 或密码：

```text
/samantha/aispace/node_info
HTTP: 200
business_code: 710022003
message: country restricted

/samantha/aispace/homepage
HTTP: 200
business_code: 710022003
message: country restricted
```

返回没有节点列表、`conversation_id`、`node_id` 或 `key`，所以不能建立：

```text
00000000000000000 → video node
```

### Full CDP 目标页刷新复核

在目标对话页启用 `Network` 后刷新并读取完整事件快照，当前页面实际产生的动态请求中没有：

```text
/im/chain/single
/samantha/aispace/*
/samantha/video/get_play_info
/samantha/media/get_play_info
/samantha/aispace/get_download_info
```

也没有发现包含 `fallback_api`、`video_list`、`original_media_info` 或 `key_seed` 的响应。WebSocket 只有连接握手和 2 字节心跳帧，没有目标媒体数据。页面 DOM 没有视频播放器、`data-node-id`、`data-node-key`、`data-vid` 或 `data-video-id` 属性。

### 官方收藏夹/集合列表复核

通过账号菜单进入 Dola 官方 `my-collection` 页面，页面自身触发了：

```text
POST /samantha/collection/list
HTTP: 200
```

返回的集合数量为 4，内容是示例收藏（YouTube、网页和 PDF 等），不包含目标标题“雨夜巷道武术对决”，也不包含目标 `conversation_id=00000000000000000`。该列表响应没有形成视频资源节点映射，因此不能替代 AISpace 节点恢复。

这说明当前登录态本身有效，但目标资源索引没有通过当前可用的官方页面/接口暴露；阻塞点是 Dola 服务侧 AISpace 地区限制与历史消息扁平化，不是内置浏览器登录失败。

本轮结果已写入：

```text
captures\\codex-cdp\\target-video-nodes.json
```

## 当前版本接口线索

只读检查 Dola 当前前端模块确认存在：

```text
POST /samantha/video/get_play_info
```

前端使用形式为：

```text
{ vid }
→ data.play_infos[0].main / backup
```

但目标历史文本消息没有合法视频 `vid`，而 AISpace 又被区域限制拦截，因此本轮不发送随机 VID，也不把页面中的非视频 `v...` 字符串当作 VID。

## 已验证边界

本轮没有：

1. 修改 `watermark_dyn` URL 参数；
2. 枚举随机 `vid` 或他人 `node_id`；
3. 绕过区域限制、403、登录或验证码；
4. 导出 Cookie、浏览器 Profile、密码或签名材料；
5. 把带水印链接或另一条历史视频的 clean 结果冒充本次两条目标视频。

## 结论

P1.4 的“资源节点反查”逻辑已执行到真实服务边界，但当前会话在 AISpace 根节点阶段被服务端区域限制阻断。当前不能证明 Dola 为这两条视频提供了可访问的 clean rendition，也不能证明 clean rendition 不存在。

若继续，必须在 Dola 官方允许 AISpace/我的创作访问的正常账号或区域中重新执行同一 P1.4 流程；一旦合法返回节点，再按 `node_id + key/vid → get_play_info/get_download_info → 下载 → ffprobe → 首中尾帧检查` 继续。
