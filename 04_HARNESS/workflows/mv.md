# Workflow｜AI MV Production v1.1

> Source: Round 01 Golden Sample calibration + WEB R2 W02 audio-lock calibration.
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

The goal is not merely to produce a 25–40s file. The goal is to deliver a first-pass excerpt whose opening, lyric body, musical release and fade already feel intentional enough that the user should only need an aesthetic `PASS / change direction` decision, not technical boundary repair.

### W02 first-pass lock algorithm

#### A. Verify the exact source before editing
1. use the actual MP3 / WAV / published audio supplied or lawfully retrieved for the chosen version;
2. verify title / artist / duration / metadata against the selected reference version;
3. never replace it silently with a cover, remix, short upload or differently trimmed version.

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

If dedicated ASR is unavailable, use exact same-version lyrics + waveform / repeated-section alignment + direct listening. Do not pretend ASR ran.

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

### Mandatory pre-delivery Audio Boundary Gate

Before exposing any preview to the user, the system must check all of the following:

1. **Section identity** — is the opening actually the intended chorus/hook/selected section?
2. **No previous-phrase contamination** — is there any intelligible lyric from the previous phrase at the start?
3. **Opening breath** — does the first target lyric have enough pickup to feel musical rather than abruptly chopped?
4. **Final lyric integrity** — is the last lyric line completely sung?
5. **Release line test** — would adding exactly one more complete line make the ending materially more natural?
6. **Fade position** — does fade begin only after the semantic/vocal resolution, rather than over an unfinished word?
7. **Platform cross-check** — when reliable short-video evidence exists, does the chosen lyric cluster align with actual recognizable usage?
8. **Isolated edge listen** — listen to the first ~3s and last ~4s separately, then listen to the entire excerpt once end-to-end.
9. **Duration sanity** — duration is the consequence of musical completeness, not the primary target.

If any item fails, revise internally and do **not** send the preview.

### Human-gate accounting

The intended human interaction is one final aesthetic gate after the first technically valid preview.

If the user has to point out:
- wrong section start;
- previous lyric contamination;
- an incomplete final lyric;
- fade hiding a cut word;
- an obviously under-breathed opening / unresolved ending;

record that as `TECHNICAL_RESCUE`, not as a normal aesthetic preference. This prevents the Automation Matrix from overstating one-shot automation quality.

### Output contract

Record:
- exact source file / version;
- candidate evidence used, including platform evidence availability;
- source start / end;
- final duration;
- first lyric / last lyric;
- pre-roll amount;
- fade in / fade out;
- Audio Boundary Gate result;
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
