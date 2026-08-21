# WEB R2｜W08 Audio / Lyric Timeline Gate v3

> Status: `BLOCKING_GATE / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`
> Trigger: W08 v1 + v2 technical rescues.
> Purpose: prevent picture edit/subtitle render until lyric timing has an independently verifiable evidence chain.

## 1. Locked audio/text

Song: `如果你也刚好抬头看树` — 孙天宇

Locked excerpt:
- source interval: `139.930s–177.050s`
- rendered content: `37.120s`
- fade in: `0.020s`
- fade out: `0.950s`
- SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`

Exact lyric text/order is locked as nine lines.

`BGM_LOCKED = YES`
`LYRIC_TEXT_LOCKED = YES`

---

## 2. Why v2 is also invalid

V2 created `lyrics_exact_v2.srt` / `lyrics_timeline_v2.csv`, but its timestamps were effectively the same acoustic candidate family already labelled diagnostic-only in the previous Gate.

No raw ASR/forced-alignment output, same-version LRC, or official timed-lyric evidence was saved.

Therefore v2 committed an `EVIDENCE_PROVENANCE_FAIL`:
`durable file exists != timing truth exists`.

V2 QA also tested only that the render followed the SRT; it did not independently test the SRT against the actual sung vocals.

Root-cause audit:
`W08_V2_TIMING_PROVENANCE_FAILURE_AUDIT.md`

---

## 3. Diagnostic acoustic candidates remain NOT truth

The previous waveform/onset/energy candidates remain useful only as cross-check evidence:
- L1 ~`0.49s`
- L2 ~`5.14–5.46s`
- L3 ~`10.97s`
- L4 ~`13.27–13.85s`
- L5 ~`16.3–16.8s`
- L6 ~`19.4–19.7s`
- L7 ~`23.2–23.8s`
- L8 ~`28.45s`
- L9 ~`32.6–33.1s`

They cannot by themselves produce `LYRIC_TIMELINE_LOCKED`.

The revoked v2 SRT must not be used as a new source just because it is durable.

---

## 4. Strong timing evidence hierarchy

At least one independent strong source is required:
1. actual ASR / forced alignment run on the locked 37.120s audio;
2. reliable same-version LRC / timed lyric source;
3. exact official same-version timestamped lyric/video evidence.

Then constrain/correct against the exact nine-line lyric text and cross-check with acoustic diagnostics.

No strong source:
`LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`

Stop. Do not render.

---

## 5. Mandatory provenance artifact

Before any line timing asset can be marked locked, save a provenance record containing:
- locked audio path/identity/hash;
- evidence class;
- raw evidence path/reference;
- tool/model/version or source/platform;
- original timestamps;
- transformation rule / clip-start offset;
- transformed timing asset path/hash;
- repeated-title mapping;
- per-line boundary audit;
- Ground-truth Alignment QA result.

Required state:
`LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
→ `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`

A filename such as `exact.srt` is not evidence.

---

## 6. Independent Ground-truth Alignment QA

This QA asks:
`Does the timing asset match the singer's actual vocal timing in the locked audio?`

For every line:
- verify actual vocal start;
- verify actual vocal end;
- inspect/listen around boundaries against the independent timing source;
- cross-check with waveform/onset/valley evidence;
- ensure L1 and L8 are distinct occurrences;
- ensure L9 resolves before the fade tail.

Required state:
`ALIGNMENT_GROUND_TRUTH_QA_PASS`

Only after this:
`LYRIC_TIMELINE_LOCKED = YES`

---

## 7. Implementation QA is separate

After the timing asset is locked and subtitles are rendered, separately test:
`Does the video display the subtitle according to the locked timing asset?`

Required state:
`SUBTITLE_IMPLEMENTATION_QA_PASS`

Sampling before/inside/after an SRT window can establish implementation correctness only. It can never validate the SRT itself.

---

## 8. Packaging shift check from v2

The v2 final AAC audio was compared against the locked BGM:
- best global lag `0.000s`;
- waveform correlation ~`0.999`.

Therefore no global FFmpeg/AAC shift explains the subtitle mismatch.

---

## 9. Hard runtime chain

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

Later states are invalid if an upstream state is missing.

---

## 10. Current truthful state

- `BGM_LOCKED = YES`
- `LYRIC_TEXT_LOCKED = YES`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = NO`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = NO`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS = NO`
- `LYRIC_TIMELINE_LOCKED = NO`
- `BEAT_MAP_VERIFIED_FOR_EDIT = NO`
- `EDIT_MAP_LOCKED = NO`
- V1 = `REVOKED`
- V2 = `REVOKED`

Current state:
`W08A / LYRIC_ALIGNMENT_EVIDENCE_BLOCKED`

Do not manually shift the v2 SRT and do not produce v3 until real timing evidence is acquired.
