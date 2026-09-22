# Motion Gate v0.1 — Expected Effect and Architectural Impact

## 1. What changes compared with the current workflow

The existing MV harness already contains useful motion rules and one-variable iteration discipline.

Motion Gate v0.1 does not replace those rules. It changes **how they are enforced**.

### Before
```text
Long project context
+ motion rules inside HARNESS
+ current prompt
-> same model generates
-> same reasoning stream self-reviews
-> continue
```

### Pilot
```text
sealed upstream state
-> GPT generates prompt
-> fresh Judge sees only contract + artifact + evidence
-> atomic decisions
-> deterministic route
-> seal compact handoff
```

## 2. Expected reliability gains

### A. Reduce rule forgetting
The Judge checks explicit atomic criteria instead of depending on the model to remember every long-form rule.

### B. Reduce self-review bias
The Judge does not see the executor's rationale or failed drafts.

### C. Reduce state hallucination
A stage cannot seal because the model says "done." Required inputs/evidence and Judge results must exist.

### D. Reduce context contamination
Superseded rules and historical drafts leave active context after stage sealing.

### E. Catch problems before generation cost
Text-level defects such as:
- unsupported sliding language;
- missing action beats;
- undefined camera behavior;
- unresolved ending pose;
- unavailable reference bindings;

can be rejected before a new video-generation attempt.

### F. Make revision local
A Motion-stage failure returns to Motion only. It should not reopen Song/Director/First Frame unless localization shows the upstream handoff itself is wrong.

## 3. Expected maintenance gains

### Stage contract stability
Internal prompt-writing technique may change without changing downstream consumers.

### Versioned Judge behavior
A Judge contract change becomes a measurable version change rather than an invisible prompt edit.

### Regression tests
The system can answer:
```text
Did v0.2 actually improve judgment?
```
instead of:
```text
Does the new wording feel better?
```

### Dataset creation
Real disagreements and downstream failures become future training data for a specialized Laya/Nimble-style Judge.

## 4. Relationship with existing repository rules

This pilot formalizes existing ideas rather than discarding them:

- `MV_CURRENT_EXECUTION_HARNESS C7` already contains anti-sliding and grounded locomotion rules.
- `C10 One-variable Iteration` already says not to rewrite every layer after one failure.
- `VIDEO_PRODUCTION_HARNESS G8` already says approved segments should not be dragged into unrelated rework.
- `Generation QA Round 01` provides real evidence that grounded leg cycling improved locomotion, while the requested post-handle settling remained imperfect.

The Agent Control Layer converts these from prose guidance into:
```text
contracts + typed judgments + state transitions + regression tests
```

## 5. What the pilot cannot solve

### It cannot guarantee generation obedience
A perfect prompt can still produce a bad video.

Therefore post-generation QA remains required.

### It cannot directly inspect pixels unless visual evidence is supplied
Motion Gate v0.1 is a pre-generation text gate.

### It cannot eliminate same-model correlated error
Executor and Fresh Judge may both use GPT-5.6 and can share model-level blind spots.

### It does not provide calibrated probability
Numeric confidence is intentionally excluded in v0.1.

### It cannot repair a bad upstream contract
If Director handoff is wrong, the Motion Judge may correctly enforce the wrong requirement.
Failure localization must be able to reopen upstream stages.

## 6. Expected end-to-end effect

If the pilot works, the practical change is:

```text
less "remember the whole project"
more "satisfy the current contract"
```

The desired project behavior becomes:

```text
Stage A
-> verified compact result
-> Stage B
-> verified compact result
-> Stage C
```

not:

```text
ever-growing context
-> repeated self-explanation
-> global self-review
-> increasing drift
```

## 7. What counts as evidence that it works

The architecture is not validated by valid JSON.

Evidence must include:
- blind regression results;
- real prompt false-pass/false-reject observations;
- downstream video QA;
- context-size reduction;
- successful local rollback;
- proof that next stage works from compact handoff without full history.

## 8. Strategic value

The pilot creates a stable interface that can later swap Judge backends:

```text
GPT-5.6 Fresh Judge
      |
      +-- future Laya compiled Judge
      |
      +-- future Nimble/Qwen Judge
```

The workflow contract remains unchanged.

Therefore the main asset being built is not a particular model. It is a **testable decision architecture**.
