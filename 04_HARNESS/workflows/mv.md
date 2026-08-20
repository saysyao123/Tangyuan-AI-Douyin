# Workflow｜AI MV Production v1.0

> Source: Round 01 Golden Sample calibration.
> Role: execution workflow. Rules live in `rules/*`; benchmark evidence lives in `knowledge/*`; project progress lives in current Round state.

## Entry Gate

Load only:
1. `04_HARNESS/SKILL.md`
2. `04_HARNESS/MANIFEST.md`
3. current MV Round `CURRENT_STATE.md`
4. stage-specific rules / templates / benchmark snapshot as required

Do not reload the full historical round unless debugging.

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

---

## Stage 2｜Lock the actual audio excerpt

Preferred order:
1. use the actual source MP3 / WAV / published audio supplied or retrieved for the chosen version;
2. identify the complete lyrical / musical excerpt;
3. preserve semantic completeness and natural musical tail;
4. render a preview;
5. user listens and approves.

Do not force an arbitrary duration if a slightly longer excerpt is more musically complete.

Output must record:
- source file;
- source start / end;
- final duration;
- fade in / fade out;
- approval status.

Downstream timing uses this exact locked file. No silent version swap.

---

## Stage 3｜Music / lyric structure

Before directing, establish:
- lyric phrases;
- musical rises / releases;
- emotional curve;
- natural Beats;
- likely visual emphasis points.

Natural Beat structure comes before the 5s generation constraint.

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
- explicit forbidden failures.

### Camera structure options

Single-shot is allowed when the visual event benefits from continuous spatial tension.

2–3 shot structure inside 5s is also validated, especially for:
- emotional fragments;
- reflection / interaction actions;
- macro detail sequences.

Do not make every clip the same structure.

### Repetition Gate
Before generation, check the whole set for repeated:
- slow push;
- standing / turning / looking up;
- wind / rain / fog as the only action;
- identical cut patterns;
- identical camera direction.

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

Retry by root cause:
- prompt / motion problem -> keep first frame, rewrite dynamic prompt;
- first frame physically unsuitable -> return to first-frame stage;
- repeated failure -> simplify motion / camera before redesigning whole concept.

Specific R1 lesson:
For foreground occlusion, prefer camera movement behind a solid intact edge over asking a large foreground sheet to deform across the frame.

---

## Stage 8｜Edit v1 / v2

Create an edit timeline before polish.

Do not force equal clip durations.

Priority:
`emotion flow > internal action integrity > musical cut point > mechanical equal timing`

R1 validated editing improvement:
- v1: heavy per-clip trimming worked but felt less precise;
- v2: preserve more complete 5s internal action and compress total duration through selective trim + short overlap / transition.

Keep source clip order, selected in/out points, overlap / transition duration and rationale traceable.

---

## Stage 9｜Lyrics / subtitle alignment

Basic lyric system first; do not mix subtitle timing calibration with complex lyric effects.

Hard rule:
**subtitle timing comes from the locked audio, never from visual segment boundaries.**

Codex preferred pipeline:
`Whisper word timestamps -> constrain / correct against known lyrics -> human spot-check -> final subtitle file`

Same-version reliable LRC may be used as additional timing evidence.

Base subtitle style:
- light Chinese text;
- dark semi-transparent rounded box tightly fitting text;
- visual horizontal + vertical centering;
- lower safe area;
- restrained fade;
- max 2 lines.

---

## Stage 10｜Final polish / publish-grade source replacement

Once edit + subtitle timing pass:
- do not casually retime already approved cuts;
- apply restrained tail / finishing only;
- replace manual watermarked source clips with watermark-free HD equivalents in the Codex production environment before publish-grade export;
- preserve the approved directing, edit timing and subtitles during source replacement.

Publish-time music availability is a separate Gate.

---

## Round close

A Round may close when it has:
- one user-accepted complete MV;
- final asset / timing records;
- success / failure root-cause notes;
- promoted rules separated from experiments;
- Golden Sample / Golden References;
- updated Current State.

Do not invent missing time or performance data during retrospective. Record unknowns explicitly and collect them prospectively next round.
