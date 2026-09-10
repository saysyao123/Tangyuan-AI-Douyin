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

`核心账号/歌库 → 具体抖音参考 → 用户下载 → BGM/Audio Version Lock → Full Timeline Lock → Segment Production Plan → Reference Deconstruction → Animation Director → K0 → Dynamic Prompt → Dola/Seedance 2.5 → QA → 单变量迭代 → Lock`

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
- **Generated Clip Duration**：允许更长，用于给剪辑保留前后 handle。
- 核心有效动作/画面放在生成素材中部，避免关键内容紧贴生成首尾。
- 是否 Promote 为 Skill 通用规则，必须经过真实生成/剪辑验证。

当前项目：Final A=`8.700s`，Final B=`6.670998s`；Generation A/B 均=`10.000s`。

## 2.3 Segment Transition｜CURRENT PROJECT

当前《爱让人脑袋空空》A→B 使用 **Hard Cut / 硬切**：

- 不做 crossfade / morph；
- 不要求首尾动作连续；
- 只保持角色身份、世界观、色彩逻辑、情绪因果；
- B 主动改变景别/机位/朝向/空间层次之一，使硬切成为明确导演选择。

## 2.4 内容与动画视觉

- 歌词视觉命中 > 轻叙事连续 > 炫技。
- 人物：高辨识动画轮廓、姿态张力、动作表现力；不复制具体受保护角色。
- 场景：明亮、治愈、通透、强天气/天空/光影空气感；不复制具体场景。
- 怪物/物品：温柔奇幻、灵性、陪伴感；不复制具体角色/道具。

## 2.5 Core Song Pool｜HARD

- 用户提供的 9 个核心账号全部进入 Song Pool。
- Primary Role 只决定权重，不决定是否纳入歌曲。
- 视觉账号歌曲同样计入；跨核心账号重复提高 Song Family 信号。
- 更新采用 BEST EFFORT，不追求伪最新。
- supplemental / 汽水音乐只作佐证，不替代核心账号。

## 2.6 Douyin Reference

负责：选歌、歌词/卡点、动作、镜头、能量曲线、Peak、Ending。

迁移 Structure，不迁移真人身份、脸、原服装、原场景和具体视觉表达。

## 2.7 Current Generation Adapter

- Dola / Seedance 2.5 I2V。
- 默认最简输入：**K0 + Dynamic Prompt**。
- refs ≤3–5；单 K0 足够就不加图。
- DEPTH 仅为未来 Motion Adapter，不是当前必经。

## 2.8 Motion

- K0 = 可表演的 0 秒动态锚点。
- 位移必须有可读抬脚→落脚→蹬地→重心转移→加减速；禁止无足部逻辑滑行/漂移。
- Prompt 正向目标优先，不因单次失败无限堆禁止项。

---

# 3. Master Flow v1.3｜TIMELINE + EDIT-HANDLE

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
    - final BGM segment
    - generation duration
    - pre/post handles
    - transition policy
↓
M6  REFERENCE DECONSTRUCTION
↓
M7  ANIMATION DIRECTOR
↓
M8  K0-A / K0-B
↓
G3  HUMAN K0 GATE
↓
M9  DYNAMIC PROMPTS
↓
M10 DOLA / SEEDANCE 2.5 I2V
↓
M11 TRIM HANDLES / HARD CUT ASSEMBLY
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
3. K0 Gate：强制。
4. Video QA Gate：好看吗 / 歌词情绪命中吗 / 动作镜头自然吗 / 值得重复吗。

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
- [x] E00 基于 Timeline：Final A=`8.700s`；Final B=`6.670998s`。
- [ ] E01 5–7 / 8–10 / 10–15 跨项目生成验证；当前项目将实际覆盖前两档。
- [x] E02 切点 `8.700s`；A→B 使用硬切。
- [x] E03 当前项目：Generation A=`10s`、B=`10s`；核心画面置中并留 handles。
- [ ] E04 Promote（真实生成/剪辑 QA 后再判断）。

Evidence：`06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v1.md`。

## Phase F｜Reference Deconstruction
- [x] F00 最小 Reference Map。
- [x] F01 动作/重心/Camera/Energy/Ending 结构。
- [x] F02 Structure Transfer / Copy Boundary。
- [x] F03 A/B 按 Timeline 实际拆解。
- [x] F04 已形成足够 Director 输入，不复制原场景。
- [ ] F05 真实生成后验证拆解是否足够。
- [ ] F06 Promote。

Evidence：`07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`。

## Phase G｜Animation Director
- [ ] G00 Locked Timeline + Segment Plan + Reference → Director。
- [ ] G01 A/B 共用角色/世界观，但分别独立成段。
- [ ] G02 A 设计 hard-cut punctuation；B 设计 hard-cut restart。
- [ ] G03 每段 10s 中 3–5 个主要视觉事件。
- [ ] G04 原创视觉边界。
- [ ] G05 用户/生成实测。
- [ ] G06 Promote。

## Phase H｜K0
- [ ] H00–H06：K0 定义 → A/B 首帧 → Gate → 生成改善验证 → Promote。

## Phase I｜Dynamic Prompt
- [ ] I00–I06：Timeline+Director+K0 → 动作/Camera/Physics/Ending → 实测/Promote。

## Phase J｜Generation
- [ ] J00–J06：Dola/Seedance 2.5 → K0+Prompt → refs≤3–5 → 10s A/B 实测 → Evidence → Promote。

## Phase K｜QA / Iteration
- [ ] K00–K06：四问 → Tech QA → S/R/D/K/P/G → 最近责任层 → 单变量 → 闭环 → Promote。

## Phase L｜Assembly
- [ ] L00 只用 QA PASS 素材。
- [ ] L01 Trim A/B handles，对齐 BGM 0.000/8.700/15.371。
- [ ] L02 A→B hard cut，无强制流畅过渡。
- [ ] L03 Final continuity / audio / ending QA。

## Phase M｜DEPTH Adapter
- [ ] M00–M06 Skill integration。
- 当前转换链：`VALIDATED / integration pending`。

## Phase N｜Skill IA
- [ ] N00–N05：名称/触发 → 最小 SKILL.md → references/scripts → 唯一事实源 → 弱模型。

## Phase O｜Full Real Project
- [ ] O00–O06：Reference → Timeline → Segment → Director → K0 → Generation → QA → PASS/明确失败。

## Phase P｜oil-skill-creator Evaluation
- [ ] P00–P06：Review → evals → with/without → objective/subjective → Human Review → regression。

## Phase Q｜Open Source
- [ ] Q00–Q05：清理单次资产 → 最小 Skill → README → validation → publish → clean rerun。

---

# 6. Current Active Module

**ACTIVE MODULE：Phase G｜《爱让人脑袋空空》Animation Director**

Locked upstream：

- Audio：selected Reference AAC
- BGM：`15.370998s`
- Timeline：`TIMELINE_LOCKED v1`
- Final Segment A：`0.000–8.700s`
- Final Segment B：`8.700–15.370998s`
- Generation：A=`10s`；B=`10s`
- A handle/core：`0–0.600 / 0.600–9.300 / 9.300–10.000`
- B handle/core：`0–1.500 / 1.500–8.170998 / 8.170998–10.000`
- Transition：`Hard Cut at BGM 8.700s`
- Reference Deconstruction：`07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`

下一步唯一任务：为 A/B 分别建立简洁 Animation Director Plan；每段只保留 3–5 个主要视觉事件。Director 锁定后再生成 K0-A / K0-B。

---

# 7. 恢复协议

项目状态至少记录：Project / Song / Primary Reference / Audio Version / Timeline Version+Status / Final Segment / Generation Duration / Handle Window / Transition / Director / K0 / Prompt / Generation / QA / Next Action。

若 `Timeline Status != LOCKED`：禁止 Director / K0 / Prompt / Generation。