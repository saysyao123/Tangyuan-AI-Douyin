# CODEX R2｜Execution Contract v1.0

Status: `CANDIDATE / REAL-MV TEST`
Branch: `test/mv-codex-r2`
Baseline: `test/mv-lean-r1 @ 6a02cff5be943488800f0d63bb2f91ef4f3cbd32`
Target: `D03-B / Lane S`

## 1. Purpose

This test answers one question: can Codex, from repository truth and minimal user input, operate the current Tangyuan Music MV workflow end-to-end without relying on chat memory or inventing a parallel automation system?

Unlike historical CODEX_R1, this is not a Golden-Sample reconstruction exercise. It is a fresh real MV using the current Canonical Runtime, Lean executor model, five Human Gates, current audio timeline route, current director layer, source QA/editing/subtitle/final QA, and Release Package boundary.

## 2. Architectural rule

Codex R2 changes transport, not truth.

ChatGPT Web requires immutable GitHub request -> Actions -> response transport. Codex has a local repository checkout and shell, so its default transport is the local operator:

`python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py ...`

The operator delegates to existing `mv_runtime_bridge.py`, `mv_runtime_lean_bridge.py`, `mv_runtime_state.py`, stage registry, validators and receipts. It must never become a second state authority.

## 3. Startup

From repository root:

```bash
git branch --show-current
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py preflight
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py resume --slot D03-B
```

Expected first real result on a clean Codex R2 branch is `ALLOCATE_NEW_SLOT / D03-B / Lane S`.

If allocation is returned, initialize exactly once:

```bash
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py init --slot D03-B
```

Then resume again. Expected canonical state after valid initialization:
`S00_SLOT_CREATED / SLOT_CREATED` with next Human Gate HG01.

Do not initialize if the fresh resume already returns `RESUME_CANONICAL`.

## 4. Runtime operating loop

For every phase:

1. `resume --slot D03-B` once at the beginning of a meaningful work session or after user/external handoff.
2. Read `resolved_executor` and only its JIT requirements.
3. Produce the real stage artifacts using existing tools/capabilities.
4. Run the relevant deterministic validators/QA.
5. Use `run-until` to advance through already-valid machine stages until Human Gate, external handoff, Release Ready or the first real BLOCK.
6. If a Human Gate is reached, present the actual review artifact to the user and stop.
7. Only after a real user approval/selection, call `accept-gate` with the exact decision text and real approved artifact paths.
8. Continue the next phase without inventing extra confirmation checkpoints.

## 5. Human Gate transaction

Example shape only; use the actual current gate/artifacts:

```bash
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py accept-gate \
  --slot D03-B \
  --gate HG01 \
  --decision 'USER EXACT DECISION TEXT' \
  --approved 'relative/path/to/approved/artifact.md'
```

The local operator performs a fresh resume/guard check, records the durable Human Gate receipt through the Canonical controller, then advances through the existing Lean gate transaction. Codex must never generate approval text on the user's behalf.

## 6. Machine macro

After real prerequisite artifacts exist:

```bash
python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py run-until --slot D03-B
```

`run-until` does not create missing artifacts. It only asks existing Canonical validators to advance stages that are already valid. A missing prerequisite must return BLOCKED, not be patched with a fake file.

## 7. Production phases

### Phase A — HG01 Song
- use current Core Benchmark / song-discovery executor JIT;
- produce a small, high-quality candidate set, not a broad web dump;
- show real reference links/evidence when available;
- stop for the user's aesthetic song decision.

### Phase B — HG02 BGM
- discover/resolve the exact usable BGM entity/version;
- produce listening candidate(s) and identity evidence;
- stop for BGM acceptance.

### Phase C — Audio Truth -> Director -> HG03
After HG02 PASS:
- P0 same-version timed lyric/LRC first;
- P1 `lightweight_align.py` if P0 is unavailable/ambiguous;
- P2 heavy forced alignment only after a concrete P1 failure;
- stop at the first passing route;
- build Natural Beat;
- build Director Plan using `MV_DIRECTOR_LEAN_OVERLAY.md`;
- prepare/generate first-frame set and machine QA;
- if Codex cannot call image generation, create the exact external handoff package;
- stop at HG03 with the real image set available for review.

### Phase D — Dynamic Sources
After HG03 PASS:
- generate bounded dynamic prompts from accepted K0 pixels;
- if Seedance/video generation is external, create a generation handoff package and stop at the external boundary;
- when files return, resume from repository truth and run source QA;
- TRIM BEFORE REGENERATE.

### Phase E — Edit -> HG04
- conditional normalization only when source structure/codec/cleaning requires it;
- locked BGM identity invariant at editor entry;
- build executable Edit Map;
- every meaningful cut needs a WHY CUT HERE;
- render picture preview and machine QA;
- stop at HG04.

### Phase F — Final -> HG05
After HG04 PASS:
- implement locked subtitle baseline;
- subtitle geometry/timing QA;
- final render;
- technical QA;
- normally run this as one machine phase;
- stop at HG05 with the real final candidate.

### Phase G — Release
After HG05 PASS:
- build Release Package;
- advance to `S16_RELEASE_PACKAGE_READY`;
- write Codex R2 result report and metrics;
- stop. Do not enter S17 without real publication confirmation.

## 8. External handoff

If a capability is not available, follow `CODEX_HANDOFF_PROTOCOL.md`. A handoff is a valid stop, not a failure, provided Codex outputs exact actionable inputs and preserves the Canonical stage boundary.

## 9. Git behavior

- Keep raw media local/ignored.
- Commit text manifests, prompts, QA reports, Canonical state/receipts generated by controllers, and test metrics.
- Prefer one coherent commit per meaningful phase or repaired blocker, not one commit per command.
- Do not modify core Runtime merely to make D03-B pass.

## 10. Completion

Codex R2 is successful only if a fresh MV reaches S16 with:
- all five Human Gates based on real user decisions;
- no hand-edited Canonical state/receipts;
- no fake external media;
- no second state machine;
- no per-slot model installation;
- no D03-B-specific core helper;
- reproducible technical artifacts and a truthful result report.