# Rules｜MV Subtitle Runtime Contract v1.0

> Status: `ACTIVE / R1_GOLDEN + WEB_R2_VALIDATED`
> Role: MV 字幕视觉、实现与 QA 的独立运行规则。
> Authority: R1 实际用户接受截图 + WEB R2 W09 校准结果。
> Principle: **字幕时间属于 Audio Timeline Package；字幕样式属于本规则。不得把两者重新混在一起。**

---

## 1. Entry contract｜HARD

进入字幕阶段前必须已经通过：
- `AUDIO_TIMELINE_PACKAGE_LOCKED`
- `EDIT_MAP_LOCKED`
- `EDIT_PREVIEW_QA_PASS`

唯一 timing source：
`AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt` / canonical line timeline。

禁止：
- 根据画面切点重新猜字幕时间；
- 为了“看着卡点”手工 nudge 某一句；
- 再跑一套自由 ASR 生成第二套 lyric clock；
- 在样式阶段修改歌词文本顺序。

---

## 2. Default visual baseline｜LOCKED

除非用户明确要求新的字幕风格，后续 MV **默认直接复用本标准，不再每首歌重新做 A/B/C 风格探索**。

### 720×1280 reference geometry

- 字体：干净粗体中文无衬线；WEB reference：`Noto Sans CJK SC Bold`
- nominal font size：`46px`
- 文字：near-white，R1/WEB reference `#F8F8F8` family
- 轻微深色描边：约 `1px`
- 对齐：水平居中
- subtitle center：约 `x=360 / y=1009`
- 最大行数：`2`
- 默认单句展示，不做重复歌词层
- fade in：`100ms`
- fade out：`180ms`
- 默认不做 karaoke / 逐字高亮 / 英文装饰 / 小字说明

### Background box

- dark semi-transparent rounded rectangle
- reference color：`#383838` family
- WEB ASS alpha reference：`H55`
- 参考圆角半径：约 `8px`（720×1280）
- **padding：top / bottom / left / right = 10px**
- 文字必须在框内上下左右视觉与几何居中

不同分辨率时按画布比例缩放 nominal size / position / padding / radius；不得把 720p 数值原样机械套到 1080p/4K。

---

## 3. Box generation algorithm｜HARD

当使用“紧贴文字的圆角底框”时：

1. 先用最终字体 / 字号 / 行数 / 换行实际渲染该句字幕；
2. 获取实际 rendered glyph/text pixel bounding box；
3. 从该 bbox **重新生成** rounded rectangle；
4. 四边分别增加目标 padding；
5. text bbox center 与 box bbox center 必须一致；
6. 每一句都重新计算，不复用上一句或上一版本的旧框路径。

禁止：
- `字符数 × 字号` 估算框宽；
- 对旧 rounded path 做 inset / outset / scale 来改变 padding；
- 只改左右、不改上下的非等边距临时修补；
- 因某一句短字幕歪了就做单句手工偏移特判。

WEB R2 已验证：旧圆角路径从 22px 内收到 10px 时，控制点变换会导致短句明显偏心；正确解法是从当前 glyph bbox 全量重建。

---

## 4. Long-line wrapping｜DEFAULT

- 默认一行；
- 超过安全宽度时最多两行；
- 换行按语义短语优先，不在词义中间强拆；
- 两行共同计算一个整体 text bbox，再统一加 10px padding；
- 两行整体中心仍保持在字幕基准中心附近；
- 不允许第二行把底框挤出安全区。

---

## 5. Fixed Subtitle QA Gate｜HARD

每次 MV 字幕必须经过以下固定审核，不再依赖用户来发现基础实现问题。

### A. Timing implementation QA

逐行比对 rendered subtitle event 与 canonical SRT / line timeline：
- 文本完全一致；
- 顺序一致；
- start/end implementation delta 应仅来自 renderer/timebase quantization；
- 720p/24fps 基线：不得超过 1 frame；
- 若出现系统性 global lag，必须阻断，不允许手工逐句补偿。

### B. Geometry QA｜ALL LINES

每一句自动检查：
- left padding = target `±1px`
- right padding = target `±1px`
- top padding = target `±1px`
- bottom padding = target `±1px`
- text bbox center vs box bbox center x error `<=1px`
- text bbox center vs box bbox center y error `<=1px`
- box 不出画面、不进入平台危险区

任一不通过：`SUBTITLE_IMPLEMENTATION_QA_PASS = NO`。

### C. Mandatory visual samples

至少抽查：
1. 第一行；
2. 最短句；
3. 最长单行句；
4. 两行句（如存在）；
5. 最后一行。

检查：
- 字重/字号一致；
- 底框 opacity 一致；
- padding 视觉一致；
- 字幕在框内真正居中；
- 不遮挡关键眼睛/动作主体；
- 手机观看可读。

短句是强制样本，因为窄框最容易放大非对称误差。

---

## 6. Gate policy｜NO REPEATED STYLE LOOP

当本标准已经被用户接受：
- 后续项目默认 `STYLE = LOCKED_BASELINE`；
- 不再先做三套 A/B/C 候选；
- 直接按标准渲染 + 固定 QA；
- 只有用户明确提出“这首歌要换字幕风格”时，才重新开启 Style Exploration；
- 单纯实现 bug（偏心、padding、溢出、时间错）只能修实现，不得借机重新设计整套风格。

Gate 顺序：
`canonical timing -> render -> all-line geometry QA -> mandatory sample visual QA -> timing implementation QA -> SUBTITLE_IMPLEMENTATION_QA_PASS`

若未改变视觉标准，`SUBTITLE_STYLE_QA_PASS` 可继承已锁 baseline；不需要每首歌重新人工选样式。

---

## 7. WEB R2 accepted evidence

Accepted subtitle baseline:
- R1 actual screenshot as visual truth；
- WEB R2 nominal `46px` / center `360,1009`；
- bbox-regenerated rounded box；
- `10px` equal padding；
- `100ms / 180ms` fade；
- max 2 lines；
- no karaoke。

WEB R2 implementation QA:
- 10 lyric lines；
- max canonical timing implementation delta `0.005s`；
- all lines geometry `10/10/10/10px` PASS；
- shortest-risk line `好吧哎哟哎哟` PASS；
- two-line line PASS。

Round receipt:
`06_TESTS/MV/WEB_R2/W09_SUBTITLE_STYLE_LOCK_RECEIPT.json`

---

## 8. Reusable output assets

Each completed MV should preserve:
- canonical SRT / line timeline pointer；
- final ASS/subtitle implementation file；
- subtitle style parameters；
- geometry QA report；
- timing implementation QA result；
- any explicit per-song semantic wrap choices。

Do not preserve only a rendered MP4. The subtitle layer must remain reproducible and auditable.
