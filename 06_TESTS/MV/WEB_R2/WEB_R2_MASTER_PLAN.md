# WEB R2｜MASTER PLAN v1.1

## Goal

测试网页端 ChatGPT 在不依赖 Codex 的情况下，能否从新歌开始完整推进 AI MV，并记录真实自动化边界。

R1 Golden Sample 是质量下限，但不限制 R2 的歌曲、人物、世界或视觉概念。

## Authority rule

本文件是 **Round summary / stage map**，不是运行时权威流程。

Operational truth 优先级固定为：
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. current Round `CURRENT_STATE.md`
4. 本 Master Plan

本文件若与 Workflow / Runtime Rule 冲突，以前两者为准，并更新本文件，禁止同时保留两套不同流程。

---

# W00｜Bootstrap / Capability Baseline

读取权威 Workflow + Golden Runtime + 当前状态，确认网页端实际能力与外部工具边界。

Output：更新 `AUTOMATION_MATRIX.md`、`CURRENT_STATE.md`。

---

# W01｜Song Discovery / Benchmark Selection

自动刷新少量高相关MV/音乐观察源，筛3–5首候选；用户只做最终歌曲审美选择。

Gate：`REFERENCE_BGM_LOCKED`。

---

# W02｜Reference BGM / Exact Clip Lock

拿到实际源音频后自动分析/裁剪/试听，锁定版本、起止点、时长、fade、文件身份/hash。

Gate：`BGM_LOCKED`。

---

# W03｜Music / Lyric / Beat Analysis

自动完成：
- 精确歌词文本；
- 情绪/语义结构；
- Natural Beats；
- 强弱分布；
- 视觉机会。

重要：W03 可形成导演级 Beat Map，但**不能用波形/BPM/估算替代精确歌词时间轴**。

Gate：`LYRIC_TEXT_LOCKED + DIRECTOR_BEAT_MAP`。

---

# W04｜Director + Production Allocation

自动完成导演概念、视觉世界、角色政策、每Beat主事件、生产段数量、镜头/运镜差异化和素材覆盖余量。

用户做导演方向审美 Gate。

Gate：`DIRECTOR_PLAN_LOCKED`。

---

# W05｜First Frames

生成并自检整组 `0-second dynamic anchors`，用户整组审美确认。

Gate：`FIRST_FRAME_SET_LOCKED`。

---

# W06｜Dynamic Prompt Design + External Generation

按歌词任务逐段选择一镜 / 2–3镜 / 更密集多镜；每个Shot使用明确 Camera Contract；做整组重复度 Gate。

当前网页端无 Seedance 执行接口时：用户只负责外部生成并上传原始视频。

Gate：`DYNAMIC_PROMPT_SET_READY`；外部执行标记 `EXTERNAL_REQUIRED`。

---

# W07｜Dynamic QA + Retry

自动做人物/面纱/肢体/场景/主事件/运镜/重复度 QA，并按：
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`
分级。

Gate：`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`。

---

# W08A｜Lyric Timing Evidence / Alignment｜MANDATORY PRE-EDIT

**禁止先剪视频。**

必须先取得独立强时间证据：
1. 实际 ASR / forced alignment；或
2. 同版本可靠 LRC；或
3. 官方同版本 timed lyric/video。

并保存：
- raw evidence；
- provenance；
- 转换方式；
- 逐句时间轴；
- Ground-truth Alignment QA。

BPM/波形谷值/能量/onset 只能做交叉验证，不能单独升级为精确时间轴。

Required states：
`LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED`
→ `LYRIC_ALIGNMENT_PROVENANCE_VERIFIED`
→ `ALIGNMENT_GROUND_TRUTH_QA_PASS`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`

任何一项缺失：`LYRIC_TIMELINE_BLOCKED`，停止，不生成剪辑版。

---

# W08B｜Picture Edit

只有 W08A 全部通过后才允许建立剪辑时间线。

原则：
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > mechanical equal timing`

每个片段记录 source in/out、final in/out、服务的歌词/Beat、剪切理由、动作弧。

Gate：`EDIT_MAP_LOCKED -> EDIT_PREVIEW_QA_PASS`。

---

# W09｜Subtitle Style + Implementation QA

字幕时间来自已锁 `LYRIC_TIMELINE`，此阶段禁止再通过画面重新估算时间。

先加载 R1 Golden 字幕规格，再做样式 QA。

必须区分：
- Ground-truth Alignment QA：时间轴是否跟真实人声对；在W08A完成；
- Subtitle Implementation QA：视频是否按锁定时间显示字幕；在W09完成。

Gate：
`SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`。

---

# W10｜Final Technical QA / Delivery

检查：
- 锁定BGM与最终音轨一致；
- 无AI源音轨；
- 画幅/SAR/FPS；
- 无黑帧/错误重复/已知风险帧；
- 字幕样式和实现；
- 完整成片复看。

Gate：`FINAL_TECH_QA_PASS -> DELIVERABLE_RENDERED`。

交付文件优先 ZIP，ZIP 内使用兼容文件名并做完整性测试。

---

# W11｜Automation Retrospective / Close

输出最终 Automation Matrix、人工干预、可自动化边界、规则晋升和 Golden 资产。

Round 只有在用户最终验收后才能 `COMPLETE_LOCKED`。

Golden close 必须保存可复现资产，不得只在文档里写文件名：尤其是锁定音频、最终SRT/LRC/时间轴及其 provenance。
