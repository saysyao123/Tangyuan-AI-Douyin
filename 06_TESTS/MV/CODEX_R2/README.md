# CODEX R2｜Current Canonical MV Reuse Test

## What this is

`CODEX_R2` is the Codex-native adapter/test layer for the current Tangyuan Music MV system.

It is intentionally different from historical `CODEX_R1`:

- CODEX_R1 built its own C00-C08 reproduction state chain around an old Golden Sample.
- CODEX_R2 uses the current Canonical S00-S18 Runtime directly.
- CODEX_R2 tests a fresh real MV, not a predetermined edit reconstruction.
- CODEX_R2 reuses Lean R1's Executor-First, fast audio route and Director overlay.
- CODEX_R2 replaces Web transport with a local Codex operator while preserving the same state/receipt/validator authority.

## Branch / target

- Branch: `test/mv-codex-r2`
- Baseline: `test/mv-lean-r1 @ 6a02cff5be943488800f0d63bb2f91ef4f3cbd32`
- Target: `D03-B / Lane S`
- Target finish: `S16_RELEASE_PACKAGE_READY`

The inherited D03-A slot belongs to the Lean R1 Web test. Codex R2 must always specify D03-B explicitly.

## Read order

Codex automatically receives repository `AGENTS.md` instructions. Manual startup should only add:

1. `CODEX_EXECUTION_CONTRACT.md`
2. `CODEX_TEST_MATRIX.md`
3. local operator `preflight` + `resume` output

Everything else is JIT.

## Key files

- `CODEX_START_PROMPT.md` — short zero-context user prompt.
- `CODEX_EXECUTION_CONTRACT.md` — exact operating loop.
- `CODEX_HANDOFF_PROTOCOL.md` — external image/video/auth/browser boundary.
- `CODEX_TEST_MATRIX.md` — success/failure metrics.
- `RESULT_REPORT_TEMPLATE.md` — required final report.
- `CODEX_R2_TEST_CONTRACT.json` — machine-readable branch/slot/runtime contract.
- `scripts/codex_mv_operator.py` — Codex-local facade over existing Canonical/Lean controllers.

## Important design choice

The Web Lean Bridge is not removed from the repository. It remains the correct transport for ChatGPT Web. It is simply not the default Codex transport.

This allows both clients to share:
- one stage registry;
- one evidence model;
- one Human Gate model;
- one validator/controller implementation;
- one promotion path;
while using client-appropriate transport.

## Workspace

Raw media belongs in ignored local workspace:
`06_TESTS/MV/CODEX_R2/workspace/D03-B/`

Do not commit large media. Canonical text manifests/receipts/QA evidence remain in the slot tree as defined by the existing Runtime.

## Smoke check

`.github/workflows/codex-r2-smoke.yml` is a read-only adapter check. It compiles the local operator plus reused Runtime modules, runs Codex preflight and a D03-B resume, verifies that the result is an allocation for `D03-B / Lane S`, and asserts that read-only commands did not create Canonical D03-B state or modify the worktree.

This smoke check never initializes the slot. D03-B initialization is deliberately reserved for the real Codex run so the automation test starts from a genuine clean allocation.

## Start

Use the content of `CODEX_START_PROMPT.md` in a Codex task configured on branch `test/mv-codex-r2`.
