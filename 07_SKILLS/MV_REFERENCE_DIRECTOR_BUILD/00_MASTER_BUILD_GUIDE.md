# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Role: 本文件是构建阶段唯一总控事实源（Single Source of Truth）。

---

# 0. 使用规则

新对话 / 换模型 / 上下文过长时：

1. 先读本文件；
2. 找 `Current Active Module`；
3. 只读该模块明确指向的 Evidence；
4. `[x]` 只代表已有真实证据 / 用户确认；
5. 完成当前项后先更新本文件，再进入下一项；
6. 每次只推进一个 Active Module；
7. 单次成功不能直接 Promote 为 Skill 规则。

状态：`EXPERIMENT → VALIDATED → PROMOTED → RETIRED`。

---

# 1. 当前生产目标

建立一套稳定、简单、可恢复的**动画 MV Reference-First Skill**。

当前简化路线：

`参考账号/歌库 → 抖音参考视频 → 用户下载提供 → BGM/歌词/卡点核对 → 决定 5–15s 合适时长 → Reference 拆解 → 动画化导演翻译 → K0 首帧 → 动态提示词 → Dola/Seedance 2.5 I2V → QA → 单变量迭代 → Lock`

---

# 2. 已锁定长期原则

## 2.1 内容与时长

- 歌词视觉命中 > 轻叙事连续 > 炫技镜头。
- 单段生成按内容在 **5–15s** 灵活决定，不固定 5s 或 15s。
- 5–7s：单一情绪/动作/视觉事件。
- 8–10s：一个完整小段。
- 10–15s：起势→发展→小高潮→收束。
- 长 MV 只拼已 QA PASS 的 Segment。

## 2.2 动画视觉

默认不走真人角色路线。

- 人物：One Piece 式高辨识度轮廓、姿态张力、动作表现力；不复制具体角色。
- 场景：新海诚式明亮、治愈、通透、天空/天气/光影/空气感；不复制具体场景。
- 怪物/物品：吉卜力式温柔奇幻、灵性、陪伴感；不复制具体角色/道具。

## 2.3 Douyin Reference

- 抖音视频负责：选歌、卡点、动作、镜头、能量曲线、Peak、Ending。
- 迁移 Structure，不迁移真人身份、脸、原服装、原场景和具体视觉表达。
- Reference 源视频不限制 5/15s。
- 用户选中后下载并提供视频；Agent 再负责 BGM/歌词/片段/卡点和拆解。

## 2.4 当前生成入口

- 默认：Dola / Seedance 2.5 Image-to-Video。
- 最简正式输入：**K0 + Dynamic Prompt**。
- 参考图默认 ≤3–5；K0 单图够用就不补图。
- 不恢复复杂多模态绑定、大量参考图堆叠、旧 Dola Video Reference 主线。

## 2.5 K0 / Motion

- K0 = 可表演的 0 秒动态锚点，不是漂亮静帧。
- 位移必须有抬脚→落脚→蹬地→重心转移→加减速；禁止无足部逻辑滑行/漂移。
- 脚步不重要时优先稳定站位 + 转髋/转肩/躯干/手势/视线。
- Prompt 正向目标优先，不因单次失败无限加禁止项。

## 2.6 DEPTH

- DEPTH 是未来 Motion Reference Adapter，不是当前必经步骤。
- 已验证：GitHub Actions + Depth Anything V2 Small + Raw / Temporal / Compare。

---

# 3. Master Flow v1.0

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
    Default = K0 + Prompt, refs ≤3–5
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

# 4. Human Gate 最小集合

1. **Reference Gate**：强制，用户选 Primary Reference。
2. **Audio/Segment Gate**：条件触发，只有版本/剪辑段有真实歧义时停。
3. **K0 Gate**：强制，确认视觉/角色/场景/动作入口。
4. **Video QA Gate**：强制，只问：
   - 画面明显好看吗？
   - 歌词/情绪明显命中吗？
   - 动作与镜头稳定自然吗？
   - 值得重复生产吗？

技术项优先交程序。

---

# 5. 失败恢复

分类：

- `S` Semantic
- `R` Reference
- `D` Director
- `K` K0
- `P` Prompt
- `G` Generation

规则：一次只改一个主要变量；回退到最近责任层；已 LOCKED 上游不因下游小问题重做。

---

# 6. Skill 构建清单

## Phase A｜产品与流程

- [x] A00｜逐段构建 Skill。
- [x] A01｜Reference-First。
- [x] A02｜Douyin Reference / DEPTH / Visual 分层。
- [x] A03｜采用 oil-skill-creator 产品化方法。
- [x] A04｜建立总控工作区。
- [x] A05｜Master Flow 边界确认。
- [ ] A06｜最终 Skill 名称 / 触发范围 / 反向边界。

## Phase B｜M0 Song Pool / Reference Account

- [x] B00｜恢复历史参考账号 / 选歌数据库。
- [x] B01｜区分可靠历史身份与需刷新趋势。
- [x] B02｜定义数据库最小字段与可靠性状态。
- [x] B03｜定义选歌原则：动画治愈适配、卡点可读、5–15s 可切、动画化潜力。
- [x] B04｜建立恢复 + Current Watch Pool。
- [x] B05｜用户确认：每轮最多 3 个候选，展示歌曲/来源/直链/动画适配/建议时长/一句话理由。
- [ ] B06｜核心账号最新直接作品 Fresh Refresh。
  - 当前：`PARTIAL / CORE INDEX PENDING`
  - 已完成公开平台/补充信号刷新；不能冒充核心账号证据。
- [ ] B07｜Promote 稳定选歌规则。

Evidence：
- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`
- `03_FRESH_REFRESH_2026-09-09.md`

## Phase C｜M1–M2 Reference Selection / Handoff

- [ ] C00｜候选筛选输入。
- [ ] C01｜最多 3 个候选。
- [ ] C02｜链接/时长/Action Arc/Camera/Lyric Fit/Risk。
- [ ] C03｜Human Reference Gate。
- [ ] C04｜用户下载后的标准交接。
- [ ] C05｜真实试跑。
- [ ] C06｜Promote。

## Phase D｜M3 Audio / Lyrics / Beat

- [ ] D00｜核对目标。
- [ ] D01｜时长/格式/BGM/歌词位置/Beat。
- [ ] D02｜Audio/Segment Gate。
- [ ] D03｜标准输出。
- [ ] D04｜真实试跑。
- [ ] D05｜判断脚本化。
- [ ] D06｜Promote。

## Phase E｜M4 Duration

- [ ] E00｜5–15s 判断规则。
- [ ] E01｜5–7 / 8–10 / 10–15 三档验证。
- [ ] E02｜时长服从歌词/卡点/动作任务。
- [ ] E03｜真实案例。
- [ ] E04｜Promote。

## Phase F｜M5 Reference Deconstruction

- [ ] F00｜Motion/Director Map 最小字段。
- [ ] F01｜动作/重心/手势/Camera/Energy/Ending。
- [ ] F02｜Structure Transfer / Copy Boundary。
- [ ] F03｜真实拆解。
- [ ] F04｜删除装饰字段。
- [ ] F05｜用户确认可指导动画导演。
- [ ] F06｜Promote。

## Phase G｜M6 Animation Director

- [ ] G00｜Lyrics + Motion → Animation Director。
- [ ] G01｜人物/场景/怪物物品三类审美职责。
- [ ] G02｜避免复制具体受保护表达。
- [ ] G03｜最小导演输出。
- [ ] G04｜真实试跑。
- [ ] G05｜用户确认。
- [ ] G06｜Promote。

## Phase H｜M7 K0

- [ ] H00｜K0 定义。
- [ ] H01｜Current State / Motion Entry / Weight / Camera / Secondary Motion。
- [ ] H02｜动画角色/场景默认。
- [ ] H03｜真实 K0。
- [ ] H04｜Human K0 Gate。
- [ ] H05｜验证对视频改善。
- [ ] H06｜Promote。

## Phase I｜M8 Dynamic Prompt

- [ ] I00｜从 Reference + Director + K0 编译。
- [ ] I01｜最小结构。
- [ ] I02｜卡点/动作链/Camera/Physics/Ending。
- [ ] I03｜正向目标优先。
- [ ] I04｜无滑行/重心链。
- [ ] I05｜真实验证。
- [ ] I06｜Promote。

## Phase J｜M9–M10 Generation

- [ ] J00｜Dola/Seedance 2.5 I2V Adapter。
- [ ] J01｜最简输入 K0 + Prompt。
- [ ] J02｜refs ≤3–5。
- [ ] J03｜真实 5–15s 生成。
- [ ] J04｜记录参数/Evidence。
- [ ] J05｜Adapter 可替换性。
- [ ] J06｜Promote。

## Phase K｜QA / Iteration

- [ ] K00｜Human QA 四问。
- [ ] K01｜Technical QA。
- [ ] K02｜S/R/D/K/P/G 归因。
- [ ] K03｜最近责任层回退。
- [ ] K04｜单变量迭代。
- [ ] K05｜真实 QA→Iteration→QA。
- [ ] K06｜Promote。

## Phase L｜Assembly

- [ ] L00｜只拼 PASS/LOCKED Segment。
- [ ] L01｜音频/人物/场景/色调/情绪/接缝/Ending QA。
- [ ] L02｜Locked Segment 不被无关修改牵连。
- [ ] L03｜多段实测后 Promote。

## Phase M｜DEPTH Adapter

- [ ] M00｜DEPTH 可选。
- [ ] M01｜DAV2 Small 路线迁移。
- [ ] M02｜Raw/Temporal/Compare。
- [ ] M03｜Video/Motion Reference 接入条件。
- [ ] M04｜不支持时自动跳过。
- [ ] M05｜不污染 I2V 主线。
- [ ] M06｜Promote。

状态：`VALIDATED`（转换链已实测；Skill 集成未完成）。

## Phase N｜Skill IA

- [ ] N00｜名称/触发范围。
- [ ] N01｜最小 SKILL.md。
- [ ] N02｜只创建稳定 references。
- [ ] N03｜只创建必要 scripts。
- [ ] N04｜唯一事实源。
- [ ] N05｜弱模型可读性。

## Phase O｜Full Real Project

- [ ] O00｜从更新歌库选全新歌曲。
- [ ] O01｜Reference Gate。
- [ ] O02｜BGM/Segment Lock。
- [ ] O03｜K0 Gate。
- [ ] O04｜真实 5–15s 生成。
- [ ] O05｜QA + 单变量迭代。
- [ ] O06｜PASS 或明确失败。

## Phase P｜oil-skill-creator Evaluation

- [ ] P00｜P0/P1/P2 Review。
- [ ] P01｜结构/重复/弱模型/宿主检查。
- [ ] P02｜evals/evals.json。
- [ ] P03｜with_skill vs without_skill/old_skill。
- [ ] P04｜客观/主观分离。
- [ ] P05｜用户 Human Review。
- [ ] P06｜整改与回归。

## Phase Q｜Open Source

- [ ] Q00｜排除单次项目/失败实验/个人路径。
- [ ] Q01｜只保留 Skill 必需内容。
- [ ] Q02｜README/安装/兼容/数据边界。
- [ ] Q03｜严格校验。
- [ ] Q04｜发布。
- [ ] Q05｜干净环境复跑。

---

# 7. Current Active Module

**ACTIVE MODULE：Phase B / B06｜核心参考账号 Fresh Refresh**

当前真实状态：

- 核心账号身份/角色：已恢复。
- 2026-09-09 平台/补充公开信号：已刷新。
- 核心账号 9 月新作品：公开索引不足，标 `INDEX_PENDING`，不能冒充已验证。
- 当前优先 Recheck：
  1. 《茶花开了，该回家了》
  2. 《雀跃》
  3. 《小半》

下一步：继续获得核心账号直接 Reference；一旦有足够直接证据，完成 B06 → B07，再进入 Phase C Human Reference Gate。

---

# 8. 恢复协议

真实项目后续建立 `PROJECT_STATE`，最低记录：Project / Song / Reference Account / Primary Reference / Reference File / BGM Segment / Target Duration / Current Stage / K0 / Prompt Version / Generation Version / QA / Next Action。

状态：`PENDING / ACTIVE / GATED / LOCKED / REWORK`。

实验不会自动修改 Skill；只有跨任务成立的规则才 Promote。
