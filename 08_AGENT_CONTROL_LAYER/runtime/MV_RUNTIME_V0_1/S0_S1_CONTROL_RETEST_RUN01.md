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


## Deterministic Runtime Validator

Validator:
`MV_RUNTIME_STATE_VALIDATOR_V0_1`

GitHub Actions:
`PASS`

Checks:
`23 / 23 PASS`

Errors:
`[]`

Validated:
- Tracker S0/S1/S2 status matches Project State;
- S0 Contract v0.3 is FINAL;
- S1 Contract v0.4 is FINAL;
- S0/S1 retest deliveries are SEALED;
- S0/S1 Human Gates are PASS;
- S0/S1 structured Judge routes are PASS and correctly marked test-only / not fully fresh;
- S0/S1 Project State is SEALED;
- S2 dependency and current-stage routing are correct;
- active State references contain no DRAFT contract references.

## Final Retest Result

`S0_TO_S1_CONTROL_RETEST_RUN01 = PASS`

Runtime truth after retest:

```
S0 SONG_SELECTION  v0.3  SEALED
        ↓
S1 PROJECT_AUDIO   v0.4  SEALED
        ↓
S2 DIRECTOR              NOT_STARTED / ALLOWED
```

The state-drift defect found during review is closed for S0/S1.

Remaining known limitation:
independent Fresh Judge execution has not yet been proven. Retest01 validates
the typed Judge protocol using same-model minimal-context execution only.
