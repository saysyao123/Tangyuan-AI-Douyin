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
- AUDIO_TIMELINE_TOOL: `04_HARNESS/tools/mv_audio_timeline/package_tool.py`
- ALIGNMENT_ADAPTER: `04_HARNESS/tools/mv_audio_timeline/run_alignment.py`
- AUDIO_PACKAGE: `06_TESTS/MV/WEB_R2/AUDIO_TIMELINE_PACKAGE/`
- ROOT_CAUSE_AUDIT: `06_TESTS/MV/WEB_R2/W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Valid locked upstream results

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, content timeline `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
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
- source content duration: `177.050 - 139.930 = 37.120s`;
- MP3 container duration from ffprobe: `37.146122s`;
- ~`0.026122s` difference is stored separately as container/encoder padding and must not redefine lyric timeline;
- therefore W02 source offset/content window remains confirmed correct.

Canonical audio identity:
`AUDIO_TIMELINE_PACKAGE/audio_identity.json`

### Critical lyric-sequence correction
The previously assumed excerpt order was wrong.
The locked 37.12s excerpt does not begin with a complete `如果你也刚好抬头看树` line.
The first full lyric is:
`我要学着树叶翩翩起舞`

The excerpt continues through:
`坐下来别那么严肃`

Canonical corrected lyrics:
`AUDIO_TIMELINE_PACKAGE/trusted_lyrics.txt`

High-confidence candidate:
`AUDIO_TIMELINE_PACKAGE/line_timeline.candidate.csv`

Legacy evidence/reference files retained:
- `trusted_lyrics_actual_excerpt_v1.txt`
- `line_timeline_high_confidence_v1.csv`
- `alignment_provenance_high_confidence_v1.md`

### Evidence method used for current candidate
1. exact source offset by audio fingerprint;
2. same-title/artist timed-LRC candidate establishes second-chorus order/coarse anchors;
3. lyric/release metadata cross-checks the recording sequence;
4. acoustic phrase-boundary analysis on locked excerpt refines coarse anchors.

This remains `DIAGNOSTIC_ONLY / HIGH_CONFIDENCE_PARTIAL`, not Strong Route truth.

## Reusable timing infrastructure now implemented

The timing system is no longer only prose.

Executable package gate:
`04_HARNESS/tools/mv_audio_timeline/package_tool.py`

Capabilities:
- initialize canonical audio identity + trusted lyrics;
- transform verified same-version LRC with exact clip offset;
- import external forced-alignment line timelines;
- preserve raw evidence + provenance;
- export SRT only from QA-passed line timeline;
- validate audio SHA/container duration/content duration separately;
- validate lyric sequence/repeated occurrences/time bounds/line QA;
- optional independent cross-source delta checks;
- write `package_manifest.json` only after machine PASS.

Alignment adapter:
`04_HARNESS/tools/mv_audio_timeline/run_alignment.py`

Supported adapter contracts:
- `xingyu-align` trusted-lyrics CTC alignment;
- `lyric-align` CJK/song-oriented known-lyrics alignment;
- unavailable engine/model returns `AUDIO_TIMELINE_PACKAGE_BLOCKED`; no silent downgrade.

Regression tests:
`04_HARNESS/tools/mv_audio_timeline/tests/test_package_tool.py`

Local validation result: `6/6 PASS`.
Covered failure classes:
- missing raw evidence;
- diagnostic candidate renamed exact;
- audio SHA mismatch;
- LRC offset + repeated occurrence mapping;
- excessive independent-source timing delta;
- valid strong-evidence package pass/manifest/SRT.

CI definition:
`.github/workflows/mv-audio-timeline-gate-tests.yml`

The current R2 candidate was intentionally tested against the new validator and remains BLOCKED (non-zero exit), because no strong-evidence final `line_timeline.csv` exists. This is expected and correct.

## Current Package state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_ACTUAL_EXCERPT_CORRECTED = YES`
- `HIGH_CONFIDENCE_LINE_TIMELINE_READY = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = PARTIAL`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = PARTIAL`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = HIGH_CONFIDENCE_PARTIAL`
- `LYRIC_TIMELINE_LOCKED = NO`
- `MUSIC_EVENT_MAP_VERIFIED = NO`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`
- `EDITOR_AUDIO_GATE_PASS = NO`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

## Editor hard entry condition

A future Agent may not self-report this Gate as PASS.
It must run the package validator against the exact current locked BGM and receive exit code `0`.
Only then may `package_manifest.json` be written with:
`AUDIO_TIMELINE_PACKAGE_LOCKED = true`.

Until then, V3 editing remains forbidden.

## Next Allowed Action

1. acquire Strong Route alignment raw evidence for the canonical 10-line lyrics;
2. import it into the canonical Package;
3. perform line-by-line Ground-truth QA and optional second-source cross-check;
4. run executable Package Validator until exit code `0`;
5. create anchor-word/music-event maps;
6. only then create V3 Edit Map.

Do not reopen approved visual-generation stages unless the verified Edit Map proves a specific source-duration gap.
