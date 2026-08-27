# Template｜MV Zero-Context Start Prompt v2.0

> 用途：新 ChatGPT / Codex 对话在零聊天上下文下进入 MV Canonical Runtime。Repository + Runtime Controller + durable evidence 是状态权威；聊天记忆不是状态权威。

```text
你现在要执行 `saysyao123/Tangyuan-AI-Douyin` 仓库中的 AI MV Canonical Runtime。

不要让我重新解释 R1 / R2 / R3。不要从聊天记忆、旧总结或上一首 MV 的创意内容猜测当前进度。

【一、启动权威】
开始时只先读取以下最小状态面：
1. `05_IP_ASSETS/ACCOUNT_POSITIONING.md`
2. `05_IP_ASSETS/MV_30D_60_TRACKER.csv`
3. `04_HARNESS/runtime/mv_resume_contract.json`
4. `04_HARNESS/runtime/mv_stage_registry.json`
5. `04_HARNESS/runtime/mv_runtime_bridge_contract.json`
6. `04_HARNESS/runtime_bridge/README.md`

权威顺序固定为：
Runtime Controller / Bridge response > Canonical durable state + receipts > Tracker > Workflow / Rules > Knowledge / History > 聊天记忆。

任何 `CURRENT_STATE`、Human Gate、Context、Rollback、Publish / Tracker transaction 都不得仅靠聊天文字自行宣布完成。

【二、先区分本次意图】
A. 如果用户是在“继续 / 恢复”现有 MV：
- 创建一个新的 immutable `RESUME` Bridge request；
- 用户明确给出 slot_id 时使用该 slot_id；未给出时允许不填 slot_id，由 Resume Controller 按 Canonical Runtime 判断唯一可恢复 slot；
- 如果多个未发布 Canonical slot 冲突，必须 BLOCKED，不得从聊天记忆猜一个。

B. 如果用户明确说这是“一首全新的 / 新建 MV”：
- 不要使用无 slot 的 RESUME 去自动继续旧 Canonical 项目；
- 先只读 Tracker 与 `06_TESTS/MV/WEB_R3/30D_60/` 下现有 slot 状态足迹；
- 选择按 Tracker 顺序出现的第一个满足以下条件的候选：status=`PLANNED`、song_family 为空、audio_asset 为空，并且既不存在该 slot 的 Canonical `00_STATE/CURRENT_STATE.json`，也不存在待迁移的根级 `CURRENT_STATE.json`；
- 这一步只是提出“候选 slot”，不是授权；随后必须对该候选 slot_id 创建 immutable `RESUME` request，让 Runtime Controller 做最终校验；
- 只有 response 明确返回 `mode=ALLOCATE_NEW_SLOT` 才允许初始化；否则以 response 为准并停止自行分配。

【三、Web Bridge 是控制面】
所有 Web 端状态读取 / mutation 走 `04_HARNESS/runtime_bridge/requests/*.json` -> GitHub Actions -> `responses/*.json`。

每次 request：
- 使用唯一 request_id；
- request 一旦得到 response 后不可修改；
- 先读取 matching response 再决定下一步；
- mutation 必须原样携带最新 response 返回的 `next_guard` / expected guard；
- stale guard 被拒绝时，不得重放旧请求；先重新 RESUME 获取新 truth；
- 禁止任意 shell、任意 repo path mutation 或绕过 authoritative controller。

`RESUME` 可能返回：
- `RESUME_CANONICAL`：从 response 的 current_stage / current_state_token / next_action 继续；
- `ALLOCATE_NEW_SLOT`：使用 response 返回的 slot_id / lane / next_guard 创建 `INIT_SLOT`；
- `MIGRATION_REQUIRED`：立即停止生产推进，只做受控 legacy migration；不得从旧成片、聊天或旧 CURRENT_STATE 反推 S05+；
- error / ambiguity / invalid state：BLOCKED，先解决具体仓库冲突。

【四、初始化与 Stage 前进】
如果 response 为 `ALLOCATE_NEW_SLOT`：
1. 原样使用其 slot_id、lane 和 ALLOCATION guard；
2. 通过 Bridge 提交 `INIT_SLOT`；
3. 读取 matching response；
4. 只有 Canonical state 已真实落盘后，才创建 HG01 所需 machine artifact；
5. 到 HG01 停止并等待真实人工选择。

每个 Stage 都只执行 response `next_action` 指定的工作，并只 JIT 读取 response 指定的 `jit_reads`。
不要在启动阶段把所有旧 R1/R2/R3 文档一次性塞进上下文。

Human Gate 固定为 HG01–HG05：
- 真实用户决定先通过 `RECORD_HUMAN_GATE` 写 durable receipt；
- Gate receipt 成功后，再用新的 guard 单独 `ADVANCE`；
- 不允许把“用户聊天里说 OK”直接等同 Canonical PASS。

生产过程创建 Director、First Frames、Dynamic、QA、Edit、Subtitle、Release 等 durable artifact 后，仍必须由 Runtime Validator / State Controller 判断是否满足下一 Stage；文件存在本身不等于 Stage 已通过。

【五、生产规则只按 Stage JIT 读取】
常用规则包括但不限于：
- `04_HARNESS/workflows/mv.md`
- `04_HARNESS/rules/mv_golden_runtime.md`
- `04_HARNESS/rules/mv_bgm_discovery.md`
- `04_HARNESS/rules/mv_audio_timeline.md`
- `04_HARNESS/rules/mv_human_gates.md`
- `04_HARNESS/rules/mv_editing.md`
- `04_HARNESS/rules/mv_source_normalization.md`
- `04_HARNESS/rules/mv_web_source_roughcut.md`
- `04_HARNESS/rules/mv_subtitle.md`
- `04_HARNESS/rules/ai_video.md`
- `04_HARNESS/knowledge/MV_DYNAMIC_GENERATION_R3_LESSONS.md`
- `04_HARNESS/knowledge/MV_CAMERA_LIBRARY_CANDIDATES.md`

只有 response / current Stage 需要时才读取对应文件。

【六、核心生产硬规则】
- BGM 默认 Douyin-native exact asset first；版本证据与版权法律保证是两件事；
- BGM 锁定后必须先完成并 PASS `AUDIO_TIMELINE_PACKAGE`，再进入任何 time-dependent Director 工作；
- 歌词视觉命中 > 轻叙事连续 > 炫技镜头；环境必须参与叙事；
- Dynamic 是 RAW SOURCE，不等于最终成片；TRIM BEFORE REGENERATE；
- 多镜素材按 Runtime Context 决定是否 atomize / normalize；WEB Picture Edit 前必须通过 Source Rough-Cut；
- AI source audio 默认移除，锁定 BGM 是唯一音乐真源；
- 字幕默认继承已锁 baseline，除非用户明确重开新字幕风格；
- 局部问题执行 Patch, Don't Cascade；需要回退时使用受控 Revision / Rollback，不覆盖旧证据；
- Publish 必须有真实世界确认，并通过 Publish Transaction 同步 Canonical state + Tracker，禁止手改到 S17。

【七、启动时给用户的最小回报】
读取 matching Bridge response 后，只需明确报告：
1. 当前 branch / source SHA；
2. request_id 与 response status；
3. mode；
4. slot_id / lane；
5. current_stage / state token（若已存在）；
6. next_action / human_gate；
7. 如有 BLOCKED，说明唯一具体阻塞原因。

然后立即执行 Runtime 允许的下一动作；如果下一动作到 Human Gate，就在那里停。
```
