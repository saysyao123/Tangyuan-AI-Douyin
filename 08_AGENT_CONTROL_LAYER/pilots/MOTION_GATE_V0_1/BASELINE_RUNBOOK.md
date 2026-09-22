# Motion Gate v0.1 — Blind Baseline Runbook

## Purpose

Run the first valid baseline without leaking answer keys or long project history into the Judge.

## A. Judge context

Use a fresh GPT-5.6 context.

Load only:
1. `MOTION_STAGE_CONTRACT_v0.1.yaml`
2. `MOTION_JUDGE_CONTRACT_v0.1.yaml`
3. `CONTRASTIVE_FIXTURES_v0.1.jsonl`

Do **not** load:
- `CONTRASTIVE_ANSWER_KEY_v0.1.jsonl`
- full MV conversation history;
- executor rationale;
- old prompt drafts;
- the Generation QA document unless a specific fixture explicitly includes evidence derived from it.

## B. Blind evaluation procedure

For every fixture pair:

1. Treat case A and case B as independent cases.
2. Ideally randomize their presentation order.
3. Do not tell the Judge that two cases form a contrastive pair.
4. Ask only for the target criterion's allowed answer.
5. Apply the deterministic route outside the Judge.
6. Store raw predictions.

Recommended prediction record:

```json
{
  "case_id": "MG001_A",
  "criterion": "J02_grounded_displacement",
  "prediction": "TRUE",
  "route": "PASS"
}
```

## C. Scoring step

Only after all predictions are frozen may a separate scoring step read:
- `CONTRASTIVE_ANSWER_KEY_v0.1.jsonl`

Calculate:

### Case Accuracy
Correct individual answers / 40 cases.

### Pair Accuracy
A pair counts correct only when both A and B are correct.

### Route Accuracy
Correct PASS / REVISE / ESCALATE result.

### Critical False Pass
Expected REVISE or ESCALATE, but system routes PASS.

### False Reject
Expected PASS, but system routes REVISE.

### Insufficient-Evidence Behavior
Judge must not invent missing first-frame facts.

## D. Why answer isolation matters

If the same Judge sees expected labels before prediction, the baseline is invalid.

The answer key is for scoring only.

## E. First baseline interpretation

Do not tune the Judge after every single error.

After the complete blind run:
1. group errors by criterion;
2. distinguish bad question wording from actual model limitation;
3. identify whether the contract lacks necessary evidence;
4. change only one major Judge variable at a time;
5. rerun the whole blind suite.

## F. Activation rule

v0.1 is a research pilot. No production activation threshold is locked before the first blind baseline.

After the first run, define thresholds using:
- critical false-pass risk;
- pair accuracy;
- error concentration;
- actual downstream cost.

The system should prioritize reducing critical false passes over maximizing a single aggregate accuracy number.

## G. Real-task validation after regression

A good synthetic/contrastive score is not sufficient.

After the blind suite is stable:
1. take one real current dynamic prompt;
2. run Executor normally;
3. send only final artifact + contract/evidence to Fresh Judge;
4. route PASS/REVISE/ESCALATE deterministically;
5. if PASS, generate the video;
6. compare the generated result with post-generation QA;
7. log any case where pre-generation Judge PASS still led to a motion failure.

Those false passes become high-value future regression cases.
