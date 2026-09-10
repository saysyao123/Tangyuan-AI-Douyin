# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Role: 构建阶段唯一总控事实源。

---

# 0. 使用规则

1. 新对话先读本文件。
2. 找 `Current Active Module`，只读对应 Evidence。
3. `[x]` 必须有真实证据 / 用户确认 / 可复核产物。
4. 每次只推进当前模块；单次成功不能直接 Promote。
5. 状态：`EXPERIMENT → VALIDATED → PROMOTED → RETIRED`。
6. **HARD：取得具体 BGM 后，必须先 Full Timeline Lock；未 LOCKED 不得进入 Director / K0 / Prompt / Generation。**

---

# 1. 当前生产目标

建立稳定、简单、可恢复的**动画 MV Reference-First Skill**。

`核心账号/歌库 → 具体抖音参考 → 用户下载 → BGM/Audio Version Lock → Full Timeline Lock → Segment Production Plan → Reference Deconstruction → Multi-shot Animation Director → K0(first-shot anchor) → Multi-shot Dynamic Prompt → Dola/Seedance 2.5 → Trim/Hard Cut → QA → 单变量迭代 → Lock`

---

# 2. 已锁定 / 当前验证中的原则

## 2.1 Timeline First｜HARD

顺序固定：

`BGM Lock → Full Timeline Lock → Segment Plan → Director`。

Timeline 至少包含：精确总时长、逐句歌词/声音事件、Beat/Accent/Transition、情绪边界、合法切点、Peak/Release/Ending。

- 有不确定点：标 `NEED_VERIFY` 并停止下游。
- 换 BGM / Audio Version：Timeline 及全部下游失效。
- 只改视觉：不得反向修改已锁 Timeline。

## 2.2 Final Duration vs Generation Duration｜EXPERIMENT

- **Final Segment Duration**：由锁定 BGM/Timeline 决定。
- **Generated Clip Duration**：由导演/剪辑需要决定，可在当前允许的 **5–15s** 内灵活选择。
- Generated Clip 可以长于 Final Segment，用于保留 pre/post handles。
- 核心有效画面尽量放在素材中部；不要让关键动作紧贴生成首尾。
- 生成条数也不是固定 2 条；若场景/镜头/剪辑覆盖确有需要，可增加 5–15s coverage clip。

当前项目：

- Final A=`8.700s`；Generation A=`12.000s`
- Final B=`6.670998s`；Generation B=`10.000s`
- Optional C：仅解决明确 coverage 问题时增加。

## 2.3 Multi-shot Director｜HARD FOR CURRENT ROUTE

当前 MV **不采用“一条生成视频 = 一镜到底”**。

- 每条 5–15s 生成素材内部允许/鼓励多镜头。
- Shot 数由歌词单元、Beat/Accent、情绪转折、场景需要决定，不设固定配额。
- 当前 10–12s 素材建议约 4–6 个主要镜头，仅为经验起点。
- 每个关键歌词/音乐节点尽量对应明确视觉事件：人物动作 / 景别 / 机位 / 环境变化之一或组合。
- 内部镜头可 hard cut / motivated cut；不追求 morph / 无缝长镜头。
- K0 只负责**第一镜头的 0 秒锚点**，不约束整条视频维持同一机位。
- Dynamic Prompt 必须显式写 Shot timeline / CUT cues。

借鉴此前高动态“疯批打戏”有效逻辑：

`动作推进 + 镜头推进 + 空间/环境推进 + 卡点视觉事件 + 动作完成后的余韵`。

转译为情绪动画，不复制打斗动作；所有动态服务歌词和音乐。

## 2.4 Segment Transition｜CURRENT PROJECT

《爱让人脑袋空空》A→B 在 `BGM 8.700s` 使用 **Hard Cut**：

- 不做 crossfade / morph；
- 不要求首尾动作连续；
- 保留角色身份、世界观、色彩逻辑、情绪因果；
- B 主动改变景别/机位/朝向/空间层次至少一个维度。

## 2.5 内容与动画视觉

- 歌词视觉命中 > 轻叙事连续 > 炫技。
- 人物：高辨识动画轮廓、姿态张力、动作表现力；不复制具体受保护角色。
- 场景：明亮、治愈、通透、强天气/天空/光影空气感；不复制具体场景。
- 怪物/物品：温柔奇幻、灵性、陪伴感；不复制具体角色/道具。

## 2.6 Core Song Pool｜HARD

- 用户提供的 9 个核心账号全部进入 Song Pool。
- Primary Role 只决定权重，不决定是否纳入歌曲。
- 视觉账号歌曲同样计入；跨核心账号重复提高 Song Family 信号。
- 更新采用 BEST EFFORT，不追求伪最新。
- supplemental / 汽水音乐只作佐证，不替代核心账号。

## 2.7 Douyin Reference

负责：选歌、歌词/卡点、动作、镜头、能量曲线、Peak、Ending。

迁移 Structure，不迁移真人身份、脸、原服装、原场景和具体视觉表达。

## 2.8 Current Generation Adapter

- Dola / Seedance 2.5 I2V。
- 默认最简输入：**K0 + Dynamic Prompt**。
- refs ≤3–5；单 K0 足够就不加图。
- DEPTH 仅为未来 Motion Adapter，不是当前必经。

## 2.9 Motion

- K0 = 第一镜头可表演的 0 秒动态锚点。
- 位移必须有可读抬脚→落脚→蹬地→重心转移→加减速；禁止无足部逻辑滑行/漂移。
- Prompt 正向目标优先，不因单次失败无限堆禁止项。

---

# 3. Master Flow v1.4｜TIMELINE + MULTI-SHOT

```text
M0  CORE ACCOUNT MUSIC DATABASE
↓
M1  CORE DOUYIN VIDEO SELECTION
↓
G1  HUMAN REFERENCE GATE
↓
M2  USER PROVIDES SELECTED VIDEO
↓
M3  BGM / AUDIO VERSION LOCK
↓
M4  FULL TIMELINE LOCK ← HARD
↓
G2  TIMELINE GATE
↓
M5  SEGMENT PRODUCTION PLAN
    - final BGM duration
    - generated material duration (5–15s)
    - handles
    - number of source clips if needed
    - transition policy
↓
M6  REFERENCE DECONSTRUCTION
↓
M7  MULTI-SHOT ANIMATION DIRECTOR
    - lyric/beat → visual event
    - shot timeline / cuts
    - character/camera/environment motion
↓
G3  DIRECTOR GATE
↓
M8  K0-A / K0-B (FIRST-SHOT ANCHORS)
↓
G4  HUMAN K0 GATE
↓
M9  MULTI-SHOT DYNAMIC PROMPTS
↓
M10 DOLA / SEEDANCE 2.5 I2V
↓
M11 TRIM HANDLES / HARD-CUT ASSEMBLY
↓
M12 TECH QA
↓
M13 HUMAN QA
↓
PASS → LOCK
FAIL → CLASSIFY → ONE-VARIABLE ITERATION
↓
M14 FINAL ASSEMBLY
↓
M15 FINAL QA / LOCK
```

---

# 4. Human Gate 最小集合

1. Reference Gate：用户选择具体抖音作品。
2. Timeline Gate：硬检查点；无阻塞歧义才通过。
3. **Director Gate**：确认镜头密度、主要视觉事件和段落动态方向后再生 K0。
4. K0 Gate：确认第一镜头锚点/角色/场景。
5. Video QA Gate：好看吗 / 歌词情绪命中吗 / 动作镜头自然吗 / 值得重复吗。

---

# 5. Skill 构建清单

## Phase A｜产品 / Flow
- [x] A00 逐段构建。
- [x] A01 Reference-First。
- [x] A02 Reference / DEPTH / Visual 分层。
- [x] A03 oil-skill-creator 方法。
- [x] A04 总控工作区。
- [x] A05 Master Flow 边界。
- [x] A05.1 Timeline-First 修正。
- [x] A05.2 Multi-shot 修正：不把生成视频默认成一镜到底。
- [ ] A06 最终 Skill 名称 / 触发 / 反向边界。

## Phase B｜Core Account Music Database
- [x] B00–B06：恢复 9 核心账号、89 条历史 work、统一 Song Pool、Best-Effort 更新。
- [ ] B07 Promote（待完整真实项目闭环）。

Evidence：`01_REFERENCE_ACCOUNT_REGISTRY.md`、`02_SONG_POOL_RECOVERY.csv`、历史 `works.csv`。

## Phase C｜Reference Selection / Handoff
- [x] C00 Core Song Pool 候选。
- [x] C01 每轮最多 3 个。
- [x] C02 直链/账号/时长/证据/适配/Risk。
- [x] C03 用户选择 `爱让人脑袋空空`。
- [x] C04 用户上传具体 Reference。
- [ ] C05 完整真实闭环。
- [ ] C06 Promote。

Evidence：`04_SELECTION_ROUND_01.md`。

## Phase D｜BGM / Full Timeline
- [x] D00 技术探测：15.370998s / 1920×1080 / 30fps / AAC 44.1kHz stereo。
- [x] D01 锁所选 Reference 内音频版本。
- [x] D02 0.000–15.371 全歌词/声音时间轴。
- [x] D03 Beat/Accent/Transition/Emotion；约129.2 BPM。
- [x] D04 合法切点；首选 `8.700s`。
- [x] D05 Timeline QA。
- [x] D06 `TIMELINE_LOCKED v1`。
- [ ] D07 技术步骤脚本化判断。
- [ ] D08 Promote（需跨项目）。

Evidence：`05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`。

## Phase E｜Segment Production Plan
- [x] E00 Final A=`8.700s`；Final B=`6.670998s`。
- [x] E01 当前项目按导演需要决定 Generation：A=`12s`，B=`10s`；不是全局固定时长。
- [x] E02 Final cut `8.700s`；A→B hard cut。
- [x] E03 Generated material 保留 handles；必要时增加 5–15s coverage clip。
- [ ] E04 Promote（真实生成/剪辑 QA 后）。

Evidence：`06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md`；v1 已 superseded。

## Phase F｜Reference Deconstruction
- [x] F00 最小 Reference Map。
- [x] F01 动作/重心/Camera/Energy/Ending。
- [x] F02 Structure Transfer / Copy Boundary。
- [x] F03 A/B 按 Timeline 实拆。
- [x] F04 足够 Director 输入。
- [ ] F05 真实生成后验证。
- [ ] F06 Promote。

Evidence：`07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`。

## Phase G｜Multi-shot Animation Director
- [x] G00 Locked Timeline + Segment Plan + Reference → Director Draft。
- [x] G01 A/B 共用角色/世界观，各自独立多镜头成段。
- [x] G02 A hard-cut punctuation；B hard-cut restart。
- [x] G03 歌词/Beat 驱动 shot density；当前 A=5 principal shots，B=4 principal core shots。
- [x] G04 人物动作 + Camera + Environment 三层动态，原创视觉边界明确。
- [ ] G05 Human Director Gate / 真实生成验证。
- [ ] G06 Promote。

Evidence：`08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v2.md`。

## Phase H｜K0
- [ ] H00 K0 仅锚定每条生成素材第一镜头。
- [ ] H01 K0-A / K0-B 首帧方案。
- [ ] H02 Human K0 Gate。
- [ ] H03–H06 生成改善验证 → Promote。

## Phase I｜Multi-shot Dynamic Prompt
- [ ] I00 Timeline + Director + K0 编译。
- [ ] I01 显式 Shot 1 / CUT / Shot 2 时间结构。
- [ ] I02 歌词/Beat、动作链、Camera、Environment、Ending。
- [ ] I03–I06 正向优先 / 无滑行 / 实测 / Promote。

## Phase J｜Generation
- [ ] J00–J06：Dola/Seedance 2.5 → K0+multi-shot prompt → refs≤3–5 → A12s/B10s → Evidence → Promote。

## Phase K｜QA / Iteration
- [ ] K00–K06：四问 → Tech QA → S/R/D/K/P/G → 最近责任层 → 单变量 → 闭环 → Promote。

## Phase L｜Assembly
- [ ] L00 只用 QA PASS 素材。
- [ ] L01 Trim handles，对齐 BGM 0.000/8.700/15.371。
- [ ] L02 A→B hard cut；内部镜头也允许明确剪切。
- [ ] L03 Final continuity / audio / ending QA。

## Phase M｜DEPTH Adapter
- [ ] M00–M06 Skill integration。
- 当前转换链：`VALIDATED / integration pending`。

## Phase N｜Skill IA
- [ ] N00–N05：名称/触发 → 最小 SKILL.md → references/scripts → 唯一事实源 → 弱模型。

## Phase O｜Full Real Project
- [ ] O00–O06：Reference → Timeline → Segment → Multi-shot Director → K0 → Generation → QA → PASS/明确失败。

## Phase P｜oil-skill-creator Evaluation
- [ ] P00–P06：Review → evals → with/without → objective/subjective → Human Review → regression。

## Phase Q｜Open Source
- [ ] Q00–Q05：清理单次资产 → 最小 Skill → README → validation → publish → clean rerun。

---

# 6. Current Active Module

**ACTIVE MODULE：Phase G / G05｜《爱让人脑袋空空》Multi-shot Director Gate**

Locked upstream：

- BGM=`15.370998s`
- Timeline=`TIMELINE_LOCKED v1`
- Final A=`0.000–8.700s`
- Final B=`8.700–15.370998s`
- Generation A=`12s`；B=`10s`
- Final A→B=`Hard Cut @ 8.700s`
- Segment Plan=`06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md`
- Reference Map=`07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`
- Director Draft=`08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v2.md`

Current Director density：

- A：5 principal shots / 8.700s final content
- B：4 principal core shots / 6.671s final content
- 全片约 9 个主要镜头；镜头数服从歌词/Beat，不作为未来固定模板。

**当前禁止生成 K0，直到 Multi-shot Director Gate 通过。**

通过后唯一下一步：K0-A / K0-B 只设计第一镜头锚点，然后编译 multi-shot Dynamic Prompt。

---

# 7. 恢复协议

项目状态至少记录：Project / Song / Primary Reference / Audio Version / Timeline Version+Status / Final Segment / Generated Material Duration / Handle / Shot Plan / Transition / Director / K0 / Prompt / Generation / QA / Next Action。

若 `Timeline Status != LOCKED`：禁止 Director / K0 / Prompt / Generation。