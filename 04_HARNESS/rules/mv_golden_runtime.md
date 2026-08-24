# Rules｜MV Golden Runtime Contract v1.4

> Status: `PRODUCTION_VALIDATED / ACTIVE`
> Purpose: 跨 Round 继承 correctness 与已验证生产纪律，不加载整轮历史。
> Evidence base: R1 Golden + WEB R2 full close。

---

## 1. Golden inheritance｜HARD

每次 MV 默认加载：
1. `workflows/mv.md`
2. `rules/mv_golden_runtime.md`
3. `rules/mv_audio_timeline.md`
4. current Round `CURRENT_STATE.md`
5. stage-specific Rules JIT。

Round Master Plan / retrospective 只做 summary / provenance，不能覆盖 Workflow/Rule。

---

## 2. Correctness promotion standard｜HARD

用户抓到的 correctness 或重复质量问题，只有完成以下链条才算真正解决：

`failure evidence`
→ `root cause`
→ `stable rule`
→ `required artifact/state`
→ `independent Gate/check`
→ `regression evidence`

仅仅在复盘里写一句“以后注意”不算晋升。

WEB R2 已晋升的典型：
- 歌词时间轴失败 → `AUDIO_TIMELINE_PACKAGE`；
- 视觉时间线少段但实际镜头仍碎 → `Shot Normalization + visible-shot Fragmentation Gate`；
- 字幕框偏心 → glyph bbox fresh-box algorithm + all-line geometry QA；
- WEB 水印反复漏角 → batch uniform crop/zoom + corner-risk QA。

---

## 3. Audio Timeline is the first post-BGM hard node｜HARD

固定顺序：
`BGM_LOCKED -> AUDIO_TIMELINE_PACKAGE_LOCKED -> time-dependent downstream work`。

原因：
- 更早：音频版本/截取可能变化，强制对齐会白做；
- 更晚：Natural Beat/Director/Edit/Subtitle 会继承猜测时间。

Package 详细权威：`rules/mv_audio_timeline.md`。

Strong evidence only：
- `SAME_VERSION_LRC`
- `ASR_FORCED_ALIGNMENT`
- `OFFICIAL_TIMED_LYRIC`

Waveform/BPM/onset 只能 diagnostic/supporting。

缺能力/证据必须 `BLOCKED`，不得为了“保持自动化”降级真值标准。

---

## 4. Three clocks｜HARD

必须区分：
1. lyric clock；
2. music-event clock；
3. visual-action clock。

Audio Timeline Package 锁 1+2；生成/素材 QA 提供 3；Picture Edit 协调三者。

Subtitle 只服从 lyric clock。
Picture cut / visual segment 不得反向修改 lyric clock。

---

## 5. Human Gate inheritance

权威：`rules/mv_human_gates.md`。

正常项目只保留 5 个固定人工 Gate：
1. Song Aesthetic；
2. BGM Excerpt Listening；
3. Visual Direction / First-frame Set；
4. Picture Edit Rhythm；
5. Final Acceptance。

其余正确性/实现 QA 应在提交用户前完成。

异常才打开：Audio Alignment Exception / Dynamic Regeneration / New Subtitle Style。

目标：用户审核审美与最终授权，不承担机器应该完成的基础技术 QA。

---

## 6. First-frame / dynamic source inheritance

Stable：
- first frame = `0-second dynamic anchor`；
- conceptual units 与 production segments 分离；
- 人物首帧 closure；
- character I2V 安全前缀由 `rules/ai_video.md` 管理；
- shot count 按歌词/导演任务，不固定配额；
- whole-set camera repetition review；
- retry by root cause；
- dynamic video 是 **editing source pool**。

WEB R2 validated portfolio：
- 1-shot：hold / space / emotion / release；
- 2-shot：常用 setup-event / detail-emotion；
- 3-shot：task-specific discovery / peak；
- >3-shot：exceptional hook/peak only。

约 5s 生成默认优先 **1–2 shots**，3-shot 必须有明确任务。

---

## 7. Dynamic QA + Source Normalization inheritance｜HARD FOR MULTI-SHOT

Raw QA status：
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

W07 必须产出 executable `VISUAL_SOURCE_MAP`，包含 clean/risk/internal-cut/action/edit-role 信息。

对于 1–3 镜/多镜 source，进入 Picture Edit 前必须按 `rules/mv_source_normalization.md`：
- 保留原始 5s；
- 映射内部真实镜头；
- 派生 `ATOM`；
- 只有导演语法成立才保留 `ARC`；
- 排除 duplicate / topology-risk / meaningless micro-shot；
- 输出 `NORMALIZED_SHOT_LIBRARY_MAP.csv`；
- Gate `SHOT_LIBRARY_READY`。

核心经验：
**少量 timeline block 不等于少镜头。**必须统计 perceptible visible-shot count。

---

## 8. Editing inheritance

权威：`rules/mv_editing.md`。

Priority：
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`。

Promoted defaults for lyrical/emotional MV：
- long-cut first；
- Anchor Word != mandatory cut；
- lyric start != mandatory cut；
- semantic hit can occur inside shot；
- preserve useful motion arc；
- avoid short A-B-A recycling；
- final release 留呼吸；
- Fragmentation Gate 同时检查 external fragment 与 perceptible visible-shot count。

WEB 当前限制：精确水印处理不可用时，使用整批统一 zoom/crop，保持 9:16 / SAR1:1，并抽查左右角最危险帧。它只是 WEB fallback，不是 publish-grade 首选。

---

## 9. Subtitle inheritance｜LOCKED BASELINE

权威：`rules/mv_subtitle.md`。

默认不再每首歌重新 A/B/C 探索。
只有用户明确要求新的字幕审美才打开 Style Exploration。

720×1280 validated baseline：
- bold clean Chinese sans serif；
- nominal 46px family；
- near-white text；
- lower center around `360,1009`；
- dark semi-transparent rounded box；
- four-side padding `10px`；
- max 2 lines；
- fade `100ms / 180ms`；
- no default karaoke。

Implementation hard rule：
`actual rendered glyph bbox -> fresh rounded box -> 10px padding each side -> all-line geometry QA`。

禁止 resize/inset legacy rounded path；禁止 character-count 估算框宽；短句必须专项抽查。

Two QA layers remain separate：
- Ground-truth Alignment QA：Stage 2A；
- Subtitle Implementation QA：Stage 9。

---

## 10. Source audio / publish quality inheritance

AI source audio 非时间真源；final edit 默认物理移除 source audio，锁定 BGM 是唯一 music truth。

Publish-grade priority：
`watermark-free HD source > Codex/precise cleanup > WEB uniform crop fallback`。

不得为了清水印偷偷改变已批准的 timing/directing。

---

## 11. Patch, Don't Cascade｜HARD

问题只回滚最近根因：
- BGM 变化 → Stage 2A 及 timing-dependent 下游失效；
- timing 真值错 → 2A；
- 首帧/视觉方向错 → 4/5；
- 单条动态 source 崩 → 6/7；
- hidden multi-shot complexity → 7.5；
- Picture 太碎 → 8B；
- subtitle geometry/implementation bug → 9；
- codec/SAR/metadata bug → 10。

下游实现 bug 不自动重开已通过的上游审美 Gate。

---

## 12. Minimum runtime state chain

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `AUDIO_TIMELINE_PACKAGE_LOCKED`
→ `DIRECTOR_BEAT_MAP`
→ `DIRECTOR_PLAN_LOCKED`
→ `FIRST_FRAME_SET_LOCKED`
→ `DYNAMIC_PROMPT_SET_READY`
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `SHOT_LIBRARY_READY`（multi-shot source 时）
→ `EDITOR_AUDIO_GATE_PASS`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`
→ `COMPLETE_LOCKED`

任一 required upstream state 缺失，later state 无效。

---

## 13. What Golden does NOT freeze

禁止把以下变成跨歌固定模板：
- R1/R2 歌曲；
- 人物/世界/材质；
- first-frame/video 固定数量；
- 固定 3-shot grammar；
- 固定 camera recipe；
- 所有类型歌曲统一 8–12 cuts；
- 复杂歌词特效。

Golden 保护 correctness 和 validated production discipline，不保护创意重复。
