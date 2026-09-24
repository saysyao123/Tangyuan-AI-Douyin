# S0 -> S1 Control Retest Run01

Mode: KNOWN_GOOD_REPLAY
Date: 2026-09-24

## Purpose

Test control flow and state consistency after Contract/State cleanup.
This run intentionally replays the known-good Song Family and Project Audio
case so creative discovery is not mixed with runtime validation.

## Human Gates

For this test only:
- S0 Human Song Family Lock: AUTO_CONFIRMED_FOR_TEST
- S1 Human Audio Lock: AUTO_CONFIRMED_FOR_TEST

Production mode still requires user confirmation.

## S0

Contract: v0.3 FINAL

Checks:
- Chinese policy: PASS
- historical dedupe: PASS
- Song Family dedupe: PASS
- Top3 cardinality: PASS
- selected Song Family belongs to shortlist: PASS
- no media/timeline work leaked into S0: PASS

Selected:
若爱有尽头

Stage Seal protocol:
PASS

## S0 -> S1 handoff

Only these categories cross the boundary:
- selected Song Family
- selection evidence
- candidate source/reference leads
- Song Family Lock

No exact media file or timeline crosses from S0.

Boundary:
PASS

## S1

Contract: v0.4 FINAL

Acquisition route for this replay:
USER_PROVIDED_MEDIA_FALLBACK

Important:
The autonomous acquisition research remains unresolved and is not falsely
converted to PASS by the fallback.

Coverage:
TARGET_SEGMENT_SOURCE_ACQUIRED

Checks:
- actual analyzable source exists: PASS
- provenance explicit: PASS
- source coverage explicit: PASS
- preview/full distinction preserved: PASS
- authoritative source explicit: PASS
- timeline ordered/in-range: PASS
- Human Audio Lock: PASS
- no Director work leaked into S1: PASS

Final audio:
0.00 -> 21.360907s

Stage Seal protocol:
PASS

## Judge limitation

The structured Judge requests/results in this replay use the same GPT model in a
minimal-context test mode. They validate Judge protocol shape and routing, but
do NOT prove independent Fresh Judge behavior.

A truly independent Fresh Judge remains a future runtime execution requirement.

## Retest verdict

S0 -> S1 control flow:
PASS

Next:
run deterministic Runtime State Validator against State / Tracker / Handoffs.
