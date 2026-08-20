# MV Benchmark Layer｜持续外部参照层

> 类型：Knowledge / External Reference
> 作用：为 MV 选歌、Hook、导演、首帧、动态、剪辑和最终复盘提供滚动外部坐标。
> 权限：**只提供参考，不直接成为硬规则。** 外部观察必须经过本项目实际生产验证，才允许进入 Golden Reference / SOP / Rules。

## 1. 为什么存在这一层

单纯依赖热榜会出现三个问题：
1. 热门歌曲不等于适合 MV；
2. 歌曲名不等于抖音里的具体热门音频实体；
3. 即使数据热，也不知道当前 MV 垂类创作者正在怎样使用它。

因此本项目在平台热度之外增加一层 `MV Benchmark Pool`，持续观察：

`头部/高质量MV作者最近在做什么 → 用什么歌/版本 → 怎么开场 → 怎么组织画面 → 哪些做法开始重复 → 哪些新方法值得我们内部测试`

这层的目标不是抄，而是让每个关键阶段拥有最新的外部坐标系。

---

## 2. 初始 Benchmark Pool v0.1

### Market / Product / Release
- `AI MV导演曹斌Johnny`：MV产品形态、歌曲包装、预告/完整版/卡拉OK衍生、Seedance MV实验。
- `Mr.16 罗隽永`：音乐人侧的音乐产品、Visualizer/MV如何服务歌曲传播；当前作为 musician-side watchlist。

### Aesthetic / Concept
- `野仙仙AI`：高审美、概念先行、专业美术/导演语法。
- `SANGR桑瑞`：艺术化 AIMV、概念表达、音乐与视觉统一。
- `丹鸾歌行`：东方/赛博东方、强动态、视觉事件、短视频节奏。

### Director / Workflow / Automation
- `老鹰的AI思考`：AI视频生产系统、自动化、模型测试、导演到工程链。
- `石硕Simon`：分镜、人物空间关系、多镜头、连续性与技术实验。
- `👑猫宅V酱`：AIMV workflow、跨题材流程、工具组合。

### World / Mood / Long-form
- `豹裂漫元AIGC`：新东方、武侠、克制情绪、场景氛围、AI短片/漫剧。
- `王悦（大悦聊）/ Ailee 艾莉（王悦作品）`：长时长 AIMV、完整世界、AI音乐与视觉的一体化包装。

> Pool 不是永久名单。目标容量默认 10–15 个。新增/移除依据“当前对项目是否仍有信息价值”，而不是粉丝量。

---

## 3. 不在每个步骤都全量分析｜采用 JIT Benchmark

### R1S01｜BGM Discovery
**必须刷新最近 7 天窗口。**
重点只看：
- 最近发布的 MV / 音乐视觉作品；
- 使用的歌曲/具体版本；
- 是否多个 Benchmark 作者出现相同歌曲/相同音乐趋势；
- 常见成片时长；
- 开头 1–3 秒；
- 当前流行的视觉/剪辑形式。

用途：给平台热榜增加 `MV_VERTICAL_ADOPTION` 信号。

### Same-BGM Reference / Opening Hook
选定具体 BGM 后，优先找：
1. 同 BGM 当前高互动视频；
2. Benchmark Pool 中类似情绪/类型的优秀作品。

Benchmark 用于判断 Hook、美感门槛、同质化，不代替同 BGM 市场样本。

### Music / Lyric Structure
默认不重新刷新整个 Pool。复用 S01 快照即可。
只有发现特殊歌曲结构时，按需找 1–3 个同结构案例。

### Director Design
**固定做 Focused Benchmark。**
按当前歌曲选择最相关的 3–5 个作品，只回答：
- 核心视觉事件怎么设计；
- 景别/视角为什么变化；
- 强弱曲线；
- 人物动作和环境动作；
- 哪些套路已经明显重复。

禁止机械复制镜头。

### First-frame Group
选择 2–3 个“审美/构图参考作品”，只做 Beauty Bar 对照：
- 第一眼是否够美；
- 主视觉是否明确；
- 光色/材质是否高级；
- 是否像普通 AI 图。

### Dynamic Prompt / Seedance QA
选择 2–3 个动态/导演型 benchmark，只对照：
- 动作密度；
- 镜头变化；
- 视觉事件；
- 首帧到动态后的美感损失；
- 模型能力边界。

### Editing / Final QA
选择 2–3 个市场/完成度 benchmark，对照：
- 前 3 秒；
- 全片节奏；
- 高潮位置；
- 歌词可读性；
- 完成度。

外部 benchmark **不能替代项目内部 Golden Sample**。最终硬下限仍由我们的 Golden Sample 决定。

---

## 4. Refresh 机制

### Rolling Window
- 默认观察窗口：最近 7 天。
- 每次 R1/R2 新歌曲进入 S01 时，刷新一次轻量快照。
- 同一制作轮内不要为了“实时”反复刷新，避免噪音。

### 强制刷新触发器
出现以下任一情况，允许提前刷新：
- Seedance / 即梦 / 主要视频模型发生明显版本升级；
- 抖音音乐/版权/发布机制明显变化；
- Benchmark 作者出现明显新工作流或爆发式新形式；
- 当前 Golden Sample 被连续多首作品明显超过；
- 某账号连续 30 天没有相关产出，权重下降；
- 新出现更贴合本项目的高质量作者。

### Freshness Weight
- `ACTIVE_7D`：最近 7 天有相关产出，优先参考当前市场/工具状态。
- `ACTIVE_30D`：最近 30 天有相关产出，可作为当前参考。
- `SPECIALIST_REFERENCE`：近期不活跃，但代表作品仍有较高审美/导演学习价值。
- `WATCHLIST`：信息不足或与当前项目距离较远，不进入默认 Focused Benchmark。

---

## 5. 每次观察的最小字段

每个被采用的参考作品至少记录：
- account
- work title / url
- observed_at
- publish_date（能取到时）
- duration（能取到时）
- BGM / version（能确认时）
- first_1_3s_hook
- core_visual_event
- shot / camera pattern
- lyric treatment
- strongest_value
- anti_pattern / homogeneity risk
- relevance_to_current_stage
- evidence_confidence

不伪造取不到的数据。

---

## 6. 观察结果只允许进入四种状态

- `OBSERVATION`：单个作品看到的事实/现象。
- `REPEATED_PATTERN`：多个作品/账号重复出现的模式。
- `ANTI_PATTERN`：已经高度同质化、我们应主动避免的模式。
- `HYPOTHESIS_TO_TEST`：看起来值得学，但尚未在本项目验证。

外部 Benchmark **不能直接产生 `PRODUCTION_VALIDATED` 或 `PERFORMANCE_VALIDATED`**。

必须经过：

`External Observation → Internal Experiment → User Review → R1/R2 Evidence → Golden/SOP/Rule Promotion`

---

## 7. Anti-Copy Gate

使用外部案例前必须回答：
1. 我们学习的是“原理”还是“表面镜头”？
2. 如果换一首歌，这个方法是否仍有逻辑？
3. 是否已经是赛道高频套路？
4. 有没有办法保留原理但换成属于本歌词的视觉事件？

如果只是复制：
`服装 + 构图 + 运镜 + 动作 + 转场`
则直接拒绝。

---

## 8. 与 BGM Data Source 的关系

Benchmark Pool 只提供 `MV_VERTICAL_ADOPTION`，不能替代真实音乐数据。

R1S01 最终仍需要同时成立：

`PLATFORM_HEAT`
+ `EXACT_DOUYIN_MUSIC_ENTITY`
+ `RECENT_SAME_BGM_SAMPLE`
+ `MV_VERTICAL_ADOPTION`（有则加分）
+ `VISUAL_FIT`
+ `ACCOUNT_AVAILABILITY`

在数据源尚未完全打通前，不设置伪精确权重。

---

## 9. 当前原则

**Benchmark 是动态导航，不是答案。**

我们希望最终得到的是：

> 集百家之长，但每首歌仍然先问“这句歌词最应该长成什么样”。
