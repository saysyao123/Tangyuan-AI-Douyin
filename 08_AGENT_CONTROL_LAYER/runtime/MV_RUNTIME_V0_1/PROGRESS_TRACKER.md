# MV Runtime v0.1 — Progress Tracker

> Human-readable view. PROJECT_STATE_SCHEMA.yaml is the state source of truth.
> This file must agree with the state validator.

## Status vocabulary

| Status | Meaning |
|---|---|
| NOT_STARTED | No detailed design work yet |
| DESIGNING | Current stage is being designed |
| READY_FOR_TEST | Contract/design exists; waiting for isolated test |
| TESTING | Test is actively being executed |
| DELIVERED | Test produced concrete delivery artifacts |
| REVIEW | Delivery is being judged |
| SEALED | Accepted; next stage may begin design |
| REVISE | Current stage failed review; revise locally |
| BLOCKED | Missing dependency/evidence prevents progress |
| DIRTY | Previously sealed downstream stage invalidated by upstream contract change |

## Global build rule

Only one not-yet-sealed build stage may be in DESIGNING at a time.

## Build progress

| Build ID | Component | Status | Test | Delivery | Review result | Next allowed action |
|---|---|---|---|---|---|---|
| F0 | Runtime Framework | SEALED | Structural self-check complete | Runtime skeleton + schemas | PASS | S0 |
| S0 | SONG_SELECTION | SEALED | Retest01 known-good replay under Contract v0.3 | S0_DELIVERY_RETEST01_v0.3.yaml | PASS / AUTO_CONFIRMED_FOR_TEST | S1 |
| S1 | PROJECT_AUDIO | SEALED | Retest01 user-source replay under Contract v0.4 | S1_DELIVERY_RETEST01_v0.4.yaml | PASS / AUTO_CONFIRMED_FOR_TEST | S2 |
| S2 | DIRECTOR | NOT_STARTED | — | — | — | May enter DESIGNING |
| S3 | FIRST_FRAME | NOT_STARTED | — | — | — | Blocked until S2 SEALED |
| S4 | MOTION | NOT_STARTED | Existing pilot available, not integrated | — | — | Blocked until S3 SEALED |
| S5 | GENERATION | NOT_STARTED | — | — | — | Blocked until S4 SEALED |
| S6 | VIDEO_QA | NOT_STARTED | — | — | — | Blocked until S5 SEALED |
| S7 | ASSEMBLY_FINAL | NOT_STARTED | — | — | — | Blocked until S6 SEALED |

## Current active build target

S2 — DIRECTOR (NOT_STARTED, allowed to enter DESIGNING)

## Current next decision

S0 and S1 have passed the Control Retest.
S1A autonomous source acquisition remains an independent research item; the
current successful S1 run uses the explicitly recorded USER_PROVIDED_MEDIA_FALLBACK.
This does not block the sealed Project Audio handoff for the current run.

## Judge caveat

Retest01 used structured same-model minimal-context Judge calls.
This validates Judge request/output protocol but does not prove independent
Fresh Judge behavior. Production runtime should still prefer a truly fresh Judge.

## Runtime completion definition

The runtime is not fully validated until:
- all S0–S7 are SEALED in one real project run;
- selective reopen/rebuild is tested at least once;
- downstream succeeds from Compact Handoff without full history;
- independent Fresh Judge execution is validated;
- final video passes human final review.
