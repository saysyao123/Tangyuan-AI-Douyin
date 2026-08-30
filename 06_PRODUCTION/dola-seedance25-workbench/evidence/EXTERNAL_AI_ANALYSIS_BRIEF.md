# Dola Seedance 2.5 问题单｜请外部 AI 深度分析

更新时间：2026-08-30

请把本文件连同本目录的 control-plane/ 和 resolver/ 源码一起分析。请不要建议读取或导出密码、Cookie、Token、浏览器 Profile，也不要建议绕过登录、额度、地区限制、验证码或水印策略。目标是找出当前正常登录会话下“生成任务已被接收，但最终媒体身份没有被观察到”的工程原因，并设计可审计、可恢复的观察方案。

## 一、目标

我们希望在用户本人正常登录的 Dola 账号中，实现以下合法工作流：

~~~text
独立账号 Session Slot
  → 用户确认的 5 秒 Seedance 2.5 生成
  → 生成过程中的媒体身份捕获
  → 真实媒体候选解析
  → 只选择授权返回的原始/clean rendition
  → 下载 MP4
  → FFprobe、SHA-256、首/中/尾帧水印检查
  → 账号/任务账本
~~~

长期目标是两个或多个用户自有 Dola 账号的后台管理和健康感知轮询，但不能把账号轮换用于规避 quota、rate-limit、地区或权限限制。

## 二、项目和实现

### A. Electron 控制平面

- Windows Electron 桌面程序；
- 每个 Dola 账号一个持久化 Chromium partition；
- 一个长生命周期隐藏 BrowserWindow 承载后台任务；
- 控制面是 loopback API + 本地短期 bearer token；
- 账号注册表只保存非敏感别名、slot、状态、统计和 sticky binding；
- 支持任务创建、分配、恢复、捕获落盘和 QA gate；
- 不读写密码、Cookie 或浏览器数据库。

### B. Python Resolver

- 捕获 response/body 和生成时 fetch/XHR/SSE/WebSocket 旁路事件；
- 识别 vid、node_id、key、fallback_api、key_seed、video_list 等媒体身份字段；
- 对候选做清晰度、码率、来源和 clean 特征排序；
- 下载使用临时文件、Content-Length/MP4 头检查、FFprobe、SHA-256 和原子改名；
- 只有真实文件和视觉抽检通过才允许 CLEAN_SOURCE=PASS。

## 三、已经确认的能力

### 本地工程层

以下已通过本地检查或单元测试：

- Electron/TypeScript 控制面健康检查；
- Dola A/B 的独立 persistent partition 和登录态重启保持；
- 账号注册表、slot 唯一性、sticky job binding；
- Durable capture sink（事件即时 flush/fsync）；
- 健康感知 round-robin 的模拟测试；
- 任务恢复、账本、5 秒时长 gate、最低分辨率 gate；
- Resolver、捕获、下载和多账号编排测试；
- 当前 resolver 虚拟环境测试：60 tests passed；
- 当前 desktop npm run check 通过。

### 真实 Dola 观测层

- Codex/In-App Browser 的 Full CDP 能力曾可用；
- Electron 隐藏后台 session 能显示已登录页面，并完成 Dola 视频页参数设置；
- 视频页可选择模型 2.5、5 秒、9:16；
- 用户图像上传成功，contenteditable prompt 成功填写；
- 本轮 /chat/completion 返回 HTTP 200 的 SSE，并产生 FULL_MSG_NOTIFY、STREAM_CHUNK、SSE_REPLY_END；
- Dola 助手回复确认使用 Dreamina Seedance 2.5，预计消耗 2 个视频生成额度，并显示“今日剩余 2 个视频生成额度”；
- 这说明请求至少到达了 Dola 的 agent/creation 层，但不等于底层媒体任务完成。

## 四、最新失败测试：Dola1 + 星河倒影图生视频

### 输入

- 测试账号别名：DOLA_A（公开材料不包含真实账号 ID）；
- 模式：I2V；
- 模型：Seedance 2.5；
- 时长参数：5 秒；
- 比例：9:16；
- 首帧：蓝紫色星空、流星、镜面水面和孤独旅人的竖图；
- 提示词：prompts/dola1_5s_star_reflection_20260830.txt；
- 生成前已 armed capture。

### 观察到的响应

捕获响应 URL 只有以下类型：

~~~text
/im/conversation/batch_get
/im/conversation/info
/im/chain/single
/chat/completion
/im/message/mark_conv_read
~~~

/chat/completion 是 text/event-stream，HTTP 200。SSE 中观察到：

~~~text
SSE_ACK
FULL_MSG_NOTIFY
STREAM_CHUNK
SSE_HEARTBEAT
SSE_REPLY_END
~~~

助手语义内容为：

~~~text
我将为您生成一个 9:16 的竖版视频，时长为 5 秒。
本次使用 Dreamina Seedance 2.5 生成，将消耗 2 个视频生成额度，预计等待 1-3 分钟。
视频生成好后，我会主动发送给你，今日剩余 2 个视频生成额度。
~~~

扩展字段包含：

~~~text
has_video_gen=1
image_attachment_num=1
ratio=9:16
model=seedance_v2.5
duration=5
disable_regen=1
task_id=""
~~~

### 180 秒后的实际结果

~~~text
generationSubmitted: true
captureArmedBeforeGeneration: true
task state: failed
error: background generation timed out before media identity was captured
MP4 count: 0
~~~

脱敏后的身份扫描结果：

~~~text
response_count=16
conversation_id_found=true
message_id_found=true
task_id_found=false
generation_id_found=false
vid_found=false
node_id_found=false
media_key_found=false
fallback_api_found=false
key_seed_found=false
video_list_found=false
original_media_info_found=false
media_info_found=false
main_url_found=false
identity_pass=false
~~~

### 重要判断

这次不是登录失败，也不是本地表单未提交：页面已登录、参数设置成功、图片和 prompt 已进入请求、Dola SSE 已确认生成意图。当前失败点是：在等待窗口内没有观察到最终媒体身份或完成消息。

但也不能据此宣称 Dola 服务端一定已经完成生成，因为当前证据没有真实 MP4，也没有后续完成事件。需要区分 agent acknowledgement、provider task accepted、provider completed、media delivered 四个层级。

## 五、前一次成功证据：为什么不能直接外推

另一条较早的用户自有账号测试曾得到：

~~~text
实时捕获前 armed：PASS
生成后 /im/chain/single：HTTP 200，body 可读
显式 vid：FOUND
fallback_api：FOUND
key_seed：FOUND
video_list：FOUND
clean candidate：1
下载：PASS
文件：MP4，1280×720，24 fps，10.08 s，约 5.78 Mbps
FFprobe：PASS
首/中/尾帧可见 Dola 水印：未观察到
~~~

这条证据证明过一条可行的身份链：

~~~text
生成结果/chain
  → 显式 vid + fallback_api
  → Resolver
  → clean candidate
  → 原文件下载与 QA
~~~

它不能证明：

- 当前星河图请求一定完成；
- 5 秒请求一定输出 5 秒，前一次实际是 10.08 秒；
- fallback_api 是官方稳定生产接口；
- AISpace 当前可用；
- 每个账号剩余额度或每天可做几条；
- 多账号真实 round-robin 已通过。

## 六、历史视频和 AISpace 分支

两条旧视频所在历史会话的资源反查曾在 AISpace 节点枚举前收到服务端：

~~~text
710022003 country restricted
~~~

因此旧视频的 node_id → key/vid → play_info/download_info 链没有被完整验证。当前结论是 BLOCKED_BY_REGION_RESTRICTION，不是“旧视频没有 clean source”。

## 七、多账号当前状态

公开导出使用别名：

~~~text
DOLA_A / slot S01：控制面已建立；登录态曾由用户手动完成；本轮生成测试使用此槽位
DOLA_B / slot S02：独立 persistent partition；登录隔离/后台激活已验证
DOLA_C / slot S03：历史上有独立槽位设计，但不作为本轮两个账号验收对象
~~~

已经通过的是“会话容器与编排层”。尚未通过的是：

~~~text
REAL_MULTI_ACCOUNT_DOLA_SESSIONS: NOT_FULLY_VERIFIED
REAL_ROUND_ROBIN_GENERATION: NOT_RUN
PER_ACCOUNT_5S_CAPACITY: UNKNOWN
~~~

Full CDP 当前不能创建新的 BrowserContext；普通多 Tab 不等于账号隔离。因此多账号生产应继续使用 Electron 独立 partition，而不是把一个浏览器的多个 Tab 当作多账号。

## 八、请外部 AI 重点回答

1. /chat/completion 在这里更像 agent acknowledgement + streaming text。根据当前响应路径和源码，真实视频完成结果最可能通过什么机制继续到达：后续 /im/chain/single、conversation polling、WebSocket、SSE 重连、service worker，还是另一个 host/endpoint？
2. task_id="" 同时出现 has_video_gen=1、disable_regen=1 和“消耗 2 个额度”的含义是什么？它更像工具调用未返回 ID、异步任务未创建、Dola 前端刻意隐藏 ID，还是我们在错误的响应层监听？
3. im/conversation/batch_get、im/conversation/info、im/chain/single 在生成后应如何安全地增量轮询和判定完成？需要哪些字段作为状态机条件，才能避免把 assistant loading 文本当成视频完成？
4. 180 秒是否只是本地超时过短？请提出一个可恢复的等待策略：例如有上限的延长、退避轮询、页面保持活动、重连后从 conversation cursor 恢复，以及每个阶段的超时和证据文件。
5. 前一次成功链出现 vid + fallback_api + key_seed + video_list，本次只有 conversation/message 字段。请对比两个代码路径，指出捕获窗口、页面导航、结果刷新、response body 读取或任务绑定的最可能差异。
6. 在不绕过平台策略的前提下，如何区分：请求被 Dola 接收、额度被预扣、provider 任务创建、provider 任务失败、视频完成、媒体 URL 可授权下载？请给出明确事件/字段/文件级验收表。
7. 前一次输出为 1280×720、10.08 秒，而 UI 请求是 5 秒。应如何以 FFprobe 实际时长为准，建立 5 秒/10 秒参数与 provider 实际输出的回归矩阵？
8. fallback candidate 的“clean”只能由下载后的文件和视觉抽检确认。请审查 Resolver 的候选排序，指出哪些字段只能算线索，哪些条件必须拒绝，如何避免把带水印预览误判为原文件。
9. 对两个 Electron persistent partitions，如何设计单 Worker 串行 round-robin 的真实验收：账号绑定、登录健康、每条成本、成功/失败原因、冷却和暂停规则应记录什么？
10. 对“每个账号 5 秒能做几个”的问题，给出严格的测量方案，不要从页面提示或本地计数器推导容量；需要怎样的逐条成功证据和停止条件？

## 九、希望得到的最终输出

请按以下格式给出分析：

~~~text
ROOT_CAUSE_RANKING:
  P0:
  P1:
  P2:

EVIDENCE_GAPS:
  -

MINIMAL_SAFE_PATCHES:
  - file / function / change / why

OBSERVATION_ONLY_TEST_PLAN:
  step 1:
  step 2:

EXPECTED_NEW_ARTIFACTS:
  -

PASS_FAIL_RULES:
  -

WHAT_MUST_NOT_BE_DONE:
  -
~~~

## 十、当前不能宣布的结论

~~~text
当前星河倒影这条 Dola1 任务：
  生成完成：UNKNOWN
  真实媒体身份：FAIL（未捕获）
  clean source：NOT_AVAILABLE
  下载：NOT_RUN
  FFprobe：NOT_RUN
  无水印：UNVERIFIED
  5 秒能力：UNVERIFIED
~~~
