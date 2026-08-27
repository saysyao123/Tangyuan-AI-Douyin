# LEAN_R1｜D03-A 新对话启动词

> 直接复制下面整段到一个全新 ChatGPT 对话。目标是以最小启动上下文进入 D03-A，而不是重读完整 R1/R2/R3 历史。

```text
请使用已连接的 GitHub，继续 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-lean-r1` 分支。

这是「汤圆音乐映像｜30天60条」下一首全新独立 MV，同时也是 LEAN_R1 的第一首真实流程提速测试。

先只读取两个文件：
1. `06_TESTS/MV/LEAN_R1/NEXT_MV_TEST_CARD.md`
2. `04_HARNESS/runtime/mv_lean_runtime_contract.json`

不要启动时全文读取 SKILL / MANIFEST / Stage Registry / Executor Registry / R1-R3 历史。Lean RESUME response 会返回当前 Stage、next action 和 resolved executor；只有执行当前动作时再读取 response 指定的 JIT 文件。

【目标 slot】
本次明确请求 `D03-A / Lane P`。不要自动续 D02-A，也不要重复占用 D02-B。

【启动】
在 `04_HARNESS/lean_runtime_bridge/requests/` 创建一条新的 immutable `RESUME` request：
- command = `RESUME`
- slot_id = `D03-A`
- requested_by = `chatgpt_web`
- payload = `{}`
- request_id 使用新的 `LR-YYYYMMDDTHHMMSSZ-...` 唯一 ID。

读取 matching response。

只有当 response 明确返回：
- mode = `ALLOCATE_NEW_SLOT`
- slot_id = `D03-A`
- lane = `P`
- valid ALLOCATION next_guard
才允许初始化。

随后在 Lean request 目录创建 `INIT_SLOT` request，原样使用该 allocation guard；context 默认：
- program = `30D_60`
- web = true
- multi_shot = false
- program_30d60 = true

读取 matching response。只要 postflight 已经是 canonical `S00_SLOT_CREATED`，就直接按 response 中的 `resolved_executor` 与 JIT reads 做 HG01 machine preflight，不再额外为了“确认一下”重复读取整套 Registry。

【Lean Runtime 两个宏】
1. 用户通过 HG01-HG05 时，优先使用 `ACCEPT_GATE`：一次外部请求内部完成 durable Gate receipt + fresh verification + canonical advance。聊天里的“OK”仍然不能直接改 State。
2. 多个机器 Stage 的所需 artifacts 已按当前 upstream truth 准备好后，使用 `RUN_UNTIL_GATE_OR_BLOCK`，让 Controller 连续执行 canonical validators/transition receipts；遇到 Human Gate、S07 视频生成 handoff、S16 Release Ready 或真正 BLOCK 自动停止。

宏只压缩 transport，不允许跳过 artifact、validator、rollback 或 Human Gate。

【五个人工 Gate 不变】
- HG01：选歌；
- HG02：实际 BGM 试听；
- HG03：完整首帧组 / 视觉方向；
- HG04：Picture Edit；
- HG05：Final。

其余正常技术检查不要变成额外人工审批。

【本轮创意】
这是一首完全新的 MV。不要继承 D02-B 的男性角色、海边、白衣、风/纱帘、雨后石材、色彩和构图。只复用 `MV_DIRECTOR_LEAN_OVERLAY.md` 中已经抽象化的导演知识。

【音频效率】
HG02 后执行：P0 same-version timed lyric/LRC -> P1 lightweight ASR -> P2 heavy forced alignment only on concrete failure。第一个 PASS 即停止，不做默认双模型复核。

【开始后的第一条用户回复】
完成 RESUME + INIT_SLOT 后，只简洁告诉我：
1. branch/source SHA；
2. Lean request/response status；
3. slot/lane；
4. current Stage/state token；
5. resolved executor；
6. 当前 Human Gate；
7. 本次启动用了多少 initial reads/calls。

然后立即把 HG01 候选交给我，不要让我重新解释项目。
```
