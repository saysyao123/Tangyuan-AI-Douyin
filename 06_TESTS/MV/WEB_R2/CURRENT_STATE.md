# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。只记录当前状态与权威资产指针；稳定方法论放在 `04_HARNESS/rules/`，避免状态文件重复膨胀。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08B / V3.2_ATOMIC_ROUGH_VIEWING_GATE`
- STATE: `W02A_PASS / W07_SOURCE_QA_PASS / SHOT_LIBRARY_READY / EDITOR_AUDIO_GATE_PASS / V3_1_BETTER / V3_2_ATOMIC_CANDIDATE_RENDERED / HUMAN_VIEW_PENDING / SUBTITLE_STYLE_NOT_LOCKED`
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

- W01 song: `如果你也刚好抬头看树` / 孙天宇
- W02 BGM: source `139.930s–177.050s`; content `37.120s`
- locked BGM SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W02A: `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- W04 Director: `树影之外`
- W05 first frames: 9/9 accepted
- W06/W06-X: 2S1–2S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- W08A: `EDITOR_AUDIO_GATE_PASS = YES`

Canonical timing package:
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

Do not reopen W02A unless audio identity/version/clip/speed/lyrics changes.

## W07.5 Shot Normalization｜NEW

User proposed: generated 1–3-shot videos should first be organized into single-state material before final editing.

Implemented non-destructively:
- all 9 original 5s videos preserved;
- 22 usable Atom/Arc derived edit units;
- duplicate / topology-risk / meaningless micro-shot units excluded from main Atom pool;
- source audio removed from derived WEB proxies;
- whole-source watermark-safe transform used consistently: `crop=576:1024:72:128 -> scale=720:1280`, about `1.25×` enlargement;
- reviewed normalized units show no remaining top-left / bottom-right platform mark.

Map:
`06_TESTS/MV/WEB_R2/W07_5_NORMALIZED_SHOT_LIBRARY_MAP.csv`

State:
`SHOT_LIBRARY_READY = YES`

## Current edit candidates

### V3.1｜Long-cut candidate
- 9 external timeline fragments;
- user judged it materially calmer/better than V3;
- weakness discovered: several 5s sources contain hidden internal cuts, so perceptible visible-shot count is still materially higher than 9.

### V3.2｜Atomic rough-cut candidate
- built from explicit single-state Atoms rather than opaque multi-shot source blocks;
- 13 selected visible units;
- no hidden/random internal cuts inside selected Atom units;
- total picture: `891 frames / 24fps / 37.125s`;
- locked audio: `37.120s`;
- decoded preview audio vs locked BGM best global lag: `0.000000s`;
- audio correlation: `0.999047`;
- preview SHA-256: `797ac52cf470fb871f312b7699247b9f0bbc46120d1124813e39a459f4f1812f`;
- diagnostic subtitle timing still comes from canonical W02A; final subtitle style remains unlocked.

Edit Map:
`06_TESTS/MV/WEB_R2/W08B_V3_2_ATOMIC_ROUGH_EDIT_MAP.csv`

QA:
`06_TESTS/MV/WEB_R2/W07_5_W08B_V3_2_ATOMIC_ROUGH_QA.md`

## Important interpretation

V3.2 does **not** automatically supersede V3.1.
The current test is whether final editing should use:
1. pure Atom-based cut; or
2. Atom-first hybrid, retaining only a few intentionally valuable multi-shot Arcs.

Stable engineering lesson:
`external fragment count` and `perceptible visible-shot count` must both be measured. A timeline with 9 fragments can still feel fragmented if those fragments contain many internal generated cuts.

## Subtitle state

- timing truth: locked W02A `lyrics_exact.srt`
- diagnostic alignment overlay: allowed
- final typography / box / padding / safe area / line wrap / restrained fade: **NOT LOCKED**
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`

## Runtime states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `SHOT_LIBRARY_READY = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = NO` — V3.1 and V3.2 still need final human picture decision
- `V3_2_ATOMIC_ROUGH_RENDERED = YES`
- `V3_2_TECH_QA_PASS = YES`
- `EDIT_PREVIEW_QA_PASS = NO / HUMAN_VIEW_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

1. Human view V3.2 atomic rough cut and compare its calmness/control with V3.1.
2. Choose the final picture basis: `ATOM` or `ATOM-FIRST HYBRID`.
3. Make only picture-level corrections needed by that decision; do not reopen audio timing.
4. Lock final Edit Map and pass `EDIT_PREVIEW_QA`.
5. Enter W09 subtitle visual optimization using canonical `lyrics_exact.srt` unchanged.
6. Final full-watch + technical QA, then delivery.