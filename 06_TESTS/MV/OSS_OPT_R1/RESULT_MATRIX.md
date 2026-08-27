# OSS MV Optimization Result Matrix v1.4

Status: `IN_PROGRESS / SIMPLE LYRIC TIMELINE CORRECTION ACTIVE`

## Test identity

- Experiment branch: `test/mv-oss-optimization-r1`
- Runtime baseline fork SHA: `89852ec5314e7579853683ef5eb40adb09f25753`
- Test MV slot: `D02-B / Lane S`
- HG01 song family: `有几次想你了 / LOCKED`
- HG02 BGM: `B variant / exact Douyin music object 7670104695834282815 / 0.8s soft tail fade / LOCKED`
- Canonical Runtime state: `S02_HG02_BGM_LOCKED / BGM_LOCKED`
- External source: `penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`
- Optimization set: Director Thesis / Primary Visual Engine / audiovisual relationship / motive-first camera-subject-space / WHY CUT HERE / optional-element stop condition / Creative Drift QA

## A/B comparison

| Dimension | Baseline Runtime | Runtime + OSS Overlay | Delta | Evidence |
|---|---:|---:|---:|---|
| Lyric visual hit | TBD | TBD | TBD | Director A/B not started |
| Director / camera quality | TBD | TBD | TBD | Director A/B not started |
| Shot diversity | TBD | TBD | TBD | TBD |
| Visual coherence | TBD | TBD | TBD | TBD |
| First-frame performability | TBD | TBD | TBD | TBD |
| Dynamic stability | TBD | TBD | TBD | TBD |
| Character / identity continuity | TBD | TBD | TBD | TBD |
| Edit-source usability | TBD | TBD | TBD | TBD |
| Regeneration count | TBD | TBD | TBD | TBD |
| Manual intervention count | TBD | TBD | TBD | TBD |
| Production time / burden | TBD | TBD | TBD | TBD |
| Runtime compatibility | Baseline | TBD | TBD | Executor-first process audit added before creative A/B |
| Zero-context reproducibility | Baseline | Improved process routing | Positive | 19/19 executor registry CI PASS |

## Gate-by-gate findings

### HG01 / Song

`PROCESS CORRECTION / VALIDATED IN EXPERIMENT`

Accepted strategy:
`CORE BENCHMARK ACCOUNTS -> DATA CENTER -> SONG_FAMILY REPEAT/VALUE RANKING -> SIMPLE DIRECT MV HANDOFF -> USER HG01`

Retained hardening:
`DELIVERED URL MUST OPEN THE CITED MV ITSELF`.

Rejected behavior:
`WEB-WIDE SEARCH -> CANDIDATES CHOSEN BY PUBLIC EVIDENCE AVAILABILITY -> HEAVY EVIDENCE TAXONOMY`.

HG01 is locked to `有几次想你了`.

### HG02 / BGM

`PASS / LOCKED`

Two core works resolved to the same Douyin music object `7670104695834282815`. User accepted the B listening variant: same exact source, final `0.8s` soft fade-out.

### Audio Timeline / Natural Beat

`CORRECTION REQUIRED / S03 NOT ALLOWED YET`

Two separate process defects were exposed before S03 advance.

#### Defect A｜Executor discovery gap

The agent initially rebuilt tooling even though the repository already contained a canonical, pinned, regression-tested `tools/mv_audio_timeline/*` toolchain.

Remediation already completed:
- `runtime/mv_stage_executor_registry.json` with 19/19 stage coverage;
- `rules/mv_executor_first.md`;
- startup/JIT now loads executor routing before new implementation;
- per-slot model install and slot-specific core helpers are rejected by default.

Classification:
- `EXECUTOR-DISCOVERY-GAP` -> `PROMOTE_RUNTIME` candidate
- `SLOT-SPECIFIC-CORE-HELPER` -> `REJECT`
- `PER-SLOT-PRODUCTION-MODEL-INSTALL` -> `REJECT AS DEFAULT`

#### Defect B｜Partial caption was mistaken for complete lyrics

The first D02-B trusted lyric set contained only four lines because it was copied from a creator work caption. The locked BGM contains more sung lines; therefore the four-line transcript and all forced-alignment candidates derived from it are INVALID regardless of their timing accuracy.

Key lesson:
`creator caption / description / hashtag / lyric quote != complete lyric truth`.

The full locked audio clip is the authority for completeness.

#### Accepted simplified S02 path

A new experiment rule is now active:
`04_HARNESS/rules/mv_lyric_timeline_simple_path.md`

Normal production Happy Path is fixed to:

`HG02 exact BGM`
→ `verify audio SHA`
→ `ONE full-clip ASR transcript`
→ `ONE lyric-text audit against the same audio`
→ `trusted_lyrics locked`
→ `ONE Xingyu forced alignment`
→ `ONE automatic timing QA`
→ `line_timeline.csv + lyrics_exact.srt`
→ `S03`

Normal PASS path explicitly forbids:
- second-model cross-check by default;
- Web-wide lyric evidence hunting;
- using waveform/BPM as lyric truth;
- per-song tooling branches;
- repeating evidence collection after the single lyric-text audit passes.

Only a concrete QA failure opens an exception path, and the same path is rerun after correcting that specific issue.

#### Minimal lyric-timeline lock assets

Required to lock:
1. `audio_identity.json`
2. `trusted_lyrics.txt`
3. `raw_evidence/xingyu/alignment.json`
4. `line_timeline.csv`
5. `lyrics_exact.srt`
6. `lyric_timeline_qa.json`
7. `package_manifest.json`

`anchor_words.csv` and `music_events.csv` move downstream to Natural Beat / Director enrichment and do not block lyric-timeline lock in this experiment.

Current D02-B status:
- HG01 PASS
- HG02 PASS
- previous 4-line lyric set = INVALID
- previous 4-line timing candidates = INVALID
- Canonical Runtime stays at `S02_HG02_BGM_LOCKED`
- next action = rebuild complete lyric text from the full locked BGM using the single Simple Path

Classification:
- `PARTIAL-CAPTION-AS-LYRIC-TRUTH` -> `REJECT`
- `SINGLE-PATH-LYRIC-TIMELINE` -> `PROMOTE_RULE` candidate pending D02-B validation
- `MULTI-SOURCE-BY-DEFAULT-LYRIC-QA` -> `REJECT`
- `ANCHOR-MUSIC-EVENTS-BLOCK-S03` -> `REJECT IN SIMPLE PATH`

### Director

TBD. First major stage where `mvmaker-h3-skills` creative overlay is intentionally allowed.

### HG03 / First Frames
TBD

### Dynamic / Dynamic QA
TBD

### Normalization / Edit
TBD

### HG04 / Picture Edit
TBD

### Subtitle / Final QA
TBD

### HG05 / Final Acceptance
TBD

## Complexity audit

Target behavior after current corrections:

- one normal lyric transcript path;
- one text audit;
- one forced alignment;
- one automatic timing QA;
- no default second source/model;
- no caption-as-complete-lyrics shortcut;
- no Anchor/Music Event work before lyric timing is locked;
- no repeated production-model installation per song;
- no slot-specific helper in core Runtime.

## Final decisions

| Optimization ID | Decision | Reason | Promotion target / next action |
|---|---|---|---|
| CORE-DATABASE-HG01-RESTORE | `PROMOTE_RULE` candidate | Restores proven R3 candidate authority and reduces unnecessary search/context | retain |
| DIRECT-LINK-IDENTITY-GUARD | `PROMOTE_RULE` candidate | Prevents incorrect MV handoff without changing discovery authority | retain |
| WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY | `REJECT` | Evidence availability started driving song choice | do not promote |
| EXECUTOR-DISCOVERY-GAP | `PROMOTE_RUNTIME` candidate | Runtime previously defined WHAT but did not reliably route HOW | validate through remainder of D02-B |
| SLOT-SPECIFIC-CORE-HELPER | `REJECT` | Duplicates canonical paths and increases maintenance | keep history only |
| PER-SLOT-PRODUCTION-MODEL-INSTALL | `REJECT AS DEFAULT` | Normal behavior is doctor/cache/reuse | environment setup only when genuinely missing |
| PARTIAL-CAPTION-AS-LYRIC-TRUTH | `REJECT` | Caption can be a lyric excerpt rather than the complete locked clip | never use as completeness authority |
| SINGLE-PATH-LYRIC-TIMELINE | `PROMOTE_RULE` candidate | Matches user goal: simple, stable, accurate lyric text + timing | validate on D02-B before stable promotion |
| MULTI-SOURCE-BY-DEFAULT-LYRIC-QA | `REJECT` | Adds time/tokens without a concrete failure signal | exception only |
| ANCHOR-MUSIC-EVENTS-BLOCK-S03 | `REJECT IN SIMPLE PATH` | These belong to downstream Director/Beat enrichment, not lyric truth | move downstream |
| OSS-VISUAL-OVERLAY | `KEEP_EXPERIMENTAL` | Creative A/B not yet started | begin after lyric timeline PASS |

## Current experiment verdict

The process is now deliberately simplified around the production goal: accurate complete lyrics and accurate timing from one locked audio. D02-B remains safely at S02. The previous four-line result is invalid and will not be promoted. The next valid action is one full-clip lyric transcript, one lyric-text audit, one Xingyu forced alignment, and one automatic QA.
