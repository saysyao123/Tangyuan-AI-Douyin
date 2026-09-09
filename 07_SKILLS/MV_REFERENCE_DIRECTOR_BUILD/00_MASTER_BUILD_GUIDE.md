# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Purpose: 逐段梳理、验证并固化一套稳定、简单、可恢复的动画 MV Reference-First 生产 Skill。

---

# 0. 本文件的地位

本文件是 **MV Reference Director Skill 构建阶段的唯一总控事实源（Single Source of Truth）**。

以后新开对话、换模型、换执行环境时：

1. 先读取本文件；
2. 找到 `Current Active Module`；
3. 再读取当前模块明确指向的文件；
4. 不依赖聊天记忆猜进度；
5. 完成一项后先更新本文件，再进入下一项。

## 勾选规则

- `[ ]` = 尚未完成，或没有足够证据证明完成。
- `[x]` = 已完成，并且有真实产物 / 测试 / 用户确认作为证据。
- 只有满足该项 **Done Definition** 才能勾选。
- 单次偶然成功不能直接 Promote 为 Skill 规则。
- 找不到可靠历史证据时保持 `[ ]`，必要时标记 `UNKNOWN / NEED REBUILD`。
- 每次只允许一个 **Active Module** 处于推进状态。

---

# 1. 原始目标

建立一套长期复用的 **动画 MV 生产 Skill**。

当前锁定的简化主路线：

`参考账号 / 歌库 → 抖音参考视频 → 用户下载并提供视频 → BGM / 歌词 / 卡点核对 → 决定最适合的 5–15s 生成时长 → 动画化导演翻译 → K0 首帧 → 动态提示词 → Dola / Seedance 2.5 图生视频 → QA → 单变量迭代 → Lock`

目标不是“偶尔生成一条好看的 AI MV”，而是建立：

1. 可重复；
2. 可恢复；
3. 可解释；
4. 可测试；
5. 不依赖长聊天上下文；
6. 不因平台能力变化就推翻整个方法；
7. 生成流程足够简单；
8. 能通过真实项目和 A/B 对照证明有效。

---

# 2. 当前已锁定的生产原则

## 2.1 内容与时长

- 歌词视觉命中 > 轻叙事连续 > 炫技镜头。
- **生成时长不固定为 5s 或 15s。**
- 单个生成段默认在 **5–15 秒**内按歌词、卡点、动作复杂度和画面任务决定。
- 5–7s：单一情绪 / 单一动作 / 单一视觉事件。
- 8–10s：一个完整小段落。
- 10–15s：起势 → 发展 → 小高潮 → 收束。
- 长 MV 由多个已经 QA PASS 的 5–15s Segment 组成。

## 2.2 视觉方向

当前正式主线为 **动画 MV**，不采用真人作为默认生产角色。

视觉参考分层：

- **人物**：One Piece 式高辨识度角色轮廓、姿态张力、动作表现力；不复制具体角色。
- **场景**：新海诚式明亮、治愈、通透、强天气 / 天空 / 光影 / 空气感；不复制具体作品场景。
- **怪物 / 物品**：吉卜力式温柔奇幻、灵性、陪伴感和可爱但不低幼的设计；不复制具体角色或道具。

以上均为审美方向参考，不代表照搬受保护角色、场景或具体画面。

## 2.3 抖音 Reference

- 抖音参考视频首先是 **选歌 / 卡点 / Director / Motion Reference 母版**。
- 它负责：节奏、动作结构、镜头关系、能量曲线、Peak、Ending。
- 它不负责：真人身份、原服装、原场景、原人物外貌复制。
- Reference 不要求恰好 5s / 15s；源视频可以更长，再按目标段落截取或抽取结构。
- 用户负责把最终选定的公开参考视频下载后提供给项目；Agent 负责后续 BGM、歌词、片段、卡点与导演拆解。

## 2.4 当前生成入口

- 当前 Dola / Seedance 2.5 默认走 **Image-to-Video**。
- 正式生产尽量简单：**K0 首帧 + 动态提示词**。
- 参考图默认做减法，整体控制在 **3–5 张以内**；能用 1 张 K0 完成时不为了数量补图。
- 需要补充时，参考资产按角色分工：角色 / 场景 / 怪物或物品 / 动作辅助。
- 当前不把复杂多模态绑定、旧 Dola Video Reference、大量参考图堆叠作为默认路线。

## 2.5 动作与 K0

- K0 必须是“**可表演的 0 秒动态锚点**”，不是单纯漂亮静帧。
- 人物位移不得无足部逻辑地滑行 / 漂移。
- 位移需要可读的：抬脚 → 落脚 → 蹬地 → 重心转移 → 加速 / 减速。
- 当脚步不是重点时，宁可采用稳定站位 + 转髋 / 转肩 / 躯干 / 手势 / 视线变化，也不要制造虚假滑行。
- 动态 Prompt 优先正向描述动作链、镜头关系、卡点与物理余韵，不为单次失败无限增加禁止项。

## 2.6 DEPTH

- DEPTH 保留为未来 **Motion Reference Adapter**。
- 它不是当前每条 MV 的必经步骤。
- 当前主线不因 Video Reference 暂停而删除抖音 Reference-First 方法。
- 已验证 DEPTH 路线继续保留：GitHub Actions + Depth Anything V2 Small + Raw / Temporal / Compare。

---

# 3. Skill 构建方法

采用 `oil-skill-creator` 的产品化思路：

1. 先确认真实流程有效；
2. 再抽象成 Skill；
3. Agent 负责语义、策略、审美和例外；
4. Script 负责确定、重复、可验证、失败敏感的动作；
5. `SKILL.md` 只保留主流程、关键分支、停止条件和资源导航；
6. 细节按需放 `references/`；
7. 确定性操作按需放 `scripts/`；
8. 实验和对照放 `evals/` / 外部 workspace；
9. 没有真实用途的目录不创建；
10. 最终使用真实项目比较 `with_skill` / `without_skill` 或新旧版本。

## Promote 状态

- `EXPERIMENT`：正在试验，不能当正式规则。
- `VALIDATED`：至少一次真实任务证明可用，但仍需观察跨任务稳定性。
- `PROMOTED`：跨任务仍成立，允许进入正式 Skill。
- `RETIRED`：曾经有效，但已被更好的规则或平台能力替代。

默认状态：`EXPERIMENT`。

---

# 4. 每个 Module 必须回答的 7 个问题

1. **目标**：为什么这一步存在？
2. **输入**：进入这一步必须有什么？
3. **Agent 判断**：哪些需要语义 / 审美 / 策略判断？
4. **Program / Tool**：哪些应当确定性执行？
5. **输出**：下一阶段必须拿到什么？
6. **Gate / Stop**：什么时候必须停下来让用户确认？
7. **Promote 条件**：什么证据足以进入正式 Skill？

任何模块没有回答清楚以上 7 点，不允许标记完成。

---

# 5. 已确认 Master Flow v1.0

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
    Character: One Piece-inspired direction
    Scene: Shinkai-inspired direction
    Creature/Object: Ghibli-inspired direction
↓
M7  K0 FIRST FRAME
↓
G2  HUMAN K0 GATE
↓
M8  DYNAMIC PROMPT COMPILATION
↓
M9  GENERATION ADAPTER
    Current: Dola / Seedance 2.5 I2V
    Default: K0 + Prompt, total refs ≤ 3–5
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
M13 ASSEMBLY（only when multi-segment）
↓
M14 FINAL QA / FINAL LOCK
```

## 可选旁路

```text
Primary Motion Reference
↓
DEPTH Adapter
↓
Raw / Temporal / Compare
↓
Future Video / Motion Reference Platform
```

## 学习旁路

```text
Production Evidence
↓
EXPERIMENT
↓
VALIDATED
↓
Cross-project Test
↓
PROMOTED TO SKILL
```

---

# 6. 人工 Gate 最小集合

1. **Reference Gate**：默认强制；用户从候选参考中选择 Primary Reference。
2. **Audio / Segment Gate**：条件触发；只有歌曲版本 / 剪辑段存在真实歧义时才停。
3. **K0 Gate**：默认强制；确认画面、角色、场景、动作入口。
4. **Video QA Gate**：默认强制；确认最终段落质量。

没有实际决策价值的 Gate 删除。

---

# 7. 最终 Human Video QA 四问

1. 画面是否明显好看？
2. 歌词 / 情绪是否明显命中？
3. 动作与镜头是否稳定、自然、无明显滑行 / 漂移？
4. 是否值得把这套方法重复用于后续生产？

技术项如时长、分辨率、FPS、文件存在、编码等优先交给程序 / 工具检查。

---

# 8. 失败恢复机制

当结果不好时，先分类，不立刻推倒重来：

- `S` Semantic：歌词 / 情绪理解错误。
- `R` Reference：参考视频选错或拆解错误。
- `D` Director：动画导演翻译失真。
- `K` K0：首帧不适合表演或审美不对。
- `P` Prompt：动态 Prompt 没有正确编译上游信息。
- `G` Generation：平台 / 模型执行能力或随机性问题。

一次只修改一个主要变量，并回退到最近责任层。

已 `LOCKED` 的上游资产默认不因下游小问题重做。

---

# 9. 项目状态恢复协议

每个真实 MV 项目后续都应有独立 `PROJECT_STATE`，最低记录：

- Project
- Song / Reference Account
- Primary Douyin Reference
- Reference Video File
- BGM / Segment Lock
- Target Duration
- Current Stage
- K0
- Prompt Version
- Generation Version
- QA Status
- Next Action

建议状态：

`PENDING / ACTIVE / GATED / LOCKED / REWORK`

新对话恢复：

`Read Skill / Build Guide → Read PROJECT_STATE → Find ACTIVE or GATED → Continue`

不要依赖“昨天好像做到哪里”的聊天记忆。

---

# 10. Master Flow 构建清单

## Phase A｜产品与流程定义

- [x] A00｜确认目标是“逐段构建 Skill”，不是一次性写完整 Skill。
- [x] A01｜确认采用 Reference-First MV 总体方向。
- [x] A02｜确认抖音 Reference 与 DEPTH / Character / Scene 分层。
- [x] A03｜确认 `oil-skill-creator` 作为 Skill 产品化方法参考。
- [x] A04｜建立本总控工作区与唯一总控文件。
- [x] A05｜完成完整 Master Flow 的阶段边界确认。
- [ ] A06｜确认最终 Skill 名称、触发范围和反向边界。

**Phase A Done Definition**：Master Flow 每一阶段职责明确，用户确认整体方向无明显缺口。

---

## Phase B｜M0 Song Pool / Reference Account

- [ ] B00｜恢复历史参考账号 / 选歌小数据库。
- [ ] B01｜核对哪些记录仍可靠、哪些需要更新。
- [ ] B02｜定义最小字段：歌名 / 作者或歌手 / 来源账号 / 参考视频 / 情绪 / 推荐片段 / 状态。
- [ ] B03｜定义选歌标准：治愈动态适配、卡点可读、5–15s 可切分、动画化潜力。
- [ ] B04｜更新第一批候选数据库。
- [ ] B05｜用户确认数据库展示方式是否足够用于选歌。
- [ ] B06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase C｜M1–M2 Douyin Reference Selection / Handoff

- [ ] C00｜定义候选搜索 / 筛选输入。
- [ ] C01｜默认最多展示 3 个候选。
- [ ] C02｜每个候选至少说明：链接 / 时长 / Action Arc / Camera / Lyric Fit / Risk。
- [ ] C03｜Human Reference Gate 选定 Primary Reference。
- [ ] C04｜定义用户下载并提供参考视频后的标准交接。
- [ ] C05｜真实试跑一次。
- [ ] C06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase D｜M3 BGM / Lyrics / Segment / Beat Verification

- [ ] D00｜定义音频核对目标。
- [ ] D01｜定义自动探测项：实际时长、格式、BGM、歌词位置、节拍 / 卡点。
- [ ] D02｜定义什么时候需要 Audio / Segment Gate。
- [ ] D03｜定义标准输出。
- [ ] D04｜用真实参考视频试跑。
- [ ] D05｜判断是否需要脚本化音频探测 / 切段。
- [ ] D06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase E｜M4 Duration Decision

- [ ] E00｜定义 5–15s 灵活时长的判断规则。
- [ ] E01｜验证 5–7 / 8–10 / 10–15s 三档是否有实际帮助。
- [ ] E02｜时长必须服从歌词 / 卡点 / 动作任务，而不是反过来凑时长。
- [ ] E03｜真实案例试跑。
- [ ] E04｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase F｜M5 Reference Deconstruction

- [ ] F00｜定义 Motion / Director Map 最小字段。
- [ ] F01｜至少覆盖动作 / 重心 / 手势 / Camera / Energy / Ending。
- [ ] F02｜明确 Structure Transfer / Copy Boundary。
- [ ] F03｜用真实 Reference 完成一次拆解。
- [ ] F04｜删除装饰性字段。
- [ ] F05｜用户确认能指导后续动画化导演。
- [ ] F06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase G｜M6 Animation Director Translation

- [ ] G00｜定义“歌词 + Reference Motion → 动画 Director Concept”。
- [ ] G01｜锁定人物 / 场景 / 怪物或物品三类审美参考职责。
- [ ] G02｜避免复制具体受保护角色 / 场景 / 物件。
- [ ] G03｜定义最小导演输出。
- [ ] G04｜真实试跑。
- [ ] G05｜用户确认动画化结果优于真人路线 / 纯自由导演。
- [ ] G06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase H｜M7 K0 First Frame

- [ ] H00｜锁定 K0 = 可表演的 0 秒动态锚点。
- [ ] H01｜定义 Current State / Motion Entry / Weight State / Camera / Secondary Motion。
- [ ] H02｜明确默认以动画角色与动画场景生成。
- [ ] H03｜生成真实 K0。
- [ ] H04｜Human K0 Gate：好看 / 歌词命中 / 动作入口 / 可表演性。
- [ ] H05｜验证 K0 对后续动态生成有实际帮助。
- [ ] H06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase I｜M8 Dynamic Prompt

- [ ] I00｜Prompt 必须从 Reference + Director + K0 编译，而非从零自由写。
- [ ] I01｜定义最小 Prompt 结构。
- [ ] I02｜加入卡点、动作链、Camera、Secondary Physics、Ending。
- [ ] I03｜正向目标优先，禁止项最小化。
- [ ] I04｜加入无滑行 / 重心链规则。
- [ ] I05｜真实生成 Prompt 并验证。
- [ ] I06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase J｜M9–M10 Generation Adapter / 5–15s Generation

- [ ] J00｜锁定当前默认：Dola / Seedance 2.5 Image-to-Video。
- [ ] J01｜锁定最简正式输入：K0 + Dynamic Prompt。
- [ ] J02｜参考图总量默认 ≤ 3–5，按需才增加。
- [ ] J03｜完成一条真实 5–15s 生成。
- [ ] J04｜记录生成参数和必要证据。
- [ ] J05｜验证平台变化只改变 Adapter，不推翻上游流程。
- [ ] J06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase K｜M11–M12 QA + One-variable Iteration

- [ ] K00｜锁定 Human QA 四问。
- [ ] K01｜定义 Technical QA。
- [ ] K02｜定义 S/R/D/K/P/G 失败归因。
- [ ] K03｜定义最近责任层回退。
- [ ] K04｜定义单变量迭代规则。
- [ ] K05｜完成真实 QA → Iteration → QA。
- [ ] K06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase L｜M13–M14 Assembly / Final Lock

- [ ] L00｜多 Segment 时只拼接已 PASS / LOCKED 的段。
- [ ] L01｜定义音频、人物、场景、色调、情绪、接缝和 Ending QA。
- [ ] L02｜验证一个 Locked Segment 不因其他 Segment 小修改被牵连重做。
- [ ] L03｜完成真实多段 Assembly 时再 Promote。

**Module 状态**：`EXPERIMENT`

---

## Phase M｜DEPTH Motion Adapter

- [ ] M00｜明确 DEPTH 为可选 Adapter，而非主流程必经步骤。
- [ ] M01｜迁移已验证 GitHub Actions + Depth Anything V2 Small 路线。
- [ ] M02｜保留 Raw / Temporal / Compare 职责。
- [ ] M03｜定义平台支持 Video / Motion Reference 时的接入条件。
- [ ] M04｜平台不支持时自动跳过。
- [ ] M05｜验证不会污染当前 Image-first 主流程。
- [ ] M06｜Promote 稳定规则。

**Module 状态**：`VALIDATED`（DEPTH 转换链已实测；作为 MV Skill Adapter 的集成尚未完成）

---

## Phase N｜Skill Information Architecture

- [ ] N00｜确定正式 Skill 名称与触发范围。
- [ ] N01｜生成最小 `SKILL.md`。
- [ ] N02｜只创建已有稳定内容的 `references/`。
- [ ] N03｜只创建确有必要的 `scripts/`。
- [ ] N04｜检查同一规则是否只有一个事实源。
- [ ] N05｜检查弱模型可读性。

---

## Phase O｜Full Workflow Real Project

- [ ] O00｜从更新后的歌库选一首全新真实歌曲。
- [ ] O01｜从 M0 开始执行，不继承旧 MV 的具体人物 / 场景 / 构图。
- [ ] O02｜完成 Reference Gate。
- [ ] O03｜完成 BGM / Segment Lock。
- [ ] O04｜完成 K0 Gate。
- [ ] O05｜完成真实 5–15s 生成。
- [ ] O06｜完成 QA 与单变量迭代。
- [ ] O07｜得到最终通过版本或明确失败结论。

---

## Phase P｜oil-skill-creator Review / Evaluation

- [ ] P00｜静态 Review：P0 / P1 / P2。
- [ ] P01｜结构 / 重复 / 弱模型 / 宿主中立检查。
- [ ] P02｜建立真实 `evals/evals.json`。
- [ ] P03｜准备 `with_skill` vs `without_skill` 或新旧版本对照。
- [ ] P04｜客观项与主观项分离。
- [ ] P05｜用户完成盲评 / Human QA。
- [ ] P06｜根据真实失败原因整改并回归。

---

## Phase Q｜Open Source Release

- [ ] Q00｜删除 / 排除单次项目数据、失败实验和个人路径。
- [ ] Q01｜公开仓库只保留执行 Skill 所需内容。
- [ ] Q02｜补齐必要 README / 安装 / 兼容 / 数据边界。
- [ ] Q03｜最终严格校验。
- [ ] Q04｜发布开源版本。
- [ ] Q05｜从干净环境重新跑一次主流程。

---

# 11. 当前 Active Module

**ACTIVE MODULE：Phase B / B00｜恢复历史参考账号 / 选歌小数据库**

当前允许：

1. 搜索 GitHub 历史文件与 Tracker，恢复可靠的参考账号 / 歌曲候选数据；
2. 找不到可靠数据时标 `UNKNOWN / NEED REBUILD`，不猜；
3. 更新数据库字段设计；
4. 先建立第一批可实际用于选歌的候选。

当前禁止：

- 不直接跳到 K0；
- 不恢复旧的甲乙丙丁实验；
- 不把历史 Harness 整体复制进 Skill；
- 不一次性创建全部 references；
- 不因为一条旧 MV 做过就把对应规则判为 PROMOTED。

---

# 12. 实验与正式规则隔离

以下内容默认不得直接写入正式 Skill：

- 某一首具体歌曲；
- 某一个抖音链接；
- 某一次 K0 提示词；
- 某个具体人物名字；
- 某次失败的临时补丁；
- 甲乙丙丁的单次实验结果；
- 对某个平台当前版本的未验证猜测；
- 聊天中的临时决定；
- 历史 Review / 修改记录。

只有跨任务仍成立的规则才能 Promote。

---

# 13. 最终成功标准

- [ ] 新对话可以仅通过 Skill + 项目状态恢复工作，不需要用户重讲整套历史。
- [ ] 选歌优先利用参考账号 / 歌库，不从零随机搜索。
- [ ] 不再混淆 Douyin Reference / DEPTH / K0 / Prompt 的职责。
- [ ] 生成时长可按歌词 / 卡点 /画面任务在 5–15s 内灵活决定。
- [ ] 默认动画路线稳定，不依赖真人身份还原。
- [ ] Dola / Seedance 2.5 默认保持 K0 + Prompt 的简单执行路径。
- [ ] 不会因为流程太长而一次加载全部历史文档。
- [ ] 同一规则没有在多份文件重复维护。
- [ ] 至少一个全新真实 MV 项目完整通过。
- [ ] Skill 对照普通 Agent 或旧方案有可见改善。
- [ ] 主观质量由用户确认，而不是 AI 自评代替。
- [ ] oil-skill-creator Review / Evaluation 的关键问题已解决或明确接受。
- [ ] 开源版本从干净环境可再次运行。

---

# 14. 下一步

只执行：

**Phase B / B00｜恢复历史参考账号 / 选歌小数据库。**

恢复后先做可靠性标记，再进入字段更新和第一批候选数据库更新。