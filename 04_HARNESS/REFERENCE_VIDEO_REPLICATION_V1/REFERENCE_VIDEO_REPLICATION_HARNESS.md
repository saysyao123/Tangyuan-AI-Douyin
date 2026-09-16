# REFERENCE_VIDEO_REPLICATION_HARNESS.md

## 0. 目标

把用户提供的一条参考视频拆成可以真正复刻、换主题复用、跨会话继续执行的工程化蓝图。

最终不是得到“提示词”，而是得到：

1. 原片事实与证据；
2. 原片为何有效的解释模型；
3. 时间可定位的系统行为；
4. 逐词/逐字语音时间轴；
5. 可迁移的语义关系；
6. 新主题的 Script / Treatment / Replica Blueprint；
7. 可执行的 Seedance / HyperFrames 生产计划。

---

## 1. 输入

至少一个：

- 用户上传视频；
- 可下载的视频链接；
- 参考视频 + 用户希望迁移的新主题。

可选：

- 准确字幕/脚本；
- 角色图；
- 产品资料；
- 目标平台、时长、画幅；
- 需要保留/替换的具体元素。

---

## 2. Reference Evidence Layer

### 2.1 基础规格

记录：

- duration
- resolution
- fps
- codec
- audio presence / sample rate / channels
- SHA256

### 2.2 全片 Overview

生成全片 contact sheet，先理解：

- Hook
- argument/story movement
- reveal
- payoff
- persistent systems
- viewer attention shifts

### 2.3 视觉变化候选

检测 adjacent-frame visual-change candidates，但禁止自动把所有变化点当成 Shot。

二次判断变化来源：

- edit
- camera motion
- subject motion
- text replacement
- effect / lighting
- occlusion

### 2.4 密集重看

遇到关键转场/动作时，将采样密度缩到 0.1–0.5s。

保存：

- labeled frames
- grids
- source clips
- motion excerpts

---

## 3. Reference Understanding Layer

### 3.1 ANALYSIS.md

必须回答：

- 整条视频要让观众理解/感受到什么？
- 为什么 Hook 有效？
- 故事/论证如何推进？
- 哪些系统持续存在？
- 每个系统对观众承担什么工作？
- 哪些远距离事件存在呼应？
- 最终 payoff 为什么成立？

明确区分：

- Observed Fact
- Interpretation

### 3.2 SYSTEMS

每个重要系统记录：

- Entry
- Initial State
- State Changes
- Persistence
- Handoff
- Exit
- Viewer Job
- Transfer Rule

常见系统：

- A-roll / Host
- Camera
- Caption
- Persistent Topic
- Typography
- MG / UI
- Effect
- Background / World
- Audio / Music / Silence

### 3.3 TIMELINE.md

按 source-media time 分段，记录并发系统：

- speech/action role
- camera relation
- subject state
- caption / typography / MG / effect
- audio state
- entry / active / persistence / exit
- viewer function
- evidence path
- transfer relation

---

## 4. Speech / Word-Time Layer

### 4.1 未知文字

优先：

`WhisperX / ASR → recover transcript → verify text → word times`

### 4.2 有可信文字

使用既有中文对齐路径：

```text
P0 trusted LRC / trusted script when available
↓
P1 Faster-Whisper Small
  zh
  CPU int8
  word_timestamps=True
  trusted-text mapping
↓
quality gate
↓
large conflict?
  NO → lock
  YES → P2 Xingyu CTC forced alignment
↓
lock word/character timeline
```

P2 不默认全量运行，只在 P1 存在真实冲突时升级。

### 4.3 Hypit 兼容层

统一输出：

```json
{
  "format": "hypit.transcript@1",
  "language": "zh",
  "passages": [{
    "words": [
      {"text":"字", "start_seconds":1.23, "end_seconds":1.41}
    ]
  }]
}
```

这样可继续使用 Hypit 的 word-labeled tile / phrase lookup / semantic timing 方法。

---

## 5. Performance Beat Layer

Shot 不是唯一节奏单位。

对于固定机位口播/Creator 视频，显式记录 `Performance Beat`：

- forward lean
- return to base
- point
- open-hand question
- two-hand comparison
- head tilt
- eye widening
- hand-to-lens
- posture reset

每个 Beat 要回答：

- 它对应什么语义？
- 是进入、强调、比较、反问、转折还是 punchline？
- 能否用 motion reference 直接携带？
- 新主题中对应哪个 Moment / Selection？

---

## 6. Transfer Layer

每个观察分类为：

### A. Must Preserve Relationship

例如：

- 问题必须立即可理解；
- Reveal 由内容语义推动；
- Persistent Topic 与 Live Caption 是不同系统；
- 每个新论证层得到一个可读的身体强调；
- 结尾的物理强度和语言强度一起到峰值。

### B. Optional Surface

例如：

- 黑色面罩；
- 工业背景；
- 某个具体字体；
- 彩条形式。

### C. Source-Specific Fact

只属于原片，不应盲目继承：

- 原主题；
- 原人物身份；
- 原例子；
- 原台词；
- 原秒数。

---

## 7. Target Design Layer

### 7.1 BRIEF

只保存用户目标和硬约束。

### 7.2 TREATMENT

导演回答：

- creative premise
- viewer experience
- hook / reveal / payoff
- pacing
- character/world
- camera
- caption / typography / MG
- audio
- identity anchors

### 7.3 Script

目标片唯一口头真值。

用语义身份而不是源片秒数绑定视觉事件：

- Moment.question
- Moment.reveal
- Selection.explain_a
- Moment.alternative
- Selection.escalation
- Moment.payoff

---

## 8. Generation Layer

不默认生成一条超长视频。

优先拆为 5–12 秒左右的语义 Take：

- OPEN
- REVEAL
- EXPLAIN_A
- EXPLAIN_B
- COUNTERQUESTION
- ESCALATION
- PAYOFF

Seedance 负责：

- character
- world
- body performance
- camera image

HyperFrames / deterministic post 负责：

- Caption
- Persistent Topic
- Typography
- MG
- UI
- precise transitions
- final timing

---

## 9. Motion Safety / Physical Coherence

禁止无依据的滑行/漂移。

人物位移必须有：

- 抬脚
- 落脚
- 蹬地
- 重心转移
- 加速/减速

坐姿/固定站姿则要保持 anchored base；上半身动作应从肩、肘、腕、躯干和重心变化产生。

---

## 10. Acceptance Gates

### Gate A — Reference Understanding

必须能回答：

- 为什么有效？
- 什么必须继承？
- 什么不能照抄？
- 关键证据在哪里？

### Gate B — Time Axis

必须：

- monotonic
- no end < start
- high trusted-text coverage
- continuous speech 无异常长空洞
- silence 区基本无错误词
- 视觉 Caption 变化与附近词语一致

### Gate C — Replica Design

换主题后：

- 结构仍成立；
- Reveal 有新的语义理由；
- Performance Beat 跟随新 Script；
- 不是表面换皮。

### Gate D — End-to-End Proof

至少完成：

1. 一个真实逐词/逐字 reference transcript；
2. 一个新主题 Script；
3. 一组真实生成 Takes；
4. 一次 deterministic composition；
5. 一条可播放 MP4；
6. 原片 vs 新片关系审查。

通过后才能标记：

`REFERENCE_REPLICATION_PIPELINE_V1 = VALIDATED`。