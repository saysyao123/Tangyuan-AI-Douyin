# Workflow｜AI MV Production v1.7

> Status: `AUTHORITATIVE / R1 + WEB_R2 VALIDATED`
> Role: MV 单一路径主流程。只定义阶段、输入/输出、Gate 与回滚边界；技术细节由独立 Rule JIT 加载。
> Core: **先锁声音坐标，再按坐标导演素材；生成的是可剪素材池，不是 5 秒成片；局部问题只回滚最近根因。**

---

## 0. Runtime load order

默认只加载：
1. `04_HARNESS/workflows/mv.md`
2. `04_HARNESS/rules/mv_golden_runtime.md`
3. `04_HARNESS/rules/mv_audio_timeline.md`
4. current MV Round `CURRENT_STATE.md`

Stage-specific JIT：
- Human decision boundary：`rules/mv_human_gates.md`
- Stage 4/6/7/8：`rules/mv_editing.md`
- Stage 6 character I2V：`rules/ai_video.md`
- Stage 7.5/8：`rules/mv_source_normalization.md`
- Stage 9：`rules/mv_subtitle.md`

历史 R1/R2 文件只用于排错、回归、溯源；正常 Runtime 不全文加载。

---

# Single Path｜固定主链

`Song Discovery`
→ `Exact BGM Clip Lock`
→ **`AUDIO_TIMELINE_PACKAGE`**
→ `Natural Beat`
→ `Director Allocation`
→ `First Frames`
→ `Dynamic Source Generation`
→ `Dynamic QA`
→ `Shot Normalization`
→ `Editor Audio Revalidation`
→ `Picture Edit`
→ `Subtitle Render + QA`
→ `Final QA`
→ `Close`

禁止跳过 Stage 2A 后再在剪辑/字幕阶段补时间真值。

---

# Stage 1｜Song Discovery

### Work
- 筛 3–5 个真正有差异的候选；
- 核对基本版本/可执行性；
- 不用 R1/R2 的具体歌曲/世界限制创意。

### Human Gate
`HG01 Song Aesthetic Gate`。

### Output / Gate
`REFERENCE_BGM_LOCKED`。

---

# Stage 2｜Exact BGM Clip Lock

### Work
使用实际 MP3/WAV/发布音频：
- 核对 title / artist / exact version；
- 选择语义完整段落；
- 检查前一句污染；
- 保留合理 pickup；
- **绝不截断一句歌词**；
- 结尾不舒服时优先多留完整 release line；
- fade 在人声完成后发生；
- 保存 source start/end、duration、speed、fade、SHA。

### Human Gate
`HG02 BGM Excerpt Listening Gate`。

### Output / Gate
`BGM_LOCKED`。

任何后续音频版本/起止点变化都使 Stage 2A 及其 timing-dependent 下游失效。

---

# Stage 2A｜AUDIO TIMELINE PACKAGE｜FIRST HARD GATE

详细规则：`rules/mv_audio_timeline.md`。

### Purpose
把锁定 BGM 变成整个 MV 的**唯一时间坐标系**，而不是只为字幕服务。

### Mandatory package
至少包含：
- `audio_identity.json`
- `trusted_lyrics.txt`
- raw strong timing evidence
- `alignment_provenance.json`
- `line_timeline.csv`
- `lyrics_exact.srt`
- `anchor_words.csv`
- `music_events.csv`
- `alignment_qa_report.md`
- `package_manifest.json`

Primary strong evidence：
- verified same-version LRC；或
- trusted lyrics + Chinese-capable forced alignment；或
- official same-version timed lyric/video。

Waveform/BPM/onset 只能 supporting。

### Human Gate
正常 PASS 不需要用户逐行人工核时间。
只有强证据冲突/unmatched/repeated occurrence 无法自动判断时触发 `CHG-A`。

### Output / Gate
`AUDIO_TIMELINE_PACKAGE_LOCKED`。

**未 PASS 不进入 Stage 3。**

---

# Stage 3｜Music / Lyric / Natural Beat

### Input
只使用已锁 Package，不创建第二套 lyric clock。

### Work
确定：
- 语义/情绪结构；
- Natural Beats；
- Hook / Peak / Release；
- Anchor Word 视觉机会；
- 能量变化。

Natural Beat 是语义/情绪单元，不是 5 秒配额。

### Output
`DIRECTOR_BEAT_MAP`。

默认 AUTO。

---

# Stage 4｜Director Concept + Production Allocation

JIT：`rules/mv_editing.md`。

### Work
定义：
- 世界 / palette / material；
- character policy；
- 每 Beat 的 dominant event；
- camera/motion differentiation；
- conceptual unit vs production segment；
- raw-video headroom；
- edit role：`HOLD / BRIDGE / HIT / PEAK / RELEASE`。

Hard concept：
`conceptual unit != first-frame count != dynamic-video count != final edit fragment count`。

### Output / Gate
`DIRECTOR_PLAN_LOCKED`。

默认不单独占用一次人工审批；与 Stage 5 的整组首帧一起做视觉 Gate。

---

# Stage 5｜First Frames

### Work
每个 production segment 形成 0 秒动态锚点：
- 主视觉事件起始态；
- 主动作入口；
- 摄影机/动作空间；
- 可持续物理余韵；
- 人物/物体 closure；
- clean source-arc potential。

整组 QA：歌词命中、美感、差异、连续性、动态可执行性、编辑价值。

### Human Gate
`HG03 Visual Direction / First-frame Set Gate`。

### Output / Gate
`FIRST_FRAME_SET_LOCKED`。

---

# Stage 6｜Dynamic Prompt + External Generation

JIT：`rules/mv_editing.md` + `rules/ai_video.md`。

### Source philosophy
动态视频是 `RAW SOURCE`，不是最终 5 秒成片。

对约 5s Seedance 类素材：
- 1-shot：空间/情绪/连续动作/release；
- 2-shot：常用默认，setup→event 或 detail→emotion；
- 3-shot：发现/高潮/setup→event→aftermath；
- >3-shot：只给真正 Hook/Peak。

默认偏好：**1–2 镜；3 镜任务型。**

每 Shot：
`1 primary camera move + 1 primary subject action + 1 secondary physical motion`。

生成前做 Camera Repetition / Load / Edit-value Gate。

### Output / Gate
`DYNAMIC_PROMPT_SET_READY`。

外部 Seedance 执行属于 capability handoff，不等于审美 Gate。

---

# Stage 7｜Dynamic Source QA

### Work
完整检查原始返回素材：
- identity / face / hands / topology；
- event 是否完成；
- camera / beauty / repetition；
- clean in/out；
- internal cut/action windows；
- source audio；
- risk windows。

Status：
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

AI source audio 默认在 ingest 物理移除；锁定 BGM 是唯一音乐真源。

### Required output
`VISUAL_SOURCE_MAP`：source、fps/duration、clean windows、internal cuts/actions、risk windows、edit role、status。

### Conditional Human Gate
只有确实 `REGENERATE` / clean duration 不足才触发 `CHG-B`；`TRIM_REQUIRED` 先剪，不先重生成。

### Gate
`DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`。

---

# Stage 7.5｜Shot Normalization / Atom-Arc Library

JIT：`rules/mv_source_normalization.md`。

**对 1–3 镜/多镜原片默认执行。**

### Work
- 原始 5s 文件永久保留；
- 映射真实内部切镜/事件；
- 派生单状态 `ATOM`；
- 只有明确导演语法才保留 `ARC`；
- 排除 duplicate / topology-risk / meaningless micro-shot；
- WEB derived proxy 统一去 source audio；
- WEB 有角落标记时整批使用同一 watermark-safe crop/zoom。

### Output / Gate
`NORMALIZED_SHOT_LIBRARY_MAP.csv`
→ `SHOT_LIBRARY_READY`。

禁止让复杂多镜原片作为 opaque block 直接进入最终剪辑再现场猜结构。

---

# Stage 8A｜Editor Audio Gate

Stage 2A 获取 timing truth；这里**只重验，不重新猜**。

核对当前 BGM：hash/version/duration/clip/speed/lyrics 与 Package 一致。

Mismatch → 回 Stage 2A。

Gate：`EDITOR_AUDIO_GATE_PASS`。

---

# Stage 8B｜Picture Edit

JIT：`rules/mv_editing.md` + `rules/mv_source_normalization.md`。

### Inputs
- `line_timeline.csv`
- `anchor_words.csv`
- `music_events.csv`
- `VISUAL_SOURCE_MAP`
- `NORMALIZED_SHOT_LIBRARY_MAP.csv`

### Three clocks
1. lyric clock；
2. music-event clock；
3. visual-action clock。

Priority：
`verified lyric/music truth > emotional flow > internal action integrity > musical cut point > equal duration`。

### Default edit grammar
抒情/诗意 MV：`long-cut first / semantic-hit inside shot`。

- lyric start ≠ mandatory cut；
- Anchor Word ≠ mandatory cut；
- 优先让已运行镜头内部动作命中语义；
- 避免短距离 A→B→A；
- 保留完整动作 arc；
- 结尾留 release breathing room。

### Fragmentation Gate｜HARD
同时统计：
1. external fragment count；
2. **perceptible visible-shot count**（含 Arc 内部镜头）。

约 35–40s 抒情 MV 可参考 8–12 个外部 block，但最终以 visible-shot flow 为准。

### WEB fallback
角落平台标记无法精确处理时：整批统一 zoom/crop，保持 9:16 + SAR1:1，抽查左上/右下 worst-case。

### Gates
`EDIT_MAP_LOCKED`
→ render `Picture + locked BGM`
→ audio global-lag QA / visual technical QA
→ `HG04 Picture Edit Rhythm Gate`
→ `EDIT_PREVIEW_QA_PASS`。

画面节奏问题默认只回 Stage 8B；clean source 不足才回 6/7。

---

# Stage 9｜Subtitle Render + QA

JIT：`rules/mv_subtitle.md`。

### Timing
唯一来源：Stage 2A canonical SRT/timeline。
禁止根据 Picture cut nudge 时间。

### Style
已锁字幕 baseline 默认直接复用：
- 不再每首歌 A/B/C；
- 只有用户明确要求新字幕风格才触发 `CHG-C`。

### Fixed QA
- all-line timing implementation check；
- actual glyph bbox → fresh rounded box；
- all-line padding/center geometry QA；
- first / shortest / longest-one-line / two-line / final samples；
- overflow / safe area / subject-cover check。

实现 bug 只修实现，不重新打开审美设计。

Gates：
`SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_IMPLEMENTATION_QA_PASS`。

---

# Stage 10｜Final QA / Delivery

### Mandatory machine QA before user
- locked BGM identity/duration/hash；
- no AI source-audio leakage；
- Package identity；
- resolution/fps/SAR/DAR；
- no stretch/blank/black/accidental duplicate/risk frames；
- watermark handling consistency；
- subtitle geometry/timing/safe area；
- opening / major transitions / peak / ending / full-watch；
- delivery ZIP integrity；
- final identity/hash。

Gate：`FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`。

### Human Gate
`HG05 Final Acceptance Gate`。

用户 PASS 后才进入 Close。

---

# Stage 11｜Close

保存可复刻资产，不只保存最终 MP4：
- final accepted MV + hash；
- BGM identity；
- full Audio Timeline Package/raw evidence/provenance；
- Director/first-frame pointers；
- `VISUAL_SOURCE_MAP`；
- normalized Shot Library Map；
- accepted Edit Map；
- subtitle implementation + geometry/timing QA；
- Final QA receipt；
- promoted runtime rules；
- Current State / Automation Matrix；
- retrospective only when it adds durable learning。

Gate：`COMPLETE_LOCKED`。

---

# Mandatory State Chain

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

---

# Rollback Rule｜Patch, Don't Cascade

详细人工/异常 Gate：`rules/mv_human_gates.md`。

默认只回最近根因：
- BGM改 → Stage 2A 及 timing-dependent 下游失效；
- timing错 → 2A；
- 首帧/视觉错 → 4/5；
- 单条动态崩 → 6/7该 source；
- 隐藏多镜/碎镜 → 7.5；
- Picture太碎 → 8B；
- 字幕框/实现错 → 9；
- Final codec/SAR/metadata错 → 10。

**下游实现 bug 不得自动重开已通过的上游审美 Gate。**
