# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / CORE_ACCOUNT_15D_PATH_VALIDATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / A1_PASS / A2_RADAR_METHOD_PASS / OLD_SHORTLIST_DOWNGRADED / CORE_ACCOUNT_IDENTITIES_LOCKED / CORE_PROFILE_URLS_REQUIRED / CORE_15D_WORK_ENUMERATION_BLOCKED / HG01_NOT_READY`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Why A3 was corrected again

用户明确收紧 R3 选歌验证逻辑：

> 最终验证必须优先落在用户亲自提供的核心账号中。先检查这些核心账号近15天作品，直接比较重复歌曲，并把对应核心账号的具体抖音视频交付给用户确认；外围音推账号只作补充。

因此旧逻辑：
`public trend radar -> candidate -> later try core evidence`
被替换为：
`user core accounts -> 15d works -> direct work links -> song repeat -> candidate -> supplemental evidence`。

Authority for current R3-A:
`R3_CORE_ACCOUNT_15D_PROTOCOL_v1.md`

## User-seeded core accounts｜IDENTITY LOCKED

| Account | Douyin ID from screenshot | R3 role |
|---|---|---|
| 泡泡与茶 | `paopaoandtea` | music/cover/revival core |
| 火乐乐 | `HaoShuo2` | music-push/OST core |
| 乐丨青春 | `87136360039` | music+MV/edit core |
| XIANGJISHI | `153552032` | scenery music-push core |
| Aura | `Auraaa0131` | scenery/music immersion core |
| 黑米与糖豆 | `48003855484` | new-song/original/packaging core |
| 佩佩治愈Ai | `25927051780` | visual core; music auxiliary |
| 爱的魔力小姐姐 | `326111404` | mixed auxiliary core |

`CORE_ACCOUNT_IDENTITIES_LOCKED = YES`

## Required 15-day window

- start: `2026-08-10`
- end: `2026-08-24`

Target deliverable per core account:
- exact recent works；
- direct Douyin/Douyin精选 work URL；
- publish date/time；
- caption/title；
- displayed song/audio；
- normalized SONG_FAMILY；
- AUDIO_VERSION when known；
- visible performance / visual format / packaging observations。

## Current retrieval limitation｜BLOCKED, NOT GUESSED

User provided profile screenshots, which are sufficient to identify nickname + Douyin ID, but screenshots do not contain canonical profile/share URLs (`/user/<sec_uid>`).

Current public web indexing does not reliably surface these exact accounts by Douyin ID/name, so it cannot truthfully enumerate the full recent 15-day work list from screenshots alone.

Correct state:
- `CORE_PROFILE_URLS_READY = NO`
- `CORE_15D_WORK_ENUMERATION = BLOCKED`
- `PUBLIC_INDEX_MISSING != NO_POSTS`

Minimal unblock input:
user provides each core account's **Share profile / Copy link** once. User does **not** need to manually send individual videos.

After profile links are supplied, target execution is:
1. open/resolve each exact core profile；
2. enumerate works from 2026-08-10 to 2026-08-24；
3. collect direct work links；
4. normalize SONG_FAMILY；
5. compute core cross-account repeats；
6. build clickable Core Douyin Evidence Pack；
7. only then set `HG01_READY = YES`。

## Old A2/A3 artifacts

Previous external/public radar remains useful as supplemental research only:
- `R3_MUSIC_RADAR_WEEK_01.csv`
- `R3_A2_FIRST_SWEEP_REPORT_v1.md`
- `R3_A2_SECOND_SWEEP_REPORT_v1.md`
- `R3_MUSIC_SHORTLIST_v1.md`

They must **not** be used as the primary HG01 decision packet until the core-account path is complete.

## Not allowed now

- no HG01 song choice from old shortlist；
- no BGM lock；
- no R3-B visual work；
- no further expansion of peripheral trend accounts as the main task；
- no assumption that missing public index means a core account did not use a song。

## Next Gate

Unblock `CORE_PROFILE_URLS_READY`.

Then execute the 15-day core-account comparison and return only direct core-account Douyin evidence to user first.
