# Workflow｜AI MV Production v1.4

> Source: Round 01 Golden Sample + WEB R2 camera calibration + WEB R2 timing rescue + WEB R2 V3/V3.1 editing calibration.
> Role: authoritative MV execution workflow.
> Core discipline: **no downstream stage may execute unless every required upstream Gate has a durable PASS artifact.**
> Editing detail is intentionally modularized into `rules/mv_editing.md` and loaded JIT rather than expanding this workflow indefinitely.

## Entry Gate

Default runtime load order:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current MV Round `CURRENT_STATE.md`
5. stage-specific rules/templates JIT.

JIT rule:
- Stage 4/6/7/8/9 when production/edit decisions are needed: load `04_HARNESS/rules/mv_editing.md`.
- Character image-to-video work: load `04_HARNESS/rules/ai_video.md`.

Do not load full historical rounds unless debugging/regression.

### No-skip rule｜HARD

A stage is complete only when:
- required artifact exists;
- provenance/identity is valid where required;
- its Gate is PASS.

Missing capability/evidence → mark `BLOCKED/PARTIAL` and stop. Never silently downgrade evidence to keep automation moving.

---

# Stage 1｜Song Discovery / Reference BGM

Goal: choose one exact song/version.

Manual validated path:
`~5 current MV/music observers -> recent songs -> direct real links -> user aesthetic choice`.

Gate:
`REFERENCE_BGM_LOCKED`

---

# Stage 2｜Lock Actual Audio Excerpt

Use actual MP3/WAV/published audio for the chosen version.

Before exposing preview:
- verify title/artist/version/duration;
- record source identity/hash when possible;
- select semantically complete lyric section;
- no previous-phrase contamination;
- preserve first lyric entrance/pickup;
- never end inside a lyric;
- test one-extra-release-line when useful;
- fade only after vocal resolution;
- inspect first ~3s / last ~4s / full excerpt.

Record:
- exact source/version;
- source clip start/end;
- rendered duration;
- pre-roll/fade;
- SHA/hash;
- approval.

Gate:
`BGM_LOCKED`

No silent source/version swap after this point.

---

# Stage 2A｜AUDIO TIMELINE PACKAGE｜FIRST HARD GATE AFTER BGM

> **Mandatory. This is the first correctness-critical deliverable after BGM lock.**
> Detailed rule: `04_HARNESS/rules/mv_audio_timeline.md`
> Contract template: `04_HARNESS/templates/mv_audio_timeline_package_contract.md`

Purpose:
lock the actual song timeline **before any time-dependent semantic analysis, director allocation, dynamic production, editing or subtitle work**.

Why this position is fixed:
- before Stage 2 the exact excerpt/version is not yet stable, so alignment work may be wasted;
- after Stage 2, the audio identity is stable enough to align;
- doing it later causes downstream visual allocation and subtitle timing to inherit guessed lyric positions, as WEB R2 V1/V2 demonstrated.

Package must establish:
1. exact locked-audio identity;
2. trusted exact lyric text/order;
3. strong line-timing evidence;
4. raw evidence + provenance;
5. line-level start/end timeline;
6. selected semantic Anchor Word timing where visually important;
7. verified musical-event map: downbeats/onsets/pickups/breaths/releases/peak/tail;
8. ground-truth alignment QA.

Accepted primary timing routes:
- reliable same-version LRC/timed lyrics + exact clip-offset transformation;
- trusted lyrics + Chinese-capable forced alignment on the locked audio;
- official same-version timestamped lyric/video evidence.

Waveform/BPM/onset guesses alone are forbidden as timing truth.

Canonical deliverable:
`<ROUND>/AUDIO_TIMELINE_PACKAGE/`

Required states:
- `AUDIO_IDENTITY_LOCKED`
- `LYRIC_TEXT_LOCKED`
- `LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
- `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`
- `ALIGNMENT_GROUND_TRUTH_QA_PASS`
- `LYRIC_TIMELINE_LOCKED`
- `MUSIC_EVENT_MAP_VERIFIED`
- `AUDIO_TIMELINE_PACKAGE_LOCKED`

If any fails:
`AUDIO_TIMELINE_PACKAGE_BLOCKED`

### Hard exit condition

**Do not enter Stage 3 until `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.**

---

# Stage 3｜Music / Lyric / Natural Beat Analysis

Load the locked Audio Timeline Package; do not create a new parallel timing model.

Establish:
- lyric semantic structure;
- emotional-strength curve;
- Natural Beats;
- primary/secondary visual opportunities;
- repeated lyric occurrence meaning;
- which Anchor Words should carry visual hits;
- opening hook / primary peak / release.

Natural Beats are semantic/emotional units, not 5s quotas.

Required artifact:
`DIRECTOR_BEAT_MAP`

Its actual time ranges must reference the locked Package.

---

# Stage 4｜Director Concept + Production Allocation

Load `rules/mv_editing.md` JIT before deciding production segments.

Define:
- overall visual concept/world/palette/material;
- character policy;
- dominant visual event per Beat;
- camera/motion differentiation;
- conceptual visual units;
- actual production segments;
- raw-video headroom against locked BGM duration;
- **edit value of each planned source**: HOLD / BRIDGE / HIT / PEAK / RELEASE.

Important:
`conceptual unit != first-frame count != dynamic-video count != final edit fragment count`.

Dynamic source is a material pool for editing, not a pre-cut final timeline.
Director must plan both generation stability and downstream editability.

Gate:
`DIRECTOR_PLAN_LOCKED`

---

# Stage 5｜First Frames

Every production segment receives a deliberate `0-second dynamic anchor` unless reuse is justified.

Each anchor should contain:
- dominant event start state;
- action entrance;
- camera/spatial room;
- secondary physical motion;
- stable character/object closure;
- enough room for a clean source arc and usable endpoint.

Review whole set for:
- beauty;
- lyric hit;
- differentiation;
- world continuity;
- dynamic executability;
- edit value.

Gate:
`FIRST_FRAME_SET_LOCKED`

---

# Stage 6｜Dynamic Prompt Design

Default generation unit: Seedance 2 mini ~5s.
Load `rules/mv_editing.md` + `rules/ai_video.md` JIT.

Shot count is selected by lyric/director task, not by a fixed quota.
WEB R2 validated production default:
- `1-shot / one-take`: breathing, spatial progression, emotion hold, final release;
- `2-shot`: common default for setup/event or detail/emotion;
- `3-shot`: task-specific discovery / setup-event-aftermath / peak;
- `>3-shot`: exceptional hook/peak only, not default.

For a 5s source, default preference is **1–2 shots**, with 3 shots used only when the semantic task earns it.
The goal is not to create a mini finished MV inside every 5s clip; the goal is to create an edit-friendly source with a complete visual-action arc and clean in/out.

Per Shot Camera Contract:
`shot size + angle + start + movement + speed + subject relation + endpoint`.

Whole-set repetition Gate:
- repeated slow pushes;
- repeated standing/look-up;
- repeated camera direction;
- multi-shots that differ only nominally;
- environment motion used as fake action;
- dense internal cut structures repeated across the batch.

Gate:
`DYNAMIC_PROMPT_SET_READY`

---

# Stage 7｜Dynamic Source QA / Retry

Load `rules/mv_editing.md` JIT.
Review the full raw source.

Allowed status:
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

Check:
- identity/face/veil/mask;
- body/hands;
- new-character violation;
- topology;
- dominant event;
- camera execution;
- visual beauty;
- whole-set repetition;
- source audio policy;
- clean in/out and useful internal action windows.

Retry by root cause; do not reset approved material unnecessarily.

AI source audio is non-authoritative and is stripped at ingest unless a deliberately motivated ambience workflow is separately locked.

### Required editor-facing output｜HARD

W07 must output an executable `VISUAL_SOURCE_MAP`, including at minimum:
- source clip id;
- duration/fps;
- clean usable window(s);
- internal cut/action-event timing where relevant;
- known risk window(s);
- recommended edit role: HOLD / BRIDGE / HIT / PEAK / RELEASE;
- QA status.

A prose-only “this clip is good” review is insufficient for reusable editing.

Gate:
`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`

---

# Stage 8A｜Editor Entry / Audio Package Revalidation｜HARD

> Stage 2A acquires timing truth. Stage 8A only revalidates it; editing may not invent timing.

First editor question:
`Does AUDIO_TIMELINE_PACKAGE exist and PASS against the exact current BGM SHA?`

Check:
- package manifest exists;
- BGM SHA/version/duration still match;
- no clip-start/end change;
- no time-stretch/speed change;
- trusted lyric text unchanged;
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`.

If mismatch:
- invalidate package;
- return to Stage 2A;
- invalidate dependent edit/subtitle timing.

Required state:
`EDITOR_AUDIO_GATE_PASS`

No picture timeline may be created before this check.

---

# Stage 8B｜Picture Edit

Load `rules/mv_editing.md` JIT.
Load:
- `line_timeline.csv`
- `anchor_words.csv`
- `music_events.csv`
- `VISUAL_SOURCE_MAP`

Create Edit Map from three clocks:
1. lyric clock;
2. music-event clock;
3. visual-action clock.

Priority:
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

### Long-cut first default
For lyrical/emotional MV, first build Natural-Beat-sized visual blocks and preserve complete source motion arcs.
Do not force lyric start = picture cut.
Do not force Anchor Word = picture cut.
A picture may pre-enter a lyric; a verified semantic hit should preferably happen inside the already-running shot.

WEB R2 default for ~35–40s lyrical MV:
- roughly `8–12` external source fragments;
- avoid multiple consecutive external fragments under `2s`;
- avoid short-distance `A -> B -> A` recycling;
- preserve a longer final release when material allows.

Run the **Fragmentation Gate** from `rules/mv_editing.md` before Edit Map lock.

### Web preview watermark fallback
When current web tooling cannot clean generator marks precisely, use one consistent whole-source zoom/crop transform derived from the worst watermark position across the batch. Do not use mixed per-shot hiding. Recheck top-left and bottom-right risk frames before user delivery. Preserve 9:16 and `SAR 1:1`.

Gate:
`EDIT_MAP_LOCKED`

Then render Picture + locked BGM preview and perform rhythm/full-watch QA plus audio-lag implementation check.

Gate:
`EDIT_PREVIEW_QA_PASS`

---

# Stage 9｜Subtitle Render + QA

Load `rules/mv_editing.md` JIT.
Subtitle timing is already fixed by the Audio Timeline Package.
Stage 9 may style/render it but may not invent a new timing table from picture cuts.

### Phase 9A｜Alignment-check preview
When alignment still needs human perceptual confirmation:
- use canonical `lyrics_exact.srt` directly;
- temporarily disable subtitle fade if needed so fade latency cannot be mistaken for timing drift;
- record frame-quantization error;
- do not manually nudge subtitle timing to match picture cuts.

### Phase 9B｜Style optimization
After timing perception is accepted, optimize:
- Chinese lyric typography;
- light text;
- dark semi-transparent rounded box tightly fit to text;
- horizontal + vertical centering;
- consistent padding;
- fixed lower safe area;
- longest-line wrapping;
- restrained fade;
- max 2 lines;
- no default karaoke.

Before full render inspect first/middle/longest/final lines.

Gate:
`SUBTITLE_STYLE_QA_PASS`

Then verify rendered subtitle follows `lyrics_exact.srt`.

Gate:
`SUBTITLE_IMPLEMENTATION_QA_PASS`

Important:
implementation QA does not re-prove the audio alignment; ground-truth alignment was locked in Stage 2A.

---

# Stage 10｜Final Polish / Delivery QA

Once edit + subtitle pass:
- keep approved timing stable;
- strip AI source audio;
- locked BGM is the sole music truth;
- replace watermarked proxy with HD/no-watermark source where available without changing timing;
- preserve approved composition where possible.

Mandatory final QA:

Audio/timing:
- BGM identity/duration/hash;
- no AI audio leakage;
- current Audio Timeline Package manifest/hash;
- subtitle asset identity.

Picture:
- resolution/fps/SAR/DAR;
- no stretch/black/blank frames;
- no accidental duplicates/topology-risk frames;
- platform marks handled consistently for delivery scope.

Subtitle:
- Golden style;
- safe area;
- centering/padding;
- no overflow/missing characters.

Full watch:
- first ~5s;
- every major lyric/music transition;
- motion peak;
- last ~5s;
- complete render end-to-end where tooling permits.

Gate:
`FINAL_TECH_QA_PASS`

Only then:
`DELIVERABLE_RENDERED`

---

# Mandatory Runtime State Chain

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
→ `DIRECTOR_BEAT_MAP`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPT_SET_READY`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `EDITOR_AUDIO_GATE_PASS`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A later state is invalid if an earlier required state is absent.

---

# Round Close

A Round closes only after preserving:
- user-accepted complete MV;
- locked BGM identity/hash;
- full `AUDIO_TIMELINE_PACKAGE` including raw timing evidence/provenance;
- accepted `VISUAL_SOURCE_MAP`;
- accepted Edit Map;
- accepted subtitle style/timing asset;
- success/failure root-cause notes;
- promoted rules separated from experiments;
- Current State / Automation Matrix.

Do not record only the name of an accepted SRT/LRC or a vague clip-quality note. Preserve executable timing and visual-source assets so the Golden result is reproducible.
