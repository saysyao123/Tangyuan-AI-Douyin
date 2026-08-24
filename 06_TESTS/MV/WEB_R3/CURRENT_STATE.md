# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / MUSIC_SHORTLIST_VALIDATION`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / A1_PASS / A2_PASS / SHORTLIST_READY / HG01_PENDING`
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

State:
`R3_A1_ACCOUNT_REGISTRY_PASS = YES`

## R3-A2｜PASS

Raw radar:
`06_TESTS/MV/WEB_R3/R3_MUSIC_RADAR_WEEK_01.csv`

Reports:
- `R3_A2_FIRST_SWEEP_REPORT_v1.md`
- `R3_A2_SECOND_SWEEP_REPORT_v1.md`

A2 proved the Radar can distinguish:
- `EARLY_RISE`
- `CONFIRMED`
- `CLASSIC_REVIVAL`
- `OVERHEATED`

and can down-rank songs with:
- saturation risk；
- format mismatch；
- AUDIO_VERSION ambiguity；
while preserving visually strong early-rise candidates.

State:
`R3_A2_7DAY_MUSIC_RADAR_PASS = YES`

## R3-A3｜SHORTLIST READY

Shortlist:
`06_TESTS/MV/WEB_R3/R3_MUSIC_SHORTLIST_v1.md`

Priority candidates:

1. `雨后轻风有香`
   - class: `EARLY_RISE`
   - strongest healing-visual fit；
   - strategic test fit #1；
   - audio-title/version ambiguity must be resolved at Stage 2.

2. `循迹`
   - class: `EARLY_RISE`
   - strongest recent 48–72h velocity；
   - high-density lyric section means excerpt selection is critical.

3. `甲乙丙丁`
   - class: `CONFIRMED`
   - strongest trend certainty / >=7 recent independent signals；
   - saturation rising.

4. `我不难过`
   - class: `CONFIRMED_CLASSIC_REVIVAL`
   - high-quality music-account revival signal；
   - darker healing direction.

5. `琵琶曲（东船与西舫）`
   - class: `CONFIRMED_VISUAL`
   - very strong visual fit but format/version risks higher.

Excluded priority example:
`第57次取消发送 = OVERHEATED / FORMAT_MISMATCH`.

## Current Gate｜HG01

User should now select only the `SONG_FAMILY` to enter R3-B0.

Recommended R3 test-value order:
1. `雨后轻风有香`
2. `循迹`
3. `甲乙丙丁`
4. `我不难过`
5. `琵琶曲（东船与西舫）`

## Not allowed until HG01 PASS

- exact AUDIO_VERSION lock；
- BGM excerpt render；
- Audio Timeline Package；
- Healing Visual B1/B2 tests；
- full R3 MV。

## Next after HG01

`R3-B0`:
1. identify exact audio version candidates；
2. obtain actual audio；
3. create full-sentence excerpt candidate；
4. run `HG02 BGM Excerpt Listening Gate`；
5. only after BGM lock build a fresh `AUDIO_TIMELINE_PACKAGE`；
6. then enter R3-B1 Static Healing Visual mini-test.
