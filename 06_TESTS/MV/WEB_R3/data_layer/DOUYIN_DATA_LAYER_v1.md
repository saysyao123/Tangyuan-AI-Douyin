# WEB R3｜Douyin Data Layer v1

Status: `R3 PRODUCTION DATA CONTRACT`
Scope: current 9 unique core Douyin accounts only.

## 1. Purpose

R3 must not choose songs from search-engine side evidence. The canonical path is:

`CORE ACCOUNT -> AUTHENTICATED LIVE COLLECTION -> WORK DATABASE -> SONG_FAMILY -> CROSS-ACCOUNT REPEAT -> DIRECT DOUYIN EVIDENCE -> HG01`

The data layer exists to make account/video/music data reproducible and auditable before any MV decision.

## 2. Collector hierarchy

### L1｜AUTH_METADATA_PRIMARY — F2 with authenticated Douyin session

Primary source for account profile + homepage work metadata.

Required capabilities:
- `sec_uid` profile verification;
- latest homepage works;
- native `max_cursor` pagination;
- raw aweme JSON;
- work/music/statistics fields;
- single-work detail revalidation;
- stop only after the requested time window is closed.

Pinned implementation for R3 bootstrap:
`Johnserf-Seed/f2@7dab3e2ffffaa2535834d28fca99dbc2e89fa9d3`

### L2｜SESSION_MEDIA_FALLBACK — jiji262/douyin-downloader

Independent fallback for:
- QR/browser Cookie bootstrap;
- homepage post browser fallback;
- single-work parsing;
- video/media download;
- download completeness validation;
- start/end time filtering;
- JSON export.

Media download is resolved on demand. Signed CDN URLs are never canonical database keys.

### L3｜PUBLIC_FAST — BugPk / short_videos

Allowed for:
- fast discovery;
- single-work convenience parsing;
- temporary media resolution;
- public-path diagnostics.

Not allowed as final evidence for:
- 15-day window completeness;
- current-edge freshness;
- denominator-complete HG01 repeat counts.

Reason: R3 regression proved public `dyzy` can return valid first-page data while deep pagination/current edge is incomplete or cached.

### GitHub Actions

GitHub-hosted runners are **regression harness only**. They are not the production Douyin collector.

R3 tests proved anonymous cloud runners can receive HTTP 200 with empty/degraded Douyin payloads even when using Chromium or F2 signing. A green CI run therefore does not prove current Douyin data coverage.

## 3. Identity contract

- account stable external key: `sec_uid`;
- internal account key: `account_id`;
- work key: `aweme_id`;
- nickname / Douyin ID are mutable attributes, not join keys;
- one shared profile link resolving to an existing `sec_uid` is a duplicate, not a new account.

## 4. Authenticated collection Gate

For every required core account and every requested window, `window_complete=1` is allowed only when all applicable checks pass:

1. **PROFILE_AUTH_PASS**  
   authenticated `fetch_user_profile(sec_uid)` returns a valid profile and the returned `sec_uid` matches the requested account.

2. **FIRST_PAGE_AUTH_PASS**  
   authenticated homepage post request completes as a valid Douyin response. Empty data caused by anti-bot/degraded response is a failure, not zero works.

3. **LATEST_OWNERSHIP_PASS**  
   if the account has at least one fetched work, re-fetch the newest `aweme_id` via single-work detail and verify `author.sec_uid == requested sec_uid`.

4. **WINDOW_CLOSURE_PASS**  
   continue native cursor pagination until either:
   - oldest successfully fetched work timestamp is **older than window_start**, or
   - a valid authenticated response explicitly returns `has_more=false`.

Only after 1–4 pass may the account be treated as denominator-complete.

### Important correction: activity age is not freshness

`latest_work_age_hours` is an account-activity metric only.

A creator may legitimately publish nothing for 3, 7 or 15 days. Therefore `latest work <=72h` is **not** a Freshness Gate and must never by itself mark collection stale.

Freshness means: **the authenticated live endpoint was successfully queried now**, not “the account posted recently.”

## 5. Failure semantics

- `SEARCH_MISS != NO_WORK`
- `PUBLIC_API_EMPTY != NO_WORK`
- `HTTP_200_EMPTY_BODY != PASS`
- `DOM_VIDEO_LINK != OWNED_WORK` unless author ownership is verified
- `HAS_MORE=true + empty page != COMPLETE`
- collector failure is `UNKNOWN/INCOMPLETE`, never zero.

## 6. Database write contract

Canonical Git-tracked tables remain in `06_TESTS/MV/WEB_R3/database/`.

### accounts.csv
Update mutable profile fields and last verification receipt. Never replace `sec_uid` identity.

### works.csv
Upsert by `aweme_id`.
Keep:
- account_id;
- create_time;
- canonical Douyin work URL;
- caption;
- work type/duration;
- raw music title/author;
- hashtags;
- first_observed_at.

Do **not** persist expiring signed video/music CDN URLs as canonical fields.

### work_metrics.csv
Append engagement snapshots by `(aweme_id, observed_at)`.

### ingestion_runs.csv
Append one run receipt per account with:
- requested window;
- pages/items;
- oldest/newest fetched;
- terminal has_more;
- profile/first-page/latest-ownership/window-closure gates;
- collector;
- error/stop reason;
- observed_at.

### song_normalization.csv
Normalization is work-level (`aweme_id`), because one creator original-sound label can represent several different songs.

## 7. Secret handling

Default local secret path:
`06_TESTS/MV/WEB_R3/.secrets/douyin_cookie.txt`

Rules:
- never commit Cookie;
- never print Cookie to terminal/logs;
- never upload raw authenticated responses containing sensitive session data to GitHub Actions artifacts;
- local raw API payloads live under `.local_raw/` and are ignored by Git;
- refresh Cookie interactively when profile/first-page auth Gate fails.

## 8. R3 local production flow

Windows entry point:
`06_TESTS/MV/WEB_R3/run_douyin_refresh.ps1`

Flow:
1. create/reuse local Python venv;
2. install pinned F2 + Playwright;
3. if Cookie is absent, open real Douyin browser and perform one QR login;
4. authenticated collection for exactly the 9 locked accounts;
5. close the R3 15-day window;
6. upsert database CSVs + ingestion receipts;
7. build/validate SQLite;
8. normalize SONG_FAMILY;
9. run trend analysis;
10. only after all required Gates pass may HG01 evidence be produced.

## 9. R3 scope lock

Do not expand beyond the current 9 unique accounts until this first authenticated database -> normalization -> analysis -> HG01 loop is complete.
