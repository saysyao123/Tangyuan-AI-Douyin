# WEB R2｜CURRENT_STATE

> WEB R2唯一状态入口。新 Chat / Agent 必须先读 Workflow v1.3 + Golden Runtime + MV Audio Timeline Rule，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08A / RETROFIT_STAGE_2A`
- STAGE_NAME: `AUDIO_TIMELINE_PACKAGE acquisition / provenance / ground-truth QA`
- STATE: `V1_REVOKED / V2_REVOKED / AUDIO_TIMELINE_PACKAGE_BLOCKED`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.3
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.2
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
- ROOT_CAUSE_AUDIT: `06_TESTS/MV/WEB_R2/W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`
- UPDATED_AT: `2026-08-23 Asia/Manila`

## Valid locked upstream results

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, rendered `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- trusted lyric text/order: available and previously locked
- W04: `DIRECTOR_PLAN_LOCKED` — `树影之外`
- W05: `FIRST_FRAME_SET_LOCKED` — 9/9 accepted
- W06: dynamic prompt/camera experiment completed
- W06-X: S1–S9 returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim

These visual assets were produced before Workflow v1.3. They remain usable. The new Stage 2A Gate is retrofitted before any V3 edit.

## Revoked edit artifacts

### V1
`REVOKED / TECHNICAL_RESCUE`
Reason: edit/subtitle proceeded before valid lyric timing; subtitle style drifted.

### V2
`REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`
Reason:
- `lyrics_exact_v2.srt` reused acoustic-candidate timing family;
- no new independent ASR/LRC/official timing evidence;
- QA verified render-vs-SRT, not SRT-vs-vocal ground truth.

Packaging/mux ruled out:
- final audio vs locked BGM global lag: `0.000s`;
- waveform correlation: ~`0.999`.

## Current Audio Timeline Package state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = NO`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = NO`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = NO`
- `LYRIC_TIMELINE_LOCKED = NO`
- `MUSIC_EVENT_MAP_VERIFIED = NO`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`
- `EDITOR_AUDIO_GATE_PASS = NO`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

Old v2 timing assets remain failure evidence only.

## New evidence finding

A public same-title/artist timed lyric result was found, but its later chorus timestamps conflict materially with the locked R2 audio/excerpt ordering.

Classification:
`CANDIDATE_TIMED_LYRIC / NOT TRUSTED`.

This proves that same title/artist + timestamps is insufficient; version/audio consistency must pass before LRC can be used.

## Preferred resolution

Primary:
- trusted exact Chinese lyrics + Chinese CTC forced alignment on locked 37.120s audio;
- current implementation candidate: `wangjiqing/xingyu-lyrics-aligner`.

Independent cross-check:
- CJK/song-oriented known-lyrics anchoring such as `ijuinryukichi/lyric-align`, preferably with vocal separation if the mix hides vocals.

Fast path remains allowed if a genuinely same-version platform LRC is obtained and verified.

## Next Allowed Action

Only continue building:
`06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`

Do not render V3 until:
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
AND
`EDITOR_AUDIO_GATE_PASS = YES`.

Do not reopen approved visual-generation stages unless a later verified Edit Map proves a specific source-duration gap.
