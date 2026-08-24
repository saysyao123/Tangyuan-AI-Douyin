# WEB R3｜Douyin Database Protocol v1

> Status: `ACTIVE / R3-A3`
> Scope: current 9 unique Douyin accounts only.
> Goal: turn Douyin retrieval into a durable, updateable evidence database before song analysis.

## 1. R3-A3 main chain
`9 CORE TEST ACCOUNTS`
→ `IDENTITY TABLE`
→ `15D COLLECTION + COMPLETENESS`
→ `WORK TABLE + METRIC SNAPSHOTS`
→ `RAW MUSIC METADATA`
→ `SONG_FAMILY / AUDIO_VERSION NORMALIZATION`
→ `7D / 15D CROSS-ACCOUNT ANALYSIS`
→ `DIRECT WORK EVIDENCE PACK`
→ `HG01`

No old public-search shortlist may bypass this chain.

## 2. Identity model
External stable account key: `sec_uid`.
Internal key: `account_id` (`DYCORE01...`).
Nickname is mutable and must not be used as a database join key.
Work key: `aweme_id`.

## 3. Database tables
- `accounts`: account identity, role/weights, active flag and current 15d completeness.
- `works`: aweme_id, account_id, publish time, direct work URL, caption, media metadata and raw music metadata.
- `work_metrics`: engagement snapshots keyed by `aweme_id + observed_at`.
- `ingestion_runs`: requested window, pages/items, oldest/newest, has_more, completeness, stop reason and collector.
- `song_normalization`: raw music -> `SONG_FAMILY` + `AUDIO_VERSION`.

Signed CDN video/music URLs are not canonical database fields.

## 4. Completeness Gate
An account/window is `COMPLETE` only when at least one is true:
1. oldest fetched publish time is earlier than the requested window start; or
2. upstream returns a reliable terminal `has_more=false`.

`EMPTY_PAGE_WITH_HAS_MORE` = incomplete upstream pagination, not zero data.

Current known seed state before fallback repair:
- 7/9 complete;
- Aura incomplete;
- XIANGJISHI incomplete.

HG01 cannot claim full 9-account coverage until those two are closed or explicitly marked unavailable with fallback evidence.

## 5. Collector priority
1. `PUBLIC_FAST` — BugPk/dyzy for low-friction refresh;
2. `SELF_HOST` — self-deployed `jiuhunwl/short_videos` with server-side Cookie;
3. `SESSION_FALLBACK` — jiji262/browser-login session path.

Collector failure must be recorded in `ingestion_runs`; it must never silently turn into zero works.

## 6. R3 analysis contract
After database completeness is sufficient, calculate from DB only:
- `distinct_account_repeat_15d`;
- `distinct_account_repeat_7d`;
- `music_radar_weighted_repeat`;
- `visual_account_repeat`;
- `72h_concentration`;
- `raw_audio_version_consistency`;
- engagement/performance snapshots as supporting signals.

Every candidate must resolve back to exact `aweme_id` + direct Douyin work URL.

## 7. Nine-account lock for this test
R3 deliberately stays at 9 unique accounts until the first full database → normalization → analysis → HG01 loop is completed.
Do not expand the sample pool before this calibration round is closed.
