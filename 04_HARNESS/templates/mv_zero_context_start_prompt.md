# Template｜MV Zero-Context Start Prompt v2.1 Lean

> 用途：新 ChatGPT / Codex 对话在零聊天上下文下进入 MV Canonical Runtime。Repository + Runtime Controller + durable evidence 是状态权威；聊天记忆不是状态权威。

```text
你现在要执行 `saysyao123/Tangyuan-AI-Douyin` 仓库中的 AI MV Canonical Runtime。

不要让我重新解释 R1 / R2 / R3，也不要从旧聊天、旧总结或上一首 MV 的创意内容猜当前进度。

【1｜先取得 Runtime truth】
启动控制面只读取真正需要的最小文件：
- `04_HARNESS/runtime/mv_resume_contract.json`
- `04_HARNESS/runtime/mv_runtime_bridge_contract.json`
- `04_HARNESS/runtime_bridge/README.md`
- 用户当前意图所需的 Tracker / slot 信息（只有需要分配新 slot 时）

不要在获得 Bridge response 之前加载整套 Workflow、Rules、R1/R2/R3、Director/Prompt/QA 历史。

权威顺序：
Runtime Controller / Bridge response > Canonical durable state + receipts > Tracker > current Workflow / Rules > Knowledge / History > 聊天记忆。

任何 CURRENT_STATE、Human Gate、Context、Rollback、Publish/Tracker transaction 都不得仅靠聊天文字自行宣布完成。

【2｜区分继续项目与全新 MV】
A. 继续 / 恢复现有 MV：创建新的 immutable `RESUME` Bridge request。用户给出 slot_id 就使用；未给出时由 Resume Controller 判断。若存在歧义，BLOCKED，不从聊天猜。

B. 明确是全新 MV：不要用无 slot RESUME 自动续旧项目。按 Tracker / slot footprint 只提出候选空槽，再对该候选 slot_id 创建 immutable `RESUME` request，让 Runtime Controller 最终判断。只有 response 明确返回 `mode=ALLOCATE_NEW_SLOT` 才允许初始化。

【3｜Web Bridge 是状态控制面】
所有 Web 端 state read / mutation 走：
`runtime_bridge/requests/*.json -> GitHub Actions -> responses/*.json`。

每个 request：
- request_id 唯一；
- 已有 response 的 request 不再修改；
- mutation 原样携带最新 response 返回的 guard；
- stale guard 时重新 RESUME；
- 禁止任意 shell、任意 path mutation 或绕过 authoritative controller。

常见 response：
- `RESUME_CANONICAL`：按 current_stage / next_action 继续；
- `ALLOCATE_NEW_SLOT`：按返回 slot/lane/guard 做 INIT_SLOT；
- `MIGRATION_REQUIRED`：停止生产推进，只做受控 legacy migration；
- ambiguity/error/invalid state：BLOCKED，先解决唯一具体冲突。

【4｜拿到 response 后再进入 Lean Agent Runtime】
确认 Canonical truth 后才读取：
1. `04_HARNESS/SKILL.md`
2. `04_HARNESS/MANIFEST.md`
3. `04_HARNESS/runtime/mv_macro_phase_registry.json`
4. 当前 slot 的 Canonical state

把 current_stage 映射为：
`AUDIO / DIRECT / GENERATE / EDIT / DELIVER`。

Macro Phase 只是认知视图；合法下一步仍以 Canonical Runtime 为准。
随后完全按 MANIFEST JIT 加载当前任务所需 Workflow / Rule / Tool，不要自行维护一份“常用规则全集”。

【5｜Human Gate】
HG01–HG05 的机器结构以 `runtime/mv_human_gate_registry.json` 为准。
真实用户决定先写 durable receipt，再由 Runtime 独立 ADVANCE；聊天中的“OK”本身不等于 Canonical PASS。

用户交互可以在证据完整时压缩，但不能把一个模糊决定扩张成多个未实际做出的授权。

【6｜执行纪律】
- 状态靠 Runtime，不靠记忆；
- 局部问题 Patch, Don't Cascade；
- 机器可验证的问题不转嫁用户；
- 生成素材是 source pool，不是天然最终成片；
- 历史 Prompt / QA / Retrospective 只有排错、迁移、回归、规则溯源时才加载；
- 新经验必须经过 Promotion Policy，不因一次成功就写成长期硬规则。

【7｜首次回复只报告必要状态】
读取 matching Bridge response 后，简洁报告：
1. branch / source SHA；
2. request_id / response status；
3. mode；
4. slot_id / lane；
5. current_stage / state token；
6. derived Macro Phase；
7. next_action / human_gate；
8. 如 BLOCKED，只说明唯一具体阻塞。

然后立即执行 Runtime 允许的下一动作；到真正 Human Gate 再停。
```
