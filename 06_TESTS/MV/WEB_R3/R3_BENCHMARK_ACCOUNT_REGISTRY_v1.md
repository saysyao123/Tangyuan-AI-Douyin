# WEB R3｜Benchmark Account Registry v1

> Status: `SEED / R3-A`
> Purpose: 建立稳定样本池，不把所有账号混成同一类。每个账号只承担最适合的 Benchmark 职能。

## 1. Seed accounts

| Account | Primary role | What to learn | What NOT to copy blindly | Weight |
|---|---|---|---|---:|
| 泡泡与茶 | 翻唱/歌曲兴趣雷达 | 最近被重新翻唱/用户愿意听的歌；温暖音乐人设 | 真人双人翻唱场景/人物关系 | 4/5 |
| 火乐乐 | 高频音推雷达 | 新歌、OST、回潮歌、标题/推荐描述 | 高信息密度真人口播外壳 | 5/5 |
| 乐丨青春 | MV剪辑/字幕/卡点 | 歌词视觉化、短标题、剪辑与旋律结合 | 具体真人/影视素材 | 5/5 |
| XIANGJISHI | 风景音推/沉浸 | 风景+音乐、低信息干扰、高停留感 | 具体城市/实拍素材 | 5/5 |
| Aura | 高审美风景音推 | 空间、光线、色调、低文字、治愈沉浸 | 具体风景素材/构图复制 | 5/5 |
| 佩佩治愈Ai | 人物型治愈AI视觉 | 画质、自然光、轻梦幻、人物治愈感、色彩 | 具体角色/具体构图/纯视觉账号运营逻辑 | 5/5 visual |
| 黑米与糖豆 | 原创/新歌包装 | 新歌发现、完整歌诉求、CTA、发布包装 | 大字营销模板直接搬到视频内部 | 3/5 |
| 爱的魔力小姐姐 | 辅助音乐/生活样本 | 偶发歌曲信号、自然治愈素材 | 账号内容过杂，不作为趋势主信号 | 1/5 |

## 2. Benchmark layers

### Layer A｜Music Discovery Radar
核心：
- 火乐乐
- 泡泡与茶
- 后续补充头部音推/音乐榜单型账号

用途：找歌，不决定视觉。

### Layer B｜Healing Visual Benchmark
核心：
- 佩佩治愈Ai：人物型
- Aura：自然型
- XIANGJISHI：风景音推型

用途：提高治愈感、画质、光色、空间与人物关系，不负责趋势判断。

### Layer C｜Edit / Lyric / Packaging Benchmark
核心：
- 乐丨青春：视频内歌词/剪辑/卡点
- 火乐乐：标题/介绍/歌曲推荐话术
- 黑米与糖豆：新歌/CTA/发布包装

用途：发布层和剪辑表达，不决定 BGM timing truth。

## 3. Required account record fields

未来新增账号必须记录：
- `account_name`
- `account_role`
- `followers_visible`
- `posting_frequency_estimate`
- `recent_7d_music_posts`
- `dominant_music_source`：新歌/OST/老歌复热/翻唱/原创/混合
- `visual_type`
- `subtitle_type`
- `cover_text_type`
- `caption_type`
- `hashtag_pattern`
- `strength`
- `copy_risk / mismatch_with_us`
- `benchmark_weight`

## 4. Song normalization rule

趋势统计必须区分：

### SONG_FAMILY
歌曲本身，例如：`偏爱`。

### AUDIO_VERSION
具体音频，例如：
- 原唱 studio
- live
- cover
- sped-up
- remix
- OST excerpt

R3-A 用 `SONG_FAMILY` 判断跨账号重复趋势；真正进入 MV Stage 2 时再锁 `AUDIO_VERSION`。

否则容易出现“大家都在推同一首歌，但实际使用的是不同录音版本”的假一致。

## 5. Packaging observation fields

每条有效样本同时记录：
- `cover/on-video hook`
- `post title`
- `description`
- `hashtags`
- `song/artist explicitness`
- `emotion hook`
- `CTA`
- `AI mentioned or not`

后续 R3-D 只从重复出现且与我们账号定位兼容的模式中提炼发布策略。

## 6. Promotion warning

Benchmark ≠ Rule。

单账号使用某种做法，不得直接写入 Runtime。
只有：
`multiple accounts / repeated evidence -> our test -> user acceptance -> data feedback`
之后才考虑晋升。
