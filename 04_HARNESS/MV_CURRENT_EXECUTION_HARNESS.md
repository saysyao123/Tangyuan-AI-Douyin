# MV_CURRENT_EXECUTION_HARNESS v1.0

> 当前实际可执行的 MV 默认流程。用于在 Dola / 当前 image-to-video 入口无法可靠使用视频参考与音频参考时，回到稳定的“音频 → 导演 → 首帧 → 动态提示词 → 15s 分段生成 → QA → 拼接”路线。

## 状态

- 当前默认主线：ACTIVE。
- Dola / 当前入口的视频参考测试：PAUSED，不再作为当前主生产路线继续投入。
- `MV_MULTIMODAL_PIPELINE.md` 与 `MULTIMODAL_REFERENCE_HARNESS.md`：保留为未来真正支持视频 / 音频参考的平台实验方案，不作为当前默认执行路线。
- `DEPTH_MOTION_HARNESS.md`：继续正式保留，状态仍为 VALID / PRESERVED，不废弃。

## 核心结论

1. 当前入口不能可靠完成正式 `@Video` / `@Audio` 多模态参考工作流，因此不再围绕 8 图 + Depth + BGM 堆叠测试。
2. 当前 MV 主线回到已验证更稳定的图生视频路线。
3. 正式生产单元默认 15 秒；更长 MV 采用 15 秒分段生产后拼接。
4. 参考素材做减法：当前生成入口默认优先 1–3 张关键图片，而不是大量参考同时输入。
5. 时间轴保留导演结构，但不把 15 秒拆成过多微小指令段。
6. DEPTH 独立保留，等待未来真正支持视频参考的平台重新接回主线。

---

# Current Locked Flow

```text
C0  PROJECT / AUDIO LOCK
↓
C1  BEAT + LYRIC / EMOTION BREAKDOWN
↓
C2  DIRECTOR CONCEPT LOCK
↓
C3  CHARACTER ANCHOR
↓
C4  SCENE ANCHOR
↓
C5  SHOT LIST
↓
C6  FIRST-FRAME PACK
↓
C7  DYNAMIC PROMPTS
↓
C8  15s SEGMENT GENERATION
↓
C9  SEGMENT QA
↓
C10 ONE-VARIABLE ITERATION
↓
C11 FINAL ASSEMBLY
↓
C12 REVIEW + RULE UPGRADE
```

## C0｜Project / Audio Lock

先锁：
- 最终歌曲 / 音频片段
- 起止点
- 总时长
- 9:16 / 其他比例
- 主角数量
- 本段是歌词命中、情绪、舞蹈、叙事还是过渡

默认正式生产单元：15 秒。

## C1｜Beat + Lyric / Emotion Breakdown

把 15 秒拆成少量有效段落：
- Opening
- Development
- Peak
- Ending

默认 4–6 个镜头阶段，不为复杂而复杂。

## C2｜Director Concept Lock

只锁真正必要的导演变量：
- 主角
- 情绪弧线
- 世界 / 场景
- 动作类型
- 镜头气质
- 最终 Ending Image

不提前堆大量配角、乐器、道具或九宫格素材。

## C3｜Character Anchor

先生成 1 张最强角色锚图并人工确认。
确认后按需要扩展：
- 全身正面
- 全身 3/4
- 背面 / 背 3/4
- 正脸
- 侧脸

不要求每个项目都生成全套。

## C4｜Scene Anchor

默认只做真正需要的：
- Scene Master Wide
- Core Performance / Action Area
- Optional Ending Atmosphere

时间轴不调用的场景图不生成。

## C5｜Shot List

每个 15 秒段落形成紧凑导演表：
- Time Range
- Visual / Lyric Function
- Shot Size
- Main Action
- Camera
- Transition
- Required First Frame

优先 4–8 个有效镜头阶段，不默认十几个微镜头。

## C6｜First-Frame Pack

只为真正需要独立视觉锚点的镜头生成首帧。

首帧必须是“可表演的 0 秒动态锚点”：
- 当前身体状态
- 情绪压力
- 主动作入口
- 后续运动方向
- 可持续物理余韵

## C7｜Dynamic Prompts

当前入口默认：
- 参考图优先 1–3 张
- 不假设 `@Video1` / `@Audio1` 可用
- 不围绕未开放能力写伪绑定 Prompt
- 重点写动作逻辑、镜头、节奏感、物理惯性和 Ending Pose

长期动作硬规则继续生效：
- 禁止无足部逻辑滑行 / 漂移
- 位移需由抬脚 → 落脚 → 蹬地 → 重心转移 → 加减速产生
- 当脚部信息不足时，优先稳定站位、转髋、转肩、躯干和重心变化

## C8｜15s Segment Generation

默认按 15 秒正式单元生成。

30 秒：
- 0–15s
- 15–30s

60 秒：
- 0–15s
- 15–30s
- 30–45s
- 45–60s

除非新的平台 / 模型已实测证明 30s 一次生成更稳，否则不把超长一次生成作为默认。

## C9｜Segment QA

固定优先级：
1. 歌词 / 情绪命中
2. 人物一致性
3. 场景一致性
4. 动作可信度
5. 无滑行 / 漂移
6. 镜头清晰度
7. Ending Pose / Ending Hold

## C10｜One-variable Iteration

一次只改一个主要变量：
- Prompt
- Shot Structure
- First Frame
- Reference Count
- Scene Anchor

禁止一次失败后同时推翻全部层。

## C11｜Final Assembly

只拼接已经通过的分段。
检查：
- 音频连续
- 情绪连续
- 人物连续
- 场景 / 色调连续
- 接缝
- 最终收束

## C12｜Review + Rule Upgrade

只有重复验证有效的规则才升级。

---

# DEPTH Preservation

DEPTH 不属于当前 Dola 主线，但必须正式保留。

读取：`DEPTH_MOTION_HARNESS.md`

锁定方案：

```text
Public Motion Reference
→ GitHub Actions
→ Depth Anything V2 Small
→ Raw Depth
→ Temporal Depth
→ Original-vs-Depth Compare
→ report.json
```

正式用途：
- 未来真正支持 Video Reference 的 Seedance 入口
- 其他支持 Motion Reference 的模型 / 平台
- 精确舞蹈、重心、手势、动作节奏迁移

默认偏好：
- Temporal Depth 作为正式动作参考
- 30fps 为实际动作参考优先规格
- ≤60s 可按 15s 有意义边界拆分
- Proxy 轮廓方案不恢复为正式路线

---

# Route Selection

## 当前默认

```text
Audio
→ Director
→ Character / Scene Anchor
→ First Frames
→ Dynamic Prompt
→ 15s Generation
→ QA
→ Assembly
```

## 未来平台真正支持视频参考时

```text
Motion Video
→ DEPTH
→ Character / Scene
→ Video Reference Binding
→ Audio Reference
→ Multimodal Generation
```

在真正验证之前，不混用两条路线。