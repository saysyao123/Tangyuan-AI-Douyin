# OSS MV Optimization Result Matrix v1.2

Status: `IN_PROGRESS / HG01 CORE DATABASE STRATEGY RESTORED`

## Test identity

- Experiment branch: `test/mv-oss-optimization-r1`
- Runtime baseline fork SHA: `89852ec5314e7579853683ef5eb40adb09f25753`
- Test MV slot: `D02-B`
- Song / audio identity: `NOT LOCKED — HG01 CORE DATABASE REBUILD REQUIRED`
- External source commit: `TBD / PENDING USER SOURCE`
- Optimization set: `TBD`

## A/B comparison

| Dimension | Baseline Runtime | Runtime + OSS Overlay | Delta | Evidence |
|---|---:|---:|---:|---|
| Lyric visual hit | TBD | TBD | TBD | TBD |
| Director / camera quality | TBD | TBD | TBD | TBD |
| Shot diversity | TBD | TBD | TBD | TBD |
| Visual coherence | TBD | TBD | TBD | TBD |
| First-frame performability | TBD | TBD | TBD | TBD |
| Dynamic stability | TBD | TBD | TBD | TBD |
| Character / identity continuity | TBD | TBD | TBD | TBD |
| Edit-source usability | TBD | TBD | TBD | TBD |
| Regeneration count | TBD | TBD | TBD | TBD |
| Manual intervention count | TBD | TBD | TBD | TBD |
| Production time / burden | TBD | TBD | TBD | TBD |
| Runtime compatibility | TBD | TBD | TBD | TBD |
| Zero-context reproducibility | TBD | TBD | TBD | TBD |

## Gate-by-gate findings

### HG01 / Song

`PROCESS CORRECTION / VALIDATED IN EXPERIMENT`

D02-B revealed two different issues:

1. a real link-integrity bug: some supposed direct evidence URLs opened an older creator work whose page merely listed the desired newer song MV;
2. an over-correction: while fixing that bug, candidate discovery drifted from the original R3 core-benchmark Data Center strategy into broad public-Web song search.

User decision on 2026-08-27:

- restore the original simple R3 strategy;
- update/read the previously supplied core comparison accounts into a database;
- select songs from that database;
- add useful supplemental accounts when appropriate;
- deliver the selected songs directly as the corresponding bloggers' corresponding MV videos;
- do not perform broad song search as the default path.

Restored path:

`CORE BENCHMARK ACCOUNTS -> DATA CENTER -> SONG_FAMILY REPEAT/VALUE RANKING -> SIMPLE DIRECT MV HANDOFF -> USER HG01`

Retained hardening:

`DELIVERED URL MUST OPEN THE CITED MV ITSELF`

Rejected experiment behavior:

`WEB-WIDE SEARCH -> CANDIDATES CHOSEN BY PUBLIC EVIDENCE AVAILABILITY -> HEAVY EVIDENCE TAXONOMY`

Current D02-B action:

`HG01_CORE_DATABASE_REBUILD_REQUIRED`

The temporary Web-driven formal candidate set (`雨后轻风有香 / 甲乙丙丁 / 差一步美满`) has been superseded as a Human Gate packet. No HG01 user receipt existed, so Canonical state remains S00 and no rollback was required.

Files corrected:

- `04_HARNESS/rules/mv_human_gates.md`
- `04_HARNESS/rules/mv_stage_entry_checklist.md`
- `06_TESTS/MV/OSS_OPT_R1/HG01_GATE_HARDENING_v1.md`
- `06_TESTS/MV/OSS_OPT_R1/NEW_CHAT_START_PROMPT.md`
- `06_TESTS/MV/WEB_R3/30D_60/D02-B/01_SONG/SONG_CANDIDATE_SET.json`
- `06_TESTS/MV/WEB_R3/30D_60/D02-B/01_SONG/HG01_CANDIDATE_EVIDENCE_PACK_v1.md`
- `.github/workflows/r3-hg01-delivery-guard-tests.yml`

Classification:

- `CORE-DATABASE-HG01-RESTORE` -> `PROMOTE_RULE` candidate
- `DIRECT-LINK-IDENTITY-GUARD` -> `PROMOTE_RULE` candidate
- `WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY` -> `REJECT`

### HG02 / BGM
TBD

### Audio Timeline / Natural Beat
TBD

### Director
TBD

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

Current HG01 correction assessment:

- context volume: `REDUCED`;
- prompt complexity: `REDUCED`;
- code/config maintenance: `LOW`;
- manual Gate work: `REDUCED TO ORIGINAL R3 BEHAVIOR`;
- external dependency: `NO NEW DEPENDENCY`;
- candidate quality authority: `IMPROVED — returns to monitored core accounts`;
- link correctness: `RETAINED`;
- broad web search burden: `REMOVED AS DEFAULT`;
- reproducibility: `IMPROVED` because discovery authority is a durable database rather than ad-hoc search results.

## Final decisions

| Optimization ID | Decision | Reason | Promotion target / next action |
|---|---|---|---|
| CORE-DATABASE-HG01-RESTORE | `PROMOTE_RULE` candidate | Restores the proven R3 selection authority and reduces unnecessary search/context burden | Continue D02-B with core Data Center rebuild; stable promotion only after experiment review |
| DIRECT-LINK-IDENTITY-GUARD | `PROMOTE_RULE` candidate | Prevents incorrect MV handoff without changing song-discovery authority | Keep as minimal HG01 delivery correctness check |
| WEB-WIDE-EVIDENCE-DRIVEN-DISCOVERY | `REJECT` | Evidence availability started driving song selection and made HG01 heavier than the original R3 process | Do not promote |
| OSS-VISUAL-OVERLAY | TBD | External source not yet locked | Continue after upstream song/audio truth is locked |

Allowed decisions:

- `PROMOTE_RUNTIME`
- `PROMOTE_RULE`
- `PROMOTE_KNOWLEDGE`
- `PROMOTE_TOOLING`
- `KEEP_EXPERIMENTAL`
- `REJECT`

## Final experiment verdict

Not yet available. HG01 has been corrected back to the original R3 core-database selection strategy with only the direct-link identity guard retained. OSS visual optimization comparison has not begun because source integration is still pending and D02-B has not yet passed HG01/HG02.
