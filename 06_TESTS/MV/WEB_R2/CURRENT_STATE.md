# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。只记录当前状态与权威资产指针；稳定方法论放在 `04_HARNESS/rules/`。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W09 / R1_GOLDEN_SUBTITLE_IMPLEMENTATION_QA`
- STATE: `W02A_PASS / SHOT_LIBRARY_READY / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / R1_GOLDEN_SUBTITLE_STYLE_TARGET_LOCKED / IMPLEMENTATION_QA_NEXT`
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

User accepted V3.2 Atom-first direction.

Accepted Edit Map:
`06_TESTS/MV/WEB_R2/W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`

Gate receipt:
`06_TESTS/MV/WEB_R2/W08B_V3_2_PICTURE_GATE_PASS_RECEIPT.json`

Technical identity:
- 13 selected visible units;
- 891 frames / 24fps / 37.125s picture;
- locked audio 37.120s;
- preview-vs-locked-BGM global lag `0.000000s`.

States:
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`

## W09 Subtitle｜R1 GOLDEN TARGET LOCKED

User rejected new A/B/C experiments and explicitly selected the previously accepted R1 subtitle standard.

Lock note:
`06_TESTS/MV/WEB_R2/W09_R1_GOLDEN_SUBTITLE_STYLE_LOCK.md`

R1 target:
- bold clean Chinese sans serif;
- near-white text;
- tight dark semi-transparent background box;
- centered horizontally/vertically in box;
- subtitle center around `y≈1010` on 720×1280;
- max 2 lines;
- restrained fade ~`0.1s in / 0.15–0.2s out`;
- no karaoke/decorative extras.

Current WEB implementation uses `Noto Sans CJK SC Bold`, size `34`, center `x=360/y=1010`, `100ms/180ms` fade as a layout-faithful R1 proxy. Exact numeric font size was not preserved as a hard R1 equality target; R1 Golden prioritizes layout/readability.

Timing remains canonical W02A and is not changed.

Current states:
- `SUBTITLE_STYLE_TARGET_LOCKED = R1_GOLDEN`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO / NEXT`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

1. Verify current R1-style burned subtitles against canonical W02A timing.
2. If implementation QA passes, enter W10 final technical/full-watch QA.
3. No new subtitle style exploration unless user explicitly reopens it.
