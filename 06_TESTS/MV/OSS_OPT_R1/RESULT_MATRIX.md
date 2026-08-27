# OSS MV Optimization Result Matrix v1.1

Status: `IN_PROGRESS / UPSTREAM_RUNTIME_CORRECTNESS_HARDENED`

## Test identity

- Experiment branch: `test/mv-oss-optimization-r1`
- Runtime baseline fork SHA: `89852ec5314e7579853683ef5eb40adb09f25753`
- Test MV slot: `D02-B`
- Song / audio identity: `NOT LOCKED — HG01 EVIDENCE REPACK IN PROGRESS`
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

`RUNTIME CORRECTNESS FINDING / VALIDATED`

Before visual OSS testing began, D02-B exposed a pre-existing Runtime delivery weakness: machine `SONG_CANDIDATE_SET` could be mistaken for user-facing HG01 evidence delivery. The initial D02-B assistant handoff therefore prematurely asked for A/B/C/D selection without first providing a valid Direct Douyin Evidence Pack.

A second evidence-quality defect was also found: some URLs described as direct evidence were actually older landing works whose pages listed a newer relevant post. These are now classified as `DISCOVERY_ONLY`, not Direct Work Evidence.

Hardening result:

- current D02-B demoted to `HG01_PREFLIGHT_PREPARED / AWAITING_EVIDENCE_REPACK`;
- `HG01_CANDIDATE_EVIDENCE_PACK` registered as an independent Canonical artifact;
- HG01 `RECORD_HUMAN_GATE` requires both candidate set + evidence pack;
- canonical S01 transition also requires both artifacts plus user receipt;
- landing-work identity rule added;
- new-chat startup guard added;
- dedicated CI completed real negative + positive Runtime path.

Validation:

- Workflow: `R3 HG01 Delivery Guard Tests`
- Run: `33036864308`
- Head: `233f7df2dd2a272b2bb390ff116d4f4d0ffa2721`
- Result: `PASS`
- Real positive fixture path: `RECORD_HUMAN_GATE -> ADVANCE -> VERIFY_STATE`

Classification:

`PROMOTE_RUNTIME_CANDIDATE / HG01 DELIVERY GUARD`

This is Runtime correctness, not evidence of OSS visual improvement.

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

Record whether each benefit required extra:

- context volume;
- prompt complexity;
- code/config maintenance;
- manual Gate work;
- regeneration cycles;
- model-specific assumptions;
- external dependencies.

An optimization that improves one visual sample but substantially harms reproducibility or maintenance is not automatically a net improvement.

Current HG01 hardening complexity assessment:

- context volume: `LOW` — short JIT rule addition;
- prompt complexity: `LOW`;
- code/config maintenance: `LOW-MEDIUM` — 1 new canonical artifact and one dedicated CI workflow;
- manual Gate work: `NO INCREASE` — still one HG01 user decision;
- external dependency: `NONE ADDED`;
- reproducibility: `IMPROVED`;
- failure containment: `IMPROVED`.

## Final decisions

| Optimization ID | Decision | Reason | Promotion target / next action |
|---|---|---|---|
| HG01-DELIVERY-GUARD | `PROMOTE_RUNTIME` candidate | Prevents machine preflight from masquerading as user evidence delivery; CI validated negative and positive canonical paths | Separate explicit audited promotion to stable Runtime after experiment-line review |
| OSS-VISUAL-OVERLAY | TBD | External source not yet locked | Continue after upstream song/audio truth is locked |

Allowed decisions:

- `PROMOTE_RUNTIME`
- `PROMOTE_RULE`
- `PROMOTE_KNOWLEDGE`
- `PROMOTE_TOOLING`
- `KEEP_EXPERIMENTAL`
- `REJECT`

## Final experiment verdict

Not yet available. HG01 Runtime correctness hardening is independently validated; OSS visual optimization comparison has not begun because source integration is still pending and D02-B has not yet passed HG01/HG02.
