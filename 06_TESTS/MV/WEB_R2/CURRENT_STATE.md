# WEB R2｜CURRENT_STATE

> WEB R2唯一状态入口。新 Chat / Agent 必须先读 Workflow v1.3 + Golden Runtime + MV Audio Timeline Rule，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08B / V3_EDIT_MAP`
- STAGE_NAME: `Picture Edit Map using locked Audio Timeline Package + existing visual source pool`
- STATE: `V1_REVOKED / V2_REVOKED / W02A_PASS / EDITOR_AUDIO_GATE_PASS / V3_EDIT_MAP_NOT_YET_LOCKED`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.3
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.2
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
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
- W06: dynamic prompt/camera experiment completed
- W06-X: S1–S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim
- W08A: `EDITOR_AUDIO_GATE_PASS`

Visual assets produced before Workflow v1.3 remain valid. Do not reopen approved visual-generation stages unless the verified V3 Edit Map proves a specific source-duration or source-quality gap.

## Revoked edit artifacts

### V1
`REVOKED / TECHNICAL_RESCUE`

Reason:
- edit/subtitle proceeded before valid lyric timing;
- subtitle style drifted from R1 Golden.

### V2
`REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`

Reason:
- wrong nine-line excerpt lyric assumption;
- `lyrics_exact_v2.srt` reused acoustic-candidate timing family under the wrong lyric mapping;
- QA verified render-vs-SRT, not SRT-vs-vocal ground truth.

Packaging/mux was ruled out:
- final audio vs locked BGM global lag: `0.000s`;
- waveform correlation: ~`0.999`.

## W02A Strong Route resolution

The previous model-download blocker was solved without changing the locked model or publishing the song audio.

Pinned production identity:
- aligner route: trusted Chinese lyrics -> CTC forced alignment;
- model: `jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`;
- revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`;
- 92 target tokens -> 92 aligned spans;
- free ASR transcription was not used as lyric truth.

The model was ferried through GitHub Actions in integrity-checked artifacts because the web/container runtime could not directly resolve the model host. The exact locked v3 BGM was aligned locally and remained private.

Ground-truth QA:
- CTC vs prior diagnostic acoustic candidate median absolute line-start delta: `0.125s`;
- main conflicts were reviewed rather than averaged;
- first/second repeated chorus L01–L07 independently aligned with median source-time shift `81.527s`;
- maximum deviation from that repeat-shift median: `0.061s`;
- no repeated-chorus occurrence swap detected.

Canonical QA report:
`AUDIO_TIMELINE_PACKAGE/alignment_qa_report.md`

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

Canonical files:
- `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`
- `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt`
- `AUDIO_TIMELINE_PACKAGE/anchor_words.csv`
- `AUDIO_TIMELINE_PACKAGE/music_events.csv`
- `AUDIO_TIMELINE_PACKAGE/raw_evidence/alignment_raw.ctc_forced.json`
- `AUDIO_TIMELINE_PACKAGE/alignment_provenance.json`
- `AUDIO_TIMELINE_PACKAGE/package_manifest.json`

## Machine Gate result

Timing Core Gate:
- exit `0`;
- `pass=true`;
- 10/10 lines;
- 0 errors;
- 0 warnings.

Complete Package Gate:
- exit `0`;
- `pass=true`;
- 10 lines;
- 10 anchor entries;
- 21 music events;
- 0 errors;
- 0 warnings;
- generated `package_manifest.json` with `AUDIO_TIMELINE_PACKAGE_LOCKED=true`.

Canonical package sync:
- workflow run: `32655263045`;
- payload ZIP SHA-256: `c8308512c9f1dd63fabe70dcafb27e0a75b2d0d3450f80371429f665866656be`;
- sync receipt status: `W02A_CANONICAL_PACKAGE_SYNCED`.

## Current Package state

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
- `EDIT_MAP_LOCKED = NO`
- `EDIT_PREVIEW_QA_PASS = NO`
- `DELIVERABLE_RENDERED = NO`

## Editor hard entry revalidation

W08A has passed because:
- canonical `package_manifest.json` exists;
- manifest audio SHA equals the locked v3 BGM SHA;
- content timeline remains `37.120s`;
- no source clip start/end change;
- no speed/time-stretch change;
- trusted lyric text/order remains the canonical 10 lines;
- `AUDIO_TIMELINE_PACKAGE_LOCKED = true`.

Editing may now load the Package. Editing must not create a second lyric timing model.

## Next Allowed Action

Only valid next path:

`W08B V3 Edit Map`

Load together:
1. `AUDIO_TIMELINE_PACKAGE/line_timeline.csv`;
2. `AUDIO_TIMELINE_PACKAGE/anchor_words.csv`;
3. `AUDIO_TIMELINE_PACKAGE/music_events.csv`;
4. existing locked `VISUAL_SOURCE_MAP` / W07 usable windows;
5. existing W04 Director intent.

Then create the V3 Edit Map using the three clocks:
`lyric clock + music-event clock + visual-action clock`.

Hard rules:
- do not reopen W01/W02/W04/W05/W06/W07 by default;
- do not derive lyric timing from picture cuts;
- do not reuse V1/V2 timing assets;
- picture may pre-enter a lyric, but semantic hits should target verified anchors/music events;
- no V3 final render until `EDIT_MAP_LOCKED` and subsequent preview QA pass.
