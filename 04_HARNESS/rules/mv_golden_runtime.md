# Rules｜MV Golden Runtime Contract v1.0

> Status: `PRODUCTION_VALIDATED / ACTIVE`
> Purpose: make cross-round MV lessons executable at runtime without loading full historical rounds.
> Evidence base: Round 01 Golden Sample + WEB R2 repeated timing failure / technical rescue.

## 1. Why this file exists

Historical retrospectives are intentionally JIT-only. Therefore every correctness-critical lesson that must survive into a new MV Round needs a small always-loaded runtime contract.

This file does **not** copy R1 creative content, characters, paper/ink imagery, songs or shot lists.
It inherits only cross-round production invariants.

A new MV Round may change aesthetics freely, but may not silently fall below this runtime contract.

---

## 2. Golden inheritance rule｜HARD

At the start of every MV task / new MV Round, load:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. current MV Round `CURRENT_STATE.md`
4. stage-specific rules / benchmark / templates JIT.

Do not require the agent to rediscover R1 lessons from `ROUND_01/*` during normal execution.
Historical R1 files are for audit / debugging / regression only.

---

## 3. Audio truth before picture edit｜HARD

R1 and WEB R2 both demonstrated the same failure mode:
`visual segmentation / waveform guessing -> wrong lyric timing -> wrong subtitle sync -> wrong perceived picture/lyric hit`.

Therefore:

- the exact BGM file/version/excerpt must be locked;
- exact lyric text/order for that excerpt must be locked;
- a durable line-level lyric timing asset must be independently verified from the locked audio before picture edit is allowed;
- BPM grid, waveform valleys, rough syllable-duration estimates, editor intuition and picture segment boundaries cannot by themselves create a locked lyric timeline;
- repeated identical lyric lines must be mapped to distinct audio occurrences;
- edit cuts may occur inside a lyric, but subtitle timing never follows picture boundaries.

Preferred timing evidence:
1. actual ASR / forced alignment on the locked audio;
2. reliable same-version LRC / timed lyrics;
3. official same-version timed lyric/video evidence.

Then constrain/correct against exact known lyrics and boundary-check against the locked audio.

If no strong timing evidence exists:
`LYRIC_TIMELINE_BLOCKED`

Stop before picture edit. Do not downgrade silently.

---

## 4. Subtitle Golden baseline｜HARD

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

## 5. First-frame / dynamic inheritance

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

## 6. Generated-source QA inheritance

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

## 7. Edit inheritance

Do not mechanically equal-trim source clips.
Priority:
`lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

Preserve useful internal motion arcs first, then solve total duration with:
- selective trim;
- overlap;
- transition;
- earlier/later exits tied to verified musical events.

Every retained picture fragment must have a traceable reason tied to at least one of:
- lyric line / semantic beat;
- verified musical event;
- motion arc;
- visual contrast / release.

---

## 8. No-skip correctness promotion rule｜HARD

A correctness failure that the user had to identify and that should have been caught automatically may not be preserved only as a retrospective lesson.

Promotion path for correctness failures:
`failure evidence -> root cause -> stable rule -> required runtime artifact/state -> self-audit gate`.

Examples:
- wrong lyric timing -> `LYRIC_TIMELINE_LOCKED` required before edit;
- subtitle visual drift -> `SUBTITLE_STYLE_QA_PASS` required before final render;
- source-audio leakage -> source-audio strip + `FINAL_TECH_QA_PASS`;
- non-square pixel aspect -> technical validation before delivery.

If the lesson cannot be verified by an artifact/state/test, it is not fully runtime-promoted.

---

## 9. Minimum runtime state chain

The authoritative detailed sequence lives in `workflows/mv.md`.
At minimum, delivery may not occur unless these states exist in order:

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A later state is invalid when an upstream required state is missing.

---

## 10. What this contract does NOT freeze

Not inherited as universal creative rules:
- R1 song choice;
- R1 paper/ink world;
- R1 exact shot list;
- fixed number of first frames / videos;
- fixed 3-shot grammar;
- fixed camera movement recipes;
- complex lyric animation;
- any one creator/reference style.

Golden inheritance protects **correctness and minimum production quality**, not creative repetition.
