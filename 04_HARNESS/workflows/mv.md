# Workflow｜AI MV Production v1.2

> Source: Round 01 Golden Sample calibration + WEB R2 W02 audio-lock calibration + WEB R2 W08 technical rescue.
> Role: execution workflow. Rules live in `rules/*`; benchmark evidence lives in `knowledge/*`; project progress lives in current Round state.
> Core discipline: **no downstream stage may execute unless every required upstream lock/gate has a durable PASS artifact.**

## Entry Gate

Load only:
1. `04_HARNESS/SKILL.md`
2. `04_HARNESS/MANIFEST.md`
3. current MV Round `CURRENT_STATE.md`
4. stage-specific rules / templates / benchmark snapshot as required

Do not reload the full historical round unless debugging.

### No-skip execution rule｜HARD

A stage is not complete because work was attempted. It is complete only when its required output artifact exists and its Gate is PASS.

If a required capability / evidence source is unavailable:
- mark the exact state `BLOCKED` / `PARTIAL`;
- record the missing evidence;
- do not silently substitute a weaker method and continue;
- do not expose a downstream preview as though the Gate had passed.

Every technical failure caught by the user that should have been caught by a documented self-audit is `TECHNICAL_RESCUE`, not an aesthetic gate.

---

## Stage 1｜Song discovery / Reference BGM

### Manual approved path

`~5 MV/music observer sources -> recent ~30-day song scan -> repeated / spreading songs -> direct real MV/video links -> user selects Reference BGM`

Use Benchmark only as evidence, not as a rule source.

### Codex hardening path
When available, additionally resolve:
- exact Douyin music_id;
- exact version / author;
- Creator Center availability;
- publish-time availability.

### Gate
Do not enter music structure until one specific Reference BGM / version is accepted.

Required artifact:
`REFERENCE_BGM_LOCKED`

---

## Stage 2｜Lock the actual audio excerpt

The goal is not merely to produce a 25–40s file. The goal is to deliver a first-pass excerpt whose opening, lyric body, musical release and fade already feel intentional enough that the user should only need an aesthetic `PASS / change direction` decision, not technical boundary repair.

### W02 first-pass lock algorithm

#### A. Verify the exact source before editing
1. use the actual MP3 / WAV / published audio supplied or lawfully retrieved for the chosen version;
2. verify title / artist / duration / metadata against the selected reference version;
3. record a stable file identity/hash when possible;
4. never replace it silently with a cover, remix, short upload or differently trimmed version.

#### B. Use platform evidence before choosing the candidate region
When the song was selected because it is spreading on Douyin / short-video platforms, inspect recent representative uses before cutting:
- preferred: artist / label short-video post, official short clip, Douyin music page or multiple recent same-BGM videos;
- record which lyric cluster repeatedly functions as the recognizable entry / hook;
- platform use is evidence for candidate selection, not permission to copy another creator's exact edit.

If no reliable platform clip is available, mark that evidence as unavailable rather than guessing.

#### C. Build the structural map before setting timecodes
Establish from the actual audio:
- lyric phrase boundaries;
- verse / pre-chorus / chorus / bridge / outro structure where applicable;
- repeated-section correspondence;
- downbeats / musical pickups;
- vocal phrase-resolution points;
- local energy / breath valleys that can support an out-point.

If dedicated ASR is unavailable at this stage, exact same-version lyrics + waveform / repeated-section alignment + direct listening may support **excerpt selection only**. This does **not** automatically qualify as a subtitle/line-timing lock for Stage 8A.

Do not pretend ASR ran.

#### D. Choose the excerpt by complete musical meaning, not a target duration
Candidate priority:
1. recognizable lyric / hook;
2. semantic completeness;
3. immediate opening;
4. dense visual opportunities for the MV;
5. natural musical release;
6. evidence of short-video adoption when available.

Do not force an arbitrary duration. A slightly longer excerpt is preferred over cutting a lyric or losing the natural tail.

#### E. In-point rule
The first audible lyric must belong to the intended section.
- never include a preceding lyrical phrase merely because it is close in time;
- normally allow about `0.3–0.8s` of musical pickup / pre-roll before the first target lyric when this makes the entrance breathe;
- the pickup must not drag in intelligible residue from the previous lyric;
- prefer a breath, downbeat, pickup or clean instrumental edge over an exact zero-margin syllable start.

#### F. Out-point rule
Never end inside a lyric line.
- the final lyric must be fully sung and semantically closed;
- after the core hook/title line, test whether one additional complete release line produces a more natural ending;
- if that additional line improves release without starting a new narrative section, prefer the longer version;
- place the cut after vocal resolution / breath valley, then apply fade;
- do not use fade to hide a truncated lyric.

Typical fade-out can be roughly `0.6–1.5s`, but phrase completion is more important than the numeric fade length.

### Mandatory Audio Boundary Gate

Before exposing any excerpt preview to the user, check:
1. section identity;
2. no previous-phrase contamination;
3. opening breath / pickup;
4. final lyric integrity;
5. one-extra-release-line test;
6. fade begins after resolution;
7. platform cross-check when reliable evidence exists;
8. isolated first ~3s + last ~4s inspection/listen where tooling permits;
9. full excerpt end-to-end inspection/listen;
10. duration is a consequence of musical completeness, not the primary target.

If any item fails, revise internally and do not send the preview.

### Output contract
Record:
- exact source file / version;
- source identity/hash when possible;
- source start / end;
- final duration;
- first lyric / last lyric;
- pre-roll;
- fade in / fade out;
- evidence used;
- Audio Boundary Gate result;
- approval status.

Required artifact/state:
`BGM_LOCKED`

Downstream timing uses this exact locked file. No silent version swap.

---

## Stage 3｜Music / lyric structure

Before directing, establish:
- exact lyric text sequence for the locked excerpt;
- musical rises / releases;
- emotional curve;
- natural Beats;
- likely visual emphasis points;
- repeated lyric occurrences distinguished from each other.

Natural Beat structure comes before the 5s generation constraint.

### Important distinction

Stage 3 may create a director-level phrase/beat map without word-level ASR, but it must label confidence honestly.

- `LYRIC_TEXT_LOCKED` may pass when exact same-version text is verified.
- `LYRIC_TIMELINE_LOCKED` does **not** pass merely because BPM, waveform valleys or approximate phrase starts are known.

Required artifacts:
- `LYRIC_TEXT_LOCKED`
- `DIRECTOR_BEAT_MAP`

---

## Stage 4｜Director concept + production-unit design

Define:
- one overall visual concept;
- world / palette / material system;
- character policy;
- Opening Hook;
- dominant visual event per Beat;
- camera / motion differentiation;
- conceptual visual units;
- actual production segments.

Important:
`conceptual visual unit != first-frame count != dynamic-video count`

Use enough production segments to cover the locked audio with edit headroom.

R1 reference only:
`36.8s final -> 8 × 5s raw clips = 40s raw material`

This is a validated example, not a universal quota.

Required artifact/state:
`DIRECTOR_PLAN_LOCKED`

---

## Stage 5｜First-frame planning and generation

Each production segment gets an explicit first-frame plan unless a deliberate reuse is justified.

A first frame is a `0-second dynamic anchor`, containing:
- main visual event at its start state;
- clear action entrance;
- camera / spatial room;
- secondary environmental motion;
- physical after-effect;
- stable character / object closure.

Generate / review as an entire set for:
- beauty;
- lyric hit;
- differentiation;
- world continuity;
- dynamic executability.

Do not enter dynamic generation until the first-frame set passes.

Required artifact/state:
`FIRST_FRAME_SET_LOCKED`

---

## Stage 6｜Dynamic prompt design

Model default: Seedance 2 mini, 5s production clips.

For any character-containing image-to-video prompt, `rules/ai_video.md` requires the exact portrait-safety prefix before all other instructions.

Every clip must define:
- 0s continuity from first frame;
- dominant visual event;
- secondary physical after-effect;
- camera grammar;
- rough internal timing;
- explicit forbidden failures;
- source-audio policy from `rules/ai_video.md`.

### Camera structure options

Shot count is selected by director task, not a fixed quota.

- one-take is valid when a continuous camera path creates sustained visual progression;
- 2–3 shots are valid for setup/event/aftermath, emotion/detail shifts, discovery;
- denser 3–5-shot structures are valid for hooks / motion peaks when each cut earns new information, emotion or viewpoint.

Per individual Shot, prefer one clear Camera Contract:
`shot size + angle + start + movement + speed + subject relation + endpoint`.

### Repetition Gate
Before generation, check the whole set for repeated:
- slow push / slow pull;
- standing / turning / looking up;
- wind / rain / fog as the only action;
- identical cut patterns;
- identical camera direction;
- adjacent multi-shots that differ in name but not materially in shot size / angle / action.

Required artifact/state:
`DYNAMIC_PROMPT_SET_READY`

---

## Stage 7｜Dynamic QA + root-cause retry

Review each full 5s source, not only the intended final trim.

Direct FAIL examples:
- new person appears;
- veil / mask breaks;
- identity drift;
- body / hand deformation;
- dominant event fails;
- camera loses control;
- first-frame beauty collapses;
- foreground topology changes incorrectly.

QA status is not binary whole-clip pass/fail. A source may be:
- `PASS_FULL`;
- `SOURCE_USABLE / TRIM_REQUIRED`;
- `REGEN_WATCH`;
- `REGENERATE`.

Retry by root cause:
- prompt / motion problem -> keep first frame, rewrite dynamic prompt;
- first frame physically unsuitable -> return to first-frame stage;
- local bad frames but enough clean material -> trim later, do not waste regeneration;
- repeated failure -> simplify motion / camera before redesigning whole concept.

Specific R1 lesson:
For foreground occlusion, prefer camera movement behind a solid intact edge over asking a large foreground sheet to deform across the frame.

Required artifact/state:
`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`

---

# Stage 8A｜Audio / Lyric Timeline Lock｜MANDATORY PRE-EDIT GATE

> This stage must complete **before any picture edit timeline is created**.
> WEB R2 W08 failure proved that exact lyric text + waveform guesses are insufficient for edit/subtitle synchronization.

## 8A.1 Verify locked audio identity again
Before alignment:
- verify the exact Stage 2 locked audio file/version/hash;
- confirm duration is unchanged;
- reject silent substitution.

## 8A.2 Lock exact lyric text
Confirm the exact lyric text/order for the locked excerpt.
Repeated identical lines must be identified as separate occurrences.

Required state:
`LYRIC_TEXT_LOCKED`

## 8A.3 Acquire strong timing evidence
Preferred evidence hierarchy:
1. actual ASR / forced alignment run on the locked audio;
2. reliable same-version LRC / timed lyric source;
3. exact timestamps from an official same-version lyric video/source when directly verifiable.

Then constrain/correct the timing source against the exact known lyric text.

### Forbidden downgrade
BPM grid, waveform valleys, rough syllable-length estimation, editor intuition, or visual segment boundaries cannot by themselves produce `LYRIC_TIMELINE_LOCKED`.

If no strong source is available:
`LYRIC_TIMELINE_BLOCKED`

Stop. Do not create a picture edit and do not render a subtitle preview from guesses.

## 8A.4 Boundary self-audit
For every lyric line:
- verify start;
- verify end;
- cross-check against onsets / valleys / beat evidence;
- inspect/listen around each boundary (approximately ±0.5s where tooling permits);
- inspect first ~3s and last ~4s independently;
- inspect/listen through the whole locked excerpt against timestamps;
- ensure repeated lyric occurrences are mapped correctly;
- ensure final lyric resolves before fade tail.

Export a durable timing asset (`.srt`, `.lrc`, CSV/JSON/MD table).

Only after this full audit:
`LYRIC_TIMELINE_LOCKED = YES`

## 8A.5 Beat / musical event map verification
With lyric timing locked, verify:
- downbeats / strong onsets;
- phrase starts and releases;
- rests / breath windows;
- primary motion peak;
- outro / tail.

Required state:
`BEAT_MAP_VERIFIED`

### Stage 8A hard exit condition
Do not enter Stage 8B unless all three exist:
- `LYRIC_TEXT_LOCKED`
- `LYRIC_TIMELINE_LOCKED`
- `BEAT_MAP_VERIFIED`

---

# Stage 8B｜Picture Edit v1 / v2

Create the edit map **after** Stage 8A, not before.

Do not force equal clip durations.

Priority:
`lyric / musical truth > emotional flow > internal action integrity > musical cut point > mechanical equal timing`

For every edit fragment record:
- source clip;
- source in/out;
- final timeline in/out;
- lyric line / phrase window it serves;
- beat/downbeat/semantic reason for the cut;
- motion-arc reason;
- whether it is full source or trimmed material.

Picture cuts may occur inside a lyric when musically/directorially justified, but subtitle timing is independent and remains bound to the locked audio timeline.

R1 validated editing improvement:
- v1: heavy per-clip trimming worked but felt less precise;
- v2: preserve more complete internal 5s action and compress through selective trim + short overlap / transition.

### Mandatory edit-map self-audit before rendering
Check:
1. every lyric line has intended visual coverage;
2. key lyric hits occur near the actual lyric/beat event, not a guessed phrase position;
3. no source fragment is duplicated without a deliberate reason;
4. repeated visual families are not back-to-back unnecessarily;
5. risky topology windows identified in Stage 7 are excluded;
6. motion peaks and releases align with the verified musical map;
7. final tail has enough visual breathing room.

Only then:
`EDIT_MAP_LOCKED = YES`

Render a clean **picture + locked BGM preview without final subtitle styling** when useful for rhythm inspection.

Required state before subtitle burn-in:
`EDIT_PREVIEW_QA_PASS`

---

## Stage 9｜Subtitle Rendering + Sync QA

Subtitle timing is already fixed by Stage 8A. Stage 9 does **not** invent or recalibrate timing from picture cuts.

### Golden subtitle style preload｜HARD
Before styling, reload the R1 Golden subtitle reference. Do not design a new style from memory.

R1 accepted base system:
- Chinese lyrics;
- light text;
- dark semi-transparent rounded background tightly fitted to the lyric;
- text visually centered horizontally and vertically inside the box;
- consistent inner padding;
- fixed comfortable lower safe-area placement;
- restrained fade behavior;
- max 2 lines;
- no base karaoke / word-by-word effect.

### Subtitle Style Gate
Before full render, inspect representative samples from:
- first lyric;
- middle lyric;
- longest lyric;
- final lyric.

Check:
- text/box centering;
- padding consistency;
- box opacity and rounding consistency;
- no clipping / overflow;
- safe-area position consistent across shots;
- readable against both bright sky and dark tree/background;
- line wrapping follows Golden rules;
- fades do not obscure the first/last syllable.

Required state:
`SUBTITLE_STYLE_QA_PASS`

### Subtitle Sync Gate
After burn-in, inspect every line start/end against the **locked audio timing asset**.

Required state:
`SUBTITLE_SYNC_QA_PASS`

If any line is wrong, repair timing/alignment asset and rerun affected downstream steps. Do not call it an aesthetic preference.

---

## Stage 10｜Final Polish / Pre-delivery QA / Publish-grade Source Replacement

Once edit + subtitle timing/style pass:
- do not casually retime already approved cuts;
- apply restrained tail / finishing only;
- strip AI source audio; locked BGM remains the only music truth;
- clean platform marks consistently or replace with watermark-free HD equivalents when available;
- preserve approved directing / edit timing / subtitles during source replacement.

### Mandatory final self-audit
Before delivery, verify and record:

#### Audio / timing
- exact locked BGM identity/duration;
- no AI source audio leakage;
- lyric timeline asset is the locked version;
- subtitle sync spot-check includes every line boundary;
- beat/cut map still corresponds to locked audio.

#### Picture
- aspect ratio / SAR / resolution / fps are valid;
- no accidental stretch;
- no black/blank frames;
- no duplicated accidental shots;
- no known topology-risk frames;
- no visible unhandled platform mark if cleanup is part of this deliverable.

#### Subtitle
- Golden visual spec loaded;
- safe-area placement consistent;
- text centered in box;
- no overflow/missing character;
- first/middle/longest/final line sampled visually.

#### Full-watch
- inspect first ~5s;
- inspect every transition around primary lyric/beat changes;
- inspect motion peak;
- inspect last ~5s;
- inspect the complete render end-to-end where playback tooling permits.

Any failed item is repaired internally before delivery.

Required state:
`FINAL_TECH_QA_PASS`

Only then:
`DELIVERABLE_RENDERED`

Publish-time music availability remains a separate Gate.

---

## Mandatory Runtime State Chain

For any future MV edit/final stage, enforce:

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `DIRECTOR_BEAT_MAP`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPT_SET_READY`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

A later state is invalid if any earlier required state is absent.

---

## Round close

A Round may close only when it has:
- one user-accepted complete MV;
- final audio / lyric timing / edit / subtitle assets;
- success / failure root-cause notes;
- promoted rules separated from experiments;
- Golden Sample / Golden References;
- updated Current State / Automation Matrix.

Do not invent missing timing or performance data during retrospective. Record unknowns explicitly and collect them prospectively next round.
