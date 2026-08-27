# OSS OPT R1｜HG01 Gate Hardening v1.1

Status: `VALIDATED / PASS / EXPERIMENT BRANCH ONLY`
Date: `2026-08-27`
Branch: `test/mv-oss-optimization-r1`
Validated head: `233f7df2dd2a272b2bb390ff116d4f4d0ffa2721`
CI run: `33036864308 / R3 HG01 Delivery Guard Tests / PASS`

## Problem

D02-B exposed a repeatable process failure:

1. machine song discovery produced a valid-looking candidate set;
2. candidate set was prematurely labeled `HG01_READY`;
3. assistant presented song names/rankings and asked the user to choose A/B/C/D;
4. the required user-facing Direct Douyin Evidence Pack was not actually delivered first;
5. several stored `direct_evidence.url` values were not the cited work itself. They were older Douyin landing works whose pages happened to list newer relevant works from the same creator.

This violates the existing R3 HG01 Evidence Delivery Contract and weakens Human Gate quality.

## Root cause

Two concepts were not machine-separated strongly enough:

- `MACHINE CANDIDATE PREFLIGHT`
- `HUMAN-DECISION EVIDENCE DELIVERY`

The Runtime previously only checked that `SONG_CANDIDATE_SET.json` existed and was valid JSON. It did not require evidence-delivery assertions or validate an independent evidence-pack artifact before `RECORD_HUMAN_GATE HG01`.

## Hardening applied

### H1｜Candidate-set artifact now contains evidence-delivery hard checks

`04_HARNESS/runtime/mv_artifact_registry.json` schema is now `1.3`.

For canonical `SONG_CANDIDATE_SET`, Runtime validation requires all of:

- `status = HG01_EVIDENCE_DELIVERY_PASS`
- exact persisted `evidence_pack_path = 01_SONG/HG01_CANDIDATE_EVIDENCE_PACK_v1.md`
- `all_candidates_min_direct_works_2 = true`
- `all_candidates_independent_accounts_2plus = true`
- `all_direct_links_landing_work_verified = true`
- `core_account_coverage_reported = true`
- `no_external_audio_substitution = true`
- `user_gate_delivery_mode = DIRECT_WORKS_FIRST`

### H2｜Evidence Pack is now its own Canonical Runtime artifact

New artifact ID:

`HG01_CANDIDATE_EVIDENCE_PACK`

Canonical path:

`01_SONG/HG01_CANDIDATE_EVIDENCE_PACK_v1.md`

It is no longer enough to put a path string in the candidate JSON. The actual pack must exist and pass its own assertions:

- `HG01_EVIDENCE_DELIVERY_PASS = YES`
- `DIRECT_DOUYIN_EVIDENCE_PACK_READY = YES`
- `CORE_ACCOUNT_COVERAGE_REPORTED = YES`
- `ALL_DIRECT_LINKS_LANDING_WORK_VERIFIED = YES`
- `NO_EXTERNAL_AUDIO_LINK_SUBSTITUTION = YES`
- `DIRECT_WORKS_FIRST`
- `LANDING_WORK`

### H3｜HG01 receipt creation checks both independent preflight artifacts

`04_HARNESS/runtime/mv_human_gate_registry.json` schema is now `1.1`.

HG01 `machine_preflight_artifacts` now contains:

1. `SONG_CANDIDATE_SET`
2. `HG01_CANDIDATE_EVIDENCE_PACK`

Therefore `RECORD_HUMAN_GATE HG01` is mechanically rejected if either side is invalid.

### H4｜S01 Canonical transition independently requires the Evidence Pack

`04_HARNESS/runtime/mv_stage_registry.json` schema is now `1.2`.

For `canonical_v2`, `S01_HG01_SONG_LOCKED` requires:

- `HG01_SELECTION_RECEIPT`
- `SONG_CANDIDATE_SET`
- `HG01_CANDIDATE_EVIDENCE_PACK`

This is deliberately redundant with the Human Gate preflight. Even if a receipt were somehow written incorrectly, Canonical `ADVANCE` cannot validate S01 without the evidence pack.

### H5｜Human Gate rule explicitly separates preflight and delivery

`04_HARNESS/rules/mv_human_gates.md` now states:

`SONG_CANDIDATE_SET != HG01 USER DELIVERY`

The assistant must show direct works first. Machine recommendation is auxiliary only.

Forbidden shortcut:

`candidate names -> machine recommendation -> ask A/B/C/D`

### H6｜Stage-entry checklist adds HG01 entry guard

`04_HARNESS/rules/mv_stage_entry_checklist.md` blocks HG01 submission when evidence is only preflight/repack state.

### H7｜Landing-work identity rule

A URL is not valid Direct Douyin Evidence merely because the page text contains the target song in a creator's recent-work list.

Formal evidence must be `LANDING_WORK`:

- URL work id = cited landing work id;
- landing work itself supports the candidate SONG_FAMILY / AUDIO_VERSION;
- profile-like listing evidence is discovery-only.

### H8｜Current D02-B corrected

`D02-B/01_SONG/SONG_CANDIDATE_SET.json` was demoted from `HG01_READY` to:

`HG01_PREFLIGHT_PREPARED`

Human gate state is:

`AWAITING_EVIDENCE_REPACK`

Current `HG01_CANDIDATE_EVIDENCE_PACK_v1.md` is intentionally `NOT READY FOR HUMAN GATE` until concrete direct works are rebuilt.

No HG01 receipt had been recorded, so no Canonical state rollback was required. D02-B remains at S00.

## CI validation

Dedicated experiment workflow:

`.github/workflows/r3-hg01-delivery-guard-tests.yml`

Final validated run:

`33036864308`

Result: `PASS`.

The CI proves all three cases:

1. current incomplete D02-B candidate set and evidence pack are both rejected;
2. synthetic `RECORD_HUMAN_GATE HG01` is mechanically rejected before evidence delivery PASS;
3. a synthetic positive fixture can complete the real Canonical chain only after candidate set + evidence pack both pass, then `RECORD_HUMAN_GATE -> ADVANCE -> VERIFY_STATE` reaches `S01_HG01_SONG_LOCKED`, with the transition evidence snapshot containing:
   - `SONG_CANDIDATE_SET`
   - `HG01_CANDIDATE_EVIDENCE_PACK`
   - `HG01_SELECTION_RECEIPT`

## Required behavior in future chats

When current stage is S00 / HG01 preparation:

1. build machine candidate set;
2. resolve concrete direct Douyin works;
3. build human-facing evidence pack;
4. verify landing-work identity;
5. only then set both candidate set and evidence pack to delivery PASS;
6. present direct works to the user;
7. user selects one song;
8. Runtime `RECORD_HUMAN_GATE HG01`;
9. separate `ADVANCE` to S01.

No model/chat-memory shortcut is authoritative over these Runtime requirements.

## Promotion policy

This is a Runtime correctness hardening discovered on the experiment branch, not an OSS visual optimization.

Stable `test/mv-web-r3` remained untouched during this experiment-branch change.

Classification after validation:

`PROMOTE_RUNTIME_CANDIDATE / HG01 DELIVERY GUARD / VALIDATED`

Production promotion must still be a separate explicit audited change; it must not be silently merged from the experiment branch.
