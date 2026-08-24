# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / NINE_ACCOUNT_DATABASE + COMPLETENESS`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / NINE_ACCOUNT_TEST_SCOPE_LOCKED / DOUYIN_DATA_PATH_PASS / DATABASE_BOOTSTRAP_PASS / SQLITE_VALIDATION_PASS / 7_OF_9_15D_COMPLETE / AURA_PAGINATION_PENDING / XIANGJISHI_PAGINATION_PENDING / SONG_NORMALIZATION_PENDING / HG01_NOT_READY`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Current authority

Primary R3-A authority is now:
`R3_DOUYIN_DATABASE_PROTOCOL_v1.md`

Database source of truth:
`06_TESTS/MV/WEB_R3/database/`

The old public-search shortlist remains supplemental only and cannot bypass the database path.

## Nine-account R3 test scope｜LOCKED FOR THIS ROUND

This calibration round uses exactly 9 unique Douyin accounts. Do not expand the sample pool before the first complete database -> normalization -> analysis -> HG01 loop is finished.

Current identities are stored in `database/accounts.csv` with `sec_uid` as the stable external key and `aweme_id` as the work key.

The ninth account, `Lynne小凌`, is currently `R3_TEST_SUPPLEMENT`; its permanent role/weight is deliberately left for post-test calibration.

## Database bootstrap result｜PASS

Automated bootstrap run at `2026-08-24 17:05 +08:00` produced:
- 9 unique accounts;
- 89 real works in the current 15-day window;
- 89 engagement snapshots;
- 9 ingestion-run records;
- generated SQLite validation: `foreign_key_check = PASS`;
- `song_normalization` intentionally empty pending the next stage.

Canonical files:
- `database/accounts.csv`
- `database/works.csv`
- `database/work_metrics.csv`
- `database/ingestion_runs.csv`
- `database/song_normalization.csv`
- `database/manifest.json`
- `database/schema.sql`
- `database/build_sqlite.py`

## 15-day completeness｜PARTIAL, EXPLICIT

Requested test window:
- start: `2026-08-10 00:00:00`
- end exclusive: `2026-08-25 00:00:00`

Current closure:
- 7/9 accounts = `COMPLETE`;
- Aura = `INCOMPLETE / EMPTY_PAGE_WITH_HAS_MORE`;
- XIANGJISHI = `INCOMPLETE / EMPTY_PAGE_WITH_HAS_MORE`.

This does **not** mean Aura / XIANGJISHI have no earlier works. Their page-1 data is real, but public pagination did not close the requested window.

Correct rollback/fallback path:
`PUBLIC_FAST -> SELF_HOST(cookie) -> SESSION_FALLBACK(jiji/browser)`.

## Data rules now locked for R3

- nickname is mutable and never a join key;
- `sec_uid` identifies account;
- `aweme_id` identifies work;
- signed CDN video/music URLs are not canonical DB fields;
- engagement is stored as time-series snapshots;
- incomplete retrieval never silently becomes zero;
- trend calculations must use normalized `SONG_FAMILY`;
- actual MV production later locks exact `AUDIO_VERSION`.

## Next execution order

1. Close Aura + XIANGJISHI 15-day pagination with fallback collector paths.
2. Populate `song_normalization.csv` from the 89+ work rows.
3. Compute database-only analysis:
   - `distinct_account_repeat_15d`;
   - `distinct_account_repeat_7d`;
   - `music_radar_weighted_repeat`;
   - `visual_account_repeat`;
   - `72h_concentration`;
   - `audio_version_consistency`.
4. Build direct Douyin work Evidence Pack for strongest candidates.
5. Only then set `HG01_READY = YES` and ask user to choose the R3 song.

## Not allowed now

- no expansion beyond these 9 accounts as the main R3 test sample;
- no HG01 choice from the old shortlist;
- no BGM lock;
- no R3-B visual work;
- no treating the current 89 works as full 9-account coverage until Aura / XIANGJISHI are closed or explicitly fallback-failed with evidence.
