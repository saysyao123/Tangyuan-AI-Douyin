# MV Runtime Consolidation｜P1 Controlled Context Mutation Receipt v1

- Date: 2026-08-26
- Branch: `refactor/mv-runtime-consolidation-v2`
- Status: `P1 CONTEXT MUTATION PASS / CANDIDATE`
- Production default: `NO`

## Problem

Some Runtime conditions are not truthfully known at slot initialization. The key case is hidden multi-shot complexity: a source may be planned as one visual source but only reveal multiple perceptible internal shots after generation and Dynamic Source QA.

If `multi_shot=false` remains an unverified S00 default, the Runtime could incorrectly skip Shot Normalization.

## Contract

New file:
`04_HARNESS/runtime/mv_context_contract.json`

Immutable after slot initialization:
- `web`;
- `program_30d60`;
- `canonical_v2`.

Controlled mutable condition:
- `multi_shot` only;
- only `false -> true`;
- only while current stage is `S08_DYNAMIC_SOURCE_QA_LOCKED`;
- must happen before `S09_SOURCE_NORMALIZATION_READY`;
- requires canonical locked `DYNAMIC_SOURCE_QA` + `VISUAL_SOURCE_MAP` evidence;
- requires an explicit reason;
- cannot be relaxed back to false.

## State model

Canonical state now includes:
- `context_revision`;
- `last_context_receipt`;
- `last_context_receipt_sha256`.

Context truth is derived as:

`SLOT_MANIFEST initial context`
→ `ordered immutable CONTEXT_EVENTS`
→ `CURRENT_STATE.context`.

A manual context edit that does not reproduce from that chain is invalid.

Context receipts live under:
`00_STATE/CONTEXT_EVENTS/`.

## Runtime behavior

`mv_runtime_state.py` now supports:

`update-context --key multi_shot --value true --reason ...`

The command:
1. verifies the current transition and context chains;
2. requires current stage S08;
3. validates locked Dynamic QA evidence;
4. verifies the change is monotonic false-to-true;
5. writes a context receipt with source evidence hashes;
6. updates CURRENT_STATE context + context revision;
7. re-verifies the whole slot and rolls back if verification fails.

## CI evidence

Workflow:
`.github/workflows/r3-mv-runtime-p1-context-tests.yml`

Run ID: `32979922216`
Conclusion: `success`

The synthetic canonical slot was executed through:
HG01 -> HG02 -> Audio Timeline -> Natural Beat -> Director -> HG03 -> Dynamic Prompt -> Dynamic Source QA.

At S08 the test verified:
- immutable `web` cannot change;
- `multi_shot false -> true` succeeds with locked source evidence;
- `true -> false` is rejected;
- before Shot Library exists, S09 advance is rejected and explicitly requires `SHOT_LIBRARY_MAP` plus WEB normalization artifacts;
- after Shot Library + WEB normalization are present, S09 advances successfully;
- a context change attempted after S09 is rejected;
- direct CURRENT_STATE context tampering is detected.

## Result

Hidden multi-shot complexity can no longer be bypassed merely because S00 initialized `multi_shot=false`.

The newly discovered condition escalates the downstream gate; it cannot relax one.
