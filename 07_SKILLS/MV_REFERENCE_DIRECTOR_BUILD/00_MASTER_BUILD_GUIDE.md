# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Purpose: 逐段梳理、验证并固化一套稳定、简单、可恢复的动画 MV Reference-First 生产 Skill。

---

# 0. 本文件的地位

本文件是 **MV Reference Director Skill 构建阶段的唯一总控事实源（Single Source of Truth）**。

新对话 / 换模型 / 上下文过长时：

1. 先读取本文件；
2. 找 `Current Active Module`；
3. 再读取该模块明确指向的文件；
4. 不依赖聊天记忆猜进度；
5. 完成一项后先更新本文件，再进入下一项。

## 勾选规则

- `[ ]` = 未完成或证据不足。
- `[x]` = 已完成，并有真实产物 / 测试 / 用户确认。
- 只有满足 Done Definition 才能勾选。
- 单次成功不能直接 Promote 为 Skill 规则。
- 找不到可靠历史证据时保持 `[ ]`，必要时标 `UNKNOWN / NEED REBUILD`。
- 每次只推进一个 Active Module。

---

# 1. 当前正式目标

建立长期可复用的 **动画 MV 生产 Skill**。

当前简化主路线：

`参考账号 / 歌库 → 抖音参考视频 → 用户下载并提供视频 → BGM / 歌词 / 卡点核对 → 决定 5–15s 合适时长 → 动画化导演翻译 → K0 首帧 → 动态提示词 → Dola / Seedance 2.5 图生视频 → QA → 单变量迭代 → Lock`

目标：可重复、可恢复、可解释、可测试、流程简单、平台变化时只替换 Adapter，不推翻上游方法。

---

# 2. 当前已锁定生产原则

## 2.1 时长

- 歌词视觉命中 > 轻叙事连续 > 炫技镜头。
- 单段生成不固定 5s 或 15s，默认 **5–15 秒灵活决定**。
- 5–7s：单一情绪 / 动作 / 视觉事件。
- 8–10s：一个完整小段落。
- 10–15s：起势 → 发展 → 小高潮 → 收束。
- 长 MV 只拼接已 QA PASS 的 Segment。

## 2.2 动画视觉方向

当前默认不采用真人角色路线。

- 人物：One Piece 式高辨识度轮廓、姿态张力、动作表现力；不复制具体角色。
- 场景：新海诚式明亮、治愈、通透、天气 / 天空 / 光影 / 空气感；不复制具体作品场景。
- 怪物 / 物品：吉卜力式温柔奇幻、灵性、陪伴感；不复制具体角色或道具。

这些是审美方向参考，不是具体受保护表达的复刻。

## 2.3 抖音 Reference

- 抖音视频是 **选歌 + 卡点 + Director / Motion Reference 母版**。
- 继承：节奏、动作结构、镜头关系、能量曲线、Peak、Ending。
- 不继承：真人身份、脸、原服装、原场景、原视觉复制。
- Reference 源视频不要求 5s / 15s；最终生成段再按歌词和卡点确定时长。
- 用户最终选中 Reference 后下载并提供视频；Agent 负责后续 BGM / 歌词 / 片段 / 卡点与拆解。

## 2.4 当前生成入口

- 当前默认：Dola / Seedance 2.5 Image-to-Video。
- 正式输入尽量简单：**K0 首帧 + Dynamic Prompt**。
- 参考图总量默认 ≤ 3–5；能用 K0 单图时不补图。
- 当前不把复杂多模态绑定、旧 Dola Video Reference、大量参考图堆叠作为主线。

## 2.5 K0 与动作

- K0 = 可表演的 0 秒动态锚点，不是漂亮静帧。
- 禁止无足部逻辑的滑行 / 漂移。
- 位移需要：抬脚 → 落脚 → 蹬地 → 重心转移 → 加速 / 减速。
- 脚步不重要时优先稳定站位 + 转髋 / 转肩 / 躯干 / 手势 / 视线。
- Prompt 正向目标优先，不为单次失败无限追加禁令。

## 2.6 DEPTH

- DEPTH = 未来 Motion Reference Adapter，不是当前每条 MV 必经步骤。
- 已验证路线继续保留：GitHub Actions + Depth Anything V2 Small + Raw / Temporal / Compare。

---

# 3. Skill 构建方法

采用 `oil-skill-creator` 的产品化思路：

1. 先证明真实流程有效，再写 Skill。
2. Agent 负责语义、策略、审美和例外。
3. Script 负责确定、重复、可验证、失败敏感的动作。
4. `SKILL.md` 只保留主路径、关键分支、停止条件、资源导航。
5. 细节按需进 `references/`；确定性执行按需进 `scripts/`。
6. 实验 / A-B / 用户反馈留在 `evals/` 或 workspace。
7. 没有实际用途的目录不创建。
8. 最终必须用真实项目比较 `with_skill` / `without_skill` 或新旧版本。

## Promote 状态

`EXPERIMENT → VALIDATED → PROMOTED → RETIRED`

默认：`EXPERIMENT`。

---

# 4. 每个 Module 必须回答 7 个问题

1. 目标：为什么存在？
2. 输入：最低必须有什么？
3. Agent 判断：需要什么语义 / 审美 / 策略？
4. Program / Tool：什么应确定性执行？
5. 输出：下一步必须拿到什么？
6. Gate / Stop：什么时候必须停？
7. Promote：什么证据足够进入正式 Skill？

---

# 5. Master Flow v1.0

```text
M0  SONG POOL / REFERENCE ACCOUNT
↓
M1  DOUYIN REFERENCE VIDEO SELECTION
↓
G1  HUMAN REFERENCE GATE
↓
M2  USER PROVIDES DOWNLOADED REFERENCE VIDEO
↓
M3  BGM / LYRICS / SEGMENT / BEAT VERIFICATION
↓
M4  DURATION DECISION（5–15s flexible）
↓
M5  REFERENCE DECONSTRUCTION
↓
M6  ANIMATION DIRECTOR TRANSLATION
↓
M7  K0 FIRST FRAME
↓
G2  HUMAN K0 GATE
↓
M8  DYNAMIC PROMPT COMPILATION
↓
M9  GENERATION ADAPTER
    Current = Dola / Seedance 2.5 I2V
    Default = K0 + Prompt, total refs ≤ 3–5
↓
M10 5–15s SEGMENT GENERATION
↓
M11 TECHNICAL QA
↓
M12 HUMAN VIDEO QA
↓
    PASS → SEGMENT LOCK
    FAIL → FAILURE CLASSIFY → ONE-VARIABLE ITERATION
↓
M13 ASSEMBLY（multi-segment only）
↓
M14 FINAL QA / FINAL LOCK
```

Optional：`Primary Motion Reference → DEPTH → Temporal Motion → future Video/Motion Reference Adapter`

Learning：`Production Evidence → EXPERIMENT → VALIDATED → Cross-project → PROMOTED`

---

# 6. Human Gate 最小集合

1. Reference Gate：强制，选择 Primary Reference。
2. Audio / Segment Gate：条件触发，只有版本 / 剪辑段有真实歧义才停。
3. K0 Gate：强制，确认视觉、角色、场景、动作入口。
4. Video QA Gate：强制，确认最终质量。

Human Video QA 固定四问：

1. 画面明显好看吗？
2. 歌词 / 情绪明显命中吗？
3. 动作与镜头稳定自然吗？
4. 值得重复生产吗？

技术项优先交给程序检查。

---

# 7. 失败恢复

失败分类：

- `S` Semantic
- `R` Reference
- `D` Director
- `K` K0
- `P` Prompt
- `G` Generation

一次只改一个主要变量；回退到最近责任层；已 LOCKED 上游默认不因下游小问题重做。

---

# 8. 项目恢复协议

真实项目后续建立 `PROJECT_STATE`，最低记录：

Project / Song / Reference Account / Primary Reference / Reference File / BGM Segment / Target Duration / Current Stage / K0 / Prompt Version / Generation Version / QA / Next Action。

状态：`PENDING / ACTIVE / GATED / LOCKED / REWORK`

恢复：`Read Skill or Build Guide → Read PROJECT_STATE → Find ACTIVE/GATED → Continue`

---

# 9. Master Flow 构建清单

## Phase A｜产品与流程定义

- [x] A00｜逐段构建 Skill，不一次性写完整 Skill。
- [x] A01｜Reference-First 总体方向。
- [x] A02｜Douyin Reference / DEPTH / Visual 分层。
- [x] A03｜采用 oil-skill-creator 产品化方法。
- [x] A04｜建立总控工作区。
- [x] A05｜完成 Master Flow 阶段边界确认。
- [ ] A06｜最终 Skill 名称、触发范围、反向边界。

---

## Phase B｜M0 Song Pool / Reference Account

- [x] B00｜恢复历史参考账号 / 选歌数据库。
- [x] B01｜区分可靠历史身份与需要刷新的趋势数据。
- [x] B02｜定义数据库最小字段与可靠性状态。
- [x] B03｜定义选歌原则：治愈动画适配、卡点可读、5–15s 可切、动画化潜力。
- [x] B04｜建立第一批恢复 + 当前 Watch 候选数据库。
- [ ] B05｜用户确认数据库展示 / 选歌方式足够简单好用。
- [ ] B06｜用核心账号最新直接作品完成首轮 Fresh Refresh。
- [ ] B07｜Promote 稳定选歌规则。

**Evidence**：
- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`

**Module 状态**：`EXPERIMENT`

---

## Phase C｜M1–M2 Douyin Reference Selection / Handoff

- [ ] C00｜定义候选筛选输入。
- [ ] C01｜默认最多展示 3 个候选。
- [ ] C02｜每候选：链接 / 时长 / Action Arc / Camera / Lyric Fit / Risk。
- [ ] C03｜Human Reference Gate。
- [ ] C04｜定义用户下载视频后的标准交接。
- [ ] C05｜真实试跑。
- [ ] C06｜Promote。

---

## Phase D｜M3 BGM / Lyrics / Segment / Beat

- [ ] D00｜定义音频核对目标。
- [ ] D01｜自动探测时长 / 格式 / BGM / 歌词位置 / Beat。
- [ ] D02｜定义 Audio / Segment Gate。
- [ ] D03｜标准输出。
- [ ] D04｜真实试跑。
- [ ] D05｜判断音频探测 / 切段脚本化。
- [ ] D06｜Promote。

---

## Phase E｜M4 Duration Decision

- [ ] E00｜定义 5–15s 判断规则。
- [ ] E01｜验证 5–7 / 8–10 / 10–15s 三档价值。
- [ ] E02｜时长服从歌词 / 卡点 / 动作任务。
- [ ] E03｜真实案例。
- [ ] E04｜Promote。

---

## Phase F｜M5 Reference Deconstruction

- [ ] F00｜Motion / Director Map 最小字段。
- [ ] F01｜动作 / 重心 / 手势 / Camera / Energy / Ending。
- [ ] F02｜Structure Transfer / Copy Boundary。
- [ ] F03｜真实拆解。
- [ ] F04｜删除装饰字段。
- [ ] F05｜用户确认可指导动画导演。
- [ ] F06｜Promote。

---

## Phase G｜M6 Animation Director Translation

- [ ] G00｜歌词 + Reference Motion → Animation Director。
- [ ] G01｜锁定人物 / 场景 / 怪物或物品三类审美职责。
- [ ] G02｜避免复制具体受保护表达。
- [ ] G03｜最小导演输出。
- [ ] G04｜真实试跑。
- [ ] G05｜用户确认。
- [ ] G06｜Promote。

---

## Phase H｜M7 K0 First Frame

- [ ] H00｜K0 = 可表演 0 秒动态锚点。
- [ ] H01｜Current State / Motion Entry / Weight / Camera / Secondary Motion。
- [ ] H02｜默认动画角色 / 场景。
- [ ] H03｜生成真实 K0。
- [ ] H04｜Human K0 Gate。
- [ ] H05｜验证 K0 对视频改善。
- [ ] H06｜Promote。

---

## Phase I｜M8 Dynamic Prompt

- [ ] I00｜从 Reference + Director + K0 编译。
- [ ] I01｜最小结构。
- [ ] I02｜卡点 / 动作链 / Camera / Physics / Ending。
- [ ] I03｜正向目标优先。
- [ ] I04｜无滑行 / 重心链。
- [ ] I05｜真实验证。
- [ ] I06｜Promote。

---

## Phase J｜M9–M10 Generation

- [ ] J00｜Dola / Seedance 2.5 I2V 默认 Adapter。
- [ ] J01｜最简输入 = K0 + Prompt。
- [ ] J02｜参考图默认 ≤ 3–5。
- [ ] J03｜真实 5–15s 生成。
- [ ] J04｜记录必要参数 / Evidence。
- [ ] J05｜验证 Adapter 可替换性。
- [ ] J06｜Promote。

---

## Phase K｜QA / One-variable

- [ ] K00｜Human QA 四问。
- [ ] K01｜Technical QA。
- [ ] K02｜S/R/D/K/P/G 归因。
- [ ] K03｜最近责任层回退。
- [ ] K04｜单变量迭代。
- [ ] K05｜真实 QA → Iteration → QA。
- [ ] K06｜Promote。

---

## Phase L｜Assembly / Final Lock

- [ ] L00｜只拼 PASS / LOCKED Segment。
- [ ] L01｜音频 / 人物 / 场景 / 色调 / 情绪 / 接缝 / Ending QA。
- [ ] L02｜验证 Locked Segment 不被无关修改牵连。
- [ ] L03｜多段实测后 Promote。

---

## Phase M｜DEPTH Adapter

- [ ] M00｜DEPTH 可选，不是必经。
- [ ] M01｜迁移 DAV2 Small 路线。
- [ ] M02｜Raw / Temporal / Compare。
- [ ] M03｜定义 Video/Motion Reference 接入条件。
- [ ] M04｜不支持时自动跳过。
- [ ] M05｜验证不污染 I2V 主线。
- [ ] M06｜Promote。

**状态**：`VALIDATED`（转换链已实测；Skill 集成未完成）

---

## Phase N｜Skill Information Architecture

- [ ] N00｜Skill 名称 / 触发范围。
- [ ] N01｜最小 `SKILL.md`。
- [ ] N02｜只创建稳定 references。
- [ ] N03｜只创建必要 scripts。
- [ ] N04｜唯一事实源检查。
- [ ] N05｜弱模型可读性。

---

## Phase O｜Full Real Project

- [ ] O00｜从更新歌库选全新歌曲。
- [ ] O01｜完整执行 Reference Gate。
- [ ] O02｜完成 BGM / Segment Lock。
- [ ] O03｜完成 K0 Gate。
- [ ] O04｜真实 5–15s 生成。
- [ ] O05｜QA + 单变量迭代。
- [ ] O06｜最终 PASS 或明确失败。

---

## Phase P｜oil-skill-creator Evaluation

- [ ] P00｜P0 / P1 / P2 Review。
- [ ] P01｜结构 / 重复 / 弱模型 / 宿主检查。
- [ ] P02｜`evals/evals.json`。
- [ ] P03｜with_skill vs without_skill / old_skill。
- [ ] P04｜客观 / 主观分离。
- [ ] P05｜用户 Human Review。
- [ ] P06｜整改与回归。

---

## Phase Q｜Open Source

- [ ] Q00｜排除单次项目 / 失败实验 / 个人路径。
- [ ] Q01｜只保留 Skill 必需内容。
- [ ] Q02｜README / 安装 / 兼容 / 数据边界。
- [ ] Q03｜严格校验。
- [ ] Q04｜发布。
- [ ] Q05｜干净环境复跑。

---

# 10. Current Active Module

**ACTIVE MODULE：Phase B / B05｜用户确认数据库展示 / 选歌方式是否足够简单好用**

当前文件：

- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`

B05 通过后：进入 B06，用核心参考账号的最新直接抖音作品做 Fresh Refresh；不直接跳 K0。

---

# 11. 实验与正式规则隔离

默认不得直接进入正式 Skill：具体歌曲、具体抖音链接、某次 K0 Prompt、具体人物、单次失败补丁、甲乙丙丁单次结果、未验证平台猜测、历史 Review。

只有跨任务仍成立的规则才能 Promote。

---

# 12. 最终成功标准

- [ ] 新对话能靠 Skill + PROJECT_STATE 恢复。
- [ ] 选歌优先利用参考账号 / 歌库。
- [ ] Douyin Reference / DEPTH / K0 / Prompt 职责不混。
- [ ] 生成时长按内容在 5–15s 灵活选择。
- [ ] 默认动画路线稳定，不依赖真人还原。
- [ ] Dola / Seedance 2.5 保持 K0 + Prompt 简单路径。
- [ ] 不一次加载全部历史文档。
- [ ] 同一规则唯一维护。
- [ ] 至少一个全新真实 MV 完整 PASS。
- [ ] Skill 相对普通 Agent / 旧方案有可见改善。
- [ ] 主观质量由用户确认。
- [ ] oil-skill-creator 关键问题解决或明确接受。
- [ ] 开源版本能在干净环境复跑。
