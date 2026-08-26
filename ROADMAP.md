# Roadmap

This roadmap focuses on turning the current production harness into a more reusable and maintainable open-source runtime.

## Phase 1 — Promote validated R3 runtime to main

Goal: reduce the gap between the public default branch and the production-tested runtime.

Planned work:

- promote authoritative R3 workflow/rule files after final cross-song review;
- remove stale bootstrap references and duplicate historical instructions;
- document authoritative vs historical vs experimental files;
- publish a compact runtime load order;
- add stable entry points for new projects and new agents;
- standardize evidence labels and promotion receipts.

Success condition:

A new contributor or agent can open the default branch and determine, without private context, which files are authoritative and how to start a production run.

## Phase 2 — Codex-powered maintenance automation

Goal: use Codex for core OSS maintenance rather than only content generation.

Target automations:

### Rule / workflow impact analysis
When a PR changes an authoritative rule, automatically identify:

- affected stages;
- downstream artifacts that may become stale;
- duplicated or conflicting instructions;
- required regression targets.

### Project-state validation
Check invariants such as:

- current state references an existing stage;
- required receipts exist before a gate is marked PASS;
- timing-dependent stages are invalidated when audio identity changes;
- tracker and per-project state do not contradict each other;
- authoritative links are not stale.

### Documentation synchronization
Detect:

- README claims that no longer match runtime files;
- renamed or moved files;
- broken internal references;
- historical instructions presented as current production rules.

### Structured regression review
For workflow/prompt changes, generate a review checklist covering:

- semantic correctness;
- identity stability;
- camera/motion repetition;
- editability;
- clean endpoints;
- rollback boundaries;
- evidence tier required for promotion.

### Issue triage
Automatically classify incoming issues into categories such as:

- audio/version identity;
- timeline/alignment;
- director/lyric fit;
- first-frame QA;
- image-to-video instability;
- camera execution;
- source normalization;
- subtitle/editing;
- documentation/runtime drift.

### Release / promotion support
Generate:

- change summaries;
- release notes;
- migration notes;
- experimental-to-production promotion receipts;
- regression requirements before merge.

## Phase 3 — Reusable examples and public eval fixtures

Goal: make the project useful without requiring access to private account data or copyrighted media.

Planned work:

- synthetic / redistributable demo projects;
- sample timeline packages;
- sample `CURRENT_STATE` transitions;
- first-frame QA fixtures;
- prompt-control examples;
- camera/motion test fixtures;
- normalized-shot-library examples;
- mock post-publish datasets.

Success condition:

Contributors can test workflow changes without using the maintainer's private media or account data.

## Phase 4 — Runtime linting and CI

Goal: prevent documentation and state drift before merge.

Planned checks:

- broken internal links;
- duplicate rule ownership;
- missing required files for authoritative stages;
- invalid state transitions;
- stale version/status headers;
- accidental secret-like strings;
- oversized media committed to Git;
- inconsistent evidence labels.

Where deterministic scripts are sufficient, prefer deterministic CI. Use Codex where semantic review or cross-file reasoning provides additional value.

## Phase 5 — Versioned OSS releases

Goal: move from an evolving research repository to explicit public runtime releases.

Candidate milestones:

- `v0.1` — documented R3 MV runtime on main;
- `v0.2` — state/rule validation automation;
- `v0.3` — reusable public fixtures + CI regression suite;
- `v1.0` — stable runtime contracts, contributor docs, versioned migration policy.

## Non-goals

The project is not intended to:

- claim that one prompt works for every video model;
- hide failed experiments;
- promote a heuristic after one successful generation;
- store private credentials or large copyrighted media archives;
- automate away all human aesthetic decisions.

The long-term goal is a maintainable production runtime where human creative judgment and machine-verifiable correctness can coexist.
