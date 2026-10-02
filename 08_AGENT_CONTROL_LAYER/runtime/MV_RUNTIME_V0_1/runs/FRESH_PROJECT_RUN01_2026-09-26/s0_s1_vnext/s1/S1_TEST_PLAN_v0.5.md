# S1 v0.5 test plan

Status: `NOT_STARTED / BLOCKED_BY_S0`.

After S0 seal, test in this order:

1. Regression fixtures: wrong version, partial source, instrumental/vocalise-only region, ASR hallucination, dirty phrase boundary, human FAIL override.
2. Full-source fixture: prove complete coverage and no gaps/overlaps in the typed timeline.
3. Real selected Song Family: autonomous acquisition, identity/version/hash lock, whole-song analysis.
4. Candidate derivation: maximum three, each grounded in the timeline and free of blocking unknowns.
5. HG02: deliver actual excerpt audio and readable line/semantic timeline to the user.
6. Seal test: only production user PASS plus fresh judge PASS permits S1 and S2 entry.

