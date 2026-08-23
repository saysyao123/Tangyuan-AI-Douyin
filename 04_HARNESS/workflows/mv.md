# Workflow｜AI MV Production v1.3

> Source: Round 01 Golden Sample + WEB R2 camera calibration + WEB R2 repeated timing technical rescue.
> Role: authoritative MV execution workflow.
> Core discipline: **no downstream stage may execute unless every required upstream Gate has a durable PASS artifact.**

## Entry Gate

Default runtime load order:
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current MV Round `CURRENT_STATE.md`
5. stage-specific rules/templates JIT.

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
lock the actual song timeline before any time-dependent directing/editing.

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

Current WEB R2 exception: visual assets created before v1.3 remain valid, but no V3 edit may proceed until its package passes.

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

Define:
- overall visual concept/world/palette/material;
- character policy;
- dominant visual event per Beat;
- camera/motion differentiation;
- conceptual visual units;
- actual production segments;
- raw-video headroom against locked BGM duration.

Important:
`conceptual unit != first-frame count != dynamic-video count`.

R1 validated example only:
`36.8s final -> 8 × 5s raw = 40s source`.

Director timing decisions must use Package line/anchor/music events, not approximate lyric guesses.

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
- stable character/object closure.

Review whole set for:
- beauty;
- lyric hit;
- differentiation;
- world continuity;
- dynamic executability.

Gate:
`FIRST_FRAME_SET_LOCKED`

---

# Stage 6｜Dynamic Prompt Design

Default generation unit: Seedance 2 mini ~5s.

Character image-to-video obeys `rules/ai_video.md` exact fictional-character prefix and first-frame character closure.

Shot count is selected by lyric/director task:
- one-take when continuous progression is strong;
- 2–3 shots for setup/event/aftermath, discovery, detail/emotion shifts;
- denser structures for earned hook/motion peaks.

Per Shot Camera Contract:
`shot size + angle + start + movement + speed + subject relation + endpoint`.

Whole-set repetition Gate:
- repeated slow pushes;
- repeated standing/look-up;
- repeated camera direction;
- multi-shots that differ only nominally;
- environment motion used as fake action.

Gate:
`DYNAMIC_PROMPT_SET_READY`

---

# Stage 7｜Dynamic Source QA / Retry

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
- source audio policy.

Retry by root cause; do not reset approved material unnecessarily.

AI source audio is non-authoritative and is stripped at ingest unless a deliberately motivated ambience workflow is separately locked.

Gate:
`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`

Output should include a `VISUAL_SOURCE_MAP` of clean/usable internal windows.

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

Do not force lyric start = picture cut.
A picture may pre-enter a lyric to set up an action; the semantic hit should land near the verified Anchor Word/music event.

For every fragment record:
- source clip;
- source in/out;
- final timeline in/out;
- lyric/Beat served;
- music event/Anchor Word served;
- motion-arc reason;
- full/trimmed status.

R1 validated edit lesson:
preserve good internal 5s actions; solve total duration by selective trim + short overlap/transition instead of equal mechanical trimming.

Self-audit:
- every lyric has intentional visual coverage;
- semantic hits use verified time, not guessed phrase positions;
- no accidental duplicate source;
- repeated visual families separated where possible;
- known topology-risk windows excluded;
- peak/release aligned to verified music map;
- final tail has breathing room.

Gate:
`EDIT_MAP_LOCKED`

Then render picture + locked BGM preview and perform rhythm/full-watch QA.

Gate:
`EDIT_PREVIEW_QA_PASS`

---

# Stage 9｜Subtitle Render + QA

Subtitle timing is already fixed by the Audio Timeline Package.
Stage 9 may style/render it but may not invent a new timing table from picture cuts.

Base Golden style from R1:
- Chinese lyrics;
- light text;
- dark semi-transparent rounded box tightly fit to text;
- horizontal + vertical centering;
- consistent padding;
- fixed lower safe area;
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
- preserve approved composition where possible rather than solving watermark by arbitrary crop.

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
- accepted Edit Map;
- accepted subtitle style/timing asset;
- success/failure root-cause notes;
- promoted rules separated from experiments;
- Current State / Automation Matrix.

Do not record only the name of an accepted SRT/LRC. Preserve the executable timing asset and provenance so the Golden result is reproducible.
