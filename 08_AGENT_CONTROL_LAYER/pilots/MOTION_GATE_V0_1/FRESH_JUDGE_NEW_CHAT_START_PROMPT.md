# Fresh Judge Blind Baseline — New Chat Start Prompt

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch:

`main`

This is a **blind benchmark execution** for:

`08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1`

## Critical isolation rule

You are the **Stateless Motion Judge**.

Do NOT search for, open, read, infer from, or reference:

- `CONTRASTIVE_ANSWER_KEY_v0.1.jsonl`
- `BASELINE_RESULTS_TEMPLATE.md`
- previous conversations about how these cases were designed
- archived project discussions
- executor rationale
- any file whose purpose is to reveal expected labels

If the answer key becomes visible for any reason, STOP and mark the run INVALID.

## Files you are allowed to read

Read exactly these three files:

1. `MOTION_STAGE_CONTRACT_v0.1.yaml`
2. `MOTION_JUDGE_CONTRACT_v0.1.yaml`
3. `CONTRASTIVE_FIXTURES_v0.1.jsonl`

You may also read this start prompt itself.

Do not read other repository files unless a fixture explicitly cannot be interpreted from the allowed material. If that happens, return `INSUFFICIENT_EVIDENCE`; do not broaden context.

## Task

Evaluate all 40 cases contained in the 20 contrastive fixture pairs.

Important:
- Treat A and B as independent cases.
- Do not assume one must be TRUE because the other is FALSE.
- Do not produce explanations.
- Do not use numeric confidence.
- Do not rewrite prompts.
- Do not diagnose creatively.
- Judge only the fixture's target criterion.
- Apply the Judge Contract literally.

## Output format

Return exactly one JSONL record per case, 40 lines total:

```json
{"case_id":"MG001_A","criterion":"J02_grounded_displacement","prediction":"TRUE","route":"PASS"}
```

Allowed prediction values:

```text
TRUE
FALSE
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

Route must be derived from the contract:

- critical FALSE -> REVISE
- critical INSUFFICIENT_EVIDENCE -> ESCALATE
- evidence-sufficiency failure -> ESCALATE
- otherwise -> PASS

For J08/J09 noncritical cases, a FALSE answer does not by itself cause REVISE.

## Save result

After producing all 40 predictions, create this file in the same GitHub folder:

`BLIND_PREDICTIONS_RUN01.jsonl`

Do not score it.

Do not read the answer key after saving predictions.

Then create/update:

`BLIND_RUN01_STATUS.md`

with:

```text
Status: PREDICTIONS_FROZEN
Judge model: <current model>
Judge contract: MOTION_JUDGE v0.1
Fixture set: CONTRASTIVE_FIXTURES v0.1
Cases: 40
Answer key accessed: NO
Scoring performed: NO
```

Stop there.

The scoring step must occur in a separate context after predictions have been frozen.
