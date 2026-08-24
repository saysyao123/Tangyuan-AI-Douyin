# Rules｜MV Editing Runtime Contract v1.0

> Status: `ACTIVE / WEB_R2_VALIDATED`
> Role: MV 后期剪辑的独立运行规则。主 Workflow 只定义阶段与 Gate；本文件负责可复用的 Picture Edit / 网页端预览 / Fragmentation / 字幕实现接口。
> Evidence base: WEB R2 V1/V2 timing failures + V3 fragmented-cut feedback + V3.1 long-cut improvement.

---

## 1. Entry contract｜HARD

进入 Picture Edit 前必须已经存在并通过：
- `BGM_LOCKED`
- `AUDIO_TIMELINE_PACKAGE_LOCKED`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
- `EDITOR_AUDIO_GATE_PASS`

编辑器只加载：
`line_timeline.csv + anchor_words.csv + music_events.csv + VISUAL_SOURCE_MAP`。

禁止在剪辑阶段重新猜歌词时间、根据画面倒推字幕、临时生成第二套 lyric clock。

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
- topology / face / fabric risk window；
- recommended role：`HOLD / BRIDGE / HIT / PEAK / RELEASE`；
- `PASS_FULL / TRIM_REQUIRED / REGEN_WATCH / REGENERATE`。

后期优先使用完整 clean arc，不应该每次重新人工猜素材里哪一段可用。

---

## 7. Web preview watermark fallback｜WEB ONLY

> 这是网页端当前能力限制下的临时 Preview 策略，不替代 Codex / publish-grade 无水印源处理。

当网页端回传 Seedance/平台素材左上角或右下角存在生成标记时：
- 默认采用**整条素材统一放大 + 固定裁切**，而不是每镜单独移动/局部遮盖；
- 同一批素材使用同一几何变换，避免构图跳动；
- 先以整批最严重水印位置确定安全 crop/zoom，再统一应用；
- 不允许出现部分镜头去掉、部分镜头漏出的混合状态；
- Preview 输出强制 `SAR=1:1`，保持 9:16，不得因裁切导致拉伸；
- 渲染后必须抽查至少：第一段、左上角最危险帧、右下角最危险帧、最后一段；
- 只要仍有一处水印残留，就继续增加统一放大/安全裁切，不把问题交给用户发现。

优先级：
`无水印 HD 原源 > Codex 精确处理 > WEB 统一放大裁切 fallback`。

---

## 8. Picture-edit workflow

1. Load locked Audio Timeline Package.
2. Load VISUAL_SOURCE_MAP.
3. 先按 Natural Beat / emotion 构建“大段”，不要先按歌词行机械切片。
4. 对每个大段选择最完整的视觉动作 arc。
5. Anchor Word 优先通过镜头内部动作命中。
6. Music event 决定必要的换场、峰值和 release。
7. 执行 Fragmentation Gate。
8. 应用网页端统一 watermark-safe crop（如果当前环境需要）。
9. Render `Picture + locked BGM` Preview。
10. Audio implementation QA：确认没有新全局 lag。
11. Human viewing Gate。

只有通过后：
`EDIT_PREVIEW_QA_PASS = YES`。

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

顺序固定：
`timing truth -> implementation check -> style optimization -> implementation re-check`。

---

## 10. Final reusable defaults from WEB R2

- 先锁音频，再做任何依赖时长的导演生产；
- 图片/视频素材为剪辑服务，不按“5s就是最终5s”理解；
- 1–2镜是常用基础资产，3镜是任务型资产，密集多镜是少数高潮资产；
- 外部剪辑长镜头优先；
- Anchor 命中不等于换镜头；
- W07 必须产出可执行 VISUAL_SOURCE_MAP；
- WEB Preview 当前统一放大裁水印；
- 字幕先验证 timing，再优化 style；
- 用户指出的同类问题必须升级成规则/Gate，而不是只修当前视频。
