# MV_MULTIMODAL_PIPELINE v1.0

> 当前动画 MV / 舞蹈短片的默认执行顺序。目标：在 Seedance 2.5 多模态参考能力下，把“动作参考、角色、场景、BGM、时间轴”拆层控制，再按固定顺序组合。

## 状态

- 执行顺序：LOCKED FOR CURRENT TEST。
- DEPTH 路线：已实测通过，读取 `DEPTH_MOTION_HARNESS.md`。
- Multimodal Reference 结构：已固化，读取 `MULTIMODAL_REFERENCE_HARNESS.md`。
- Seedance 2.5 最终效果参数：首轮完整成片尚待 QA；允许后续迭代，但不得跳过顺序。

## 总原则

1. **先锁目标与音频，再锁动作，再做视觉，再上传，再写最终 Prompt。**
2. **动作与外观分离**：Motion 不负责角色身份；Character 不负责动作。
3. **一个素材一个主要职责**，减少多模态参考互相争夺控制权。
4. **先 QA 再下一步**，但不做过度审核；每个 Gate 只检查会影响下一步的关键问题。
5. **先跑完整基线，再做单变量修正**。
6. **1 分钟以内默认拆段生产**，不追求 60s 一次生成。

---

# Locked Flow

```text
P0  PROJECT / SEGMENT LOCK
↓
P1  MOTION REFERENCE LOCK
↓
P2  SOURCE DOWNLOAD + TECHNICAL QA
↓
P3  MASTER BGM LOCK
↓
P4  DEPTH GENERATION + DEPTH QA
↓
P5  CHARACTER STYLE / IDENTITY ANCHOR
↓
P6  CHARACTER MULTI-VIEW PACK
↓
P7  SCENE LOCK PACK
↓
P8  STORYBOARD / ATMOSPHERE PACK
↓
P9  ASSET ROLE MAP + INDEX PLAN
↓
P10 SEEDANCE UPLOAD + INDEX AUDIT
↓
P11 MULTIMODAL PROMPT ASSEMBLY
↓
P12 CLEAN BASELINE GENERATION
↓
P13 OUTPUT QA
↓
P14 ONE-VARIABLE ITERATION
↓
P15 SCALE TO 30–60s
↓
P16 FINAL ASSEMBLY / REVIEW
↓
P17 RULE UPGRADE
```

---

## P0｜Project / Segment Lock

先锁本轮测试合同：

- 目标时长
- 9:16 / 其他比例
- 主角数量
- BGM 来源
- 是否需要歌词 / 情绪段落
- 动作目标
- Style Preset
- 生成模型 / 平台

当前测试预设：

- 15.57s
- 9:16
- 单女主
- 动画人物
- 古风雅室
- 冒险动画人物设计 + 明亮动画电影背景 + 手作奇想物件语言

P0 未锁，不找素材。

## P1｜Motion Reference Lock

寻找一条真正值得借动作的公开参考视频。

优先：

- 单人
- 镜头稳定
- 动作连续
- 主体清晰
- 遮挡少
- 节奏明确
- 若测试脚步，必须完整看到脚和地面

只确定动作参考，不在这一阶段设计角色外观。

## P2｜Source Download + Technical QA

下载参考视频后立即 Probe：

- duration
- resolution
- aspect ratio
- fps
- codec
- audio presence

人工快速看：

- 动作是否完整
- 是否切镜
- 是否有严重遮挡
- 是否适合 Depth
- 是否真的满足本轮测试目标

不合格则回 P1，不继续投入。

## P3｜Master BGM Lock

两种允许模式：

### Mode A｜参考视频自带 BGM

直接从参考视频抽取原音轨，锁为 Master BGM。

### Mode B｜独立目标歌曲

先剪出最终目标音乐段，再让动作参考与这段 BGM 对齐。

一旦进入 P4，Master BGM 不再随意改变。

后续 Timeline 只认这条 Master BGM。

## P4｜Depth Generation + QA

读取：`DEPTH_MOTION_HARNESS.md`

默认：

```text
GitHub Actions
→ Depth Anything V2 Small
→ Raw Depth
→ Temporal Depth
→ Original-vs-Depth Compare
→ report.json
```

正式 Motion Reference 优先 Temporal Depth。

### <=60s 规则

- 高动态 / 强动作：优先 15s 分段；
- 稳定连续动作：可测试 20–30s 分段；
- 不要求 60s 单次处理；
- Depth 分段边界与最终 BGM / Timeline 边界一致。

Depth QA 不通过，不进入人物图生成。

## P5｜Character Style / Identity Anchor

先只生成 **1 张最强角色主锚点**。

先锁：

- 角色设计语言
- 脸型
- 发型
- 主服装
- 身材比例
- 色彩
- 可动画性

不要一开始就批量生成 10 张。

主锚点人工确认后再扩展。

## P6｜Character Multi-view Pack

由确认过的主锚点连续派生。

默认：

1. 全身正面
2. 全身 3/4
3. 背面 / 3/4
4. 正面脸部近景
5. 侧脸 / 3/4 近景

目标：不是五张漂亮插画，而是给 Seedance 一个一致的 Character Identity Pack。

角色图必须互相引用 / 延续同一锚点，禁止每张重新随机设计。

## P7｜Scene Lock Pack

默认只需要 2 张：

1. `Scene Master Wide`
2. `Performance Area Mid / Full`

先建立唯一空间，再做局部表演区域。

场景图负责：

- Architecture
- Layout
- Lighting
- Color
- Performance Zone

不负责重新设计人物。

## P8｜Storyboard / Atmosphere Pack

只生成 Timeline 真正会调用的特殊镜头。

不强制九宫格，不为了“素材丰富”堆图。

当前测试只额外保留：

- Sunset / Silhouette Closing Reference

未来如歌词需要，可按句增加：

- 情绪近景
- 特殊道具
- 关键姿态
- 转场构图

但每张必须有明确 Timeline 用途。

## P9｜Asset Role Map + Index Plan

在进入 Seedance 前先建立角色表：

```text
WHO      = Character Images
WHERE    = Scene Images
END LOOK = Atmosphere / Storyboard Image
HOW MOVE = Temporal Depth
WHEN     = Master BGM
```

然后写出预期上传编号。

当前测试：

```text
@Image1–5 = Character
@Image6–7 = Scene
@Image8   = Silhouette / Atmosphere
@Video1   = Temporal Depth
@Audio1   = Master BGM
```

## P10｜Seedance Upload + Index Audit

固定上传顺序：

```text
Character
→ Scene
→ Storyboard / Atmosphere
→ Temporal Depth
→ Master BGM
```

建议逐项上传，不一次多选。

上传后不立即生成。

必须核对 UI 实际编号与 P9 完全一致。

编号不一致先修 Prompt 映射，不靠猜。

## P11｜Multimodal Prompt Assembly

读取：`MULTIMODAL_REFERENCE_HARNESS.md`

Prompt 固定骨架：

```text
Task
→ Reference Binding
→ Character Isolation
→ Visual Direction
→ Timeline
→ Motion Priority
→ Motion Physics
→ Camera Discipline
→ Overall Requirements
```

关键不是 Prompt 越长越好，而是明确：

- 谁负责角色
- 谁负责空间
- 谁负责动作
- 谁负责节奏
- 哪个时间段谁优先

## P12｜Clean Baseline Generation

第一条正式结果必须是干净基线：

- 不临时加素材
- 不同时测试多个 Prompt 版本
- 不生成前反复换角色图
- 不偷偷换 Depth
- 不换 BGM

当前 15s 测试直接生成完整一条，不先拆成 3–5s。

## P13｜Output QA

固定看 7 项：

1. Character Identity
2. Scene Continuity
3. Reference Crossover
4. Depth Obedience
5. Audio Sync
6. Motion Physics / Foot Sliding
7. Ending Pose

### 当前最关键的成功判断

不是“漂不漂亮”，而是：

- 主舞段动作是否明显更接近 Depth；
- 人物身份是否没有被 Scene / Silhouette 图污染；
- BGM 卡点是否有效；
- Dance → Beauty → Dance → Silhouette 的控制权切换是否自然。

## P14｜One-variable Iteration

失败后一次只改一个层：

```text
Reference Mapping
Timeline
Motion Priority
Camera
Style
Depth Segment
Audio Alignment
```

如果不知道问题在哪，先用原始视频 vs Depth vs Seedance 成片三列对比定位，不凭感觉全盘重做。

## P15｜Scale to 30–60s

1 分钟以内默认采用分段生产。

推荐：

```text
0–15s
15–30s
30–45s
45–60s
```

或在 Seedance 30s 已验证稳定后：

```text
0–30s
30–60s
```

但默认仍优先 15s 高控制方案。

每段都重新绑定：

- Character Pack
- Scene Pack
- 对应 Depth Segment
- 对应 BGM Segment
- 对应 Storyboard / Atmosphere

连续性通过：

- 同一 Character Pack
- 同一 Scene Pack
- 上一段 Ending State
- 下一段 Opening State

实现，不要求用一条超长生成解决全部问题。

## P16｜Final Assembly / Review

所有分段通过后再合成完整 MV。

检查：

- 音频无缝
- 动作切点
- 角色一致
- 场景一致
- 光线连续
- 无黑帧 / 重复帧
- 结尾完整

必要时只修接缝，不重做已 APPROVED 的整段。

## P17｜Rule Upgrade

只把重复验证有效的规律升级。

当前分级：

### 已锁定
- Depth Anything V2 Small 云端 DEPTH 方案
- <=60s 允许拆段
- Temporal Depth 优先作为 Motion Reference
- 角色 / 场景 / Motion / Audio 分层
- 固定上传顺序 + Index Audit
- 一次只改一个主要变量

### 待首轮 Seedance 完整验证
- Motion Priority 分级是否显著提升控制
- 8图 + 1Depth + 1BGM 的最佳参考密度
- Scene / Silhouette Reference 是否会出现 crossover
- 15s 完整多模态一次生成的动作命中率

验证后再升级，不提前把“看起来合理”写成长期硬规则。

---

# 当前一句话执行口令

以后在本路线中，默认理解为：

> **锁目标 → 找动作 → 下载核验 → 锁 BGM → 做 Temporal Depth → 锁角色主锚点 → 做角色多视图 → 做 Scene Wide / Performance Area → 只补必要 Storyboard → 建 Role Map → 按角色/场景/氛围/Depth/BGM 顺序上传 → 核对编号 → 写 Binding + Timeline + Motion Priority Prompt → 生成完整基线 → QA → 单变量修正 → 15s 分段扩展到 1 分钟以内。**
