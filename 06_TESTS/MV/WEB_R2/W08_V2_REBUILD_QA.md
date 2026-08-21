# WEB R2｜W08 v2 Rebuild QA — REVOKED

> Status: `REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`
> Date: `2026-08-21`
> Historical output: `如果你也刚好抬头看树_MV_WEB_R2_第二版成片.mp4`
> Historical SHA-256: `ff1bbb67427b0067001ebe97f5e0d7bcb3e4c9c434606c2c833ba280647adc3b`
> Root-cause audit: `W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`

## 1. Why the previous INTERNAL_QA_PASS is invalid

The v2 SRT/CSV used these line starts:
`0.470 / 5.451 / 10.954 / 13.827 / 16.788 / 19.702 / 23.470 / 28.439 / 32.618`.

Those values are effectively the same acoustic candidate family that `W08_AUDIO_LYRIC_TIMELINE_GATE_v2.md` had already labelled `DIAGNOSTIC_ONLY / NOT timing truth`.

No independent raw ASR/forced-alignment result, reliable same-version LRC, or official timed-lyric source was saved before the v2 timeline was promoted to an `exact` SRT.

Therefore the timeline was never legitimately locked.

`LYRIC_TIMELINE_LOCKED = NO`

---

## 2. QA category error

The earlier v2 QA sampled frames before/inside/after each SRT interval and verified that the rendered subtitle followed the SRT.

That verifies only:
`SUBTITLE IMPLEMENTATION -> follows SRT`

It does not verify:
`SRT -> follows actual sung vocal timing`

The missing Gate was independent Ground-truth Alignment QA.

Correct separation:
- `ALIGNMENT_GROUND_TRUTH_QA_PASS`: timing asset vs actual vocal timing, supported by independent timing evidence;
- `SUBTITLE_IMPLEMENTATION_QA_PASS`: rendered subtitle vs already-locked timing asset.

The first must pass before the second can count as correctness evidence.

---

## 3. Packaging/audio shift ruled out

The final v2 AAC audio was compared with the locked BGM after common resampling.

- best global lag: `0.000s`
- correlation: approximately `0.999`
- final AAC stream begins at `0.000000`

So the mismatch is not an FFmpeg/AAC global shift.

---

## 4. What remains valid from v2

The following engineering work may be reused later after a real lyric timeline is obtained:
- visual source selections;
- S1 duplicate-window exclusion;
- S7 topology-risk exclusion;
- S8/S9 visual-role distinction;
- R1 Golden subtitle visual style;
- source-audio stripping;
- aspect-ratio/SAR validation.

The following may NOT be reused as timing truth:
- `lyrics_exact_v2.srt`;
- `lyrics_timeline_v2.csv`;
- any picture cut whose timing rationale depends on those line windows.

---

## 5. Current Gate

`W08A / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`

A v3 render is forbidden until all exist:
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS`
- `LYRIC_TIMELINE_LOCKED`
- `BEAT_MAP_VERIFIED`

Do not repair v2 by manually nudging its SRT.
