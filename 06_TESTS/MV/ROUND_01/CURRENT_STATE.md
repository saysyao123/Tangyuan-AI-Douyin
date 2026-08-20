# Round 01｜CURRENT_STATE

> This file is the unique state entry for Round 01. New Chat / Codex / Agent must read this file first.

## Current Status

- ROUND: `R1`
- STAGE: `R1S01`
- STAGE_NAME: `热门 BGM 发现 / 用户选歌 / Exact Entity 验证`
- STATE: `IN_PROGRESS_BGM_PICK`
- PREVIOUS_LOCK: `ROUND_CHARTER_LOCKED`
- BRANCH: `test/mv-round-01`
- CHARTER: `06_TESTS/MV/ROUND_01/ROUND_CHARTER.md`
- CHARTER_COMMIT: `e112e602ad1e9f66c390bab3341e2db7f8258960`
- PRELIMINARY_OUTPUT: `06_TESTS/MV/ROUND_01/R1S01_BGM_SELECTION.md`
- PRELIMINARY_OUTPUT_STATUS: `NOT_LOCKABLE`
- SELECTION_OBSERVER_POOL: `06_TESTS/MV/ROUND_01/R1S01_SELECTION_OBSERVER_POOL.md`
- ACTIVE_POC: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/README.md`
- CODEX_REQUIREMENT: `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/CODEX_TEST_REQUIREMENT.md`
- MV_BENCHMARK_LAYER: `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`
- CURRENT_BENCHMARK_SNAPSHOT: `06_TESTS/MV/ROUND_01/R1_BENCHMARK_SNAPSHOT_2026-08-21.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Latest User Decision｜Simplify S01

User feedback shows the previous S01 became too technically heavy before the user could simply judge the songs.

New approved order inside the same S01:

`5-source song observer pool -> recent 30-day repeated-song scan -> direct real MV/video links -> user taste pick -> exact music entity / account availability / hot interval validation -> S01 LOCK`

This is a reordering, **not removal**, of `BGM_DATASOURCE_READY`.

The user should not be blocked by Git/Python/Codex setup before first hearing/seeing candidate songs.

## Current User Taste Feedback

From the latest reference set:
- `你有没有真的爱过我`: acceptable / shortlist.
- `午后树下微风`: acceptable / shortlist.
- `回到小村落`: reference link unavailable; no current judgment.
- `像我这样爱你的人`: reference link unavailable; no current judgment.
- `起势`: user does not like it; downgrade.
- `借一页童话`: user says it does not feel enough like an MV; downgrade for current Golden Sample direction.
- `山风山风等等我`: user does not like it; remove from current R1 candidate path.

### Current recommendation

Primary R1 candidate: `你有没有真的爱过我`.
Backup: `午后树下微风`.

Reason: `你有没有真的爱过我` has visible cross-content diffusion beyond the AIMV account (recent dance / emotion-music usage), while public evidence for `午后树下微风` is still mainly concentrated in one AIMV source.

## R1S01 Song Observer Pool｜Active

Use `R1S01_SELECTION_OBSERVER_POOL.md` for song discovery. Current five sources:
1. AI MV导演曹斌Johnny — high-frequency AIMV / MV vertical adoption.
2. 清琉隐士 — hot-song + self-made MV distribution signal.
3. 最熟悉的陌生人2022《音乐视频制作》 — music-video production / new-song / 看见音乐计划 signal.
4. 城市音乐 — broader hot-song / music-consumption diffusion signal.
5. 相信音乐官方MV — official-version / release / identity anchor.

Important: these five are a **song-observer pool**, not a claim that all five are equivalent “top creators” by follower count.

### Simplified repeated-song rule
- Seen in >=2 observer sources -> candidate.
- Seen in >=3 -> `CROSS_ACCOUNT_HOT_LEAD`.
- Then verify recent diffusion outside MV accounts (dance / cover / lifestyle / emotion music).
- Give the user real MV/video links first.
- User taste can immediately downgrade a hot song.

## Rolling MV Benchmark Layer｜Active Knowledge

Full aesthetic/director Benchmark Pool remains separate:
- `04_HARNESS/knowledge/MV_BENCHMARK_LAYER.md`

It is loaded JIT in later stages:
- Opening Hook: same-BGM + relevant benchmark works;
- Director: 3–5 relevant works;
- First-frame: 2–3 Beauty references;
- Dynamic: 2–3 Director/Action references;
- Final QA: 2–3 completion/market references.

External benchmark observations never directly become hard Rules / Golden References.

## BGM_DATASOURCE_READY｜Still Required Before S01 LOCK

After user picks one song, complete this chain:
1. lock exact Douyin music entity / version as far as possible;
2. distinguish original / cover / DJ / Remix;
3. identify a 10–30s current hot reference interval / sample;
4. on Codex-capable computer, validate current account `AVAILABLE_AT_BUILD` in Creator Center;
5. preserve account-side validation requirement for later `AVAILABLE_AT_PUBLISH`.

The first local Windows PoC was blocked before reaching this test because Git/Python/Pip environment was unavailable. Classification: `ENVIRONMENT_DEPENDENCY_FAILURE`, not datasource failure.

Full account/browser test is deferred to:
- `06_TESTS/MV/ROUND_01/R1S01_DATASOURCE/CODEX_TEST_REQUIREMENT.md`

## Current Risks / Unknowns

- Exact music_id / hot version is not locked yet.
- Creator Center account availability requires later Codex-side live calibration.
- Public search/index can identify adoption and song identity but cannot prove future publish rights.
- `AVAILABLE_AT_BUILD` does not guarantee future availability; final production still requires `AVAILABLE_AT_PUBLISH`.

## Next Allowed Action

**Continue R1S01 only.**

Immediate action:
- expand comparison from one AIMV creator to the five-source observer pool;
- use recent-30-day/recent-7-day evidence to identify repeated songs;
- present direct real MV/video references to the user;
- currently prefer `你有没有真的爱过我` over `午后树下微风` unless new cross-account evidence changes the ranking.

After the user picks the song, perform Exact Entity / availability validation before S01 LOCK.

Do not begin music-structure analysis, Beat design, director design, first-frame generation, Seedance generation or editing before S01 receives a separate LOCK commit.