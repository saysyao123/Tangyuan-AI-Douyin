# Rules｜MV Golden Runtime Contract v1.3

> Status: `PRODUCTION_VALIDATED / ACTIVE`
> Purpose: inherit cross-round correctness without loading full historical rounds.
> Evidence base: R1 Golden Sample + WEB R2 repeated lyric-timing failures + WEB R2 V3/V3.1 editing calibration.

## 1. Golden inheritance｜HARD

At every MV start load:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current MV Round `CURRENT_STATE.md`
5. stage-specific rules JIT.

Editing detail is intentionally not duplicated here. Load `rules/mv_editing.md` JIT for Stage 4/6/7/8/9.
Round Master Plans are summaries only and cannot override these runtime sources.

---

## 2. Audio Timeline Package is the first post-BGM hard node｜HARD

After `BGM_LOCKED`, every MV must build and lock:
`AUDIO_TIMELINE_PACKAGE`.

This position is deliberate:
- before BGM lock, clip/version may still change and alignment work may be wasted;
- immediately after BGM lock, exact audio identity is stable enough for alignment;
- any later placement allows Natural Beat, Director allocation, dynamic production or subtitles to inherit guessed lyric positions.

No timing-dependent Director allocation, Picture Edit or Subtitle Render may proceed before:
`AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.

Detailed contract:
`rules/mv_audio_timeline.md`.

---

## 3. R1 / R2 timing lesson｜HARD

R1 successful path:
`same-version LRC -> subtract exact clip start -> corrected clip timeline -> playback review`.

WEB R2 proved the stronger engineering requirement:
- timing truth requires raw evidence + provenance + ground-truth QA;
- an `exact.srt` filename or waveform candidate is not sufficient;
- visual segments cannot define lyric timing;
- repeated occurrences must remain distinct;
- the Package must exist before time-dependent production.

---

## 4. Evidence provenance｜HARD

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

For human timing-review previews, subtitle fade may be temporarily disabled so fade latency is not mistaken for timing error. After timing perception is accepted, style/fade can be optimized without changing timestamps.

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
- retry by root cause;
- dynamic source is an **editing material pool**, not a pre-cut final timeline.

WEB R2 promoted source-portfolio lesson:
- 1-shot / one-take for hold, space, emotion, release;
- 2-shot as common setup/event or detail/emotion structure;
- 3-shot for task-specific discovery or peak;
- >3-shot only when a real hook/peak earns the density.

For ~5s generation, default preference is 1–2 shots, not dense multi-shot everywhere.

Raw dynamic QA statuses:
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

W07 must preserve an executable `VISUAL_SOURCE_MAP` with clean/risk windows and edit roles.

AI source audio is non-authoritative and stripped before final edit unless a deliberately motivated ambience workflow is separately locked.

---

## 8. Edit inheritance

Detailed execution: `rules/mv_editing.md`.

Priority:
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

Promoted WEB R2 lessons:
- **Anchor Word != mandatory picture cut**;
- lyrical/emotional MV defaults to long-cut-first;
- preserve useful internal source arcs;
- avoid repeated external micro-cuts and short A-B-A recycling;
- dense internal multi-shot source + dense external edit compounds fragmentation;
- use mixed 1–3-shot source portfolio instead;
- final release deserves breathing room;
- user should not have to discover watermark leakage or frame-aspect errors.

WEB current limitation fallback:
if precise watermark cleanup is unavailable, use a consistent whole-source zoom/crop derived from worst-case batch marks, preserve 9:16/SAR1:1, and validate top-left/bottom-right risk frames before handoff.
This is a WEB preview fallback, not the preferred publish-grade path.

---

## 9. No-skip correctness promotion｜HARD

A correctness or repeated quality failure caught by the user must be promoted as:
`failure evidence -> root cause -> stable rule -> required artifact/state -> independent Gate/check`.

Examples now promoted:
- lyric timing failure -> Audio Timeline Package Gate;
- fragmented “every anchor = cut” edit -> Fragmentation Gate;
- prose-only dynamic QA -> executable VISUAL_SOURCE_MAP;
- recurring WEB watermark leak -> uniform watermark-safe preview transform + risk-frame QA.

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
- R1/R2 song;
- exact visual world;
- exact shots;
- fixed first-frame/video count;
- fixed 3-shot grammar;
- fixed camera recipe;
- fixed external fragment count for all genres;
- complex lyric animation.

Golden inheritance protects correctness and validated production discipline, not creative repetition.
