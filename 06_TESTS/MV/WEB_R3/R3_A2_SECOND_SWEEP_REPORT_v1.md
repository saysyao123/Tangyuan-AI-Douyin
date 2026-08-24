# WEB R3｜A2 7-Day Music Radar｜Second Sweep v1

> Date: 2026-08-24
> Status: `A2 PASS / READY FOR A3 SHORTLIST`
> Principle: 只把“作品级可验证的近期信号”计入 creator repeat；平台列表只作 corroboration。

## 1. Second-sweep result

第二轮扩样后，第一轮方法得到进一步验证：

### 甲乙丙丁｜CONFIRMED / SATURATION RISING
近约 4 天内可验证的独立 creator / official signals 至少包括：
- 浙江卫视：张碧晨×侯明昊舞台；
- 不爱笑的谭老师：舞台/声乐解析；
- 付飞翔：制作人解析；
- 鬼面P：洛天依翻唱；
- 张與息：短视频演唱/使用；
- 何和声音社长：近期音乐解析；
- 媛圆姐姐：舞蹈使用。

平台侧汽水音乐多个相关 playlist 也持续出现李佳薇版本。

结论：趋势确定性目前最高之一，但已从“抢跑”进入“确认热 + 饱和度开始上升”。

### 循迹｜EARLY_RISE / HIGH VELOCITY
48–72h 内可验证的独立音乐信号：
- 王铮亮：舞台 cut；
- 李佳薇：15秒70字挑战；
- 匡泓霖琵琶：琵琶高燃改编。

并且《天赐的声音7》舞台及相关媒体讨论在 8/21–8/23 集中出现。

结论：creator repeat 数低于《甲乙丙丁》，但时间集中度更高，属于明显 `EARLY_RISE`。风险是歌词存在高密度段，R3-B 必须选对 excerpt，不能把“15秒70字”本身当成视觉任务硬做。

### 雨后轻风有香｜EARLY_RISE / BEST HEALING FIT
严格 7d 边界内可验证的独立信号至少包括：
- wuhu动画人空间：电影《牛来》片尾曲介绍；
- 立德读书：歌词解析；
- 乐活花道：同名音乐内容；
- Scot_1988：动态简谱/不同演唱版本。

另有多个近期外围讨论/发行信号。

结论：绝对重复量不如《甲乙丙丁》，但视觉适配是当前候选中最高：雨、风、荒草、丘壑、枝柯等意象非常适合 R3 的自然治愈 + 轻梦幻视觉。需要特别处理 `轻风/清风` 标题写法和不同 cover/audio version，不允许直接把 SONG_FAMILY 当作 exact audio identity。

### 我不难过｜CONFIRMED CLASSIC REVIVAL
约 24h 内至少三个高质量音乐账号集中出现：
- 马呜呜：制作人解析孙燕姿现场；
- 志鹏Cello：经典赏析；
- DSD音乐：流行热歌榜版本。

结论：这是比“随机老歌被某一个账号发”更强的经典复热信号。趋势质量高，格式也更接近音乐推荐；视觉情绪偏伤感，需要 R3-B 把“治愈”理解为克制/释怀，而不是明亮童话。

### 琵琶曲（东船与西舫）｜CONFIRMED VISUAL / FORMAT RISK
近约 3 天内可验证：
- 可尔rke：唱跳/短视频；
- 青雀 易小木：敦煌舞；
- 轻风如沐：首唱/音乐内容。

结论：古风视觉适配很高，但当前扩散格式明显偏舞蹈/古典舞，且 `东船与西舫` 是歌词识别词，exact SONG_FAMILY / AUDIO_VERSION 需要进一步澄清。适合做备选，不适合在 A3 前假装版本已锁。

### 第57次取消发送｜OVERHEATED / FORMAT MISMATCH
第二轮继续看到多个舞蹈/手势舞/教程账号密集使用。

结论：它是很好的反例：cross-account repeat 非常强，但扩散格式与“治愈AI音推”差异太大，而且已经明显饱和。A3 不作为优先候选。

---

## 2. A2 scoring model after calibration

R3-A2 实验评分建议：

- 30% `distinct_creator_repeat_7d`
- 20% `72h_concentration / velocity`
- 15% `head / high-quality music account signal`
- 10% `platform corroboration`
- 15% `healing visual fit`
- 10% `lyric visualizability`
- minus `saturation_penalty`
- minus `format_mismatch_penalty`
- minus `audio_version_ambiguity_penalty`

注意：这还是 R3 实验评分，不晋升生产 Runtime。

---

## 3. Evidence-coverage finding

公开搜索无法完整索引用户最初提供的所有主页近7天作品，因此：
- 搜不到不计 0；
- 用户截图用于账号角色、视觉、包装 Benchmark；
- A2 trend repeat 只使用可验证的作品级证据；
- supplemental music creators 用于弥补公开索引覆盖；
- A3 必须显示“趋势确定性”与“视觉适配”是两个维度。

这比假装已经完整抓取所有主页更可靠。

---

## 4. A2 Gate result

`R3-A2 = PASS`。

理由：
1. 已经能稳定识别 `EARLY_RISE / CONFIRMED / OVERHEATED` 三类不同趋势；
2. 重复率高但格式不匹配的歌能被主动降权；
3. 视觉高度适配但绝对重复较低的早升歌不会被简单排行榜漏掉；
4. SONG_FAMILY 与 AUDIO_VERSION 的区分在多个候选上都证明必要。

Next：`R3-A3 / Shortlist Validation -> HG01`。
