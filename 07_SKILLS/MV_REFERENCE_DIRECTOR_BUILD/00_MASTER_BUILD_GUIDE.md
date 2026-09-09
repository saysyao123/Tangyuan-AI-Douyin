# MV Reference Director Skill｜总控构建指南

> Repository: `saysyao123/Tangyuan-AI-Douyin`
> Workspace: `07_SKILLS/MV_REFERENCE_DIRECTOR_BUILD/`
> Status: **ACTIVE / BUILDING**
> Role: 构建阶段唯一总控事实源。

---

# 0. 使用规则

1. 新对话先读本文件。
2. 找 `Current Active Module`，只读取对应 Evidence。
3. `[x]` 必须有真实证据 / 用户确认。
4. 每次只推进一个 Active Module。
5. 单次成功不能直接 Promote。
6. 状态：`EXPERIMENT → VALIDATED → PROMOTED → RETIRED`。

---

# 1. 当前生产目标

建立稳定、简单、可恢复的**动画 MV Reference-First Skill**。

`核心账号/歌库 → 具体抖音参考视频 → 用户下载提供 → BGM/歌词/卡点核对 → 决定 5–15s 合适时长 → Reference 拆解 → 动画化导演翻译 → K0 → Dynamic Prompt → Dola/Seedance 2.5 I2V → QA → 单变量迭代 → Lock`

---

# 2. 已锁定长期原则

## 2.1 时长

- 歌词视觉命中 > 轻叙事连续 > 炫技。
- 单段按内容在 **5–15s** 灵活决定。
- 5–7s：单一事件；8–10s：完整小段；10–15s：起势→发展→高潮→收束。

## 2.2 动画视觉

默认不走真人路线。

- 人物：One Piece 式高辨识轮廓 / 姿态张力 / 动作表现力，不复制具体角色。
- 场景：新海诚式明亮 / 治愈 / 通透 / 天空天气光影，不复制具体场景。
- 怪物 / 物品：吉卜力式温柔奇幻 / 灵性 / 陪伴感，不复制具体角色或道具。

## 2.3 核心账号与 Song Pool｜HARD

- 用户提供的 **9 个核心账号全部进入 Song Pool**。
- `Primary Role` 只决定权重和解释方式，不决定歌曲是否纳入。
- 视觉账号使用的歌曲同样是选歌证据；有时“歌曲 × 画面适配”价值更高。
- 同一 `SONG_FAMILY` 跨核心账号出现时提高信号。
- 数据更新采用 **BEST EFFORT**：能更新到哪里就到哪里，不追求伪最新。
- 搜不到更新作品 = `INDEX_PENDING`，不是“没发”。
- supplemental / 汽水音乐只做佐证，不替代核心账号。
- Work-level 原始事实源继续使用历史 `works.csv`，避免复制两套 89 行原始数据。

## 2.4 Douyin Reference

- 负责：选歌、卡点、动作、镜头、能量曲线、Peak、Ending。
- 迁移 Structure，不迁移真人身份 / 脸 / 原服装 / 原场景 / 具体视觉表达。
- Reference 源时长不限 5/15s。
- 用户选中**具体视频**后下载提供；此后才锁 AUDIO_VERSION。

## 2.5 当前生成入口

- Dola / Seedance 2.5 Image-to-Video。
- 默认最简输入：**K0 + Dynamic Prompt**。
- refs ≤3–5；K0 单图够用就不补图。

## 2.6 K0 / Motion

- K0 = 可表演 0 秒动态锚点。
- 禁止无足部逻辑滑行 / 漂移；位移需抬脚→落脚→蹬地→重心转移→加减速。
- Prompt 正向目标优先，不因单次失败无限加禁止项。

## 2.7 DEPTH

- 未来 Motion Reference Adapter，不是当前必经。
- 已验证：GitHub Actions + Depth Anything V2 Small + Raw / Temporal / Compare。

---

# 3. Master Flow v1.1

```text
M0  CORE ACCOUNT MUSIC DATABASE / SONG POOL
↓
M1  CORE DOUYIN VIDEO CANDIDATE SELECTION
↓
G1  HUMAN REFERENCE GATE
↓
M2  USER DOWNLOADS & PROVIDES SELECTED VIDEO
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
M8  DYNAMIC PROMPT
↓
M9  DOLA / SEEDANCE 2.5 I2V
↓
M10 SEGMENT GENERATION
↓
M11 TECH QA
↓
M12 HUMAN QA
↓
PASS → LOCK
FAIL → CLASSIFY → ONE-VARIABLE ITERATION
↓
M13 ASSEMBLY（if multi-segment）
↓
M14 FINAL QA / LOCK
```

Optional：`Selected Reference → DEPTH → Temporal Motion → future Motion/Video Reference Adapter`。

---

# 4. Human Gate

1. **Reference Gate**：强制；用户打开具体核心账号作品，选择要下载的一条。
2. **Audio / Segment Gate**：条件触发；仅版本或切段有真实歧义时停。
3. **K0 Gate**：强制。
4. **Video QA Gate**：强制，只问：
   - 好看吗？
   - 歌词 / 情绪命中吗？
   - 动作 / 镜头自然吗？
   - 值得重复生产吗？

---

# 5. Skill 构建清单

## Phase A｜产品 / Flow
- [x] A00 逐段构建 Skill。
- [x] A01 Reference-First。
- [x] A02 Reference / DEPTH / Visual 分层。
- [x] A03 oil-skill-creator 产品化方法。
- [x] A04 总控工作区。
- [x] A05 Master Flow 边界。
- [ ] A06 最终 Skill 名称 / 触发 / 反向边界。

## Phase B｜Core Account Music Database
- [x] B00 恢复 9 个核心账号。
- [x] B01 恢复历史 work-level 数据。
- [x] B02 数据可靠性 / Song Family / Audio Version 分层。
- [x] B03 选歌原则：动画治愈 / 卡点 / 5–15s / 动画化潜力。
- [x] B04 所有核心账号 `music_pool = YES`；Primary Role 只影响权重。
- [x] B05 统计 2026-08-10～08-17 历史抓取窗：89 works；8 个账号有作品，DYCORE09 为 data gap。
- [x] B06 Best-Effort 数据库更新：逐账号处理，明确覆盖与缺口；不追求同步最新。
- [ ] B07 Promote 稳定选歌规则（待本轮实际 Reference Gate 验证）。

Evidence：
- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`
- `test/mv-web-r3/06_TESTS/MV/WEB_R3/database/works.csv`

## Phase C｜Reference Selection / Handoff
- [x] C00 候选从 Core Song Pool 产生。
- [x] C01 每轮最多 3 个 Primary Candidates。
- [x] C02 每候选提供：核心账号 / 直链 / 时长 / 跨账号证据 / 动画适配 / Risk。
- [ ] C03 Human Reference Gate。
- [ ] C04 用户下载后的标准交接。
- [ ] C05 真实试跑。
- [ ] C06 Promote。

Evidence：`04_SELECTION_ROUND_01.md`

## Phase D｜Audio / Lyrics / Beat
- [ ] D00–D06：核对目标 → 技术探测 → Gate → 标准输出 → 实测 → 脚本化判断 → Promote。

## Phase E｜Duration
- [ ] E00–E04：5–15s 判断规则 → 三档验证 → 服从歌词/卡点/动作 → 实例 → Promote。

## Phase F｜Reference Deconstruction
- [ ] F00–F06：最小 Motion Map → 动作/重心/Camera/Energy/Ending → Copy Boundary → 实拆 → 删除装饰字段 → Human Review → Promote。

## Phase G｜Animation Director
- [ ] G00–G06：Lyrics + Motion → Animation Director → 三类审美职责 → 原创边界 → 最小导演输出 → 实测 → Review/Promote。

## Phase H｜K0
- [ ] H00–H06：K0 定义 → 动态锚点字段 → 动画默认 → 真图 → Gate → 改善验证 → Promote。

## Phase I｜Dynamic Prompt
- [ ] I00–I06：Reference + Director + K0 编译 → 最小结构 → 卡点/动作链/Camera/Physics/Ending → 正向优先 → 无滑行 → 实测/Promote。

## Phase J｜Generation
- [ ] J00–J06：Dola/Seedance 2.5 Adapter → K0+Prompt → refs≤3–5 → 真实5–15s → Evidence → 可替换性 → Promote。

## Phase K｜QA / Iteration
- [ ] K00–K06：四问 → Tech QA → S/R/D/K/P/G → 最近层回退 → 单变量 → 实测闭环 → Promote。

## Phase L｜Assembly
- [ ] L00–L03：只拼 LOCKED → 连续性 QA → 不牵连已锁段 → 多段实测 Promote。

## Phase M｜DEPTH Adapter
- [ ] M00–M06：可选 → DAV2 Small → Raw/Temporal/Compare → 接入条件 → 自动跳过 → 不污染 I2V → Promote。
- 当前转换链：`VALIDATED / Skill integration pending`。

## Phase N｜Skill IA
- [ ] N00–N05：名称/触发 → 最小 SKILL.md → 稳定 references → 必要 scripts → 唯一事实源 → 弱模型。

## Phase O｜Full Real Project
- [ ] O00–O06：新歌 → Reference Gate → Audio Lock → K0 Gate → 5–15s → QA/Iteration → PASS/明确失败。

## Phase P｜oil-skill-creator Evaluation
- [ ] P00–P06：Review → 结构/弱模型 → evals → with/without → 客观/主观 → Human Review → 回归。

## Phase Q｜Open Source
- [ ] Q00–Q05：清理单次资产 → 最小 Skill → README → 校验 → 发布 → 干净环境复跑。

---

# 6. Current Active Module

**ACTIVE MODULE：Phase C / C03｜Human Reference Gate**

当前交付：`04_SELECTION_ROUND_01.md`

本轮 Primary Candidates：

1. `Summer Love / 爱在盛夏`｜Aura + XIANGJISHI
2. `爱让人脑袋空空`｜乐♩青春 + Aura + Lynne小凌 + 火乐烁
3. `向山河林响`｜火乐烁

用户实际打开具体抖音作品：

- 有合适 → 选定一条并下载发回 → C04 / D00。
- 都不合适 → 从完整 Core Song Pool 输出 Round 02 三条；不退回随机平台榜。

---

# 7. 恢复协议

真实项目后续 `PROJECT_STATE` 至少记录：Project / Song / Core Account / Primary Reference / Reference File / Audio Version / BGM Segment / Target Duration / Current Stage / K0 / Prompt Version / Generation Version / QA / Next Action。

状态：`PENDING / ACTIVE / GATED / LOCKED / REWORK`。