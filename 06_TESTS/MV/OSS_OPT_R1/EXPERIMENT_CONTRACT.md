# OSS MV Optimization Integration Test｜Experiment Contract v1.0

## 1. Purpose

This experiment line exists to test whether external/open-source MV production ideas can materially improve the current Canonical MV Runtime without weakening correctness, durability, or production stability.

Baseline branch:

- `test/mv-web-r3`
- baseline SHA at fork: `89852ec5314e7579853683ef5eb40adb09f25753`

Experiment branch:

- `test/mv-oss-optimization-r1`

## 2. Isolation rule

This branch is an R&D overlay, not a production deployment branch.

Locked rules:

- do not modify `test/mv-web-r3` while the experiment is running;
- do not rewrite or reinterpret D02-A legacy history;
- do not relax Canonical Runtime guards, Human Gate receipts, hash chains, rollback semantics, media identity or publish transaction safety merely to make an external idea easier to integrate;
- external project logic is treated as `CANDIDATE` until a full comparison proves value;
- no optimization is promoted directly into Workflow / Rule / Runtime merely because it looks promising in one sample;
- experimental code/docs must remain attributable to its source project and mapped to a specific current Runtime stage or production concern.

## 3. Experiment unit

The primary experiment should be one complete MV production case on this branch, using the same Canonical Runtime baseline and a clearly documented optimization overlay.

The experiment may use the first currently-unused slot available on the experiment branch after revalidation. The production branch remains unchanged.

## 4. Required integration mapping

Every incoming open-source optimization must be classified before implementation:

1. `DIRECT_RUNTIME_REPLACEMENT`
   - proposes replacing authoritative state / validator / gate logic;
   - highest risk; default recommendation is reject or wrap, not direct replacement.

2. `STAGE_OVERLAY`
   - improves one existing stage such as Director, First Frame, Dynamic Prompt, Dynamic QA, Edit, Subtitle, etc.;
   - preferred integration form.

3. `KNOWLEDGE_CANDIDATE`
   - heuristics, prompt patterns, camera grammar, aesthetic rules, evaluation methods;
   - test as optional knowledge first.

4. `TOOLING_ADAPTER`
   - helper scripts, analyzers, converters, extractors, renderers;
   - may be attached around the Runtime if it does not become state authority.

5. `OUT_OF_SCOPE`
   - publishing automation, unrelated product features, duplicated legacy flow, or ideas that cannot be tested against the stated MV goal.

## 5. Comparison design

At minimum compare:

- Baseline Runtime output path;
- Baseline + OSS optimization overlay.

Where practical, hold constant:

- song/audio truth;
- lyric timeline;
- model/tool availability;
- target duration and aspect ratio;
- Human Gate criteria.

The test is not judged only by visual novelty. It must be scored on:

- lyric visual hit;
- director/camera quality;
- shot diversity without incoherence;
- first-frame performability;
- dynamic generation stability;
- edit usability;
- identity/continuity stability;
- number of regenerations;
- time/cost burden;
- Runtime compatibility;
- zero-context reproducibility;
- risk of hidden chat-memory dependence.

## 6. Promotion rule

Each tested optimization receives one final decision:

- `PROMOTE_RUNTIME` — rare; only if it belongs in authoritative Runtime behavior;
- `PROMOTE_RULE` — stable production rule;
- `PROMOTE_KNOWLEDGE` — useful but optional/contextual;
- `PROMOTE_TOOLING` — helper tool with bounded authority;
- `KEEP_EXPERIMENTAL` — promising but insufficient evidence;
- `REJECT` — no net benefit or unacceptable complexity/risk.

A promotion proposal must identify exactly what existing file/rule it would modify and what old behavior it supersedes. No silent overwrite.

## 7. Final state

Status: `COMPLETE / CLOSE PASS / NO STABLE DEPLOYMENT YET`

Completed experiment unit:
- slot: `D02-B / Lane S`;
- song: `《有几次想你了》`;
- Canonical Runtime: `S16_RELEASE_PACKAGE_READY / RELEASE_READY`;
- HG01-HG05: all PASS;
- selected Director candidate: `R3 + bounded OSS overlay`;
- final accepted render SHA-256: `7f77a41a68db47d4f7992cb77161c86414eeb0fd1cf8233322956b4025bf43d9`.

Final evidence:
- `RESULT_MATRIX.md`;
- `PROCESS_AUDIT/OSS_OPT_R1_CLOSE_AUDIT_v1.md`;
- `OSS_OPT_R1_CLOSE_RECEIPT.json`.

Promotion boundary:
- useful Director/Montage ideas are recorded as selective knowledge promotions / candidates;
- Executor-First routing is a `PROMOTE_RUNTIME_CANDIDATE`;
- Audio Timeline P0/P1/P2 priority is a `PROMOTE_RULE_CANDIDATE`;
- H3-specific execution/container/input constraints remain rejected for R3;
- `test/mv-web-r3` has not been silently modified or promoted.

The next action is **not more experiment production**. Any move into stable Runtime/Rule/Knowledge must be a separate explicit promotion review with exact diff, regression validation and deployment receipt.
