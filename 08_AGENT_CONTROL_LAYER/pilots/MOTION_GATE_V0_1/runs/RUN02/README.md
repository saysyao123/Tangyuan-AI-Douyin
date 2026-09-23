# Motion Gate Blind Regression Run02

Status: `READY_FOR_FRESH_JUDGE`

## Why Run02 exists

Run01 scored 40/40, but every visible pair had the same positional polarity:

```text
A = TRUE
B = FALSE
```

Therefore Run01 demonstrated consistency with the answer key but did not exclude a trivial positional shortcut.

Run02 changes the benchmark without changing `MOTION_JUDGE v0.1`.

## Run02 design

- 54 total independent cases.
- J01–J09: exactly 6 cases each.
- No visible A/B case identifiers.
- Pair membership is hidden from the Judge.
- 36 cases belong to hidden contrastive relations.
- 18 are standalone cases.
- Expected labels include:
  - TRUE
  - FALSE
  - INSUFFICIENT_EVIDENCE
  - NOT_APPLICABLE
- Weak lexical-boundary cases are included.
- Several cases test whether camera/environment movement is confused with character translation.
- Several cases deliberately require the Judge to refuse inference when upstream state is unresolved.
- Noncritical J08/J09 FALSE/UNKNOWN cases test whether routing remains PASS when appropriate.

## Locked variable

Judge Contract remains:

`MOTION_JUDGE_CONTRACT_v0.1.yaml`

Stage Contract remains:

`MOTION_STAGE_CONTRACT_v0.1.yaml`

Run02 is a fixture-quality test, not a contract rewrite.

## Files

- `FIXTURES_v0.2.jsonl` — Judge-visible cases only
- `ANSWER_KEY_v0.2.jsonl` — scoring only
- `FRESH_JUDGE_START_PROMPT.md`
- `SCORING_START_PROMPT.md`
- `score_run02.py`
- `RUN02_STATUS.md`

## Promotion rule

Do not promote Motion Gate to a real-task pilot solely on overall accuracy.

Review especially:

- Critical False Pass
- ESCALATE correctness
- TRUE/FALSE/UNKNOWN/NA confusion
- hidden contrastive-pair accuracy
- standalone accuracy
- errors concentrated by criterion

If Run02 is strong, the next step is **one real current Motion Prompt**, not another synthetic benchmark expansion by default.
