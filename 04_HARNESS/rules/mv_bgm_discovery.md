# Rules｜MV BGM Discovery v1.0

> Status: `ACTIVE / HARD PRIORITY`
> Role: MV 歌曲选中后，决定“优先从哪里获取真实可用 BGM 版本”的唯一发现规则。
> Core: **Douyin-native exact music asset first. Generic full-track search is fallback, not default.**

---

## 1. Position in workflow

本规则位于：

`HG01 Song Aesthetic PASS`
→ **`BGM VERSION DISCOVERY`**
→ `HG02 BGM Excerpt Listening`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE`

本规则只负责：
- 找到真实候选音频版本；
- 建立版本证据链；
- 生成 HG02 试听候选。

不负责：
- 正式歌词时间轴；
- Director；
- First Frames；
- Picture Edit。

---

## 2. Priority order｜HARD

未来所有 MV 获取 BGM 原曲/母版时，固定优先级：

### P1｜Verified Douyin Music Asset｜DEFAULT FIRST ROUTE
优先从真实抖音作品反查其 `music asset`：
- music asset id；
- displayed music title；
- music author；
- direct asset URL/reference（如可得）；
- aweme id / work URL；
- 实际作品音频。

如果可确认同一趋势中的多个作品使用相同 asset，优先锁这个 asset family，再决定使用短版还是扩展版。

### P2｜Douyin asset anchored full-track discovery
当用户需要比趋势原生片段更长的 30–40s / 完整副歌时：
- 仍以已验证 Douyin asset 为锚点；
- 再寻找公开完整发行版；
- 必须做 audio fingerprint / waveform / vocal phrase / timing 对齐，证明完整发行版包含并匹配该 Douyin asset；
- 对齐成功后才能从完整版扩展。

### P3｜Generic public full-track discovery｜FALLBACK
只有以下情况才进入：
- 找不到可解析的 Douyin asset；
- asset URL 已失效或不可获取；
- 只有单个弱样本且无法建立版本证据；
- 用户明确要求非抖音版本。

可使用：
- 官方发行平台；
- 官方/可信 MV、lyric video；
- Bilibili/其他公开听歌来源；
- 用户上传完整 MP3/WAV。

### P4｜Other recovery routes
P1–P3 均失败时才使用：
- 搜索同名音频下载源；
- 从公开视频提取；
- 其他可验证的镜像/缓存来源。

任何恢复路线都不得静默伪装成 `exact Douyin version`。

---

## 3. Douyin asset verification standard

### Preferred evidence package
至少收集 2 个独立实际作品；优先 3 个。

每个样本保存：
- account / author；
- aweme_id；
- work_url；
- work duration；
- displayed music metadata；
- music asset id；
- music asset URL/reference（如可得）；
- decoded audio duration；
- fingerprint / comparison result。

### Strong PASS
满足以下组合之一：

#### A｜Exact asset identity
- 多个作品暴露相同 `music asset id`；
- 资产标题/作者一致；
- 实际解码音频指纹高相似；
- 最佳 alignment 无异常 global shift，或 shift 可被明确解释。

State：
`DOUYIN_EXACT_MUSIC_ASSET_CONFIRMED = YES`

#### B｜Single direct asset + independent corroboration
只有单个可下载 asset 时，必须再有至少一条独立证据：
- 另一作品相同 asset metadata；或
- 与官方/完整发行版 fingerprint 对齐；或
- 同一 hook 的强声学对齐。

State：
`DOUYIN_MUSIC_ASSET_HIGH_CONFIDENCE = YES`

### Weak / blocked
仅有：
- 相同歌名；
- 相同 hashtag；
- 评论区说是同一首；
- 搜索页面标题相似；
- 人耳觉得“像”；

均不足以锁版本。

State：
`BGM_VERSION_DISCOVERY_BLOCKED / NEEDS_VERIFICATION`

---

## 4. Trend-native excerpt strategy

当多个核心作品使用同一 asset 且起点一致：
- 优先选择其中**最长、音质最好、结构最完整**的实际使用版本作为 HG02 trend-native reference；
- 短作品若 fingerprint 表明只是同起点 truncation，不把它误判为另一版本；
- 不为了凑 30–40 秒擅自换成未知完整版。

默认先给用户：
`Option A｜trend-native exact excerpt`

只有用户觉得太短或语义不完整时，再给：
`Option B｜asset-anchored extended excerpt`

---

## 5. Quality checks before HG02

试听文件提交用户前至少检查：
- 可正常解码；
- 无明显视频残留噪声/二次压缩故障；
- 无前一句污染；
- 不截断当前句；
- 结尾 release 完整；
- 采样率/声道信息可读；
- duration 与来源记录一致；
- 保存 source identity / transform / hash。

如果直接从视频抽取：
- 记录它是 `video-derived listening reference`；
- 后续若拿到同 asset 的直接 MP3，优先替换为 direct asset master 并重新核 hash。

---

## 6. Platform-availability meaning｜IMPORTANT

本规则中的“抖音可用 / trend-native / platform-native”表示：
- 该音乐资产可被真实抖音作品引用；
- 我们能验证实际作品正在使用；
- asset/version identity 可追溯。

它**不等于跨平台版权授权证明**，也不替代抖音账号在具体地区、具体发布时间、具体商业用途下的音乐授权状态。

发布前若平台实际显示音乐不可用/被替换，以平台当时状态为准。

---

## 7. Required provenance artifact

每首歌在 BGM lock 前至少保存一个 discovery receipt，建议：

`BGM_DISCOVERY/asset_probe_report.json`

字段至少包含：
- song_family；
- discovery_priority_used；
- sampled_aweme_ids；
- music_asset_id；
- music_title；
- music_author；
- music_asset_reference；
- pairwise fingerprint results；
- selected listening source；
- selected excerpt duration；
- direct_asset_or_video_derived；
- fallback_reason（若未走 P1）；
- decision。

正式 `BGM_LOCKED` 后，再由 `mv_audio_timeline.md` 接管时间真值。

---

## 8. Hard anti-shortcut rules

禁止：
- 一上来按歌名搜索完整 MP3，跳过 Douyin asset probe；
- 因为公开完整版更容易下载，就覆盖已验证的趋势原生版本；
- 只凭 title/artist 相同认定 same recording；
- 把 12s/24s 不同长度直接当成不同 remix；
- 没有 provenance 就声称“抖音同款”；
- 用户未要求扩展时，为追求更长而主动换版本。

---

## 9. Current validated example｜R3 evidence

WEB R3《如果风会替我说话》验证：
- 3 个独立核心作品；
- 相同 Douyin music asset id `7670880580757867270`；
- displayed music：`@林叙（错位秋天已上线）创作的原声`；
- pairwise Chromaprint similarity ≈ `0.986–0.995`；
- best alignment `shift=0`；
- 两个约 12s 作品是同起点截短；
- 最长约 24.3s 样本被用于 HG02 trend-native listening reference。

该案例证明：
**先从抖音真实使用资产反查版本，能显著降低“同歌名、错录音版、错副歌位置”的风险。**

本案例只作为方法验证，不把具体歌曲/长度固化为模板。
