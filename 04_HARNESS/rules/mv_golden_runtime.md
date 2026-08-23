# Rules｜MV Golden Runtime Contract v1.2

> Status: `PRODUCTION_VALIDATED / ACTIVE`
> Purpose: inherit cross-round correctness without loading full historical rounds.
> Evidence base: R1 Golden Sample + WEB R2 repeated lyric-timing failures.

## 1. Golden inheritance｜HARD

At every MV start load:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current MV Round `CURRENT_STATE.md`
5. stage-specific rules JIT.

Round Master Plans are summaries only and cannot override these runtime sources.

---

## 2. Audio Timeline Package is the first post-BGM hard node｜HARD

R1 proved the correct principle but did not preserve the full reproducible asset chain.
WEB R2 proved that a rule sentence or an `exact.srt` filename is not enough.

Therefore after `BGM_LOCKED`, every MV must build and lock:
`AUDIO_TIMELINE_PACKAGE`.

No timing-dependent Director allocation, Picture Edit or Subtitle Render may proceed before:
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.

Detailed contract:
`rules/mv_audio_timeline.md`.

---

## 3. R1 timing lesson｜HARD

R1 final successful correction:
`same-version LRC -> subtract exact clip start 01:23.800 -> corrected clip timeline -> user playback review`.

Stable lesson:
- subtitle/lyric time comes from locked audio alignment, never visual segment boundaries;
- exact clip offset matters;
- repeated lyric occurrences must remain distinct.

Reproducibility gap from R1:
- raw LRC/source ID was not preserved;
- accepted `lyrics_exact_v3_1.srt` was named in docs but not reliably packaged as a canonical runtime asset.

Future Golden close is incomplete without the full Audio Timeline Package.

---

## 4. Evidence provenance｜HARD

A timing file becomes authoritative only with independent provenance.

Allowed primary evidence classes:
- `SAME_VERSION_LRC`
- `ASR_FORCED_ALIGNMENT`
- `OFFICIAL_TIMED_LYRIC`

Required provenance:
- locked audio identity + hash;
- raw evidence path/reference;
- source/platform/tool/model/version;
- original timestamps;
- transformation rule;
- final timing asset/hash;
- repeated-line mapping;
- warnings/unmatched;
- per-line ground-truth QA.

No raw evidence/provenance = no lock.

Waveform/BPM/onset candidates are `DIAGNOSTIC_ONLY`.
They may support strong evidence but never replace it.

---

## 5. Two-layer subtitle QA｜HARD

### Ground-truth Alignment QA
Question:
`Does the timing asset match the singer in the locked audio?`

This belongs to the Audio Timeline Package.
Required:
`ALIGNMENT_GROUND_TRUTH_QA_PASS`.

### Subtitle Implementation QA
Question:
`Does the rendered subtitle follow the already-locked timing asset?`

Required:
`SUBTITLE_IMPLEMENTATION_QA_PASS`.

Implementation QA cannot validate Ground Truth.

---

## 6. Subtitle Golden baseline｜HARD

R1 accepted base style:
- Chinese lyric;
- light text;
- dark semi-transparent rounded box tightly fitted to text;
- text centered horizontally/vertically;
- consistent padding;
- comfortable fixed lower safe area;
- restrained fade;
- max 2 lines;
- no default karaoke/word-by-word effect.

A new style requires an explicit aesthetic decision, not accidental drift.

---

## 7. First-frame / dynamic inheritance

Stable:
- first frame = `0-second dynamic anchor`;
- conceptual units and production segments are separate;
- first-frame character closure;
- exact AI-fictional-character safety prefix from `rules/ai_video.md`;
- shot count selected by lyric/director task, not fixed quota;
- whole-set camera repetition review;
- retry by root cause.

Raw dynamic QA statuses:
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

AI source audio is non-authoritative and stripped before final edit unless a deliberately motivated ambience workflow is separately locked.

---

## 8. Edit inheritance

Priority:
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

Do not mechanically equal-trim 5s clips.
Preserve useful internal motion arcs, then use selective trim / overlap / transition / earlier-later exit tied to verified music events.

Every retained fragment should trace to at least one:
- lyric/semantic Beat;
- Anchor Word;
- verified musical event;
- motion arc;
- contrast/release.

---

## 9. No-skip correctness promotion｜HARD

A correctness failure caught by the user must be promoted as:
`failure evidence -> root cause -> stable rule -> required artifact/state -> independent Gate`.

A Gate that can be passed merely by renaming a file or testing an output against itself is invalid.

---

## 10. Minimum runtime state chain

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `AUDIO_IDENTITY_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
→ `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`
→ `ALIGNMENT_GROUND_TRUTH_QA_PASS`
→ `LYRIC_TIMELINE_LOCKED`
→ `MUSIC_EVENT_MAP_VERIFIED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `EDITOR_AUDIO_GATE_PASS`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

Any later state is invalid if an earlier required state is absent.

---

## 11. Package invalidation｜HARD

Automatically invalidate timing/edit/subtitle dependency if any changes:
- BGM hash/version;
- clip start/end;
- lead-in/padding;
- speed/time-stretch;
- trusted lyric text/order;
- repeated occurrence mapping.

Then return to Audio Timeline Package rebuild/revalidation.

---

## 12. What Golden does NOT freeze

Do not inherit as universal creative rules:
- R1 song;
- R1 visual world;
- R1 exact shots;
- fixed first-frame/video count;
- fixed 3-shot grammar;
- fixed camera recipe;
- complex lyric animation.

Golden inheritance protects correctness and minimum production quality, not creative repetition.
