# 04 — Judge Data, Contrastive Regression, and Future Training

## 1. Why tests are required

Judge prompts and Skills must not be maintained by intuition alone.

A change is "better" only if it improves measured behavior on stable tests without unacceptable regressions.

## 2. Contrastive pair principle

Create two cases that are nearly identical except for one decisive fact, and require the expected decision to flip.

Example:

### MOTION_001_A
```text
Actor pushes off the right foot, left foot lifts and lands,
hips translate forward, center of gravity follows the step.
```
Expected:
```text
motion_grounded = TRUE
```

### MOTION_001_B
Only change the decisive fact:
```text
Actor keeps the same pose and rapidly translates to the right.
```
Expected:
```text
motion_grounded = FALSE
```

The pair tests whether the Judge detects the actual boundary, rather than guessing from topic/style.

## 3. Test families

Each Judge Contract should eventually contain:

- Positive cases
- Negative cases
- Counterfactual pairs
- Insufficient-evidence cases
- Not-applicable cases
- Boundary/ambiguous cases
- Known historical failures
- Adversarial wording variants
- Option-order variants where applicable

## 4. Core metrics

Do not rely only on overall accuracy.

Track:

### Pair Accuracy
Both members of a contrastive pair must be correct.

### Critical False Pass Rate
```text
should FAIL -> Judge says PASS
```

For production gates this is often more dangerous than false rejection.

### False Reject Rate
```text
should PASS -> Judge says FAIL
```

This costs retries but may be safer than false pass.

### Insufficient-Evidence Accuracy
Does the Judge correctly refuse to decide when required evidence is missing?

### Stability
Does paraphrasing irrelevant wording change the decision?

### Option-order sensitivity
Does changing candidate order alter the answer?

## 5. Versioned regression

Every Judge Contract has a version:

```text
MOTION_GATE v0.1
MOTION_GATE v0.2
```

Any meaningful change to:
- acceptance criteria;
- question wording;
- answer schema;
- model;
- system instructions;

must rerun its regression suite.

Record:

```yaml
judge_version:
model:
test_suite_version:
pair_accuracy:
critical_false_pass_rate:
false_reject_rate:
notes:
```

## 6. Real project data logging

Each production run should be able to generate a record such as:

```yaml
case_id:
stage:
contract_version:

input_summary:
artifact_ref:
evidence_refs:

executor_output:

judge_result:

human_final_decision:

observed_downstream_outcome:

correction:
failure_category:
```

The most valuable cases are often disagreements:

```text
GPT Judge != human final decision
```

and:

```text
Judge PASS -> downstream result fails
```

## 7. Ground truth hierarchy

Prefer labels in this order when available:

1. verified physical/tool fact;
2. explicit user approval/rejection;
3. measured downstream outcome;
4. independent expert/human review;
5. GPT-generated label.

Do not train a future independent Judge only on labels produced by the same GPT that it is supposed to check.

## 8. Future Laya/Nimble training trigger

Do not train merely because training is possible.

A Gate becomes a candidate when:
- definition has remained stable;
- decisions repeat frequently;
- enough high-quality labels exist;
- the cost of Fresh GPT judging is meaningful;
- regression suite is already strong;
- human correction rate is understood.

Suggested first candidate: one narrow Motion Prompt Gate, not a universal Judge.

## 9. Dataset splits

When training begins, separate:
- training set;
- validation set;
- calibration set;
- final test set.

Never report training-set performance as proof of production reliability.

## 10. Data is a by-product of good workflow design

The Stage Seal architecture should collect useful judgment data automatically during real work.

The project should not interrupt normal production merely to manufacture a large synthetic dataset unless a specific research question requires it.
