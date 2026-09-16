# CASE_001 — REPLICA_BLUEPRINT.md

## 目标

验证 Reference 的导演语法能否迁移到一个完全不同的主题，而不是复制原片服装、背景或话题。

示例新主题：

**“为什么很多 AI 视频越做越复杂，反而越不好看？”**

这只是当前测试主题，后续可替换。

---

## Transfer Map

| Reference function | Target equivalent |
|---|---|
| Counter-intuitive question | 为什么 AI 视频越复杂反而越不好看？ |
| Ordinary presenter | 普通 AI 创作者状态 |
| Anticipation pause | 问题后短停顿 |
| Persona reveal | 普通创作者 → “AI 导演模式” |
| Rare chapter interrupt | system/glitch/pipeline interrupt |
| Stable host world | 固定 AI 工作台 / 导演控制台 |
| Persistent topic | 顶部固定本期问题 |
| Environmental typography | “先解决问题，再加效果” 等场景文字 |
| Live caption | 根据目标真实 aligned speech 自动生成 |
| Progressive loophole closure | 镜头多？Prompt 长？运动大？效果多？逐个否定 |
| Strong physical payoff | 身体前倾 + 更简洁决定性手势 + punchline |

---

## Suggested Target Structure

### Segment A — Hook

**功能**：2–3 秒内让问题成立。

- 普通 Creator；
- 固定正面构图；
- 直接问：“为什么很多 AI 视频越做越复杂，反而越不好看？”
- Persistent Topic 同时出现。

Target Script Anchor：`Moment.question`

### Segment B — Pause / Reveal

**功能**：把问题从信息变成视觉期待。

- 问题结束后短暂停顿；
- Hand toward lens / occlusion；
- 进入“AI 导演模式”身份。

Target Anchors：`Selection.anticipation` + `Moment.reveal`

### Segment C — Chapter Interrupt

**功能**：正式进入解释章节。

- 0.3–0.8s 的短 system/glitch；
- 不频繁使用；
- 之后进入稳定主视觉世界。

### Segment D — Explain A

核心命题：

“效果多，不等于信息更清楚。”

Performance：单手定义 / 小幅前倾。

Anchor：`Moment.first_answer`

### Segment E — Alternative 1

核心命题：

“是不是镜头越多就越高级？”

Performance：open-hand question / two-hand comparison。

Anchor：`Moment.alternative_1`

### Segment F — Alternative 2

核心命题：

“是不是 Prompt 写得越长越专业？”

Performance：双手框定、轻微反问表情。

Anchor：`Moment.alternative_2`

### Segment G — Constraint / Reframe

核心命题：

“真正决定效果的不是元素数量，而是观众能不能第一眼理解重点。”

Performance：动作减少，变得更决定性。

Anchor：`Moment.constraint`

### Segment H — Payoff

示例 Punchline：

“复杂不是高级。能让观众一眼看懂，才是高级。”

Performance：身体略前倾、短而强的收尾手势，然后稳定停住。

Anchor：`Moment.payoff`

---

## Generation Take Plan

不要默认一次生成完整 60–100 秒。

建议：

```text
TAKE_00_OPEN       3–5s
TAKE_01_REVEAL     2–4s
TAKE_02_EXPLAIN_A  6–10s
TAKE_03_ALT_1      6–10s
TAKE_04_ALT_2      6–10s
TAKE_05_REFRAME    6–10s
TAKE_06_PAYOFF     5–8s
```

同一 Character/World Anchor 贯穿主段。

每个 Take 独立失败、独立重做。

---

## Seedance Responsibility

Seedance 负责：

- Presenter identity；
- scene / lighting；
- upper-body performance；
- eye/head/hand dynamics；
- camera image；
- 必要时 motion-reference transfer。

禁止依赖 Seedance 生成：

- 正确中文字；
- Persistent Topic；
- 精确字幕；
- 精确 MG；
- 最终时间轴。

---

## HyperFrames / Deterministic Post Responsibility

负责：

- Persistent Topic；
- Live Caption；
- Environmental Typography；
- system/glitch；
- Jump Cuts / trims；
- word-following emphasis；
- final compositing；
- final MP4。

---

## Word-Time Production Rule

Target Script 是唯一可信 verbal authority。

生成 Take 后：

```text
Target Script
+
Take Audio
↓
P1 Faster-Whisper Small trusted-text mapping
↓
必要时 P2 Xingyu CTC
↓
真实 word/character timeline
↓
Caption / MG / B-roll / Effect 自动绑定
```

因此 Reference 的原秒数只用于学习 rhythm，不进入 Target 作为硬时间。

---

## Acceptance

Replica 必须满足：

- 看得出同一种“问题→Reveal→稳定解释→逐层封闭→Payoff”的导演语法；
- 但人物、主题、文案、视觉世界与原片独立；
- Performance Beat 与新 Script 语义对应；
- 字幕时间来自 Target 真实 alignment；
- 无无依据滑行/漂移；
- Camera motion 与 Subject motion 不混淆；
- 结尾强度高于中段。

满足以上条件才算“结构复刻”，不是简单换皮。