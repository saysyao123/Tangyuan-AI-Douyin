# S1 PROJECT_AUDIO — Fresh Review Start Prompt

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch: `main`

This is an independent review context for:

`08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO`

## Allowed files

Read only:

1. `S1_STAGE_CONTRACT_v0.1.yaml`
2. `S1_JUDGE_CONTRACT_v0.1.yaml`
3. `S1_DELIVERY_RUN01.yaml`
4. `S1_TEST_REPORT_RUN01.md`

You may read the evidence files explicitly referenced by the delivery/report only to verify claims:
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/09_LOVE_EMPTY_HEAD_K0_SPEC_v1.md`
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`

Do not read:
- prior chat history;
- S2 design materials;
- unrelated MV archive;
- superseded audio-selection discussions.

## Task

Judge J01–J05 exactly according to `S1_JUDGE_CONTRACT_v0.1.yaml`.

Return only:

`S1_FRESH_REVIEW_RUN01.yaml`

with:

judge:
  judge_id: PROJECT_AUDIO_JUDGE
  version: "0.1"
  model: "<current model>"
  results:
    J01: TRUE|FALSE|INSUFFICIENT_EVIDENCE|NOT_APPLICABLE
    J02: TRUE|FALSE|INSUFFICIENT_EVIDENCE|NOT_APPLICABLE
    J03: TRUE|FALSE|INSUFFICIENT_EVIDENCE|NOT_APPLICABLE
    J04: TRUE|FALSE|INSUFFICIENT_EVIDENCE|NOT_APPLICABLE
    J05: TRUE|FALSE|INSUFFICIENT_EVIDENCE|NOT_APPLICABLE
  route: PASS|REVISE|ESCALATE

Routing:
- any critical FALSE -> REVISE
- any critical INSUFFICIENT_EVIDENCE -> ESCALATE
- all critical TRUE -> PASS
- J03 is noncritical

Do not redesign S1 in the same review context.

## If route = PASS

Update:
`S1_STATUS.md`

to:
- Status: REVIEW_PASS
- Ready to Seal: YES

Stop.

Do not start S2.
