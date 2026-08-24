# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。只记录当前状态与权威资产指针；稳定方法论放在 `04_HARNESS/rules/`。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W09 / R1_SCREENSHOT_SUBTITLE_CALIBRATION`
- STATE: `W02A_PASS / SHOT_LIBRARY_READY / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / PREVIOUS_R1_PROXY_REJECTED / ACTUAL_R1_SCREENSHOT_REFERENCE_ACTIVE / V2_EQUAL_PADDING_CANDIDATE_RENDERED / HUMAN_VIEW_PENDING`
- BRANCH: `test/mv-web-r2`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Runtime authority

- Workflow: `04_HARNESS/workflows/mv.md` v1.5
- Golden Runtime: `04_HARNESS/rules/mv_golden_runtime.md` v1.3
- Audio Timeline: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- Editing Runtime: `04_HARNESS/rules/mv_editing.md` v1.0
- Source Normalization: `04_HARNESS/rules/mv_source_normalization.md` v1.0
- AI Video: `04_HARNESS/rules/ai_video.md` v1.3

## Locked upstream truth

- song: `如果你也刚好抬头看树` / 孙天宇
- locked BGM: source `139.930s–177.050s`; content `37.120s`
- BGM SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- Director: `树影之外`
- first frames: 9/9 accepted
- dynamic sources: 2S1–2S9
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `SHOT_LIBRARY_READY = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`

Canonical timing package:
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

## W07.5 Shot Library｜LOCKED

- all 9 original sources preserved;
- 22 usable Atom/Arc edit units mapped;
- duplicate/topology-risk/meaningless micro-shots excluded;
- derived WEB proxies source-audio removed;
- WEB batch transform: `crop=576:1024:72:128 -> scale=720:1280` (~`1.25×`).

Map:
`06_TESTS/MV/WEB_R2/W07_5_NORMALIZED_SHOT_LIBRARY_MAP.csv`

## W08B V3.2 Picture Edit｜LOCKED

Accepted Edit Map:
`06_TESTS/MV/WEB_R2/W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`

Gate receipt:
`06_TESTS/MV/WEB_R2/W08B_V3_2_PICTURE_GATE_PASS_RECEIPT.json`

States:
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`

## W09 Subtitle｜ACTUAL R1 SCREENSHOT IS VISUAL TRUTH

Correction:
- the prior WEB implementation labeled `R1_GOLDEN` was only a prose-spec proxy and was rejected by user visual comparison;
- the user-provided actual R1 screenshot is the higher-priority visual reference for subtitle appearance.

Observed R1 screenshot characteristics:
- bold clean sans serif;
- near-white text;
- dark substantial semi-transparent rounded rectangle;
- text optically centered inside the box;
- lower safe-area center around the historical `y≈1010` family;
- restrained fade;
- max 2 lines; no karaoke/decorative extras.

### Current calibrated WEB candidate v2｜EQUAL PADDING

User feedback on v1:
- overall direction acceptable;
- background left/right excess too large;
- all four sides should use a consistent modest padding;
- text must be centered horizontally and vertically inside the background.

Implementation correction:
- do **not** estimate box width from character count × nominal font size;
- first measure the actual rendered glyph pixel bounds from libass;
- construct the rounded rectangle from those real bounds;
- fixed padding: `22px` on top / bottom / left / right at 720×1280;
- nominal font: `Noto Sans CJK SC Bold`, size `46`;
- subtitle center: `x=360 / y≈1009–1010`;
- rounded radius approx `12px`;
- fade `100ms in / 180ms out`;
- canonical W02A subtitle timing unchanged.

This removes the v1 failure where horizontal box padding was much larger than vertical padding because box width used incorrect nominal-font metrics.

Current states:
- `PREVIOUS_R1_PROXY_STYLE = REJECTED`
- `R1_SCREENSHOT_CALIBRATION_V1 = REVISE_PADDING`
- `R1_SCREENSHOT_CALIBRATION_V2_EQUAL_PADDING = HUMAN_VIEW_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

1. Human-view v2 equal-padding subtitle candidate.
2. If visually accepted, lock the exact equal-padding geometry/style parameters as the R1-derived runtime subtitle reference.
3. Perform subtitle implementation QA against canonical W02A timing.
4. Enter W10 final technical/full-watch QA only after subtitle style + implementation pass.
