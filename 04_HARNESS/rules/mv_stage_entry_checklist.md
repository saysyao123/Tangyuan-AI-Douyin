# Rules｜MV Stage Entry Checklist v1.1

> Status: `DEPRECATED AS RUNTIME AUTHORITY / COMPATIBILITY NOTE ONLY`
> Reason: Canonical Runtime now machine-enforces Stage prerequisites, artifacts, transitions, Human Gate receipts, revision/rollback, and resume semantics. Keeping a second Markdown checklist as an independent authority creates duplicated truth and maintenance drift.

## Canonical Authority

Do not use this file to decide whether a Stage may advance.

Use:
- `runtime/mv_stage_registry.json`
- `runtime/mv_artifact_registry.json`
- `runtime/mv_transition_contract.json`
- `runtime/mv_human_gate_registry.json`
- `tools/mv_runtime_gate.py`
- `tools/mv_runtime_state.py`
- corresponding Canonical Runtime controllers/tests

A declared chat state, prose checklist PASS, or Human Gate PASS never substitutes for Canonical validation.

## Compatibility Principle

The historical intent remains valid:

> Known prerequisites must be machine-enforced before downstream work.

But the enforcement now lives in Runtime/Validator, not in this Markdown file.

## Failure Behavior

When Canonical validation fails:
1. identify the nearest missing/invalid prerequisite;
2. patch only that root cause;
3. re-run the authoritative Validator / transition path;
4. continue only after machine validation passes.

Do not reopen unrelated approved aesthetic decisions unless the repair materially changes what the user approved.

## Migration Note

Any Workflow/Manifest/Skill that still treats this file as a required Stage-entry JIT dependency should be updated to call Canonical Runtime validation instead.

Historical R1/R2/R3 documents may continue referencing this file for provenance; those references do not make it an active Runtime authority.
