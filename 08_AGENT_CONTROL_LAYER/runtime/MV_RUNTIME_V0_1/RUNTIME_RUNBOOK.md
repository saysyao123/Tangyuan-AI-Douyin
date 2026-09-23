# MV Runtime v0.1 — Build / Test / Seal Runbook

## 1. Core construction discipline

Build one stage at a time.

Never deeply design Stage N+1 while Stage N is not SEALED.

The workflow for every build stage is:

A. DESIGN
B. ISOLATED TEST PLAN
C. TEST EXECUTION
D. DELIVERY ARTIFACT
E. REVIEW
F. PASS -> SEAL
G. ONLY THEN DESIGN NEXT STAGE

## 2. What design complete means

Before a Stage may enter READY_FOR_TEST, it must have:

- goal;
- input contract;
- output contract;
- required evidence;
- deterministic checks;
- semantic Judge criteria if needed;
- failure routes;
- handoff schema;
- test cases;
- explicit non-goals.

## 3. What test complete means

A Stage test must use a concrete input.

Synthetic tests are allowed for contract logic, but before final Stage sealing it should also use a real or representative project artifact whenever practical.

A test run must produce:

- actual Stage output;
- Judge result;
- failure/route result;
- any human decision required;
- a recorded test report.

## 4. Delivery

Every Stage test must end in a concrete delivery package.

Examples:
- PROJECT_AUDIO: locked clip + timeline handoff
- DIRECTOR: sealed director handoff
- FIRST_FRAME: approved image refs + state handoff
- MOTION: generation-ready prompt + Motion handoff
- GENERATION: actual generated MP4 + technical evidence
- VIDEO_QA: structured QA report + retry/keep route
- ASSEMBLY_FINAL: final video + final QA report

## 5. Review

Review asks only:

- Does this Stage reliably fulfill its Contract?
- Can the next Stage operate from its Handoff?
- Are any rules unnecessary or missing?
- Did testing expose a structural failure?

Do not optimize unrelated stages during review.

## 6. Seal

When accepted:

- status = SEALED
- version = frozen
- handoff = authoritative
- archive = out of active context
- next stage = may enter DESIGNING

## 7. Failed review

If failed: REVIEW -> REVISE -> DESIGNING -> retest.

Do not start the next Stage.

## 8. Runtime framework F0

F0 is the current build stage.

F0 delivery contains:

- runtime folder structure;
- progress tracker;
- project state schema;
- stage registry;
- transition rules;
- context compiler spec;
- runbook;
- stage placeholders.

F0 does not implement any production Stage deeply.

## 9. After F0

If F0 passes: F0 SEALED -> S1 PROJECT_AUDIO DESIGNING.

S1 should then be developed and tested in isolation.

## 10. Rule against architecture creep

When a new concern appears, classify it before adding anything:

- execution method -> Stage Skill
- acceptance rule -> Stage Judge Contract
- project truth -> Project State / Handoff
- deterministic workflow rule -> Transition Rules
- old attempts -> Archive
- regression evidence -> Test dataset/report

If it does not belong to the current Stage, do not add it now.