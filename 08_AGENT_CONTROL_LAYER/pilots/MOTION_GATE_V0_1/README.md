# Motion Gate v0.1 — First Real Agent-Control Pilot

Status: `DRAFT_READY_FOR_BASELINE`  
Date: 2026-09-22

## Purpose

This pilot validates one question only:

> Can GPT-5.6, used as a fresh stateless typed Judge, make the Dynamic Prompt / Motion stage more reliable and modular than long-context self-review?

The pilot does **not** train Laya, deploy Nimble, or refactor the whole MV workflow.

## Existing project evidence used

This pilot is based on already locked or observed repository rules:

- `MV_CURRENT_EXECUTION_HARNESS.md / C7`:
  - no unsupported foot sliding/drifting;
  - displacement should come from foot lift -> plant -> push-off -> center-of-gravity transfer -> acceleration/deceleration;
  - if foot information is insufficient, prefer stable stance, hip/shoulder/torso/center-of-gravity motion rather than inventing unreadable locomotion.
- `DEPTH_MOTION_HARNESS.md`:
  - if validating foot sliding / weight landing, feet and ground contact must be readable.
- Real generation evidence in `11_LOVE_EMPTY_HEAD_GENERATION_QA_ROUND01.md`:
  - the locomotion section with explicit leg cycling and grounded foot positions produced no obvious whole-body sliding in sampled frames;
  - the tail did not settle as requested, proving that end-state/settling is a real independent criterion;
  - prompt timestamps behaved as soft choreography rather than frame-accurate edit contracts.
- Current workflow rule:
  - after a failure, change one main variable rather than rewriting every layer.

## Files

- `MOTION_STAGE_CONTRACT_v0.1.yaml`
- `MOTION_JUDGE_CONTRACT_v0.1.yaml`
- `MOTION_HANDOFF_CONTRACT_v0.1.yaml`
- `CONTRASTIVE_TESTSET_v0.1.jsonl`
- `BASELINE_RUNBOOK.md`

## Core flow

```text
sealed upstream handoff
        |
        v
GPT-5.6 Motion Executor
        |
        v
dynamic prompt candidate
        |
        v
deterministic checks
        |
        v
GPT-5.6 Fresh Stateless Judge
(minimal context only)
        |
        v
atomic results
        |
        v
deterministic route
 PASS / REVISE / ESCALATE
        |
        v
if PASS -> seal -> compact motion handoff
```

## Non-goals

This v0.1 does not judge:
- final rendered video aesthetics;
- final character identity from pixels;
- lip sync;
- exact generated timecodes;
- final edit rhythm;
- Dola watermark;
- generated audio/BGM quality.

Those belong to later gates. The first pilot stays deliberately narrow.
