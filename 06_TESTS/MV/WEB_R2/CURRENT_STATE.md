# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读权威 Workflow + Golden Runtime，再读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W08A`
- STAGE_NAME: `Lyric alignment evidence acquisition / provenance verification`
- STATE: `V2_REVOKED / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`
- BRANCH: `test/mv-web-r2`
- WORKFLOW: `04_HARNESS/workflows/mv.md` v1.2+
- GOLDEN_RUNTIME: `04_HARNESS/rules/mv_golden_runtime.md` v1.1
- ROOT_CAUSE_AUDIT: `06_TESTS/MV/WEB_R2/W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Valid locked upstream results

- W01: `HUMAN_GATE / PASSED` — `如果你也刚好抬头看树` / 孙天宇
- W02: `BGM_LOCKED` — source `139.930s–177.050s`, rendered content `37.120s`, SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- W03: `LYRIC_TEXT_LOCKED + DIRECTOR_BEAT_MAP` — exact nine-line lyric text; no word-level ASR claim
- W04: `DIRECTOR_PLAN_LOCKED` — `树影之外`
- W05: `FIRST_FRAME_SET_LOCKED` — 9/9 accepted
- W06: dynamic prompt/camera experiment completed
- W06-X: S1–S9 external Seedance clips returned
- W07: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` — visual batch pass with trim

## Revoked edit artifacts

### V1
`如果你也刚好抬头看树_MV_WEB_R2_第一版成片.mp4`

Status: `REVOKED / TECHNICAL_RESCUE`.
Reason: picture edit/subtitles proceeded before valid lyric timing; subtitle style drifted.

### V2
`如果你也刚好抬头看树_MV_WEB_R2_第二版成片.mp4`

Status: `REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`.

The v2 timing asset reused the same acoustic-candidate family previously labelled `NOT timing truth`, without new independent ASR/LRC/official timed-lyric evidence.

The previous internal QA was circular: it verified the render obeyed the SRT, not that the SRT matched the actual vocal timing.

Packaging/mux has been ruled out:
- final audio vs locked BGM global lag: `0.000s`;
- waveform correlation: ~`0.999`.

Therefore the timing asset itself is the failure.

## Current lyric timing truth

- `BGM_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- acoustic diagnostics available = YES, but `DIAGNOSTIC_ONLY`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = NO`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = NO`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = NO`
- `LYRIC_TIMELINE_LOCKED = NO`
- `BEAT_MAP_VERIFIED_FOR_EDIT = NO`
- `EDIT_MAP_LOCKED = NO`
- `DELIVERABLE_RENDERED = NO`

The old v2 `lyrics_exact_v2.srt` / `lyrics_timeline_v2.csv` are failure evidence only and must never be used as timing truth.

## Evidence requirement before any v3

Acquire one strong independent timing source:
1. actual ASR / forced alignment on the locked 37.120s audio; or
2. reliable same-version LRC / timed lyric source; or
3. official same-version timestamped lyric/video evidence.

Then save provenance:
- source/raw evidence;
- tool/model/version or source identity;
- original timestamps;
- exact cut-offset transformation where relevant;
- transformed timing asset/hash;
- repeated title occurrence mapping;
- per-line boundary audit.

Only after `ALIGNMENT_GROUND_TRUTH_QA_PASS` may `LYRIC_TIMELINE_LOCKED` be set.

## Next Allowed Action

Continue W08A only: acquire and verify real lyric-timing evidence.

Do NOT render a third cut by manually shifting v2 timestamps.
Do NOT reopen accepted visual-generation stages unless the later verified edit proves a specific visual-source gap.
