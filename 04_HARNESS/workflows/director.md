# Workflow｜Director & Material Audit v1.1

> Status: `ACTIVE / MOVING-CHARACTER CAMERA GRAMMAR ADDED`
> Added evidence: Face R&D 02 `Healing Tension + Moving Camera`, 2026-08-25.

## Responsibility
把真实时间轴转成可生产的导演表；决定每段“为什么这样拍”，而不是先决定用什么工具或套用某一种运镜。

导演先决定：
1. 这句歌词/语义的叙事任务；
2. 观众应该站在人物的什么位置；
3. 人物是否需要真实位移；
4. 摄影机与人物是什么关系；
5. 最后才命名具体摄影机运动。

## Input Contract
- `SCRIPT_LOCKED`
- `AUDIO_LOCKED`
- 句级真实时间轴
- 当前真实Evidence与已存在Asset
- 若已通过 HG03：实际验收首帧 / K0 pixels 为最高视觉真值

## Visual Function Routing
- Evidence → REAL
- Complex Explanation / Logic Motion → HyperFrames优先
- Simple Explanation / Utility → Remotion/程序化简单组件
- Concept / Emotion → AI按需
- Capability Proof → REAL OUTPUT

## Camera–Subject Relationship｜MOVING CHARACTER DIRECTOR CONTRACT

人物镜头不再默认采用“人物站着 + 摄影机自己动”。导演必须先判断歌词是否需要：
- 人物主动接近 / 离开；
- 人物穿过空间；
- 人物持续行走；
- 人物被摄影机发现 / 追上；
- 摄影机主动让位 / 保持 / 领先。

对需要人物运动的 Beat，先选择一种主要关系：

- `HOLD / OBSERVE`：摄影机稳定观察，人物承担表演；
- `FOLLOW`：摄影机从后侧或侧后跟随人物移动；
- `LEAD`：摄影机位于人物前方，与人物同轴移动；
- `YIELD`：人物向摄影机方向移动，摄影机后退或侧退让出路径；
- `OVERTAKE`：摄影机沿真实平移路径追上并略微超过持续移动的人物；
- `DISCOVER / REVEAL`：摄影机通过前景、遮挡或空间移动逐步发现人物/信息。

### Relationship first, move second

禁止只写：
`横移 / 推近 / 环绕 / 电影级运镜`。

必须至少明确：
- Camera start position；
- subject screen direction / movement direction；
- camera–subject relationship；
- relative speed / relative distance change；
- physical camera path；
- endpoint / edit handoff。

例如：
- `LEAD`: 人物向前走，摄影机在前方稳定后退；若要产生靠近感，人物前进速度略快于摄影机后退速度；
- `YIELD`: 人物持续穿过空间，摄影机只短距离后退 + 侧退，为人物让出路径；
- `FOLLOW -> OVERTAKE -> LEAD`: 摄影机从后3/4真实向前平移，经侧面追上并略微超过人物；这是 translational tracking，不是原地 orbit。

## Moving Subject Control Budget｜HARD DIRECTOR RULE

5秒人物 I2V 默认仍遵守：

`1 primary subject event + 1 primary camera relationship/move + 1 secondary physical feedback`

如果摄影机运动复杂度为 `M–L`：
- 人物主事件必须简化；
- 不同时加入复杂液体 / 镜面 / 大幅手部变化 / 多次表情高潮；
- 人物可持续行走，但头部、手部、道具只允许一个小的附属变化；
- 需要大角度人脸变化时，优先让身体运动方向稳定。

如果人物运动复杂度为 `M–L`：
- 摄影机只保留一个明确关系；
- 环境只承担风、布料、叶片、光、水面等次级余韵；
- 不把每个5秒都做成多镜炫技段。

## K0 Action Phase Continuity｜HARD DIRECTOR RULE

实际验收首帧不是“动作开始前的概念图”，而是视频真实第0秒。

若 K0 已经处于动作中段：
- 手已经靠近镜头 → 从该手位继续，不先缩回再重新伸手；
- 人物已经在走 → 继续步态，不先停住再起步；
- 人物已经回头 → 从当前头部角度继续，不重置成完全背对；
- 布料已被风吹起 → 从当前受力状态继续，不重新发起一次新事件。

导演文字与 K0 冲突时：改 Director State / dynamic prompt，不改 K0 事实。

## Face-Degrade / Unveiled Character Path｜PRODUCTION-READY EXPERIMENTAL

Face R&D 02 三段测试提供正向证据：低信息面部首帧可以在视频中自然补全，并在人物行走、近前景手部、摄影机追越和头部角度变化中维持可接受的连续身份感。

当前层级：
`PRODUCTION-READY EXPERIMENTAL / NOT UNIVERSAL HARD DEFAULT`

允许在下一首真实 MV 中，当歌词和人物设计确实受益于无遮挡面部表演时，选择性启用。

不得因此删除原有面纱 / 面罩稳定路径；两者是不同生产模式。

评估项：
- `FACE_COMPLETION`
- `IDENTITY_STABILITY`
- `FACE_ROTATION_STABILITY`
- `GAIT_STABILITY`
- `CAMERA_EXECUTION`
- `EDITABILITY`

## Internal Attraction / Relationship Tension Direction

导演内部允许设计：靠近、错身、遮挡揭示、被发现、短暂眼神、距离变化等关系张力。

但生成提示词优先翻译成可执行的物理语言：
- 距离如何变化；
- 人物走向哪里；
- 手/布料位于哪里；
- 目光何时短暂停留；
- 摄影机如何跟随/让位/追越。

不要依赖抽象词如“性感 / 性张力 / 女性凝视 / 电影级动态”代替动作设计。

## Per-Segment Contract
使用 `templates/director_segment.md`，每段必须写：
- Narrative Task
- Voiceover / Lyric Range
- Evidence
- Visual Function
- Teaching Truth（解释段）
- Subject Motion Task
- Camera–Subject Relationship
- Camera Start / Path / Speed / Endpoint
- K0 Action Phase
- Text
- Assets
- Transition
- Fallback

## Material Coverage Gate
每个关键视觉必须属于：
- `REAL`
- `EXTRACTABLE`
- `PROGRAMMATIC`
- `GENERATABLE`（必须有Intent + Fallback）

`MISSING / ASSUMED` 禁止进入 Director Lock。

## Anti-Homogeneity
连续第三个语义段必须检查：
- 是否重复同一构图 / 景别；
- 是否重复“人物站立 + 风吹衣摆”；
- 是否摄影机总是慢推 / 慢拉；
- 是否人物从未发生真实空间位移；
- 是否 Camera–Subject Relationship 连续重复。

变化的是镜头语法与叙事位置，不是每天重做整套视觉语言。

## Output Contract
- 完整Director表
- Material Audit
- 新增Asset清单
- 每个移动人物 Beat 的 Camera–Subject Relationship
- 风险与Fallback
- `STATUS = DIRECTOR_LOCKED`
