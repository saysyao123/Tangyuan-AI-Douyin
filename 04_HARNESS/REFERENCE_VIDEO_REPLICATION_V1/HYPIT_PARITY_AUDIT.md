# HYPIT_PARITY_AUDIT.md

## Hypit 原项目要求

Hypit 的 reference-video 方法不是“抽几帧然后总结”，而是要求：

- whole-piece meaning；
- concrete system behavior；
- source-time evidence；
- word-level speech timing；
- entry / active / persistence / exit；
- facts 与 interpretation 分离；
- 必要时高密度重新检查；
- evidence clips / grids；
- 把参考片转成 target relationships，而不是复制 source seconds。

## v1 → v2 对照

| 原项目要求 | v1 | 当前方案 |
|---|---|---|
| Hook / story / payoff | 已覆盖 | 保留 |
| Persistent Caption/MG/Typography/Effect/Audio | 部分 | 显式记录生命周期与 handoff |
| Source-time TIMELINE | 偏粗 | 记录并发系统 + viewer function |
| Word-level transcript | 缺失 | 接入 P1/P2 + Hypit adapter |
| Dense 0.1–0.5s reinspection | 仅关键开头 | 关键区间按需执行 |
| Exact text / placement / state | 部分 | 作为系统证据保存 |
| Visual boundary != shot | 已意识到 | 正式拆成 Shot / Performance Beat |
| Motion/camera source excerpts | 缺失 | 纳入正式证据层 |
| Facts vs inference | 混合 | 明确分栏/分段 |
| Reference 与 target 分离 | 有 | 固化为 Harness 规则 |
| Semantic target timing | 有 | 用 Script Moment / Selection 正式表达 |
| Editable Source/Run/Studio build | 未做 | 仍待端到端验证 |

## 关键结论

此前方案不是方向错，而是停在了“导演理解正确”这一层，还没有完整达到“证据可重新执行”的程度。

当前方案补强后，Reference Archive 应至少能回答：

1. 这条片整体在做什么；
2. 为什么有效；
3. 每个系统什么时候进入、变化、持续、退出；
4. 这些变化对应哪些词、停顿或动作；
5. 哪些关系换主题后必须保留；
6. 哪些只是原片表面风格；
7. 哪些动作/摄影机运动值得保留 source excerpt。

## Deep Replica 的定义

成功复刻不意味着：

- 同样的面罩；
- 同样的背景；
- 同样的话题；
- 同样的秒数。

成功意味着新主题仍能复现原片的因果关系，例如：

1. 问题立即落地；
2. 停顿制造期待；
3. Reveal 因主题而发生；
4. 一个少见 interrupt 打开主解释章节；
5. Persistent Topic + Live Caption + Stable Host Shot 同时运行；
6. 每个语义转折有 intentional Performance Beat；
7. 论证逐层封闭漏洞；
8. 结尾语言强度与身体强度共同达到峰值。

如果这些关系能跟随新 Script 的真实时间重新落位，就属于结构复刻，而不是表面模仿。