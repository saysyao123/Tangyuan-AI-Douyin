# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-D1 REAL PACKAGE LOCKED / R3-D2 WAITING FOR ACTUAL PUBLISH`
- STATE: `R3_A_PASS / R3_B_CURRENT_CALIBRATION_PASS / R3_C_FULL_MV_INTEGRATION_PASS / HG05_PASS / R3_D1_PACKAGING_BENCHMARK_COMPLETE / MUSIC_FIRST_SELECTED / REAL_PUBLISH_PACKAGE_LOCKED / FRONT_FACING_ACCOUNT_NAME_LOCKED / R3_D2_WAITING_FOR_PUBLISH_TIMESTAMP`
- UPDATED_AT: `2026-08-25 Asia/Shanghai`

## Program-level status

- `R3-A Music Radar / Benchmark Calibration = PASS`
- `R3-B Healing Visual Calibration = PASS FOR CURRENT CALIBRATION`
- `R3-C Full MV Integration = PASS / HG05`
- `R3-D1 Publish Packaging Benchmark = PASS / REAL PACKAGE SELECTED`
- `R3-D2 Live Data Feedback = WAITING FOR ACTUAL POST`

`R3_PROGRAM_COMPLETE = NO`

## Accepted production asset

Song family:
`如果风会替我说话`

Final accepted MV:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`

Upstream remains locked:
- BGM / exact Douyin version;
- Audio Timeline Package;
- HG03 first-frame set;
- Dynamic / material pool;
- WEB Source Rough-Cut Gate;
- HG04 Picture Edit;
- subtitle implementation;
- Final Tech QA;
- HG05 final acceptance.

Do not reopen production variables during R3-D data testing.

## R3-D1 selection

Benchmark artifact:
`R3_D1_PUBLISH_PACKAGING_BENCHMARK_v1.md`

Selection receipt:
`R3_D1_REAL_PUBLISH_SELECTION_RECEIPT_v1.md`

Human selected:
`MUSIC_FIRST`

Locked title:
`如果风会替我说话｜有些话没说出口，就让风替我说吧`

Locked description:
`有些牵挂，不一定真的要说出口。`

`这次把《如果风会替我说话》做成了一段雨夜到天亮的治愈画面：风替她开口，雨替她回答，最后把没有说完的话留在天亮以后。`

`戴耳机听，会更完整。`

Locked hashtags:
`#如果风会替我说话 #音乐推荐 #治愈系 #氛围感 #音乐MV`

Locked pinned comment:
`这段里你最喜欢哪一句？我最想留下的是最后那句。`

Preferred cover:
S01 eye / veil / wind close-up.

`R3_D1_REAL_PUBLISH_PACKAGE_LOCKED = YES`
`ACTUAL_PUBLISH_TIMESTAMP = PENDING`

The alternate `EMOTION_FIRST` must not be duplicate-posted with the same MV.

## Account operating shift｜LOCKED

User confirmed the new Douyin front-facing display name:

**`汤圆音乐映像`**

Locked public bio:
`每天2条音乐MV｜热歌 × 电影感画面`
`把喜欢的歌词，做成能看见的故事`
`30天60条`

Front-facing brand rule:
- ordinary Douyin account/publication identity does not foreground `AI`;
- no `AI` in account name or bio;
- no default `AI生成 / AI视觉 / AIGC` in ordinary MV cover/title/tags;
- viewer-facing promise = music + lyrics + cinematic emotion;
- AI remains fully available as backstage production / R&D infrastructure;
- explicit behind-the-scenes / workflow posts are the exception and may mention AI because technology is then the content subject.

Current account operating authority:
- `05_IP_ASSETS/ACCOUNT_POSITIONING.md`
- `05_IP_ASSETS/PUBLISH_SYSTEM.md`
- `05_IP_ASSETS/MV_30D_60_OPERATING_SYSTEM.md`
- `05_IP_ASSETS/MV_30D_60_TRACKER.csv`

Portfolio target:
- Lane P Primary/Trend = 30;
- Lane S Stable/Fast = 24;
- Lane R Camera/Director R&D = 6.

The previous `汤圆AI实战 / 37→1000` phase remains historical evidence, not the current front-facing promise.

## Scale discipline

Do not reproduce full R3 R&D intensity on every one of the ~60 posts.

Preserve correctness but batch human review:
- batch HG01 song review;
- batch HG02 BGM listening;
- batch HG03 first-frame sets;
- batch HG04 clean Picture Edits;
- small-batch HG05 final candidates.

Dynamic production defaults should favor stable, physically believable motion. Camera-language experiments are isolated into Lane R instead of being mixed into every normal production source.

## R3-D2 metric contract

After actual publication, record exact publish timestamp and metrics at:
- 1h;
- 3h;
- 24h.

When visible:
- views;
- likes;
- comments;
- favorites;
- shares;
- profile visits;
- new follows;
- followers before/after;
- completion rate;
- average watch time.

Primary normalized metric:
`follows_per_1000_views = new_follows / views * 1000`.

Single-post evidence remains `EXPERIMENT`, not `PERFORMANCE_VALIDATED`.

## Next action

1. user manually updates Douyin display name to `汤圆音乐映像` and applies the locked bio;
2. publish the locked MUSIC_FIRST package once;
3. record exact actual publish timestamp;
4. enter R3-D2 1h / 3h / 24h review;
5. in parallel, begin filling the 30D/60 song queue and batch HG01/HG02 for the next production set.
