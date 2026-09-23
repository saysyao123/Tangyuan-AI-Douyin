# Motion Gate Run02 — Independent Scoring Context

Use the connected GitHub repository:

`saysyao123/Tangyuan-AI-Douyin`

Branch: `main`

This is a new scoring context, not a Judge context.

## Read

1. `RUN02_STATUS.md`
2. `PREDICTIONS_RUN02.jsonl`
3. `ANSWER_KEY_v0.2.jsonl`
4. `score_run02.py`
5. `MOTION_JUDGE_CONTRACT_v0.1.yaml`

Confirm:
- status is `PREDICTIONS_FROZEN`;
- predictions contain exactly 54 cases;
- no prediction is modified during scoring.

## Score

Calculate at minimum:

- overall case accuracy;
- accuracy by label;
- accuracy by criterion;
- route accuracy;
- hidden contrastive relation accuracy;
- standalone case accuracy;
- critical false-pass count;
- false-reject count;
- ESCALATE precision/recall or equivalent error counts;
- confusion matrix across TRUE/FALSE/INSUFFICIENT_EVIDENCE/NOT_APPLICABLE.

Also test for any obvious residual shortcut in case ordering or criterion-specific label pattern.

## Interpretation

Do not modify `MOTION_JUDGE v0.1` in this scoring context.

Classify the result as one of:

- `PROCEED_TO_REAL_TASK_PILOT`
- `EXPAND_FIXTURES_AGAIN`
- `INVESTIGATE_CONTRACT`
- `MODEL_LIMITATION_SUSPECTED`

Explain the evidence for the classification.

## Save

Write:

`BLIND_SCORING_RUN02.md`

Do not overwrite Run01 files.
