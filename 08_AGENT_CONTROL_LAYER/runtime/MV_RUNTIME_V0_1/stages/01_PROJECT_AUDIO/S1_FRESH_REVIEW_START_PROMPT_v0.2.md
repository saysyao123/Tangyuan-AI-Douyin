# S1 PROJECT_AUDIO v0.2 — Fresh Review Start Prompt

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch: `main`

This is an independent Stateless Judge review of S1 PROJECT_AUDIO.

## Read only

1. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_STAGE_CONTRACT_v0.2.yaml`
2. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_JUDGE_CONTRACT_v0.2.yaml`
3. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_DELIVERY_RUN02_v0.2.yaml`
4. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_TEST_REPORT_RUN02_v0.2.md`

Evidence files may be read only to verify explicit claims:
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`

Do not read:
- previous conversation history;
- v0.1 S1 experiment files;
- S2 design;
- unrelated project archive.

## Judge

Evaluate J01–J05 exactly according to `S1_JUDGE_CONTRACT_v0.2.yaml`.

Write:

`S1_FRESH_REVIEW_RUN02_v0.2.yaml`

Format:

judge:
  judge_id: PROJECT_AUDIO_JUDGE
  contract_version: "0.2"
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

Do not redesign the stage.

If PASS, update `S1_STATUS.md` to:
- Status: REVIEW_PASS
- Candidate Contract: v0.2
- Ready to Seal: YES

Stop. Do not start S2.
