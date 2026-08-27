# OSS MV Optimization Integration Test｜New Chat Start Prompt v1.4

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-oss-optimization-r1` 分支。

这是「汤圆音乐映像」Canonical MV Runtime 的独立开源优化实验线，不是正式生产线。

先读取：
1. `06_TESTS/MV/OSS_OPT_R1/EXPERIMENT_CONTRACT.md`
2. `06_TESTS/MV/OSS_OPT_R1/SOURCE_INTAKE.md`
3. `06_TESTS/MV/OSS_OPT_R1/RESULT_MATRIX.md`
4. `06_TESTS/MV/OSS_OPT_R1/HG01_GATE_HARDENING_v1.md`
5. `06_TESTS/MV/OSS_OPT_R1/PROCESS_AUDIT/END_TO_END_EXECUTION_AUDIT_v1.md`
6. `05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`
7. `04_HARNESS/runtime/mv_stage_executor_registry.json`
8. `04_HARNESS/rules/mv_executor_first.md`
9. `04_HARNESS/rules/mv_lyric_timeline_simple_path.md`
10. 当前 Canonical Runtime / Web Bridge 最小启动文件。

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

EXECUTOR-FIRST 是本实验的硬约束：
- Runtime/Stage Registry 决定 WHAT；`mv_stage_executor_registry.json` 决定 HOW；
- 每个 Stage 执行前先解析 registered executor，再读取 Stage Rule / Template / Tool；
- Rule 中提到开源工具，不等于需要安装该工具；
- 没有 repo-local Python 脚本，不等于缺实现：CREATIVE_SYNTHESIS / CAPABILITY_HANDOFF 是合法执行类别；
- 创建任何新 helper/workflow/model route 前，必须先查 existing canonical tool / prior PASS / existing workflow / dependency doctor；
- 缺依赖默认 BLOCK，不得为了继续执行自动换模型或每首 MV 重装生产模型；
- slot-specific helper 不得进入 `04_HARNESS/tools/`；
- authoritative Runtime Web Bridge 不得挂载歌曲/slot专用实验 job；
- OSS overlay 只能进入 executor registry 中 `experiment_overlay_allowed=true` 的 Stage。

HG01 恢复原 R3 选歌策略：
- 默认主源是用户已经锁定的核心 Benchmark / 对照账号数据库；
- 路径固定为：`核心账号更新/读取 -> Data Center -> SONG_FAMILY repeat/value ranking -> HG01`；
- 不把“全网搜索歌曲”作为每首 MV 的默认选歌方式；
- 只有发现长期值得跟踪的新账号时，才作为 supplemental benchmark 加入数据库；
- Web / Radar 只用于按需定位具体 work、补充新账号或做趋势 freshness 佐证，不能取代核心数据库成为正式候选池；
- HG01 给用户的交付保持简单：歌名 + 一句入选原因 + 对应博主的对应歌曲 Douyin MV；
- 保留唯一硬防错：交付的 direct URL 必须真正打开被引用的那条 MV；
- 用户选择后才执行 `RECORD_HUMAN_GATE HG01`，随后单独 `ADVANCE` 到 S01。

S02 歌词时间线采用唯一 Simple Path：
- 目标只回答两件事：完整歌词是什么、每句什么时候开始/结束；
- 唯一路径：`HG02 exact BGM -> verify audio SHA -> full-clip ASR transcript -> ONE lyric-text audit -> trusted_lyrics locked -> Xingyu forced alignment -> ONE automatic QA -> line_timeline.csv + lyrics_exact.srt -> S03`；
- Douyin work caption / description / hashtag / partial lyric quote 永远不能单独作为完整歌词真值；
- 正常 PASS 路径不跑第二模型、不做 Web 歌词证据扫、不做 waveform/BPM 猜测、不建立每首歌专用工具；
- 只有具体 QA FAIL 才允许修正该问题并重跑同一路径一次；
- `anchor_words.csv` 与 `music_events.csv` 移到 Natural Beat / Director enrichment，不再阻塞歌词时间线锁定；
- D02-B 之前基于 4 句 creator caption 的 trusted lyrics / timeline 全部视为 INVALID，不得封包或推进 S03，必须从锁定 BGM 全段重建完整歌词。

当前 OSS source 已锁定：
`penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`

本轮只允许测试 SOURCE_INTAKE 已登记的最小 overlay：
1. Director Thesis；
2. Primary Visual Engine；
3. audiovisual relationship；
4. motive-first camera-subject-space；
5. WHY CUT HERE；
6. optional-element stop condition；
7. Director -> First Frame -> Dynamic Prompt Creative Drift QA。

明确排除：
- H3 10–15s integer production containers；
- H3 16:9 four-panel storyboard input；
- RunningHub/H3 orchestration；
- 替换 R3 HG01/HG02/Runtime/Publish truth。

共同上游允许先锁：slot / HG01 song / HG02 BGM / Lyric Timeline。
只有 Lyric Timeline 按 Simple Path 通过后，才进入 OSS Director A/B。
```
