# WEB R2｜MASTER PLAN v1.3｜FINAL

> Status: `ROUND CLOSED / HISTORICAL SUMMARY`
> Operational truth now lives in `04_HARNESS/workflows/mv.md` + current Runtime Rules. 本文件只总结 WEB R2 最终执行链，不再覆盖 Runtime。

## Goal achieved

WEB R2 验证了网页端高自动化 MV 流程，并完成以下正式晋升：
- post-BGM `AUDIO_TIMELINE_PACKAGE` hard gate；
- 1–3镜 RAW SOURCE → Atom/Arc Shot Normalization；
- long-cut-first + perceptible visible-shot Fragmentation Gate；
- WEB batch uniform watermark-safe crop/zoom fallback；
- locked subtitle baseline + glyph-bbox geometry QA；
- 5 fixed Human Gates + nearest-cause rollback。

Final retrospective:
`WEB_R2_FINAL_RETROSPECTIVE_AND_SOP_v1.md`

---

# Final stage map

## W00｜Bootstrap
读取 Workflow / Golden Runtime / Audio Timeline / Current State，确认工具边界。

## W01｜Song Discovery
系统筛选，用户做审美选择。

Human Gate：`HG01`
Gate：`REFERENCE_BGM_LOCKED`

## W02｜Exact BGM Clip Lock
锁 actual source / start / end / fade / duration / hash；检查前句污染和结尾完整性。

Human Gate：`HG02`
Gate：`BGM_LOCKED`

## W02A｜AUDIO TIMELINE PACKAGE
BGM 之后第一 correctness-critical Gate。

锁定：
- audio identity；
- trusted lyrics；
- raw strong evidence/provenance；
- line timeline；
- exact SRT；
- anchors；
- music events；
- ground-truth QA；
- manifest。

Gate：`AUDIO_TIMELINE_PACKAGE_LOCKED`

正常 AUTO；只有 evidence conflict 触发条件 Human Gate。

## W03｜Natural Beat
基于 Package 建立 semantic/emotion/Hook/Peak/Release/Anchor opportunities。

Output：`DIRECTOR_BEAT_MAP`

## W04｜Director Allocation
视觉世界、production segment、dominant event、edit role、camera differentiation。

Gate：`DIRECTOR_PLAN_LOCKED`

默认不单独占一次人工审批，与 W05 一起看。

## W05｜First Frames
0-second dynamic anchors + whole-set QA。

Human Gate：`HG03`
Gate：`FIRST_FRAME_SET_LOCKED`

## W06｜Dynamic Prompt / External Generation
约 5s source 默认 1–2 镜；3镜任务型；>3镜只给真正高潮。

Gate：`DYNAMIC_PROMPT_SET_READY`

外部生成属于 capability handoff，不等于审美 Gate。

## W07｜Dynamic Source QA
`PASS_FULL / TRIM_REQUIRED / REGEN_WATCH / REGENERATE`
并输出 executable `VISUAL_SOURCE_MAP`。

Gate：`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`

## W07.5｜Shot Normalization
保留原片，拆 Atom，保留有导演价值的 Arc，排除重复/风险/micro-shot；WEB derived proxy 统一 strip audio + batch safe crop。

Output：`NORMALIZED_SHOT_LIBRARY_MAP.csv`
Gate：`SHOT_LIBRARY_READY`

## W08A｜Editor Audio Revalidation
只验证 current BGM 与 Audio Timeline Package identity，不重新猜时间。

Gate：`EDITOR_AUDIO_GATE_PASS`

## W08B｜Picture Edit
协调 lyric / music-event / visual-action clocks。

Default：`long-cut first / semantic-hit inside shot`。

必须同时检查：
- external fragment count；
- perceptible visible-shot count。

Gate：`EDIT_MAP_LOCKED`
→ Picture+BGM tech QA
→ Human Gate `HG04`
→ `EDIT_PREVIEW_QA_PASS`

## W09｜Subtitle
Timing 只来自 canonical Package；默认直接复用已锁 baseline，不再每歌 A/B/C。

实施必须：actual glyph bbox → fresh rounded box → equal padding → all-line geometry QA。

Gates：
`SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`

## W10｜Final QA
Audio identity/lag、source-audio leakage、SAR/fps/resolution、black/risk frames、watermark、subtitle、full-watch、ZIP integrity。

Gate：`FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`
→ Human Gate `HG05`

## W11｜Close
保存完整可复刻资产、receipts、promoted rules。

Gate：`COMPLETE_LOCKED`

---

# Fixed Human Gate map

Normal target = 5：
1. HG01 Song Aesthetic
2. HG02 BGM Excerpt Listening
3. HG03 Visual Direction / First-frame Set
4. HG04 Picture Edit Rhythm
5. HG05 Final Acceptance

Conditional only：
- Audio Alignment Exception
- Dynamic Regeneration Decision
- New Subtitle Style

Authority：
`04_HARNESS/rules/mv_human_gates.md`

---

# R2 final state

- Song: 《如果你也刚好抬头看树》 / 孙天宇
- BGM: `37.120s`
- Director: `树影之外`
- first frames: `9/9`
- dynamic: `2S1–2S9`
- normalized library: `22 Atom/Arc units`
- accepted picture basis: `V3.2 Atom-first`
- subtitle: R1-derived screenshot-calibrated locked baseline
- final: `720×1280 / 24fps / 891 frames`
- audio global lag: `0.000000s`
- final SHA: `ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`
- Round: `COMPLETE_LOCKED`

Future new rounds must use current Runtime Workflow, not copy this historical plan literally.
