# S1 PROJECT_AUDIO — Test Plan v0.1

## Objective

Validate that PROJECT_AUDIO can establish a stable timeline truth and hand it to DIRECTOR without leaking downstream creative decisions.

## Representative real project

Use the already executed project:

《爱让人脑袋空空》

Primary evidence:
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
- `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/09_LOVE_EMPTY_HEAD_K0_SPEC_v1.md`
- later downstream artifacts as consumption evidence only

## Test questions

### Deterministic
1. Is one audio version authoritative?
2. Does start/end produce the locked duration?
3. Does the timeline cover 0.000 through 15.370998 without material gaps?
4. Are timeline units ordered?
5. Is target aspect ratio explicit?
6. Is a Human Lock present?

### Semantic
1. Are lyric units complete across the selected range?
2. Is 8.700s a meaningful semantic boundary?
3. Can a Director use the handoff without rereading the source-selection history?
4. Does the proposed handoff avoid generation duration / shot count / visual creative decisions?

## Pass requirement

S1 may SEALED only if:
- all deterministic checks pass;
- J01/J02/J04/J05 pass;
- Human Lock passes;
- representative handoff is sufficient for downstream use.

## Important

S1 does not need to prove that later Director or Seedance generation is good.
It only needs to prove that all downstream stages can rely on one correct media/timeline truth.
