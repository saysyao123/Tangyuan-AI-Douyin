# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W00`
- STAGE_NAME: `Bootstrap / Capability Baseline`
- STATE: `READY_TO_START`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Objective

从一首新的候选歌开始，在网页端重新跑完整 MV 流程，并逐 Stage 标记：

- `AUTO`
- `HUMAN_GATE`
- `EXTERNAL_REQUIRED`
- `PARTIAL`
- `BLOCKED`

重点不是假装全自动，而是测出网页端的真实自动化边界。

## Golden Quality Floor

R1 Golden Sample 是质量下限，不要求复制纸墨视觉：
- 单帧美感不得明显更低；
- 歌词视觉命中不得明显更低；
- 导演/运镜重复度不得更高；
- 动态失败必须做根因分析；
- 剪辑与字幕时间不得低于 R1 最终通过水平。

## Stage Map

- `W00` Bootstrap / capability baseline
- `W01` Song discovery / benchmark-assisted selection
- `W02` Reference BGM acquisition + exact clip lock
- `W03` Music / lyric / Beat analysis
- `W04` Director concept + production-unit allocation
- `W05` First-frame prompts + image generation
- `W06` Dynamic prompts + external Seedance generation gate
- `W07` Dynamic QA + retry design
- `W08` Edit + subtitle alignment + final polish
- `W09` Automation retrospective / Round close

## Expected Automation Hypothesis

Initial hypothesis to test, not pre-declared truth:
- W01: mostly AUTO, user only final song preference gate.
- W02: AUTO if usable audio file/source is available; otherwise may require minimal user upload.
- W03: AUTO.
- W04: AUTO + optional user creative review.
- W05: prompts AUTO, image generation AUTO in ChatGPT, user review is HUMAN_GATE.
- W06: prompt design AUTO; Seedance execution currently expected `EXTERNAL_REQUIRED`.
- W07: AUTO after user uploads generated clips.
- W08: AUTO once source clips and locked audio are available; subtitle alignment method depends on available audio/ASR resources.
- W09: AUTO.

These must be updated from real execution evidence.

## Next Allowed Action

Run `W00` only.

Read:
1. `README.md`
2. `WEB_R2_MASTER_PLAN.md`
3. `AUTOMATION_MATRIX.md`
4. `WEB_START_PROMPT.md` only as launch contract

Then establish actual available tools and move to W01 without asking the user questions that can be resolved automatically.
