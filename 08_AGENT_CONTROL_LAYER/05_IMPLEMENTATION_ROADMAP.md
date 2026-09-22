# 05 — Implementation Roadmap

## Phase 0 — Architecture record
Status: CURRENT

Deliverables:
- architecture definition;
- stage lifecycle;
- Judge protocol;
- regression strategy;
- research boundaries.

No production behavior changes yet.

## Phase 1 — One-stage pilot

Select one stage from the real MV/Seedance workflow.

Recommended candidate:
```text
Dynamic Prompt / Motion Design
```

Why:
- repeated;
- strong existing rules;
- current known failure modes such as unsupported sliding;
- output is text and easy to judge before consuming video-generation credits.

Build:

```text
MOTION_STAGE_CONTRACT v0.1
MOTION_JUDGE_CONTRACT v0.1
MOTION_HANDOFF v0.1
20–40 contrastive test pairs
```

Use GPT-5.6 as both executor and Fresh Stateless Judge.

## Phase 2 — Validate stage sealing

Run real tasks and verify:

- previous stage history is not normally loaded;
- Judge receives only minimal context;
- a passed stage produces a compact handoff;
- next stage can work using the handoff plus its Skill;
- archived history is only reopened on failure.

Record context size and failure types.

## Phase 3 — Selective rebuild

Introduce version/dependency tracking.

Test scenarios:
1. internal Skill edit with unchanged contract;
2. artifact update with compatible contract;
3. contract-breaking change;
4. downstream failure caused by upstream handoff defect.

Expected behavior:
- unrelated sealed stages remain untouched;
- only relevant dependents become DIRTY.

## Phase 4 — Regression gate

Before activating a modified Judge Contract:
- run contrastive suite;
- compare to current production Judge;
- block activation if critical false-pass rate worsens beyond threshold.

Do not use "prompt looks better" as the release criterion.

## Phase 5 — Expand to adjacent stages

Possible order:
1. Dynamic Prompt / Motion
2. Stage Seal
3. Video retry routing
4. First-frame handoff
5. Director handoff
6. Edit/continuity gate

Do not refactor all stages simultaneously.

## Phase 6 — Data maturity review

After sufficient production use, analyze:

- number of decisions per Judge;
- disagreement rate;
- false-pass categories;
- stable vs changing acceptance criteria;
- repeated expensive GPT judgments.

At this point decide whether any Gate should remain GPT-only or be specialized.

## Phase 7 — Optional specialized Judge

Only if justified, test:
- Laya-style small trained Judge;
- Nimble/Qwen-style specialized LLM Judge;
- GPT Fresh Judge as baseline.

All candidates must use the same:
- Stage Contract;
- Judge Schema;
- regression suite;
- held-out cases.

The backend is replaceable. The workflow contract is the product.

## Phase 8 — Production integration

Only after pilot evidence shows improvement:
- integrate Stage State into HARNESS;
- route required Skills through stage contracts;
- automate compact handoff generation;
- add archive lookup/reopen mechanism;
- establish Judge version tracking.

## Stop conditions

Pause or roll back if:
- Judge produces more false passes than current manual process;
- context reduction removes necessary information;
- local changes unexpectedly invalidate unrelated stages;
- contract maintenance becomes more complex than the original workflow;
- human review burden increases without quality gain.

## First experiment acceptance criteria

The v0.1 pilot is considered promising if:

1. it completes real Motion Prompt tasks without needing full project history;
2. Fresh Judge catches known failure cases in the regression suite;
3. failed criteria lead to local revision, not global workflow reset;
4. the sealed handoff is sufficient for the next stage;
5. a later failure can reopen only the relevant archived stage;
6. the workflow is easier to maintain than the current long-form HARNESS path.
