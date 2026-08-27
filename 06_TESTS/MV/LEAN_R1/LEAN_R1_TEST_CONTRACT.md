# LEAN_R1｜Real MV Test Contract v1

Status: `READY_FOR_D03-A / NOT STARTED`
Branch: `test/mv-lean-r1`
Baseline: latest clean `test/mv-web-r3` + selective OSS_OPT_R1 promotion only
Test slot: `D03-A / Lane P`

## 1. Experiment question

Can one normal new MV reach `S16_RELEASE_PACKAGE_READY` with the same five Human Gates, the same canonical correctness and no creative-quality regression, while materially reducing user-visible Runtime/Bridge interactions and repository noise?

This is a **process-efficiency experiment**, not a new visual-style experiment.

## 2. Fixed controls

Keep unchanged:
- Canonical S00-S18 evidence/state semantics for this test;
- HG01 Song;
- HG02 BGM excerpt;
- HG03 first-frame/visual direction;
- HG04 picture rhythm;
- HG05 final acceptance;
- exact BGM identity and canonical lyric clock;
- Patch, Don't Cascade;
- TRIM BEFORE REGENERATE;
- actual K0/source pixels outrank stale prose;
- S17 requires real-world publish confirmation.

## 3. Lean variables under test

### V1 Macro transport
Use `RUN_UNTIL_GATE_OR_BLOCK` to compress consecutive already-ready machine transitions. It must never fabricate missing artifacts. First missing prerequisite = BLOCK.

### V2 Gate acceptance transport
Use `ACCEPT_GATE` as one external request while preserving internal durable two-phase semantics: record gate receipt, then canonical advance.

### V3 Thin startup
A new chat should normally need only:
1. this test/start file;
2. one Lean `RESUME` request/response;
3. current executor JIT files returned by the response.

Do not preload all R1/R2/R3 history.

### V4 Conditional normalization
Run full atomization / WEB rough-cut / proxy normalization only when actual source/context requires it.

### V5 Edit audio invariant
Treat editor audio revalidation as a cheap identity invariant. No new lyric clock and no heavy standalone work when the locked BGM identity is unchanged.

### V6 Auto-chain finish
After HG04, subtitles and Final Tech QA should run as machine work and surface only at HG05 unless blocked.

## 4. Selectively promoted knowledge

Use `04_HARNESS/knowledge/MV_DIRECTOR_LEAN_OVERLAY.md`:
- Director Thesis;
- Primary Visual Engine;
- audiovisual relationship;
- motive-first camera/subject/space;
- WHY CUT HERE;
- optional-element stop condition;
- Creative Drift QA.

These are test knowledge, not stable hard rules yet.

Rejected from universal core:
- H3 10–15s integer containers;
- H3 four-panel Picture-1 packaging;
- RunningHub/H3 orchestration;
- D02-B-specific character/world/props/composition.

## 5. Audio route

Priority is:
`P0 SAME-VERSION TIMED LYRIC -> P1 LIGHTWEIGHT ASR MAPPING -> P2 HEAVY FORCED ALIGNMENT ONLY ON FAILURE`.

Stop at first PASS. Do not run multiple aligners for reassurance.

## 6. D03-A creative isolation

D03-A must be a completely new song/visual world selected through HG01.
Do not inherit D02-B's male character, coast, pale stone, curtain, rain aftermath, white linen, or `握住 -> 松手 -> 世界打开` visual progression.

Only general promoted production knowledge may carry forward.

## 7. Metrics

Record at least:
- startup read/call count before HG01;
- external Lean Runtime command count to S16;
- Human Gate count;
- unexpected manual RESUME count;
- number of machine stages compressed by macros;
- normalization used? why?;
- regeneration count;
- number of new helper/model installations created for the slot;
- HG03/HG04/HG05 result;
- any rollback and whether nearest-layer repair worked.

Targets:
- fixed Human Gates = 5;
- startup reads/calls before actionable state <= 3;
- external controller cycles to S16 <= 12, excluding external video generation/upload actions;
- per-slot core helper creation = 0;
- per-song new production model route = 0;
- no chat-only PASS;
- no fabricated publication state;
- final quality no worse than current R3/D02-B accepted bar.

## 8. PASS / FAIL

PASS only if one real D03-A MV reaches S16 and correctness is preserved while interaction overhead is materially reduced.

FAIL if:
- speed comes from bypassing evidence/Gates;
- quality materially regresses;
- macros silently advance through missing artifacts;
- a new slot-specific core helper/model route is created;
- user-visible workflow remains essentially as slow as the current 19-stage transport pattern.

## 9. Promotion boundary

Even if D03-A passes, do not merge `test/mv-lean-r1` wholesale into `main`.
First prepare a clean promotion diff against latest `test/mv-web-r3`, run regressions, and write a deployment receipt.
