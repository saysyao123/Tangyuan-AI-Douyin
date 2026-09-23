# F0 Runtime Framework — Review Checklist

Status: READY_FOR_REVIEW

## Review objective

Decide whether the framework is stable and small enough to SEALED before S1 PROJECT_AUDIO is designed.

## A. Scope

- [ ] Seven-stage runtime is an appropriate first granularity.
- [ ] No necessary major production phase is missing.
- [ ] No stage is obviously duplicated or unnecessary.
- [ ] Framework remains experimental and does not replace current MV mainline.

## B. Progressive construction rule

- [ ] Only one unsealed stage may be deeply designed at a time.
- [ ] Next-stage design is blocked until upstream delivery is tested and SEALED.
- [ ] Placeholder stages contain no premature detailed implementation.
- [ ] Failed review returns to the same stage instead of advancing.

## C. State truth

- [ ] Project State can represent NOT_STARTED / DESIGNING / TESTING / REVIEW / SEALED / DIRTY / BLOCKED.
- [ ] Model prose alone cannot mark a stage SEALED.
- [ ] Required artifacts/evidence are mandatory for Seal.
- [ ] Reopen requires version change and dependency impact check.

## D. Context control

- [ ] Next stage receives Compact Handoff rather than full history.
- [ ] Executor and Judge contexts are separated.
- [ ] Archive is excluded on the normal path.
- [ ] Targeted archive lookup is available on fault path.

## E. Progress visibility

- [ ] PROGRESS_TRACKER clearly shows current active build target.
- [ ] Every stage has Status / Test / Delivery / Review / Next Action fields.
- [ ] Tracker is simple enough to update after every stage.
- [ ] One glance is enough to know what is allowed next.

## F. Human gates — provisional review

Current provisional gates:

- PROJECT_AUDIO: no mandatory human gate yet
- DIRECTOR: human gate
- FIRST_FRAME: human gate
- MOTION: automated by default
- GENERATION: automated evidence gate by default
- VIDEO_QA: automated/review routing by default
- ASSEMBLY_FINAL: human final gate

Question for F0 review: should PROJECT_AUDIO require a human lock for song/segment selection? This should be decided before S1 contract design.

## G. F0 Seal decision

If all structural issues are acceptable:

F0 status -> SEALED
S1 PROJECT_AUDIO -> DESIGNING

If any structural issue is material:

F0 status -> REVISE
S1 remains NOT_STARTED.

## Explicit rule

Do not begin detailed S1 design in the same step as F0 structural revision. First finish and seal F0.