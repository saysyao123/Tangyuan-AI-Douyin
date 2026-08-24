# WEB R3｜Douyin Data Center v1

- Mode: `PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`
- Anchor: `2026-08-17 22:41:09`
- Rolling window: `2026-07-19 00:00:00` → `2026-08-18 00:00:00`
- Core accounts: `9`
- Fresh snapshot rows: `134`
- Cumulative unique observed works: `134`
- AUTO_HIGH works in current window: `98`
- Repeated SONG_FAMILY: `8`
- Refresh cadence: every `15` days

## Evidence semantics

- Observed same-song use across independent core accounts is valid positive evidence.
- Missing works/accounts are UNKNOWN, never interpreted as a negative signal.
- Current ranking is an observed-repeat ranking, not a complete-platform popularity ranking.

## Top observed repeats

| SONG_FAMILY | acc/15d | acc/30d | weighted/15d | best72h | visual overlap | grade |
|---|---:|---:|---:|---:|---:|---|
| 如果风会替我说话 | 3 | 3 | 2.1 | 3 | 2 | STRONG |
| 爱让人脑袋空空 | 2 | 2 | 1.65 | 1 | 1 | CONFIRMED_REPEAT |
| 有几次想你了 | 2 | 2 | 1.45 | 2 | 1 | CONFIRMED_REPEAT |
| 做她的大地别做她的天 | 2 | 2 | 1.35 | 2 | 1 | CONFIRMED_REPEAT |
| 杀破狼 | 2 | 2 | 1.1 | 2 | 2 | CONFIRMED_REPEAT |
| 若爱有尽头 | 2 | 2 | 1.1 | 2 | 2 | CONFIRMED_REPEAT |
| 我救自己于人间水火 | 2 | 2 | 0.8 | 2 | 2 | CONFIRMED_REPEAT |
| Summer Love 爱在盛夏 | 2 | 2 | 0.8 | 2 | 2 | CONFIRMED_REPEAT |

## Canonical files

- `observed_works.csv` — cumulative observed work facts
- `observed_metrics.csv` — engagement snapshots
- `snapshots.csv` — every refresh receipt
- `coverage_latest.csv` — latest public page coverage per account
- `song_normalization.csv` — work-level SONG_FAMILY mapping
- `song_repeat_candidates.csv` — positive cross-account repeat ranking
- `direct_douyin_evidence.json` — exact account/work links for HG01
- `manifest.json` — machine-readable state
