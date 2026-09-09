# MV Reference Director｜参考账号恢复表 v1

> Build Phase: B00–B01
> Status: `RECOVERED / FRESHNESS RECHECK REQUIRED`
> Historical source: `test/mv-web-r3`

## 1. 恢复结论

旧项目中已经存在较完整的参考账号体系，不需要从零重建。

当前恢复的可靠事实：

- 用户种子核心账号共 9 个；
- 账号职责原本就分为：选歌 / 趋势、视觉、剪辑包装、辅助样本；
- 账号身份、历史角色和历史 profile link 可作为恢复基线；
- 2026-08-24 的趋势热度、近 7 天作品和歌曲排序属于历史快照，**不能直接视为当前有效**；
- 当前选歌优先恢复“账号池”，再刷新这些账号最近作品。

---

## 2. Core Accounts

| Account | Primary Role | 当前用途 | 历史 Profile | Freshness |
|---|---|---|---|---|
| 火乐烁 | 高频音推 / OST / 热歌信息 | **Primary Song Radar** | https://v.douyin.com/usOw3DchtXY/ | RECHECK |
| 泡泡与茶 | 翻唱 / 复热 + 温暖人设音乐 | **Song Revival / Cover Radar** | https://v.douyin.com/TJckP4icg1A/ | RECHECK |
| 黑米与糖豆 | 新歌 / 原创 / 音推包装 | **New Song Radar + Packaging** | https://v.douyin.com/_YS8e0YhgWo/ | RECHECK |
| 乐 ♩青春 | 音乐 + 剪辑 + 歌词 + 卡点 | **Song + Beat/Edit Reference** | https://v.douyin.com/CjEXFsxea4E/ | RECHECK |
| 佩佩治愈Ai | 人物型 AI 治愈视觉 | **Animation Visual Benchmark** | https://v.douyin.com/wIybp87hyRc/ | RECHECK |
| Aura | 高审美风景 / 低文字沉浸 | **Scene / Healing Benchmark** | https://v.douyin.com/u8LKkQ0QoY4/ | RECHECK |
| XIANGJISHI | 风景音推 / 治愈空间 | **Scene + Music Mood Benchmark** | https://v.douyin.com/Gy5W5QEGc_s/ | RECHECK |
| Lynne小凌 | 历史补充测试账号 | Auxiliary | https://v.douyin.com/GkxtPfYaRFk/ | RECHECK / ROLE TBD |
| 爱的魔力小姐姐 | 混合内容辅助样本 | Auxiliary | https://v.douyin.com/vZceq-VjuH8/ | RECHECK |

### 当前推荐优先级

选歌时先看：

1. 火乐烁
2. 泡泡与茶
3. 黑米与糖豆
4. 乐 ♩青春

视觉翻译时再看：

1. 佩佩治愈Ai
2. Aura
3. XIANGJISHI
4. 乐 ♩青春

不要把视觉账号的用歌直接等权当趋势信号。

---

## 3. Supplemental Radar

历史补充账号：

- 碳酸音乐：近期 / 月度热歌盘点；趋势辅助。
- 油条Music：大体量音乐盘点；需类型降权。
- CD传媒：动态歌词 / 经典歌近期再出现。
- 志鹏Cello：音乐赏析 / 经典复热。
- 马呜呜：音乐制作 / 经典歌讨论辅助。
- DSD音乐〖百万调音师〗：高频热歌 / 经典歌发布；只作重复率辅助。

当前公开检索已确认：

- `碳酸音乐` 在 2026-09-02 仍发布“2026年9月最近很火的12首歌曲”类内容，因此可继续保留为当前 supplemental radar。

Supplemental 账号只能作为辅助；正式 Primary Reference 仍优先回到用户种子账号和直接抖音作品。

---

## 4. 选歌数据的可靠性等级

### A｜CURRENT DIRECT

当前核心参考账号中存在可直接查看的近期作品，并能明确识别歌曲 / 音频。

可用于 Human Reference Gate。

### B｜CURRENT CORROBORATED

有当前补充账号 / 汽水音乐 / 其他公开抖音信号，但尚未在核心账号中确认。

可进入 WATCH，不直接锁歌。

### C｜HISTORICAL

只有旧 Radar / 旧数据库证据。

只能作为重新检查的候选，不允许直接使用旧热度结论。

### D｜UNKNOWN

身份、链接、歌曲或版本无法确认。

不使用，直到重新建立证据。

---

## 5. Song Family / Audio Version 规则继续保留

趋势阶段先判断：

`SONG_FAMILY = 歌曲本身`

进入真实 MV 后再锁：

`AUDIO_VERSION = 具体原唱 / Live / Cover / Remix / sped-up / OST excerpt`

禁止因为多账号都在使用同一 SONG_FAMILY，就误以为它们使用的是同一音频版本。

---

## 6. 当前更新策略

每次选新 MV：

1. 先查看核心 Song Radar 账号近期作品；
2. 提取 3–8 个 Song Family；
3. 用 supplemental / 汽水音乐做当前性佐证；
4. 过滤明显过热、纯舞蹈玩法或动画化价值低的候选；
5. 最终只向用户展示最多 3 个可直接查看的抖音 Reference 候选；
6. 用户选择 Primary Reference；
7. 用户下载视频并提供给项目；
8. 后续才进入 BGM / Lyrics / Beat / Duration。

---

## 7. 旧数据源

可靠恢复源：

- `06_TESTS/MV/WEB_R3/R3_BENCHMARK_ACCOUNT_REGISTRY_v1.md`
- `06_TESTS/MV/WEB_R3/database/accounts.csv`
- `06_TESTS/MV/WEB_R3/R3_MUSIC_RADAR_WEEK_01.csv`
- `06_TESTS/MV/WEB_R3/R3_MUSIC_SHORTLIST_v1.md`
- `06_TESTS/MV/WEB_R3/database/`

这些历史文件作为 Evidence，不再作为当前执行事实源。
