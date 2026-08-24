# Rules｜MV Source Normalization v1.0

> Status: `ACTIVE / WEB_R2_VALIDATED`
> Role: 在 Dynamic Source QA 与 Picture Edit 之间，将 AI 返回的 1–3 镜复杂视频非破坏性整理为可执行的 Atom/Arc 素材库。
> Evidence: WEB R2 V3.1 showed that `9 external fragments` could still contain ~18 perceptible shots because generated sources carried hidden internal cuts. V3.2 validates explicit atomization before final edit.

---

## 1. Core principle｜HARD

AI 生成的 5s 视频是 `RAW SOURCE`，不是最终剪辑单元。

W07 之后必须保留：
1. 原始完整视频；
2. 内部真实切镜 / 动作事件地图；
3. 可独立使用的单镜头 `ATOM`；
4. 只有在内部剪辑语法确实有导演价值时，才保留完整 `ARC`。

禁止为了“整理素材”破坏或覆盖原始 5s 文件。

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
- topology / face / hand / fabric risk；
- 与相邻镜头高度重复；
- 没有独立语义价值的 `<0.8s` micro-shot；
- 只承担生成模型随机过渡、不承担导演任务的镜头；
- 不能形成 clean in / clean out 的破碎区间。

短镜头若只对一个已验证 Arc 有价值，可以保留在 Arc 中，但不得冒充独立 Atom。

---

## 4. WEB preview proxy normalization

当网页端素材带角落平台标记：
- 统一在 Normalization 层处理，而不是最终时间线逐段修；
- 整批使用同一 crop/zoom；
- source audio 全部移除；
- 输出统一 fps / resolution / SAR；
- 原始视频保持不变。

WEB R2 当前验证 fallback：
`720×1280 -> crop 576×1024 at x=72,y=128 -> scale 720×1280 -> SAR 1:1`
即约 `1.25×` 整体放大。

这不是跨模型永久固定数值。新一批素材应先检查最严重的左上 / 右下水印，再确定全批次安全参数。

---

## 5. Mandatory output

Normalization 完成后必须产出：
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

Gate state：
`SHOT_LIBRARY_READY = YES`

未形成可执行 Shot Library 时，最终 Picture Edit 不应直接拿复杂 1–3 镜原片现场重新猜内部结构。

---

## 6. Final editor behavior

Picture Edit 默认优先选择 Atom。

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

`1–3 shot generation`
→ `W07 source QA + internal-cut map`
→ `non-destructive Atom/Arc normalization`
→ `SHOT_LIBRARY_READY`
→ `Editor Audio Gate`
→ `Picture Edit`
→ `Fragmentation QA by visible-shot count`
→ `Picture Preview`

This layer improves edit control without forcing all future dynamic prompts to become one-take videos.