# Rules｜MV Executor-First Contract v1.0

> Status: `EXPERIMENT ENFORCEMENT CANDIDATE / HARD`
> Purpose: prevent an Agent from inventing a new implementation before checking the repository's already-validated execution path.
> Applies to: every Canonical MV stage from `S00` through `S18`, including OSS optimization branches.

---

## 1. Core rule｜HARD

Before doing work for the current Runtime stage, resolve execution in this order:

`RESUME / CURRENT_STATE`
→ `mv_stage_registry.json`
→ `mv_stage_executor_registry.json`
→ current stage Rules / Templates
→ existing canonical tool / deterministic recipe / capability handoff
→ dependency preflight
→ execute
→ validate required artifacts
→ Runtime advance.

**A Rule is not an Executor. An external project mentioned by a Rule is not automatically a new dependency to install.**

The Agent MUST NOT jump from a prose rule directly to creating a helper script, new workflow, new model route, or new service integration.

---

## 2. Existing implementation first｜HARD

For every stage, before writing any new implementation, the Agent must answer from durable repository truth:

1. What is the registered execution class for this stage?
2. Is there an existing canonical toolchain?
3. Is there an existing deterministic recipe / Rule that is the intended executor?
4. Is the step intentionally a creative synthesis or external capability handoff rather than a repository tool?
5. Is there a prior PASS sample or regression test that should be reused?
6. Are dependencies already available / cached / preheated?

Only after the registry explicitly says there is an implementation gap may a new implementation be proposed.

---

## 3. Dependency policy｜HARD

Dependency handling order:

`CHECK / DOCTOR`
→ `REUSE existing environment/cache`
→ `BLOCK if required capability is absent`
→ only then, if the registered executor explicitly permits environment setup, perform a separate controlled setup.

Forbidden defaults:
- installing a model merely because a Rule names a reference implementation;
- downloading the same production model once per MV slot;
- silently substituting a different model/library when the locked one is unavailable;
- adding installation logic inside a per-song helper;
- using a fresh ephemeral runner as if it were the canonical persistent production environment unless the executor contract explicitly defines that runner.

For Audio Timeline specifically, `alignment_runtime.lock.json` is version authority; `bootstrap_alignment_env.py doctor` precedes any explicit `install` action.

---

## 4. New-tool admission gate｜HARD

A new helper / workflow / adapter may be created only when ALL are true:

- current stage executor registry has been read;
- no existing canonical executor satisfies the requirement;
- prior PASS examples / existing workflows were checked for reusable implementation;
- the missing capability is written as a concrete implementation gap;
- the new item is scoped to an experiment area unless/until promoted;
- it does not modify the active Runtime Bridge into a stage-specific script host;
- it has an output contract, failure behavior, and cleanup/promotion decision;
- it does not weaken existing Gate criteria.

Slot-specific helpers such as `d02b_*` are forbidden under core `04_HARNESS/tools/` unless they are temporary migration fixtures explicitly marked as such. Experimental one-offs belong under the experiment directory and must not become Runtime authority.

---

## 5. Runtime Bridge purity｜HARD

`r3-mv-runtime-web-bridge.yml` is a transport/execution bridge for registered Runtime commands.

It must not become a host for:
- song-specific audio probes;
- one-slot model downloads;
- one-slot timeline builders;
- Director experiments;
- rendering experiments.

Stage work may use a separate registered capability/workflow, but Runtime state mutation remains isolated and authoritative.

---

## 6. Creative and external stages are not implementation gaps

The absence of a Python script does NOT mean a stage is incomplete.

Valid registered execution classes include:
- `RUNTIME_CONTROLLER`
- `DATA_ORCHESTRATION`
- `EVIDENCE_ORCHESTRATION`
- `CANONICAL_TOOLCHAIN`
- `CREATIVE_SYNTHESIS`
- `CAPABILITY_HANDOFF`
- `DETERMINISTIC_MEDIA_TRANSFORM`
- `TECHNICAL_VALIDATION`
- `HUMAN_GATE`
- `TRANSACTIONAL_PUBLISH`
- `DATA_REVIEW`

For `CREATIVE_SYNTHESIS`, the existing Workflow/Rule/Template is the intended production path; do not invent a model deployment.

For `CAPABILITY_HANDOFF`, use the already-available product/tool boundary and persist the returned assets; do not build a new backend unless a separate experiment explicitly targets that backend.

---

## 7. OSS experiment boundary｜HARD

An external OSS reference may alter only stages explicitly marked `experiment_overlay_allowed=true` in `mv_stage_executor_registry.json`.

For the current `mvmaker-h3-skills` experiment, the intended optimization scope begins in Director / First Frame / Dynamic / Edit reasoning. It must not silently replace:
- HG01 selection truth;
- HG02 audio truth;
- Audio Timeline correctness;
- Runtime state controllers;
- publish transaction truth.

External implementation details such as H3 10–15s containers, four-panel inputs, or RunningHub orchestration remain out of scope unless separately approved.

---

## 8. Failure behavior

When the canonical executor is unavailable:

`STATE = BLOCKED_AT_CURRENT_STAGE`

Report exactly:
- missing executor/dependency/capability;
- canonical path that was checked;
- whether environment setup is permitted;
- nearest valid recovery action.

Do NOT proceed with a substitute implementation merely to keep momentum.

---

## 9. Efficiency objective

This rule exists to reduce:
- duplicated research;
- duplicated model downloads;
- ad-hoc scripts;
- unnecessary GitHub Actions runs;
- Token/context expansion;
- divergence between production and experiments.

The expected normal behavior is: **reuse validated production truth by default; experiment only where the experiment is actually scoped.**
