# 07 — First Pilot: Motion Prompt Gate v0.1

## 1. Why this stage first

The Dynamic Prompt / Motion stage is a good first experiment because:

- it is text-first, so perception is not a prerequisite;
- it occurs before expensive video generation;
- we already have recurring failure classes;
- acceptance criteria can be made relatively explicit;
- known historical problems such as unsupported sliding provide useful negative cases.

The pilot should test architecture, not attempt full workflow refactoring.

## 2. Pilot boundary

Input:
- upstream sealed director/shot handoff;
- first-frame handoff when required;
- motion-generation Skill;
- current dynamic prompt.

Output:
- sealed Motion Prompt Handoff, or REVISE/ESCALATE.

Do not include the entire MV project history.

## 3. Candidate critical criteria

### C01 — Required action coverage
All required story/action beats for the shot are represented.

### C02 — Grounded locomotion
When a character changes ground position, the prompt contains a readable physical chain appropriate to the action:
- lift / step / plant / push;
- weight transfer;
- acceleration/deceleration when needed.

The exact wording is not mandatory; the physical relationship is.

### C03 — No unsupported translation
The prompt must not imply unexplained body translation that would likely produce sliding/drifting unless such motion is intentionally required by the scene.

### C04 — Camera definition
The required camera behavior is explicit enough for the generation stage.

### C05 — Dialogue/audio requirement
If upstream contract requires dialogue or voice behavior, it is present and consistent.

### C06 — Continuity/end state
The end state needed by the next shot or edit is represented.

### C07 — Evidence sufficient
The Judge has enough upstream state to evaluate all critical criteria.

## 4. Judge questions

Prefer independent questions:

```text
Q1 Does the prompt cover every required action beat?
Q2 Does any required ground displacement have an explicit plausible physical movement chain?
Q3 Does the prompt contain unsupported sliding/drifting translation?
Q4 Is required camera behavior specified?
Q5 Are required dialogue/audio instructions present?
Q6 Is the required end/transition state specified?
Q7 Is evidence sufficient to make these judgments?
```

Allowed answers:
```text
TRUE
FALSE
INSUFFICIENT_EVIDENCE
NOT_APPLICABLE
```

## 5. Routing

Example deterministic rules:

```text
if Q7 != TRUE:
    ESCALATE
elif Q1 == FALSE:
    REVISE
elif Q2 == FALSE:
    REVISE
elif Q3 == TRUE:
    REVISE
elif Q4 == FALSE:
    REVISE
elif Q5 == FALSE:
    REVISE
elif Q6 == FALSE:
    REVISE
else:
    PASS
```

Judge does not decide to waive a critical rule because other qualities are strong.

## 6. Initial regression suite

Build 20–40 contrastive pairs before production activation.

Minimum families:
- grounded step vs unsupported translation;
- complete action beat vs omitted beat;
- camera defined vs vague camera;
- dialogue required/present vs required/missing;
- end state explicit vs absent;
- evidence complete vs evidence missing.

Include known historical failure patterns whenever possible.

## 7. What to measure

During real pilot runs record:

- active context size;
- judge pass/revise/escalate result;
- human correction;
- generation outcome;
- false pass;
- false reject;
- whether archive had to be reopened;
- whether next stage needed information missing from the handoff.

## 8. Pilot success

Do not call the pilot successful merely because the Judge returns valid JSON.

Success requires evidence that:

1. the Judge catches known motion-prompt defects;
2. next stage can operate from the sealed handoff;
3. full prior project context is normally unnecessary;
4. corrections remain local to the Motion stage;
5. the new process is simpler to maintain than the current long-form review path.

## 9. Explicit non-goals

The pilot does not:
- train Laya;
- deploy Nimble;
- replace video visual QA;
- remove human creative approval;
- refactor every MV stage at once.

The first question is only:

> Can GPT-5.6, used as a fresh stateless typed Judge, make one stage more reliable and more modular?


## Implementation status update — 2026-09-22

The v0.1 implementation package now exists at:

`08_AGENT_CONTROL_LAYER/pilots/MOTION_GATE_V0_1/`

Current status:

`BASELINE_READY / NOT_VALIDATED`

It contains the formal Stage/Judge/Handoff contracts plus a blind 20-pair contrastive regression suite. The next valid step is a fresh-context blind Judge baseline; do not treat document creation as proof that the architecture improves production yet.
