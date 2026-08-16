# HYPERFRAMES_EXPLANATION_HARNESS v1.0

> 状态：DAY02 实测通过后固化。  
> 角色：**HyperFrames = Logic Motion Engine（逻辑动态图形引擎）**。  
> 目标：让复杂逻辑“发生在观众眼前”，而不是把知识排成PPT。  
> 第一原则：**画面为内容服务。先讲明白、逻辑正确，再追求美观和动效。**

---

# 0｜适用范围

## 默认优先 HyperFrames

当旁白核心是下面任一种关系时，Explanation 默认优先 HyperFrames：

- 顺序变化
- 因果关系
- 错误 → 修正
- Before → Process → After
- 状态变化
- 工作流 / 流程
- 循环 / 反馈回路
- 规则进入系统
- 多步骤机制
- A/B关系需要“过程化”解释
- 一个变量改变，另一个结果随之改变

## 默认继续 Remotion

以下内容不需要为了“更高级”强行 HyperFrames：

- 普通标题
- DAY XX
- 数字强调
- 37粉等真实数字标注
- CTA
- 常规字幕
- 四句话截图卡
- 简单静态 Before / After
- 轻量标签 / 提示框
- 最终总装配

## 真实 Evidence 不被 HyperFrames 替代

真实截图、真实数据、真实 Prompt、真实产物、真实 QA：

> **先显示真实证据，再用 HyperFrames 解释关系。**

禁止把真实证据重新画成“看起来像真的”程序界面。

---

# 1｜来源与已验证学习

本 Harness 参考并吸收：

- `heygen-com/hyperframes`
  - `faceless-explainer`
  - `hyperframes-animation`
  - `hyperframes-creative`
  - `frame-presets`
- `heygen-com/hyperframes-launches`
  - Timeline Editor launch
  - Variables launch
  - Frame.md launch storyboard
  - PR-to-video launch
  - Website → HyperFrames
- `nexu-io/open-design` 的 HyperFrames / Remotion compatible frame 方案

本项目 DAY02 已做 HF03 A/B：

> **“顺序错 → 流程重排” HyperFrames 方向明显优于原 Remotion 卡片式解释。**

通过原因不是“动得更多”，而是：

> **同一个视觉世界里，结构真的发生变化；观众看到逻辑，而不是看到两张流程图。**

---

# 2｜HyperFrames 核心导演原则

## 2.1 Teaching Truth First

写任何 HyperFrames 场景前，先回答：

1. 这句旁白真正要让观众明白什么？
2. 哪个关系最容易被误解？
3. 如果把所有文字删掉，什么“变化”仍然能表达这层逻辑？
4. 最终观众必须记住哪一个视觉关系？

回答不清，不进入动画设计。

---

## 2.2 Development Is Teaching

禁止：

> 前 25% 把整张流程图全部摆出来 → 后 75% 只是轻微漂浮或等待旁白。

这属于 **Slideshow Failure**。

正确方式：

> 旁白讲到哪里，画面才长到哪里。

每个场景必须写成 **time-coded shot sequence**：

```text
Scene 1：只出现当前旁白正在说的第一层关系
Scene 2：下一概念被说到时，才新增 / 移动 / 替换对应元素
Scene 3：关键关系真正发生变化
Scene N：逻辑完成，停止炫技，留出完整读图
```

**画面如何形成，本身就是解释。**

---

## 2.3 Anchor + Variable + Consequence

复杂流程优先采用：

- **Anchor**：保持不动的核心对象
- **Variable**：真正发生变化的对象
- **Consequence**：变化之后的结果

例：DAY02 HF03

```text
Anchor      = AI
Variable    = 旧稿 / 真实录音进入 AI 的先后顺序
Consequence = 字幕结果是否被带偏
```

视觉设计：

- AI 节点不动
- 旧稿从主轨退出
- 真实录音进入主轨
- 正确流程从 AI 后继续生长

最终观众自然得到：

> AI没换，顺序换了。

---

## 2.4 Signature Move

每个 HyperFrames 场景只允许一个真正的 **Signature Move**。

它必须对应本段的核心逻辑。

可选：

- 节点换位
- 路径断开并重连
- Camera Journey：摄影机沿因果链移动
- Spatial Pan：在同一大画布中移动到下一站
- Fixed Anchor Cycle：一个锚点固定，周围状态变化
- Live Sync：改变 A，B 同步变化
- Comparison Split：两条路径同时比较
- Artifact Reveal：过程走完，最终产物出现

禁止：

- 同一场景同时使用多个抢戏大招
- 为了“高级”加入与逻辑无关的3D旋转、漂浮、粒子爆炸

---

# 3｜Anti-PPT / Anti-Screensaver

## Slideshow Failure

表现：
- 卡片一次性出现
- 旁白继续说，但视觉不再产生新信息
- 只是偶尔Zoom或漂移

修正：
- 把信息拆到VO节点
- 让关系逐步生成
- 把关键变化放到后50%

## Screensaver Failure

表现：
- 所有元素都在各自漂浮
- 没有主次
- 摄影机和对象都在动
- 看起来“高级”，但不知道该看哪

修正：
- 一个 Anchor
- 一个 Signature Move
- Hold 阶段允许真正静止

## Card Wall Failure

表现：
- 所有概念都长成相同圆角矩形
- 视觉上像咨询PPT或SaaS后台

修正：
- 不同信息使用不同视觉身份：
  - 输入：文件 / 音频波形 /真实截图
  - 流程：线 / 路径
  - 核心节点：实体锚点
  - 结果：最终产物 / 强调文字
  - 状态：小型标签或光点
- 卡片只是容器之一，不是唯一语言

---

# 4｜9:16 竖屏构图硬规则

所有短视频 HyperFrames 从一开始按：

- 1080×1920
- 9:16

设计。

禁止：

> 先做横屏 → 最后裁成竖屏。

## Portrait Rules

- 流程优先 **纵向堆叠**，不是横向长链
- 两项比较优先上下或斜向，而不是左右窄塞
- 主视觉约占画面 **40%–60%**
- 中央Hero的视觉中心约在画高的 **42%附近**，但按内容调整
- 关键文字：短句、大字、少换行
- 画面至少有：背景 / 中景结构 / 前景主视觉 三层
- 同一条视频至少使用 3 种不同 framing
- 禁止连续两个主要语义段使用完全相同构图

推荐 framing：

- Centered Hero
- Vertical Rule-of-Thirds
- Layered Depth
- Vertical Step Stack
- Full-Width Stacked Bands
- Asymmetric 60/40 的竖屏变体

慎用：

- 横向 Split Screen
- 横向 Triptych
- 细长多列仪表盘

---

# 5｜美术系统：Tangyuan AI Logic Motion v1

> 目标：暗色编辑科技感，不做赛博朋克HUD，不做SaaS后台，不做AI默认紫蓝渐变。

## 5.1 Palette

默认：

- Canvas：`#111511` 深墨绿黑，不用纯黑
- Surface：`#171C18`
- Surface Elevated：`#202620`
- Primary Text：`#F1F0E8` 暖白，不用纯白
- Secondary Text：`#AEB5AA`
- Keyword / Voltage：`#FFD54A`（与账号字幕系统一致）
- Correct / Flow：低饱和浅青绿，如 `#78B9A5`
- Error：克制暖红，如 `#D26A5C`

规则：

- 一帧只有 **一个主强调色时刻**
- Correct / Error 属于语义色，不与 Keyword 争主视觉
- 中性灰必须向墨绿/暖色轻微偏色
- 禁止默认蓝紫渐变、霓虹青紫、纯黑纯白

## 5.2 Typography

中文：
- Noto Sans CJK / 思源黑体类

英文 / 数字技术标签：
- JetBrains Mono / 等宽字体

层级：

- Hero：明显大于其他信息，至少形成约 3:1 的视觉权重差
- Body：只保留必要词，不承担完整口播
- Mono Label：只做技术索引、状态、数字，不写长句

原则：

> **旁白负责完整语言；HyperFrames负责关系。**

禁止把整句口播再次写满屏幕。

## 5.3 Depth

一帧至少 3 层：

1. Background：暗场 / 轻网格 / 极低对比环境结构
2. Midground：流程路径 / 次级节点 / Evidence surface
3. Foreground：当前核心 Anchor / Hero / 关键结论

背景不能空，但也不能成为第二主角。

## 5.4 Decorative Budget

每场允许少量：

- hairline
- grid
- low-opacity oversized ghost word
- 微弱环境光
- 极轻颗粒

禁止：

- 无意义漂浮圆球
- 满屏粒子
- 紫蓝AI渐变
- 六七个独立呼吸动画
- 科技HUD装饰墙

---

# 6｜Motion Grammar

## 6.1 Build → Breathe → Resolve

默认三阶段：

### Build
0–30%左右：
- 关键元素分批进入
- 不一次性摆满

### Breathe
30–70%左右：
- 逻辑继续建立
- 同一时间只有一个主要环境运动

### Resolve
70–100%左右：
- Signature Move完成
- 最终关系清楚
- 结论进入
- **敢于停住**

比例按旁白自由变化，不是机械模板。

## 6.2 Stillness Is Allowed

禁止为了“画面一直动”在结论阶段继续：

- 呼吸Zoom
- 漂移
- 无意义Pan

正确：

> 动作完成 → 读图 → Cut。

## 6.3 Easing = Meaning

- Enter：`.out`
- Exit：`.in`
- Move Between Positions：`.inOut`

不同元素不要全部同一速度、同一ease、同一方向。

速度：

- Fast：紧急 / 冲击
- Medium：解释 / 专业
- Slow：认知峰值 / 重量

## 6.4 Camera Movement Must Teach

摄影机只在它能解释空间关系时移动。

适合：

- 沿流程从原因移动到结果
- 从局部拉开看到完整系统
- 推向关键结果

不适合：

- 每场都慢Push
- 纯装饰Pan
- 追着所有小节点移动

---

# 7｜Blueprint Routing

优先从 HyperFrames proven shapes 选，不每次从零发明。

## 本项目高频

### Fixed Anchor Cycle
适合：
- AI不变，输入 / 状态改变
- 工作流核心固定，周围规则变化

### Spatial Pan Stations
适合：
- 多个步骤处在同一连续世界
- 摄影机沿步骤移动

### Camera Journey
适合：
- 原因 → 结果由摄影机旅行来解释

### Comparison Split
适合：
- 两种方法 A/B
- 竖屏改为上下或前后层级

### Grid / List Assemble
适合：
- 四问法
- 多项规则逐步形成

### Titlecard Reveal
适合：
- 认知峰值
- 结论/呼吸段

### Device / Evidence Surface
适合：
- 真实截图 / 真产物作为Hero

选择原则：

> Story truth first。Blueprint服务内容，内容不为Blueprint让路。

---

# 8｜Real Evidence + HyperFrames 混合规则

推荐结构：

```text
真实 Evidence
→ 锁定“事情真的发生”
→ HyperFrames 拆解关系
→ 必要时再回到真实结果
```

例：

```text
真实Storyboard错误图
→ HyperFrames解释：我要什么 / 不要什么 / Done标准
→ Day1真实正确成片
```

禁止：

- 用程序化动画替代真实数据
- 把日志内容改写成虚构软件界面冒充录像
- 为了美观重造平台UI

---

# 9｜HyperFrames Director Packet

每个准备进入生产的 HF 语义段必须填写：

```md
## HF-XX｜名称

Narrative Task:
Teaching Truth:
Evidence:
Visual Function: Explanation

Anchor:
Variable:
Consequence:
Signature Move:
Blueprint / Compose:

Focal:
Supporting Roles:

Scene 1 (...s):
Scene 2 (...s):
Scene 3 (...s):
Final Held Read (...s):

On-screen Text:
SFX:
Transition In:
Transition Out:

Fallback:
```

没有真实Audio前：

> 时间全部为 DRAFT_TIMING。

Audio Lock 后：

> 必须按真实 VO 重新写 time-coded windows。

---

# 10｜HyperFrames QA Gate

## A. Logic QA

必须全部 YES：

- 不看字幕，能大致看懂关系吗？
- 视觉因果与口播因果一致吗？
- 有没有把先后关系画反？
- 有没有视觉新增口播没有说的结论？
- 最终一帧是否清楚表达本段结论？

## B. Clarity QA

- 3秒内知道看哪里
- 同时主焦点 ≤ 2
- Hero 占比足够
- 字号在手机上可读
- 文字没有重复完整旁白
- 关系线不会穿过主文字

## C. Beauty QA

使用四个 Eyeball Tests：

### Squint
模糊看仍知道谁是第一主角。

### Silence
有没有足够负空间？是否一帧只讲一个主问题？

### Restraint
强调色是否克制？是否出现AI默认设计感？

### Reference
像一段真正的视频镜头，还是网页 / 后台 / PPT？

## D. Motion QA

- Reveal是否跟VO节点同步
- 是否前25%一次性摆完
- 是否所有元素都在漂
- 是否有唯一Signature Move
- 结论是否真正停住
- Camera是否有叙事理由

## E. Technical QA

HyperFrames正式环境可用时：

- `lint` PASS
- `check` PASS
- 关键中点 snapshot 检查
- 无溢出
- 无字体缺失
- 无冲突transform tween
- 无无限 repeat
- timeline seek-safe / deterministic

---

# 11｜Production Strategy

## 第一次使用新视觉语言

不要一次做完整条。

执行：

```text
1个代表场景
→ Produce
→ QA
→ Human Approve
→ Lock visual language
→ 批量扩展
```

DAY02 已按此路径测试 HF03，结果 PASS。

## 降级顺序

当 HyperFrames 场景制作成本超过价值：

1. 保留 Teaching Truth
2. 减少装饰
3. 减少摄影机运动
4. 保留唯一 Signature Move
5. 必要时降级为 Remotion 简单解释

禁止为了保住工具而牺牲“看得懂”。

---

# 12｜长期路由（当前状态）

```text
Evidence        → REAL
Complex Explanation / Logic Motion → HYPERFRAMES（主要手段）
Simple Explanation / Labels / Titles / CTA / Subtitle → REMOTION
Concept / Emotion / Hook Visual → AI VIDEO（按导演需要）
Capability Proof → REAL OUTPUT
Final Assembly  → 稳定主剪辑链路
```

优先级永远是：

> **逻辑正确 > 一眼看懂 > 画面美观 > 动画复杂度。**

不是：

> 动得越多越高级。
