# LEAN_R1｜D03-A 新对话启动词

> 直接复制下面整段到一个全新 ChatGPT 对话。D03-A 已由 Lean Controller 合法初始化到 S00，HG01 machine preflight 候选包也已经准备好；新对话只需 Resume → 读取候选包 → 让我选歌。

```text
请使用已连接的 GitHub，继续 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-lean-r1` 分支。

这是「汤圆音乐映像｜30天60条」下一首全新独立 MV，同时也是 LEAN_R1 的第一首真实流程提速测试。

启动先只读取：
1. `06_TESTS/MV/LEAN_R1/NEXT_MV_TEST_CARD.md`
2. `04_HARNESS/runtime/mv_lean_runtime_contract.json`

不要启动时全文读取 SKILL / MANIFEST / Stage Registry / Executor Registry / R1-R3 历史。

【目标 slot】
固定 `D03-A / Lane P`。该 slot 已合法初始化为：
`S00_SLOT_CREATED / SLOT_CREATED`。
不要再次 INIT_SLOT，不要自动续 D02-A，也不要重复占用 D02-B。

【第一步：Lean RESUME】
在 `04_HARNESS/lean_runtime_bridge/requests/` 创建一条新的 immutable RESUME request：
- command = `RESUME`
- slot_id = `D03-A`
- requested_by = `chatgpt_web`
- payload = `{}`
- request_id 使用新的 `LR-YYYYMMDDTHHMMSSZ-...` 唯一 ID。

读取 matching response。

正常预期：
- mode = `RESUME_CANONICAL`
- slot_id = `D03-A`
- lane = `P`
- current_stage = `S00_SLOT_CREATED`
- current_state_token = `SLOT_CREATED`
- next_action = HG01 song selection
- resolved_executor = `HG01_CORE_DATABASE_ORCHESTRATION`

如果不一致，以 response 为权威并说明唯一冲突，不准用聊天记忆补状态。

【第二步：直接进入 HG01】
HG01 machine preflight 已经完成，不要重新全库研究选歌。直接读取：
- `06_TESTS/MV/WEB_R3/30D_60/D03-A/01_SONG/SONG_CANDIDATE_SET.json`
- `06_TESTS/MV/WEB_R3/30D_60/D03-A/01_SONG/HG01_CANDIDATE_EVIDENCE_PACK_v1.md`

然后把候选简洁交给我。不要替我自动选歌，不要提前做 HG02、Director 或视觉设计。

【Lean Runtime 两个宏】
1. 用户通过 HG01-HG05 时，优先使用 `ACCEPT_GATE`：一次外部请求内部完成 durable Gate receipt + fresh verification + canonical advance。聊天里的“OK”本身仍不直接等于 State mutation。
2. 多个 machine Stage 的所需 artifacts 已按当前 upstream truth 准备好后，使用 `RUN_UNTIL_GATE_OR_BLOCK`；Controller 连续执行 canonical validators/transition receipts，并在 Human Gate、S07 视频生成 handoff、S16 Release Ready 或真正 BLOCK 自动停止。

宏只压缩 transport，不允许跳过 artifact、validator、rollback 或 Human Gate。

【五个人工 Gate 不变】
- HG01：选歌；
- HG02：实际 BGM 试听；
- HG03：完整首帧组 / 视觉方向；
- HG04：Picture Edit；
- HG05：Final。

其余正常技术检查不要变成额外人工审批。

【创意隔离】
这是一首完全新的 MV。不要继承 D02-B 的男性角色、海边、白衣、风/纱帘、雨后石材、色彩和构图。只允许复用 `04_HARNESS/knowledge/MV_DIRECTOR_LEAN_OVERLAY.md` 中抽象化的通用导演知识。

【音频效率】
HG02 后执行：P0 same-version timed lyric/LRC -> P1 lightweight ASR -> P2 heavy forced alignment only on concrete failure。第一个 PASS 即停止，不做默认双模型复核。

【第一条用户回复格式】
Lean RESUME 正常后，简洁告诉我：
1. branch/source SHA；
2. request/response status；
3. slot/lane；
4. current Stage/state token；
5. resolved executor；
6. 当前 Human Gate；
7. 启动 initial reads/calls 数量。

随后立即展示已经准备好的 HG01 候选让我选，不要让我重新解释项目。
```
