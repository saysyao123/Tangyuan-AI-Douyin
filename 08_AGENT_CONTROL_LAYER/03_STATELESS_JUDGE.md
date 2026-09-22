# 03 — Stateless Judge Protocol

## 1. Objective

The first production Judge should use GPT-5.6 in a **fresh, short-lived context**.

The objective is not to imitate Jev latency. It is to obtain:
- independent review;
- bounded output;
- reduced context contamination;
- explicit insufficient-evidence handling;
- measurable judgment quality.

## 2. Judge request contract

A Judge receives only:

```yaml
judge_contract_version:

stage:
goal:

acceptance_criteria:

locked_rules:

artifact:

evidence:

questions:
```

It must not receive:
- executor rationale;
- discarded drafts;
- full chat transcript;
- unrelated earlier stage history;
- "why this should probably pass" explanations.

## 3. Atomic answer types

### Boolean-like / Noul-style
Preferred for critical checks:

```text
TRUE
FALSE
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

### Choice
Use a small candidate set:

```text
PASS
REVISE
ESCALATE
```

Prefer fewer than ~10 options; most workflow gates should use 2–4.

### Score
Use only when an ordered scale is genuinely required and criteria are explicit.

Avoid vague:
```text
quality = 7/10
```

Prefer:
```text
0 = clearly unusable
1 = blocking defect
2 = usable with revision
3 = meets contract
```

## 4. Explicit unknown state

Never force the Judge to choose PASS/FAIL when evidence can be incomplete.

```text
INSUFFICIENT_EVIDENCE
```

is a valid and important result.

This prevents:
```text
missing evidence -> forced guess -> hallucinated state transition
```

## 5. Flat, independent questions

Avoid questions that depend on previous Judge answers.

Bad:
```text
Q1 Does the clip contain dialogue?
Q2 If Q1 is yes, is lip sync correct?
```

Better:
```text
Q1 Does available evidence show dialogue is present?
Q2 For any observed dialogue interval, does evidence show a blocking lip-sync mismatch?
```

Program logic handles applicability.

## 6. Overall route should be deterministic when possible

Example:

```yaml
judge_result:
  motion_grounded: TRUE
  identity_consistent: TRUE
  dialogue_complete: FALSE
  evidence_sufficient: TRUE
```

Then code/state rule:

```text
if evidence_sufficient != TRUE:
    ESCALATE
elif any critical criterion == FALSE:
    REVISE
else:
    PASS
```

Do not ask GPT to override a critical failure because "overall quality is good."

## 7. Judge output format

Recommended internal structure:

```json
{
  "contract_version": "motion_gate_v0.1",
  "results": {
    "motion_grounded": "TRUE",
    "no_unsupported_translation": "FALSE",
    "camera_defined": "TRUE",
    "evidence_sufficient": "TRUE"
  },
  "failed_criteria": [
    "no_unsupported_translation"
  ]
}
```

No essay is required.

If diagnosis is needed, invoke a separate diagnostic call after the gate result.

## 8. Judge vs Diagnostic Agent

### Judge
Answers:
- does it pass?
- which criterion failed?
- is evidence sufficient?

### Diagnostic Agent
Answers:
- why did it fail?
- how should it be repaired?
- what new prompt should be written?

Do not merge these responsibilities in the first implementation.

## 9. Same model, separate context

The initial implementation may use GPT-5.6 for both:

```text
Executor GPT-5.6
Judge GPT-5.6
```

The independence comes from:
- fresh call;
- different system/task contract;
- minimal input;
- no executor rationale;
- typed output.

This reduces context bias, but does not eliminate correlated model errors. Regression tests and human ground truth are still required.

## 10. Confidence policy

Do not treat a generated number such as `0.93` as a calibrated probability.

For v0.1, prefer:
- explicit UNKNOWN/INSUFFICIENT_EVIDENCE;
- independent repeat judgments in high-risk gates;
- disagreement-based escalation;
- empirical error rates from regression datasets.

Probability thresholds should be introduced only after calibration is measured on held-out project data.

## 11. High-value first Judge candidates

For MV/video workflows:

### Dynamic Prompt Gate
- required action covered?
- grounded locomotion described?
- unsupported sliding language present?
- required dialogue present?
- camera behavior specified?
- transition/end state specified?

### Stage Seal Gate
- output contract complete?
- locked rules satisfied?
- blocking issue present?
- evidence sufficient?

### Retry Router
- keep result?
- revise prompt?
- regenerate current shot?
- escalate to human/deep diagnosis?

## 12. Anti-patterns

Do not:
- use the same long conversation as "fresh review";
- ask "review everything" with unlimited output;
- ask the Judge to invent missing evidence;
- let a Judge modify project state directly;
- let a Judge silently change acceptance criteria;
- allow old archived requirements to leak into current criteria;
- use model-generated confidence as proof of correctness.
