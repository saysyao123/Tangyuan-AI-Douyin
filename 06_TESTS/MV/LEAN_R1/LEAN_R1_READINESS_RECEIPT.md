# LEAN_R1｜Readiness Receipt v1

Status: `READY_FOR_REAL_HG01 / D03-A`
Date: `2026-08-28`
Branch: `test/mv-lean-r1`
Clean baseline: latest `test/mv-web-r3` at branch creation (`bea684ad8844a9ee3a3219fcf81fe115f2f7c28f`)

## 1. Scope completed

Lean R1 setup is complete enough to begin the next real MV without importing OSS_OPT_R1 wholesale.

Selectively installed/tested layers:
- Lean macro Runtime contract;
- one active Lean Runtime Bridge implementation and one active workflow;
- compact Stage Executor Registry;
- Executor-First admission rule;
- Audio Timeline priority route P0 -> P1 -> P2;
- reusable P1 `lightweight_align.py` registered under S02;
- bounded Director Lean Overlay;
- real-MV Lean test contract;
- zero-context D03-A new-chat start prompt.

## 2. Duplicate cleanup

Only the proven Lean controller path is retained:
- tool: `04_HARNESS/tools/mv_runtime_lean_bridge.py`;
- workflow: `.github/workflows/r3-mv-lean-runtime-web-bridge.yml`.

A later duplicate helper/workflow pair was removed before production use. Lean R1 must keep one control entrypoint for this experiment.

## 3. Tracker / slot truth

- D02-A already has canonical state and is not free; it remains a separate existing project.
- D02-B is marked `RELEASE_READY` in this Lean branch with song/audio identity so it cannot be allocated again; it is not marked PUBLISHED.
- D03-A / Lane P is the Lean R1 real-MV slot.

## 4. D03-A allocation and initialization proof

Read-only allocation RESUME:
- request: `LR-20260828T080100Z-D03ASTART`;
- result: `ALLOCATE_NEW_SLOT / D03-A / Lane P`;
- resolved executor: `HG01_CORE_DATABASE_ORCHESTRATION`.

INIT:
- request: `LR-20260828T080200Z-D03AINIT`;
- result: PASS;
- canonical state: `S00_SLOT_CREATED / SLOT_CREATED`;
- transition receipt: `00_STATE/TRANSITIONS/000_INIT__S00_SLOT_CREATED.json`.

## 5. Macro safety proof

Request `LR-20260828T080300Z-D03AGATESTOP` executed `RUN_UNTIL_GATE_OR_BLOCK` at S00.

Result:
- outcome: `HUMAN_GATE`;
- Human Gate: `HG01`;
- stop stage: `S00_SLOT_CREATED`;
- attempted next stage: `S01_HG01_SONG_LOCKED`;
- transitions advanced: `0`.

This proves the macro does not cross a Human Gate merely to reduce interaction count.

## 6. Final regression after cleanup

Final read-only request: `LR-20260827T180500Z-D03AFINAL`.

Result:
- status: EXECUTED;
- mode: `RESUME_CANONICAL`;
- slot/lane: `D03-A / P`;
- current stage: `S00_SLOT_CREATED`;
- transition sequence: `0`;
- next action: `PREPARE_HG01_SONG_SELECTION`;
- Human Gate: `HG01`;
- resolved executor: `HG01_CORE_DATABASE_ORCHESTRATION / DATA_ORCHESTRATION`;
- state/revision/asset/tracker verification: PASS;
- no transition occurred during the final regression.

## 7. Next real action

The next action is not another Runtime redesign and not another initialization.

It is:
`D03-A HG01 machine preflight -> Core Benchmark Data Center candidate preparation -> Human song-aesthetic decision`.

No D02-B visual world is inherited. The selected song and visual world must be new.

## 8. Experiment boundary

This remains `Candidate Runtime / Lean R1 test chain`.
Do not merge the branch wholesale to stable R3 or `main` before:
1. one real D03-A MV reaches S16;
2. Lean efficiency metrics are measured;
3. correctness/rollback regressions pass;
4. a clean promotion diff and deployment receipt are produced.
