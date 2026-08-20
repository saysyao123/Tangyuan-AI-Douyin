# CODEX R1｜CURRENT_STATE

> Codex 专用状态入口。任何 Codex / Agent 进入本测试必须先读本文件。

## Current Status

- TEST: `CODEX_R1`
- BRANCH: `test/mv-codex-r1`
- MODE: `MODE_A_ENGINEERING_REPRODUCTION`
- STAGE: `C00`
- STAGE_NAME: `Bootstrap / Environment Preflight`
- STATE: `READY_TO_START`
- HUMAN_GOLDEN_ROUND: `06_TESTS/MV/ROUND_01`
- GOLDEN_SAMPLE: `你有没有真的爱过我｜阿图表妹`
- GOLDEN_DURATION: `36.80s`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Test Objective

在不修改人工 R1 已通过创意决定的前提下，测试 Codex 能否尽量自动完成：

`环境检查 -> BGM / 数据源 -> 精确音频裁剪 -> Whisper 字幕 -> 无水印高清源 -> 剪辑复刻 -> 字幕烧录 -> QA -> 最终报告`

## Hard Boundaries

1. 人工 R1 是 Golden Truth，Codex 不得覆盖 `06_TESTS/MV/ROUND_01/*`。
2. Codex 测试提交只进入 `test/mv-codex-r1`，不得直接修改人工 Golden 分支。
3. 不得静默换歌、换版本、改音频区间、改歌词、改镜头顺序。
4. 不得把缺失能力伪装成 PASS。
5. 如果需要外部登录 / CAPTCHA / 外部生成工具，标记真实状态并请求最小人工介入。
6. 发布级视频必须使用无水印高清源；如果无法获取，最终状态不能写 `PUBLISH_READY`。

## Golden Locks

- Song: `你有没有真的爱过我`
- Artist: `阿图表妹`
- Human source interval: `00:01:23.800 -> 00:02:00.600`
- Reference duration: `36.80s`
- Human accepted final family: `R1_MV_v4_final_polish.mp4`
- Human accepted lyric timing source: `lyrics_exact_v3_1.srt`
- Segment order: `S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8`

## Stage Map

- `C00` Environment preflight
- `C01` BGM / datasource reproduction
- `C02` Audio exact-cut reproduction
- `C03` Whisper + lyric constrained alignment
- `C04` Source-video discovery / watermark-free HD replacement
- `C05` Timeline reconstruction
- `C06` Subtitle render + final polish
- `C07` Automated QA / Golden comparison
- `C08` Final result report / close

## Next Allowed Action

1. Confirm branch is `test/mv-codex-r1`; if not, checkout it.
2. Run `C00` only.

Read:
- `CODEX_R1_MASTER_PLAN.md`
- `INPUT_CONTRACT.md`
- `GOLDEN_TARGET.md`

Then execute environment preflight. Do not jump directly to editing.
