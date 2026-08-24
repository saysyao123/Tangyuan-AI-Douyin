# WEB R3｜A2 7-Day Music Radar｜First Sweep v1

> Date: 2026-08-24
> Status: `A2 IN PROGRESS / FIRST SWEEP COMPLETE`
> Scope: 先验证“跨账号重复 + 时间集中 + 视觉适配 + 饱和风险”的方法是否能产生有效信号；本文件不是 A3 最终 shortlist。

## 1. Current strongest observed SONG_FAMILY signals

| SONG_FAMILY | Verified distinct creator signals | Platform corroboration | Recency concentration | Visual fit | Saturation risk | Current read |
|---|---:|---|---|---:|---|---|
| 第57次取消发送 | >=6 | yes/current ecosystem | 2–6d very dense | 6/10 | **HIGH** | 明显爆发趋势，但当前主要由舞蹈/手势舞扩散；可能已偏过热，需惩罚 |
| 甲乙丙丁 | >=3 | yes | **<1d very dense** | 8/10 | MEDIUM | 当前最强的“正在集中出现”音乐信号之一；情绪视觉可做 |
| 我不难过 | >=3 | supporting music ecosystem | **<1d very dense** | 8/10 | MEDIUM | 经典歌复热非常明显；至少三个音乐解析/发布账号集中出现 |
| 雨后轻风有香 | >=2 | yes | 1–5d | **10/10** | LOW–MEDIUM | 重复数低于前两首，但自然意象/治愈视觉适配极高，属于值得追踪的早升候选 |
| 开始懂了 | >=2 | supporting | 1–5d | 8/10 | LOW–MEDIUM | 中等复热信号；需要继续看第二批账号是否重复 |
| 我怀念的 | creator evidence incomplete | yes/current multiple lists | current | 8/10 | MEDIUM | 平台信号较多，但本轮公开可索引的独立7d创作者证据还不够 |
| 一直很安静 | creator evidence incomplete | yes/current multi-version | current | 9/10 | MEDIUM | 多版本在平台生态重复，需特别防止 AUDIO_VERSION 混淆 |
| 情歌 | creator evidence incomplete | yes/current | current | 9/10 | MEDIUM | 视觉适配强，但当前跨UP主证据不足 |

## 2. Why the method is already useful

### Example A｜`第57次取消发送`
如果只看“重复率”，它会排第一。
但样本显示主要扩散在：
- 手势舞；
- 舞蹈教程；
- 卡点舞；
- 同类玩法。

所以 R3 必须加入：
`saturation_penalty + format_mismatch_penalty`。

它证明“重复最多 ≠ 最适合我们”。

### Example B｜`雨后轻风有香`
跨账号重复数目前只到约2个 creator，但：
- 近几天集中出现；
- 有平台/曲谱侧 corroboration；
- 歌词/歌名天然具备风、雨、香、自然、轻治愈视觉意象；
- 与 R3-B 的佩佩/Aura/XIANGJISHI视觉升级目标高度适配。

所以它可能比单纯重复率更高的舞蹈热歌更适合我们的账号。

### Example C｜`甲乙丙丁` vs `我不难过`
两首都在约24小时内出现 >=3 个独立 creator signals：
- `甲乙丙丁` 更像近期具体版本/舞台推动的集中传播；
- `我不难过` 更像经典歌曲的集中复热。

R3-A3 必须区分：
`NEW/ACTIVE_PUSH` vs `CLASSIC_REVIVAL`，不能只给一个总分。

## 3. First scoring model adjustment

R3-A2 后续建议评分：

`Trend Score =`
- 30% distinct creator repeat 7d
- 20% 72h concentration / velocity
- 15% head-account or high-quality music-account signal
- 10% platform corroboration
- 15% healing visual fit
- 10% lyric visualizability
- minus saturation penalty
- minus format mismatch penalty
- minus audio-version ambiguity penalty

这只是 R3 测试评分，不晋升 Production Runtime。

## 4. Evidence coverage limitation

当前第一轮主要依赖：
- 用户提供的 Benchmark 账号角色信息；
- 公开索引的抖音/抖音精选近期作品；
- 汽水音乐相关列表；
- supplemental public accounts。

限制：
- 泡泡与茶、火乐乐、乐丨青春、Aura、XIANGJISHI、佩佩治愈Ai 等用户核心种子账号的完整近7天作品，没有全部被公开搜索索引；
- 因此没有把“搜不到”记成0；
- A3 之前应继续扩大可索引样本，并尽可能对用户核心雷达账号补齐近期作品。

## 5. Current stage decision

`R3-A1 = PASS`

`R3-A2 = IN PROGRESS / METHOD VALIDATED BY FIRST SWEEP`

Do not enter A3/HG01 yet.

Next A2 pass:
1. 继续补充 7d music-push/revival creators；
2. 专项追踪当前 top signals；
3. 查同一 SONG_FAMILY 是否在用户核心雷达账号出现；
4. 计算 evidence coverage + weighted score；
5. 再形成 A3 3–5首 shortlist。
