# WEB R3｜Douyin Data Center

This directory is the canonical R3-A historical-observation data center.

Mode: `PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`

It is generated from the locked 9-account core pool and refreshed approximately every 15 days. Missing public observations are treated as `UNKNOWN`, never as negative evidence.

Generated files:
- `observed_works.csv`
- `observed_metrics.csv`
- `snapshots.csv`
- `coverage_latest.csv`
- `song_normalization.csv`
- `song_repeat_candidates.csv`
- `direct_douyin_evidence.json`
- `manifest.json`
- `DATA_CENTER_STATUS.md`

The build script is `../build_public_data_center.py` and the live public collector is `../../tools/run_public_observed_30d.py`.
