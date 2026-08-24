# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A / MUSIC_RADAR_BENCHMARK_CALIBRATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / BENCHMARK_SEEDS_DEFINED / MUSIC_RADAR_PENDING`
- CREATED_AT: `2026-08-24 Asia/Manila`

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

## Current allowed work｜R3-A ONLY

Allowed:
- establish benchmark account registry；
- add more head music-push accounts；
- inspect recent 7-day posts；
- normalize song family / audio version；
- calculate cross-account repeat / recency / velocity / saturation；
- analyze title / caption / tag / cover packaging；
- produce shortlist for HG01。

Not allowed yet:
- lock R3 song before shortlist；
- generate R3 first frames；
- change R2 subtitle/edit/timeline rules；
- run R3-B visual experiments；
- build full R3 MV；
- promote benchmark observations to hard runtime rules。

## Seed benchmark accounts from user

Core music/trend:
- 泡泡与茶
- 火乐乐

Visual / music integration:
- 乐丨青春
- XIANGJISHI
- Aura

Healing AI visual target:
- 佩佩治愈Ai

Original/new-song packaging:
- 黑米与糖豆

Auxiliary:
- 爱的魔力小姐姐

## Next Gate

Deliver:
- `R3_BENCHMARK_ACCOUNT_REGISTRY_v1.md`
- `R3_MUSIC_RADAR_WEEK_01.csv`
- `R3_MUSIC_SHORTLIST_v1.md`

Then run:
`HG01 Song Aesthetic Gate`

Only after HG01 PASS + actual BGM excerpt HG02 may R3-B begin.
