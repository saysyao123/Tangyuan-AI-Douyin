# AGENTS.md — Tangyuan MV Codex R2

Scope: the entire repository when Codex is working on branch `test/mv-codex-r2`.

## Mission

For MV work, Codex is an operator of the existing Canonical MV Runtime. It is not allowed to invent a second workflow/state machine merely because local shell access is available.

## Authority order for MV tasks

1. Current explicit user instruction.
2. Canonical slot state, transition/revision receipts, asset records, Human Gate receipts.
3. `04_HARNESS/runtime/mv_stage_registry.json` and `mv_resume_contract.json`.
4. `04_HARNESS/runtime/mv_stage_executor_registry.json`.
5. Current stage JIT Rule / Workflow / Template / Knowledge files.
6. `06_TESTS/MV/CODEX_R2/*` test documentation.
7. Historical rounds, old CODEX_R1, old Harness files and chat summaries.

For Canonical MV work, `00_CONTROL/CURRENT_STATE.md` is NOT project-state authority. Do not let the generic v3 router override the slot state under `06_TESTS/MV/WEB_R3/30D_60/<slot>/00_STATE/`.

## Branch and Git discipline

- Expected branch: `test/mv-codex-r2`.
- Verify the branch before writing. If the environment is on another branch, do not mutate repository truth until the user/task environment is corrected.
- Do not create another branch, force-push, amend, rewrite history, or merge stable branches during this test.
- Make coherent commits at meaningful phase boundaries; do not commit every read/status query.
- Before finishing a task, inspect `git status` and relevant diffs. Leave the worktree clean when practical.
- Never commit secrets, cookies, login state, tokens, private credentials, or unredacted private data.
- Do not commit large audio/video working media. Respect repository `.gitignore` and the CODEX_R2 workspace ignore rules.

## Context budget

Do not scan the whole repository at startup. Initial context for a Codex R2 MV task should normally be limited to:

1. this `AGENTS.md` (loaded automatically by Codex);
2. `06_TESTS/MV/AGENTS.md`;
3. `06_TESTS/MV/CODEX_R2/CODEX_EXECUTION_CONTRACT.md`;
4. the output of the Codex local operator `resume` command.

After that, read only the `resolved_executor` / JIT paths required by the current phase.

## Runtime mutation rule

Use `python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py ...` for normal Codex-side Runtime operations.

That operator delegates to the existing Canonical Runtime / Lean controller implementation. It does not define a new state authority.

Never hand-edit any of the following to make a stage look passed:
- `CURRENT_STATE.json`;
- transition / revision receipts;
- Human Gate receipts;
- package manifests whose truth is owned by a validator;
- Tracker status as a substitute for Runtime transition.

The Web Lean Bridge request/Actions transport exists for ChatGPT Web. Codex should not use `04_HARNESS/lean_runtime_bridge/requests/*` as its normal transport path because Codex has a local shell and repository checkout.

## Human Gates

The five Human Gates remain mandatory: HG01 song, HG02 BGM, HG03 first-frame set, HG04 picture edit, HG05 final acceptance.

Never infer a PASS from silence, an earlier conversation, or a machine QA result. `accept-gate` may be called only when the current user instruction contains a real approval/selection for that gate.

## External-capability rule

Codex must distinguish local engineering from capabilities it may not possess in the current environment. If browser authentication, image generation, Seedance/video generation, or another external capability is unavailable, use the CODEX_R2 handoff protocol. Produce exact inputs/prompts/expected filenames and stop at the correct boundary. Never create dummy media or claim an external generation happened when it did not.

## Core-change admission

Do not modify `04_HARNESS` core code just because a task is awkward. First use the registered executor and existing tools. A core change is allowed only for a concrete reproducible blocker/bug, and then:
- keep the change generic, never D03-B-specific;
- add/update regression coverage;
- run the relevant tests and syntax checks;
- document the reason in the Codex result report.

## Definition of done

A Codex R2 task is complete only when the requested phase has real artifacts/evidence, Canonical Runtime truth is consistent, required tests/QA pass, Human Gate boundaries are respected, and the result is committed/documented without hidden manual state edits.