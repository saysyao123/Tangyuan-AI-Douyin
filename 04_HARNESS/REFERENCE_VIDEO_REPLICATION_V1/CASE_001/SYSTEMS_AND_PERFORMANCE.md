# CASE_001 — SYSTEMS_AND_PERFORMANCE.md

## Persistent System Lifetimes

| System | Entry | Major state changes | Exit | Viewer job |
|---|---:|---|---:|---|
| Cold-open headline | 0.00 | 单一开场状态 | ~0.5 | 态度 / stop-scroll |
| Topic board | ~0.5 | Reveal/interrupt 期间退出；主段重新进入 | 108.5 | Persistent Context |
| Presenter identity | 0.00 | 普通 → 新 Persona ~5.5 | 108.5 | Semantic A-roll + Persona |
| Background/world | 0.00 | 普通房间 → interrupt ~8.0 → 主场景 ~8.6 | 108.5 | World / Chapter State |
| Live caption | ~1.0 | Pause/Reveal 时退出；主段高频替换 | 108.5 | Speech comprehension + motion |
| Environmental typography | ~8.6 | 基本稳定 | 108.5 | Persona / Worldbuilding |
| Camera | 0.00 | 基本固定，表观尺度由 Subject 改变 | 108.5 | Stable frame of reference |
| Speech | question start | 2.912–5.088 near-silence；主段连续 | 108.5 | Semantic pacing |

## 关键 Handoff

1. **Question → Silence**：语音停止但画面继续，注意力从信息输入切换到等待。
2. **Silence → Hand Occlusion**：身体动作先出现，再发生身份变化。
3. **Persona → Chapter Interrupt**：先让新角色成立，再重置主视觉世界。
4. **Interrupt → Main Host World**：Persistent Topic / Environmental Typography / Live Caption 一起进入长期解释模板。
5. **Middle → Payoff**：无需换场，通过更强 Lean / Hand Proximity 提高强度。

---

## Performance Beats

下表中的时间来自视觉运动峰值 + close reading。运动峰值只是证据，不自动等于 Shot。

| Time | Nearby semantic role | Performance class | Replication meaning |
|---:|---|---|---|
| 18.4 | define / reframe | hand + upper-body emphasis | first decisive answer |
| 21.8 | rhetorical comparison | foreground hand beat | explanation → question |
| 27.4 | state transition | posture / hand change | before vs after |
| 31.6 | analogy begins | two-hand framing | hold two categories |
| 33.8 | comparison continues | head / hand accent | sustain contrast |
| 36.2 | new constraint | strong hand beat | new argument layer |
| 39.8 | concrete example | hand proximity / head change | abstraction → concrete |
| 42.6 | constraint intensifies | eye/head/hand change | escalation |
| 56.8 | usability/traceability turn | two-hand emphasis | close new loophole |
| 60.4 | consequence expands | symmetric framing | scale grows |
| 73.8 | summary | compact decisive gesture | condense argument |
| 78.6 | cost escalation | bigger body/hand change | comedy rises |
| 82.4 | incredulous question | foreground gesture | rhetorical peak |
| 101.4 | final payoff run-up | largest measured peak | ending intensity spike |
| 103.6 | final binary | close hand / lean beat | last setup before punchline |

---

## Replication Rule

新主题不能机械复制上述秒数。

未来应把 Beat 绑定到目标 Script 的语义角色：

- `Moment.question`
- `Moment.first_answer`
- `Moment.alternative`
- `Selection.comparison`
- `Moment.constraint`
- `Selection.escalation`
- `Moment.payoff`

目标片真实生成完成后，再用 P1/P2 的 aligned word time 把这些 Moment / Selection 投影到实际帧位置。

---

## Motion Generation Rule

当某个动作路径本身非常关键：

- 保存 Reference Source Excerpt；
- 把它作为 motion-reference；
- Image Reference 负责新角色/新世界；
- Prompt 负责说明“保留什么动作关系、替换什么身份与场景”。

不要只靠长提示词重新描述复杂动作。

---

## Physical Coherence

固定坐姿/站姿时保持 anchored base。

动作来源应可读：

- shoulder
- elbow
- wrist
- torso shift
- center-of-mass change

禁止：

- 无步法逻辑的横向漂移；
- 身体整体突然平移；
- 手与身体动力链完全脱节；
- camera push 与 subject lean 混淆。