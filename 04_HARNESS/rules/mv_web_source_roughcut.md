# Rules｜WEB MV Source Rough-Cut Gate v1.0

> Status: `ACTIVE / WEB_R2_VALIDATED / WEB HARD GATE`
> Role: 网页端在 Dynamic Source QA 之后、正式 Picture Edit 之前，对所有可用 AI 视频源执行非破坏性素材粗剪、去源音轨、统一水印安全裁切与角落风险 QA。
> Evidence: WEB R2 W07.5 / V3.2 atomic rough cut + Editing Runtime Retrofit。

---

## 1. Why this Gate exists｜HARD

WEB R2 已验证：如果把水印处理留到 Picture Edit / Final Polish，容易出现：
- 一部分镜头已去标记、一部分漏角；
- 每镜单独裁切导致构图跳动；
- 左上安全但右下仍残留，或反之；
- Picture Rhythm 已通过后才发现必须改几何，造成无意义返工。

因此 WEB 路径固定：

`Dynamic Source QA`
→ `Shot/Arc Normalization（需要时）`
→ **`WEB SOURCE ROUGH-CUT GATE`**
→ `Editor Audio Gate`
→ `Picture Edit`

本 Gate 是网页端技术 Gate，不增加固定人工 Gate 数量。

---

## 2. Source preservation｜HARD

- 原始 AI 生成 5s/原文件永久保留，不覆盖；
- 粗剪只生成 derived WEB proxy；
- proxy 必须可由 Source Map / Rough-Cut Map 重建；
- 所有 AI source audio 在 proxy 层物理移除；
- 锁定 BGM 仍是唯一 production music truth。

---

## 3. Rough-cut work｜HARD

对所有 `PASS_FULL` / `TRIM_REQUIRED` / 可编辑 source：

1. 根据 `VISUAL_SOURCE_MAP` / internal-cut map 确认 clean window；
2. 多镜素材按真实内部 CUT 派生 Atom/Arc；
3. topology / face / hand / fabric / physics risk window 不进入主 proxy；
4. 不在人物动作中途无理由截断；优先保留完整 action arc；
5. `<0.8s` 无独立语义 micro-shot 默认拒绝；
6. duplicate / meaningless transition 默认拒绝；
7. 输出可直接进入 Picture Edit 的 clean proxy，而不是让编辑阶段重新猜 source 结构。

核心：
`RAW SOURCE != EDIT SOURCE`。

---

## 4. WEB watermark-safe geometry｜HARD

### R2 validated baseline for 720×1280 Doubao/Seedance corner marks

统一使用：

`crop=576:1024:72:128 -> scale=720:1280`

等效视觉：约 `1.25×` whole-source zoom。

含义：
- 从 720×1280 源中取中间 576×1024；
- x=72, y=128；
- 再缩放回 720×1280；
- 强制 `SAR=1:1`；
- 保持 9:16，不拉伸。

### Batch rule

- 同一批 WEB proxy 默认使用**同一个 crop/zoom 几何**；
- 禁止每镜单独移动画面去追水印；
- 禁止局部贴片/模糊遮挡作为默认方案；
- 禁止出现 mixed state：部分镜头干净、部分镜头仍有平台生成标记。

### New-batch calibration

1. 先检查整批左上 / 右下最严重风险帧；
2. R2 baseline `1.25×` 先作为 WEB 默认起点；
3. 若当前批水印位置更极端，只允许**整批统一**增加安全 crop；
4. 若统一裁切会严重伤害已批准构图，标记 `ROUGH_CUT_GEOMETRY_EXCEPTION`，再寻找更干净 source/take；不得静默交给用户发现。

---

## 5. Mandatory corner-risk QA｜HARD

粗剪 proxy 渲染后，至少检查：
- 第一段代表帧；
- 左上角最危险 source / frame；
- 右下角最危险 source / frame；
- 中间至少一个近景人物镜头；
- 最后一段 / release 镜头。

PASS 条件：
- `NO_VISIBLE_GENERATOR_MARK = YES`；
- 左上/右下均无遗漏；
- batch geometry 一致；
- 9:16；
- `SAR=1:1`；
- 无拉伸；
- 主体没有被统一 crop 破坏到不可用；
- source audio 已移除；
- clean window / risk window 继承正确。

只要任一可见平台生成标记残留：
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = NO`。

---

## 6. Required artifacts

至少保存：

### `WEB_SOURCE_ROUGH_CUT_MAP.csv`
字段建议：
- source_id
- source_file
- source_in / source_out
- internal_cut_note
- risk_trim_note
- proxy_file
- crop_w / crop_h / crop_x / crop_y
- output_w / output_h
- SAR
- source_audio_removed
- watermark_left_top_pass
- watermark_right_bottom_pass
- status

### `WEB_SOURCE_ROUGH_CUT_QA.md`
记录：
- batch crop profile；
- worst-case corner samples；
- watermarks PASS/FAIL；
- geometry / composition exceptions；
- rejected risk windows；
- proxy identity/hash when available。

Gate state：
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`。

---

## 7. Picture Edit entry contract｜HARD FOR WEB

网页端进入正式 Picture Edit 前必须同时存在：
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
- `SHOT_LIBRARY_READY`（需要 Atom/Arc 时）
- **`WEB_SOURCE_ROUGH_CUT_GATE_PASS`**
- `EDITOR_AUDIO_GATE_PASS`

Picture Edit 只能优先使用已通过本 Gate 的 clean WEB proxy / Atom / Arc，不直接把带角落水印的 raw source 塞进正式 Preview。

---

## 8. Human Gate boundary

本 Gate 默认自动完成，不要求用户承担技术验收。

只有以下异常才提示：
- 1.25× 或全批统一安全 crop 明显破坏核心构图；
- clean duration 因 risk trim 不足以承担歌词；
- 唯一可用 source 的标记位置无法通过统一裁切安全移除。

正常情况下用户看到的 HG04 Picture Preview 应该已经完成 WEB 粗剪与水印安全处理。

---

## 9. Patch, Don't Cascade

- 水印漏角 / proxy 几何错误 → 只回本 Gate；
- 不重新生成首帧/动态；
- 不重新打开已锁 Audio Timeline；
- 不改变 Picture timing，除非 rough trim 证明 clean duration 不足；
- HG04 已通过但发现遗漏本 Gate 时：补做粗剪 proxy + 用同一 EDL 重渲染，并做节奏回归；只有构图/节奏实质变化才重开 HG04。

---

## 10. R2 evidence

WEB R2 已验证 normalized proxy：
- 24fps / 720×1280 / SAR 1:1；
- source audio removed；
- `crop=576:1024:72:128 -> scale=720:1280`；
- equivalent visual zoom `1.25×`；
- representative contact-sheet review 未见左上/右下 generator mark。

这条规则属于 WEB 环境明确生产纪律，不再作为“最后润色时记得处理”的 TODO。