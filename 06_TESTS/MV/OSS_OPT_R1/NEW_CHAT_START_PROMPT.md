# OSS MV Optimization Integration Test｜New Chat Start Prompt v1.1

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-oss-optimization-r1` 分支。

这是「汤圆音乐映像」Canonical MV Runtime 的独立开源优化实验线，不是正式生产线。

先读取：
1. `06_TESTS/MV/OSS_OPT_R1/EXPERIMENT_CONTRACT.md`
2. `06_TESTS/MV/OSS_OPT_R1/SOURCE_INTAKE.md`
3. `06_TESTS/MV/OSS_OPT_R1/RESULT_MATRIX.md`
4. `06_TESTS/MV/OSS_OPT_R1/HG01_GATE_HARDENING_v1.md`
5. `05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`
6. 当前 Canonical Runtime / Web Bridge 最小启动文件。

实验基线固定来自正式 Runtime fork SHA：
`89852ec5314e7579853683ef5eb40adb09f25753`

锁定规则：
- 不修改 `test/mv-web-r3`；
- 不为了适配外部项目放松 Runtime correctness；
- 不整体照搬外部仓库，先做 source-level 分析和最小优化映射；
- 外部优化先分类为 Runtime replacement / Stage overlay / Knowledge candidate / Tooling adapter / Out of scope；
- 先填写 SOURCE_INTAKE，再进入外部优化相关代码、规则或流程修改；
- 任何实验结论必须进入 RESULT_MATRIX；
- 单次视觉更漂亮不等于可晋升，必须同时检查稳定性、复现性、成本和维护复杂度；
- 只有完成整轮对比后，才可以提出 PROMOTE_RUNTIME / RULE / KNOWLEDGE / TOOLING；正式生产分支的晋升另开明确变更，不在实验中静默合并。

HG01 硬规则：
- `SONG_CANDIDATE_SET` 只是机器候选预检，不等于用户选歌交付；
- 禁止只给“歌名 + 排名 + 机器推荐”就让用户 A/B/C/D；
- 在向用户提交 HG01 前，必须先有持久化 `HG01_CANDIDATE_EVIDENCE_PACK`；
- 每个正式候选必须有 >=2 个近期 concrete direct Douyin works，来自 >=2 个独立账号；
- 必须报告 account / publish date / duration / evidence tier / core benchmark coverage；
- 必须验证 direct URL 的 landing work 本身就是被引用作品；旧作品页/作者页中列出的近期作品只能用于 discovery，不能作为 direct-work evidence；
- 只有 `SONG_CANDIDATE_SET.status = HG01_EVIDENCE_DELIVERY_PASS` 且 evidence delivery assertions 全部 true，才允许把 HG01 呈现给用户；
- 用户选择后才执行 `RECORD_HUMAN_GATE HG01`，随后单独 `ADVANCE` 到 S01。

如果用户已经提供开源仓库 URL / 项目文件 / 优化说明：
- 直接读取并深度分析；
- 锁定具体 source commit / 文件；
- 建立与当前 MV Runtime Stage 的逐项映射；
- 找出冲突、重复、真正增益和最低成本的集成点；
- 输出推荐的最小测试集；
- 然后开始本轮实验，不要求用户重新解释正式 Runtime。

如果用户还没有提供 source，但用户明确要求先开始一首新 MV：
- 允许先锁定与后续 A/B 测试共同使用的上游真值：slot / HG01 song family / HG02 BGM / Audio Timeline；
- 不得开始外部优化相关 Director / First Frame / Dynamic 集成；
- SOURCE_INTAKE 保持 PENDING_USER_SOURCE；
- 不自行搜索一个替代项目填进去。
```
