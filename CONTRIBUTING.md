# Contributing to Tangyuan AI Douyin

Thank you for helping improve the project.

This repository treats AI media production workflows as a testable runtime rather than a loose prompt collection. Contributions are most useful when they improve **reproducibility, correctness, observability, maintainability, or cross-project reuse**.

## Good contribution areas

We especially welcome work on:

- workflow and state-machine consistency;
- validation scripts and GitHub Actions;
- prompt/runtime regression tests;
- audio timeline provenance and QA;
- first-frame and image-to-video evaluation methods;
- camera / motion execution tests;
- source-normalization tooling;
- editability and clean-endpoint checks;
- stale-document / broken-reference detection;
- issue templates and reproduction workflows;
- release and promotion automation;
- documentation that makes the runtime easier to reuse outside the original account experiment.

## Evidence before promotion

A technique working once is not enough to become a production rule.

When proposing a new production heuristic, include as much of the following as possible:

1. **Problem** — what failed or remained unstable?
2. **Hypothesis** — what single change is being tested?
3. **Environment** — model/tool, source type, duration, relevant constraints.
4. **Result** — what actually happened, including partial failures.
5. **Evidence level** — single positive result, repeated result, cross-song result, etc.
6. **Regression risk** — which existing rules or stages could be affected?
7. **Promotion target** — knowledge candidate, experimental production rule, or authoritative runtime rule.

Prefer small, reversible rule changes over broad rewrites.

## Runtime change discipline

The active MV runtime follows a strict authority hierarchy.

A typical change should move through:

`experiment -> receipt -> review -> regression -> promotion`

Do not directly turn an untested observation into a hard rule.

For changes to authoritative workflows or rules:

- identify the stage(s) affected;
- check whether downstream artifacts become invalid;
- avoid duplicating rules across multiple files;
- prefer JIT-loaded specialized rules over expanding one giant instruction file;
- document rollback boundaries;
- preserve existing Human Gates unless the proposal explicitly tests a gate change.

## Pull requests

A useful PR description should include:

- **What changed**
- **Why**
- **Evidence / reproduction**
- **Files and stages affected**
- **Backward-compatibility / regression notes**
- **Whether the change is EXPERIMENTAL or PRODUCTION-READY**

Keep PRs focused. A local production problem should not trigger unrelated architecture changes.

## Issues

When reporting a failure, please include:

- expected behavior;
- actual behavior;
- runtime stage;
- relevant rule/workflow file;
- minimal reproducible inputs or metadata when they can be shared legally;
- whether the issue is deterministic or intermittent;
- screenshots/logs with secrets and personal data removed.

Do not upload copyrighted media merely to reproduce an issue if a metadata-only or synthetic reproduction is sufficient.

## Repository safety

Never commit:

- API keys or bearer tokens;
- cookies or browser/session state;
- passwords or secrets;
- private emails, phone numbers, IDs, or account credentials;
- unredacted private analytics/admin screenshots;
- private chat transcripts;
- third-party copyrighted media without redistribution rights.

Large generated outputs should normally stay outside Git. Commit indexes, hashes, timing metadata, QA reports, recipes, or receipts instead.

## Branches

Current production research may live on explicit test branches before promotion to `main`.

Examples:

- `test/...` — experiments, probes, cross-song validation;
- `chore/...` — repository maintenance and documentation;
- feature/fix branches — focused implementation work.

The current R3 MV runtime is being hardened on `test/mv-web-r3` before formal promotion.

## Maintainer review

The maintainer may request:

- a smaller reproduction;
- clearer evidence;
- separation of unrelated changes;
- a rollback plan;
- additional cross-song / cross-source validation before a rule is promoted.

The goal is not maximum rule count. The goal is a smaller, more reliable runtime whose behavior can be explained and reproduced.
