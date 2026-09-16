# VALIDATION_PLAN.md

## 目标

验证本 Harness 是否真正能把“理解参考视频”转成“可生成的新主题视频”，而不仅是写出一份漂亮分析。

---

## V0 — Mechanical Evidence

必须得到：

- probe / metadata；
- whole-video overview；
- visual-change candidates；
- dense grids for critical ranges；
- audio silence/accent evidence；
- representative motion clips。

PASS 条件：关键事件均可重新回到 source time 核查。

---

## V1 — Reference Understanding

必须完成：

- ANALYSIS；
- SYSTEM lifetimes；
- TIMELINE；
- Performance Beats；
- facts vs interpretation；
- must-preserve / optional-surface / source-specific 分类。

PASS 条件：另一个 Agent 只看档案就能解释原片为何有效，并定位证据。

---

## V2 — Word / Character Timeline

### Reference

根据文字可信度选择：

- Unknown Text → WhisperX/ASR；
- Trusted Text → P1 Faster-Whisper Small；
- Conflict → P2 Xingyu CTC。

产物：

- normalized timeline；
- `hypit.transcript@1`；
- word-labeled evidence grids；
- phrase lookup 可正常定位。

PASS 条件：时间单调、覆盖充分、已知 silence 无明显错词、重要 Caption/动作事件能够绑定到附近真实词语。

---

## V3 — Transferable Replica Design

换一个完全不同主题，禁止只换人物/颜色。

必须重新设计：

- Script；
- Character/world；
- Topic board；
- Environmental typography；
- examples / claims；
- payoff。

必须保留：

- 原片真正有效的因果关系；
- Performance Beat 的语义角色；
- persistent systems 的职责；
- reveal / escalation / payoff 关系。

PASS 条件：用户能看出“同一种导演语法”，但不是对原片的表面复制。

---

## V4 — Generation Proof

至少生成：

- OPEN Take；
- REVEAL Take；
- 2–3 个 EXPLAIN/ESCALATION Take；
- PAYOFF Take。

优先使用 5–12s 的语义 Take，不以一次生成完整长视频为目标。

PASS 条件：

- Character/world continuity 可接受；
- 动作与语义一致；
- 无无依据滑行/漂移；
- camera / subject motion 区分清楚；
- 失败时能只重做局部 Take。

---

## V5 — Deterministic Composition Proof

使用 HyperFrames / Studio 或等价确定性后期实现：

- Persistent Topic；
- Live Caption；
- Typography；
- MG；
- deterministic transitions；
- final timing；
- audio mix。

PASS 条件：视觉元素跟随 target 的真实 aligned word time，而不是硬复制 reference 秒数。

---

## V6 — Final Comparison

最终同时检查：

### Reference relationship preservation

- Hook 的工作是否保留；
- Reveal 是否仍有语义理由；
- Stable Host World 是否成立；
- 论证升级是否仍由视觉 Performance Beat 支撑；
- Payoff 是否在身体和语言上共同增强。

### Surface independence

- 是否过度复制原人物、服装、背景、措辞或构图细节；
- 换主题后是否仍自然；
- 是否仍能看作独立原创制作。

---

## 状态定义

当前：

```text
ANALYSIS_ARCHITECTURE = PASS
HYPIT_REFERENCE_PARITY = PASS_EXCEPT_REAL_ALIGNMENT
TIME_AXIS_COMPATIBILITY = PASS
REPLICA_DESIGN = PASS
END_TO_END_REPLICATION = PENDING
```

只有 V2–V6 都通过后，才能改为：

```text
REFERENCE_REPLICATION_PIPELINE_V1 = VALIDATED
```