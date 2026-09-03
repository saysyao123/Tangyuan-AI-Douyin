# Workflow｜AI MV Production v2.0 Lean Interface

> Status: `AUTHORITATIVE AGENT WORKFLOW / CANONICAL RUNTIME BACKED`
> Role: 给 Agent / 用户提供最小可执行 MV 心智模型；不复制底层 Stage、Artifact、Transition、Gate 的机器定义。
> Core: **锁定声音真值 -> 形成可生产视觉意图 -> 生产可剪素材 -> 完成画面编辑 -> 技术交付与闭环。**

## 0. Authority

本文件只负责“当前要解决什么问题”和 Macro Phase 之间的生产意图。

机器权威：
- Stage：`runtime/mv_stage_registry.json`
- Transition：`runtime/mv_transition_contract.json`
- Human Gate：`runtime/mv_human_gate_registry.json`
- Artifact：`runtime/mv_artifact_registry.json`
- Macro Phase 映射：`runtime/mv_macro_phase_registry.json`

若本文件中的解释与 Canonical Runtime 冲突，以机器权威为准。

不要读取整个 S00–S18 链来执行普通任务；先从 current canonical stage 派生当前 Macro Phase，再只加载当前任务 JIT 模块。

---

# Macro Path

`AUDIO -> DIRECT -> GENERATE -> EDIT -> DELIVER`

这 5 个 Phase 是认知/生产层，不替代底层 Canonical Stage。

---

# 1. AUDIO｜锁定唯一声音真值

### Goal
确保后续所有歌词、导演、剪辑、字幕都建立在同一个真实音频版本和时间坐标上。

### Work
按当前任务 JIT 完成：
- 歌曲候选与版本发现；
- 实际可试听 BGM 片段；
- 用户审美/听感决定；
- exact audio identity；
- trusted lyric/music timeline package。

### Human Decisions
底层仍保留 `HG01` 与 `HG02` 两个独立 durable decision。
用户交互可以在信息已经完整时合并成一次提交，但两个判断必须分别明确，Runtime receipt 仍分别记录，禁止伪造或跳过。

### JIT
- 版本发现：`rules/mv_bgm_discovery.md`
- BGM 锁定后：`rules/mv_audio_timeline.md` + 对应 tools

### Exit Outcome
Canonical Runtime 已证明 exact BGM 与 Audio Timeline 可供下游使用。

---

# 2. DIRECT｜把歌词变成可生产视觉意图

### Goal
不是先套镜头配方，而是为每个 Natural Beat 找到不可替代的视觉答案，并明确它如何成为可生成、可剪辑的素材任务。

### Work
- Natural Beat / Hook / Peak / Release；
- 世界、人物、材质和视觉母题；
- 每个 Beat 的 `INTENT` 与 dominant visual event；
- Production segment / source role；
- 人物动作与摄影机关系；
- Reference / K0 设计；
- 视觉差异、连续性、可执行性检查。

### Core Rules
- `lyric visual hit > light narrative continuity > camera trick`；
- conceptual beat、Reference 数量、生成 source 数量、最终剪辑段数不是同一个概念；
- 实际已接受 Reference/K0 像素高于旧 Director prose；
- 不为了流程完整而强制固定镜头数量或固定 camera recipe。

### Human Decision
`HG03` 当前仍保留为 Canonical durable Gate。
是否未来改为 Conditional，必须由 Seedance 2.5 Benchmark 证明，不在本次 Lean refactor 中先验删除。

### JIT
- 首帧/Reference QA：`rules/mv_first_frame_qa.md`
- AI Reference / I2V：`rules/ai_video.md`
- 需要时加载少量当前歌曲 Benchmark / Knowledge

### Exit Outcome
Natural Beat、Director allocation、实际视觉 Anchor 已可直接交给素材生产。

---

# 3. GENERATE｜生产可剪素材，而不是“生成任务记录”

### Goal
以最少生成与返工获得足够的 usable material。

### Work
- 由当前 Production task 编译生成 Prompt；
- 外部 Provider / Seedance 生成；
- 检查 identity、事件完成度、明显拓扑/物理问题；
- 记录 usable windows、risk windows、source role；
- 能 trim 就 trim，只有无法获得足够 clean material 时才局部 regen；
- 多镜/隐藏切镜被实际证明后，再启用 Atom/Arc normalization；
- 编辑前重新验证锁定音频身份。

### Material-first Output
每条 source 的核心问题只有：
1. 能不能剪？
2. 哪几秒能剪？
3. 承担什么角色？
4. 真正失败点是什么？
5. 下一步唯一动作是什么？

推荐最小 QA 语义：
`STATUS / USABLE / FAILURE / NEXT`。

### Duration Strategy｜Seedance 2.5 Trial
当前实验只研究：
- `PRECISION = 5–8s`
- `STANDARD = 8–15s`
- `EXTENDED = 15–20s`

三者共用同一生产链，只是 Duration Strategy，不创建三套 Workflow。
30s 不在当前实验范围。

### Repair Rule
`Patch, Don't Cascade`：单条 source 失败只修该 source 或失败区间；已有 usable window 不因尾部失败自动报废。

### JIT
- 生成控制：`rules/ai_video.md`
- 实际证明 multi-shot complexity 后：`rules/mv_source_normalization.md`
- WEB source cleanup 需要时：`rules/mv_web_source_roughcut.md`

### Human Decision
正常无固定 Human Gate。只有真实异常且机器无法做低成本局部修复时才升级用户。

### Exit Outcome
Material pool 足以进入 Picture Edit，并已通过 Canonical Runtime 的必要技术前置。

---

# 4. EDIT｜用三个时钟组织作品

### Goal
把可用素材组织成完整 MV，而不是追求每条 source 自己成为迷你成片。

### Three Clocks
1. lyric clock；
2. music-event clock；
3. visual-action clock。

前两者来自锁定 Audio Timeline；第三者来自实际素材。

### Work
- 建立 executable edit map；
- 优先保护歌词/音乐真值与完整动作弧；
- 允许 semantic hit 发生在镜头内部；
- 避免因为歌词起点/Anchor Word 机械切镜；
- 检查真实 perceptible shot flow，而不只数 timeline block；
- Picture 通过后再做字幕实现；
- Subtitle timing 只服从 canonical lyric clock，不从 Picture cut 反推。

### Human Decision
`HG04`：用户只判断整体画面节奏、情绪、导演取舍；技术错误应在提交前机器处理。

### JIT
- Picture Edit：`rules/mv_editing.md`
- Subtitle 阶段：`rules/mv_subtitle.md`

### Exit Outcome
Picture rhythm 已接受，字幕实现已通过必要技术 QA。

---

# 5. DELIVER｜验证、交付、发布状态闭环

### Goal
确认作品真实可交付，并把生产结束、真实发布、发布后数据区分为不同 durable truth。

### Work
- Final technical validation；
- source audio leakage / media identity / resolution / SAR / subtitle / major risk checks；
- final media identity/hash；
- release package；
- 用户实际确认发布后再执行 publish sync；
- 单条表现数据进入 learning evidence，不自动重写 Production Rule。

### Human Decision
`HG05`：最终作品接受/发布授权。

### Exit Outcome
Canonical Runtime 负责 Release / Publish / Post-publish 的真实状态推进。

---

# Rollback｜Nearest Cause Only

默认只修最近根因：
- audio identity/timeline → AUDIO；
- visual intent/reference → DIRECT；
- 单条 source / usable material → GENERATE；
- picture/subtitle implementation → EDIT；
- codec/metadata/release implementation → DELIVER。

只有上游事实真的变化时，才让依赖它的下游失效。

---

# Normal Runtime Does Not Load

- 历史 R1/R2/R3 Prompt 全文；
- 历史大型 QA / retrospective；
- 旧 `*_HARNESS.md`；
- `rules/mv_stage_entry_checklist.md` 作为第二套前置条件权威。

需要排错、迁移、回归、规则溯源时再 JIT 读取。
