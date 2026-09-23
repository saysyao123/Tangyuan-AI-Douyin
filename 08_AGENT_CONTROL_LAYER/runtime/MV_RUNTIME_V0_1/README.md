# Tangyuan MV Agent Runtime v0.1

Status: F0_FRAMEWORK_READY_FOR_REVIEW
Mode: EXPERIMENTAL / DOES_NOT_REPLACE_CURRENT_MV_MAINLINE

## 1. Purpose

Build a stable video-production runtime using the Agent Control Layer principles already recorded in this repository.

The runtime must be developed stage by stage.

No stage is allowed to become a large speculative design before the previous stage has:

1. been designed;
2. been tested;
3. produced a concrete delivery artifact;
4. been reviewed;
5. been accepted and SEALED.

The goal is not to design the perfect full workflow in advance. The goal is to build a chain of independently validated modules.

## 2. Locked development method

DESIGN -> READY_FOR_TEST -> TEST -> DELIVERY -> REVIEW -> PASS? -> SEAL -> NEXT STAGE MAY ENTER DESIGN

If review fails: REVISE CURRENT STAGE ONLY.

A later stage may have a placeholder contract before that point, but must not be deeply implemented.

## 3. Runtime target flow

S1 PROJECT_AUDIO -> S2 DIRECTOR -> S3 FIRST_FRAME -> S4 MOTION -> S5 GENERATION -> S6 VIDEO_QA -> S7 ASSEMBLY_FINAL

This is the first proposed runtime shape. It is intentionally smaller than the existing long-form MV HARNESS.

## 4. Core runtime components

- PROJECT_STATE_SCHEMA.yaml — single source of project truth
- STAGE_REGISTRY.yaml — all runtime stages and dependency order
- TRANSITION_RULES.yaml — what allows/blocks transitions
- CONTEXT_COMPILER_SPEC.md — what each stage is allowed to read
- PROGRESS_TRACKER.md — human-readable project/build progress
- RUNTIME_RUNBOOK.md — how to build/test/seal each stage
- stages/ — one isolated folder per stage

## 5. Runtime responsibility split

- Executor GPT: create / revise artifact
- Perception GPT / tools: convert non-structured media into evidence when needed
- Fresh Judge: judge current contract only
- Code / State Rules: decide transitions
- Human Gate: creative direction / first-frame acceptance / final-film acceptance

## 6. Current development state

Only framework F0 is implemented now.

The seven stages are registered as placeholders. Do not treat them as complete designs.

Next allowed development action after F0 review: S1 PROJECT_AUDIO — Contract Design.

## 7. Existing Motion work

The existing 08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/ is preserved as a research/pilot asset.

It may later be connected into S4 MOTION, but the runtime will not silently inherit it until S1–S3 contracts establish the actual upstream handoff requirements.

## 8. Success condition for the runtime

The runtime succeeds only when one real MV can travel through all seven stages while demonstrating:

- small active context;
- verified stage state;
- compact handoffs;
- local retries;
- selective rebuild;
- targeted archive lookup;
- no silent state progression;
- human review only at high-value gates.