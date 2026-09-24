# S0 SONG_SELECTION — Test Plan v0.1

## Test 1 — Historical successful-path reconstruction

Use:
- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`
- `04_SELECTION_ROUND_01.md`

Expected:
- shortlist contains no more than 3 primary candidates;
- each has a concrete reference;
- selection reasons/risks are visible;
- candidate logic can explain why A/B/C were surfaced;
- user selection of 《爱让人脑袋空空》 can be represented as Human Reference Lock;
- handoff contains only selection truth, not S1 timeline analysis.

## Test 2 — Boundary regression

Verify that S0 does NOT contain:
- exact 15.370998s Audio Version lock;
- T00–T12 timeline;
- 8.700s semantic cut;
- 12s/10s generation durations;
- Director shots.

Those belong downstream.

## Test 3 — Reject-all route

Construct or replay a round where user rejects all candidates.

Expected:
- S0 remains open;
- no song is auto-selected;
- next round is requested from trusted pool;
- S1 remains blocked.

## Test 4 — Version ambiguity

Use a song family with clearly different cover/remix variants.

Expected:
- S0 may shortlist the family and a concrete work;
- version risk is surfaced;
- no exact Audio Version is claimed before user locks one concrete reference and S1 begins.

## Seal requirement

S0 must demonstrate:
1. stable shortlist construction;
2. no more than 3 primary candidates;
3. concrete reference evidence;
4. user retains final choice;
5. reject-all works;
6. clean handoff into S1;
7. no timeline-analysis leakage.
