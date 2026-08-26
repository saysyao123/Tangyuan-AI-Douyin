# MV Runtime Consolidation｜P0 Canonical Stage + Artifact + Validator Receipt v1

- Date: 2026-08-26
- Branch: `refactor/mv-runtime-consolidation-v2`
- Status: `P0 CORE PASS / CANDIDATE / NOT PRODUCTION DEFAULT`
- Scope: original Tangyuan MV Runtime execution hardening only
- Explicitly excluded: `mvmaker-h3-skills`-inspired Director redesign / Aesthetic redesign. Those remain a separate future D02-B experiment and are not part of this P0.

---

## 1. P0 objective

Convert the existing MV Golden Runtime from prose-only execution discipline into a machine-readable, machine-auditable evidence chain.

P0 does **not** redesign the creative workflow. It answers three questions:

1. What is the one canonical ordered stage chain?
2. What durable artifacts prove each stage actually happened?
3. Can a machine reject a downstream state when the upstream evidence chain is incomplete or ambiguous?

Core rule:

`DECLARED STATE != PROVEN STATE`

A `CURRENT_STATE` string is informative only. It cannot substitute for required artifacts / receipts.

---

## 2. Delivered P0 assets

### A. Canonical Stage Registry

`04_HARNESS/runtime/mv_stage_registry.json`

Current registry:
- 19 ordered stages;
- 5 Human Gates only: HG01 / HG02 / HG03 / HG04 / HG05;
- technical stages remain machine Gates and do not add Human Gates;
- supports conditional requirements for WEB, multi-shot normalization and 30D/60 publish sync;
- includes post-publish review so production forms a closed loop rather than stopping at final render.

Current chain:

`S00_SLOT_CREATED`
→ `S01_HG01_SONG_LOCKED`
→ `S02_HG02_BGM_LOCKED`
→ `S03_AUDIO_TIMELINE_LOCKED`
→ `S04_NATURAL_BEAT_LOCKED`
→ `S05_DIRECTOR_PLAN_LOCKED`
→ `S06_HG03_FIRST_FRAMES_LOCKED`
→ `S07_DYNAMIC_PROMPT_SET_READY`
→ `S08_DYNAMIC_SOURCE_QA_LOCKED`
→ `S09_SOURCE_NORMALIZATION_READY`
→ `S10_EDITOR_AUDIO_GATE_PASS`
→ `S11_EDIT_MAP_LOCKED`
→ `S12_HG04_PICTURE_EDIT_PASS`
→ `S13_SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `S14_FINAL_TECH_QA_PASS`
→ `S15_HG05_FINAL_ACCEPTANCE_PASS`
→ `S16_RELEASE_PACKAGE_READY`
→ `S17_PUBLISHED_DATA_COLLECTION_ACTIVE`
→ `S18_POST_PUBLISH_REVIEWED`.

### B. Canonical Artifact Registry

`04_HARNESS/runtime/mv_artifact_registry.json`

Current registry:
- 31 canonical artifacts;
- canonical future slot directory families from `00_STATE` through `13_POST_PUBLISH`;
- legacy R1/R2/R3 filenames are read-only compatibility aliases;
- future slots must create canonical paths rather than invent a new naming family;
- a legacy alias match is always reported;
- multiple legacy candidates are **ambiguous and BLOCKING**; the validator must not guess which revision is authoritative;
- a QA artifact cannot substitute for an implementation artifact merely because its filename is similar.

### C. Runtime Validator

`04_HARNESS/tools/mv_runtime_gate.py`

P0 commands:

```text
registry-check
artifact-check
validate-stage
audit-slot
explain-stage
```

Exit contract:
- `0` = requested validation PASS;
- `1` = evidence / stage validation FAIL;
- `2` = registry/configuration/tool invocation failure.

P0 validator is deliberately **read-only**. It does not advance `CURRENT_STATE`.

Capabilities:
- registry integrity checking;
- canonical + legacy artifact resolution;
- artifact content checks (`min_size`, JSON-object, regex evidence);
- conditional stage prerequisites;
- cumulative chain validation;
- highest contiguous proven stage reporting;
- declared-state reporting for divergence diagnosis;
- ambiguous legacy alias blocking;
- artifact path-collision reporting.

---

## 3. Regression fixture A｜D02-A execution-gap case

Slot:
`06_TESTS/MV/WEB_R3/30D_60/D02-A`

Declared durable state:
`HG05_PASS / RELEASE_READY / PUBLISH_PENDING`

Machine-audited highest contiguous proven stage:
`S04_NATURAL_BEAT_LOCKED`

Expected result:
`FAIL / divergence detected`

Interpretation:
D02-A produced a valid final creative result, but several middle-stage durable artifacts were never written. The validator correctly refuses to infer Director / HG03 / Dynamic / Edit completion merely from the late CURRENT_STATE or final output.

This is the exact class of “conversation done but Runtime evidence missing” defect P0 is intended to stop.

---

## 4. Regression fixture B｜D01-B legacy-complete case

Slot:
`06_TESTS/MV/WEB_R3/30D_60/D01-B`

Declared durable state:
`PUBLISHED / DATA_COLLECTION_ACTIVE`

Machine-audited highest contiguous proven stage:
`S03_AUDIO_TIMELINE_LOCKED`

Expected result:
`FAIL / historical artifact gaps detected`

Important distinction:
D01-B contains many genuine later-stage artifacts (Director plans, Video QA, WEB rough-cut QA, Picture Edit plan, HG04, Subtitle QA, Final Tech QA, HG05, Publish Package). The validator recognizes those through legacy aliases, but does not permit them to repair a broken continuous evidence chain.

Strict legacy-resolution regression:
- `DIRECTOR_PLAN_v1.md` and `DIRECTOR_PLAN_v2.md` coexist;
- no canonical `05_DIRECTOR/DIRECTOR_PLAN.md` pointer exists;
- validator must return `ambiguous` rather than silently choose v2.

False-positive regression:
- `SUBTITLE_IMPLEMENTATION_QA_v1.md` exists;
- it must not be accepted as `SUBTITLE_IMPLEMENTATION`;
- QA evidence and implementation evidence remain separate artifact identities.

---

## 5. CI evidence

Workflow:
`.github/workflows/r3-mv-runtime-p0-tests.yml`

Latest strict regression run:
- Run ID: `32977382688`
- Job: `runtime-p0`
- Conclusion: `success`

Verified behaviors:
1. Stage/Artifact registries are internally consistent.
2. Conditional normalization requirements resolve correctly.
3. D02-A declared HG05 state does not override the incomplete evidence chain.
4. D01-B legacy artifacts are visible, but missing upstream evidence still blocks the chain.
5. Ambiguous legacy revisions block rather than being guessed.
6. QA files cannot impersonate implementation artifacts.
7. Artifact path collisions are rejected/reported rather than silently accepted.

---

## 6. What P0 now solves

P0 converts these previous soft statements:

- “不要跳步”
- “每步要留证据”
- “Gate PASS 才能继续”
- “CURRENT_STATE 要更新”

into an initial executable evidence model.

For the first time the Runtime can answer mechanically:

- What exact artifacts should exist at this stage?
- Which one is missing?
- Is an old filename being used?
- Are two old revisions competing for authority?
- What is the highest continuously proven stage?
- Does the declared CURRENT_STATE outrun the durable evidence?

---

## 7. What P0 deliberately does NOT solve yet

Do not promote to Production Default yet.

Still missing:
1. machine-controlled state transition / `advance` command;
2. transition receipts;
3. canonical Human Gate receipt templates;
4. canonical new-slot scaffold / init command;
5. migration strategy for legacy slots;
6. tracker + slot transactional publish sync;
7. validation of actual external media hashes / asset manifests;
8. a brand-new MV run proving the canonical path can be completed without skipping a stage.

Therefore current authority is:

`P0 CORE PASS / CANDIDATE`

not:

`PRODUCTION DEFAULT`.

---

## 8. Next hardening boundary

Next implementation should build on this P0 evidence model rather than rewrite it:

`State Transition Receipt + Human Gate Receipt Contract + Canonical Slot Scaffold`

A future state mutation must be allowed only after `mv_runtime_gate.py validate-stage` returns PASS for the target stage.

No merge into `test/mv-web-r3` should occur until transition enforcement and at least one clean regression/new-slot validation are complete.
