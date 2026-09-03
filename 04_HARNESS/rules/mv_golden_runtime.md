# Rules｜MV Golden Runtime Contract v1.6 Lean

> Status: `ACTIVE / PRODUCTION-VALIDATED CORE + TRIAL GENERATION OVERLAY`
> Purpose: 只保留跨歌曲长期成立的 correctness 原则与权威边界；不复制 Workflow、Stage Registry、工具实现或历史案例。

## 1. Authority Map

同一事实只能有一个权威来源：

- 当前阶段 / 合法下一步 → `runtime/mv_stage_registry.json` + `runtime/mv_transition_contract.json`
- Human Gate 结构 → `runtime/mv_human_gate_registry.json`
- Artifact 前置 → `runtime/mv_artifact_registry.json`
- Agent/用户 Macro Phase → `runtime/mv_macro_phase_registry.json`
- Audio version discovery → `rules/mv_bgm_discovery.md`
- Audio timeline truth → `rules/mv_audio_timeline.md` + corresponding tools
- AI generation control → `rules/ai_video.md`（Batch B 将拆分为 Compiler + conditional modules）
- Editing → `rules/mv_editing.md`
- Subtitle implementation → `rules/mv_subtitle.md`
- Rule lifecycle → `knowledge/PROMOTION_POLICY.md`

历史 Round、Prompt、QA、Receipt、Retrospective 只做 evidence / provenance，不负责正常 Runtime 继承。

## 2. Production-validated Golden Principles

### G1｜State over memory
聊天中的“已经做到哪一步”不能替代 Canonical Runtime state、artifact 和 transition receipt。

### G2｜Evidence before rule
单次成功/失败不直接升级长期 Rule。必须经过重复验证和 Promotion Policy；被新证据推翻的旧规则应替换/废止，而不是继续追加例外。

### G3｜Exact audio truth before time-dependent work
锁定 exact BGM 后，Audio Timeline 才建立 lyric/music truth；Director/Edit/Subtitle 不创建自己的第二套时间真值。

### G4｜Actual accepted asset > old prose
实际通过的 Reference / K0 / media asset 是下游事实。旧 Prompt、旧 Director prose 与实际已接受资产冲突时，修改文字和 state，不要求模型恢复废弃计划。

### G5｜Patch, Don't Cascade
问题只回最近根因。下游实现 bug 不无故重开已经通过的上游审美决定；只有上游事实真的变化时才使依赖它的下游失效。

### G6｜Human reviews taste; machines review correctness
用户主要负责歌曲/片段、视觉方向、Picture rhythm、最终接受等审美与授权判断。机器可验证的问题在提交 Human Gate 前完成。

### G7｜Generated video is a source pool
AI source 是可剪素材，不是天然最终剪辑单元。保留 usable windows、实际内部动作/切镜与 source role，比强求每条生成自己成为“迷你成片”更重要。

### G8｜Creative grammar is not globally frozen
不跨歌曲固定人物、世界、首帧数量、source 数量、镜头数、camera recipe、统一 cut 配额或复杂歌词特效。Golden 保护 correctness，不保护创意重复。

## 3. Lean Generation Overlay｜TRIAL UNTIL SEEDANCE 2.5 BENCHMARK

以下是当前 v1.0 设计方向，不得因为写在 Golden 文件里就误标为 `PRODUCTION_VALIDATED`：

### T1｜Positive-first prompting
Prompt 优先描述成功结果、人物表演、摄影机关系、核心视觉事件和结束状态；只有高频、高代价、无法后处理的问题才占用 Hard Constraint。

### T2｜Negative constraint budget
默认目标：Hard Constraints ≤3；软上限 5。超过时应触发复杂度审查，优先改为正向目标、Reference、参数或 Validator，而不是继续堆禁止项。

### T3｜Outcome-based material QA
素材审核优先回答：`STATUS / USABLE / FAILURE / NEXT`。没有改变下一动作、也不承担必要 durable evidence 的审核结果应视为 log，而不是新 Gate。

### T4｜Stop when accepted
达到预设可剪阈值后停止继续优化。MV 目标是足够高质量、足够覆盖的素材组合，不要求所有 source 达到同一峰值质量。

### T5｜Duration is strategy, not workflow
Seedance 2.5 当前只实验 `5–8s / 8–15s / 15–20s`。三者共用同一 Workflow；是否晋升为长期默认必须看真实 usable yield / repair cost / human interruption 数据。

## 4. Promotion Requirement for Trial Overlay

任何 T1–T5 想成为 Production-validated Rule，至少记录：
- tested model / provider；
- baseline vs lean prompt；
- attempts；
- usable seconds / accepted material yield；
- repair count；
- human interruption count；
- observed failure modes。

单条漂亮样片不构成晋升证据。

## 5. Anti-Duplication Rule

如果某项前置条件已经由 Canonical Runtime / Validator 机械强制，不再在 Workflow、Golden、Checklist、Gate 文档中重复维护完整条件列表。

文档可以解释“为什么”，但机器 Contract 负责“是否合法”。
