# OSS MV Optimization Source Intake v1.1

Status: `SOURCE_LOCKED / UPSTREAM_SONG_AUDIO_PENDING`

## Source project

- Repository / URL: `https://github.com/penposs/mvmaker-h3-skills`
- Branch: `main`
- Locked source commit: `796797030275fe57afaba736771e8510c848799d`
- Commit message: `Publish MVMaker H3 skills`
- License: `Apache-2.0`
- Relevant files / directories:
  - `mv-storyboard-director/SKILL.md`
  - `mv-storyboard-director/references/concept-and-audiovisual.md`
  - `mv-storyboard-director/references/staging-and-montage.md`
  - `mv-storyboard-director/references/optional-elements.md`
  - `mv-storyboard-director/references/output-contract.md`
  - `mvmaker-h3-skill/SKILL.md`
- User-specified optimization focus: test whether the source project's director knowledge and stage-handoff discipline can improve the current R3 MV without replacing stable song/audio/Runtime truth.

## What the source actually changes

The source contains two separable layers:

1. `mv-storyboard-director`: creative/director knowledge before generation.
2. `mvmaker-h3-skill`: H3-specific orchestration, segmentation, storyboard packaging, RunningHub execution, validation and assembly.

For this experiment, the first layer is the main optimization source. H3-specific production constraints are not imported into R3 by default.

| ID | Source location | Claimed improvement | Current Runtime equivalent | Integration class | Risk | Test decision |
|---|---|---|---|---|---|---|
| OSS-01 | `mv-storyboard-director/SKILL.md` | Establish Director Thesis before shot writing | Natural Beat -> Director Plan | `KNOWLEDGE_CANDIDATE` | LOW | TEST |
| OSS-02 | `concept-and-audiovisual.md` | One primary visual engine + bounded auxiliaries | Director concept / visual world | `KNOWLEDGE_CANDIDATE` | LOW | TEST |
| OSS-03 | `concept-and-audiovisual.md` | Sync / parallel / counterpoint / negative-space / audiovisual bridge | Lyric visual hit + beat map | `KNOWLEDGE_CANDIDATE` | MEDIUM | TEST without weakening lyric-hit priority |
| OSS-04 | `staging-and-montage.md` | Motive-first camera-subject-space design | Director camera grammar | `STAGE_OVERLAY` | LOW | TEST |
| OSS-05 | `staging-and-montage.md` | Every cut has a continuity/montage reason | Dynamic multi-shot / Edit Map | `STAGE_OVERLAY` | LOW | TEST |
| OSS-06 | `optional-elements.md` | Every optional effect has trigger/function/range/stop condition | Director / Dynamic Prompt | `KNOWLEDGE_CANDIDATE` | LOW | TEST |
| OSS-07 | `mvmaker-h3-skill/SKILL.md` | Persist immutable creative handoffs and reduce downstream creative drift | Runtime durable artifacts | `STAGE_OVERLAY` | MEDIUM | TEST as Creative Drift QA, not Runtime replacement |
| OSS-08 | H3 integer 10-15s production containers | H3 execution compatibility | R3 5s-ish Seedance source strategy | `OUT_OF_SCOPE` | HIGH if imported | REJECT for this test |
| OSS-09 | H3 16:9 four-panel storyboard-as-Picture-1 | H3 Ref2VA input packaging | R3 first-frame-per-source workflow | `OUT_OF_SCOPE` | HIGH if imported | REJECT for this test |
| OSS-10 | RunningHub/H3 submission + assembly | H3 production orchestration | R3 Web/Seedance execution path | `OUT_OF_SCOPE` | HIGH / unrelated execution boundary | REJECT for this test |

## Conflict check

Locked current Runtime rules remain authoritative:

- Canonical state authority: KEEP CURRENT.
- HG01-HG05 durable receipts: KEEP CURRENT.
- Audio Timeline before time-dependent Director work: KEEP CURRENT.
- transition / revision hash-chain logic: KEEP CURRENT.
- media asset identity and publish transaction truth: KEEP CURRENT.
- Web Bridge guard semantics: KEEP CURRENT.
- `歌词视觉命中 > 轻叙事连续 > 炫技镜头`: KEEP CURRENT and use as tie-break authority over source-project director suggestions.
- `Patch, Don't Cascade`: KEEP CURRENT.
- accepted actual first frame K0 remains authoritative over abandoned prose at Dynamic stage.

Potential conflict: source project encourages 10-15 second integer production segments and intact four-panel H3 storyboard inputs. These are model-adapter constraints, not general director truth. They are explicitly excluded from the first R3 integration test.

## Minimal integration set

Do not import the source project wholesale.

After HG01 + HG02 + Audio Timeline are locked, test only these bounded overlays:

1. Director Thesis.
2. Primary Visual Engine.
3. Explicit audiovisual relationship per beat/segment.
4. Motive-first camera-subject-space grammar.
5. `WHY CUT HERE` montage check for multi-shot dynamics.
6. Optional-element stop conditions.
7. Creative Drift QA across `Director -> First Frame -> Dynamic Prompt`.

Hold constant where practical:
- SONG_FAMILY;
- exact locked BGM;
- lyric/audio timeline;
- aspect ratio and target final duration;
- generation model/tool availability;
- Human Gate criteria.

## Evaluation dimensions

Record in `RESULT_MATRIX.md`:
- lyric visual hit;
- whole-MV coherence;
- director/camera quality;
- shot diversity without incoherence;
- first-frame performability;
- dynamic generation stability;
- edit usability;
- character/identity continuity;
- regeneration count;
- manual intervention count;
- production time/burden;
- Runtime compatibility;
- zero-context reproducibility;
- hidden chat-memory dependence.

## Source evidence archive

Locked source revision for this experiment:

`penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`

Do not silently follow future upstream changes during this experiment. Any source update requires an explicit revision note before comparing results.
