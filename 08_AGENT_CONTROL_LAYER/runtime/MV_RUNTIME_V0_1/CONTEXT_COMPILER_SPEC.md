# MV Runtime v0.1 — Context Compiler Specification

## Purpose

Every Stage call should receive the minimum complete context, not the maximum available history.

## Context package

A compiled Stage context may include only:

1. Current Stage Goal
2. Current Stage Contract
3. Current Stage Skill / execution method
4. Required fields from sealed upstream Handoff(s)
5. Current user change/request
6. Current Artifact(s)
7. Evidence required by this Stage
8. Locked rules that are actually relevant here

## Excluded by default

- full project chat transcript;
- entire repository;
- superseded rules;
- failed versions;
- upstream rationale;
- unrelated Stage Skills;
- previous Judge explanations;
- archived discussions.

## Two compiler modes

### EXECUTOR_CONTEXT

May contain current Skill, creative/technical goal, current artifact, relevant upstream handoff, and current revision target.

### JUDGE_CONTEXT

Must contain acceptance criteria, locked rules, final artifact, and required evidence.

Must not contain executor rationale, failed drafts, persuasive self-explanation, or unrelated project history.

## Archive lookup

Archive may only be loaded when current evidence cannot localize a real failure.

Then:
1. identify suspected source stage;
2. open only that stage's relevant archive;
3. resolve;
4. return archive out of active context.

## Context completeness test

A context is valid only if both are true:

- NO_IRRELEVANT_HISTORY
- NO_REQUIRED_FIELD_MISSING

Small context is not allowed to mean missing necessary evidence.

## Runtime measurement

During later real tests, record:

- approximate number of files loaded per Stage;
- whether full history was required;
- whether next Stage requested missing upstream information;
- whether archived context was reopened.

The desired trend is less active context without loss of task correctness.