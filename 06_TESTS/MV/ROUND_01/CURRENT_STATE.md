# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S01`
- STAGE_NAME: `最近 7 天热门 BGM 筛选`
- STATE: `READY_FOR_REVIEW`
- PREVIOUS_LOCK: `ROUND_CHARTER_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- CHARTER_COMMIT: `e112e602ad1e9f66c390bab3341e2db7f8258960`
- STAGE_OUTPUT: `06_TESTS/MV/ROUND_01/R1S01_BGM_SELECTION.md`
- STAGE_OUTPUT_COMMIT: `d9fae80f6702f7fe3a1771686d13466620812a98`
- AI_SELF_CHECK: `PASS`
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

## R1S01 Result Summary

Five candidates are ready for human review:
1. `我们好像在哪见过` — R1 recommended first choice; strong recent heat persistence + very high visual fit.
2. `雨下一整晚` — very high visual fit; latest momentum requires Douyin in-app confirmation.
3. `好想再爱你` — strong recent heat + emotional fit; exact trending audio version must be locked.
4. `差一步` — strong current edit trend + high saturation / homogeneity risk.
5. `分手就分手` — challenge candidate; current “你终于开了口反差转场” signal is fresh, but exact Remix/audio must be locked.

## Data Confidence / Known Gap

Public sources can support recent Douyin trend-topic heat, recent usage evidence, song identity and some visible interaction samples, but do not expose a consistent public dataset for exact audio-level 7-day total uses, total MV likes or growth curves.

Therefore R1S01 uses evidence confidence rather than fake precision. Final `BGM_AVAILABLE` still requires Douyin in-app confirmation.

## Waiting For Human Review

User should:
1. review / listen to the 5 candidates and choose 1 preferred R1 Golden Sample track;
2. check the selected track in Douyin and confirm the currently active audio can be found and selected by the user's account;
3. if multiple audio versions exist, return the current active version / screenshot / link so the system can lock the exact BGM and dominant clip template.

## Current Effective Files

- `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- `06_TESTS/MV/ROUND_01/R1S01_BGM_SELECTION.md`
- `06_TESTS/MV/ROUND_01/CURRENT_STATE.md`
- Runtime architecture remains inherited from `refactor/thin-skill-architecture-v3`.

## Current Risks / Unknowns

- Exact audio-level 7-day Douyin total-use / total-MV-interaction / growth data is not publicly complete.
- Douyin account-level BGM availability is pending user in-app verification.
- Exact hot audio version and exact dominant clip start/end seconds are not locked yet.
- Exact audio extraction / acquisition path will be tested only after BGM lock.

## Next Allowed Action

**Only complete R1S01 human review and BGM availability lock.**

Do not begin music-structure analysis, Beat design, director design, first-frame generation, Seedance generation, or editing before R1S01 receives user PASS and a separate LOCK commit.