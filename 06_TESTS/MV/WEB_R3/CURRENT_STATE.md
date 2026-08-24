# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A2 / 7-DAY_MUSIC_RADAR`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / A1_ACCOUNT_REGISTRY_PASS / A2_FIRST_SWEEP_COMPLETE / A2_EXPANSION_PENDING`
- CREATED_AT: `2026-08-24 Asia/Manila`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## R2 frozen baseline

Do not retest unless regression evidence appears:
- `AUDIO_TIMELINE_PACKAGE` after BGM lock；
- strong-evidence lyric timing；
- 1–3 shot raw source logic；
- W07 source QA；
- W07.5 Atom/Arc normalization；
- long-cut-first Picture Edit；
- visible-shot Fragmentation Gate；
- R1/WEB R2 locked subtitle baseline；
- 5 fixed Human Gates；
- Patch, Don't Cascade。

Authority:
- `04_HARNESS/workflows/mv.md`
- `04_HARNESS/rules/mv_golden_runtime.md`
- `04_HARNESS/rules/mv_audio_timeline.md`
- `04_HARNESS/rules/mv_human_gates.md`

## R3 staged program

1. `R3-A Music Radar / Benchmark Calibration`
2. `R3-B Healing Visual Calibration`
3. `R3-C Full MV Integration Test`
4. `R3-D Publish Packaging Calibration`

Master:
`06_TESTS/MV/WEB_R3/R3_MASTER_PLAN.md`

Micro-round matrix:
`06_TESTS/MV/WEB_R3/R3_TEST_MATRIX_v1.md`

## R3-A1｜PASS

Registry:
`06_TESTS/MV/WEB_R3/R3_BENCHMARK_ACCOUNT_REGISTRY_v1.md`

Current registry includes:
- 8 user-seeded benchmark accounts；
- 6 supplemental public music-radar accounts；
- platform corroboration channels；
- separate trend / visual / packaging weights。

State:
`R3_A1_ACCOUNT_REGISTRY_PASS = YES`

## R3-A2｜FIRST SWEEP COMPLETE / NOT YET PASS

Raw radar:
`06_TESTS/MV/WEB_R3/R3_MUSIC_RADAR_WEEK_01.csv`

First-sweep report:
`06_TESTS/MV/WEB_R3/R3_A2_FIRST_SWEEP_REPORT_v1.md`

Current strongest observed SONG_FAMILY signals:

1. `第57次取消发送`
   - >=6 independent creator signals in roughly 2–6d；
   - saturation / dance-format mismatch risk HIGH；
   - strong trend signal but not automatically suitable for our MV.

2. `甲乙丙丁`
   - >=3 independent creator signals concentrated around <1d；
   - platform corroboration present；
   - visual fit ~8/10；
   - current strong active-push candidate.

3. `我不难过`
   - >=3 independent music-account signals around <1d；
   - strong classic-revival signal；
   - visual fit ~8/10.

4. `雨后轻风有香`
   - >=2 creator signals + platform/search corroboration in 1–5d；
   - visual fit ~10/10；
   - low-medium saturation；
   - important early-rise healing candidate.

5. `开始懂了`
   - >=2 creator signals in 1–5d；
   - medium revival signal；
   - visual fit ~8/10.

Platform-watch only for now:
- `我怀念的`
- `一直很安静`
- `情歌`

## A2 evidence policy

- 搜不到某用户核心账号的近7天作品 != 该账号没发；标 `INDEX_PENDING`；
- platform playlist appearance != independent creator post；
- SONG_FAMILY 用于趋势聚合，AUDIO_VERSION 进入 MV Stage 2 才锁；
- A3 shortlist 必须报告 evidence coverage；
- repetition alone cannot win：必须扣除 saturation / format mismatch / audio-version ambiguity。

## Current allowed work｜A2 ONLY

Allowed:
- expand public recent music-push/revival creator evidence；
- track current top SONG_FAMILY signals；
- attempt to fill recent posts from user-seeded core accounts；
- normalize AUDIO_VERSION variants；
- compute weighted repeat / 72h velocity / visual fit / saturation；
- observe title / caption / tag / cover patterns associated with top songs。

Not allowed yet:
- HG01 song lock；
- BGM clip lock；
- R3-B first-frame tests；
- full R3 MV；
- changing R2 correctness runtime。

## Next Gate

Finish A2 expansion and produce weighted candidate table.

Then create:
`R3_MUSIC_SHORTLIST_v1.md`

Only after that run:
`HG01 Song Aesthetic Gate`.
