# OSS_OPT_R2 / Lean Runtime Integration Test Plan v1

Status: `PROPOSED / NOT STARTED`  
Date: `2026-08-28`

## 1. Goal

The next round should not add another large creative feature set. Its purpose is to prove that the MV system can become materially faster and simpler while preserving the correctness learned in R3 and OSS_OPT_R1.

Primary question:

**Can we keep the same five Human Gates, same durable rollback truth and same visual quality while reducing machine-stage interaction/transport overhead by at least half?**

## 2. Branch strategy

Do not continue production on `test/mv-oss-optimization-r1` and do not merge that branch wholesale.

Observed repository topology at planning time:
- experiment branch vs stable `test/mv-web-r3`: experiment contains a very large R&D delta (hundreds of commits) and stable has two later commits not present in the experiment history;
- `test/mv-web-r3` vs default `main`: R3 contains roughly 660 commits beyond the merge base while `main` has one separate documentation/governance commit.

Recommended new branch:

`test/mv-lean-r1`

Fork it from the **latest `test/mv-web-r3`**, then selectively re-apply only approved candidates from OSS_OPT_R1.

Do not copy experimental runtime history merely to obtain a candidate feature.

## 3. Selective inputs from OSS_OPT_R1

### Promote into the next test branch

Runtime/process candidates:
- Executor-First concept;
- a compact Stage Executor Registry or equivalent controller-resolved executor payload;
- Audio Timeline P0 -> P1 -> P2 route;
- validated `run_alignment/bootstrap` correctness fixes + unit tests;
- HG01 direct-work identity guard if not already present in stable.

Creative knowledge candidates:
- Director Thesis;
- Primary Visual Engine;
- audiovisual relationship modes;
- motive-first camera-subject-space;
- WHY CUT HERE;
- optional-element stop condition;
- Creative Drift QA.

### Do not promote wholesale

- `06_TESTS/MV/OSS_OPT_R1/**` test history;
- D02-B Canonical slot history as production template;
- experiment Bridge request/response history;
- experiment runtime-executor request/retry history;
- D02-B-specific probe workflows;
- H3 10-15 second container rules;
- H3 four-panel Picture-1 rules;
- RunningHub/H3 orchestration;
- face-degrade/grid techniques as universal core behavior (keep optional/capability-specific unless separately validated).

## 4. R2 hypotheses

### H1｜Machine stages can auto-chain

Introduce a candidate controller operation conceptually equivalent to:

`RUN_UNTIL_GATE_OR_BLOCK`.

Given a valid canonical guard, the controller may execute consecutive machine-only stages, writing and validating every required artifact/transition receipt internally, and return only when:
- a Human Gate is reached;
- an external generation handoff requires user assets;
- a genuine BLOCK occurs.

No stage validation may be skipped.

### H2｜Human Gate transport can be one user action

Test an atomic external command equivalent to `ACCEPT_GATE` while preserving two-phase internal semantics:
- write gate receipt;
- refresh guard internally;
- advance after receipt validation.

### H3｜Startup can be thin

Target new-chat startup:
- no more than 2-3 initial reads/calls before Runtime identifies the slot and next executor;
- resolved executor ID / class / JIT paths returned directly by Controller;
- full Registry/MANIFEST only loaded when debugging or explicitly requested.

### H4｜S10 can disappear as a standalone operational stage

Editor Audio Gate becomes a deterministic invariant inside Edit entry:
- same locked BGM hash / duration / identity -> proceed;
- mismatch -> BLOCK and reopen audio prerequisite.

No separate user-visible or transport-visible stage is needed.

### H5｜Normalization is conditional

Only run atomization/proxy/watermark normalization when active source/context requires it.
Single-shot clean sources should not pay the full multi-shot normalization process cost.

### H6｜Natural Beat remains useful but need not be a visible stop

Natural Beat remains a derived Director input and durable artifact when useful, but generation should auto-chain from Audio Timeline into Director preparation.

## 5. Proposed macro production path

1. Start / allocate.
2. HG01 Song.
3. HG02 BGM.
4. Audio Truth -> Natural Beat -> Director -> First Frames -> HG03.
5. Dynamic Prompt -> external generation -> Dynamic QA -> conditional normalization.
6. Edit Map -> preview -> HG04.
7. Subtitle -> Final Tech -> HG05.
8. Release Package -> S16.

Publishing and post-publish review remain real-world stages outside pre-publish production.

## 6. Test asset

Use one completely new MV slot/song/world.

Requirements:
- no inherited D02-B specific visual world;
- normal production use case, not a deliberately exotic stress test;
- use the same five Human Gates;
- preferably another Lane S or P production slot so speed matters;
- Dynamic generation should use current actual Web/Seedance-class production path.

The experiment variable is **process efficiency**, not creative novelty.

## 7. Metrics and PASS thresholds

### Correctness must not regress
- Human Gates = exactly five normal fixed Gates;
- no chat-only canonical PASS;
- zero fabricated state;
- rollback still works;
- exact BGM/timeline truth preserved;
- final audio/source identity checks pass;
- S17 still requires real-world publish confirmation.

### Efficiency targets
- startup pre-action reads/calls: `<= 3`;
- normal Bridge/controller user-visible command cycles before S16: target `<= 12` excluding external generation/upload time;
- no per-song production model installation;
- no slot-specific core helper creation;
- no repeated full Registry reads at every stage;
- machine stages between Human Gates auto-run until Gate/BLOCK;
- read-only state queries should not require one content-branch commit each.

### Creative/non-regression targets
- HG03 first-frame set accepted without broad redesign, or no worse than current baseline;
- Dynamic source usable without increased regeneration burden;
- lyric visual hit remains first priority;
- HG04 edit passes without becoming more fragmented;
- HG05 final acceptance passes;
- Director OSS knowledge remains useful without adding another approval stage.

## 8. Stage-schema policy for R2

Do not immediately delete the 19-stage Canonical schema at the start of R2.

First test:

`same internal evidence granularity + compressed external execution`.

If R2 proves equivalent correctness, prepare a Stage Registry v2 proposal that may collapse/downgrade:
- S04 Natural Beat from hard stage to derived artifact;
- S09 normalization to conditional substage;
- S10 Editor Audio standalone stage into Edit invariant;
- S11 Edit Map lock + preview preparation into one macro executor;
- S13 Subtitle QA into Finish macro machine substage.

This sequencing prevents us from confusing “fewer user-visible steps” with “less evidence”.

## 9. Stable promotion plan after R2

### Phase A｜Clean integration branch

From latest `test/mv-web-r3`, create a clean promotion/test branch and selectively implement candidates in grouped commits:
1. Runtime routing / lean controller behavior;
2. Audio Timeline route + regression tests;
3. compact Director/Montage knowledge overlay;
4. startup/context simplification;
5. workflow/test consolidation.

### Phase B｜Regression

Run existing Runtime P0/P1 tests, Audio Timeline tests, publish transaction tests, revision/rollback tests and Bridge tests.

No D02-B experiment history should be required for these tests to pass.

### Phase C｜One real Lean MV

Complete one new MV to S16 under the new lean path.

### Phase D｜Stable R3 promotion

If PASS, merge/squash only the clean integration branch into `test/mv-web-r3` and write a deployment receipt.

### Phase E｜Main branch consolidation

Do not directly merge the current experiment branch or the whole historical test tree into `main`.

At planning time, `main` contains one separate governance/documentation line (`README`, `LICENSE`, `CONTRIBUTING`, `MAINTAINERS`, `ROADMAP`, deployment instructions) while R3 has a large production history delta.

Recommended main-line consolidation:
1. create `release/mv-runtime-v1` from latest `main`;
2. bring the latest approved stable R3 system into that release branch using a reviewed merge/squash strategy;
3. preserve the main-only governance/documentation commit;
4. exclude test runtime logs and experimental slot histories from the release surface where they are not required;
5. run full regressions on the release branch;
6. after two consecutive real MV passes on the promoted stable runtime, merge `release/mv-runtime-v1` to `main` and tag a version such as `mv-runtime-v1.0`.

After this point:
- `main` = stable product/runtime truth;
- `test/mv-*` = bounded experiment branches;
- promotion always goes through a clean `promote/` or `release/` branch, never experiment-branch wholesale merge.

## 10. Workflow consolidation candidate

R2 should also test reducing permanent GitHub Actions workflow count.

Target:
- one Audio Timeline regression suite;
- one reusable/on-demand Audio Timeline execution workflow (optionally a separate controlled environment-preheat workflow);
- Runtime regression suites remain grouped by functional risk rather than per-song/per-probe;
- no D02-B-specific workflow survives as stable infrastructure.

## 11. R2 PASS definition

`OSS_OPT_R2 / LEAN_RUNTIME_R1 = PASS` only if:
- one real new MV reaches S16;
- all five Human Gates remain authoritative;
- no correctness or rollback regression;
- controller/user-visible cycles are materially reduced;
- startup context is materially smaller;
- no unnecessary new model/tool route is created;
- final visual quality is not worse;
- branch diff is clean enough to promote without importing experiment history.

If quality stays good but efficiency does not improve, R2 fails its purpose.
If efficiency improves by bypassing evidence/Gates, R2 also fails.
