# CODEX / Agent Runtime Instructions v4.0 — Codex R2 Branch

Target branch: `test/mv-codex-r2`

This file is a compatibility pointer for older repository instructions. For Codex R2, persistent repository instructions now live in `AGENTS.md` and the MV-specific `06_TESTS/MV/AGENTS.md`, matching Codex's native instruction model.

## MV startup

Do NOT use the old generic startup chain `SKILL -> MANIFEST -> 00_CONTROL/CURRENT_STATE` as MV project-state authority.

For a Codex R2 MV task:

1. Let Codex load root `AGENTS.md` automatically.
2. Read `06_TESTS/MV/CODEX_R2/CODEX_EXECUTION_CONTRACT.md`.
3. Read `06_TESTS/MV/CODEX_R2/CODEX_TEST_MATRIX.md`.
4. Run:
   `python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py preflight`
5. Run an explicit slot resume, normally:
   `python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py resume --slot D03-B`
6. From then on, load only `resolved_executor` / JIT files for the current phase.

Canonical MV state comes from:
`06_TESTS/MV/WEB_R3/30D_60/<slot>/00_STATE/`
plus the Runtime registry/receipts, never from chat memory or a Codex-only CURRENT_STATE file.

## Transport

Codex has a local shell. Its default Runtime transport is the local CODEX_R2 operator over existing Canonical/Lean controllers.

The immutable GitHub request -> Actions -> response bridge remains the ChatGPT Web transport and should not be used by Codex by default.

## Human Gates

HG01 / HG02 / HG03 / HG04 / HG05 remain mandatory. Machine QA never substitutes for user approval.

## External generation

If image generation, Seedance/video generation, authenticated browser access or another external capability is unavailable, use `06_TESTS/MV/CODEX_R2/CODEX_HANDOFF_PROTOCOL.md`. Do not fabricate success.

## Git safety

- no new branches during the test;
- no force/amend/history rewrite;
- no secrets/auth state;
- no large media commits;
- no manual Canonical state/receipt edits;
- commit coherent phase-level changes and inspect final diff/status.

Historical `06_TESTS/MV/CODEX_R1` is reference-only. It is not the active Codex workflow.