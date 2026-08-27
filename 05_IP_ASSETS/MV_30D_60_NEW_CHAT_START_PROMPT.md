# 汤圆音乐映像｜30D/60 下一首 MV 新对话启动词 v2.0

> 用途：每一首“全新 MV”单独开新 ChatGPT 对话。正式入口已切换到 Canonical Runtime + Web Bridge；新对话不再靠聊天记忆或旧 Markdown CURRENT_STATE 自行判断项目状态。

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-web-r3` 分支。

这是「汤圆音乐映像｜30天60条音乐MV」的一首全新、独立 MV。
不要让我重新解释 R1 / R2 / R3，也不要自动继承上一首 MV 的具体人物、场景、道具、色调、构图、故事或已经失效的聊天状态。

本对话的状态权威不是聊天记忆，而是：
Runtime Controller / Web Bridge response > Canonical durable state + receipts > Tracker > Workflow / Rules > Knowledge / History > 聊天记忆。

【启动最小读取】
先读取：
1. `05_IP_ASSETS/ACCOUNT_POSITIONING.md`
2. `05_IP_ASSETS/MV_30D_60_TRACKER.csv`
3. `04_HARNESS/runtime/mv_resume_contract.json`
4. `04_HARNESS/runtime/mv_stage_registry.json`
5. `04_HARNESS/runtime/mv_runtime_bridge_contract.json`
6. `04_HARNESS/runtime_bridge/README.md`

不要一开始把所有 R1 / R2 / R3 历史文档全部读入上下文。只有 Runtime response 指定某个 Stage 后，再按 `jit_reads` 读取该 Stage 所需 Workflow / Rule / Knowledge。

【这是“新 MV”，不要误续旧 slot】
因为本次明确要求新建一首 MV，所以不要先发无 slot 的 RESUME 去自动继续某个仍处于 pre-publish 的 Canonical 历史项目。

先只读 Tracker 和 `06_TESTS/MV/WEB_R3/30D_60/` 下已有 slot 状态足迹，按 Tracker 顺序找第一个候选空槽，候选必须同时满足：
- `status=PLANNED`；
- `song_family` 为空；
- `audio_asset` 为空；
- 不存在该 slot 的 Canonical `00_STATE/CURRENT_STATE.json`；
- 不存在该 slot 待迁移的根级 `CURRENT_STATE.json`。

这里只是找“候选”，不能直接初始化。
随后对该候选 slot_id 创建新的 immutable `RESUME` Web Bridge request，让 Runtime Controller 做最终校验。

只有 response 明确返回：
- `mode=ALLOCATE_NEW_SLOT`
- 正确的 slot_id / lane
- `next_action=INIT_SLOT_AND_PREPARE_HG01`
- 有效的 `next_guard` / ALLOCATION guard
才允许进入初始化。

如果 response 返回 `RESUME_CANONICAL`、`MIGRATION_REQUIRED`、ambiguity、stale 或 error，不得为了“这是新歌”而绕过 Runtime；说明具体冲突并先解决仓库状态。

【初始化】
当 response 为 `ALLOCATE_NEW_SLOT`：
1. 原样使用 response 返回的 slot_id、lane、next_guard；
2. 通过 Web Bridge 创建 `INIT_SLOT` request；
3. 读取 matching response；
4. 只有 Canonical `00_STATE/CURRENT_STATE.json` 与 transition receipt 已由 authoritative controller 落盘，才开始 HG01 machine preflight；
5. 建立 `SONG_CANDIDATE_SET` 后停在 HG01，让我做人类选歌审美决策。

任何 mutation 都必须使用上一份最新 response 返回的 guard；guard stale 时重新 RESUME，禁止继续重放旧请求。
Request / response 都是 durable evidence；已处理 request 不得修改。

【正常生产 Runtime】
固定 Stage 主线由 `mv_stage_registry.json` / `mv_resume_contract.json` 决定，不靠聊天自行跳步。
正常人工 Gate 只有：
- HG01：选歌审美；
- HG02：BGM 试听锁定；
- HG03：首帧整组 / 视觉方向；
- HG04：Picture Edit 节奏；
- HG05：最终验收。

真实人工决定必须先通过 `RECORD_HUMAN_GATE` 写 durable receipt，成功后再用新 guard 单独 `ADVANCE`。聊天里一句“OK”本身不等于 Canonical Gate PASS。

每完成一个 machine Stage：
- 先生成该 Stage 所需 durable artifact；
- 由 Runtime Validator / State Controller 验证；
- 只有 transition receipt 真正落盘，才算 Stage 前进。

【30D/60 固定生产原则】
- 账号前台身份固定为「汤圆音乐映像」；普通 MV 的标题、封面、包装默认不主动强调 AI；
- 当前生产目标约60条 / 30天，Lane P=Primary/Trend，S=Stable/Fast，R=Camera/Director R&D；
- 不允许每条都复制 R&D 的研发成本；稳定生产优先复用已验证 correctness；
- BGM 默认 Douyin-native exact asset first；
- HG02 锁定后必须先完成并 PASS `AUDIO_TIMELINE_PACKAGE`，才能进入任何 time-dependent Director 工作；
- 每句歌词先找不可替代的视觉答案：歌词视觉命中 > 轻叙事连续 > 炫技镜头；
- 环境必须参与叙事，避免整组退化为近景人物写真；
- Dynamic 是 RAW SOURCE，不等于最终5秒成片；TRIM BEFORE REGENERATE；
- 多镜素材由 Runtime Context 决定 atomization / normalization；
- WEB正式 Picture Edit 前必须通过 Source Rough-Cut Gate；AI source audio 默认移除；
- 字幕默认继承已锁 R2 baseline，除非我明确要求重新设计；
- 局部问题 Patch, Don't Cascade；若要推翻已锁上游，用受控 Revision / Rollback，旧证据归档而不是覆盖；
- Publish 必须有真实世界确认，并通过 Publish / Tracker transaction，同步失败不能半提交。

【创意隔离】
上一首或任何历史 MV 的人物身份、面纱/面罩、场景、道具、天气、色调、构图和故事都不是新项目模板。
只允许复用已经晋升为 Workflow / Rule / Gate / Knowledge 的通用生产经验。
R3 Camera / Dynamic 经验只在相关 Stage JIT 读取，不得在 HG01 前预先锁定新歌视觉。

【开始后的回复格式】
完成第一轮 Bridge 校验后，先简洁告诉我：
1. 当前 branch / source SHA；
2. 本次 RESUME request_id 与 response status；
3. Runtime mode；
4. 本条新 MV 被验证的 slot / lane；
5. 当前 Stage / state token；
6. 当前 next_action 与第一个 Human Gate；
7. 如果 BLOCKED，唯一具体阻塞是什么。

如果 response 已允许 `ALLOCATE_NEW_SLOT`，立即完成 INIT_SLOT 和 HG01 machine preflight，然后直接进入 HG01，不要让我重新解释项目背景。
```

## 当前 Runtime 切换说明

- 本文件 v2.0 取代 v1 的“聊天自行建立 slot / 更新 CURRENT_STATE”方式。
- 新 MV 入口必须先经过 Web Bridge 的 read-only RESUME 校验，再通过 guard 驱动 INIT_SLOT。
- 通用“继续现有项目”仍可使用无 slot RESUME；本文件专门用于“全新 MV”，因此采用显式空槽候选 + Runtime 最终校验，避免误续历史 Canonical slot。
- Legacy 项目只能按其 durable evidence 边界受控迁移，不允许从成片或旧聊天反向补造缺失 Stage。
