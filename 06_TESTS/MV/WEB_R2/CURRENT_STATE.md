# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。Round 已完成；稳定方法论已晋升到 `04_HARNESS/workflows|rules|templates/`，本文件只保留最终状态与资产指针。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W11 / CLOSED`
- STATE: `COMPLETE_LOCKED`
- BRANCH: `test/mv-web-r2`
- CLOSED_AT: `2026-08-24 Asia/Manila`
- USER_FINAL_ACCEPTANCE: `目前，我觉得这个已经OK了，可以进行一次收口`

## Runtime authority promoted from R2

- Workflow: `04_HARNESS/workflows/mv.md` v1.7
- Golden Runtime: `04_HARNESS/rules/mv_golden_runtime.md` v1.4
- Audio Timeline: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- Human Gates: `04_HARNESS/rules/mv_human_gates.md` v1.0
- Editing Runtime: `04_HARNESS/rules/mv_editing.md` v1.1+
- Source Normalization: `04_HARNESS/rules/mv_source_normalization.md` v1.0
- Subtitle Runtime: `04_HARNESS/rules/mv_subtitle.md` v1.0
- AI Video: `04_HARNESS/rules/ai_video.md` v1.3+
- Zero-context next-round template: `04_HARNESS/templates/mv_zero_context_start_prompt.md` v1.0

## Final accepted identity

- song: `如果你也刚好抬头看树` / 孙天宇
- locked BGM source: `139.930s–177.050s`
- locked BGM content: `37.120s`
- locked BGM SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- final video: `如果你也刚好抬头看树_MV_WEB_R2_FINAL.mp4`
- final SHA-256: `ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`

## Locked production assets

### Audio truth
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

State:
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`

### Director / first frames / dynamic
- Director concept: `树影之外`
- first frames: `9/9 accepted`
- dynamic sources: `2S1–2S9`
- source QA: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`

### Shot Library
`06_TESTS/MV/WEB_R2/W07_5_NORMALIZED_SHOT_LIBRARY_MAP.csv`

State:
`SHOT_LIBRARY_READY = YES`

R2 WEB fallback used consistent batch crop/zoom around `1.25×`; value is batch-specific, method is reusable.

### Picture Edit
`06_TESTS/MV/WEB_R2/W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`

States:
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`

Accepted basis:
- Atom-first;
- retain Arc only when it has Director value;
- long-cut-first;
- count perceptible visible shots, not external blocks only.

### Subtitle
Runtime:
`04_HARNESS/rules/mv_subtitle.md`

Lock receipt:
`06_TESTS/MV/WEB_R2/W09_SUBTITLE_STYLE_LOCK_RECEIPT.json`

Accepted 720×1280 baseline:
- bold clean Chinese sans serif / nominal 46px family;
- center around `360,1009`;
- dark semi-transparent rounded box;
- four-side padding `10px`;
- actual glyph bbox -> fresh box generation;
- max 2 lines;
- fade `100ms / 180ms`;
- all-line geometry QA required.

States:
- `SUBTITLE_STYLE_QA_PASS = YES`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`

### Final QA
Receipt:
`06_TESTS/MV/WEB_R2/W10_FINAL_TECH_QA_RECEIPT.json`

Result:
- `720×1280 / 24fps / 891 frames`
- picture `37.125s`
- audio `37.120s`
- audio global lag `0.000000s`
- subtitle max implementation delta `0.005s`
- blackdetect `0`
- WEB sampled corner watermark-risk clear

States:
- `FINAL_TECH_QA_PASS = YES`
- `DELIVERABLE_RENDERED = YES`

## Close assets

- Final retrospective + future SOP:
  `06_TESTS/MV/WEB_R2/WEB_R2_FINAL_RETROSPECTIVE_AND_SOP_v1.md`
- Close receipt:
  `06_TESTS/MV/WEB_R2/W11_CLOSE_RECEIPT.json`

## Final state chain

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `DIRECTOR_BEAT_MAP`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPT_SET_READY`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `SHOT_LIBRARY_READY`
→ `EDITOR_AUDIO_GATE_PASS`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`
→ **`COMPLETE_LOCKED`**

## Reopen policy

WEB R2 is closed. Do not continue editing this Round by default.
If a future regression needs R2 evidence, load only the specific receipt/artifact/rule required for diagnosis.
New MV work should use:
`04_HARNESS/templates/mv_zero_context_start_prompt.md`
with a new Round state rather than reopening WEB R2.
