# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。只记录当前状态与权威资产指针；稳定方法论放在 `04_HARNESS/rules/`。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W09 / SUBTITLE_STYLE_OPTIMIZATION`
- STATE: `W02A_PASS / W07_PASS / SHOT_LIBRARY_READY / EDITOR_AUDIO_GATE_PASS / V3_2_PICTURE_LOCKED / EDIT_PREVIEW_QA_PASS / SUBTITLE_STYLE_PENDING`
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

## W07.5 Shot Library｜LOCKED PROCESS

- all 9 original ~5s sources preserved unchanged;
- 22 usable Atom/Arc edit units mapped;
- duplicate / topology-risk / meaningless micro-shot units excluded from main pool;
- derived WEB proxies have source audio removed;
- WEB batch transform: `crop=576:1024:72:128 -> scale=720:1280` (~`1.25×`);
- top-left / bottom-right platform-mark risk checked clear in normalized review.

Map:
`06_TESTS/MV/WEB_R2/W07_5_NORMALIZED_SHOT_LIBRARY_MAP.csv`

## W08B V3.2 Picture Edit｜LOCKED

User feedback:
`这次的效果不错，按这个方案先进行固化`

Accepted basis:
- Atom-first editing;
- retain a coherent multi-shot Arc only when it has explicit Director value;
- no opaque multi-shot 5s block is treated as a single unknown source during final edit;
- visible-shot count is audited in addition to external fragment count.

Accepted Edit Map:
`06_TESTS/MV/WEB_R2/W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`

Gate receipt:
`06_TESTS/MV/WEB_R2/W08B_V3_2_PICTURE_GATE_PASS_RECEIPT.json`

Technical identity:
- 13 selected visible units;
- 891 frames / 24fps / 37.125s picture;
- locked audio 37.120s;
- preview-vs-locked-BGM global lag `0.000000s`;
- accepted preview SHA-256 `797ac52cf470fb871f312b7699247b9f0bbc46120d1124813e39a459f4f1812f`.

States:
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES`

Picture timing/rhythm is now frozen for W09 except for a later clearly evidenced local defect.

## W09 Subtitle state｜CURRENT

Timing source is already locked:
`AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`

W09 may change only presentation/implementation, not lyric timing.

Next work:
1. subtitle typography/size;
2. tight semi-transparent box;
3. horizontal + vertical centering;
4. padding consistency;
5. lower safe area;
6. longest-line wrapping;
7. restrained fade after timing confirmation;
8. first/middle/longest/final-line visual QA;
9. rendered subtitle vs canonical SRT implementation QA.

Current states:
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

Proceed with W09 subtitle visual style candidates on the locked V3.2 picture edit and canonical `lyrics_exact.srt` unchanged.
