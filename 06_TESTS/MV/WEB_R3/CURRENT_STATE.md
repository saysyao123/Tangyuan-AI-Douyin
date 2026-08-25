# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-D2 / FIRST POST PUBLISHED / LIVE DATA COLLECTION ACTIVE`
- STATE: `R3_A_PASS / R3_B_CURRENT_CALIBRATION_PASS / R3_C_FULL_MV_INTEGRATION_PASS / HG05_PASS / R3_D1_PACKAGING_BENCHMARK_COMPLETE / MUSIC_FIRST_SELECTED / FIRST_POST_FINAL_PACKAGE_LOCKED / FRONT_FACING_ACCOUNT_NAME_LOCKED / D01_A_PUBLISHED / R3_D2_DATA_ACTIVE`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Program-level status

- `R3-A Music Radar / Benchmark Calibration = PASS`
- `R3-B Healing Visual Calibration = PASS FOR CURRENT CALIBRATION`
- `R3-C Full MV Integration = PASS / HG05`
- `R3-D1 Publish Packaging Benchmark = PASS / FINAL FIRST-POST PACKAGE LOCKED`
- `R3-D2 Live Data Feedback = ACTIVE`

`R3_PROGRAM_COMPLETE = NO`

## Accepted production asset

Song family:
`如果风会替我说话`

Final accepted MV:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

Upstream remains locked and must not be reopened during D-series data observation.

## R3-D1 final publish authority

Final first-post plan:
`R3_D1_FIRST_POST_FINAL_PUBLISH_PLAN_v1.md`

Front-facing account:
`汤圆音乐映像`

Locked caption:
`如果风会替我说话。`
`有些没说出口的话，就让风替我说吧。`
`风替她开口，雨替她回答，天亮以后，就继续往前走。`

Locked hashtags:
`#如果风会替我说话 #如果风会替我说话林叙 #音乐推荐 #氛围感 #治愈系`

Locked pinned comment:
`如果风真的能替你说一句话，你最想让它替你说什么？`

Exact audio asset id:
`7670880580757867270`

## Publication｜D01-A

Tracker slot:
`D01-A / Lane P / MUSIC_FIRST`

User has confirmed the post is live.

Exact actual publish timestamp:
`timestamp_pending_backfill`

Early observation reported by user:
`approximately 2 views`.

Important: elapsed time for that observation was not normalized to a confirmed 1h / 3h checkpoint, so it is stored only as an early observation and must not be written as `views_1h` or `views_3h` without timing evidence.

`D01_A_STATUS = PUBLISHED`
`LIVE_DATA_COLLECTION = ACTIVE`

Do not reopen the production chain because of this single low-view observation.

## Account operating shift｜LOCKED

Display name:
**`汤圆音乐映像`**

Bio:
`每天2条音乐MV｜热歌 × 电影感画面`
`把喜欢的歌词，做成能看见的故事`
`30天60条`

Front-facing brand rule:
- ordinary MV identity does not foreground AI;
- music + lyrics + cinematic emotion are the audience-facing promise;
- AI remains backstage production/R&D infrastructure.

Current account operating authority:
- `05_IP_ASSETS/ACCOUNT_POSITIONING.md`
- `05_IP_ASSETS/PUBLISH_SYSTEM.md` v3.1+
- `05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`
- `05_IP_ASSETS/MV_30D_60_TRACKER.csv`

Portfolio target:
- Lane P Primary/Trend = 30;
- Lane S Stable/Fast = 24;
- Lane R Camera/Director R&D = 6.

## Production Runtime hardening after D01-B

The active production workflow is now `04_HARNESS/workflows/mv.md` v1.9+.

Promoted hardening includes:
- machine Stage Entry Checklist;
- first-frame beauty + differentiation QA;
- accepted actual first frame / K0 outranks older prose;
- full dynamic prompt control skeleton promoted into `rules/ai_video.md`;
- WEB rough-cut gate enforced before formal HG04;
- account-level cover/caption component contract;
- `POST_PUBLISH_SYNC` for durable state consistency.

Audit:
`06_TESTS/MV/WEB_R3/30D_60/MV_PIPELINE_STABILITY_AUDIT_2026-08-25.md`

## Conversation / project boundary｜IMPORTANT

R3 remains the evidence/data thread for D01-A.

New MV production should use a new independent 30D/60 slot/context and must not automatically inherit a previous song's concrete visual world.

Reason:
- prevent current-song visual residue from contaminating the next song;
- keep each MV's creative context small;
- reuse Runtime/Rules/Knowledge through GitHub instead of carrying historical chat context;
- allow live-data tracking to continue independently from next-video production.

New-conversation authority:
`05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`

## Next actions

### D01-A data lane
1. backfill exact actual publish timestamp when available;
2. collect normalized +1h / +3h / +24h metrics when timing is known;
3. record views / likes / comments / favorites / shares / follows / completion / avg watch where visible;
4. do not promote a packaging/content rule from one post.

### 30D/60 production lane
1. continue with the same v1.9 single path, not a new workflow;
2. use the hardened first-frame / dynamic / stage-entry rules;
3. keep MUSIC_FIRST packaging family stable through the initial baseline block;
4. separate production correctness from distribution performance.
