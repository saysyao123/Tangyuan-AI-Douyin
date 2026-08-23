# WEB R2｜MASTER PLAN v1.2

## Goal

测试网页端 ChatGPT 在不依赖 Codex 的情况下，完整推进 AI MV，并记录真实自动化边界。

R1 Golden Sample 是质量下限，不限制 R2 的歌曲、人物、世界或视觉概念。

## Authority rule

本文件只是 Round summary / stage map。
Operational truth：
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current Round `CURRENT_STATE.md`
5. 本 Master Plan

---

# W00｜Bootstrap

读取权威 Workflow + Runtime Rules + Current State，确认工具边界。

---

# W01｜Song Discovery

筛3–5首候选；用户只做歌曲审美选择。

Gate：`REFERENCE_BGM_LOCKED`。

---

# W02｜Reference BGM / Exact Clip Lock

锁定实际音频版本、起止点、时长、fade、hash。

Gate：`BGM_LOCKED`。

---

# W02A｜AUDIO TIMELINE PACKAGE｜FIRST HARD GATE

**BGM 锁定后的下一份强制交付。未 PASS 不进入正式 W03/W04。**

必须产出 canonical：
`<ROUND>/AUDIO_TIMELINE_PACKAGE/`

核心内容：
- audio identity/hash；
- trusted lyrics；
- raw timing evidence；
- provenance；
- line timeline；
- exact SRT；
- selected Anchor Word timings；
- verified music events；
- ground-truth QA；
- package manifest。

Timing route：
1. 同版本可靠 LRC；或
2. trusted lyrics + forced alignment；或
3. 官方同版本 timed lyric/video。

波形/BPM/onset 只能 supporting，不能单独成为真值。

Gate：
`AUDIO_TIMELINE_PACKAGE_LOCKED`。

当前 WEB R2 视觉素材在该 Gate 加入前已完成，因此不自动作废；但任何 V3 edit 都必须先补齐本 Gate。

---

# W03｜Music / Lyric / Natural Beat Analysis

使用已锁 Package，不再创建平行时间轴。

分析：
- 语义/情绪结构；
- Natural Beats；
- 强弱；
- Anchor Word视觉机会；
- Hook / Peak / Release。

Gate：`DIRECTOR_BEAT_MAP`。

---

# W04｜Director + Production Allocation

基于真实 line/anchor/music-event timing 做导演分配、生产段数量、镜头差异化、素材余量。

Gate：`DIRECTOR_PLAN_LOCKED`。

---

# W05｜First Frames

整组 `0-second dynamic anchors`。

Gate：`FIRST_FRAME_SET_LOCKED`。

---

# W06｜Dynamic Prompt + External Generation

按歌词/导演任务选择一镜 / 2–3镜 / 更密多镜；做 Camera Repetition Gate。

Gate：`DYNAMIC_PROMPT_SET_READY`；外部执行可标记 `EXTERNAL_REQUIRED`。

---

# W07｜Dynamic QA

按 `PASS_FULL / SOURCE_USABLE-TRIM_REQUIRED / REGEN_WATCH / REGENERATE` 分级，并建立 clean `VISUAL_SOURCE_MAP`。

Gate：`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`。

---

# W08A｜Editor Audio Gate Revalidation

此处不再获取/猜时间轴，只验证 W02A Package 仍对应当前 BGM hash/version/duration。

Gate：`EDITOR_AUDIO_GATE_PASS`。

不通过 → 回 W02A。

---

# W08B｜Picture Edit

使用三只时钟：
- lyric clock；
- music-event clock；
- visual-action clock。

原则：
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`。

Gate：
`EDIT_MAP_LOCKED -> EDIT_PREVIEW_QA_PASS`。

---

# W09｜Subtitle Style + Implementation QA

时间来自 W02A `lyrics_exact.srt`，本阶段只做 Golden 样式和实现检查。

必须区分：
- Ground-truth Alignment QA：W02A；
- Subtitle Implementation QA：W09。

Gate：
`SUBTITLE_STYLE_QA_PASS -> SUBTITLE_IMPLEMENTATION_QA_PASS`。

---

# W10｜Final QA / Delivery

检查音频、时间轴Package identity、画幅/SAR/FPS、风险帧、字幕、完整观看、交付ZIP完整性。

Gate：`FINAL_TECH_QA_PASS -> DELIVERABLE_RENDERED`。

---

# W11｜Retrospective / Close

只有用户最终验收后才 `COMPLETE_LOCKED`。

Golden close 必须保存完整 `AUDIO_TIMELINE_PACKAGE`，不能只在文档里写“准确字幕文件叫xxx”。
