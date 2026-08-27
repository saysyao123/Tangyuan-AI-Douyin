# OSS MV Optimization Source Intake v1.0

Status: `WAITING_FOR_USER_SOURCE`

## Source project

- Repository / URL:
- Branch / tag / commit:
- License:
- Relevant files / directories:
- User-specified optimization focus:

## What the source actually changes

To be filled after source review.

For each optimization, record:

| ID | Source location | Claimed improvement | Current Runtime equivalent | Integration class | Risk | Test decision |
|---|---|---|---|---|---|---|
| OSS-01 | TBD | TBD | TBD | TBD | TBD | TBD |

Integration classes are defined in `EXPERIMENT_CONTRACT.md`:

- `DIRECT_RUNTIME_REPLACEMENT`
- `STAGE_OVERLAY`
- `KNOWLEDGE_CANDIDATE`
- `TOOLING_ADAPTER`
- `OUT_OF_SCOPE`

## Conflict check

Before implementation explicitly record whether the source conflicts with any locked Runtime rule, especially:

- Canonical state authority;
- HG01–HG05 durable receipts;
- Audio Timeline before time-dependent Director work;
- transition / revision hash-chain logic;
- bounded legacy import;
- media asset identity;
- publish transaction truth;
- Web Bridge guard semantics;
- lyric visual hit > light narrative continuity > flashy camera tricks;
- Patch, Don't Cascade.

A conflict must be resolved explicitly as one of:

- keep current rule and adapt external idea;
- replace current rule for the experiment only;
- reject the external idea;
- escalate experiment scope with a new test contract.

## Minimal integration set

Do not import the source project wholesale by default.

The preferred first test is the smallest set of changes capable of testing the claimed improvement. Record that minimal set here before implementation.

## Source evidence archive

After review, record exact commit SHAs / file paths used so later results are reproducible even if the external repository changes.
