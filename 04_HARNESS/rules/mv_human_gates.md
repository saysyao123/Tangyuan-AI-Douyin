# Rules｜MV Human Gate Guidance v1.1 Lean

> Status: `ACTIVE GUIDANCE / MACHINE STRUCTURE LIVES IN REGISTRY`
> Core: **Human reviews taste and authority; machines review correctness.**

Human Gate 的机器定义、stage_id、required receipt fields、preflight artifacts 以：
`runtime/mv_human_gate_registry.json`
为唯一权威。

本文件只定义用户应该判断什么，以及怎样减少不必要的人工中断。

## Fixed Human Decisions

### HG01｜Song Aesthetic
用户判断：这首歌是否值得做、哪个候选方向最对。
机器负责候选筛选、基本版本与可执行性证据。

### HG02｜BGM Excerpt Listening
用户判断：实际可试听片段的开头、主体段落、结尾与 fade 是否舒服、完整。
机器负责 exact version、候选边界和技术准备。

### HG03｜Visual Direction / Reference Set
用户判断：世界、人物、色彩、歌词视觉命中、整组美感与差异是否成立。
机器先拦截明显重复、不可执行、身份/连续性错误。

当前仍是 Canonical durable Gate。是否未来改为 Conditional，必须由 Seedance 2.5 Benchmark 证明，而不是为了减少 Gate 先验删除。

### HG04｜Picture Rhythm
用户判断：整体节奏、情绪峰值/释放、镜头取舍是否舒服。
机器负责音频真值、source risk、画幅、source-audio、基础实现正确性。

### HG05｜Final Acceptance
用户判断：成片是否可接受/发布，以及是否存在必须重开上游的明确创意问题。
机器先完成 Final technical validation。

## Interaction Compression

**Durable Gate 数量 != 用户必须被打断的次数。**

当多个判断所需证据已经同时完整时，可以在一次用户交互里顺序询问/确认多个明确决定，例如 HG01 + HG02；但必须满足：
- 每个判断问题独立清晰；
- 用户的决定文本能分别对应；
- Runtime 仍生成独立 durable receipt；
- 不允许把一个模糊的“都可以”扩张成未实际做出的多个授权。

目标不是追求固定交互次数，而是减少没有新增判断价值的中断。

## Conditional Escalation

只有机器不能以低成本确定下一步时才升级用户，例如：
- 强音频证据冲突且无法自动判定；
- clean material 不足且局部 regen / alternate material 都无法自动选择；
- 用户明确要求新的字幕审美或新的高成本视觉方向。

技术实现 bug 默认机器修复，不新增 Human Gate。

## Gate Submission Contract

提交用户前只需要做到：
1. 说明当前唯一或少量明确的主观判断；
2. 提供可以直接看/听的 artifact；
3. 基础机器 QA 已完成；
4. 说明 PASS 后会锁定什么决定。

不要把大段技术检查清单转嫁给用户。

## Nearest-cause Rollback

问题只回最近根因：
- song / excerpt → AUDIO；
- world / reference → DIRECT；
- source usability → GENERATE；
- picture / subtitle implementation → EDIT；
- final technical / release → DELIVER。

下游实现 bug 不自动重开已通过的上游审美 Gate。

## Human Attention Health Check

如果用户频繁被要求审核：
- 机器可判断的技术项；
- 同一视觉方向的细小中间稿；
- 不会改变下游动作的 QA；
- 已经明确通过、却因无关实现 bug 被重新打开的决定；

则视为 Harness 设计问题，应优先修 Validator / state / handoff，而不是继续增加 Human Gate。
