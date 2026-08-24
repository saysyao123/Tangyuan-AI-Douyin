# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。只记录当前状态与权威资产指针；稳定方法论放在 `04_HARNESS/rules/`。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W10 PASS / W11 CLOSE_PENDING`
- STATE: `W02A_PASS / SHOT_LIBRARY_READY / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / SUBTITLE_STYLE_QA_PASS / SUBTITLE_IMPLEMENTATION_QA_PASS / FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED`
- BRANCH: `test/mv-web-r2`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Runtime authority

- Workflow: `04_HARNESS/workflows/mv.md` v1.5
- Golden Runtime: `04_HARNESS/rules/mv_golden_runtime.md` v1.3
- Audio Timeline: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- Editing Runtime: `04_HARNESS/rules/mv_editing.md` v1.1+
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

- 9 original ~5s files preserved;
- 22 usable Atom/Arc units mapped;
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

## W09 Subtitle｜LOCKED

User accepted the R1-derived screenshot-calibrated subtitle system and requested it become the stable default instead of restarting style exploration each project.

Lock receipt:
`06_TESTS/MV/WEB_R2/W09_SUBTITLE_STYLE_LOCK_RECEIPT.json`

720×1280 baseline:
- `Noto Sans CJK SC Bold`, nominal `46px`;
- near-white text + restrained dark outline;
- lower center around `x=360 / y=1009`;
- dark semi-transparent rounded box;
- **10px padding on all four sides**;
- max 2 lines;
- fade `100ms in / 180ms out`;
- timing exclusively from canonical Audio Timeline Package.

Hard implementation rule:
- measure actual rendered glyph/text bbox for every line;
- generate box fresh from that bbox + target padding;
- never resize/inset a legacy rounded path;
- QA every line: four-side padding target ±1px; text/box center error <=1px;
- shortest line + longest one-line + two-line + first + final are mandatory sampled QA cases.

W09 implementation result:
- 10 lines checked;
- max ASS-vs-canonical time delta `0.005s`;
- all geometry `10/10/10/10px` PASS;
- prior short-line defect `L05 好吧哎哟哎哟` PASS after bbox regeneration;
- two-line L09 PASS.

States:
- `SUBTITLE_STYLE_QA_PASS = YES`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`

## W10 Final QA｜PASS

Receipt:
`06_TESTS/MV/WEB_R2/W10_FINAL_TECH_QA_RECEIPT.json`

Final technical identity:
- 720×1280 / H.264 / 24fps / 891 frames;
- picture `37.125s`;
- locked audio `37.120s`;
- preview/final decoded audio vs locked BGM global lag `0.000000s`;
- no detected black frames;
- WEB top-left/bottom-right watermark-risk samples clear;
- source metadata stripped by stream-copy final remux; no picture/audio retime introduced.

Final file:
`如果你也刚好抬头看树_MV_WEB_R2_FINAL.mp4`

Final SHA-256:
`ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`

States:
- `FINAL_TECH_QA_PASS = YES`
- `DELIVERABLE_RENDERED = YES`

## Next Allowed Action

W11 close:
1. deliver final package to user;
2. preserve accepted subtitle rule/gate as reusable runtime baseline;
3. write final WEB R2 retrospective only if it adds new durable rules not already promoted;
4. mark Round closed after final user acceptance.
