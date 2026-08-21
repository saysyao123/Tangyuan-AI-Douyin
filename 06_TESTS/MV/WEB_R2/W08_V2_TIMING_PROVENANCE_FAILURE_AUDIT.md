# WEB R2｜W08 v2 Lyric Timing Provenance Failure Audit

> Status: `TECHNICAL_RESCUE / V2_REVOKED`
> Date: `2026-08-21`
> Purpose: explain why v2 still had wrong lyric/subtitle sync after the first W08 process repair.

## Executive conclusion

V2 did **not** fail because FFmpeg/AAC shifted the BGM. It failed because `LYRIC_TIMELINE_LOCKED` was falsely treated as satisfied without an independent timing source.

The process failure has four layers:

1. diagnostic acoustic candidates were repackaged as an `exact` SRT/CSV;
2. the QA verified subtitle implementation against that SRT, not the SRT against the actual vocal performance;
3. the R1 user-approved timing asset/mechanism was documented but the actual accepted SRT/LRC asset was not preserved in the repository;
4. multiple process descriptions drifted: the newer authoritative workflow requires pre-edit lyric alignment, while the older WEB R2 Master Plan still described edit-first/subtitle-later sequencing.

V2 must therefore remain a failure artifact. Do not hand-adjust its SRT and call it fixed.

---

## 1. False lock: v2 reused the forbidden acoustic candidates

V2 durable files:
- `lyrics_timeline_v2.csv`
- `lyrics_exact_v2.srt`

V2 start points:
- L1 `0.470`
- L2 `5.451`
- L3 `10.954`
- L4 `13.827`
- L5 `16.788`
- L6 `19.702`
- L7 `23.470`
- L8 `28.439`
- L9 `32.618`

But `W08_AUDIO_LYRIC_TIMELINE_GATE_v2.md` had already classified the following as **diagnostic only / NOT timing truth**:
- L1 ~`0.49`
- L2 ~`5.14–5.46`
- L3 ~`10.97`
- L4 ~`13.27–13.85`
- L5 ~`16.3–16.8`
- L6 ~`19.4–19.7`
- L7 ~`23.2–23.8`
- L8 ~`28.45`
- L9 ~`32.6–33.1`

The v2 timestamps are effectively the same candidate family. No ASR transcript, forced-alignment output, same-version LRC, or official timed lyric source was introduced between the blocked candidate state and the v2 `exact` asset.

Therefore:
`LYRIC_TIMELINE_LOCKED = FALSE`

Naming a file `exact` does not change its evidence class.

---

## 2. Circular QA: implementation was tested, ground truth was not

V2 QA sampled frames:
- before SRT start;
- inside SRT window;
- before SRT end;
- after SRT end.

That test proves only:
`rendered subtitle visibility == SRT instructions`

It does **not** prove:
`SRT timing == actual sung lyric timing`

The process incorrectly collapsed two different QA layers:

### A. Ground-truth Alignment QA
Question:
`Does the timing asset match the singer's actual vocal phrase/word boundaries in the locked audio?`

Required evidence must be independent of the render:
- ASR / forced alignment raw output;
- reliable same-version timed lyrics;
- official same-version timestamped lyric evidence;
- boundary listening/inspection against those source timestamps.

### B. Subtitle Implementation QA
Question:
`Does the video display the subtitle at the already-locked timestamps?`

This happens only **after** A passes.

V2 performed B and mislabeled it as evidence for A.

---

## 3. Packaging / AAC shift ruled out

The v2 final MP4 audio was extracted and compared with the locked 37.120s BGM using waveform cross-correlation after common resampling.

Result:
- best global lag: `0.000s`
- correlation: approximately `0.999`
- final MP4 AAC stream start time: `0.000000`
- final MP4 audio duration: `37.120000`

Therefore the subtitle mismatch is not caused by an FFmpeg/AAC mux delay or a global soundtrack shift.

Root cause remains the lyric timing asset itself.

---

## 4. R1 reproducibility gap

R1 retrospective records the same original failure:
- visual-segment-derived lyric timing was wrong;
- the successful correction used a **same-version LRC**, converted relative to the exact R1 cut start `01:23.800`;
- the corrected subtitle timing was user-reviewed as accurate.

R1 Golden documents name the accepted asset:
`lyrics_exact_v3_1.srt`

However that actual timing asset is not available at the expected path in the current repository branch. The successful method is described, but the accepted executable artifact was not versioned alongside the Golden Sample.

This is a reproducibility failure:
`documented success != reproducible success`

Future Golden close must preserve both:
- the rule/method;
- the exact accepted timing asset + provenance.

---

## 5. Duplicate process-truth drift

Current authoritative workflow:
`04_HARNESS/workflows/mv.md v1.2`

It requires:
`LYRIC_TIMELINE_LOCKED -> BEAT_MAP_VERIFIED -> EDIT_MAP_LOCKED`

before picture edit.

But WEB R2 still had:
`WEB_R2_MASTER_PLAN.md v1.0`

whose W08 text begins by building the edit timeline and only later creating subtitles/alignment.

`WEB_START_PROMPT.md` also instructed a new chat to read the old Master Plan before the authoritative workflow/runtime rules.

This creates competing process models inside the same context.

Fix:
- `workflows/mv.md` + `rules/mv_golden_runtime.md` are operational truth;
- round Master Plans are summaries and cannot override runtime rules;
- startup order must load authoritative workflow/runtime before round summary.

---

## 6. Evidence provenance is now mandatory

A line-timing file may be promoted to `LYRIC_TIMELINE_LOCKED` only if an accompanying provenance asset exists.

Required record fields:
- locked audio file identity + SHA;
- evidence class: `ASR_FORCED_ALIGNMENT | SAME_VERSION_LRC | OFFICIAL_TIMED_LYRIC`;
- raw evidence asset path / stable source reference;
- tool/model/version or source/platform;
- original timestamps before transformation;
- transformation rule (for example source-song timestamp minus exact clip start);
- resulting line-level timing asset path + SHA;
- repeated-line mapping;
- per-line boundary audit result;
- `ALIGNMENT_GROUND_TRUTH_QA_PASS`.

Waveform/BPM/onset candidates may be stored as supporting diagnostics but can never be the provenance source.

---

## 7. Correct QA chain

Future lyric/subtitle runtime must use:

`BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
→ `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`
→ `ALIGNMENT_GROUND_TRUTH_QA_PASS`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A downstream state is invalid if an upstream state is missing.

---

## 8. Current truthful state

- V1: `REVOKED / TECHNICAL_RESCUE`
- V2: `REVOKED / TECHNICAL_RESCUE / EVIDENCE_PROVENANCE_FAIL`
- locked BGM: `YES`
- exact lyric text: `YES`
- strong independent lyric-timing evidence: `NO`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = NO`
- `LYRIC_TIMELINE_LOCKED = NO`
- picture-edit v3 allowed: `NO`

Current correct state:
`W08A / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`

Do not produce a v3 by manually shifting the v2 SRT. Acquire a real timing source first.
