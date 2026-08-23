# WEB R2｜CURRENT_STATE

> WEB R2唯一状态入口。新 Chat / Agent 必须先读 Workflow v1.3 + Golden Runtime + MV Audio Timeline Rule，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08B / V3_EDIT_PREVIEW_VIEWING_GATE`
- STAGE_NAME: `V3 Picture+BGM Preview human aesthetic viewing`
- STATE: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / EDIT_MAP_LOCKED / PICTURE_PREVIEW_RENDERED / TECH_QA_PASS / AESTHETIC_VIEWING_PENDING`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.3
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.2
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
- EDIT_MAP: `06_TESTS/MV/WEB_R2/W08B_V3_EDIT_MAP_v1.csv`
- EDIT_PREVIEW_QA: `06_TESTS/MV/WEB_R2/W08B_V3_EDIT_PREVIEW_QA_v1.md`
- W02A_GATE_RECEIPT: `06_TESTS/MV/WEB_R2/W02A_GATE_PASS_RECEIPT.json`
- W02A_SYNC_RECEIPT: `06_TESTS/MV/WEB_R2/W02A_PACKAGE_SYNC_RECEIPT.json`
- ROOT_CAUSE_AUDIT: `06_TESTS/MV/WEB_R2/W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Valid locked upstream results

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, content timeline `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W02A: `AUDIO_TIMELINE_PACKAGE_LOCKED / PASS`
- W04: `DIRECTOR_PLAN_LOCKED` — `树影之外`
- W05: `FIRST_FRAME_SET_LOCKED` — 9/9 accepted
- W06/W06-X: dynamic prompt/camera experiment + S1–S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim
- W08A: `EDITOR_AUDIO_GATE_PASS`
- W08B: `EDIT_MAP_LOCKED / V3 Picture Preview rendered`

Do not reopen approved visual-generation stages unless a specific preview defect proves a source-duration/source-quality gap.

## Revoked artifacts｜HARD

### V1
`REVOKED / TECHNICAL_RESCUE`

Reason:
- edit/subtitle proceeded before valid lyric timing;
- subtitle style drifted from R1 Golden.

### V2
`REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`

Reason:
- wrong nine-line excerpt assumption;
- diagnostic acoustic timing was repackaged as exact;
- QA proved render-vs-SRT, not SRT-vs-vocal ground truth.

V1/V2 timing assets may not be reused as timing truth.
Visual source-selection lessons may be reused.

## W02A canonical timing truth

Strong Route:
- trusted Chinese lyrics -> CTC forced alignment;
- model: `jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`;
- revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`;
- 92 target tokens -> 92 aligned spans;
- no free ASR lyric transcription used as truth.

Ground-truth QA:
- CTC vs prior diagnostic candidate median absolute line-start delta: `0.125s`;
- repeated chorus L01–L07 source-time shift median: `81.527s`;
- maximum repeat-shift deviation: `0.061s`;
- no chorus occurrence swap.

Machine Gates:
- Timing Core Gate: exit `0`, 10 lines, 0 errors/warnings;
- Complete Package Gate: exit `0`, 10 lines, 10 anchors, 21 music events, 0 errors/warnings;
- `package_manifest.json`: `AUDIO_TIMELINE_PACKAGE_LOCKED=true`.

Canonical sync:
- workflow run `32655263045`;
- payload ZIP SHA `c8308512c9f1dd63fabe70dcafb27e0a75b2d0d3450f80371429f665866656be`;
- status `W02A_CANONICAL_PACKAGE_SYNCED`.

## Canonical lyric timeline

| Line | Lyric | Start | End |
|---|---|---:|---:|
| L01 | 我要学着树叶翩翩起舞 | 0.440 | 3.702 |
| L02 | 喊几声布谷布谷 | 3.702 | 6.023 |
| L03 | 或许少有人知道 | 6.023 | 8.304 |
| L04 | 有鸟儿是这样叫 | 8.304 | 10.946 |
| L05 | 好吧哎哟哎哟 | 10.946 | 13.067 |
| L06 | 一颗心叽叽喳喳飞过了树梢 | 13.067 | 19.090 |
| L07 | 如果你也刚好抬头看树 | 19.090 | 23.493 |
| L08 | 向一朵白云学习如何漂浮 | 23.493 | 28.415 |
| L09 | 在某天某个随机的清晨或是下午 | 28.415 | 32.838 |
| L10 | 坐下来别那么严肃 | 32.838 | 37.120 |

Canonical timing/editor files:
- `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`
- `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`
- `AUDIO_TIMELINE_PACKAGE/anchor_words.csv`
- `AUDIO_TIMELINE_PACKAGE/music_events.csv`
- `AUDIO_TIMELINE_PACKAGE/raw_evidence/alignment_raw.ctc_forced.json`
- `AUDIO_TIMELINE_PACKAGE/alignment_provenance.json`
- `AUDIO_TIMELINE_PACKAGE/package_manifest.json`

## W08B V3 Edit Map result

The old V1/V2 visual order was not reused because it was built around the wrong first-lyric assumption.

V3 reorders accepted material against canonical timing:
- opening: S2 leaf/hand -> S4 dance for L01;
- L02: short S5 upward/giant-tree cue without prematurely revealing bird;
- L03: S3 intimate eye/veil;
- L04: S6 person -> bird -> person, with bird reveal ~`8.542s` vs `鸟儿` anchor `8.525s`;
- L06: S4 energy rise -> S7 clean peak -> S7 clean canopy resolve;
- L07/title: S1 monumental tree -> low-angle look-up -> eye -> canopy;
- L08: shortened S8 literal cloud -> S3 floating veil;
- L09: S5 morning light -> S4 human bridge;
- L10/tail: long S9 cloud/sky release.

W07 risk exclusions preserved:
- S1 source frames `58–75` excluded (duplicate low-angle family);
- S7 source frames `65–97` excluded (fabric topology risk);
- S8 ~`2.917s`, S9 ~`4.292s` to preserve short reset vs long final-release roles.

Picture clock:
- `24fps`;
- `891 frames`;
- `37.125s`;
- locked audio content `37.120s`;
- end quantization delta `+0.005s`.

`EDIT_MAP_LOCKED = YES`

## V3 Picture+BGM Preview technical QA

Preview identity:
- filename: `如果你也刚好抬头看树_MV_WEB_R2_V3_PicturePreview.mp4`
- SHA-256: `09e68c852d50fd43059fa70b8555ec7a742451af27ca2e3c177595ae5f240111`
- H.264 `720×1280`, 24fps, SAR `1:1`;
- video `37.125s / 891 frames`;
- AAC audio `37.120s`.

Audio implementation check:
- Preview decoded audio vs locked v3 BGM best global lag: `0.000s`;
- normalized correlation: ~`0.99960`;
- no new AAC/FFmpeg global timing shift.

Source audio policy:
- all Seedance source audio ignored at ingest;
- only locked W02 v3 BGM is mapped.

Preview safe crop:
- `crop=630:1120:20:72 -> scale=720:1280 -> SAR 1:1`;
- used consistently for the viewing preview.

Anchor-frame spot checks:
- ~8.40s person -> ~8.55s bird;
- 20.85s low-angle look-up;
- 21.40s eye close-up;
- 24.35s white cloud;
- 26.05s wind/veil portrait;
- 30.70s morning light / giant tree;
- 32.83s transition into final cloud release.

`PICTURE_PREVIEW_RENDERED = YES`
`EDIT_PREVIEW_TECH_QA_PASS = YES`
`EDIT_PREVIEW_QA_PASS = NO / AESTHETIC_VIEWING_PENDING`

## Current Package / Runtime state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = YES`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = YES`
- `LYRIC_TIMELINE_LOCKED = YES`
- `ANCHOR_WORD_MAP_LOCKED = YES`
- `MUSIC_EVENT_MAP_VERIFIED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = YES`
- `PICTURE_PREVIEW_RENDERED = YES`
- `EDIT_PREVIEW_TECH_QA_PASS = YES`
- `EDIT_PREVIEW_QA_PASS = NO / AESTHETIC_VIEWING_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

**Human viewing Gate on the actual V3 Picture+BGM Preview.**

If user accepts:
`EDIT_PREVIEW_QA_PASS -> W09 Subtitle Style + Implementation QA`.

W09 must use canonical `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`; it may style/render subtitles but may not invent or nudge a parallel lyric timing table.

If user identifies a specific visual rhythm problem:
modify only the affected W08B fragment(s); W02A remains locked unless the audio itself changes.
