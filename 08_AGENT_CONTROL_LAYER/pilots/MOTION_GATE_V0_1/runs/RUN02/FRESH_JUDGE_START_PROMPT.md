# Motion Gate v0.1 — Fresh Blind Regression Run02

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch: `main`

This is a new, blind Stateless Judge context.

## Allowed files

Read exactly:

1. `08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/MOTION_STAGE_CONTRACT_v0.1.yaml`
2. `08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/MOTION_JUDGE_CONTRACT_v0.1.yaml`
3. `08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/runs/RUN02/FIXTURES_v0.2.jsonl`

Do not read any other file from the pilot.

Specifically prohibited:

- `ANSWER_KEY_v0.2.jsonl`
- any Run01 prediction or scoring file
- prior conversation history about fixture construction
- any design note describing expected labels

If prohibited material becomes visible, stop and mark the run INVALID.

## Task

Judge all 54 cases independently.

Each fixture already specifies the target criterion.

Do not:
- infer relationships between cases;
- search for paired examples;
- use numeric confidence;
- explain answers;
- rewrite prompts;
- broaden context;
- invent missing evidence.

Allowed predictions:

```text
TRUE
FALSE
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

Use the Judge Contract semantics literally.

## Route

Return the route that follows from the contract and the target criterion, assuming all other stated-valid criteria remain valid.

Examples of routing logic:
- critical FALSE -> REVISE
- critical INSUFFICIENT_EVIDENCE -> ESCALATE
- J07 FALSE -> ESCALATE
- noncritical J08/J09 FALSE, INSUFFICIENT_EVIDENCE, or NOT_APPLICABLE -> PASS
- otherwise -> PASS

## Output

Create exactly 54 JSONL records:

```json
{"case_id":"R2_001","criterion":"J03_no_unsupported_translation","prediction":"TRUE","route":"PASS"}
```

Write them to:

`08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/runs/RUN02/PREDICTIONS_RUN02.jsonl`

Then update:

`RUN02_STATUS.md`

to:

```text
Status: PREDICTIONS_FROZEN
Judge model: <current model>
Judge contract: MOTION_JUDGE v0.1
Fixture set: FIXTURES v0.2
Cases: 54
Answer key accessed: NO
Scoring performed: NO
```

Stop. Do not score in this context.
