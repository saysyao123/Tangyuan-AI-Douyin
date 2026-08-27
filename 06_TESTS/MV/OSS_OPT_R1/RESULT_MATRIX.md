# OSS MV Optimization Result Matrix v1.3

Status: `IN_PROGRESS / EXECUTOR-FIRST REMEDIATION PASS`

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

D02-B exposed a real link-integrity bug and an over-correction. The final accepted strategy is restored to:

`CORE BENCHMARK ACCOUNTS -> DATA CENTER -> SONG_FAMILY REPEAT/VALUE RANKING -> SIMPLE DIRECT MV HANDOFF -> USER HG01`

Retained hardening:
`DELIVERED URL MUST OPEN THE CITED MV ITSELF`.

Rejected behavior:
`WEB-WIDE SEARCH -> CANDIDATES CHOSEN BY PUBLIC EVIDENCE AVAILABILITY -> HEAVY EVIDENCE TAXONOMY`.

HG01 is now locked to `有几次想你了`.

Classification:
- `CORE-DATABASE-HG01-RESTORE` -> `PROMOTE_RULE` candidate
- `DIRECT-LINK-IDENTITY-GUARD` -> `PROMOTE_RULE` candidate
- `WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY` -> `REJECT`

### HG02 / BGM

`PASS / LOCKED`

Two core works resolved to the same Douyin music object `7670104695834282815`. User accepted the B listening variant: same exact source, final `0.8s` soft fade-out.

No Director work started before the BGM lock.

### Audio Timeline / Natural Beat

`PROCESS DEFECT FOUND BEFORE S03 ADVANCE`

Failure observed:
- Agent read the Audio Timeline Rule;
- saw Xingyu as an allowed implementation;
- started a slot-specific helper / Actions execution route;
- only afterwards rediscovered that the repository already contained a canonical, pinned, regression-tested `tools/mv_audio_timeline/*` toolchain.

This was an execution-routing failure, not a missing R3 implementation.

Root cause:
- `SKILL.md + MANIFEST.md` had executor detail;
- the newer Canonical Runtime startup/JIT path did not make executor discovery first-class;
- S02 RESUME previously surfaced only `rules/mv_audio_timeline.md`.

Remediation:
- added `runtime/mv_stage_executor_registry.json` with 19/19 stage coverage;
- added hard `rules/mv_executor_first.md`;
- upgraded SKILL/MANIFEST/Stage Entry Checklist/new-chat prompts;
- upgraded `mv_resume_contract.json` so startup loads the executor layer and S02 JIT explicitly points to the existing Audio Timeline toolchain;
- restored Runtime Web Bridge purity;
- removed slot-specific helpers/workflow from core;
- removed non-authoritative partial S03 files from current Canonical tree;
- left Git history/audit receipt as durable evidence;
- kept D02-B at S02.

Post-remediation read-only RESUME confirms:
- `current_stage = S02_HG02_BGM_LOCKED`;
- `current_state_token = BGM_LOCKED`;
- S02 JIT now includes package template, Audio Timeline README, runtime lock, `package_tool.py`, and `final_gate.py`;
- startup now includes Executor Registry, Executor-First Rule and MANIFEST.

CI:
`R3 MV Executor-First Tests` -> PASS, validating 19/19 stage mappings and key S02/S16/Runtime-Bridge regressions.

Classification:
- `EXECUTOR-DISCOVERY-GAP` -> `PROMOTE_RUNTIME` candidate
- `SLOT-SPECIFIC-CORE-HELPER` -> `REJECT`
- `PER-SLOT-PRODUCTION-MODEL-INSTALL` -> `REJECT AS DEFAULT`

### Director

TBD. This is the first major stage where the locked `mvmaker-h3-skills` creative overlay is intentionally allowed.

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

## End-to-end executor audit summary

All Canonical stages S00-S18 now have an explicit execution class. Important distinction:

- some stages use a real canonical toolchain (`S02`, `S09`, `S16`);
- some stages are deterministic media transforms (`S08`, `S11`, `S12`, `S13`);
- some are creative synthesis (`S03`, `S04`, `S06`, `S10`, `S15`);
- some are external product capability handoffs (`S05`, `S07`);
- Human Gates remain Runtime-controlled (`S14` and earlier Gate stages);
- missing repo-local code in a creative/capability stage is not an implementation gap.

Full audit:
`06_TESTS/MV/OSS_OPT_R1/PROCESS_AUDIT/END_TO_END_EXECUTION_AUDIT_v1.md`

## Complexity audit

Executor-first remediation expected effect:

- unnecessary repository search: `DOWN`;
- ad-hoc helper creation: `HARD-BLOCKED BEFORE EXECUTOR CHECK`;
- repeated model download risk: `DOWN / DEFAULT FORBIDDEN`;
- Runtime Bridge complexity: `RESTORED TO TRANSPORT-ONLY`;
- context/token use: `MORE TARGETED` because the Stage executor points to the smallest known production path;
- zero-context recovery: `IMPROVED`;
- experimentation contamination risk: `REDUCED` through stage allowlist.

## Final decisions

| Optimization ID | Decision | Reason | Promotion target / next action |
|---|---|---|---|
| CORE-DATABASE-HG01-RESTORE | `PROMOTE_RULE` candidate | Restores proven R3 candidate authority and reduces unnecessary search/context | retain through full experiment |
| DIRECT-LINK-IDENTITY-GUARD | `PROMOTE_RULE` candidate | Prevents incorrect MV handoff without changing discovery authority | retain |
| WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY | `REJECT` | Evidence availability started driving song choice | do not promote |
| EXECUTOR-DISCOVERY-GAP | `PROMOTE_RUNTIME` candidate | Runtime previously defined WHAT but did not reliably route HOW, causing duplicated implementation | validate through remainder of D02-B before stable promotion |
| SLOT-SPECIFIC-CORE-HELPER | `REJECT` | Pollutes core tools and duplicates canonical paths | keep experiment history only |
| PER-SLOT-PRODUCTION-MODEL-INSTALL | `REJECT AS DEFAULT` | Production dependency is already pinned; normal behavior is doctor/cache/reuse | setup only as a separate controlled environment action when genuinely missing |
| OSS-VISUAL-OVERLAY | `KEEP_EXPERIMENTAL` | Source locked; creative A/B not yet started | begin only after canonical Audio Timeline PASS |

Allowed decisions:
- `PROMOTE_RUNTIME`
- `PROMOTE_RULE`
- `PROMOTE_KNOWLEDGE`
- `PROMOTE_TOOLING`
- `KEEP_EXPERIMENTAL`
- `REJECT`

## Current experiment verdict

Process architecture is now corrected and machine-tested on the experiment branch. D02-B remains safely at S02; the next valid action is to build Audio Timeline using the already-existing canonical toolchain. The actual `mvmaker-h3-skills` visual A/B has not started yet.
