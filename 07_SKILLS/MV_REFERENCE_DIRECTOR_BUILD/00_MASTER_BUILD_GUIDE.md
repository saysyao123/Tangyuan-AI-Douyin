# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Purpose: 逐段梳理、验证并固化一套稳定的 MV Reference-First 生产 Skill。

---

# 0. 本文件的地位

本文件是 **MV Reference Director Skill 构建阶段的唯一总控事实源（Single Source of Truth）**。

以后新开对话、换模型、换执行环境时，先读取本文件，再读取当前 Active Module 指向的文件。

不要依赖聊天记忆来判断进度；不要根据旧 Harness 猜当前状态；不要因为某一步“好像做过”就视为完成。

## 勾选规则

- `[ ]` = 尚未完成，或没有足够证据证明完成。
- `[x]` = 已完成，并且有真实产物 / 测试 / 用户确认作为证据。
- 任何项目只有在满足该步骤的 **Done Definition** 后才能勾选。
- 单次偶然成功不能直接 Promote 为 Skill 规则。
- 找不到可靠历史证据时，保持 `[ ]`，必要时标记 `UNKNOWN / NEED REBUILD`。
- 每次只允许一个 **Active Module** 处于推进状态。
- 完成当前 Active Module 后，先更新本文件，再进入下一模块。

---

# 1. 原始目标

建立一套可长期复用的 MV 生产 Skill，使 Agent 在获得歌曲 / 音频后，能够稳定执行：

`Audio → Lyric / Emotion / Motion Need → Douyin Reference Discovery → Human Reference Gate → Reference Deconstruction → Lyric × Motion Director Translation → Character → Scene → Shot / Motion Map → K0 → Dynamic Prompt → ~15s Generation → QA → One-variable Iteration → Final`

目标不是“偶尔做出一条好看的 AI MV”，而是建立：

1. 可重复；
2. 可恢复；
3. 可解释；
4. 可测试；
5. 不依赖长聊天上下文；
6. 不因平台能力变化就推翻整个方法；
7. 对较弱模型也尽量清楚；
8. 能通过真实项目和 A/B 对照证明有效。

---

# 2. 当前长期硬原则

这些原则当前视为已确认的设计约束，但在正式 Skill 中仍需放到正确层级，避免重复扩写。

- 歌词视觉命中 > 轻叙事连续 > 炫技镜头。
- 抖音参考视频是 **Director / Motion Reference 母版**，不是角色、美术、真人身份复制源。
- 当前 Dola / I2V 的 Video Reference 主线暂停，不因此删除 Reference-First 方法。
- DEPTH 保留为未来 Motion Reference Adapter，不是当前每条 MV 的必经步骤。
- K0 必须是“可表演的 0 秒动态锚点”，不是单纯漂亮静帧。
- 人物位移不得无足部逻辑地滑行 / 漂移；需要可读的抬脚、落脚、蹬地、重心转移和加减速。
- 优先正向描述目标与动作链，不为每次失败无限增加禁止项。
- 不堆参考；每个参考资产只承担明确角色。
- 不做过度审核；人工 Gate 只保留真正会改变结果的节点。
- 未验证实验留在 workspace / tests，不直接进入正式 Skill。

---

# 3. Skill 构建方法

采用 `oil-skill-creator` 的产品化思路：

1. 先确认流程真实有效；
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

每个模块和规则只允许以下状态：

- `EXPERIMENT`：正在试验，不能当正式规则。
- `VALIDATED`：至少一次真实任务证明可用，但仍需观察跨任务稳定性。
- `PROMOTED`：跨任务仍成立，允许进入正式 Skill。
- `RETIRED`：曾经有效，但已被更好的规则或平台能力替代。

默认状态：`EXPERIMENT`。

---

# 4. 全局工作方式

每个 Module 必须回答 7 个问题：

1. **目标**：为什么这一步存在？
2. **输入**：进入这一步必须有什么？
3. **Agent 判断**：哪些需要语义 / 审美 / 策略判断？
4. **Program / Tool**：哪些应当确定性执行？
5. **输出**：下一阶段必须拿到什么？
6. **Gate / Stop**：什么时候必须停下来让用户确认？
7. **Promote 条件**：什么证据足以进入正式 Skill？

任何模块没有回答清楚以上 7 点，不允许标记完成。

---

# 5. Master Flow 构建清单

## Phase A｜产品与流程定义

- [x] A00｜确认目标是“逐段构建 Skill”，不是一次性写完整 Skill。
- [x] A01｜确认采用 Reference-First MV 总体方向。
- [x] A02｜确认抖音 Reference 与 DEPTH / Character / Scene 分层。
- [x] A03｜确认 `oil-skill-creator` 作为 Skill 产品化方法参考。
- [x] A04｜建立本总控工作区与唯一总控文件。
- [ ] A05｜完成完整 Master Flow 的阶段边界确认。
- [ ] A06｜确认最终 Skill 名称、触发范围和反向边界。

**Phase A Done Definition**：Master Flow 每一阶段都有明确职责，且用户确认整体方向无明显缺口。

---

## Phase B｜M0 Audio / Song Segment

- [ ] B00｜定义 M0 目标与必要性。
- [ ] B01｜定义最小输入：音频 / 歌曲 / 用户指定片段。
- [ ] B02｜定义自动探测项：时长、格式、版本、可用片段等。
- [ ] B03｜定义什么时候需要人工 Audio Gate。
- [ ] B04｜定义 M0 标准输出。
- [ ] B05｜用一个真实歌曲案例试跑。
- [ ] B06｜根据试跑删掉无价值字段。
- [ ] B07｜判断是否需要脚本化音频探测 / 切段。
- [ ] B08｜将稳定规则 Promote 到 Skill 结构。

**Module 状态**：`EXPERIMENT`

---

## Phase C｜M1 Lyric / Emotion / Motion Need

- [ ] C00｜定义 M1 目标。
- [ ] C01｜定义歌词 / 情绪拆解的最小字段。
- [ ] C02｜明确“Motion Need”如何服务下一步 Reference Search。
- [ ] C03｜避免把导演方案提前写进歌词分析。
- [ ] C04｜用真实歌曲段试跑。
- [ ] C05｜用户确认拆解对搜参考有实际帮助。
- [ ] C06｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase D｜M2 Douyin Reference Discovery

- [ ] D00｜定义 Reference Discovery 的目标与边界。
- [ ] D01｜定义搜索输入：歌词功能 / Emotion Arc / Motion Need / 人物数量等。
- [ ] D02｜定义候选数量默认值（当前方向：最多 3 条）。
- [ ] D03｜定义每个候选必须提供的比较信息。
- [ ] D04｜明确 Reference 可以继承和不能继承的内容。
- [ ] D05｜用真实歌曲搜索真实抖音 Reference。
- [ ] D06｜进入 Human Reference Gate。
- [ ] D07｜用户确认候选展示方式足够用于选择。
- [ ] D08｜Promote 稳定规则到 `reference-discovery` 资源。

**Module 状态**：`EXPERIMENT`

---

## Phase E｜M3 Reference Gate + Deconstruction

- [ ] E00｜明确 Gate 输入和唯一决策目标。
- [ ] E01｜选定 Primary Reference。
- [ ] E02｜定义 Motion / Director Map 最小字段。
- [ ] E03｜包含动作、脚步 / 重心、手势、Camera、Energy、Ending。
- [ ] E04｜验证哪些字段是真正有用的，删除装饰性字段。
- [ ] E05｜明确 Structure Transfer / Copy Boundary。
- [ ] E06｜用真实 Reference 完成一次拆解。
- [ ] E07｜用户确认拆解结果能指导后续导演设计。
- [ ] E08｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase F｜M4 Lyric × Motion Director Translation

- [ ] F00｜定义“歌词结构 × 运动结构 → Director Concept”。
- [ ] F01｜禁止凭空跳过 Reference 直接做世界观设计。
- [ ] F02｜定义导演翻译最小输出。
- [ ] F03｜用真实歌词 + Reference Map 完成一次翻译。
- [ ] F04｜验证视觉命中是否高于纯自由导演。
- [ ] F05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase G｜M5 Character Anchor

- [ ] G00｜定义角色 Anchor 的职责。
- [ ] G01｜定义 Motion Compatibility 原则。
- [ ] G02｜避免人物服装 / 配饰妨碍动作可读性。
- [ ] G03｜确认初始阶段只需要最小角色资产。
- [ ] G04｜真实生成并人工 Gate。
- [ ] G05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase H｜M6 Scene / Performance Zone

- [ ] H00｜定义 Scene Anchor 职责。
- [ ] H01｜加入 Performance Zone / Movement Space。
- [ ] H02｜明确地面、脚部可见性、移动空间与遮挡要求。
- [ ] H03｜真实生成并验证场景与 Motion Map 匹配。
- [ ] H04｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase I｜M7 Shot + Motion Map

- [ ] I00｜定义 Shot Map 的最小字段。
- [ ] I01｜整合 Time / Lyric Function / Body / Foot-Weight / Camera / Ending State。
- [ ] I02｜删除无实际生产价值字段。
- [ ] I03｜用真实 MV 段完成一次完整 Shot + Motion Map。
- [ ] I04｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase J｜M8 First Frame / K0

- [ ] J00｜锁定 K0 = 可表演的 0 秒动态锚点。
- [ ] J01｜定义 Current State / Motion Entry / Weight State / Camera Relationship / Secondary Motion。
- [ ] J02｜生成真实 K0。
- [ ] J03｜Human K0 Gate：审美、歌词命中、动作入口、双脚 / 重心可读性。
- [ ] J04｜验证 K0 对后续动态生成有实际改善。
- [ ] J05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase K｜M9 Dynamic Prompt

- [ ] K00｜定义 Prompt 必须从 Reference Map + Director Translation + K0 编译，而非从零自由写。
- [ ] K01｜定义最小 Prompt 结构。
- [ ] K02｜明确正向目标优先、禁止项最小化。
- [ ] K03｜加入物理步法 / 重心链规则。
- [ ] K04｜用真实 K0 生成动态 Prompt。
- [ ] K05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase L｜M10 ~15s Generation

- [ ] L00｜定义约 15 秒是生成单元，不是 Reference 时长限制。
- [ ] L01｜定义当前 Image-to-Video 默认路径。
- [ ] L02｜明确平台能力变化只改变 Adapter，不推翻上游流程。
- [ ] L03｜完成一条真实约 15 秒生成。
- [ ] L04｜记录生成参数与必要证据。
- [ ] L05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase M｜M11 QA + One-variable Iteration

- [ ] M00｜锁定四项最终人工判断：好看 / 歌词命中 / 动作镜头自然 / 值得复用。
- [ ] M01｜定义客观 QA：时长、规格、明显技术错误等。
- [ ] M02｜定义单变量迭代规则。
- [ ] M03｜禁止一次同时修改多个核心变量后声称得到结论。
- [ ] M04｜完成真实 QA → Iteration → QA。
- [ ] M05｜Promote 稳定规则。

**Module 状态**：`EXPERIMENT`

---

## Phase N｜DEPTH Motion Adapter

- [ ] N00｜将 DEPTH 明确为可选 Adapter，而非主流程必经步骤。
- [ ] N01｜迁移已验证 GitHub Actions + Depth Anything V2 Small 路线。
- [ ] N02｜保留 Raw / Temporal / Compare 职责。
- [ ] N03｜定义平台支持 Video / Motion Reference 时的接入条件。
- [ ] N04｜定义平台不支持时的跳过条件。
- [ ] N05｜验证该模块不会污染当前 Image-first 主流程。
- [ ] N06｜Promote 稳定规则。

**Module 状态**：`VALIDATED`（DEPTH 转换链本身已实测；作为 MV Skill Adapter 的集成尚未完成）

---

## Phase O｜Skill Information Architecture

- [ ] O00｜确定正式 Skill 名称。
- [ ] O01｜确定 frontmatter description 与反向边界。
- [ ] O02｜生成最小 `SKILL.md`。
- [ ] O03｜只创建已经有稳定内容的 `references/`。
- [ ] O04｜只创建确有必要的 `scripts/`。
- [ ] O05｜检查同一规则是否只存在一个事实源。
- [ ] O06｜检查 SKILL.md 是否只保留主流程 / 分支 / 停止条件 / 导航。
- [ ] O07｜检查弱模型可读性。

---

## Phase P｜Full Workflow Real Project

- [ ] P00｜选择一首全新真实歌曲作为完整验证项目。
- [ ] P01｜从 M0 开始，不继承旧 MV 的具体人物 / 场景 / 构图。
- [ ] P02｜完整执行到 Reference Gate。
- [ ] P03｜完整执行到 K0 Gate。
- [ ] P04｜完成约 15 秒生成。
- [ ] P05｜完成 QA 与单变量迭代。
- [ ] P06｜得到最终通过版本或明确失败结论。
- [ ] P07｜记录 Skill 流程缺陷与平台 / 模型外部限制，二者分开。

---

## Phase Q｜oil-skill-creator Review / Evaluation

- [ ] Q00｜静态 Review：P0 / P1 / P2。
- [ ] Q01｜运行结构 / 重复 / 弱模型 / 宿主中立检查。
- [ ] Q02｜建立真实 `evals/evals.json`。
- [ ] Q03｜准备 `with_skill` vs `without_skill` 对照。
- [ ] Q04｜客观项：流程完整、遗漏、规格、返工、Token / 时间（能获取时）。
- [ ] Q05｜主观项由用户判断，不用 AI 自评分替代。
- [ ] Q06｜根据真实失败原因整改 Skill。
- [ ] Q07｜使用同类失败请求做回归。
- [ ] Q08｜确认新版无明显回归。

---

## Phase R｜Open Source Release

- [ ] R00｜删除 / 排除单次项目数据、失败实验和个人路径。
- [ ] R01｜公开仓库只保留执行 Skill 所需内容。
- [ ] R02｜补齐必要 README / 安装 / 兼容 / 数据边界。
- [ ] R03｜最终严格校验。
- [ ] R04｜打包 / 发布开源版本。
- [ ] R05｜用公开版本从新环境重新跑一次主流程。

---

# 6. 当前 Active Module

**ACTIVE MODULE：Phase A / A05｜完整 Master Flow 的阶段边界确认**

当前禁止：

- 不生成新的 MV K0；
- 不继续甲 / 乙 / 丙 / 丁测试；
- 不把现有 Harness 整体复制进 Skill；
- 不一次性创建全部 references；
- 不因为某个旧测试存在就标记对应模块完成。

当前允许：

1. 审核 Master Flow 是否符合真实需求；
2. 调整阶段顺序、职责、Gate 和停止条件；
3. 确认后勾选 A05；
4. 然后只进入 A06 或 Phase B，不跳步。

---

# 7. 人工 Gate 最小集合（当前设计）

候选 Gate：

1. **Audio Gate**：只有音频版本 / 片段存在真实歧义时触发。
2. **Reference Gate**：默认重要 Gate；用户从候选参考中选择 Primary Reference。
3. **K0 Gate**：用户确认视觉、角色、场景和动作入口。
4. **Final Video QA Gate**：用户回答最终四问。

原则：没有实际决策价值的 Gate 删除。

---

# 8. 实验与正式规则隔离

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

# 9. 失败归因顺序

当结果不好时，按顺序判断：

1. 输入是否不足或错误；
2. Reference 是否选错；
3. Reference Deconstruction 是否错误；
4. Director Translation 是否失真；
5. Character / Scene 是否不适合动作；
6. K0 是否不是可表演锚点；
7. Prompt 是否没有正确编译上游信息；
8. 平台 / 模型是否存在能力上限或随机波动；
9. Skill 是否真的缺规则。

只有第 9 项成立，或前面问题由 Skill 设计导致，才修改正式 Skill。

不要看到一次失败就追加永久禁止项。

---

# 10. 新对话恢复协议

新对话或上下文丢失时：

1. 读取本文件；
2. 找到 `Current Active Module`；
3. 检查该模块前一项是否已 `[x]`；
4. 只读取该模块明确指向的参考 / 测试文件；
5. 不重新解释已经 `[x]` 且有证据的模块；
6. 不跳到后续模块；
7. 完成当前项后先更新本文件；
8. 再继续下一项。

如果本文件与聊天记忆冲突，以本文件的已验证状态为准；如果本文件本身缺少证据，保持未完成并重新验证。

---

# 11. 最终成功标准

本项目只有同时满足以下条件才算完成：

- [ ] 新对话可以仅通过 Skill + 项目状态恢复工作，不需要用户重讲整套历史。
- [ ] 不再混淆 Douyin Reference / DEPTH / Character / Scene / K0 / Prompt 的职责。
- [ ] 不会跳过关键 Reference Gate。
- [ ] 不会因为流程太长而一次加载全部历史文档。
- [ ] 同一规则没有在多份文件重复维护。
- [ ] 普通 Agent / 弱模型的走错率明显下降。
- [ ] 至少一个全新真实 MV 项目完整通过。
- [ ] Skill 对照普通 Agent 或旧方案有可见改善。
- [ ] 主观质量由用户确认，而不是 AI 自评代替。
- [ ] oil-skill-creator Review / Evaluation 的关键问题已解决或明确接受。
- [ ] 开源版本从干净环境可再次运行。

---

# 12. 下一步

只执行：

**A05｜逐段确认 Master Flow 的阶段边界、先后顺序、每个阶段为什么存在，以及哪些阶段可以合并 / 删除。**

A05 未完成前，不开始正式 Skill 文件编写。
