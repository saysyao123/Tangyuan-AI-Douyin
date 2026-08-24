# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / DATA_CENTER_READY -> DIRECT_EVIDENCE_QA`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / NINE_ACCOUNT_TEST_SCOPE_LOCKED / PUBLIC_HISTORICAL_MODE_LOCKED / DATA_CENTER_V1_PASS / 30D_POSITIVE_EVIDENCE_PASS / AUTO_REFRESH_PASS / SONG_NORMALIZATION_PASS / REPEAT_ANALYSIS_PASS / HG01_DATA_READY / HG01_PENDING_USER_REVIEW`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Current authority

Canonical R3-A data center:
`06_TESTS/MV/WEB_R3/database/data_center/`

Operating contract:
`database/data_center/README.md`

Machine state:
`database/data_center/manifest.json`

Human status:
`database/data_center/DATA_CENTER_STATUS.md`

The old public-search shortlist is historical/supplemental only and cannot bypass the data-center evidence path.

## Locked R3-A operating mode

`9 CORE ACCOUNTS -> PUBLIC OBSERVED SNAPSHOT -> ROLLING 30D -> AWEME_ID MERGE -> WORK-LEVEL SONG_FAMILY -> POSITIVE CROSS-ACCOUNT REPEAT -> DIRECT DOUYIN EVIDENCE -> HG01`

Mode:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

Evidence semantics:
- directly observed repetition across independent core accounts is valid positive evidence;
- unobserved work/song = `UNKNOWN`, never negative evidence;
- the data center is an observed-repeat system, not a complete real-time Douyin census.

Authenticated F2 / jiji / TikHub are retained as future upgrade/fallback paths and are not prerequisites for the first R3 loop.

## Nine-account core pool｜LOCKED

Exactly 9 unique Douyin accounts are used for this calibration round.
Do not expand the main sample pool until the first data -> song -> MV -> publish loop is complete.

Stable identity:
- account: `sec_uid` / internal `account_id`;
- work: `aweme_id`;
- nickname is mutable.

## Data Center v1｜PASS

First canonical build completed at approximately `2026-08-24 20:29 +08:00`.

Current observation anchor:
- latest reliably observed work: `2026-08-17 22:41:09`;
- rolling window start: `2026-07-19 00:00:00`;
- rolling window end exclusive: `2026-08-18 00:00:00`.

Current dataset:
- core accounts: `9`;
- fresh public observations: `134` works;
- cumulative unique observed works: `134`;
- AUTO_HIGH normalized works in current window: `98`;
- REVIEW_REQUIRED: `24`;
- UNRESOLVED: `12`;
- cross-account repeated SONG_FAMILY: `8`.

Current strongest observed repeat:
- `如果风会替我说话`;
- observed in `3` independent core accounts;
- all 3 observations fall inside the latest 15-day half-window;
- best 72h concentration: `3` accounts;
- visual-overlap accounts: `2`;
- evidence grade: `STRONG`.

Other observed repeats (2 independent accounts each):
- `爱让人脑袋空空`;
- `有几次想你了`;
- `做她的大地别做她的天`;
- `杀破狼`;
- `若爱有尽头`;
- `我救自己于人间水火`;
- `Summer Love 爱在盛夏`.

## Canonical data-center files

- `database/data_center/observed_works.csv` — cumulative observed work facts;
- `database/data_center/observed_metrics.csv` — engagement snapshots;
- `database/data_center/snapshots.csv` — refresh receipts;
- `database/data_center/coverage_latest.csv` — latest public-page account coverage;
- `database/data_center/song_normalization.csv` — work-level SONG_FAMILY/AUDIO_VERSION mapping;
- `database/data_center/song_repeat_candidates.csv` — repeat ranking;
- `database/data_center/direct_douyin_evidence.json` — exact account/work links for HG01;
- `database/data_center/manifest.json` — machine-readable state;
- `database/data_center/DATA_CENTER_STATUS.md` — human-readable status.

## Refresh automation｜PASS

Collector:
`tools/run_public_observed_30d.py`

Builder:
`database/build_public_data_center.py`

Workflow:
`.github/workflows/r3-public-data-center-build.yml`

Validated flow:
`public collect -> 30d snapshot -> aweme_id merge -> normalization -> repeat analysis -> validation -> auto-commit back to test/mv-web-r3`.

Target cadence:
- refresh approximately every `15 days`;
- current approximate next refresh: `2026-09-08`;
- every refresh preserves prior observations and merges by `aweme_id`.

## Current Gate

`HG01_DATA_READY = YES`

But HG01 has **not** passed yet.

Next required step is to turn the strongest database candidates into a user-facing Direct Douyin Evidence Pack and let the user inspect the exact core-account works before choosing one `SONG_FAMILY`.

## Next execution order

1. QA `direct_douyin_evidence.json` for the strongest candidates.
2. Deliver direct core-account Douyin work links to the user, starting with the strongest repeated families.
3. Run `HG01 Song Aesthetic Gate` and lock one `SONG_FAMILY` only after user confirmation.
4. Enter R3-B0 exact `AUDIO_VERSION` discovery and HG02 BGM listening.
5. Continue the R2-validated audio timeline / director / MV chain.
6. Refresh the data center again in ~15 days and merge new observations.

## Not allowed now

- no expansion beyond the 9 core accounts before the first loop closes;
- no claim that observed absence means an account did not publish something;
- no claim that this is a complete real-time Douyin trend database;
- no requirement to log in to the user's Douyin account for the first R3 loop;
- no BGM lock or visual work before HG01 PASS.
