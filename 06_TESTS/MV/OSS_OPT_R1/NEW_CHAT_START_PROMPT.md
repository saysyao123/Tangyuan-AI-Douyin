# OSS MV Optimization Integration Test｜New Chat Start Prompt v1.2

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

HG01 恢复原 R3 选歌策略：
- 默认主源是用户已经锁定的核心 Benchmark / 对照账号数据库；
- 路径固定为：`核心账号更新/读取 -> Data Center -> SONG_FAMILY repeat/value ranking -> HG01`；
- 不把“全网搜索歌曲”作为每首 MV 的默认选歌方式；
- 只有发现长期值得跟踪的新账号时，才作为 supplemental benchmark 加入数据库；
- Web / Radar 只用于按需定位具体 work、补充新账号或做趋势 freshness 佐证，不能取代核心数据库成为正式候选池；
- `SONG_CANDIDATE_SET` 仍是机器预检，不等于用户选择；
- HG01 给用户的交付保持简单：歌名 + 一句入选原因 + 对应博主的对应歌曲 Douyin MV；
- 不要求用户阅读 Tier A/B/C、Core coverage、Evidence taxonomy 或全网检索过程；
- 保留唯一硬防错：交付的 direct URL 必须真正打开被引用的那条 MV；作者旧作品页里列出的近期作品只能用于定位，不能冒充正式交付链接；
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
