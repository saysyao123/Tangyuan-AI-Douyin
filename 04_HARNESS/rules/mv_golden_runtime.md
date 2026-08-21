# Rules｜MV Golden Runtime Contract v1.1

> Status: `PRODUCTION_VALIDATED / ACTIVE`
> Purpose: make cross-round MV lessons executable at runtime without loading full historical rounds.
> Evidence base: Round 01 Golden Sample + WEB R2 repeated timing failures / technical rescues.

## 1. Golden inheritance rule｜HARD

At the start of every MV task / new MV Round, load in this order:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. current MV Round `CURRENT_STATE.md`
4. stage-specific rules / benchmark / templates JIT.

Round-specific Master Plans are summaries only. They may not override the authoritative Workflow or this Runtime Contract.

Historical R1 files remain audit/debug/regression references. New rounds must not rediscover correctness-critical lessons from history; those lessons must already be represented here or in the authoritative workflow/rule layer.

---

## 2. Audio truth before picture edit｜HARD

The exact BGM file/version/excerpt must be locked before downstream work.
Exact lyric text/order for that excerpt must also be locked.

A picture edit that depends on lyric/music timing is forbidden until a durable line-level lyric timing asset has been independently verified from the locked audio.

Forbidden as standalone timing truth:
- BPM grid;
- waveform valleys;
- onset/energy peaks;
- rough syllable-duration estimates;
- editor intuition;
- picture segment boundaries.

These may only support/cross-check a stronger timing source.

Preferred timing evidence:
1. actual ASR / forced alignment on the locked audio;
2. reliable same-version LRC / timed lyric source;
3. exact timestamps from an official same-version timed lyric/video source.

If no strong timing evidence exists:
`LYRIC_TIMELINE_BLOCKED`

Stop before picture edit. Do not silently downgrade the evidence standard.

---

## 3. Lyric timing evidence provenance｜HARD

A `.srt`, `.lrc`, CSV, JSON or MD table does **not** become exact merely because a durable file exists or its filename contains `exact` / `locked`.

Before `LYRIC_TIMELINE_LOCKED = YES`, save a provenance record with all applicable fields:
- locked audio identity + SHA/hash;
- evidence class: `ASR_FORCED_ALIGNMENT | SAME_VERSION_LRC | OFFICIAL_TIMED_LYRIC`;
- raw evidence asset path or stable source reference;
- tool/model/version, or source/platform identity;
- original timestamps before transformation;
- transformation rule, including exact clip-start subtraction when used;
- generated line-level timing asset path + SHA/hash;
- repeated identical lyric occurrences mapped separately;
- per-line start/end audit result;
- final `ALIGNMENT_GROUND_TRUTH_QA_PASS` status.

No raw evidence asset/reference = no provenance.
No provenance = no lyric timeline lock.

Acoustic diagnostic candidates must be explicitly labelled `DIAGNOSTIC_ONLY` and may never be copied/renamed into an `exact` timing asset without an independent strong source.

---

## 4. Two-layer subtitle QA｜HARD

Never collapse these two tests:

### A. Ground-truth Alignment QA
Question:
`Does the timing asset match the singer's actual vocal timing in the locked audio?`

This must be checked before picture edit/subtitle rendering can treat the timeline as truth.
Required state:
`ALIGNMENT_GROUND_TRUTH_QA_PASS`

### B. Subtitle Implementation QA
Question:
`Does the rendered video show the subtitle at the already-locked timestamps?`

Sampling before/inside/after an SRT window tests only implementation. It cannot validate the SRT itself.
Required state:
`SUBTITLE_IMPLEMENTATION_QA_PASS`

Implementation QA can only run meaningfully after Ground-truth Alignment QA has passed.

---

## 5. R1 Golden timing reproducibility｜HARD

Round close is incomplete for timing/subtitle correctness unless the accepted timing assets are preserved, not merely named in documentation.

For every accepted Golden MV preserve:
- final locked audio identity/hash;
- exact accepted SRT/LRC/timing table;
- provenance record/raw timing source where legally/technically retainable;
- transformation/offset method;
- user acceptance state.

`documented success != reproducible success`

A future Round must be able to audit how the accepted subtitle times were obtained.

---

## 6. Subtitle Golden baseline｜HARD

Base lyric subtitle system inherited from R1:
- Chinese lyrics;
- light text;
- dark semi-transparent rounded background tightly fitting the actual lyric;
- text visually centered horizontally and vertically inside the box;
- consistent inner padding;
- fixed comfortable lower safe-area placement;
- restrained fade;
- max 2 lines;
- no default karaoke / word-by-word effect.

Before full subtitle render, inspect at minimum:
- first lyric;
- middle lyric;
- longest lyric;
- final lyric.

A new subtitle aesthetic may replace this only through an explicit aesthetic decision, not accidental drift.

---

## 7. First-frame / dynamic inheritance

Stable inherited rules:
- first frame = `0-second dynamic anchor`, not a poster;
- conceptual visual units and production segments are separate decisions;
- character-containing image-to-video prompts obey the exact portrait-safety prefix in `rules/ai_video.md`;
- first-frame character closure remains mandatory;
- shot count is selected by lyric/director task, not a fixed quota;
- single-shot, 2–3-shot and denser structures are all valid when they earn their use;
- camera / shot repetition must be reviewed across the whole set;
- dynamic retries are root-cause driven rather than whole-set resets.

---

## 8. Generated-source QA inheritance

Raw AI video QA is not binary whole-clip pass/fail.
Allowed statuses:
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

Good internal shots may enter the material pool even if other frames need trimming.
Regenerate only when the usable clean window is insufficient for the final edit.

All AI source audio is non-authoritative:
- final MV timing/music truth is the locked BGM;
- strip AI source audio at ingest unless a Director explicitly locks a motivated ambience workflow;
- unintended AI BGM does not invalidate otherwise good visuals, but is marked `SOURCE_AUDIO_POLICY_FAIL`.

---

## 9. Edit inheritance

Do not mechanically equal-trim source clips.
Priority:
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

Preserve useful internal motion arcs first, then solve total duration with selective trim / overlap / transition / earlier-later exits tied to verified musical events.

Every retained picture fragment must have a traceable reason tied to at least one of:
- lyric line / semantic beat;
- verified musical event;
- motion arc;
- visual contrast / release.

---

## 10. No-skip correctness promotion rule｜HARD

A correctness failure that the user had to identify and that should have been caught automatically may not be preserved only as a retrospective lesson.

Promotion path:
`failure evidence -> root cause -> stable rule -> required artifact/state -> independent self-audit gate`.

Examples:
- wrong lyric timing -> provenance + `ALIGNMENT_GROUND_TRUTH_QA_PASS` + `LYRIC_TIMELINE_LOCKED`;
- subtitle visual drift -> `SUBTITLE_STYLE_QA_PASS`;
- subtitle rendering not following locked SRT -> `SUBTITLE_IMPLEMENTATION_QA_PASS`;
- source-audio leakage -> source-audio strip + `FINAL_TECH_QA_PASS`;
- non-square pixel aspect -> technical validation before delivery.

If a rule can be satisfied only by renaming an artifact or self-referencing its own output, the Gate is insufficient and must be strengthened.

---

## 11. Minimum runtime state chain

The authoritative detailed sequence lives in `workflows/mv.md`.
At minimum, timing/edit delivery may not occur unless these states exist in order:

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
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

A later state is invalid when an upstream required state is missing.

---

## 12. What this contract does NOT freeze

Not inherited as universal creative rules:
- R1 song choice;
- R1 paper/ink world;
- R1 exact shot list;
- fixed number of first frames / videos;
- fixed 3-shot grammar;
- fixed camera movement recipes;
- complex lyric animation;
- any one creator/reference style.

Golden inheritance protects correctness and minimum production quality, not creative repetition.
