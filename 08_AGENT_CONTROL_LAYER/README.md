# Tangyuan Agent Control Layer

> Status: Architecture Record v0.1  
> Date: 2026-09-22  
> Scope: MV / Seedance / Dola / AI video production workflows  
> Principle: **Main Agent creates; State owns truth; Judge validates; Code controls transitions; each stage seals into a compact handoff.**

## 1. Why this project exists

The current long-running video workflow has repeatedly exposed a structural problem:

- the model is capable enough, but long context grows continuously;
- old and new rules coexist in context;
- generation, self-review, project state, and routing are often handled by the same reasoning stream;
- a successful local edit can unintentionally alter other workflow behavior;
- plans, assumptions, and actually verified execution state can become mixed;
- adding more SKILL/HARNESS prose can eventually reduce reliability instead of improving it.

This project records a different architecture.

The goal is **not** to replace GPT with Jev/Laya/Nimble. The first implementation should continue to use GPT-5.6 for the strongest reasoning and creative work, while restructuring the workflow so that each model call receives only the context required for its current responsibility.

## 2. Core architecture

```text
User Goal
   |
   v
Main Agent / Stage Executor (GPT-5.6)
   |
   v
Stage Result
   |
   +--> Deterministic Checks (code/state)
   |
   v
Stateless Fresh Judge (GPT-5.6, minimal context)
   |
   v
Atomic Decisions
   |
   v
Deterministic Gate
   |------ REVISE ---> reopen current stage only
   |------ ESCALATE --> diagnostic / human gate
   |
   v
SEAL
   |
   v
Compact Handoff
   |
   X  previous working context leaves active context
   |
   v
Next Stage
```

Archive remains available, but is **not loaded by default**. It is reopened only when a later failure requires targeted diagnosis.

## 3. Five locked design rules

### A. No Evidence, No State Transition
A model statement is not proof of execution. File existence, tool output, user approval, verified media result, or another explicit evidence source is required before a state that depends on it may become true.

### B. Generator != Judge
The executor and judge may use the same base model, but the Judge runs in a fresh context and does not inherit the executor's explanations, failed drafts, or rationale.

### C. Atomic Judgment before Overall Judgment
Prefer small factual questions:
- requirement satisfied?
- blocking defect present?
- evidence sufficient?
- contract complete?

Do not rely on one vague question such as "Is this stage good enough?"

### D. Code owns deterministic control flow
If the answer is mechanically knowable, use code/state rather than AI.

Examples:
- file exists;
- shot count >= required count;
- user gate approved;
- required field present.

AI Judge is reserved for semantic ambiguity.

### E. Sealed stages pass contracts, not history
The next stage inherits:
- Result
- Decisions
- Locked Rules
- Evidence references
- Open Issues
- Next-stage input

It does not inherit the entire discussion history unless a fault requires rollback.

## 4. Stage lifecycle

```text
OPEN
  |
  v
WORK / ITERATE
  |
  v
REVIEW
  |
  +-- REVISE --> OPEN
  +-- UNCERTAIN --> ESCALATE
  |
  v
SEALED
```

A sealed stage is immutable. A later change requires:
```text
REOPEN -> new version -> REVIEW -> SEAL
```

If the new version changes an output contract field used downstream, only dependent downstream stages are marked DIRTY.

## 5. What Jev / Laya / Nimble contribute

This architecture borrows concepts, not dependencies.

### Jev
Useful ideas:
- typed decisions;
- Choice / Score / Noul primitives;
- uncertainty as a routing signal;
- code-controlled workflow;
- narrow System-One decisions.

Current limitation:
- text/JSON decision layer, not a direct video perception layer.

### Laya
Useful ideas:
- stateless specialized judge;
- domain-specific decision training;
- calibration;
- mature high-frequency judgments can eventually be "compiled" into a small model.

Current decision:
- do not insert Laya into production yet;
- first collect real Stage Judge data.

### Nimble
Most directly relevant to the first implementation:
- use a general LLM as a decision engine;
- restrict output to candidates;
- independent atomic fields;
- small context;
- explicit unknown / insufficient-evidence option;
- contrastive test pairs;
- version and regression-test the judging contract.

## 6. First implementation decision

Do **not** start by training or deploying another model.

Start with:

```text
GPT-5.6 Stage Executor
+
GPT-5.6 Fresh Stateless Judge
+
Stage Contracts
+
Deterministic Gate
+
Compact Handoff
+
Contrastive Regression Tests
```

Only after a judgment becomes repetitive, stable, well-labeled, and high-volume should it be considered for Laya/Nimble-style specialization.

## 7. Project files

- `01_ARCHITECTURE.md` — responsibilities and control boundaries
- `02_STAGE_CONTRACTS.md` — Stage / Handoff / Seal / Reopen contracts
- `03_STATELESS_JUDGE.md` — GPT-Nimble style Judge design
- `04_DATA_AND_REGRESSION.md` — contrastive tests and future training data
- `05_IMPLEMENTATION_ROADMAP.md` — staged implementation path
- `06_JEV_LAYA_NIMBLE_NOTES.md` — research conclusions and adoption boundaries
- `templates/` — reusable stage and handoff templates

## 8. Success criteria

This architecture is successful only if real project runs demonstrate:

1. fewer state hallucinations and premature stage transitions;
2. fewer forgotten locked rules;
3. lower active-context size per stage;
4. a local stage change does not force unrelated stages to be reworked;
5. stage failures can be localized and rolled back selectively;
6. Judge changes are measurable through regression tests rather than intuition;
7. archived history remains recoverable without becoming default active context.

A generated file or successful model response alone does not prove the architecture works. It must be validated on real MV/video production runs.
