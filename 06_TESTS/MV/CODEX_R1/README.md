# CODEX R1｜AI MV 独立复刻与自动化测试

> 目的：给 Codex 一套与人工 R1 Golden Sample 隔离的、可执行、可审计的测试流程，用来判断 Codex 到底能自动完成多少 AI MV 生产工作。

## 0. 测试定位

本目录不是人工 R1 的继续修改区。

人工 R1 已经锁定：
- `06_TESTS/MV/ROUND_01/CURRENT_STATE.md`
- `06_TESTS/MV/ROUND_01/R1_FINAL_LOCK.md`
- Golden Sample：`你有没有真的爱过我｜阿图表妹`

Codex R1 的任务是：

1. **先工程复刻同一条 Golden Sample**，验证 Codex 对数据源、音频、Whisper、无水印高清源、时间线、字幕、QA、最终导出的自动化能力；
2. 不得擅自改变已经通过的人工作品创意；
3. 记录所有人工介入、失败、重试、耗时与环境依赖；
4. 最终输出一份 `CODEX_R1_RESULT.md`，明确哪些环节可自动化、哪些仍需要人。

## 1. 两种模式

### MODE A｜ENGINEERING_REPRODUCTION｜默认，必须先跑

目标：使用人工 R1 已批准的创意决定和时间线，Codex 尽量自动重建发布级版本。

必须测试：
- 环境自动检查；
- 抖音 / BGM 数据源能力；
- Reference BGM 获取或本地输入识别；
- ffmpeg 精确裁剪；
- Whisper 逐词时间戳；
- 已知歌词约束校正；
- 无水印高清源获取 / 替换；
- 36.8s 剪辑重建；
- 字幕烧录；
- 自动 QA；
- 最终报告。

MODE A 不重新设计首帧、不重新设计导演、不重新生成 Seedance 视频；它先测试 Codex 的工程复刻能力。

### MODE B｜FRESH_R1_CREATIVE｜MODE A 通过后再开

目标：Codex 按 `04_HARNESS/workflows/mv.md` 独立跑一首新歌。

Codex 可以自动完成：
- 选歌研究；
- 音频处理；
- Beat；
- 导演；
- 首帧提示词；
- 动态提示词；
- QA 规则；
- 剪辑；
- Whisper 字幕；
- 结果归档。

如果当前 Codex 环境没有 GPT 生图 / Seedance 生成接口：
- 生成首帧提示词后停在 `EXTERNAL_GENERATION_REQUIRED`；
- 用户生成图片并放入约定目录后，Codex 自动继续；
- 动态视频同理；
- **不得假装已经生成。**

## 2. 启动顺序

Codex 进入本测试后只读：

1. `06_TESTS/MV/CODEX_R1/CURRENT_STATE.md`
2. `06_TESTS/MV/CODEX_R1/CODEX_R1_MASTER_PLAN.md`
3. `06_TESTS/MV/CODEX_R1/INPUT_CONTRACT.md`
4. `06_TESTS/MV/CODEX_R1/GOLDEN_TARGET.md`
5. 当前 Stage 需要的 Runtime 文件

不要一开始扫描整个仓库。

## 3. 核心原则

- 人工 R1 = Golden Truth；Codex R1 = Reproduction / Automation Test。
- 不允许静默修改歌、音频区间、镜头顺序、字幕文本、字幕时间或已锁导演决定。
- 无法完成必须明确标记 `BLOCKED` / `EXTERNAL_GENERATION_REQUIRED` / `MANUAL_CONFIRM_REQUIRED`。
- 每个 Stage 都必须产生机器可读结果或明确文件产物。
- 每个 Stage 更新 `CURRENT_STATE.md`。
- 所有关键步骤都记录：开始时间、结束时间、自动执行时间、人工介入次数、失败重试次数。

## 4. 通过条件

Codex R1 只有在以下产物齐全时才算完成：

- `outputs/final/CODEX_R1_FINAL.mp4`
- `outputs/final/lyrics_whisper_corrected.srt`
- `outputs/reports/CODEX_R1_RESULT.md`
- `outputs/reports/CODEX_R1_METRICS.json`
- `outputs/reports/FAILURE_LOG.md`
- `outputs/manifests/timeline.json`
- `outputs/manifests/source_manifest.json`

如果某项因当前环境不具备能力，结果报告必须明确写出原因，不能用占位文件冒充通过。

## 5. 第一条测试对象

Song：`你有没有真的爱过我｜阿图表妹`

人工 R1 Golden 信息见：
`GOLDEN_TARGET.md`

## 6. 推荐执行方式

把 `CODEX_START_PROMPT.md` 的全文直接交给 Codex。

Codex 必须自行：
- 检查环境；
- 创建本地输出目录；
- 执行当前 Stage；
- 自检；
- 记录结果；
- 只有真正需要用户操作时才停下来请求输入。

不要让用户手工替 Codex 执行可以自动完成的命令。
