# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / PUBLIC_OBSERVED_30D`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / NINE_ACCOUNT_TEST_SCOPE_LOCKED / PUBLIC_DATA_PATH_PASS / HISTORICAL_OBSERVATION_MODE_LOCKED / 30D_POSITIVE_EVIDENCE_ONLY / BIWEEKLY_REFRESH / SONG_NORMALIZATION_NEXT / HG01_NOT_READY`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Current R3 strategy｜SIMPLIFIED

R3 no longer requires real-time/latest-edge completeness before the first song test.

Current test path:

`9 CORE ACCOUNTS -> PUBLIC OBSERVED SNAPSHOT -> 30-DAY HISTORICAL WINDOW -> WORK-LEVEL SONG_FAMILY -> CROSS-ACCOUNT POSITIVE REPEAT -> DIRECT DOUYIN WORK EVIDENCE -> HG01`

The goal of R3-A is now to prove that a stable public historical sample is sufficient to select a useful song and complete one full MV loop.

Authenticated F2 / jiji / TikHub remain future upgrade paths and are **not** prerequisites for the first R3 loop.

## Nine-account R3 test scope｜LOCKED

Exactly 9 unique Douyin accounts are used for this calibration round.
Do not expand the core pool before the first observed-data -> song -> MV -> publish loop is complete.

Stable identity:
- account key: `sec_uid`;
- work key: `aweme_id`;
- nickname is mutable.

## Historical Observation Mode｜LOCKED FOR R3 TEST

### Anchor

Use the latest reliably observed work timestamp from the current public collection as the analysis anchor.

### Window

Create a rolling 30-day historical observation window ending at the anchor day.

Example when anchor day is `2026-08-17`:
- window start: approximately `2026-07-19 00:00:00`;
- window end exclusive: `2026-08-18 00:00:00`.

### Evidence semantics

This mode uses **positive evidence only**.

Allowed inference:
- if the same normalized SONG_FAMILY is directly observed in 2/3/4 independent core accounts, that cross-account repeat is valid evidence.

Forbidden inference:
- a work not observed does NOT mean the account did not publish it;
- a song not seen on an account does NOT count as a negative signal;
- partial public pagination must not be converted into zero.

Therefore missing high-frequency historical pages reduce recall, but they do not invalidate a positive repeated-song signal.

## Refresh cadence｜15 DAYS

For the first R3 operating model:
- refresh the 9-account public snapshot every ~15 days;
- merge by `aweme_id` instead of replacing history;
- keep the latest observed anchor of every snapshot;
- accumulate historical works over time;
- after multiple refreshes, dependence on deep historical pagination naturally decreases.

Real-time monitoring is explicitly out of scope for the first R3 loop.

## Existing database result｜SEED DATA

The first public bootstrap produced:
- 9 unique accounts;
- 89 real work rows in the previously requested 15-day slice;
- work URLs, captions, raw music metadata, hashtags and interaction snapshots;
- SQLite foreign-key validation PASS.

These rows remain valid seed observations, but prior `7/9 COMPLETE` labels are no longer used as a prerequisite for HG01 in Historical Observation Mode.

## Current public capability boundary

Reliable now:
- shared profile URL -> `sec_uid`;
- core account identity;
- public first-page work observations;
- `aweme_id` + publish time + caption + hashtags;
- raw music title/author;
- direct Douyin work URL;
- engagement snapshot;
- known-work single-video parsing;
- on-demand MP4 resolution/download.

Not required for this R3 loop:
- latest-minute freshness;
- complete deep pagination for every high-frequency account;
- full account history;
- authenticated Douyin session.

## New collection artifact

Historical observed collector:
`tools/run_public_observed_30d.py`

Expected snapshot output:
`database/public_observed_30d/`

Semantics:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`.

## Next execution order

1. Build the first 30-day observed public snapshot from the 9 locked accounts.
2. Normalize works to `SONG_FAMILY` at `aweme_id` level.
3. Rank only positive cross-account repeats.
4. For strongest candidates, generate a direct Douyin Evidence Pack:
   - account;
   - publish time;
   - exact work URL;
   - caption / song evidence;
   - observed audio version when identifiable.
5. Open HG01 and let the user choose one SONG_FAMILY.
6. Continue the existing R2-validated BGM/timeline/MV production chain.
7. Refresh the account sample again in ~15 days and compare new observations.

## Not allowed now

- no expansion beyond 9 core accounts before first loop closes;
- no claim that this is a complete real-time Douyin trend database;
- no treating unobserved works as negative evidence;
- no requirement to log in to the user's Douyin account for the first R3 loop;
- no BGM lock or visual work before HG01.
