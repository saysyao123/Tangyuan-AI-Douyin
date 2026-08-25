# Rules｜MV Editing Runtime Contract v1.2

> Status: `ACTIVE / WEB_R2_VALIDATED / WEB_ROUGH_CUT_GATE_PROMOTED`
> Role: MV 后期剪辑的独立运行规则。主 Workflow 只定义阶段与 Gate；本文件负责可复用的 Picture Edit / 网页端预览 / Fragmentation / 字幕实现接口。
> Evidence base: WEB R2 V1/V2 timing failures + V3 fragmented-cut feedback + V3.1 long-cut improvement + W07.5/V3.2 source normalization + WEB watermark rough-cut validation + W09 subtitle geometry calibration.

---

## 1. Entry contract｜HARD

进入 Picture Edit 前必须已经存在并通过：
- `BGM_LOCKED`
- `AUDIO_TIMELINE_PACKAGE_LOCKED`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
- `SHOT_LIBRARY_READY`（需要 Atom/Arc 时）
- **`WEB_SOURCE_ROUGH_CUT_GATE_PASS`（WEB 环境 HARD）**
- `EDITOR_AUDIO_GATE_PASS`

WEB 权威粗剪规则：`rules/mv_web_source_roughcut.md`。

编辑器只加载：
`line_timeline.csv + anchor_words.csv + music_events.csv + VISUAL_SOURCE_MAP + clean WEB proxy / normalized Shot Library`。

禁止：
- 在剪辑阶段重新猜歌词时间；
- 根据画面倒推字幕；
- 临时生成第二套 lyric clock；
- 把带角落平台生成标记的 raw WEB source 直接塞进正式 Picture Preview；
- 把水印安全处理拖到 HG04 之后或 Final Polish。

---

## 2. Three-clock model｜HARD

最终 Edit Map 同时协调三只时钟：
1. Lyric Clock：歌词行、Anchor Word；
2. Music-event Clock：pickup / onset / release / peak / tail；
3. Visual-action Clock：素材内部动作、切镜、可用 in/out。

优先级：
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`。

**Anchor Word 不等于 Cut Point。**
优先让一个已经进入的镜头内部动作命中 Anchor，而不是每个 Anchor 都换素材。

---

## 3. Long-cut first｜DEFAULT

抒情 / 诗意 / 情绪型 MV 默认采用：
`long-cut first / semantic-hit inside shot`。

目标不是减少所有镜头，而是减少“后期外部切换”。

默认建议：
- 35–40s 成片：约 `8–12` 个外部素材段；
- 单个外部段通常 `2.5–5.0s`；
- 连续 `<2.0s` 的外部段默认视为 Fragmentation Risk；
- 最终 release / tail 尽量保留 `3.5–5.0s` 连续镜头；
- 同一歌词行原则上不主动换场超过 1 次，除非是明确的高潮 / 发现 / 对比结构；
- 禁止短距离 `A -> B -> A` 回切，除非有明确叙事意义。

这些是默认剪辑约束，不是机械配额；强节奏歌曲可以提高密度，但必须由音乐/导演任务证明。

---

## 4. Fragmentation Gate｜HARD QA

Edit Map 锁定前检查：
- 外部 fragment 数是否过多；
- 是否出现多个连续 <2s 片段；
- 是否把每个歌词 start / Anchor 都误处理成 cut；
- 是否频繁 A-B-A 回切；
- 源视频自身已有内部切镜时，后期是否又重复加切；
- 是否存在“技术上每刀都对、整体观看却忙乱”的情况。

若命中以上问题：
优先合并外部段、保留素材内部动作完整性，而不是继续增加转场。

---

## 5. Dynamic-source interface｜生成素材必须为剪辑服务

动态视频不是最终成片，它是可剪素材源。

### Preferred source portfolio
默认整组采用混合结构，而不是全多镜或全一镜：
- `1-shot / one-take`：空间、呼吸、情绪持续、结尾 release；
- `2-shot`：建立 -> 事件 / 细节 -> 情绪；
- `3-shot`：发现、高潮、明确 setup -> event -> aftermath；
- `>3-shot`：只用于真正需要高能量的 hook / peak，不能成为默认。

对当前 5s Seedance 类生产，**默认优先 1–2 镜，3 镜只在语义任务需要时使用**。

原因：如果每条 5s 原始视频自身已经有 3–5 次内部切镜，而最终又使用 8–12 个外部段，真实观看镜头数会再次膨胀，重现 V3 的碎片感。

### Edit-friendly source contract
每条动态素材尽量提供：
- 唯一主视觉事件；
- 清晰的动作开始 -> 发展 -> 结束；
- 可识别的 clean in / clean out；
- 若有内部切镜，切镜必须承担不同叙事任务，不得只是换景别；
- 避免 0.5–0.8s 的无意义 micro-shot；
- 5s 内 2 镜时优先让每镜有足够完整动作；
- 5s 内 3 镜时必须有明确 setup / event / aftermath；
- 结尾留下可延续的物理余韵，便于后期长持有。

Director 在 Stage 4/6 应同时考虑：
`lyric task + generation stability + final edit value`。

---

## 6. VISUAL_SOURCE_MAP｜HARD OUTPUT

W07 不只写“PASS/FAIL”，必须给编辑器可执行素材地图：
- source clip id；
- fps / duration；
- clean window(s)；
- internal cut / action event approximate frame or time；
- topology / face / fabric / physics risk window；
- recommended role：`HOLD / BRIDGE / HIT / PEAK / RELEASE`；
- `PASS_FULL / TRIM_REQUIRED / REGEN_WATCH / REGENERATE`。

后期优先使用完整 clean arc，不应该每次重新人工猜素材里哪一段可用。

---

## 7. WEB Source Rough-Cut Gate｜HARD / WEB ONLY

权威：`rules/mv_web_source_roughcut.md`。

> R2 已验证：水印/平台生成标记不能作为 Final Polish TODO；必须在正式 Picture Edit 前，将 raw source 非破坏性派生为 clean WEB proxy。

### Default WEB geometry baseline
对于 720×1280 Doubao/Seedance 角落生成标记，R2 已验证：

`crop=576:1024:72:128 -> scale=720:1280`

等效约 `1.25×` whole-source zoom。

要求：
- 同一批素材使用同一 crop/zoom；
- 原始素材不覆盖；
- source audio 物理移除；
- 输出 `720×1280 / SAR=1:1 / 9:16`；
- 禁止逐镜移动画面追水印；
- 禁止局部模糊/贴片作为默认方案；
- 以整批最危险左上 / 右下帧做 corner-risk QA；
- 不允许 mixed state：部分镜头干净、部分仍有平台标记。

新批次先用 R2 1.25× baseline；若水印位置更极端，只能整批统一扩大安全 crop。若统一裁切明显破坏核心构图，触发 `ROUGH_CUT_GEOMETRY_EXCEPTION`，不得静默进入 Picture Edit。

Required outputs：
- `WEB_SOURCE_ROUGH_CUT_MAP.csv`
- `WEB_SOURCE_ROUGH_CUT_QA.md`

Gate：
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`。

---

## 8. Picture-edit workflow

1. Load locked Audio Timeline Package.
2. Load VISUAL_SOURCE_MAP / normalized Shot Library as needed.
3. **确认 WEB_SOURCE_ROUGH_CUT_GATE_PASS；只加载 clean WEB proxy。**
4. 先按 Natural Beat / emotion 构建“大段”，不要先按歌词行机械切片。
5. 对每个大段选择最完整的视觉动作 arc。
6. Anchor Word 优先通过镜头内部动作命中。
7. Music event 决定必要的换场、峰值和 release。
8. 执行 Fragmentation Gate。
9. Render `Picture + locked BGM` Preview。
10. Audio implementation QA：确认没有新全局 lag。
11. Visual technical QA：再次抽查角落标记一致性 / SAR / 拉伸 / risk frames。
12. Human `HG04 Picture Edit Rhythm Gate`。

只有通过后：
`EDIT_PREVIEW_QA_PASS = YES`。

如果 HG04 之后发现“只是 WEB 粗剪 Gate 漏做/几何实现错误”：
- 用同一 EDL 替换成 clean proxy 重渲染；
- 不自动重开导演/动态生成；
- 只有统一 crop 实质改变构图/节奏时才重开 HG04。

---

## 9. Subtitle workflow｜AFTER picture rhythm is stable

歌词 timing 在 Stage 2A 已锁；这里不重新对齐。

### Alignment-check preview
当需要用户确认“字幕是否早/晚”时：
- 直接使用 `lyrics_exact.srt`；
- 测试版可暂时关闭淡入淡出，避免 80–150ms fade 造成主观延迟错觉；
- 以 frame quantization 记录实际烧录误差；
- 不手动 nudge 单句来迎合画面切点。

### Style optimization
时间确认后再进行字幕视觉优化：
- 字体 / 字号；
- 字幕底框；
- padding；
- 水平 + 垂直居中；
- safe area；
- 长句换行；
- restrained fade；
- 与画面亮暗的可读性。

### Subtitle-box geometry｜HARD

当字幕采用“紧贴文字的半透明圆角底框”时：
- **底框必须从该句字幕实际渲染后的 glyph/text pixel bounding box 重新生成**；
- 禁止通过“把上一版圆角路径整体内收/外扩 N px”来改变 padding；圆角路径含控制点，几何缩放容易产生非对称框；
- 禁止仅用 `字符数 × 字号` 估算框宽；必须基于实际渲染字形；
- 当前 R1-derived WEB 基线 padding：`10px`，四边一致；
- 单行与双行字幕使用同一 bbox→padding 算法；
- 自动 QA：`left/right/top/bottom padding = target ±1px`；
- 自动 QA：`text bbox center` 与 `box bbox center` 的 x/y 偏差均 `<=1px`；
- 短句必须作为专项 QA 样本，因为短框最容易放大非对称误差；
- 修改 padding 时必须**从文字 bbox 重建底框**，不得修改旧框坐标后复用。

WEB R2 证据：`好吧哎哟哎哟` 为短句，旧版 22→10px 通过旧圆角路径坐标内收后产生明显视觉偏心；重建 bbox 后消除。该问题属于实现错误，不允许单句手工特判作为最终解决方案。

顺序固定：
`timing truth -> implementation check -> style optimization -> geometry QA -> implementation re-check`。

---

## 10. Final reusable defaults from WEB R2/R3

- 先锁音频，再做任何依赖时长的导演生产；
- 图片/视频素材为剪辑服务，不按“5s就是最终5s”理解；
- 1–2镜是常用基础资产，3镜是任务型资产，密集多镜是少数高潮资产；
- 外部剪辑长镜头优先；
- Anchor 命中不等于换镜头；
- W07 必须产出可执行 VISUAL_SOURCE_MAP；
- **WEB 正式 Picture Edit 前必须先过 Source Rough-Cut Gate；**
- R2 WEB baseline：统一 1.25× whole-source crop/zoom + corner-risk QA；
- 水印处理不得拖到 HG04 后；
- 字幕先验证 timing，再优化 style；
- 字幕底框必须由实际 glyph bbox 重建，并通过四边 padding / 中心误差自动 QA；
- 用户指出的同类问题必须升级成规则/Gate，而不是只修当前视频。
