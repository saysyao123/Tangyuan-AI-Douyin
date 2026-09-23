# Motion Gate v0.1 — Scoring Context Start Prompt

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch: `main`

This is **not a judging run**. Predictions must already be frozen.

## Read

From:

`08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/`

read:

1. `BLIND_PREDICTIONS_RUN01.jsonl`
2. `CONTRASTIVE_ANSWER_KEY_v0.1.jsonl`
3. `BASELINE_RESULTS_TEMPLATE.md`
4. `score_baseline.py`
5. `BLIND_RUN01_STATUS.md`

Verify status says:
`PREDICTIONS_FROZEN`

If predictions are missing or the status does not confirm answer-key isolation, mark the run INVALID.

## Score

Score deterministically. Calculate:

- Case Accuracy
- Pair Accuracy
- Route Accuracy
- Critical False Pass count/rate
- False Reject count/rate
- Insufficient-Evidence routing accuracy
- Errors by criterion

Do not retroactively change any prediction.

## Save

Write the completed result to:

`BASELINE_RESULTS_RUN01.md`

Then update `BLIND_RUN01_STATUS.md` to:

```text
Status: SCORED
Predictions frozen before answer-key access: YES
Scoring complete: YES
```

Do not revise the Judge Contract in the same scoring step.

After scoring, report which criterion families require investigation. Contract revision is a separate stage.
