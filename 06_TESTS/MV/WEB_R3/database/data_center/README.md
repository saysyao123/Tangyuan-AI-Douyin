# WEB R3｜Douyin Data Center v1

Canonical R3-A historical-observation data center for the locked 9-account core pool.

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
- `manifest.json` — machine-readable current state;
- `DATA_CENTER_STATUS.md` — compact human-readable report.

## Build path

Collector:
`../../tools/run_public_observed_30d.py`

Builder:
`../build_public_data_center.py`

Automation:
`.github/workflows/r3-public-data-center-build.yml`

The workflow performs:
`public collect -> 30d snapshot -> aweme_id merge -> SONG_FAMILY normalization -> repeat analysis -> validation -> automatic commit back to test/mv-web-r3`.

## Evidence grades

- `STRONG`: observed in 3+ independent core accounts;
- `CONFIRMED_REPEAT`: observed in 2 independent core accounts;
- single-account observations are retained in the work database but do not enter the repeat shortlist.

## Current refresh policy

Target cadence: every 15 days. The first canonical build was completed on 2026-08-24; the approximate next refresh due date is stored in `manifest.json`.
