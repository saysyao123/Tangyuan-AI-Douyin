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
- MANIFEST: `04_HARNESS/MANIFEST.md` v3.5
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.2
- AUDIO_TIMELINE_RULE: `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- TIMING_CORE_TOOL: `04_HARNESS/tools/mv_audio_timeline/package_tool.py`
- COMPLETE_PACKAGE_GATE: `04_HARNESS/tools/mv_audio_timeline/final_gate.py`
- ALIGNMENT_ADAPTER: `04_HARNESS/tools/mv_audio_timeline/run_alignment.py`
- ALIGNMENT_BOOTSTRAP: `04_HARNESS/tools/mv_audio_timeline/bootstrap_alignment_env.py`
- ALIGNMENT_RUNTIME_LOCK: `04_HARNESS/tools/mv_audio_timeline/alignment_runtime.lock.json`
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
- ~`0.026122s` difference is recorded as container/encoder padding, not lyric-timeline shift.

Canonical audio identity:
`AUDIO_TIMELINE_PACKAGE/audio_identity.json`

### Corrected actual excerpt lyrics
The first full lyric is:
`我要学着树叶翩翩起舞`

The excerpt continues through:
`坐下来别那么严肃`

Canonical corrected lyrics:
`AUDIO_TIMELINE_PACKAGE/trusted_lyrics.txt`

Current high-confidence review candidate:
`AUDIO_TIMELINE_PACKAGE/line_timeline.candidate.csv`

It is deliberately marked:
`DIAGNOSTIC_ONLY / HIGH_CONFIDENCE_PARTIAL / NOT_LOCKABLE`.

## Timing evidence cross-check status

A public same-title/artist LRC matches the formal recording lyric order but uses coarse whole-second timestamps.
Against the current acoustic-refined candidate, approximate line-start differences have:
- median absolute delta ~`0.375s`;
- max delta ~`0.79s`.

This does not meet the automatic dual-source green thresholds:
- median <= `0.25s`;
- individual line <= `0.50s` unless reviewed/resolved.

Therefore public coarse LRC is retained only as supporting evidence, not Strong Route lock.

## Reusable timing infrastructure implemented

### 1. Timing Core Gate
`package_tool.py`

Verifies:
- strong evidence class;
- raw evidence + SHA;
- provenance;
- locked audio SHA;
- content duration vs MP3 container duration separately;
- lyric order/repeated occurrences;
- line-time monotonicity/bounds;
- every line QA PASS;
- optional independent-source timing delta.

It cannot promote `DIAGNOSTIC_ONLY` simply because a file is renamed `exact`.

### 2. Complete Package Gate｜Final lock authority
`final_gate.py`

Only this layer may create a final manifest with:
`AUDIO_TIMELINE_PACKAGE_LOCKED = true`.

It requires Core Gate PASS plus:
- `lyrics_exact.srt` exactly matches locked line timeline;
- `anchor_words.csv` anchors are inside their lyric windows and QA PASS;
- `music_events.csv` events are valid, sorted, in current content timeline and QA PASS;
- `alignment_qa_report.md` exists and its SHA is sealed into provenance;
- all mandatory editor-facing assets exist.

### 3. Alignment adapters
`run_alignment.py`

Supported engine contracts:
- primary `xingyu-align`: trusted Chinese lyrics -> CTC forced alignment;
- secondary `lyric-align`: CJK/song known-lyrics anchoring;
- missing engine/model => `AUDIO_TIMELINE_PACKAGE_BLOCKED`, no waveform fallback.

### 4. Reproducible environment lock
`alignment_runtime.lock.json`

Pinned current environment:
- Python 3.11 recommended;
- primary `xingyu-lyrics-aligner` v0.7.0 at exact Git commit;
- WhisperX 3.8.6;
- Chinese wav2vec2 align-model identity recorded;
- secondary `lyric-align` v0.3.0 at exact Git commit;
- secondary faster-whisper model identity recorded;
- timing thresholds locked.

`bootstrap_alignment_env.py` installs/checks this pinned environment explicitly. It never silently downgrades when model/network preparation fails.

### 5. Regression protection
Core regression suite:
`tests/test_package_tool.py`

Previously executed locally: `6/6 PASS`.

Complete-package regression suite:
`tests/test_final_gate.py`

Newly added cases:
- incomplete package -> FAIL;
- anchor outside lyric window -> FAIL;
- complete package -> PASS + final manifest.

CI:
`.github/workflows/mv-audio-timeline-gate-tests.yml`

CI now syntax-checks all timing tools and runs both suites. Current web/container environment cannot independently retrieve the workflow run status, so the new final-gate tests are `DEFINED / CI_RESULT_NOT_YET_CONFIRMED`; do not claim CI PASS until evidence is available.

## Current runtime limitation

This web/container runtime cannot currently download the large forced-alignment model weights because outbound model-host/DNS access is restricted.

Therefore:
- integration contract and pinned environment are implemented;
- current R2 strong forced-alignment result is **not** falsely claimed;
- final package remains blocked until Strong Route raw evidence is actually produced in a capable runtime or a verified higher-precision same-version timed lyric source is acquired.

## Current Package state

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_ACTUAL_EXCERPT_CORRECTED = YES`
- `HIGH_CONFIDENCE_LINE_TIMELINE_READY = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = PARTIAL`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = PARTIAL`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = HIGH_CONFIDENCE_PARTIAL`
- `LYRIC_TIMELINE_LOCKED = NO`
- `ANCHOR_WORD_MAP_LOCKED = NO`
- `MUSIC_EVENT_MAP_VERIFIED = NO`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`
- `EDITOR_AUDIO_GATE_PASS = NO`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

## Editor hard entry condition

Future Agent may not self-report this Gate as PASS.
It must run both machine gates against the exact current BGM:
1. Timing Core Gate -> exit `0`;
2. Complete Package Gate -> exit `0` + final manifest.

Only then may Editor start.

## Next Allowed Action

1. obtain Strong Route raw timing evidence for the canonical 10-line lyrics:
   - preferred: pinned trusted-lyrics forced alignment runtime; or
   - verified higher-precision same-version timed lyric source;
2. import/retain raw evidence + provenance;
3. line-by-line Ground-truth QA and optional second-source check;
4. generate exact SRT + anchor-word map + music-event map + QA report;
5. pass Timing Core Gate;
6. pass Complete Package Gate and generate final manifest;
7. only then create V3 Edit Map.

Do not reopen approved visual-generation stages unless the verified Edit Map proves a specific source-duration gap.
