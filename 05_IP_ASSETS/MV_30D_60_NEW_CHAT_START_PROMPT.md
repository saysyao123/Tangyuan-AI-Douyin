# 汤圆音乐映像｜30D/60 下一首 MV 新对话启动词 v2.1 Lean

> 用途：每一首全新 MV 单独开新对话。正式入口仍是 Canonical Runtime + Web Bridge；新对话不靠聊天记忆或旧 Markdown state 猜进度。

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-web-r3` 分支。

这是「汤圆音乐映像｜30天60条音乐MV」的一首全新、独立 MV。
不要让我重新解释 R1 / R2 / R3，也不要自动继承上一首 MV 的人物、场景、道具、色调、构图、故事、Prompt 或聊天状态。

状态权威：
Runtime Controller / Web Bridge response > Canonical durable state + receipts > Tracker > current Workflow / Rules > Knowledge / History > 聊天记忆。

【1｜启动只读控制面】
先读取：
- `05_IP_ASSETS/MV_30D_60_TRACKER.csv`
- `04_HARNESS/runtime/mv_resume_contract.json`
- `04_HARNESS/runtime/mv_runtime_bridge_contract.json`
- `04_HARNESS/runtime_bridge/README.md`

不要在 Runtime 确认 slot 前加载所有历史 MV、Prompt、QA 或大型 Knowledge。

【2｜本次是新 MV，不误续旧 slot】
按 Tracker 顺序只提出第一个候选空槽，候选需满足：
- status=`PLANNED`；
- song_family 为空；
- audio_asset 为空；
- 不存在该 slot Canonical `00_STATE/CURRENT_STATE.json`；
- 不存在待迁移的根级 `CURRENT_STATE.json`。

候选不是授权。随后对该 slot_id 创建新的 immutable `RESUME` Web Bridge request，让 Runtime Controller 最终校验。

只有 response 明确返回：
- `mode=ALLOCATE_NEW_SLOT`；
- 正确 slot_id / lane；
- 有效 next_guard；
- next_action 允许初始化；
才进入 INIT_SLOT。

若 response 返回 `RESUME_CANONICAL`、`MIGRATION_REQUIRED`、ambiguity、stale 或 error，不得因为“这是新歌”而绕过 Runtime；只说明具体冲突并处理它。

【3｜初始化】
response 允许新 slot 后：
1. 原样使用 slot_id、lane、guard；
2. 通过 Bridge 创建 `INIT_SLOT`；
3. 读取 matching response；
4. 只有 Canonical state + transition receipt 已由 controller 落盘，才进入 HG01 machine preflight。

mutation 始终使用最新 guard；stale 时重新 RESUME。已处理 request 不修改。

【4｜进入 Lean MV Runtime】
Canonical slot 建立后读取：
1. `04_HARNESS/SKILL.md`
2. `04_HARNESS/MANIFEST.md`
3. `04_HARNESS/runtime/mv_macro_phase_registry.json`
4. 当前 slot Canonical state
5. `05_IP_ASSETS/ACCOUNT_POSITIONING.md`（准备 HG01 候选时）

根据 current_stage 派生当前：
`AUDIO / DIRECT / GENERATE / EDIT / DELIVER`。

合法下一步仍由 Canonical Runtime 决定；Macro Phase 只是给 Agent / 用户的轻量心智模型。
所有具体 BGM、Timeline、Director、Reference、Prompt、Generation、Edit、Subtitle 规则均按 MANIFEST JIT 读取，不再在启动词复制一套生产 SOP。

【5｜Human Gate】
HG01–HG05 仍是 Canonical durable decisions，其机器结构由 `runtime/mv_human_gate_registry.json` 定义。
真实用户决定先 RECORD_HUMAN_GATE，再独立 ADVANCE。

可以减少“用户被打断的次数”，但不能减少用户真实做出的决定：当证据已经完整时，多个明确判断可以一次提交给用户，receipt 仍分别记录。

【6｜创意与规则隔离】
- 新歌不继承上一首具体世界/人物/面纱/面罩/道具/天气/镜头配方；
- 只继承已晋升的 correctness 与当前有效 Rule；
- 历史 R&D 只在相关任务 JIT；
- Seedance 2.5 的 `5–8s / 8–15s / 15–20s`、Positive-first Prompt、Hard Constraint Budget 当前属于 Trial，必须经真实 Benchmark 才能升级长期默认；
- 30s 不属于当前素材生产实验范围。

【7｜执行纪律】
- 歌词视觉命中优先于轻叙事连续，炫技镜头排最后；
- Dynamic 是可剪 source pool，不是天然最终片段；
- 优先保留 usable material、局部 trim / repair，再考虑整条 regen；
- AI source audio 不成为时间真值；
- Patch, Don't Cascade；
- 机器可验证的技术问题不转嫁用户；
- 单条成功/失败不自动改长期 Rule。

【8｜第一次只报告必要状态】
完成 Bridge 校验后简洁报告：
1. branch / source SHA；
2. request_id / response status；
3. Runtime mode；
4. slot / lane；
5. current_stage / state token；
6. derived Macro Phase；
7. next_action / first Human Gate；
8. 如 BLOCKED，唯一具体原因。

如果 Runtime 已允许新 slot，立即完成 INIT_SLOT 和 HG01 machine preflight，然后进入真正需要我的第一次判断，不要让我重新解释项目背景。
```

## 说明

- v2.1 保留 v2.0 的 Canonical Runtime / Web Bridge 安全边界，但删除启动词中重复的完整生产规则清单。
- 正常生产细节统一由 `SKILL.md + MANIFEST.md + current state` JIT 路由。
- 全新 MV 与继续旧 MV 仍严格区分；Legacy 项目仍只能按 durable evidence 边界受控迁移。
