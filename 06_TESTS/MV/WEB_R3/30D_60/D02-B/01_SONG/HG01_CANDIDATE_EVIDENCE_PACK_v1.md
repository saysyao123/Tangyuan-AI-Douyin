# 汤圆音乐映像｜D02-B HG01 Candidate Pack v1.2

Status: `SUPERSEDED_TEST_ARTIFACT / REBUILD_FROM_CORE_DATABASE`
Slot: `D02-B`
Lane: `S / Stable-Fast`
Date: `2026-08-27`
Branch: `test/mv-oss-optimization-r1`

## Why this pack is superseded

上一版把一次 HG01 链接真实性修复扩大成了新的选歌策略：为了满足公开 Web 证据完整度，候选主要从全网 Radar / 搜索结果中重新筛选。

用户已明确恢复原 R3 策略：

`核心对照账号 -> 更新/读取 Data Center -> 从数据库选歌 -> 直接交付对应博主的对应歌曲 MV -> 用户选歌`

因此上一版正式候选：
- 《雨后轻风有香》
- 《甲乙丙丁》
- 《差一步美满》

全部撤回正式 HG01 身份。它们仍可作为历史 Radar 信息保留，但不能因为“公开搜索证据比较完整”而优先进入当前 Gate。

## Restored HG01 strategy

### Candidate discovery

默认只从已锁定的核心 Benchmark / 对照账号数据库出发：

1. 更新或读取 `06_TESTS/MV/WEB_R3/database/data_center/`；
2. 找跨账号重复或明显值得做的 SONG_FAMILY；
3. 综合歌曲吸引力、近期性、音频 family 一致性、歌词视觉空间与饱和风险排序；
4. 如发现长期有价值的新账号，可作为 supplemental benchmark 纳入数据库；
5. 不执行全面歌曲搜索作为默认候选发现方式。

### User delivery

HG01 给用户的内容保持简单：
- 歌名；
- 一句“为什么从核心数据库进入候选”；
- 直接给对应博主的对应歌曲 Douyin MV 视频；
- 必要时一条简短风险提示。

用户只需要看/听这些 MV，然后判断歌本身抓不抓人。

不再要求用户阅读 Tier A/B/C、Core coverage、Evidence taxonomy 或全网搜索报告。

### Retained integrity guard

本轮测试唯一保留的加固：

`DELIVERED URL MUST BE THE CITED MV LANDING WORK`

也就是说，如果交付“火乐烁的某首歌 MV”，链接必须实际打开那条 MV；不能用作者旧作品页面里列出的“近期作品”代替。

这个规则只负责**交付链接不出错**，不参与决定哪首歌值得进入候选池。

## Current D02-B state

- HG01 selection: `NOT MADE`
- Canonical state: remains `S00_SLOT_CREATED`
- Current action: `REBUILD CANDIDATES FROM CORE BENCHMARK DATA CENTER`
- Previous web-wide candidate pack: `SUPERSEDED`

HG01_READY = NO
SOURCE_MODE = CORE_BENCHMARK_DATABASE
DELIVERY_MODE = CORE_CREATOR_MV_DIRECT
ALL_DELIVERY_LINKS_LANDING_WORK_VERIFIED = NO

Do not present an HG01 selection until the core-database candidate pack is rebuilt.
