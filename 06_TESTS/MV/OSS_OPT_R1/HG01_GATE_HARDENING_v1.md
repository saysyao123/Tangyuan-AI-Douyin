# OSS OPT R1｜HG01 Gate Hardening v1

Status: `ACTIVE / EXPERIMENT BRANCH ONLY`
Date: `2026-08-27`
Branch: `test/mv-oss-optimization-r1`

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

The Runtime only checked that `SONG_CANDIDATE_SET.json` existed and was valid JSON. It did not require evidence-delivery assertions before `RECORD_HUMAN_GATE HG01`.

## Hardening applied

### H1｜Candidate-set artifact now contains evidence-delivery hard checks

`04_HARNESS/runtime/mv_artifact_registry.json` schema bumped to `1.2`.

For canonical `SONG_CANDIDATE_SET`, Runtime validation now requires all of:

- `status = HG01_EVIDENCE_DELIVERY_PASS`
- persisted `evidence_pack_path`
- `all_candidates_min_direct_works_2 = true`
- `all_candidates_independent_accounts_2plus = true`
- `all_direct_links_landing_work_verified = true`
- `core_account_coverage_reported = true`
- `no_external_audio_substitution = true`
- `user_gate_delivery_mode = DIRECT_WORKS_FIRST`

Because `HG01` already uses `SONG_CANDIDATE_SET` as a machine preflight artifact, `RECORD_HUMAN_GATE HG01` now fails automatically until these assertions are true.

### H2｜Human Gate rule explicitly separates preflight and delivery

`04_HARNESS/rules/mv_human_gates.md` now states:

`SONG_CANDIDATE_SET != HG01 USER DELIVERY`

The assistant must show direct works first. Machine recommendation is auxiliary only.

### H3｜Stage-entry checklist adds HG01 entry guard

`04_HARNESS/rules/mv_stage_entry_checklist.md` now blocks HG01 submission when evidence is only preflight/repack state.

### H4｜Landing-work identity rule

A URL is not valid Direct Douyin Evidence merely because the page text contains the target song in a creator's recent-work list.

Formal evidence must be `LANDING_WORK`:

- URL work id = cited landing work id;
- landing work itself supports the candidate SONG_FAMILY / AUDIO_VERSION;
- profile-like listing evidence is discovery-only.

### H5｜Current D02-B corrected

`D02-B/01_SONG/SONG_CANDIDATE_SET.json` was demoted from `HG01_READY` to:

`HG01_PREFLIGHT_PREPARED`

Human gate state is now:

`AWAITING_EVIDENCE_REPACK`

No HG01 receipt had been recorded, so no Canonical state rollback was required.

## Required behavior in future chats

When current stage is S00 / HG01 preparation:

1. build machine candidate set;
2. resolve concrete direct Douyin works;
3. build human-facing evidence pack;
4. verify landing-work identity;
5. only then set `HG01_EVIDENCE_DELIVERY_PASS`;
6. present direct works to the user;
7. user selects one song;
8. Runtime `RECORD_HUMAN_GATE HG01`;
9. separate `ADVANCE` to S01.

Forbidden shortcut:

`candidate names -> machine recommendation -> ask A/B/C/D`

## Promotion policy

This is a Runtime correctness hardening discovered on the experiment branch, not an OSS visual optimization.

Stable `test/mv-web-r3` remains untouched during the experiment.

After branch validation, classify this change separately as a candidate:

`PROMOTE_RUNTIME / HG01 DELIVERY GUARD`

It should not wait on visual-quality evidence because it fixes Gate correctness, but production promotion must still be explicit and audited.
