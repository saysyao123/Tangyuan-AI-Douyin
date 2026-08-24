# Workflow｜AI MV Production v1.6

> Source: Round 01 Golden + WEB R2 timing rescue + V3/V3.1 editing calibration + V3.2 shot normalization + W09 subtitle calibration.
> Role: authoritative MV execution workflow.
> Core: **no downstream stage executes unless required upstream Gate has a durable PASS artifact.**
> Detailed timing/edit/source-normalization/subtitle rules are modular and loaded JIT.

## Runtime load order

1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current Round `CURRENT_STATE.md`
5. stage-specific rules JIT

JIT:
- Stage 4/6/7/8/9: `rules/mv_editing.md`
- Stage 6 character I2V: `rules/ai_video.md`
- Stage 7.5/8: `rules/mv_source_normalization.md`
- **Stage 9: `rules/mv_subtitle.md`**

A stage is complete only when its required artifact exists and its Gate is PASS. Missing evidence/capability means `BLOCKED/PARTIAL`; never silently downgrade evidence.

---

# Stage 1｜Song Discovery

Choose one exact song/version.

Gate: `REFERENCE_BGM_LOCKED`

---

# Stage 2｜Lock Actual Audio Excerpt

Use the actual MP3/WAV/published audio.

Before approval:
- verify title/artist/version/duration;
- select a semantically complete lyric section;
- no previous-phrase contamination;
- preserve pickup/first lyric entrance;
- never end inside a lyric;
- test an extra release line when useful;
- fade only after vocal resolution;
- inspect opening / ending / full excerpt.

Record source identity, clip start/end, duration, fade/lead-in, hash and approval.

Gate: `BGM_LOCKED`

No silent version/source swap after this point.

---

# Stage 2A｜AUDIO TIMELINE PACKAGE｜FIRST HARD GATE AFTER BGM

Detailed rule: `rules/mv_audio_timeline.md`.

Purpose: lock the song timeline **before any time-dependent semantic analysis, Director allocation, dynamic production, edit or subtitle work**.

This position is fixed:
- earlier than BGM lock risks wasted alignment if version/excerpt changes;
- later lets guessed timing contaminate downstream production.

Package must lock:
- exact audio identity/hash;
- trusted lyric text/order;
- strong line-timing evidence + raw evidence/provenance;
- line timeline;
- selected Anchor Words;
- verified music events;
- ground-truth alignment QA.

Accepted primary evidence:
- verified same-version LRC/timed lyrics;
- trusted lyrics + Chinese-capable forced alignment;
- official same-version timed lyric/video evidence.

Waveform/BPM/onsets alone are diagnostic, never timing truth.

Gate: `AUDIO_TIMELINE_PACKAGE_LOCKED`

**Do not enter Stage 3 until PASS.**

---

# Stage 3｜Music / Lyric / Natural Beat Analysis

Load the locked Package; never create a second lyric clock.

Establish:
- semantic structure;
- emotion/energy curve;
- Natural Beats;
- primary/secondary visual opportunities;
- repeated-line meaning;
- Anchor Words for visual hits;
- hook / peak / release.

Natural Beats are semantic/emotional units, not 5s quotas.

Required artifact: `DIRECTOR_BEAT_MAP`

---

# Stage 4｜Director Concept + Production Allocation

Load `rules/mv_editing.md` JIT.

Define:
- visual world / palette / material;
- character policy;
- dominant event per Beat;
- camera/motion differentiation;
- conceptual units vs actual production segments;
- raw-video headroom;
- planned edit role: `HOLD / BRIDGE / HIT / PEAK / RELEASE`.

Important:
`conceptual unit != first-frame count != dynamic-video count != final edit fragment count`.

Dynamic generation creates an editable source pool, not a pre-cut final MV.

Gate: `DIRECTOR_PLAN_LOCKED`

---

# Stage 5｜First Frames

Each production segment receives a deliberate 0-second dynamic anchor unless reuse is justified.

Require:
- dominant event start state;
- action entrance;
- spatial/camera room;
- secondary physical motion;
- stable character/object closure;
- clean source-arc potential and usable endpoint.

Review whole set for lyric hit, beauty, differentiation, continuity and dynamic/edit executability.

Gate: `FIRST_FRAME_SET_LOCKED`

---

# Stage 6｜Dynamic Prompt Design

Default generation unit: Seedance-like ~5s.
Load `rules/mv_editing.md` + `rules/ai_video.md`.

Shot count follows the Director task:
- 1-shot: space / breathing / continuous emotion / release;
- 2-shot: common default for setup-event or detail-emotion;
- 3-shot: task-specific discovery / setup-event-aftermath / peak;
- >3-shot: exceptional hook/peak only.

Default preference for 5s source: **1–2 shots**. Three shots only when earned by semantics.

The goal is an edit-friendly source with a clear motion arc and clean in/out, not a miniature finished MV in every 5s clip.

Run whole-set camera/motion/repetition review before generation.

Gate: `DYNAMIC_PROMPT_SET_READY`

---

# Stage 7｜Dynamic Source QA / Retry

Review full raw source.

Statuses:
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

Check identity, hands/body, topology, event execution, camera, beauty, repetition, source audio, clean in/out and internal action/cut windows.

AI source audio is non-authoritative and removed at ingest unless a separately locked ambience workflow exists.

Required editor-facing output: executable `VISUAL_SOURCE_MAP` containing source id, fps/duration, clean windows, internal cut/action timing, risk windows, edit role and QA status.

Gate: `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`

---

# Stage 7.5｜Shot Normalization / Atom-Arc Library｜HARD FOR MULTI-SHOT SOURCES

Load `rules/mv_source_normalization.md`.

Purpose: remove hidden edit complexity before Picture Edit.

For returned 1–3-shot sources:
- preserve original 5s file unchanged;
- map real internal cuts/events;
- derive usable single-state `ATOM` units;
- retain a multi-shot `ARC` only when its internal grammar has clear Director value;
- reject duplicate, topology-risk and meaningless micro-shots;
- for WEB preview, apply one consistent batch watermark-safe crop/zoom to derived proxies and remove source audio.

Required artifact:
`NORMALIZED_SHOT_LIBRARY_MAP.csv`

Gate:
`SHOT_LIBRARY_READY`

A complex multi-shot source must not arrive at final editing as an opaque block that the editor has to rediscover from scratch.

---

# Stage 8A｜Editor Audio Gate｜HARD

Stage 2A acquires timing truth; Stage 8A only revalidates it.

Check exact current BGM against Package manifest/hash/version/duration/clip/speed/lyrics.

Mismatch -> invalidate timing-dependent edit/subtitle work and return to Stage 2A.

Gate: `EDITOR_AUDIO_GATE_PASS`

---

# Stage 8B｜Picture Edit

Load:
- `line_timeline.csv`
- `anchor_words.csv`
- `music_events.csv`
- `VISUAL_SOURCE_MAP`
- `NORMALIZED_SHOT_LIBRARY_MAP.csv` when Stage 7.5 applies.

Coordinate three clocks:
1. lyric clock;
2. music-event clock;
3. visual-action clock.

Priority:
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`.

### Long-cut-first default
For lyrical/emotional MV:
- build Natural-Beat-sized visual blocks first;
- preserve complete motion arcs;
- lyric start does not require picture cut;
- Anchor Word does not require picture cut;
- allow semantic hit inside an already-running shot;
- avoid repeated short-distance A-B-A recycling;
- preserve a long final release when material allows.

### Fragmentation QA｜HARD
Count both:
1. external timeline fragment count;
2. **perceptible visible-shot count**, including shots hidden inside retained Arcs.

A timeline with few external blocks may still be visually fragmented if those blocks contain many generated internal cuts.

For ~35–40s lyrical MV, `8–12 external blocks` remains a useful default, but visible-shot count and subjective flow decide the Gate—not the external number alone.

### WEB watermark fallback
When exact cleanup is unavailable, use one consistent whole-source batch crop/zoom derived from the worst corner mark. Preserve 9:16 and SAR 1:1; inspect top-left and bottom-right risk frames before delivery.

Gate: `EDIT_MAP_LOCKED`

Render Picture + locked BGM preview, verify no new global audio lag, then human rhythm/full-watch review.

Gate: `EDIT_PREVIEW_QA_PASS`

---

# Stage 9｜Subtitle Render + QA

**Load `rules/mv_subtitle.md` JIT.**

Subtitle timing already comes from the locked Audio Timeline Package. Stage 9 cannot invent/nudge a second timing table from picture cuts.

### 9A Alignment-check preview
When perceptual confirmation is needed:
- use canonical `lyrics_exact.srt`;
- fade may be temporarily disabled so fade latency is not confused with timing drift;
- record frame quantization;
- investigate a reported line against Stage 2A evidence before any timing change.

### 9B Default style
When the locked subtitle baseline has already been user-accepted:
- **reuse it directly**;
- do not restart A/B/C style exploration per song;
- render the established typography/position/rounded-box/padding/fade system;
- only reopen style design if the user explicitly requests a different subtitle look.

### 9C Fixed implementation QA｜HARD
Run the Subtitle Runtime Gate:
- all-line timing implementation check against canonical SRT;
- actual rendered glyph bbox -> fresh rounded box generation;
- all-line four-side padding QA;
- all-line text/box center QA;
- mandatory first / shortest / longest-one-line / two-line / final visual samples;
- no overflow / critical-subject cover / unsafe-area failure.

Implementation defects are fixed as implementation defects; they do not automatically reopen style exploration.

Gates:
`SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`

Implementation QA proves render follows the locked SRT; it does not re-prove singer alignment.

---

# Stage 10｜Final Polish / Delivery QA

Keep approved timing stable.

Mandatory:
- locked BGM identity/duration/hash;
- no AI source-audio leakage;
- current Audio Timeline Package identity;
- resolution/fps/SAR/DAR;
- no stretch/blank/black/accidental duplicate/risk frames;
- platform marks handled consistently;
- subtitle style/safe area/centering/overflow;
- full-watch opening, major transitions, peak, ending and complete render.

Prefer watermark-free HD source/Codex cleanup for publish-grade output; WEB uniform crop remains fallback only.

Gate: `FINAL_TECH_QA_PASS`

Then: `DELIVERABLE_RENDERED`

---

# Mandatory Runtime State Chain

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `DIRECTOR_BEAT_MAP`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPT_SET_READY`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `SHOT_LIBRARY_READY` when multi-shot sources require normalization
→ `EDITOR_AUDIO_GATE_PASS`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A later state is invalid when an earlier required state is absent.

---

# Round Close

Preserve:
- user-accepted complete MV;
- locked BGM identity/hash;
- full Audio Timeline Package including raw evidence/provenance;
- accepted `VISUAL_SOURCE_MAP`;
- normalized Shot Library Map when used;
- accepted Edit Map;
- accepted subtitle timing/style asset + geometry/timing QA report;
- root-cause notes and promoted rules;
- Current State / Automation Matrix.

Do not preserve only filenames or vague QA prose. Preserve executable timing/source/edit/subtitle assets so the result is reproducible.
