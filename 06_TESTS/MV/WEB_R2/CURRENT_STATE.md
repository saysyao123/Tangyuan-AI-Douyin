# WEB R2｜CURRENT_STATE

> WEB R2唯一状态入口。新 Chat / Agent 必须先读 Workflow v1.3 + Golden Runtime + MV Audio Timeline Rule，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08A / RETROFIT_STAGE_2A`
- STAGE_NAME: `AUDIO_TIMELINE_PACKAGE acquisition / provenance / ground-truth QA`
- STATE: `V1_REVOKED / V2_REVOKED / HIGH_CONFIDENCE_LINE_TIMELINE_READY / PACKAGE_NOT_YET_LOCKED`
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
- wrong nine-line excerpt lyric assumption;
- `lyrics_exact_v2.srt` reused acoustic-candidate timing family under the wrong lyric mapping;
- QA verified render-vs-SRT, not SRT-vs-vocal ground truth.

Packaging/mux ruled out:
- final audio vs locked BGM global lag: `0.000s`;
- waveform correlation: ~`0.999`.

## Current Audio Timeline evidence

### Audio identity
- original master duration: `196.127347s`;
- locked excerpt fingerprint-measured offset in original: `139.930s`;
- normalized cross-correlation for source-offset verification: ~`0.99997`;
- therefore W02 source offset is confirmed correct.

### Critical lyric-sequence correction
The previously assumed excerpt order was wrong.
The locked 37.12s excerpt does not begin with a complete `如果你也刚好抬头看树` line.
The first full lyric is:
`我要学着树叶翩翩起舞`

The excerpt continues through:
`坐下来别那么严肃`

Canonical corrected assets:
- `AUDIO_TIMELINE_PACKAGE/trusted_lyrics_actual_excerpt_v1.txt`
- `AUDIO_TIMELINE_PACKAGE/line_timeline_high_confidence_v1.csv`
- `AUDIO_TIMELINE_PACKAGE/alignment_provenance_high_confidence_v1.md`

### Evidence method
1. exact source offset by audio fingerprint;
2. same-title/artist timed-LRC candidate establishes the correct second-chorus line order and coarse integer-second anchors;
3. official/commercial lyric text and release duration cross-check the recording identity/sequence;
4. acoustic phrase-boundary analysis on the locked excerpt refines the coarse anchors to high-confidence line-level start/end windows.

## Current Package state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_ACTUAL_EXCERPT_CORRECTED = YES`
- `HIGH_CONFIDENCE_LINE_TIMELINE_READY = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = PARTIAL` (timed-LRC source reference + acoustic analysis evidence; no retained platform raw LRC/forced-alignment raw result yet)
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = PARTIAL`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = HIGH_CONFIDENCE_PARTIAL`
- `LYRIC_TIMELINE_LOCKED = NO` (reserved for Strong Route final lock)
- `MUSIC_EVENT_MAP_VERIFIED = NO`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`
- `EDITOR_AUDIO_GATE_PASS = NO`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

## Current usable timeline status

The corrected CSV is materially stronger than V1/V2 and suitable for human review / edit planning.
Do not rename it to `lyrics_exact.srt` or render V3 as final until Strong Route lock completes.

Preferred final lock path:
- verified platform same-version timed lyric with retained provenance and/or
- trusted-lyrics Chinese forced alignment on the locked 37.120s master.

## Next Allowed Action

1. expose the corrected high-confidence timeline for review;
2. complete Strong Route raw evidence/provenance;
3. lock `AUDIO_TIMELINE_PACKAGE`;
4. only then create V3 Edit Map.

Do not reopen approved visual-generation stages unless the verified Edit Map proves a specific source-duration gap.
