# MV Reference Director｜核心参考账号与音乐池 v2

> Build Phase: B00–B06
> Status: `RECOVERED / BEST-EFFORT UPDATED`
> Historical raw source: `test/mv-web-r3/06_TESTS/MV/WEB_R3/database/works.csv`

## 1. 核心修正

用户提供的 9 个核心账号 **全部进入 Song Pool**。

账号的 `Primary Role` 只决定权重和擅长方向，不再决定“是否允许贡献歌曲”。

- 音乐雷达账号：更适合判断新歌 / 复热 / 版本 / 包装。
- 视觉账号：同样贡献歌曲，并且对“歌曲 × 画面适配”价值很高。
- 剪辑 / 卡点账号：同时贡献歌曲、片段长度、卡点和镜头参考。
- 辅助账号：有可验证作品就纳入；没有抓取到作品时标记缺口，不按 0 处理。

因此正式规则为：

`ALL CORE ACCOUNTS → SONG POOL`  
`ACCOUNT ROLE → WEIGHT / INTERPRETATION`  
`NOT → EXCLUSION`

---

## 2. Core Accounts

| ID | Account | Primary Role | Music Pool | Music Use | Visual / Edit Use | Captured Works* |
|---|---|---|---|---|---|---:|
| DYCORE01 | 黑米与糖豆 | 新歌 / 原创 / 音推包装 | YES | 原创新歌、甜歌、R&B、新歌上线 | 包装辅助 | 8 |
| DYCORE02 | 佩佩治愈Ai | 人物型 AI 治愈视觉 | YES | 画面与配乐组合、情绪音乐 | **高权重动画视觉** | 8 |
| DYCORE03 | 乐 ♩青春 | 音乐 + 剪辑 + 歌词 + 卡点 | YES | 歌曲发现、歌词段 | **高权重卡点 / 剪辑** | 12 |
| DYCORE04 | Aura | 高审美风景 / 低文字沉浸 | YES | 风景型歌曲、情绪歌曲 | **高权重场景 / 治愈** | 18 |
| DYCORE05 | Lynne小凌 | 翻唱 / 音乐种草补充 | YES | 翻唱、经典、热歌版本 | 表演辅助 | 7 |
| DYCORE06 | 泡泡与茶 | 翻唱 / 复热 + 温暖人设 | YES | Cover、复热、情绪歌曲 | 人物包装辅助 | 3 |
| DYCORE07 | XIANGJISHI | 风景音推 / 治愈空间 | YES | **歌曲 + 场景双重信号** | **高权重治愈场景** | 16 |
| DYCORE08 | 火乐烁 | 高频音推 / OST / 热歌信息 | YES | **高权重 Song Radar / 版本发现** | 包装辅助 | 17 |
| DYCORE09 | 爱的魔力小姐姐 | 混合内容辅助样本 | YES | 有作品即纳入 | Auxiliary | 0 captured |

`*` Captured Works = 旧数据库已实际保存的 2026-08-10 ～ 2026-08-17 抓取窗作品数；不是账号总作品量，也不是当前作品量。

总计：`89 captured works`。

DYCORE09 的 `0 captured` 只代表该抓取窗没有保存到作品，禁止解释为“账号没有音乐作品”。

---

## 3. 账号权重的正确用法

以后选歌不是“先只看 4 个音乐账号”。

正确方式：

1. 9 个核心账号的可验证音乐作品全部入池；
2. 同一 `SONG_FAMILY` 跨账号出现时提高信号；
3. 再根据账号角色解释信号：
   - 火乐烁重复：趋势 / 版本信号更强；
   - Aura / XIANGJISHI 重复：治愈视觉适配更强；
   - 乐♩青春重复：歌词 / 卡点 / 剪辑适配更强；
   - 佩佩治愈Ai 使用：动画 / AI 视觉适配值得重点观察；
   - 泡泡与茶 / Lynne：Cover / 复热 / 人声版本价值更高；
   - 黑米与糖豆：原创 / 新歌 / 包装价值更高。
4. 不做简单等权平均，也不因 Primary Role 是 Visual 而丢弃音乐。

---

## 4. 已恢复的跨账号歌曲信号

当前历史抓取窗中，已明确看到：

- `爱让人脑袋空空`：乐♩青春 + Aura + Lynne小凌 + 火乐烁（≥4 core accounts）。
- `如果风会替我说话`：乐♩青春 + XIANGJISHI + 火乐烁（≥3）。
- `若爱有尽头`：乐♩青春 + XIANGJISHI（≥2）。
- `我救自己于人间水火`：Aura + XIANGJISHI（≥2）。
- `Summer Love / 爱在盛夏`：Aura + XIANGJISHI（≥2）。
- `杀破狼`：乐♩青春 + XIANGJISHI（≥2）。
- `做她的大地别做她的天`：Aura + 火乐烁（≥2）。
- `有几次想你了`：XIANGJISHI + 火乐烁（≥2）。
- `沈园外`：Lynne小凌 + 火乐烁（≥2，版本不同）。

这些重复只证明 `SONG_FAMILY` 信号；进入 MV 后必须重新锁具体 `AUDIO_VERSION`。

---

## 5. 数据更新策略｜BEST EFFORT，不追求伪最新

每轮更新：

1. 优先从 9 个核心账号恢复 / 获取可直接打开的真实作品；
2. 能更新到哪里就更新到哪里，不要求所有账号同步到同一天；
3. 旧数据库中已经有直接作品 URL 的，允许作为有效候选池；
4. 搜索引擎没有索引到更新作品时，标 `INDEX_PENDING`，不解释为“没发”；
5. supplemental / 汽水音乐只做佐证，不能替代核心账号作品；
6. 数据库完成条件 = **每个核心账号都被处理，并明确写出目前可恢复覆盖和缺口**，不是强行追到最新。

---

## 6. Song Family / Audio Version

选歌比较阶段：`SONG_FAMILY`。

用户选中具体抖音作品并下载后：锁 `AUDIO_VERSION`。

同一歌不同账号可能是：原唱 / Cover / Remix / 电音 / R&B / Live / 剪辑片段；禁止提前当成同一音频。

---

## 7. 人工交付规则

完成数据库比较后，每轮只给用户最多 3 个 Primary Candidates：

- 歌曲；
- 来源核心账号；
- 对应抖音视频直链；
- 跨账号证据；
- 动画 MV 适配理由；
- 风险 / 已使用历史；
- 推荐优先级。

用户只需要实际打开视频，选定要下载并发回的一个 Reference。

---

## 8. Evidence

- `test/mv-web-r3/06_TESTS/MV/WEB_R3/database/accounts.csv`
- `test/mv-web-r3/06_TESTS/MV/WEB_R3/database/works.csv`
- `test/mv-web-r3/06_TESTS/MV/WEB_R3/R3_BENCHMARK_ACCOUNT_REGISTRY_v1.md`
- `02_SONG_POOL_RECOVERY.csv`

旧 `works.csv` 保留为 work-level 唯一原始快照，不在本工作区复制 89 行，避免双份事实源漂移。