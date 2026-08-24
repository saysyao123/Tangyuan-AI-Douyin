# WEB R2｜Final Retrospective & Reproducible SOP v1

> Date: 2026-08-24
> Round: `WEB_R2`
> Final song: 《如果你也刚好抬头看树》｜孙天宇
> Status: `USER_ACCEPTED / CLOSE READY`
> Purpose: 把“审美选择 Gate”早期 W00–W07 与后续 W02A/W07.5/W08–W10 的全部关键经验压缩成未来可复刻的单一路径，并区分自动化与人工审核边界。

---

# 1. Executive conclusion

WEB R2 最重要的成果不是做完一条 MV，而是完成了 4 个原先不稳定模块的闭环：

1. **Audio Timeline**：从“剪辑/字幕时再估时间”升级为 BGM 后第一硬 Gate；
2. **Dynamic Source**：从“5 秒视频就是剪辑单元”升级为 1–3 镜 RAW SOURCE + Atom/Arc Normalization；
3. **Picture Edit**：从“每个歌词/Anchor 都切一下”升级为 long-cut-first + visible-shot Fragmentation Gate；
4. **Subtitle**：从每轮重新设计/人工发现偏心问题，升级为锁定 baseline + glyph bbox fresh-box + all-line geometry QA。

最终推荐生产逻辑：

> **先把声音变成坐标，再按坐标导演素材；生成的是可剪素材池；素材先标准化再剪；剪辑优先完整动作和呼吸；字幕使用锁定样式并机器审核；用户只在 5 个真正需要审美/最终授权的位置确认。**

---

# 2. R2 originally wanted to test

WEB R2 目标：测试 ChatGPT 网页端在不依赖 Codex 的情况下，能够把 R1 Golden 经验执行到什么程度，并真实记录自动化边界。

R1 是 quality/correctness floor，但不能变成创意模板：
- 不复制 R1 歌曲；
- 不复制纸墨视觉世界；
- 不复制具体人物/镜头；
- 只继承正确性与稳定生产纪律。

R2 最终证明：**历史经验只有变成 Runtime Rule + Artifact + Gate，才算真正被继承。**

---

# 3. Full Round chronology and what each failure taught us

## Phase A｜W00–W02：审美选择与真正的 BGM 锁定

用户最终选中《如果你也刚好抬头看树》。

第一次音频截取出现两个典型问题：
- 前面带入一句不属于目标副歌/段落的尾部；
- 结尾一句没有唱完整，收口断裂。

用户进一步明确：
- **前面再多进约 0.5 秒会更舒服**；
- **后面多保留完整一句，再做淡出更舒服**。

最终 locked excerpt：
- source start `139.930s`
- source end `177.050s`
- content `37.120s`
- SHA-256 `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`

### Promoted lesson

BGM 截取本质上有强听感/审美成分，不能只依赖机器“句子边界”。
因此：

`Song Aesthetic Gate`
→ `BGM Excerpt Listening Gate`
→ **之后才允许 Audio Timeline alignment**。

这是未来固定 HG01/HG02。

---

## Phase B｜R2 early timing mistake：有歌词文本，不等于有时间真值

R2 早期视觉生产时，系统知道歌词内容和大概段落，但没有在 Director/Edit 前建立 strong-evidence line timeline。

最严重后果：
- 一度把 `如果你也刚好抬头看树` 当成更靠前/开场的重要行；
- 实际 locked clip 的第一句是 `我要学着树叶翩翩起舞`；
- title line 实际从 `19.090s` 左右才进入；
- V1/V2 的画面顺序与字幕逻辑因此受到错误时间假设污染。

这重现了 R1 的本质问题：
`visual segment / approximate phrase structure` 不能证明 singer timeline。

### Root cause

当时“subtitle timing comes from locked audio”只是原则，没有 mandatory canonical package 和 hard blocking gate。

### Final fix

新增并锁定：
`AUDIO_TIMELINE_PACKAGE`。

WEB R2 最终采用 trusted Chinese lyrics + Chinese-capable CTC forced alignment strong Route B，并保存：
- raw evidence；
- model/tool provenance；
- line timeline；
- exact SRT；
- Anchor Words；
- music events；
- ground-truth QA；
- package manifest/hash。

最终 10 行 canonical lyric timeline 建立并通过机器 Gate；重复副歌 occurrence 也做了独立对齐差异验证，排除了串错 occurrence / global drift。

### Promoted lesson

**Audio Timeline Package 固定放在 BGM Lock 之后、Natural Beat/Director 之前。**

不是：
- 选歌前做；
- 动态生成后做；
- 剪辑时做；
- 字幕时才做。

正确位置只有一个：

`BGM_LOCKED -> AUDIO_TIMELINE_PACKAGE_LOCKED -> downstream`。

---

## Phase C｜W03–W05：Natural Beat、Director、首帧

时间轴锁定后，歌词不再机械按 5 秒分段，而是先做：
- 语义/情绪；
- Natural Beat；
- Hook / Peak / Release；
- Anchor Word 视觉机会；
- Director production allocation。

R2 视觉方向：`树影之外`。

最终 9 张首帧 9/9 接受。

### Stable lesson

`conceptual unit != production segment != first-frame count != final edit cut count`。

首帧仍是：
`0-second dynamic anchor`，必须为后续动作和剪辑留入口，而不是只追求漂亮海报。

### Human Gate optimization

未来不再增加一个“纯文字 Director Plan 人工确认”作为默认步骤。
系统内部做完 Director Plan 后直接生成整组 First Frames，然后一次 HG03 同时审核：
- 世界审美；
- 歌词视觉命中；
- 整组差异；
- 连续性；
- 可动态化/可剪辑性。

减少一次低价值人工循环。

---

## Phase D｜W06：一镜到底 vs 多镜——最终答案不是固定镜数

R2 专门测试了镜头结构。

### S1 v1 failure

固定 extreme-wide one-take：
- 5 秒主体/空间关系变化不够；
- 动态被迫依赖白纱；
- 模型把纱生成成独立拓扑物体；
- 视觉进程不足。

结论：
`一镜到底 + 弱视觉进程` 失败，不等于 one-take 本身失败。

### S2 positive one-take

单一 Arc/orbit：
- 前景树干 / 人物 / 弧墙有持续 parallax；
- 人物动作很简单；
- 摄影机运动持续改变空间关系；
- 5 秒一直有视觉进程。

### Whole batch result

最终 2S1–2S9 混合：
- one-take；
- 2-shot；
- 3-shot；
- 少量 dense multi-shot。

### Promoted lesson

未来默认 source portfolio：
- 1-shot：hold / space / emotion / release；
- **2-shot：最常用基础结构**；
- 3-shot：发现/高潮/setup-event-aftermath；
- >3-shot：真正 Hook/Peak 才用。

对 5 秒类生成默认：**1–2 镜为主，3 镜任务型。**

最重要的是：
`lyric task -> first-frame potential -> shot count -> camera contract -> load budget -> edit value`。

不是：
`所有 5 秒统一三镜`。

---

## Phase E｜W07：动态素材不是 PASS/FAIL，而是可执行的素材地图

R2 raw source QA 最终采用：
- `PASS_FULL`
- `SOURCE_USABLE / TRIM_REQUIRED`
- `REGEN_WATCH`
- `REGENERATE`

典型：
- S1 中部两个低机位过近似 → trim，不重生；
- S7 2.8–4.0s 大白纱拓扑风险 → clean early + final resolve，先 trim；
- S8/S9 视觉语法接近 → S8缩短、S9留长 release；
- 全部 source AAC 音轨 → final ingest 物理移除，不让 Seedance audio 影响节奏。

### Promoted lesson

W07 的输出不能只有 prose `PASS`。
必须给编辑器 executable `VISUAL_SOURCE_MAP`：
- source id；
- duration/fps；
- clean windows；
- internal cut/action events；
- risk windows；
- edit role；
- status。

并遵守：
**TRIM_REQUIRED 先剪，不自动重生成。**
只有 clean duration 不足/核心事件失败才重生。

---

## Phase F｜W07.5：这轮最重要的新层——Shot Normalization

用户提出非常关键的问题：
既然生成视频本身是 1–3 镜，是否应该先整理成单一状态素材，再做最终剪辑？

答案经过 V3.1/V3.2 实测后为：**是，但必须非破坏性。**

### Why V3.1 exposed the hidden problem

V3.1 时间线上只有约 9 个外部 fragment，看起来已经“减少剪辑”。
但 S4/S6/S1 等 source 内部自己还有 cuts，观众实际感知镜头约接近 18 个。

所以：
`external fragments 少 != visible shots 少`。

### W07.5 solution

9 条原始 5 秒素材完整保留，同时整理出 22 个 Atom/Arc 单元：
- `ATOM`：一个单一状态/单一连续镜头；
- `ARC`：2–3 个内部镜头共同完成明确导演语法时保留。

排除：
- duplicate；
- topology-risk；
- meaningless micro-shot；
- 没有 clean in/out 的随机过渡。

### WEB watermark handling

网页端因为源视频有角落平台标记，最终把整批 derived proxy 使用同一个几何变换：
`720×1280 -> crop 576×1024 @ x72,y128 -> scale 720×1280`
约 `1.25×`。

关键不是永远固定 1.25×，而是：
- 先看本批 worst-case 水印位置；
- 全批次同一个 crop/zoom；
- 交付前抽查左上/右下风险帧；
- WEB fallback 与 Codex 无水印原源处理分开。

### Promoted lesson

以后多镜 source 默认：

`Raw 1–3 shot`
→ `W07 Source QA`
→ **`W07.5 Atom/Arc Normalization`**
→ `SHOT_LIBRARY_READY`
→ final Picture Edit。

不再把复杂 5 秒 source 当 opaque block 扔给最终编辑器。

---

## Phase G｜W08 Picture Edit：V3 → V3.1 → V3.2

### V3 problem

V3 技术上每个 Anchor 都“命中”，但视觉太碎。
根因：把 `semantic hit` 误等于 `picture cut`。

例如：
- 鸟儿；
- 飞过树梢；
- 抬头；
- 看树；
- 白云；
- 漂浮；
都被过度当成换镜理由。

### V3.1 correction

改成 long-cut-first：
- external fragments 从 17 降到约 9；
- Anchor 尽量由已运行镜头内部动作命中；
- 结尾保留长 release。

用户反馈：明显好很多，但仍问到 source 内部多镜与最终剪辑关系。

### V3.2 correction

用 W07.5 Atom Library 重建：
- 13 个**明确可感知**的镜头单元；
- 不再隐藏内部随机 cut；
- Picture Edit 成为“主动选镜头”，不是“被 Seedance 内部剪辑牵着走”。

用户反馈：`这次的效果不错，按这个方案先进行固化`。

### Promoted lesson

Picture Edit 同时审计：
1. external fragment count；
2. perceptible visible-shot count。

抒情/诗意 MV 默认：
`long-cut first / semantic-hit inside shot`。

`Anchor Word != Cut`
`Lyric start != Cut`

对于约 35–40s 抒情 MV，8–12 external block 可作为初始参考，但不是硬配额；最终看 visible-shot flow。

---

## Phase H｜W09 Subtitle：为什么这一段会反复，以及如何彻底防止

### First mistake｜A/B/C over-exploration

画面已经锁后，系统尝试 A/B/C 三套字幕：
- 克制电影感；
- 清晰度优先；
- 平衡版。

用户反馈：三套都一般，要求回到 R1 已经验证的字幕标准。

Lesson：已有 Golden baseline 时，每首歌重新设计字幕属于低价值循环。

### Second mistake｜prose spec proxy != actual Golden visual

系统读取 R1 文档描述后做了一版“近似 R1”，但用户用实际 R1 截图指出明显不一致：
- 字号/字重；
- 背景框；
- padding；
- 整体视觉存在感。

Lesson：Golden visual 如果只保存 prose 描述，仍可能发生 drift；实际 accepted screenshot / implementation asset 的优先级更高。

### Third correction｜padding geometry

用户要求：
- 底框不要左右过长；
- 上下左右多出区域应一致；
- 字必须在框内真正居中。

先测 actual rendered glyph bbox，再给四边统一 padding。
22px 仍偏大，最终用户选 `10px`。

### Fourth bug｜22px → 10px legacy rounded-path inset

为了快，曾直接把旧圆角路径每边内收 12px。
`好吧哎哟哎哟` 短句出现明显偏心，而其他长句不明显。

Root cause：圆角矩形含 Bézier/control points，旧路径变换不是可靠的 bbox re-generation。

### Final correct algorithm

每一句：
1. 用最终字体/字号/换行真实渲染；
2. 获取 actual glyph/text pixel bbox；
3. 从 bbox **fresh generate** rounded rectangle；
4. top/right/bottom/left 各 `10px`；
5. text center 与 box center 误差 `<=1px`；
6. all-line geometry QA；
7. shortest line 必须专项抽查。

最终 10 行全部：`10/10/10/10px PASS`。

### Locked subtitle baseline｜720×1280

- `Noto Sans CJK SC Bold` family；
- nominal `46px`；
- near-white；
- center ~`x360 / y1009`；
- dark semi-transparent rounded box；
- `10px` equal padding；
- max 2 lines；
- fade `100ms in / 180ms out`；
- no default karaoke。

### Promoted lesson

以后默认**直接复用**。
不再每首歌 A/B/C。

只有用户明确要求新的字幕审美才重开 Style Exploration。
实现 bug 只能修实现，不得借机重新设计整套字幕。

---

## Phase I｜W10 Final QA

Final machine QA result：
- H.264 `720×1280`
- 24fps
- 891 frames
- picture `37.125s`
- locked audio `37.120s`
- audio vs locked BGM global lag `0.000000s`
- subtitle max implementation delta `0.005s`
- blackdetect events `0`
- all subtitle geometry PASS
- WEB corner watermark-risk sampled clear
- source metadata stream-copy cleaned without retime
- final SHA `ac0cc8da59cebad3485a6da13c7d9a6d1ff00d4baaafbe2ffdfce2405b939286`

用户最终反馈：当前已经 OK，可以收口。

---

# 4. Final single-path SOP｜future production

| Stage | 系统主要工作 | Durable Output / Gate | 人工 |
|---|---|---|---|
| 1 Song | 3–5 候选、基本核验 | `REFERENCE_BGM_LOCKED` | **HG01 选歌** |
| 2 BGM | exact source、完整截取、fade、SHA | `BGM_LOCKED` | **HG02 听片段** |
| 2A Timeline | strong evidence、forced alignment/LRC、SRT、anchors、events、QA | `AUDIO_TIMELINE_PACKAGE_LOCKED` | 正常无；异常 CHG-A |
| 3 Beat | Natural Beat / emotion / hook peak release | `DIRECTOR_BEAT_MAP` | AUTO |
| 4 Director | visual world / production allocation / edit roles | `DIRECTOR_PLAN_LOCKED` | AUTO，和首帧合并看 |
| 5 First Frames | 0s anchors + set QA | `FIRST_FRAME_SET_LOCKED` | **HG03** |
| 6 Dynamic | 1–2镜默认，3镜任务型 | `DYNAMIC_PROMPT_SET_READY` | 外部执行，不是审美 Gate |
| 7 Source QA | clean/risk/internal cuts/status | `VISUAL_SOURCE_MAP` / `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT` | 只有需重生 CHG-B |
| 7.5 Normalize | Atom/Arc / source audio strip / WEB crop | `SHOT_LIBRARY_READY` | AUTO |
| 8A Audio Gate | BGM Package revalidation | `EDITOR_AUDIO_GATE_PASS` | AUTO |
| 8B Edit | 3 clocks + long-cut + fragmentation QA | `EDIT_MAP_LOCKED` / preview | **HG04** |
| 9 Subtitle | locked baseline + geometry/timing QA | `SUBTITLE_IMPLEMENTATION_QA_PASS` | AUTO；换风格才 CHG-C |
| 10 Final | technical/full-watch/package | `FINAL_TECH_QA_PASS / DELIVERABLE_RENDERED` | **HG05** |
| 11 Close | preserve reproducible assets | `COMPLETE_LOCKED` | 用户 Final PASS 后自动收口 |

正常目标：**用户只需要 5 次人工确认。**

---

# 5. Fixed QA Gates｜what users should no longer have to catch

以下问题以后原则上不应该再由用户第一个发现：

## Audio
- wrong master/version；
- excerpt 前句污染；
- 句尾截断（HG02前机器先检查，最终听感用户确认）；
- BGM SHA mismatch；
- waveform guess 冒充 strong timeline；
- repeated chorus occurrence 串错；
- edit stage 重新猜 lyric timeline。

## Dynamic source
- source audio track 混入；
- 明显 topology risk window 未标记；
- duplicate shot 没有在 source map 中指出；
- multi-shot source 内部 cut 未映射就直接编辑。

## Picture Edit
- Anchor=Cut 的机械逻辑；
- 只统计 external fragments 不统计 visible shots；
- source 内多镜 + 外部多切叠加；
- 结尾没有 release；
- WEB 水印左右角漏出；
- SAR/9:16 拉伸。

## Subtitle
- 每首歌重新 A/B/C；
- timing 根据 picture cut 修改；
- character-count 估算 box width；
- legacy rounded path 缩放；
- padding 四边不一致；
- 短句偏心；
- 长句/两行出安全区。

## Final
- black frame；
- audio lag；
- source audio leakage；
- metadata/codec/SAR 问题；
- ZIP 不完整。

---

# 6. Rollback matrix｜avoid cascade rework

未来出现问题，只回最近根因：

| 现象 | 回滚 |
|---|---|
| 歌不合适 | Stage 1 |
| BGM截取不舒服 | Stage 2；之后重建 2A |
| singer timeline 真值错 | Stage 2A |
| Director/世界不对 | Stage 4/5 |
| 单条动态崩 | Stage 6/7，仅该 source |
| 多镜隐藏碎片 | Stage 7.5 |
| Picture太碎/节奏乱 | Stage 8B；先重排 Atom，不先重生 |
| subtitle padding/偏心/overflow | Stage 9 implementation |
| subtitle singer sync 真值错 | Stage 2A，不是 Stage 9 |
| Final codec/SAR/metadata | Stage 10 |

核心：**Patch, Don't Cascade。**

---

# 7. Remaining bottlenecks / still needs human or external capability

## 7.1 Song aesthetic｜必须人工

推荐系统可以缩小候选，但“我愿不愿意做这首”“这个感觉对不对”仍然是用户主观价值判断。

Status：不可消除，正确保留 HG01。

## 7.2 BGM final excerpt comfort｜必须人工

机器可以找到句子边界，但“前面再多 0.5 秒是否更舒服”“多留一句是否更有余韵”属于听感。

Status：正确保留 HG02。

## 7.3 Audio forced-alignment runtime availability｜技术卡点，正常应自动

WEB R2 为完成中文 CTC forced alignment，经历了模型/依赖/DNS 的工程恢复与 ferry。
未来标准 runtime 已锁 model/tool identity，但网页端环境若不能直接拿到模型，仍可能 `AUDIO_ALIGNMENT_RUNTIME_BLOCKED`。

正确策略：
- 不降级 waveform guess；
- 优先 Route A same-version LRC；
- Route B runtime doctor；
- 仍不可用才明确 BLOCKED/条件人工处理。

这是当前最值得继续工程自动化的技术卡点。

## 7.4 External Seedance generation｜能力边界

目前用户仍负责把首帧/提示词提交给外部模型，并回传动态视频。

这不是流程不稳定，而是网页端工具连接边界。

未来 Codex/API 能直接生成/取无水印 HD 时，可以自动化 W06-X，但不改变 Workflow Gate。

## 7.5 Visual beauty / First-frame whole-set taste｜必须人工

机器可以做重复、构图、可执行性 QA，但“整组够不够好看、歌词命中是否有感觉”仍需 HG03。

## 7.6 Picture Edit emotional rhythm｜必须人工

Fragmentation/clock/technical QA 可机器做，但“舒服不舒服”“高潮/呼吸对不对”仍是导演听感。

保留 HG04。

## 7.7 WEB watermark cleanup｜暂时技术限制

当前 WEB fallback 是 batch uniform crop/zoom；会牺牲一定构图和原生清晰度。
Codex/无水印 HD 源才是 publish-grade 首选。

流程已经稳定，但能力仍可升级。

## 7.8 Final acceptance｜必须人工

任何自动 QA 都不能替代创作者最终授权。
保留 HG05。

---

# 8. What should be automated next

优先顺序：

1. **Audio Alignment Environment bootstrap**：让 Route B 在新环境更少 ferry/block；
2. **Shot internal-cut detection + Atom extraction**：W07.5 自动化程度继续提高；
3. **Subtitle bbox render/QA script productization**：当前算法已锁，变成标准 tool；
4. **WEB/Codex source ingest**：自动 strip audio、hash、probe、watermark-risk sample；
5. **Picture Fragmentation report**：自动统计 external/visible shot count、<2s cluster、A-B-A；
6. **Final QA command**：统一执行 audio lag / blackdetect / SAR / subtitle implementation / package integrity。

不要优先自动化：
- song aesthetic；
- final BGM comfort；
- final visual taste；
- final acceptance。

自动化目标不是“取消所有人”，而是让用户只做真正有价值的判断。

---

# 9. Repository promotion map after close

Authoritative reusable runtime：
- `04_HARNESS/workflows/mv.md` v1.7
- `04_HARNESS/rules/mv_golden_runtime.md` v1.4
- `04_HARNESS/rules/mv_audio_timeline.md` v1.0
- `04_HARNESS/rules/mv_human_gates.md` v1.0
- `04_HARNESS/rules/mv_editing.md` v1.1+
- `04_HARNESS/rules/mv_source_normalization.md` v1.0
- `04_HARNESS/rules/mv_subtitle.md` v1.0
- `04_HARNESS/rules/ai_video.md` v1.3+
- `04_HARNESS/templates/mv_zero_context_start_prompt.md` v1.0

Round evidence remains in：
`06_TESTS/MV/WEB_R2/`

原则：
**Runtime 读取 Rule；排错才读历史。**

---

# 10. Definition of a successful next Round

下一首 MV 如果这套流程真正固化成功，应看到：

- 不再在 Edit 阶段重新找歌词时间；
- 不再因 subtitle sync 反推 Picture timeline；
- 不再把 5 秒 multi-shot source 当黑盒；
- 第一次 Picture rough cut 就基于 Atom/Arc；
- 不再先做 A/B/C 字幕候选；
- 不再让用户指出左右角水印、字幕框偏心等 implementation defect；
- 用户正常只需要 5 次确认；
- 出问题时只改最近根因，不级联重做整个项目。

如果下一 Round 仍出现同类重复返工，则说明对应 lesson 尚未真正被 Gate 自动阻断，应再次按：

`failure -> root cause -> rule -> artifact/state -> independent Gate -> regression`

进行升级。

---

# 11. Final R2 judgment

WEB R2：`PASS / PROMOTABLE`。

最终流程不应被描述为“全自动 MV”。更准确的是：

> **高自动化、强 Gate、少数高价值人工审美决策的 MV 生产流水线。**

这是当前比“尽量所有步骤 AUTO”更稳定、更可复刻的目标状态。
