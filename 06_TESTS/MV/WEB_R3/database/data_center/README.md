# WEB R3｜Douyin Data Center v1

Canonical R3-A historical-observation data center for the locked 9-account core pool.

Status: `STABLE DATABASE PROTOTYPE / R3 FIRST LOOP SOURCE OF TRUTH`

Runtime contract:
`DATA_CENTER_RUNTIME_CONTRACT_v1.md`

## Operating mode

`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

- use the latest reliably observed public work as the anchor;
- analyze the rolling 30 days ending at that anchor;
- refresh approximately every 15 days;
- merge by `aweme_id` and preserve prior observations;
- missing observations are `UNKNOWN`, never negative evidence;
- rank only directly observed cross-account SONG_FAMILY repeats.

This first R3 loop intentionally does **not** require real-time freshness, authenticated Douyin sessions, or complete deep pagination.

## Stable keys

- account: `sec_uid` / internal `account_id`;
- work: `aweme_id`;
- song trend unit: work-level normalized `SONG_FAMILY`;
- production audio is locked later as exact `AUDIO_VERSION`.

## Canonical generated files

- `observed_works.csv` — cumulative observed work facts;
- `observed_metrics.csv` — engagement snapshots by observation time;
- `snapshots.csv` — every refresh receipt and anchor/window;
- `coverage_latest.csv` — latest visible public-page coverage per account;
- `song_normalization.csv` — work-level SONG_FAMILY/AUDIO_VERSION mapping;
- `song_repeat_candidates.csv` — positive cross-account repeat ranking;
- `direct_douyin_evidence.json` — exact core-account Douyin work links for HG01;
- `manifest.json` — machine-readable current state/version;
- `DATA_CENTER_STATUS.md` — compact human-readable report.

Source account registry:
`../accounts.csv`

## Stable query interface

Query tool:
`../query_data_center.py`

Commands:
- `status`
- `health`
- `accounts`
- `account <account>`
- `repeats`
- `song <song>`
- `work <aweme_id>`
- `search <keyword>`

Examples:
```bash
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json status
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json health
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json repeats --limit 10
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json song "如果风会替我说话"
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json account "火乐烁" --limit 15
```

Natural-language calls such as `查数据库：X` / `更新数据库` are defined in the runtime contract and should resolve to this data center by default.

## Build/update path

Collector:
`../../tools/run_public_observed_30d.py`

Builder:
`../build_public_data_center.py`

Automation:
`.github/workflows/r3-public-data-center-build.yml`

Validated workflow:
`public collect -> rolling 30d -> aweme_id merge -> SONG_FAMILY normalization -> repeat analysis -> health validation -> automatic commit back to test/mv-web-r3`.

## Evidence grades

- `STRONG`: observed in 3+ independent core accounts;
- `CONFIRMED_REPEAT`: observed in 2 independent core accounts;
- single-account observations are retained in the work database but do not enter the repeat shortlist.

## Current refresh policy

Target cadence: approximately every 15 days.
The current approximate next refresh due date is machine-stored in `manifest.json`.

A refresh never deletes historical observations merely because a later public page no longer shows them. Historical facts are accumulated by `aweme_id`; metric snapshots and refresh receipts are append-oriented.

## Production boundary

This v1 is stable enough for:
- database reference;
- account/work/song lookup;
- repeated-song analysis;
- direct Douyin evidence retrieval;
- periodic updates;
- R3 HG01 decisions.

It is not yet a hosted real-time SQL/API service and does not claim complete Douyin coverage. Those are future upgrades, not blockers for R3 v1.
