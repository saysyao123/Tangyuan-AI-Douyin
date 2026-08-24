# WEB R3｜Data Center Runtime Contract v1

Status: `LOCKED FOR R3 FIRST LOOP`

## 1. What this is

This is the stable database prototype for R3 music-promotion research.
It is a Git-tracked historical observation data center, not a real-time complete Douyin census and not yet a hosted SQL service.

Canonical directory:
`06_TESTS/MV/WEB_R3/database/data_center/`

Canonical branch:
`test/mv-web-r3`

## 2. Stable identity rules

- account external key: `sec_uid`;
- account internal key: `account_id`;
- work primary key: `aweme_id`;
- nickname / Douyin ID are mutable attributes;
- song trend unit: normalized `SONG_FAMILY` at work level;
- exact production sound remains a separate `AUDIO_VERSION` decision after HG01.

Keys must never be redefined without an explicit schema migration.

## 3. Canonical storage

Authoritative generated datasets:
- `observed_works.csv` — cumulative observed works, one row per `aweme_id`;
- `observed_metrics.csv` — time-series engagement snapshots;
- `snapshots.csv` — refresh receipts;
- `coverage_latest.csv` — latest public account-page coverage;
- `song_normalization.csv` — `aweme_id -> SONG_FAMILY/AUDIO_VERSION`;
- `song_repeat_candidates.csv` — positive repeat ranking;
- `direct_douyin_evidence.json` — exact work evidence used before HG01;
- `manifest.json` — machine state/version/window;
- `DATA_CENTER_STATUS.md` — human status.

Source account registry remains:
`../accounts.csv`

## 4. Query interface

Single local/Codex interface:
`../query_data_center.py`

Supported commands:
- `status` — current version/window/counts/refresh due;
- `health` — structural integrity checks;
- `accounts` — core account summaries;
- `account <name|douyin_id|account_id|case_id>` — account + recent observed works;
- `repeats` — ranked repeated SONG_FAMILY values;
- `song <name>` — candidate + direct Douyin evidence;
- `work <aweme_id>` — one work + normalization + latest metrics;
- `search <keyword>` — full observed-data keyword search.

Examples:
```bash
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json status
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json health
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json repeats --limit 10
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json song "如果风会替我说话"
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json account "火乐烁" --limit 15
python 06_TESTS/MV/WEB_R3/database/query_data_center.py --json search "林叙"
```

## 5. ChatGPT/Codex natural-language contract

When the user says any equivalent of:
- `查数据库：X`
- `数据库里找 X`
- `看 X 这首歌`
- `看 X 账号`
- `查重复歌曲`

use this canonical data center first. Do not silently substitute old R3 search-engine shortlist files.

When the user says:
- `更新数据库`
- `刷新抖音数据库`
- `跑一轮数据中心`

run the canonical public historical refresh path for the locked core pool, validate it, and persist the generated data center back to `test/mv-web-r3`.

## 6. Update contract

Current operating mode:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

Current target refresh cadence:
approximately every `15 days`.

Refresh pipeline:
`9 core accounts -> public snapshot -> rolling 30d -> merge by aweme_id -> normalize -> repeat analysis -> validate -> persist`

Update semantics:
- never replace historical works merely because they disappeared from a later public page;
- upsert/merge by `aweme_id`;
- append metric snapshots;
- append refresh receipts;
- recompute normalization/repeat ranking for the current rolling window;
- missing observation remains `UNKNOWN`, never negative evidence.

## 7. Health Gate

Before using the database for HG01, `query_data_center.py health` must PASS.
Minimum checks include:
- all required files exist;
- exactly 9 locked core accounts in this R3 calibration scope;
- unique non-empty `aweme_id`;
- every work references a known account;
- normalization/metrics/direct evidence only reference known works;
- snapshot history exists;
- coverage has one row per locked core account;
- candidate rows have SONG_FAMILY values.

## 8. Versioning / migrations

Current runtime version: `DATA_CENTER_v1`.

Allowed backward-compatible changes without major migration:
- add new observations;
- add new metric snapshots;
- improve normalization aliases/rules;
- add derived analysis fields;
- add new query commands.

Require explicit `v2` migration before:
- changing account/work primary keys;
- changing positive-evidence semantics;
- replacing historical-observation mode with a different canonical evidence model;
- changing canonical file meanings in a breaking way.

## 9. Current limitations

This v1 is stable enough for:
- historical account reference;
- observed work lookup;
- SONG_FAMILY lookup;
- cross-account repeat discovery;
- direct Douyin evidence retrieval;
- periodic refresh and accumulation;
- R3 HG01 song selection.

It is not yet claiming:
- complete real-time Douyin coverage;
- full historical pagination for every account;
- hosted multi-user SQL/API availability;
- guaranteed current-minute engagement counts.

Those are future upgrades and are not required for the first R3 loop.

## 10. Lock decision

For R3 first loop, this data center is the canonical source of truth for core-account observed song evidence.
Old R3 public-search candidate files are supplemental/historical only and must not override this data center.
