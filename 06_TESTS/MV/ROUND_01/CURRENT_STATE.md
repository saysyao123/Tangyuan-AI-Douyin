# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S01`
- STAGE_NAME: `最近 7 天热门 BGM 筛选`
- STATE: `IN_PROGRESS`
- PREVIOUS_LOCK: `ROUND_CHARTER_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- CHARTER_COMMIT: `e112e602ad1e9f66c390bab3341e2db7f8258960`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked Decisions

- R1 is a Golden Sample calibration round, not an automation-speed round.
- R1 does not use 1 hour as a pass/fail target.
- GitHub is the unique fact / rules / state source; large media mainly stays on the user's local computer with a matching directory/index structure.
- All stage outputs must pass AI self-check before entering human review.
- Round 01 critical stages use two-step commits: stage output commit → `READY_FOR_REVIEW` → user PASS → separate LOCK commit + Current State update.
- Seedance 2 mini is the fixed video model for R1.
- GPT is the fixed first-frame image model for R1.
- User acts only as Seedance execution operator during R1; no hidden prompt rescue.

## R1S01 Goal

Find and rank 5 strong Chinese-language BGM candidates from the most recent 7-day Douyin trend window for MV production.

Candidate composition target:
- 4 candidates: high heat + strong MV interaction + high fit for the current New Eastern cinematic visual system.
- 1 challenge candidate: very high heat but lower visual-system fit.

Primary ranking logic:
1. Related MV-video interaction performance;
2. recent 7-day growth / momentum;
3. BGM usage heat;
4. fit with the current visual system;
5. expected beauty / production success rate.

If heat differences are small, prefer the candidate with a higher probability of producing a beautiful MV.

## R1S01 Required Checks

Before a BGM can be marked `BGM_AVAILABLE`, verify as far as public data allows:
1. The BGM is discoverable on Douyin;
2. New videos have used it recently;
3. The user's own Douyin account can select it and enter the publishing flow — this final account-level check is performed by the user.

Also identify the dominant current hot clip template when possible:
- common start point;
- common end point;
- common duration;
- alternative clip templates if any;
- relative MV interaction performance between templates.

## Current Effective Files

- `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- `06_TESTS/MV/ROUND_01/CURRENT_STATE.md`
- Runtime architecture remains inherited from `refactor/thin-skill-architecture-v3`.

## Current Risks / Unknowns

- Whether reliable 7-day Douyin BGM usage / interaction / growth data can be obtained consistently from public and third-party sources is not yet proven.
- Douyin account-level BGM availability cannot be fully confirmed without the user's final in-app check.
- Exact audio extraction / acquisition path for the selected BGM remains to be tested after candidate selection.

## Next Allowed Action

**Only execute R1S01:** research current 7-day Douyin BGM / MV trends, build the 5-candidate shortlist, document data confidence and missing fields, run AI self-check, then submit R1S01 output as `READY_FOR_REVIEW`.

Do not begin music-structure analysis, Beat design, director design, first-frame generation, Seedance generation, or editing before R1S01 is locked.