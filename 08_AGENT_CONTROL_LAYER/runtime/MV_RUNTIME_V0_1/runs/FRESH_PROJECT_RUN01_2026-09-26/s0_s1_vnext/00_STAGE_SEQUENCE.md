# Stage sequence

1. Build the S0 contract and deterministic validator.
2. Pass S0 regression tests.
3. Evaluate actual current evidence.
4. Refresh references until at least one eligible direction is genuinely reviewable.
5. Human Gate HG01 locks one Song Family. Only a production human decision may seal S0.
6. Implement and test S1 against that sealed handoff.
7. In S1, acquire the exact full source, lock its version, analyze the **entire** song timeline, derive review excerpts, and run Human Audio Lock HG02.
8. Only after HG02 PASS may S1 be sealed and S2 begin.

`review_excerpt` is produced after the full timeline and is an input to HG02. `locked_final_audio` exists only after HG02 PASS. Test automation can exercise gates but cannot impersonate either production human decision.

