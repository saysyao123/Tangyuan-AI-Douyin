# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-D2 / FIRST POST SCHEDULED / WAITING FOR ACTUAL PUBLISH + LIVE DATA`
- STATE: `R3_A_PASS / R3_B_CURRENT_CALIBRATION_PASS / R3_C_FULL_MV_INTEGRATION_PASS / HG05_PASS / R3_D1_PACKAGING_BENCHMARK_COMPLETE / MUSIC_FIRST_SELECTED / FIRST_POST_FINAL_PACKAGE_LOCKED / FRONT_FACING_ACCOUNT_NAME_LOCKED / D01_A_SCHEDULED / R3_D2_WAITING_FOR_ACTUAL_PUBLISH`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Program-level status

- `R3-A Music Radar / Benchmark Calibration = PASS`
- `R3-B Healing Visual Calibration = PASS FOR CURRENT CALIBRATION`
- `R3-C Full MV Integration = PASS / HG05`
- `R3-D1 Publish Packaging Benchmark = PASS / FINAL FIRST-POST PACKAGE LOCKED`
- `R3-D2 Live Data Feedback = WAITING FOR ACTUAL POST`

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

## Scheduled publication｜D01-A

Tracker slot:
`D01-A / Lane P / MUSIC_FIRST`

User scheduled publication for approximately:
`2026-08-25 17:30 Asia/Shanghai`

This is a scheduled target, not the actual publish timestamp.
After the post is actually live, replace with exact actual timestamp and begin 1h / 3h / 24h observations.

`D01_A_STATUS = SCHEDULED`
`SCHEDULED_PUBLISH_AT = 2026-08-25 17:30 Asia/Shanghai`
`ACTUAL_PUBLISH_TIMESTAMP = PENDING`

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
- `05_IP_ASSETS/PUBLISH_SYSTEM.md`
- `05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`
- `05_IP_ASSETS/MV_30D_60_TRACKER.csv`

Portfolio target:
- Lane P Primary/Trend = 30;
- Lane S Stable/Fast = 24;
- Lane R Camera/Director R&D = 6.

## Conversation / project boundary｜IMPORTANT

R3 should now remain the evidence/data thread for D01-A.

The **next MV should start in a new conversation as a new 30D/60 production instance**, not as a continuation of this song's R3 creative context.

Reason:
- prevent current-song visual residue (rain/night/veil/ice/etc.) from contaminating the next song;
- keep each MV's creative context small;
- reuse Runtime/Rules/Knowledge through GitHub instead of carrying historical chat context;
- allow R3-D2 data tracking to continue independently from next-video production.

New-conversation authority:
`05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`

## Next actions

### D01-A data lane
1. wait for actual publication;
2. record exact actual publish timestamp;
3. update tracker from `SCHEDULED` to `PUBLISHED`;
4. collect 1h / 3h / 24h metrics.

### Next-MV production lane
1. open a new chat;
2. paste `MV_30D_60_NEW_CHAT_START_PROMPT.md` contents or equivalent startup command;
3. new chat reads current production runtime + account OS;
4. start from Song Queue / batch HG01 unless the user already supplies a song;
5. do not ask the user to re-explain R1/R2/R3.
