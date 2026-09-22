# 01 — Agent Control Layer Architecture

## 1. Problem definition

The system should optimize for **reliable execution**, not maximum context retention.

Long-context failure modes observed in complex AI production projects include:

- obsolete requirements remain salient after replacement;
- the same model both creates and defends its own output;
- plans and tool-verified facts are confused;
- process instructions expand faster than they can be maintained;
- every change appears to require reloading the entire project history;
- global "self-review" becomes long but not necessarily independent.

The solution is separation of responsibilities.

## 2. Responsibility map

### Main Agent / Executor
Responsible for:
- understanding new goals;
- creative reasoning;
- directing scenes;
- writing prompts;
- diagnosing novel failures;
- revising artifacts.

Not responsible for:
- being the source of truth for project state;
- declaring its own work verified without evidence;
- deciding deterministic workflow transitions.

### Skill
Responsible for **HOW** a bounded capability is performed.

A Skill should contain:
- purpose;
- input contract;
- capability procedure;
- output contract;
- necessary domain rules.

A Skill should not contain:
- the entire project history;
- all stage states;
- every historical exception;
- unrelated downstream logic.

### HARNESS / State Store
Responsible for **WHERE WE ARE**.

It should track:
- current stage;
- stage version;
- state: OPEN / REVIEW / SEALED / DIRTY;
- dependency versions;
- evidence pointers;
- user gates;
- active artifact references.

It should not be the full operational manual.

### Stateless Judge
Responsible for **DOES THIS RESULT SATISFY THE CURRENT CONTRACT?**

Characteristics:
- fresh context;
- minimal evidence;
- no long-term memory;
- no generator rationale;
- typed output only;
- atomic questions;
- explicit insufficient-evidence state.

### Deterministic Gate
Responsible for **WHAT HAPPENS NEXT**.

The Judge supplies judgments. Code/state rules decide whether to:
- SEAL;
- REVISE;
- ESCALATE;
- BLOCK.

### Archive
Responsible for historical recoverability:
- discussions;
- failed versions;
- full judge reports;
- old rules;
- discarded options.

Archive is excluded from normal next-stage context.

## 3. Context compilation

Every working call should be assembled from the smallest necessary package:

```text
Current User Change
+ Current Stage Goal
+ Current Stage Contract
+ Current Stage Skill
+ Required upstream Handoff fields
+ Current Artifact
+ Required Evidence
```

Do not load:
- unrelated earlier stages;
- abandoned drafts;
- reasons behind already sealed decisions;
- entire repository docs by default.

This is called **Context Compilation**.

## 4. Failure isolation

When Stage B fails:

1. inspect B's artifact and its input handoff;
2. determine whether B misused a valid input;
3. only if the input itself is invalid, inspect Stage A handoff/evidence;
4. reopen A only if the defect originated there;
5. mark only dependent downstream stages DIRTY.

This is **Failure Localization**, not full-history replay.

## 5. Change propagation

### Internal implementation change
Example: first-frame generation technique changes, but output contract does not.

Impact:
- current stage only.

### Contract-compatible output change
Example: first frame image updated but same character/composition contract retained.

Impact:
- dependent stages may require artifact refresh, but upstream unrelated stages remain sealed.

### Contract-breaking change
Example: 10-shot director plan becomes 6 long takes and downstream expects 10 shot IDs.

Impact:
- contract version increments;
- direct dependents become DIRTY;
- no need to invalidate unrelated upstream stages.

## 6. Reliability hierarchy

Use the cheapest and most deterministic mechanism capable of answering the question:

```text
1. Code / State
2. Atomic Semantic Judge
3. Fresh Deep Judge / Diagnostic GPT
4. Human Gate
```

Examples:

```text
"Does file X exist?"                  -> code
"Did user approve first frame?"       -> state
"Does prompt describe grounded steps?"-> semantic judge
"Why does this choreography feel wrong?" -> GPT diagnosis
"Is the artistic direction acceptable?" -> human gate when required
```

## 7. Judge isolation

A Judge must not receive the executor's persuasive rationale.

Bad:
```text
I chose this design because...
Here are five reasons it should work...
Please review my result.
```

Good:
```text
GOAL
LOCKED RULES
ACCEPTANCE CRITERIA
FINAL ARTIFACT
EVIDENCE
```

This approximates blind review and reduces context bias.

## 8. Why not a persistent Judge Agent?

A persistent Judge accumulates:
- memory;
- preferences;
- stale project details;
- context contamination.

Therefore the preferred first design is a **Stateless Judge Worker**:

```text
construct request -> judge -> typed result -> destroy context
```

A separate long-lived agent is only justified if later testing proves a need that cannot be met by stateless calls.
