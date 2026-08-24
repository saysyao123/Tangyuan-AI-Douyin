# WEB R3｜CURRENT_STATE

> R3 是多轮阶段性测试，不等于一次完整 MV。R2 correctness baseline 默认冻结。

## Current Status

- ROUND: `WEB_R3`
- BRANCH: `test/mv-web-r3`
- STAGE: `R3-A3 / DIRECT_DOUYIN_EVIDENCE_REPACK`
- STATE: `R3_INITIALIZED / R2_BASELINE_FROZEN / A1_PASS / A2_PASS / RADAR_SHORTLIST_EXISTS / HG01_NOT_READY / DIRECT_DOUYIN_EVIDENCE_PACK_REQUIRED`
- UPDATED_AT: `2026-08-24 Asia/Manila`

## Why A3 was reopened

用户指出首轮 HG01 交付逻辑有缺陷：
- shortlist 声称来自趋势/Benchmark 分析；
- 但用户没有拿到“对应账号 → 对应抖音作品 → 可直接点开看/听”的决策材料；
- 外部平台试听链接不能替代抖音作品证据；
- 搜不到某核心账号作品也不能推断“抖音没有这首歌”。

因此：
- A2 Radar 分类逻辑保留；
- `R3_MUSIC_SHORTLIST_v1.md` 降级为 Radar candidates；
- 原 `READY FOR HG01` 状态撤回；
- 新增 `R3_HG01_EVIDENCE_DELIVERY_CONTRACT_v1.md`；
- HG01 只有在 direct Douyin evidence pack 完成后才能重新开启。

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

## R3-A1｜PASS

Registry:
`R3_BENCHMARK_ACCOUNT_REGISTRY_v1.md`

## R3-A2｜PASS

Radar:
`R3_MUSIC_RADAR_WEEK_01.csv`

A2 proved the Radar can distinguish:
- EARLY_RISE
- CONFIRMED
- CLASSIC_REVIVAL
- OVERHEATED

and can penalize saturation / format mismatch / audio-version ambiguity.

## R3-A3｜EVIDENCE REPACK

Radar candidate priority remains:
1. 雨后轻风有香
2. 循迹
3. 甲乙丙丁
4. 我不难过
5. 琵琶曲（东船与西舫）

But this ranking is **not yet a user decision packet**.

Required before HG01:
- `DIRECT_DOUYIN_EVIDENCE_PACK_READY = YES`
- each HG01 candidate has >=2 direct recent Douyin/Douyin精选 work links from >=2 accounts；
- each link labels account / date / duration / Tier A or Tier B；
- core benchmark account coverage explicitly reported；
- missing core-account indexing marked UNKNOWN/INDEX_PENDING, never 0；
- no Weibo/other external audio link used as substitute for Douyin viewing evidence。

Contract:
`R3_HG01_EVIDENCE_DELIVERY_CONTRACT_v1.md`

## Current allowed work

Allowed:
- retrieve direct Douyin works for top candidates；
- prioritize user-seeded Benchmark accounts；
- where core accounts cannot be publicly indexed, say so and use supplemental Douyin evidence only with lower confidence；
- build a clickable HG01 decision packet。

Not allowed:
- ask user to choose before the direct evidence pack is usable；
- lock SONG_FAMILY；
- enter BGM Stage 2/B0；
- start visual R3-B1/B2；
- modify R2 correctness runtime。

## Next Gate

Finish `DIRECT DOUYIN EVIDENCE PACK`.

Then:
`HG01_READY = YES`
→ user directly views/listens to Douyin works
→ selects SONG_FAMILY
→ enter R3-B0 exact AUDIO_VERSION + BGM excerpt + HG02.
