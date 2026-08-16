# HYPERFRAMES_ASSET_HARNESS v1.0

> 角色：管理 HyperFrames 的背景、程序化元素、生图资产、开源适配资产和真实Evidence。  
> 目标：从“每条视频临时找素材”升级为“可复用、可追踪、有IP风格的资产系统”。  
> 第一原则：**结构程序化，质感资产化，证据真实化。**

---

# 0｜Asset Routing

每个视觉元素进入制作前必须先归类。

## REAL
真实截图、真实视频、真实Prompt、真实QA、真实数据。

必须原样来源可追踪。

## PROGRAMMATIC
HyperFrames / SVG / Canvas / GSAP 生成。

适合：
- 路径
- 连接线
- 准确文字
- 数字
- 状态
- 逻辑结构
- 流程变化

## GENERATED_ASSET
AI生图生成的单元素 / 背景Plate。

适合：
- 材质
- 视觉符号
- 特殊载体
- 高质量背景
- 不规则形状
- IP化视觉对象

禁止承担：
- 准确文字
- 真实数字
- Evidence
- 精确流程结构

## OPEN_SOURCE_ADAPTED
来自开源组件/图标/背景/动画机制的二次适配。

必须：
- 记录来源
- 检查License
- 改成Tangyuan Skin
- 改成Tangyuan Motion Grammar
- 验证HyperFrames可Seek/确定性

## PRE_RENDERED_MEDIA
预先渲染好的背景视频/动效素材。

适合：
- Shader背景
- 第三方wall-clock动画难以直接seek时

---

# 1｜资产生产流程

```text
Narrative Role
↓
Asset Type Route
↓
Source / Generate / Program
↓
Tangyuan Skin
↓
Tangyuan Motion Grammar
↓
Deterministic Render Check
↓
Visual QA
↓
Registry
↓
APPROVED / REJECTED
```

禁止：

> 先做一个好看的东西，再想它能放在哪里。

必须先回答：

> 这个资产在叙事里承担什么？

---

# 2｜Primitive vs Block

参考 HyperFrames Registry：

## Primitive / Component
小型机制，没有独立镜头叙事。

例如：
- Tangyuan Node
- Status badge
- Grain
- Light sweep
- Connector
- Audio waveform
- Rule stamp

## Block
可以独立承担一个镜头或一段完整逻辑。

例如：
- Prompt → Generate → Result
- AI Chat Reveal
- QA Scan
- Rule Injection
- Before → Process → After
- Evidence Stage

原则：

> 能复用“机制”的做 Primitive；能复用“镜头结构”的做 Block。

---

# 3｜资产Registry字段

每个正式资产至少记录：

```yaml
id: TY-INPUT-001
name: Prompt Artifact
type: GENERATED_ASSET | PROGRAMMATIC | BLOCK | REAL | BACKGROUND
role: input
ip_skin: Tangyuan Logic v1
source: original | generated | open-source-adapted | real
source_ref: optional
license: optional
use_when:
  - 展示Prompt作为输入对象
avoid_when:
  - 需要展示真实Prompt全文时
restraint: medium
motion_verb: reveal / seat
background_compat:
  - BG01
  - BG02
safe_area: portrait-center
resolution: 1536x1536
transparent: true
contains_text: false
evidence_safe: false
status: DRAFT | QA | APPROVED | DEPRECATED
fallback: programmatic document surface
notes: ...
```

---

# 4｜use_when / avoid_when / restraint

这是资产能否长期稳定使用的关键。

每个资产不能只写“长什么样”。

必须写：

## use_when
什么时候它最能帮助表达。

## avoid_when
什么时候它会误导、抢戏、降低真实性。

## restraint
- low：可以频繁出现，但非常克制
- medium：一段1次
- high：整条视频1–2次

例如：

```yaml
name: Rule Patch
use_when:
  - 规则被正式写入工作流
avoid_when:
  - 只是普通提示词修改
  - 规则尚未通过验收
restraint: high
```

---

# 5｜Generated Asset Prompt Gate

生图前必须写：

- Asset Role
- Visual Identity
- Material
- Light Direction
- Camera / View
- Transparency
- Negative List
- Scale / Margin
- Motion Possibility

## 单元素默认Prompt骨架

```text
只生成一个独立视觉资产。
透明背景。
不要文字、数字、Logo、水印。
资产属于 Tangyuan AI Logic Motion 世界：深墨绿、暖白、少量暖黄Voltage，暗色编辑科技感，真实材质，不是卡通，不是赛博朋克HUD。
对象居中，四周留足透明空间，不裁切边缘。
统一左上/侧上方柔和主光，少量暖金轮廓光。
适合后续在9:16视频中缩放、平移、旋转和做轻Parallax。
```

正式Prompt必须再加当前Asset的具体结构。

---

# 6｜Generated Background Plate Gate

AI背景Plate默认：

- 9:16
- 无人物
- 无文字
- 无Logo
- 无真实UI
- 无准确数据
- 为前景Hero留负空间
- 有前/中/后景
- 允许1.00→1.03慢Push
- 支持Parallax

必须标记：

`BACKGROUND_ONLY = TRUE`

背景不能偷偷承担解释逻辑。

---

# 7｜Open-source Asset Adaptation

## 可以直接学习的内容

- Geometry
- Composition mechanic
- Motion recipe
- Parameter system
- Registry schema
- Blueprint structure
- Background math / shader idea

## 进入项目以前必须重做

- Color
- Typography
- Radius / surface
- Accent
- Motion token
- IP signifier

原则：

> **借机制，不借脸。**

---

# 8｜License Gate

开源不等于可以无条件复制。

任何代码/Asset直接进入仓库前：

1. 确认License
2. 记录Source
3. 判断是否允许修改/商用/再分发
4. 需要Attribution时保留
5. License不清晰时，只学习设计与机制，不直接复制代码/资产

优先：
- MIT
- Apache-2.0
- 明确允许修改/商用的开源许可

不清晰：
- 只做参考
- 自己重新实现

---

# 9｜Deterministic Animation Gate

网页动画“浏览器里会动”不等于HyperFrames最终Render可靠。

禁止直接依赖：
- wall-clock requestAnimationFrame
- 独立setInterval
- 与主timeline无关的无限动画
- 无法seek的第三方交互状态

解决顺序：

1. 将时间变量绑定到 HyperFrames / GSAP seekable timeline
2. 无法改造 → 预渲染为MP4/WebM
3. 只借视觉公式，自行做确定性实现

必须通过：

`SEEK TEST = PASS`

---

# 10｜Asset QA

## Logic QA
- 资产有没有改变原意？
- 会不会把示意误认为Evidence？

## Visual QA
- 和Tangyuan Skin一致吗？
- 有没有第三方模板味？
- 缩小到手机屏还看得懂吗？

## Motion QA
- 动作是否对应语义？
- 动效是不是比信息更抢眼？

## Technical QA
- 透明边缘
- 清晰度
- 分辨率
- Seek
- Render
- 黑边
- Color banding

## Reuse QA
- 下一个项目能不能复用？
- 需要改哪些变量？

---

# 11｜资产批准等级

## EXPERIMENTAL
只用于测试。

## PROJECT_APPROVED
当前项目可以用。

## IP_APPROVED
至少跨2条视频验证，风格稳定，可进入长期IP资产库。

## CORE_ASSET
长期识别资产。

例如未来验证后的：
- Tangyuan Node
- Evidence Frame
- Rule Patch
- Deep Silk

---

# 12｜资产增量原则

每条新视频最多新增：

- 1–2个新核心Asset
- 1个新Background Preset（只有必要时）
- 1个新Block

其他优先复用。

目的：

> **视频越做越快，IP资产越做越厚。**

不是：

> 每天重新设计一套视觉。

---

# 13｜与现有生产Gate衔接

## Director阶段
写清Asset ID / Background ID。

## Material Coverage
确认Asset：
- EXISTING
- GENERATABLE
- PROGRAMMATIC
- REAL

## Segment Production
先复用IP_APPROVED，再新制。

## QA
通过后更新Asset状态。

## Rule Upgrade
跨项目验证后才升级CORE_ASSET。

---

# 14｜最终原则

> **结构 = HyperFrames**  
> **质感 = Asset**  
> **空间 = Background**  
> **事实 = Evidence**  
> **准确语言 = Typography / Subtitle**  
> **统一识别 = Tangyuan Skin + Tangyuan Motion Grammar**
