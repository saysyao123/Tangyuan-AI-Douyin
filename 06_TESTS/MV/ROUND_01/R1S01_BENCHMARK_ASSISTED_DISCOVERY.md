# R1S01｜Benchmark-assisted BGM Discovery Test

> 状态：EVIDENCE_ONLY / NOT_LOCKABLE
> 日期：2026-08-21
> 目的：验证 Rolling MV Benchmark 是否能改善 S01 的 BGM 候选发现质量。

## 1. 测试方法

不再只从泛热榜找歌，而是先观察 Benchmark Pool 中当前仍活跃的 MV 作者近期作品，再去普通抖音内容与外部音乐热度信号中验证是否存在更广泛采用。

本轮主要观察：
- `AI MV导演曹斌Johnny` 最近 7 天作品；
- 普通舞蹈 / 翻唱 / 生活 / 音乐账号近期使用；
- 可公开验证的音乐榜/搜索热度作辅助。

当前仍未拿到：
- exact Douyin music_id；
- 当前账号是否可用；
- 音频级精确 7 日使用量。

因此本文件只用于验证“Benchmark 是否能改善发现”，不能成为最终 BGM LOCK。

---

## 2. LEAD 01｜《你有没有真的爱过我》｜阿图表妹方向

### MV Vertical Adoption
- AI MV导演曹斌Johnny 最近约 11 小时内仍在发布该歌曲相关 `MV纯享版 / 卡拉OK学唱版`。
- 说明该歌至少已经进入当前 MV 制作者的近期选歌池。

### Broader Douyin Adoption
公开索引可见：
- 约 21 小时前仍有舞蹈账号发布该歌曲 9 秒内容；
- 约 2–4 天内多个舞蹈/音乐/生活账号仍出现该歌曲；
- 有普通创作者直接描述为“最近大热的歌曲，跟风一下”。

### External Heat Support
公开音乐榜/搜索榜辅助信号中，该歌曲仍位于多个当前华语热歌/会员畅听/搜索高位。

### Visual Fit
HIGH：
- 情绪明确；
- 关系冲突清楚；
- 容易形成“问而无答 / 空位 / 错过 / 记忆 / 距离”类视觉事件；
- 与当前新东方电影感体系兼容。

### Risk
- 当前可能存在多个翻唱/剪辑/平台音频版本；
- 必须锁具体 Douyin music entity，不能只写歌曲名。

### Current Status
`LEAD / WAITING_EXACT_ENTITY`

---

## 3. LEAD 02｜《山风山风等等我》｜万海东方向

### MV Vertical Adoption
- AI MV导演曹斌Johnny 最近约 2–3 天内发布过该歌曲 MV 卡拉OK版本。

### Broader Douyin Adoption
公开索引中近期可以看到：
- 舞蹈账号近 2–3 天继续使用；
- 翻唱账号近 2–4 天继续使用；
- 洛天依 cover 相关内容近 1–2 天仍出现；
- 生活类视频继续使用核心歌词片段。

这是目前本轮最明显的“跨内容类型扩散”之一。

### Exact Public Short Reference Found
已找到一个公开 11 秒抖音精选样本，标题直接使用核心歌词：
`我想要个潇洒的以后，山风山风等等我带我去山那头…`

这证明“给用户短片段而不是整首歌”的产品形态可以先用**公开短视频样本**实现，不必把完整版权音频重新托管。

### External Heat Support
- 当前多个音乐榜/搜索榜仍把该歌列在高位；
- 公开报道/社交索引也出现该歌走红信号。

### Visual Fit
VERY HIGH：
- 山风、山那头、潇洒、远方、行走本身就是强视觉词；
- 可做环境主导，不必依赖双人关系；
- 很适合新东方、山谷、长风、衣摆、纸灯/丝带/道路等视觉语法。

### Risk
- 翻唱 / 0.9倍速 / DJ / cover 很多；
- 当前“热的是哪一个具体音频实体”仍未解决。

### Current Status
`STRONG_LEAD / WAITING_EXACT_ENTITY`

---

## 4. WATCH 03｜《回到小村落》｜宋盐球方向

### MV Vertical Adoption
- Johnny 最近约 18 小时内发布相关 MV 卡拉OK版本。

### Broader Douyin Adoption
- 另一普通创作者最近约 12 小时内发布《回到小村落》完整版相关内容。

### External Heat Support
- 公开音乐榜中出现当前飙升/热门高位信号。

### Visual Fit
HIGH：
- 村落、蛐蛐、乡间、回去、归属感都有直接视觉空间；
- 但容易做成普通田园治愈片，需要更强导演概念。

### Current Status
`WATCH_HIGH / NEED_MORE_DOUYIN_SAMPLES`

---

## 5. WATCH 04｜《像我这样爱你的人》

### MV Vertical Adoption
- Johnny 最近约 3 天内发布相关 MV 卡拉OK版本。

### Creator-side Launch Signal
- 原唱/音乐人相关账号最近数小时内连续发布“新歌上线 / 新歌来了”。

### Interpretation
这更像“新歌正在被作者/合作方强推”的早期信号，尚不能证明已经形成广泛抖音采用。

### Visual Fit
HIGH：情绪空间足够，但需要等平台扩散证据。

### Current Status
`WATCH_EARLY / NOT_ENOUGH_ORGANIC_ADOPTION`

---

## 6. DEPRIORITIZED｜《起势》

Johnny 近期多次发布该歌曲完整 MV / 卡拉OK / 首发内容，但当前公开证据主要集中在同一创作体系内部。

这说明：
- 它适合研究“一首歌如何被产品化”；
- 但暂时不适合作为 R1“蹭当前平台热度”的首选候选。

状态：`PRODUCT_REFERENCE_ONLY`

---

## 7. 第一轮 Benchmark Layer 验证结论

### PASS｜Benchmark 能改善候选发现
与第一版纯热榜候选相比，当前方法可以同时回答：
- 哪些歌最近 MV 作者真的在做；
- 哪些歌在普通抖音内容中仍继续扩散；
- 哪些只是作者自己在推；
- 哪些歌曲视觉空间明显更适合当前 Golden 体系。

因此 `MV_VERTICAL_ADOPTION` 值得保留为 S01 的第二层信号。

### FAIL / Missing｜Benchmark 不能解决 Exact Entity
它仍然无法独立回答：
- 当前具体 music_id；
- 原版 / Remix / 翻唱究竟哪个音频在爆；
- 当前账号能否使用；
- 是否会在发布时被静音。

因此 `BGM_DATASOURCE_READY` Gate 仍然必须保留。

---

## 8. 当前临时优先顺序｜不是最终 5 首

1. `山风山风等等我` — STRONG_LEAD
2. `你有没有真的爱过我` — LEAD
3. `回到小村落` — WATCH_HIGH
4. `像我这样爱你的人` — WATCH_EARLY

不生成第五首只是为了凑数。等 Exact Entity / 平台信号补齐后，再生成正式 4+1 候选。

---

## 9. 对 S01 的进一步产品化建议

正式候选卡以后应同时展示：
- exact title / author / version；
- Douyin music_id；
- platform heat evidence；
- recent same-BGM samples；
- MV vertical adoption；
- 10–30 秒**官方/公开短视频试听参考**；
- visual fit；
- account availability；
- data confidence。

如果公开短视频本身已经提供 10–30 秒热点区间，优先直接引用该公开样本用于试听识别，避免重复托管完整版权音频。
