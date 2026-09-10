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
7. **HARD：具体 BGM / Audio Version 一旦取得，必须先完成 Full Timeline Lock；时间轴未 LOCKED，禁止进入 Reference Deconstruction、Director、K0、Prompt 或视频生成。**

---

# 1. 当前生产目标

建立稳定、简单、可恢复的**动画 MV Reference-First Skill**。

`核心账号/歌库 → 具体抖音参考视频 → 用户下载提供 → BGM / Audio Version Lock → Full Timeline Lock → Segment / Duration Plan → Reference 拆解 → 动画化导演翻译 → K0 → Dynamic Prompt → Dola/Seedance 2.5 I2V → QA → 单变量迭代 → Lock`

---

# 2. 已锁定长期原则

## 2.1 Timeline First｜HARD

时间轴是所有后续导演决策的上游基准。

取得具体 BGM 后，按固定顺序执行：

`BGM / Audio Version Lock → Full Timeline Lock → Segment Plan → Director`。

Full Timeline 至少包含：

- 精确音频总时长；
- 逐句歌词 / 声音事件起止；
- 关键 Beat / Accent / Transition；
- 情绪段落边界；
- 可切 Segment 边界；
- 开始 / 高潮 / 收束 / Ending 落点；
- 对不确定点明确标记 `NEED_VERIFY`，禁止猜测后继续。

时间轴一旦 LOCKED：

- 后续 K0、动作、镜头、Prompt 必须引用该时间轴；
- 若 BGM / Audio Version 改变，Timeline 及其下游全部失效；
- 若只改下游视觉，不得反向修改已 LOCKED Timeline。

## 2.2 时长

- 歌词视觉命中 > 轻叙事连续 > 炫技。
- 单段按内容在 **5–15s** 灵活决定。
- 5–7s：单一事件；8–10s：完整小段；10–15s：起势→发展→高潮→收束。
- **最终 Segment 时长只能在 Full Timeline Lock 后决定，不允许先拍脑袋决定 5 / 10 / 15s。**

## 2.3 动画视觉

默认不走真人路线。

- 人物：One Piece 式高辨识轮廓 / 姿态张力 / 动作表现力，不复制具体角色。
- 场景：新海诚式明亮 / 治愈 / 通透 / 天空天气光影，不复制具体场景。
- 怪物 / 物品：吉卜力式温柔奇幻 / 灵性 / 陪伴感，不复制具体角色或道具。

## 2.4 核心账号与 Song Pool｜HARD

- 用户提供的 **9 个核心账号全部进入 Song Pool**。
- `Primary Role` 只决定权重和解释方式，不决定歌曲是否纳入。
- 视觉账号使用的歌曲同样是选歌证据；有时“歌曲 × 画面适配”价值更高。
- 同一 `SONG_FAMILY` 跨核心账号出现时提高信号。
- 数据更新采用 **BEST EFFORT**：能更新到哪里就到哪里，不追求伪最新。
- 搜不到更新作品 = `INDEX_PENDING`，不是“没发”。
- supplemental / 汽水音乐只做佐证，不替代核心账号。
- Work-level 原始事实源继续使用历史 `works.csv`，避免复制两套 89 行原始数据。

## 2.5 Douyin Reference

- 负责：选歌、卡点、动作、镜头、能量曲线、Peak、Ending。
- 迁移 Structure，不迁移真人身份 / 脸 / 原服装 / 原场景 / 具体视觉表达。
- Reference 源时长不限 5/15s。
- 用户选中**具体视频**后下载提供；此后先锁 AUDIO_VERSION 与 Full Timeline，再做导演拆解。

## 2.6 当前生成入口

- Dola / Seedance 2.5 Image-to-Video。
- 默认最简输入：**K0 + Dynamic Prompt**。
- refs ≤3–5；K0 单图够用就不补图。

## 2.7 K0 / Motion

- K0 = 可表演 0 秒动态锚点。
- 禁止无足部逻辑滑行 / 漂移；位移需抬脚→落脚→蹬地→重心转移→加减速。
- Prompt 正向目标优先，不因单次失败无限加禁止项。

## 2.8 DEPTH

- 未来 Motion Reference Adapter，不是当前必经。
- 已验证：GitHub Actions + Depth Anything V2 Small + Raw / Temporal / Compare。

---

# 3. Master Flow v1.2｜TIMELINE-FIRST

```text
M0  CORE ACCOUNT MUSIC DATABASE / SONG POOL
↓
M1  CORE DOUYIN VIDEO CANDIDATE SELECTION
↓
G1  HUMAN REFERENCE GATE
↓
M2  USER DOWNLOADS & PROVIDES SELECTED VIDEO
↓
M3  BGM ACQUISITION / AUDIO VERSION LOCK
↓
M4  FULL TIMELINE LOCK  ← HARD CHECKPOINT
    - exact duration
    - lyric / audio-event timestamps
    - beat / accent / transitions
    - emotional boundaries
    - valid cut points
    - peak / release / ending
↓
G2  TIMELINE GATE
    - no unresolved timing ambiguity
    - otherwise NEED_VERIFY and stop
↓
M5  SEGMENT / DURATION PLAN（5–15s flexible, derived from Timeline）
↓
M6  REFERENCE DECONSTRUCTION
↓
M7  ANIMATION DIRECTOR TRANSLATION
↓
M8  K0 FIRST FRAME
↓
G3  HUMAN K0 GATE
↓
M9  DYNAMIC PROMPT
↓
M10 DOLA / SEEDANCE 2.5 I2V
↓
M11 SEGMENT GENERATION
↓
M12 TECH QA
↓
M13 HUMAN QA
↓
PASS → LOCK
FAIL → CLASSIFY → ONE-VARIABLE ITERATION
↓
M14 ASSEMBLY（if multi-segment）
↓
M15 FINAL QA / LOCK
```

Optional：`Selected Reference → DEPTH → Temporal Motion → future Motion/Video Reference Adapter`。

---

# 4. Gate / Checkpoint

1. **Reference Gate**：强制；用户选择具体核心账号作品。
2. **Timeline Gate**：**硬检查点**；Timeline 未精确锁定不得进入导演流程。仅存在无法从素材确定的真实歧义时才需要用户额外判断。
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
- [x] A05.1 Timeline-First 修正：BGM 后必须先 Full Timeline Lock，再进入任何导演流程。
- [ ] A06 最终 Skill 名称 / 触发 / 反向边界。

## Phase B｜Core Account Music Database
- [x] B00 恢复 9 个核心账号。
- [x] B01 恢复历史 work-level 数据。
- [x] B02 数据可靠性 / Song Family / Audio Version 分层。
- [x] B03 选歌原则：动画治愈 / 卡点 / 5–15s / 动画化潜力。
- [x] B04 所有核心账号 `music_pool = YES`；Primary Role 只影响权重。
- [x] B05 统计 2026-08-10～08-17 历史抓取窗：89 works；8 个账号有作品，DYCORE09 为 data gap。
- [x] B06 Best-Effort 数据库更新：逐账号处理，明确覆盖与缺口；不追求同步最新。
- [ ] B07 Promote 稳定选歌规则（待本轮 Reference → Timeline 实测完成）。

Evidence：
- `01_REFERENCE_ACCOUNT_REGISTRY.md`
- `02_SONG_POOL_RECOVERY.csv`
- `test/mv-web-r3/06_TESTS/MV/WEB_R3/database/works.csv`

## Phase C｜Reference Selection / Handoff
- [x] C00 候选从 Core Song Pool 产生。
- [x] C01 每轮最多 3 个 Primary Candidates。
- [x] C02 每候选提供：核心账号 / 直链 / 时长 / 跨账号证据 / 动画适配 / Risk。
- [x] C03 Human Reference Gate：用户选择 `爱让人脑袋空空`。
- [x] C04 用户下载并上传具体 Reference 视频。
- [ ] C05 真实试跑完成（需 Timeline → Director → Generation → QA 后闭环）。
- [ ] C06 Promote。

Evidence：`04_SELECTION_ROUND_01.md` + 当前用户上传 Reference。

## Phase D｜BGM / Full Timeline Lock
- [x] D00 Reference 媒体技术探测：15.370998s；视频 1920×1080 30fps；AAC 44.1kHz stereo。
- [ ] D01 锁定具体 BGM / Audio Version。
- [ ] D02 建立完整逐句歌词 / Audio Event 时间轴。
- [ ] D03 标注 Beat / Accent / Transition / Emotional Boundary。
- [ ] D04 标注合法 Segment Cut Points / Peak / Release / Ending。
- [ ] D05 Timeline QA：所有关键点有证据；不确定点标 NEED_VERIFY。
- [ ] D06 `TIMELINE_LOCKED`。
- [ ] D07 判断哪些技术探测 / 时间轴步骤可脚本化。
- [ ] D08 Promote Timeline-First 规则（跨项目验证后）。

## Phase E｜Segment / Duration Plan
- [ ] E00 只基于 LOCKED Timeline 决定 5–15s Segment。
- [ ] E01 验证 5–7 / 8–10 / 10–15 三档。
- [ ] E02 多段 BGM 时，切点必须落在歌词 / 音乐 / 情绪合法边界。
- [ ] E03 实例验证。
- [ ] E04 Promote。

## Phase F｜Reference Deconstruction
- [ ] F00–F06：最小 Motion Map → 动作/重心/Camera/Energy/Ending → Copy Boundary → 实拆 → 删除装饰字段 → Human Review → Promote。

## Phase G｜Animation Director
- [ ] G00–G06：Locked Timeline + Motion → Animation Director → 三类审美职责 → 原创边界 → 最小导演输出 → 实测 → Review/Promote。

## Phase H｜K0
- [ ] H00–H06：K0 定义 → 动态锚点字段 → 动画默认 → 真图 → Gate → 改善验证 → Promote。

## Phase I｜Dynamic Prompt
- [ ] I00–I06：Timeline + Reference + Director + K0 编译 → 最小结构 → 卡点/动作链/Camera/Physics/Ending → 正向优先 → 无滑行 → 实测/Promote。

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
- [ ] O00–O06：新歌 → Reference Gate → **BGM + Timeline Lock** → K0 Gate → 5–15s → QA/Iteration → PASS/明确失败。

## Phase P｜oil-skill-creator Evaluation
- [ ] P00–P06：Review → 结构/弱模型 → evals → with/without → 客观/主观 → Human Review → 回归。

## Phase Q｜Open Source
- [ ] Q00–Q05：清理单次资产 → 最小 Skill → README → 校验 → 发布 → 干净环境复跑。

---

# 6. Current Active Module

**ACTIVE MODULE：Phase D / D01–D06｜《爱让人脑袋空空》BGM + Full Timeline Lock**

已锁：

- Song Family：`爱让人脑袋空空`
- Primary Reference：用户上传具体抖音视频
- Reference duration：`15.370998s`

当前禁止推进：Reference Deconstruction / Director / K0 / Prompt / Generation。

下一步唯一任务：

1. 锁具体 Audio Version；
2. 建整段精确 Timeline；
3. 标歌词 / Beat / 情绪 / 合法切点；
4. QA 后标 `TIMELINE_LOCKED`；
5. 只有此后才能进入 Segment Plan 与 Director。

---

# 7. 恢复协议

真实项目 `PROJECT_STATE` 至少记录：Project / Song / Core Account / Primary Reference / Reference File / Audio Version / **Timeline Version / Timeline Status** / BGM Segment / Target Duration / Current Stage / K0 / Prompt Version / Generation Version / QA / Next Action。

状态：`PENDING / ACTIVE / GATED / LOCKED / REWORK`。

若 `Timeline Status != LOCKED`：禁止进入 Director / K0 / Prompt / Generation。