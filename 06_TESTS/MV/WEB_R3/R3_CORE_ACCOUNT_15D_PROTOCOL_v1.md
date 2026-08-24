# WEB R3｜Core Account 15-Day Music Evidence Protocol v1

> Status: `ACTIVE / R3-A3 CORRECTION`
> Purpose: 把 R3 选歌验证简化为“用户指定核心账号优先”，外围账号只做补充，不允许侧面证据替代核心账号作品级证据。

## 1. Core principle｜HARD FOR R3-A

R3-A 正常主链固定为：

`USER-SEEDED CORE ACCOUNTS`
→ `RECENT 15-DAY WORKS`
→ `WORK-LEVEL DIRECT DOUYIN LINKS`
→ `SONG_FAMILY NORMALIZATION`
→ `CROSS-CORE REPEAT COUNT`
→ `DIRECT VIDEO EVIDENCE PACK`
→ `HG01`

外围音推账号 / 平台榜单只允许在核心账号已经出现歌曲信号之后补充：
- velocity；
- saturation；
- AUDIO_VERSION；
- broader trend corroboration。

**外围证据不能把一个“核心账号中未验证出现”的歌曲直接升级为 HG01 主候选。**

---

## 2. User-seeded core accounts

当前由用户截图明确指定的 8 个账号：

| Account | Douyin ID from user screenshot | Role in R3-A |
|---|---|---|
| 泡泡与茶 | `paopaoandtea` | 核心音乐/翻唱/复热信号 |
| 火乐乐 | `HaoShuo2` | 核心音推/OST/热歌信号 |
| 乐丨青春 | `87136360039` | 核心音乐+MV剪辑信号 |
| XIANGJISHI | `153552032` | 核心风景音推信号 |
| Aura | `Auraaa0131` | 核心风景/音乐沉浸信号 |
| 黑米与糖豆 | `48003855484` | 核心新歌/原创/音推包装信号 |
| 佩佩治愈Ai | `25927051780` | 核心视觉账号；其用歌只作辅助重复信号 |
| 爱的魔力小姐姐 | `326111404` | 辅助核心账号；内容较混合，低权重 |

所有 8 个都观察近15天，但歌曲重复评分按账号角色加权，避免“视觉号的随机BGM”与“音推号主动推歌”完全等权。

---

## 3. 15-day window

当前 R3-A 测试窗口：
- anchor date: `2026-08-24`
- window start: `2026-08-10`
- window end: `2026-08-24`

对每个核心账号，必须逐条建立近15天作品表：
- account；
- exact publish date/time；
- direct Douyin/Douyin精选 work URL；
- work id；
- title/caption；
- song/audio displayed in Douyin（若可见）；
- normalized `SONG_FAMILY`；
- `AUDIO_VERSION`（能识别时）；
- visual format；
- likes/visible performance（如果页面可见）；
- confidence。

没有 direct work URL 的记录不得计入 HG01 的核心重复数。

---

## 4. Repeat logic

### Primary metric
`core_distinct_account_repeat_15d`

同一 `SONG_FAMILY` 在多少个不同用户核心账号的近15天作品中出现。

### Supporting metrics
- `core_music_radar_repeat`：只统计泡泡与茶 / 火乐乐 / 乐丨青春 / 黑米与糖豆等主动音乐类账号；
- `core_visual_repeat`：XIANGJISHI / Aura / 佩佩治愈Ai 等视觉型账号是否也在使用；
- `72h_concentration`；
- `recent_7d_repeat`；
- `audio_version_consistency`。

### Initial R3 threshold
优先进入 HG01：
- 至少 `2` 个不同用户核心账号的 direct work evidence；
- 其中最好至少 `1` 个来自主动音乐/音推账号；
- 3+ 核心账号重复 = 强信号；
- 只有1个核心账号 = 不作为“重复候选”，最多列 `SINGLE_CORE_WATCH`。

阈值仍属于 R3 calibration，不晋升永久 Rule。

---

## 5. Direct evidence pack｜MANDATORY

每个 HG01 候选必须直接交付：

### Song
`SONG_FAMILY / current likely AUDIO_VERSION`

### Core Account Evidence
- 核心账号A｜发布时间｜作品标题｜direct Douyin work link
- 核心账号B｜发布时间｜作品标题｜direct Douyin work link
- 核心账号C（如有）｜...

### What user can inspect directly
- 实际使用哪一段歌；
- 画面/剪辑；
- 字幕；
- 封面文字；
- 标题/描述/标签；
- 当前音推包装方式。

### Supplemental evidence｜optional
只有在核心证据之后附：
- 头部补充音推账号；
- 官方舞台；
- 抖音/汽水榜单；
- 其他趋势信号。

不得用 supplemental evidence 替换 Core Account Evidence。

---

## 6. Retrieval truthfulness｜HARD

必须区分：
- `CORE_WORK_VERIFIED`：已取得核心账号的作品级直接链接；
- `CORE_PROFILE_VERIFIED / WORKS_PENDING`：主页身份可确认，但近15天作品尚未取得；
- `PUBLIC_INDEX_MISSING`：公开搜索未索引；
- `INPUT_PROFILE_URL_REQUIRED`：只有截图/抖音号，没有 canonical profile URL，当前工具无法稳定枚举近15天作品；
- `NOT_FOUND`：只有在已稳定访问主页并完整检查15天窗口后才能使用。

**公开搜索搜不到 ≠ 账号没发。**

---

## 7. Current input reality

用户已提供：
- 8个核心账号主页截图；
- 可读账号昵称、抖音号、视觉/内容定位。

当前缺失：
- 这8个账号的 canonical Douyin profile/share URLs（`/user/<sec_uid>` 或可跳转到该主页的分享链接）。

仅凭截图中的抖音号，当前公开 Web 搜索对这些账号的索引不完整，不能可靠枚举近15天作品。

因此当前正确状态：
`CORE_ACCOUNT_IDENTITIES_LOCKED = YES`
`CORE_PROFILE_URLS_READY = NO`
`CORE_15D_WORK_ENUMERATION = BLOCKED`

解除方法：用户只需一次性提供这些核心账号的“分享主页/复制链接”。不需要逐条提供视频；获取主页链接后，系统目标是自行枚举近15天作品并返回 direct work links。

---

## 8. Stop rule

在 `CORE_15D_WORK_ENUMERATION` 跑通之前：
- 不恢复旧 Radar shortlist 为 HG01；
- 不让用户从外围证据选歌；
- 不进入 R3-B；
- 不把外围账号重复率继续扩张为主任务。

先把核心账号路径跑通，再考虑扩大样本池。
