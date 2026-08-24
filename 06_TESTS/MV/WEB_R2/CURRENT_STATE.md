# WEB R2｜CURRENT_STATE

> WEB R2 唯一状态入口。新 Chat / Agent 必须先读 Workflow v1.3 + Golden Runtime + MV Audio Timeline Rule，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08B / V3.1_LONG_CUT_SUBTITLE_VIEWING_GATE`
- STAGE_NAME: `V3.1 long-cut picture edit + diagnostic exact-lyric subtitle human viewing`
- STATE: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / V3_SUPERSEDED_BY_USER_FEEDBACK / V3_1_CANDIDATE_RENDERED / TECH_QA_PASS / HUMAN_VIEW_PENDING`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.3
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.2
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
- CURRENT_EDIT_MAP: `06_TESTS/MV/WEB_R2/W08B_V3_1_LONG_CUT_EDIT_MAP_v1.csv`
- CURRENT_PREVIEW_QA: `06_TESTS/MV/WEB_R2/W08B_V3_1_LONG_CUT_SUBTITLE_PREVIEW_QA.md`
- PREVIOUS_V3_EDIT_MAP: `06_TESTS/MV/WEB_R2/W08B_V3_EDIT_MAP_v1.csv`
- W02A_GATE_RECEIPT: `06_TESTS/MV/WEB_R2/W02A_GATE_PASS_RECEIPT.json`
- W02A_SYNC_RECEIPT: `06_TESTS/MV/WEB_R2/W02A_PACKAGE_SYNC_RECEIPT.json`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Locked upstream truth

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, content timeline `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W02A: `AUDIO_TIMELINE_PACKAGE_LOCKED / PASS`
- W04: `DIRECTOR_PLAN_LOCKED` — `树影之外`
- W05: `FIRST_FRAME_SET_LOCKED` — 9/9 accepted
- W06/W06-X: dynamic prompt/camera experiment + 2S1–2S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim
- W08A: `EDITOR_AUDIO_GATE_PASS`

Do not reopen approved visual-generation stages unless a specific preview defect proves a real source shortage.

## Revoked / superseded edit artifacts

### V1
`REVOKED / TECHNICAL_RESCUE`
- picture/subtitle work began before valid lyric timing;
- subtitle style drifted.

### V2
`REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`
- wrong excerpt assumption;
- diagnostic timing was promoted without Strong Route provenance;
- QA proved render-vs-SRT, not SRT-vs-vocal.

### V3
`SUPERSEDED_BY_USER_AESTHETIC_FEEDBACK`
- timing/order correction was materially better;
- user feedback: external cuts still felt too fragmented / visually busy;
- V3 timing truth remains valid, but its 17-fragment picture map is no longer the active candidate.

## Canonical W02A lyric clock

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

Canonical files:
- `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`
- `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`
- `AUDIO_TIMELINE_PACKAGE/anchor_words.csv`
- `AUDIO_TIMELINE_PACKAGE/music_events.csv`
- `AUDIO_TIMELINE_PACKAGE/raw_evidence/alignment_raw.ctc_forced.json`
- `AUDIO_TIMELINE_PACKAGE/alignment_provenance.json`
- `AUDIO_TIMELINE_PACKAGE/package_manifest.json`

W02A machine gates remain PASS; the audio/lyric truth is not reopened by V3.1 picture changes.

## V3.1 Long-Cut strategy

User requested a less fragmented cut and requested subtitles be embedded to judge alignment.

Main change:
- V3 external fragments: `17`
- V3.1 external fragments: `9`
- no V3.1 external fragment shorter than `2.0s`
- Anchor Word no longer automatically equals picture cut
- generated clips with useful internal multi-shot grammar are allowed to carry semantic hits internally

Active sequence:
1. S2 Arc / leaves — `0.000–3.000`
2. S4 dance long section — `3.000–7.125`
3. S6 person→bird→person complete structure — `7.125–12.125`
4. S3 emotional close-up — `12.125–14.125`
5. S7 clean motion peak — `14.125–16.833`
6. S5 one-take breathing shot, slowed smoothly — `16.833–23.625`
7. S8 sky/space long shot — `23.625–28.417`
8. S1 giant-tree/morning-light source sequence — `28.417–32.833`
9. S9 final release — `32.833–37.125`

Key semantics retained:
- S6 internal bird reveal remains ~`8.54s`, near `鸟儿 8.525s`;
- S7 clean early region carries `飞过树梢` peak;
- title line L07 is carried inside the long S5 breathing shot without external cuts;
- L09 begins essentially with S1 giant-tree/morning-light sequence;
- S9 enters ~5ms before L10 and remains uninterrupted through tail.

## V3.1 subtitle diagnostic overlay

User explicitly requested subtitles in this preview to judge alignment.

Rules:
- source timing: canonical W02A `line_timeline.csv` only;
- no free ASR / no manual nudge / no picture-derived subtitle timing;
- subtitle fade intentionally disabled for this diagnostic preview so apparent timing is not distorted by fade;
- rendering at 24fps means only normal display-frame quantization applies (`<41.667ms`; measured maximum start quantization ~`37ms`);
- visual style for this preview: centered light text + semi-transparent dark tight box + lower safe area;
- this overlay does **not** lock W09 final subtitle style.

## V3.1 technical QA

Preview SHA-256:
`9088dc30c06bc65cacf50dd0b28bbd2042de95ea9a7dcf5a461aef9e903d3c0e`

Technical state:
- H.264 `720×1280`
- 24fps / SAR `1:1`
- video `891 frames / 37.125s`
- locked-audio content `37.120s`
- decoded preview audio vs locked v3 BGM best global lag: `0.000000s`
- audio correlation: `0.999043`
- all Seedance source audio discarded
- consistent safe crop used to remove lower-right platform mark in reviewed frames

`V3_1_PREVIEW_RENDERED = YES`
`V3_1_TECH_QA_PASS = YES`
`V3_1_AESTHETIC_QA_PASS = NO / HUMAN_VIEW_PENDING`
`V3_1_SUBTITLE_ALIGNMENT_VIEW_PASS = NO / HUMAN_VIEW_PENDING`

## Current runtime states

- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `EDITOR_AUDIO_GATE_PASS = YES`
- `EDIT_MAP_LOCKED = NO` — previous V3 lock superseded; V3.1 candidate awaits user acceptance
- `PICTURE_PREVIEW_RENDERED = YES / V3.1`
- `EDIT_PREVIEW_TECH_QA_PASS = YES / V3.1`
- `EDIT_PREVIEW_QA_PASS = NO / HUMAN_VIEW_PENDING`
- `SUBTITLE_STYLE_QA_PASS = NO`
- `SUBTITLE_IMPLEMENTATION_QA_PASS = NO` — diagnostic overlay is not W09 lock
- `FINAL_TECH_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Next Allowed Action

**Human viewing Gate on V3.1 long-cut + exact-subtitle diagnostic preview.**

The user should judge two things separately:
1. whether the 9-fragment long-cut rhythm is calmer / more coherent;
2. whether each lyric subtitle visually enters/exits with the sung vocal.

If both are accepted:
- lock V3.1 Edit Map;
- `EDIT_PREVIEW_QA_PASS = YES`;
- enter W09 and finalize subtitle style/implementation without changing canonical timing.

If only picture rhythm needs changes:
- modify W08B picture fragments only.

If the user perceives subtitle timing mismatch:
- first inspect the exact reported line against W02A ground-truth assets; do not manually nudge all subtitles or reopen unrelated picture work.
