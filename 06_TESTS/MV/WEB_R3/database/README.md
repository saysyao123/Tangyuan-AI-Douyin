# WEB R3｜Douyin Core Database v1

Status: `ACTIVE / R3 TEST DATABASE`
Scope: current 9 unique Douyin accounts only.

## Purpose
R3 song selection must come from a durable account/work database, not one-off search notes.

Canonical chain:
`ACCOUNT IDENTITY -> INGESTION RUN -> WORK -> RAW MUSIC METADATA -> SONG NORMALIZATION -> CROSS-ACCOUNT ANALYSIS -> EVIDENCE PACK -> HG01`

## Source of truth
Git-tracked CSV files are canonical. SQLite is generated for analysis.

- `accounts.csv`: one row per account. `sec_uid` is the stable external key; nickname is mutable.
- `works.csv`: one row per `aweme_id`; stable work/content fields.
- `work_metrics.csv`: time-series engagement snapshots.
- `ingestion_runs.csv`: collection coverage/completeness evidence.
- `song_normalization.csv`: raw music metadata -> `SONG_FAMILY` / `AUDIO_VERSION`.
- `manifest.json`: current snapshot summary.
- `schema.sql` + `build_sqlite.py`: reproducible SQLite layer.

## Hard rules
1. Never join accounts by nickname; use `sec_uid` / internal `account_id`.
2. Never join works by title; use `aweme_id`.
3. Do not persist signed CDN video/music URLs as canonical fields; re-resolve them when needed.
4. Missing data is not zero unless the requested collection window is proved closed.
5. Engagement values are snapshots with `observed_at`; later collection appends snapshots.
6. Trend analysis uses normalized `SONG_FAMILY`; exact MV production later locks `AUDIO_VERSION`.
7. Incomplete accounts may be used for exploratory observation but cannot be treated as denominator-complete HG01 evidence.

## Build SQLite
```bash
python build_sqlite.py --out r3_douyin.sqlite3
```
The generated `.sqlite3` is disposable and should not become the Git source of truth.

## Current R3 sequence
1. Bootstrap the 9-account database.
2. Close incomplete Aura / XIANGJISHI pagination using fallback collector paths.
3. Normalize raw music metadata.
4. Calculate 7d/15d repeats, weighted music-radar repeats, 72h concentration and version consistency.
5. Produce direct Douyin work Evidence Pack.
6. Open HG01 only after evidence is ready.
