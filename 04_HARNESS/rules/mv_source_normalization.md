# Rules｜MV Source Normalization v1.1

> Status: `ACTIVE / WEB_R2_VALIDATED`
> Role: 在 Dynamic Source QA 与 Picture Edit 之间，将 AI 返回的 1–3 镜复杂视频非破坏性整理为可执行的 Atom/Arc 素材库；网页端同时必须完成独立 `WEB SOURCE ROUGH-CUT GATE`。
> Evidence: WEB R2 V3.1 showed that `9 external fragments` could still contain ~18 perceptible shots because generated sources carried hidden internal cuts. V3.2 validates explicit atomization before final edit. WEB R2 also validates batch-uniform watermark-safe rough-cut proxies before Picture Edit.

---

## 1. Core principle｜HARD

AI 生成的 5s 视频是 `RAW SOURCE`，不是最终剪辑单元。

W07 之后必须保留：
1. 原始完整视频；
2. 内部真实切镜 / 动作事件地图；
3. 可独立使用的单镜头 `ATOM`；
4. 只有在内部剪辑语法确实有导演价值时，才保留完整 `ARC`。

禁止为了“整理素材”破坏或覆盖原始 5s 文件。

网页端额外 HARD：
- 无论 source 是一镜到底还是多镜，只要要进入正式 WEB Picture Edit，都必须先通过 `rules/mv_web_source_roughcut.md`；
- Atom/Arc normalization 可以按 source complexity 条件执行，但 WEB 水印安全粗剪 Gate 不可因“该 source 只有一镜”而跳过。

---

## 2. Atom vs Arc

### ATOM
单一视觉状态 / 单一连续镜头，可被最终编辑器独立使用。

每个 Atom 必须记录：
- source id；
- source start/end frame；
- duration；
- visual description；
- role: `SETUP / HOLD / BRIDGE / HIT / PEAK / AFTERMATH / RELEASE`；
- QA status；
- derived proxy hash when rendered.

### ARC
由 2–3 个内部镜头组成，但它们共同完成一个明确结构，例如：
- setup -> event -> aftermath；
- person -> bird -> person；
- dance build -> peak -> settle。

只有当内部切镜承担不同导演任务时，Arc 才可以进入主素材库。
若只是随机换景别 / micro-shot / 重复镜头，则拆成 Atom 或直接拒绝。

---

## 3. Reject rules｜HARD

以下单元默认不进入主 Atom 池：
- topology / face / hand / fabric / obvious physics risk；
- 与相邻镜头高度重复；
- 没有独立语义价值的 `<0.8s` micro-shot；
- 只承担生成模型随机过渡、不承担导演任务的镜头；
- 不能形成 clean in / clean out 的破碎区间。

短镜头若只对一个已验证 Arc 有价值，可以保留在 Arc 中，但不得冒充独立 Atom。

---

## 4. WEB source rough-cut / preview proxy normalization｜HARD FOR WEB

权威：`rules/mv_web_source_roughcut.md`。

当网页端素材带角落平台生成标记：
- 在 Picture Edit **之前**的 source rough-cut 层统一处理，而不是最终时间线逐段修；
- 整批使用同一 crop/zoom；
- source audio 全部移除；
- 输出统一 fps / resolution / SAR；
- 原始视频保持不变；
- 必须做 batch corner-risk QA；
- Gate：`WEB_SOURCE_ROUGH_CUT_GATE_PASS`。

WEB R2 已验证 baseline：
`720×1280 -> crop 576×1024 at x=72,y=128 -> scale 720×1280 -> SAR 1:1`
即约 `1.25×` whole-source zoom。

对应 FFmpeg geometry：
`crop=576:1024:72:128 -> scale=720:1280`。

使用纪律：
- 新批次先以 R2 1.25× baseline 测试；
- 抽查整批最严重左上 / 右下风险帧；
- 若仍残留，只能整批统一增加安全 crop；
- 禁止局部遮盖 / 每镜单独平移作为默认网页端方案；
- 如果统一 crop 严重破坏核心构图，进入 `ROUGH_CUT_GEOMETRY_EXCEPTION`，不得静默进入 Picture Edit。

---

## 5. Mandatory outputs

### Normalization output（需要 Atom/Arc 时）
`NORMALIZED_SHOT_LIBRARY_MAP.csv`

最低字段：
- `unit_id`
- `kind = ATOM / ARC`
- `source`
- `start_frame`
- `end_frame`
- `duration_s`
- `visual`
- `role`
- `status`
- `note`
- derived proxy identity/hash when applicable

Gate：
`SHOT_LIBRARY_READY = YES`。

### WEB rough-cut output（所有 WEB edit source）
必须额外产出：
- `WEB_SOURCE_ROUGH_CUT_MAP.csv`
- `WEB_SOURCE_ROUGH_CUT_QA.md`

Gate：
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`。

未通过 WEB Gate 时，正式 Picture Edit Preview 不得使用带角落生成标记的 raw source。

---

## 6. Final editor behavior

Picture Edit 默认优先选择已通过 WEB Rough-Cut Gate 的 Atom / Arc / clean one-take proxy。

Arc 只有在以下情况优先：
- 内部切镜本身已经精确承担 lyric/music/visual task；
- 完整 Arc 比拆开使用更自然；
- 不会让整片 perceptible shot count 重新膨胀。

最终 Fragmentation QA 必须统计两种数量：
1. timeline external fragment count；
2. perceptible visible-shot count（包括 Arc 内部镜头）。

**只看 external fragment 数不足以判断是否碎。**

---

## 7. Recommended chain

`1–3 shot / one-take generation`
→ `W07 source QA + internal-cut/risk map`
→ `non-destructive Atom/Arc normalization（按需要）`
→ `SHOT_LIBRARY_READY（按需要）`
→ **`WEB SOURCE ROUGH-CUT GATE`**
→ `WEB_SOURCE_ROUGH_CUT_GATE_PASS`
→ `Editor Audio Gate`
→ `Picture Edit`
→ `Fragmentation QA by visible-shot count`
→ `Picture Preview / HG04`

This layer improves edit control without forcing all future dynamic prompts to become one-take videos, and prevents WEB watermark handling from being deferred until final polish.