# Rules｜MV Executor-First v1 Lean R1

Status: `EXPERIMENT_CANDIDATE / HARD DURING LEAN_R1`

## Purpose

Runtime defines WHAT stage is current. The Stage Executor Registry defines HOW that stage is already executed. A Rule defines constraints; it is not permission to invent a new tool, workflow, model or service.

## Required order

For every stage:

`RESUME -> resolved executor -> JIT rule/template -> existing tool/recipe/capability -> dependency doctor/cache -> execute -> validate`

## New-tool admission gate

Before creating any new helper/workflow/model route, all must be true:
1. current stage and executor entry are known;
2. canonical tool/recipe/capability was checked first;
3. prior PASS path was checked when available;
4. dependency doctor/cache was checked;
5. a concrete implementation gap exists;
6. current experiment explicitly allows solving that gap;
7. new implementation is isolated from stable core until promotion;
8. Human Gate and canonical state semantics remain unchanged.

If any item is false: do not create the tool.

## Hard prohibitions

- no per-song production-model installation;
- no slot-specific helper inside core tools by default;
- no stage-specific job inside the authoritative stable Runtime bridge;
- no external OSS implementation imported merely because a rule mentions it;
- no second lyric clock for reassurance;
- no new image/video backend when the registered executor is a capability handoff.

## Lean R1 addition

Lean macros may compress external controller round-trips, but may not skip machine validation, Human Gates, rollback receipts or stage evidence. `RUN_UNTIL_GATE_OR_BLOCK` only advances through already-valid machine stages; it does not fabricate stage artifacts. `ACCEPT_GATE` keeps the internal two-step semantics (record receipt, then advance) inside one external command.
