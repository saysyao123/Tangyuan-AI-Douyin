# WEB R3｜Database Song Analysis v1

- observed_at: `2026-08-24T17:47:17+08:00`
- eligible normalized works: `83` / `89`
- repeated SONG_FAMILY (2+ accounts): `9`
- latest-edge gate: `FAIL`
- stale/high-trend accounts: `DYCORE01, DYCORE03, DYCORE06, DYCORE08`

## Interpretation

This report is database-only. 15-day repeat values are lower bounds while any account is incomplete, and no current 7-day/72h trend conclusion is allowed while the latest-edge gate fails.

## Repeated song families｜lower bound

| SONG_FAMILY | accounts/15d | weighted radar | visual overlap | local72h | versions | latest observed |
|---|---:|---:|---:|---:|---:|---|
| 爱让人脑袋空空 | 4 | 2.5 | 1 | 3 | 4 | 2026-08-14T18:22:13+08:00 |
| 如果风会替我说话 | 3 | 2.1 | 1 | 3 | 1 | 2026-08-15T19:08:14+08:00 |
| 沈园外 | 2 | 1.5 | 0 | 2 | 2 | 2026-08-16T20:16:04+08:00 |
| 有几次想你了 | 2 | 1.45 | 1 | 2 | 1 | 2026-08-15T19:02:51+08:00 |
| 做她的大地别做她的天 | 2 | 1.35 | 1 | 2 | 1 | 2026-08-15T17:05:47+08:00 |
| 杀破狼 | 2 | 1.1 | 1 | 2 | 2 | 2026-08-14T20:03:41+08:00 |
| 若爱有尽头 | 2 | 1.1 | 1 | 2 | 1 | 2026-08-14T17:43:48+08:00 |
| Summer Love 爱在盛夏 | 2 | 0.8 | 2 | 2 | 1 | 2026-08-13T17:00:00+08:00 |
| 我救自己于人间水火 | 2 | 0.8 | 2 | 2 | 2 | 2026-08-13T18:25:19+08:00 |

## Gate

HG01 remains blocked if either:
- any required 15-day core window is not closed;
- high-trend account latest-edge freshness is not verified.
