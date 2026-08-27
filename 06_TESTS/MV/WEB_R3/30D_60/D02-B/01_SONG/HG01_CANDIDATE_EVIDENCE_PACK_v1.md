# 汤圆音乐映像｜30天60条｜D02-B HG01 Candidate Evidence Pack v1

Status: `EVIDENCE_REPACK_REQUIRED / NOT READY FOR HUMAN GATE`
Slot: `D02-B`
Lane: `S`
Date: `2026-08-27`

## Scope

本文件只负责 HG01 Song Aesthetic Gate 的用户可决策证据。

当前**禁止**让用户直接按 A/B/C/D 选歌，因为机器候选预检已经完成，但 direct Douyin evidence 尚未全部满足 landing-work identity 要求。

`SONG_CANDIDATE_SET != HG01 USER DELIVERY`。

## Root-cause audit

本轮发现的错误不是候选歌趋势判断本身，而是 evidence URL 语义混淆：

- 搜索引擎可以打开一个作者的旧 Douyin 精选作品页面；
- 该页面又会列出作者最近的新作品；
- 搜索摘要因此能显示候选歌标题、发布时间、时长；
- 但页面 URL 对应的 landing work 仍然是旧作品；
- 如果把这个 URL 直接保存成 `direct_evidence.url`，用户点击后并不会直接进入被引用的候选歌作品。

这类链接从现在起定义为：
`PROFILE_LISTING_REFERENCE / DISCOVERY_ONLY / NOT_DIRECT_WORK_EVIDENCE`。

## Hard evidence identity rule

每条正式 Direct Douyin Work 必须同时满足：

1. URL 是 concrete work URL；
2. URL 中 work/video id 与 landing work id 一致；
3. landing work 主标题/音频身份本身能够支持对应 SONG_FAMILY；
4. account / publish date / duration 从该 landing work 或同一 concrete work 的可靠元数据得到；
5. 不依赖页面中的“作者近期作品列表”来证明另一条作品；
6. evidence location 必须是 `LANDING_WORK`，不得是 `PROFILE_LISTING`；
7. 每首至少 2 条，且来自至少 2 个独立账号。

## Current candidate audit

### A｜循迹

Trend signal: `EARLY_RISE_ACCELERATING`
Current evidence status: `REPACK_REQUIRED`

已确认存在的新近作品信号包括：
- 李佳薇：`《循迹》15秒唱完70个字，大家也来一起挑战吧！`，搜索摘要显示 00:36；
- 王铮亮：`《循迹》cut 调整好呼吸节奏，一起来听这首《循迹》～`，搜索摘要显示 00:34；
- 匡泓霖 琵琶：`琵琶高燃版《循迹》`，搜索摘要显示 00:50；
- 嗨椰教育-椰子老师：近期解析《循迹》。

但此前保存的部分 URL 对应的是作者旧 landing work，只在页面列表中显示上述新作品，因此不能作为正式 HG01 direct-work 链接。

结论：`NOT READY`。

### B｜雨后轻风有香

Trend signal: `EARLY_RISE_STRATEGIC_VISUAL_FIT`
Current evidence status: `PARTIAL / REVERIFY ALL BEFORE GATE`

当前至少有 concrete landing-work 证据：
- wuhu动画人空间：`《牛来》片尾曲《雨后轻风有香》你听了吗？`，2026-08-18；
- 立德读书：`电影《牛来》片尾曲《雨后轻风有香》歌词解析`，2026-08-19；
- 魔都炒家：`牛来 雨后清风有香，很好听！`，2026-08-17 13:27。

在正式交付前仍需把每条 duration / evidence tier / core-account coverage 完整持久化并复核链接目标。

结论：`NOT READY`。

### C｜甲乙丙丁

Trend signal: `CONFIRMED_TREND`
Current evidence status: `PARTIAL / REPACK_REQUIRED`

已确认 concrete landing-work：
- 浙江卫视：`张碧晨 侯明昊合唱《甲乙丙丁》`，2026-08-21，00:40。

但此前保存的付飞翔、嗨椰教育链接属于旧 landing work 页面，其摘要列出了新的《甲乙丙丁》解析内容，不满足 direct-work identity。

结论：`NOT READY`。

### D｜我不难过

Trend signal: `CLASSIC_REVIVAL`
Current evidence status: `REVERIFY_REQUIRED`

公开索引能确认近期多账号 revival 信号，但当前 D02-B 还没有完成两条 concrete landing-work 的统一 date / duration / tier / core-coverage 持久化。

结论：`NOT READY`。

## HG01 readiness assertions

- `all_candidates_min_direct_works_2 = false`
- `all_candidates_independent_accounts_2plus = false`
- `all_direct_links_landing_work_verified = false`
- `core_account_coverage_reported = false`
- `no_external_audio_substitution = true`
- `user_gate_delivery_mode = DIRECT_WORKS_FIRST`

Therefore:

`HG01_EVIDENCE_DELIVERY_PASS = NO`

## Required next action

继续检索并解析每首候选的 concrete direct-work URL；不够证据的候选直接降级到 `RADAR_WATCH`，不要为了凑 4 首歌放松 Gate。

只有 Evidence Pack 最终达到：

- 3–5 个正式候选；
- 每首 >=2 direct works；
- >=2 independent accounts；
- account/date/duration/tier 完整；
- landing-work identity 全部 PASS；
- core-account coverage 已报告；

才允许把 `SONG_CANDIDATE_SET.status` 升级为 `HG01_EVIDENCE_DELIVERY_PASS`，然后向用户提交真正的 HG01。
