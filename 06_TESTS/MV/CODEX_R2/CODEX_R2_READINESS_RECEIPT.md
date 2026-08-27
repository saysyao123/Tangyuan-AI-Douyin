# CODEX R2｜Readiness Receipt v1.0

Status: `READY_FOR_REAL_CODEX_RUN`
Date: `2026-08-28`
Branch: `test/mv-codex-r2`
Baseline: `test/mv-lean-r1 @ 6a02cff5be943488800f0d63bb2f91ef4f3cbd32`
Target: `D03-B / Lane S`

## 1. Adapter scope

Codex R2 is a Codex-native adapter/test layer over the existing Canonical/Lean MV Runtime. It does not define a second production state machine.

Installed branch-local adapter assets:
- root `AGENTS.md` repository instructions;
- `06_TESTS/MV/AGENTS.md` MV-specific instructions;
- machine-readable `CODEX_R2_TEST_CONTRACT.json`;
- `CODEX_EXECUTION_CONTRACT.md`;
- `CODEX_HANDOFF_PROTOCOL.md`;
- `CODEX_TEST_MATRIX.md`;
- `RESULT_REPORT_TEMPLATE.md`;
- short zero-context `CODEX_START_PROMPT.md`;
- local `scripts/codex_mv_operator.py`;
- compatibility update to root `CODEX_DEPLOY_INSTRUCTIONS.md`.

## 2. Transport decision

Default Codex transport is local controller execution:
`python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py ...`

The operator reuses:
- `04_HARNESS/tools/mv_runtime_bridge.py`;
- `04_HARNESS/tools/mv_runtime_lean_bridge.py`;
- `04_HARNESS/tools/mv_runtime_state.py`;
- current Runtime registries/validators/receipts.

ChatGPT Web's immutable request -> Actions -> response bridge remains available in the repository but is not the default Codex transport.

## 3. Historical branch handling

Existing historical branch `test/mv-codex-r1` was not overwritten. It represents the earlier Golden-Reproduction C00-C08 experiment and remains reference-only.

Codex R2 was created fresh from current Lean R1 so it includes the current Runtime, fast Audio Timeline route, Executor-First registry and Director Lean Overlay.

## 4. Target-slot isolation

- D03-A is inherited active state from Lean R1 and is NOT the Codex R2 target.
- D03-B is the explicit Codex R2 slot.
- Before the real Codex run, D03-B has no Canonical `00_STATE/CURRENT_STATE.json`.
- Tracker truth identifies D03-B as Lane S / PLANNED.
- Every Codex Runtime command must use explicit `--slot D03-B`.

## 5. CI verification

Registered workflow used:
`.github/workflows/mv-audio-timeline-gate-tests.yml`

Verification run:
- run id: `33102443394`;
- branch: `test/mv-codex-r2`;
- head: `691de1f67f8dc8f3033e0fa6148663cdbd587253`;
- conclusion: `success`.

Successful steps:
1. checkout;
2. Python 3.11 setup;
3. ffmpeg/ffprobe environment;
4. Python syntax compile for current Audio Timeline tools, Canonical/Lean Runtime controllers and `codex_mv_operator.py`;
5. timing-core regression suite;
6. complete-package gate regression suite;
7. Codex R2 read-only preflight + `resume --slot D03-B` smoke;
8. no-worktree-mutation checks.

The smoke assertions proved:
- preflight is not BLOCKED;
- `resume --slot D03-B` returns `ALLOCATE_NEW_SLOT`;
- selected slot is `D03-B`;
- lane is `S`;
- resolved executor is `HG01_CORE_DATABASE_ORCHESTRATION`;
- guard kind is `ALLOCATION`;
- read-only commands do not create D03-B Canonical state;
- read-only commands leave git diff clean.

## 6. CI cleanup

A newly introduced standalone `codex-r2-smoke.yml` did not register/trigger reliably when first created on the non-default test branch. It was removed rather than keeping duplicate CI definitions.

The Codex smoke was folded into the already registered Audio Timeline regression workflow on this Codex-only branch. One proven CI path remains.

## 7. Real Codex run boundary

D03-B has intentionally NOT been initialized by this setup process.

The real Codex test must itself perform:
1. `preflight`;
2. fresh `resume --slot D03-B`;
3. valid `init --slot D03-B` from the fresh allocation truth;
4. HG01 machine preflight;
5. user song decision;
6. the real Canonical workflow onward.

This preserves initialization as part of the Codex automation test instead of pre-solving it here.

## 8. Ready-state conclusion

Codex R2 adapter readiness: `PASS`.

What is proven now:
- branch isolation;
- Codex-native instruction hierarchy;
- local operator syntax/import compatibility;
- reuse of existing Canonical/Lean controllers;
- existing Audio Timeline regressions remain green;
- D03-B read-only allocation/resume path is correct and non-mutating.

What is NOT yet proven and must be measured by the real Codex run:
- real INIT transaction;
- Human Gate accept transaction under Codex;
- end-to-end artifact production through S16;
- external image/video handoff quality;
- Codex efficiency and autonomy metrics;
- final creative quality versus the accepted Tangyuan MV baseline.

Next action: open Codex on `test/mv-codex-r2` and send the contents of `06_TESTS/MV/CODEX_R2/CODEX_START_PROMPT.md`.