# 汤圆音乐映像｜D02-B HG01 Core Database Candidate Pack v1.3

Status: `HG01_EVIDENCE_DELIVERY_PASS / USER_SELECTION_REQUIRED`
Slot: `D02-B`
Lane: `S / Stable-Fast`
Date: `2026-08-27`
Branch: `test/mv-oss-optimization-r1`

## HG01 path

本轮恢复 R3 原始简单策略：

`核心 Benchmark 账号 -> Data Center -> SONG_FAMILY 重复/价值排序 -> 直接交付对应博主 MV -> 用户选歌`

默认不进行全网歌曲扫描。

当前数据库仍处于既定 15 天刷新周期内；本次候选直接来自：
- `database/data_center/song_repeat_candidates.csv`
- `database/data_center/direct_douyin_evidence.json`

D02-A 已使用《如果风会替我说话》，本轮 D02-B 排除该 SONG_FAMILY。

---

## A｜有几次想你了

为什么进入候选：核心账号 **火乐烁 + XIANGJISHI** 在同一时间窗口重复使用，数据库记录为同一林叙原声 family；Hook 清楚，短情绪 MV 适配度高。

对应核心博主 MV：
- 火乐烁｜https://www.douyin.com/video/7674212223707078833
- 𝑿𝑰𝑨𝑵𝑮𝑱𝑰𝑺𝑯𝑰｜https://www.douyin.com/video/7674136937083676665

简短提醒：情绪偏想念/克制，和已有 emo 视觉赛道存在一定同质化风险。

---

## B｜若爱有尽头

为什么进入候选：核心账号 **XIANGJISHI + 乐 ♩青春** 重复使用，而且两个都是当前数据库中的视觉型对照账号；歌词 Hook 本身有很强的画面空间。

对应核心博主 MV：
- 𝑿𝑰𝑨𝑵𝑮𝑱𝑰𝑺𝑯𝑰｜https://www.douyin.com/video/7673820758652768945
- 乐 ♩青春｜https://www.douyin.com/video/7672790854586937178

简短提醒：容易落入星空、海、遗憾这类常见抒情语法，后续导演需要明显差异化。

---

## C｜我救自己于人间水火

为什么进入候选：核心账号 **Aura + XIANGJISHI** 同时使用，两个都属于视觉表达较强的 Benchmark；“自救 / 苦难 / 重新站起来”的歌词语义和我们当前治愈视觉方向高度匹配。

对应核心博主 MV：
- Aura｜https://www.douyin.com/video/7673460363010018611
- 𝑿𝑰𝑨𝑵𝑮𝑱𝑰𝑺𝑯𝑰｜https://www.douyin.com/video/7673442358406957285

简短提醒：两个账号观察到的原声音频 family 不完全一致；如果你选这首，HG02 前需要重新锁 exact Douyin version。

---

## D｜Summer Love 爱在盛夏

为什么进入候选：核心账号 **Aura + XIANGJISHI** 重复使用，并观察到同一三棱镜原声 family；夏日、海、自由、心动这些意象对 Stable/Fast MV 非常友好。

对应核心博主 MV：
- Aura｜https://www.douyin.com/video/7673385877871136042
- 𝑿𝑰𝑨𝑵𝑮𝑱𝑰𝑺𝑯𝑰｜https://www.douyin.com/video/7673068083896814202

简短提醒：现在已到 8 月底，季节窗口正在缩短。

---

## 你在 HG01 只判断一件事

直接打开上面的 MV，看/听哪首歌本身最抓你。

现在不需要判断：
- exact BGM 版本；
- 具体截哪 15–30 秒；
- 导演方案；
- OSS 优化怎么拍。

你选定 SONG_FAMILY 后，再进入 HG02 exact audio / BGM listening。

---

## Machine-only link integrity

本轮没有重新进行 Web-wide Evidence Search。

交付链接直接来自 Core Data Center 的 observed work 记录；机器核对：
- `work_url` 中 aweme id = 数据库 `aweme_id`；
- 数据库 caption 明确支持对应 SONG_FAMILY；
- 每个候选均来自已锁定核心 Benchmark 账号。

该校验只防止发错链接，不参与歌曲排序。

HG01_EVIDENCE_DELIVERY_PASS = YES
DIRECT_DOUYIN_EVIDENCE_PACK_READY = YES
CORE_ACCOUNT_COVERAGE_REPORTED = YES
ALL_DIRECT_LINKS_LANDING_WORK_VERIFIED = YES
NO_EXTERNAL_AUDIO_LINK_SUBSTITUTION = YES
USER_GATE_DELIVERY_MODE = DIRECT_WORKS_FIRST
DELIVERY_STRATEGY = CORE_CREATOR_MV_DIRECT
SOURCE_MODE = CORE_BENCHMARK_DATABASE
EVIDENCE_LOCATION = LANDING_WORK
