# CODEX R1｜ZERO-CONTEXT START PROMPT

把下面整段直接交给 Codex：

```text
你现在要执行本仓库的 CODEX R1 AI MV 独立自动化测试。

测试目标不是自由创作，而是先用 MODE_A_ENGINEERING_REPRODUCTION 客观复刻人工 R1 Golden Sample，测出你能自动完成多少工程流程。

开始前严格按顺序读取：
1. 06_TESTS/MV/CODEX_R1/CURRENT_STATE.md
2. 06_TESTS/MV/CODEX_R1/README.md
3. 06_TESTS/MV/CODEX_R1/CODEX_R1_MASTER_PLAN.md
4. 06_TESTS/MV/CODEX_R1/INPUT_CONTRACT.md
5. 06_TESTS/MV/CODEX_R1/GOLDEN_TARGET.md
6. 只有当前 Stage 需要时，再按 JIT 原则读取 04_HARNESS/SKILL.md、MANIFEST.md、workflows/mv.md、rules/ai_video.md 或人工 R1 对应文件。

不要一开始扫描整个仓库，不要要求我重复人工 R1 的上下文。

执行规则：
- 从 CURRENT_STATE 指定的 Stage 开始；
- 当前是 C00，就先做环境自检，不允许跳到剪辑；
- 可以自动执行的命令、安装、脚本、ffmpeg、Whisper、文件整理都由你自己做，不要让我替你输入命令；
- 需要抖音登录 / CAPTCHA 时，你启动浏览器并只让我做登录或验证码；完成后你继续；
- 不允许让我提供密码、Cookie、Token；
- 不允许把私密登录状态提交 GitHub；
- 缺文件时先尝试自动获取，自动获取失败后再向我请求最小输入；
- 每个 Stage 必须输出真实产物 / 日志 / manifest，并更新 CODEX_R1/CURRENT_STATE.md；
- 每个 Stage 记录自动执行、人工介入、失败重试和耗时；
- 不得修改或覆盖 06_TESTS/MV/ROUND_01 的 Golden 创意资产；
- 不得静默换歌、换版本、改音频区间、改歌词、改 S1-S8 顺序；
- 如果能力缺失，明确标记 BLOCKED / PARTIAL / EXTERNAL_GENERATION_REQUIRED，不允许用空文件冒充成功；
- 最终必须按 RESULT_REPORT_TEMPLATE.md 输出 CODEX_R1_RESULT.md 和 CODEX_R1_METRICS.json；
- 最终给出 Automation Score /16，并明确每一次人工介入。

MODE A 目标链路：
C00 环境
-> C01 BGM / datasource
-> C02 精确音频裁剪
-> C03 Whisper逐词 + 已知歌词约束
-> C04 无水印高清 S1-S8 源替换
-> C05 36.8秒时间线重建
-> C06 字幕烧录 + Final Polish
-> C07 QA / Golden comparison
-> C08 结果报告与收尾

特别注意：
人工 R1 已验证的最终歌词时间、音频区间和创意决定在 GOLDEN_TARGET.md。MODE A 的任务是复刻和验证自动化，不是重新设计。

人物相关图生视频硬规则只在未来 MODE B 使用。任何人物相关动态提示词第一行必须原样为：
*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。
前面的 *** 不能删除。

现在开始执行 C00。先自己运行环境检查，生成 env_report.json 和 C00 日志，再根据真实结果继续，不需要先向我提问。
```
