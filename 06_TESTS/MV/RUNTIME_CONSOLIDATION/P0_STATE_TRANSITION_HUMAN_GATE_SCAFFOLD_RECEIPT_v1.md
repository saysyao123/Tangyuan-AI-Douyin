# MV Runtime Consolidation｜P0 State Transition + Human Gate + Scaffold Receipt v1

- Date: 2026-08-26
- Branch: `refactor/mv-runtime-consolidation-v2`
- Status: `P0 ENFORCEMENT PASS / CANDIDATE / NOT PRODUCTION DEFAULT`
- Scope: original Tangyuan MV Runtime only
- Excluded: D02-B Director/Aesthetic experiment inspired by external MV projects

## Delivered

1. `04_HARNESS/runtime/mv_human_gate_registry.json`
   - exactly HG01–HG05;
   - machine-preflight artifacts are separate from user approval;
   - canonical PASS receipts are structured JSON.

2. `04_HARNESS/runtime/mv_transition_contract.json`
   - only the immediate next stage may advance;
   - target evidence must validate before mutation;
   - every advance writes an immutable transition receipt;
   - receipts form a SHA-256 chain;
   - manual state jumps are invalid.

3. `04_HARNESS/runtime/mv_slot_scaffold.json`
   - canonical directories `00_STATE` through `13_POST_PUBLISH`;
   - new slots start in `canonical_v2` mode;
   - old R1/R2/R3 projects remain legacy audit fixtures.

4. `04_HARNESS/tools/mv_runtime_state.py`
   - `init-slot`;
   - `record-human-gate`;
   - `advance`;
   - `verify-state`.

5. Stage/Artifact Registry v1.1
   - historical mode keeps old evidence readable;
   - canonical_v2 mode adds machine preflight requirements for HG01, HG02 and HG04;
   - future Human Gate receipts use canonical JSON paths;
   - a PASS receipt never replaces machine QA.

## Canonical Human Gate rule

`UPSTREAM CHAIN PASS`
→ `MACHINE PREFLIGHT ARTIFACTS PASS`
→ `USER PASS`
→ `CANONICAL HUMAN GATE RECEIPT`
→ `TARGET STAGE VALIDATION PASS`
→ `TRANSITION RECEIPT`
→ `CURRENT_STATE UPDATE`.

The state controller will not create a PASS receipt when required machine evidence is missing.
The state controller will not advance merely because a user approval string exists.

## State mutation rule

`mv_runtime_gate.py` remains the read-only evidence judge.
`mv_runtime_state.py` is the only candidate state mutator.

The mutator:
- verifies the current transition chain first;
- allows only the immediate next registered stage;
- validates the complete target evidence chain;
- rejects legacy aliases in canonical_v2 slots;
- snapshots immutable evidence hashes;
- writes a transition receipt;
- updates CURRENT_STATE only after the receipt exists;
- re-verifies after mutation and rolls state back if post-validation fails.

`CURRENT_STATE.json` is deliberately excluded from immutable evidence snapshots because it is the mutable ledger itself.

## CI evidence

Workflow: `.github/workflows/r3-mv-runtime-p0-tests.yml`

Run ID: `32978759224`
Conclusion: `success`

Verified in the canonical_v2 synthetic slot:
1. `init-slot` creates a valid S00 slot;
2. HG01 cannot be recorded before `SONG_CANDIDATE_SET` exists;
3. S01 cannot advance before the HG01 PASS receipt exists;
4. after machine preflight + receipt, S01 advances and verifies;
5. direct S01 → S03 skipping is blocked;
6. HG02 cannot be recorded before `BGM_CANDIDATE_PACKAGE` exists;
7. after machine preflight + receipt, S02 advances and verifies;
8. manual CURRENT_STATE tampering is detected by transition-sequence/hash-chain verification;
9. D02-A and D01-B historical audit regressions still behave as expected.

## Remaining before Production Default

- controlled legacy migration / canonical pointers;
- controlled runtime-context mutation for conditions discovered later (notably multi-shot normalization);
- tracker + slot transactional publish sync;
- external media asset manifest + hash verification;
- canonical rollback / revision attempts;
- zero-context start prompt wired to `init-slot / verify / advance`;
- at least one full new MV run through canonical_v2 without bypassing a stage.

Therefore authority remains:

`P0 ENFORCEMENT PASS / CANDIDATE`

not:

`PRODUCTION DEFAULT`.
