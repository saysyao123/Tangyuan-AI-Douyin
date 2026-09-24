# MV Runtime v0.1 — Progress Tracker

> This file is the primary human-readable progress table. Update it whenever a build stage changes state.

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
| DIRTY | Previously sealed downstream stage invalidated by an upstream contract change |

## Global build rule

Only one not-yet-sealed build stage may be in DESIGNING at a time.

A downstream stage may have a placeholder folder, but detailed design must wait for upstream SEAL.

## Build progress

| Build ID | Component | Status | Test | Delivery | Review result | Next allowed action |
|---|---|---|---|---|---|---|
| F0 | Runtime Framework | SEALED | Structural self-check complete | Runtime skeleton + tracker + schemas | PASS / entry-stage correction accepted | Start S0 SONG_SELECTION |
| S0 | SONG_SELECTION | SEALED | Chinese filter + dedupe + Top3 PASS; 若爱有尽头 selected | S0_DELIVERY_RUN01_v0.2.yaml | Human Song Family Lock PASS | S1 owns material acquisition |
| S1 | PROJECT_AUDIO | SEALED | User-provided 21.4s source validated; full lyric timeline built | S1_DELIVERY_RUN02_FINAL.yaml | HUMAN_AUDIO_LOCK PASS | S2 DIRECTOR may begin |
| S2 | DIRECTOR | NOT_STARTED | — | — | — | Blocked until S1 SEALED |
| S3 | FIRST_FRAME | NOT_STARTED | — | — | — | Blocked until S2 SEALED |
| S4 | MOTION | NOT_STARTED | Existing pilot available, not integrated | — | — | Blocked until S3 SEALED |
| S5 | GENERATION | NOT_STARTED | — | — | — | Blocked until S4 SEALED |
| S6 | VIDEO_QA | NOT_STARTED | — | — | — | Blocked until S5 SEALED |
| S7 | ASSEMBLY_FINAL | NOT_STARTED | — | — | — | Blocked until S6 SEALED |

## F0 Framework delivery checklist

- [x] Runtime directory created
- [x] Stage order registered
- [x] Project state schema created
- [x] Transition rules created
- [x] Context Compiler rules created
- [x] Runtime build/test/seal runbook created
- [x] Eight-stage placeholders created
- [x] Progress tracker created
- [x] F0 reviewed
- [x] F0 SEALED

## Current active build target

S2 — DIRECTOR (allowed, not started)

## Current next decision

S0 remains SEALED. S1A component is now validated and frozen at v0.2. The current project is blocked only because the selected 张蓓蓓/林叙 version is not covered by the current compliant acquisition catalogs. Resume S1B immediately once exact media is acquired.

## Runtime completion definition

The runtime itself is not considered validated until:

- all S0–S7 are SEALED in one real project run;
- selective reopen/rebuild has been tested at least once;
- a downstream stage succeeds from Compact Handoff without loading full history;
- final video passes human final review.