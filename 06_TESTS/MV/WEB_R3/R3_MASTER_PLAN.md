# WEB R3｜MASTER PLAN v1.0

> Branch: `test/mv-web-r3`
> Goal: 在不破坏 R2 已锁生产链的前提下，分阶段验证「趋势选歌雷达 → 治愈视觉升级 → 完整MV整合 → 发布包装」四个新模块。
> Principle: **一次只测试一个主变量；R2 correctness pipeline 默认冻结。**

---

# 0. R3 不是什么

R3 不是“再做一首歌然后边做边改所有东西”。

R3 是一个多轮实验计划：
- 每轮只回答一个核心问题；
- 每轮都有明确输入、输出、Gate；
- PASS 才晋升到下一轮；
- FAIL 只修当前变量，不重开 R2 已通过模块。

R2 frozen baseline：
- `AUDIO_TIMELINE_PACKAGE` hard gate；
- 1–3镜 RAW SOURCE + W07.5 Atom/Arc Normalization；
- long-cut-first + visible-shot Fragmentation Gate；
- R1/WEB R2 locked subtitle baseline + geometry QA；
- 5 fixed Human Gates；
- Patch, Don't Cascade。

R3 禁止为了新视觉/新选歌实验修改上述 correctness baseline，除非出现真实回归证据。

---

# 1. R3 总体测试结构

## R3-A｜Music Radar / Benchmark Calibration

回答：
**我们能不能稳定找出“过去7天正在起势、多个音推账号重复出现、又适合我们AI治愈视觉”的歌？**

不做完整 MV。

主要新变量：选歌情报系统。

### Inputs
第一批人工种子账号：
- 泡泡与茶
- 火乐乐
- 乐丨青春
- XIANGJISHI
- Aura
- 黑米与糖豆
- 佩佩治愈Ai
- 爱的魔力小姐姐（辅助样本，非核心）

后续再补充若干真正头部/高频音推账号。

### Observe
过去 7 天每个账号的：
- song family；
- audio version（能识别时）；
- publish time；
- likes / visible performance；
- video visual type；
- cover/on-video title；
- caption/description；
- hashtags；
- 是否明显属于新歌 / OST / 翻唱回潮 / 老歌复热。

### Core metrics
每首 SONG_FAMILY：
- `cross_account_repeat_7d`
- `cross_account_repeat_72h`
- `distinct_account_count`
- `trend_velocity`
- `head_account_signal`
- `visual_fit_score`
- `lyric_visualizability`
- `saturation_penalty`

### Output
`R3_MUSIC_RADAR_WEEK_01.csv`
+ `R3_MUSIC_SHORTLIST_v1.md`

Shortlist 只分：
- `EARLY_RISE / 抢跑候选`
- `CONFIRMED / 稳妥候选`
- `OVERHEATED / 已过热观察`

### Human Gate
HG01 只在 shortlist 后选 1 首进入下一阶段。

### PASS
至少能找到 3 首来源独立、重复信号明确、视觉适配可解释的候选；不能只是凭单账号主观推荐。

---

## R3-B｜Healing Visual Calibration

回答：
**结合我们当前生成能力，能否把画质和视觉气质明显向“高质感治愈AI视觉”推进，而不牺牲稳定生产？**

不做整首 MV；先做小样测试。

主要新变量：视觉美术层。

### Locked from R2
- 歌曲和 BGM 片段按 Stage 2 锁定；
- Audio Timeline Package 先锁；
- 不改剪辑/字幕系统；
- 不测试发布文案。

### Visual Benchmark roles
- `佩佩治愈Ai`：人物型治愈视觉上限参考
- `Aura / XIANGJISHI`：自然风景、空间沉浸、低文字干扰
- `乐丨青春`：歌词/画面/卡点/情绪结合

只学习：
- 光感；
- 色彩；
- 人物/环境比例；
- 治愈感；
- 镜头呼吸；
- 视觉记忆点。

禁止复制具体人物、具体构图、具体作品/IP。

### First test set
从锁定歌曲选 3 个代表 Beat：
1. `HOOK`
2. `EMOTION/HOLD`
3. `RELEASE`

每 Beat 只生成少量候选首帧，验证两条视觉支柱：
- A `自然治愈 / 风景沉浸`
- B `人物治愈 / 轻梦幻`

不是每个 Beat 都做 A/B 对比；只在真正有歧义的 Beat 做双路线。

### Visual target
优先升级：
- natural light / backlight / dappled light；
- clean palette；
- bright but not plastic；
- healing > spectacle；
- light fantasy > heavy fantasy；
- character as emotional vessel；
- environment retains large share of frame；
- visual should still be dynamically executable in 5s.

### Dynamic mini test
首帧通过后，只挑 2–3 个 Beat 做 5s 动态：
- 1-shot breathing sample；
- 2-shot common sample；
- 3-shot task-specific sample（仅需要时）。

检查：
- image quality retention；
- character stability；
- motion elegance；
- healing feeling；
- Atom/Arc edit value。

### Human Gate
只做一次 `R3-B VISUAL CALIBRATION GATE`：看整组代表性静帧 + 少量动态小样。

### PASS
用户能明确判断：
- 相比 R2 画质/治愈感有提升；
- 不是单纯更艳/更AI；
- 动态仍稳定可生产；
- 至少一条视觉支柱可晋升到 R3 full MV。

如果不 PASS：只继续 R3-B，不进入整片。

---

## R3-C｜Full MV Integration Test

回答：
**Music Radar 选出的歌 + 新治愈视觉语言，能不能无缝跑进 R2 已锁的完整生产链？**

这是 R3 第一次完整 MV。

### Variable policy
新变量只有：
- 已验证的 Music Radar 选歌；
- R3-B 已通过的视觉语言。

以下保持 R2 baseline：
- Stage 2 Audio lock；
- Stage 2A Timeline Package；
- Natural Beat；
- 1–3 shot source logic；
- W07 QA；
- W07.5 Atom/Arc；
- long-cut Picture Edit；
- subtitle baseline；
- Final QA。

### Human Gates
恢复正式 5-Gate 模型：
1. song（R3-A 已完成）
2. BGM excerpt
3. first-frame set
4. Picture Edit
5. Final

R3-B 视觉小样 Gate 属于研发期额外 Gate，只在 R3 校准期间存在；视觉系统晋升后取消。

### PASS
- 不出现 R2 已修复问题回归；
- 第一次 Picture rough edit 就基于 Atom/Arc；
- 不做字幕风格重选；
- 治愈视觉明显优于 R2 baseline；
- 生产成本仍可接受；
- 用户技术问题反馈次数显著下降。

---

## R3-D｜Publish Packaging Calibration

回答：
**我们能不能建立稳定的“音推发布包装”，而不是每次成片后临时想标题、简介、标签？**

主要新变量：发布层。

### Benchmark roles
重点学习：
- 火乐乐：歌曲推荐表达 / 信息型包装
- 泡泡与茶：歌名/翻唱兴趣入口
- 黑米与糖豆：新歌/原创/CTA/完整歌表达
- 乐丨青春 / XIANGJISHI：短视觉标题和情绪词
- Aura：低文字干扰、视觉第一

### Required packaging set
每条完整 MV 产出：
1. `COVER_TEXT`
2. `POST_TITLE`
3. `POST_DESCRIPTION`
4. `HASHTAGS`
5. `PINNED_COMMENT`（需要时）

### Default roles
- 视频内部：克制、情绪/歌词优先；
- 标题：情绪钩子 + 歌名/识别信息；
- 简介：歌名/歌手/一句推荐理由/情绪；
- 标签：先音乐搜索，再治愈/氛围，再 AI；AI 不抢第一身份。

### Test method
先不做复杂多变量 A/B。
第一阶段只建立 2 个包装方向：
- `MUSIC_FIRST`：音乐推荐清晰度优先
- `EMOTION_FIRST`：情绪/氛围吸引优先

每次只选一个实际发布，另一个作为记录候选，不同时发重复视频。

### PASS
连续多条数据后再晋升，不凭单条热视频下结论。

---

# 2. Promotion policy

每一轮测试结果分：
- `EXPERIMENTAL`
- `POSITIVE_EVIDENCE`
- `VALIDATED`
- `PROMOTED_TO_RUNTIME`

新规则至少满足：
1. 有明确对照/失败或正证据；
2. 能解释为什么有效；
3. 不与 R2 correctness baseline 冲突；
4. 经用户实际观看/发布反馈；
5. 只有重复验证后才晋升正式 Rule。

视觉偏好不能因为一轮好看就变成硬规则；优先存 Benchmark/Knowledge，成熟后再晋升。

---

# 3. R3 success definition

R3 不是一次测试全部完成。

阶段性成功：
- R3-A PASS：我们有自己的 7-Day Music Radar；
- R3-B PASS：有一套比 R2 更高级、仍可稳定动态化的治愈视觉语言；
- R3-C PASS：新选歌 + 新视觉能稳定跑完全链；
- R3-D PASS：发布标题/简介/标签开始形成可复制模板。

最终 R3 成功：
`trend discovery -> song selection -> healing AI visual MV -> publish packaging -> data feedback`
形成闭环，同时 R2 correctness pipeline 无回归。

---

# 4. Immediate next action

**只执行 R3-A，不提前做 R3-B/C/D。**

第一步：建立 Benchmark Account Registry + 7-Day Music Radar 数据结构，补充头部音推账号，抓取/记录最近7天重复歌曲，再交付第一版 shortlist 给 HG01。
