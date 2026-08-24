# WEB R3｜Benchmark Account Registry v1

> Stage: `R3-A1 / Account Registry`
> Status: `PASS / FIRST REGISTRY LOCKED`
> Principle: 不同账号承担不同观测职能，不做等权平均。

## 1. User-seeded core registry

| Account | Primary role | Trend weight | Visual weight | Packaging weight | R3 usage |
|---|---|---:|---:|---:|---|
| 泡泡与茶 | 翻唱/复热信号 + 温暖人设音乐 | 0.90 | 0.45 | 0.70 | SONG_FAMILY 回潮、cover-version signal、轻治愈包装 |
| 火乐乐 | 高频音推 / OST / 热歌信息 | 1.00 | 0.25 | 1.00 | 主趋势雷达、标题/介绍/歌单话术 |
| 乐丨青春 | 音乐+剪辑+歌词+卡点 | 0.65 | 0.80 | 0.75 | Edit/subtitle/cover benchmark；趋势辅助 |
| XIANGJISHI | 风景音推 / 治愈空间 | 0.45 | 0.90 | 0.55 | Nature-healing visual benchmark |
| Aura | 高审美风景 / 低文字沉浸 | 0.35 | 0.95 | 0.40 | Nature-healing visual benchmark |
| 黑米与糖豆 | 新歌/原创/汽水音乐包装 | 0.70 | 0.45 | 0.80 | New-song + caption/tag benchmark |
| 佩佩治愈Ai | 人物型高质感 AI 治愈视觉 | 0.25 | 1.00 | 0.35 | Healing visual benchmark，不作为主要选歌统计源 |
| 爱的魔力小姐姐 | 混合内容辅助样本 | 0.25 | 0.30 | 0.30 | Auxiliary only |

## 2. Supplemental public music-radar accounts

这些账号来自当前可公开检索的抖音/抖音精选结果，用于增强 R3-A2 的近期歌曲信号。

| Account | Primary role | Trend weight | Notes |
|---|---|---:|---|
| 碳酸音乐 | 月度/近期热歌盘点 | 0.90 | 公开页面可检索，约20万粉、200万+获赞；持续做“最近很火的歌曲” |
| 油条Music | 大体量音乐盘点 | 0.75 | 公开页面可检索，约65万粉、2200万+获赞；偏纯音乐/盘点，需要类型降权 |
| CD传媒 | 高频动态歌词排版 | 0.75 | 近7天可见高频日更；很适合观察经典歌/流行歌近期再出现 |
| 志鹏Cello | 音乐赏析 / 热点回潮 | 0.70 | 近期作品能提供经典歌曲复热信号 |
| 马呜呜 | 音乐制作人解析 | 0.65 | 对“经典歌为什么又被讨论”有辅助价值 |
| DSD音乐〖百万调音师〗 | 高频热歌/经典歌发布 | 0.60 | 高频日更；商业/HiFi属性明显，只作重复率辅助 |

## 3. Institutional / platform corroboration

以下不计入“UP主重复率”，只作为第二层佐证：

| Source | Role | Use |
|---|---|---|
| 汽水音乐 / douyin.com qishui playlists | 平台音乐推荐与相关歌单 | `platform_signal`，确认某 SONG_FAMILY 是否在近期推荐生态重复出现 |
| 抖音公开搜索 / 抖音精选 | 作品发布时间与近期作品证据 | 作品级 provenance |
| 其他音乐榜单 | 辅助交叉验证 | 不得单独定义 Douyin trend truth |

## 4. Benchmark layers

### Layer A｜Music Discovery Radar
优先：
- 火乐乐
- 泡泡与茶
- 碳酸音乐
- CD传媒
- 志鹏Cello / 马呜呜
- DSD音乐（降权）
- 平台/汽水只作 corroboration

用途：找歌，不决定视觉。

### Layer B｜Healing Visual Benchmark
优先：
- 佩佩治愈Ai：人物型治愈视觉上限
- Aura：自然空间、低文字沉浸
- XIANGJISHI：风景音推
- 乐丨青春：歌词/画面/节奏结合

用途：R3-B 提高光感、色彩、人物/环境比例、画质和治愈感，不负责趋势判断。

### Layer C｜Edit / Lyric / Packaging Benchmark
优先：
- 乐丨青春：视频内字幕/卡点/剪辑
- 火乐乐：标题/介绍/歌曲推荐话术
- 黑米与糖豆：新歌/CTA/发布包装
- 泡泡与茶：歌名/翻唱人设/封面包装
- CD传媒：动态歌词表达

## 5. Song normalization rule｜HARD FOR R3-A

趋势统计必须区分：

### SONG_FAMILY
歌曲本身，例如：`一直很安静`。

### AUDIO_VERSION
具体音频，例如：
- 原唱 studio
- live
- cover
- sped-up
- remix
- OST excerpt
- R&B/女声/释怀版

R3-A 用 `SONG_FAMILY` 判断跨账号重复趋势；真正进入 MV Stage 2 时再锁 `AUDIO_VERSION`。

否则会出现“大家都在推同一首歌，但实际用的是不同录音版本”的假一致。

## 6. Required observation fields

每条有效样本记录：
- `observed_at`
- `account/source`
- `source_role`
- `publish_time`
- `song_family`
- `audio_version`
- `visible_performance`
- `cover/on-video hook`
- `post title`
- `description`
- `hashtags`
- `visual_type`
- `subtitle_type`
- `evidence_url/reference`
- `confidence`

## 7. Evidence policy

- 有作品级可验证证据才计入 `observed_post_count`；
- 搜不到不等于账号没发，标 `INDEX_PENDING`；
- 用户主页截图可用于账号角色/视觉/包装分类，但不能推断完整7天歌单；
- 平台歌单出现不等于某UP主发过，只记 `platform_signal`；
- A3 shortlist 必须同时报告 `evidence_coverage`，不能把未索引账号默认为0。

## 8. A1 PASS

当前 registry：
- 8 个用户种子账号；
- 6 个 supplemental public music accounts；
- 2+ platform corroboration channels；
- trend / visual / packaging 三类职责完整；
- 每类有权重和证据政策。

`R3-A1 = PASS`。

Next：`R3-A2 / 7-Day Music Radar`。
