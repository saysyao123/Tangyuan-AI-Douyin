# VISUAL_SYSTEM v1.1

> Day1生产验证后的稳定视觉系统 + Day2 HyperFrames 解释层验证。  
> 固化“视觉职能、稳定生产、美术纪律”，不把某一种电影风或某一种Frame preset锁成账号永久风格。

---

## 1. 画幅

- 9:16
- 1080×1920
- 默认30fps

所有程序化视觉必须从一开始按9:16设计。

禁止：

> 先做16:9横屏，再裁成竖屏。

---

## 2. 字幕 Default v1

当前生产验证稳定：

- 字体：Noto Sans CJK Medium（环境可用时）
- 常规字号：约48px
- 正文：白色
- 关键词：暖黄 `#FFD54A`
- 双层轻阴影
- 局部 Soft Scrim
- 字幕中心约 Y=1432
- 一行优先，最多两行
- 按语义块出现
- 不逐字弹跳
- 不做关键词Bounce

注意：

Day1早期曾用56–64px，后续实际审片稳定在约48px。

字幕负责完整语言。

程序化画面中的大字、节点、标签只负责视觉关系，不重复整段口播。

---

## 3. 镜头运动

必须有：
- 起点
- 单一主方向
- 终点

优先：
- 1.00→1.04/1.08稳定推进
- 单向平移
- 固定轴缩放
- Cut + 120–220ms淡变

默认禁止：
- 呼吸式Zoom
- 随机漂移
- 反复摇摆
- 无语义浮动

### HyperFrames补充

摄影机只有在“移动本身能解释逻辑”时才移动，例如：

- 沿因果链从原因移动到结果
- 从一个局部拉开看到完整系统
- 沿连续流程移动到下一站

禁止每个程序化场景都默认慢Push。

---

## 4. 真实素材

### Source Asset
高清原图。
用于：
- 放大
- 特写
- 数字证据
- 裁局部

### Motion Asset
录屏/滚屏。
用于：
- 操作
- 页面运动
- 真实过程

低清Motion不承担高倍放大。

真实证据不得被AI或程序化界面“重新画成看起来像真的”。

---

## 5. Visual Function Routing v1.1

### Evidence
**REAL**

使用：
- 真实截图
- 真实数据
- 真实Prompt
- 真实日志
- 真实产物
- 真实Before/After

### Complex Explanation / Logic Motion
**HYPERFRAMES（主要手段）**

适用：
- 顺序
- 因果
- 状态变化
- 错误→修正
- 流程
- 循环
- 规则进入系统
- 多步骤机制
- 变量变化导致结果变化

读取：
`04_HARNESS/HYPERFRAMES_EXPLANATION_HARNESS.md`

### Simple Explanation / Utility
**REMOTION**

适用：
- 标题
- DAY XX
- 数字强调
- 标签
- CTA
- 截图卡
- 简单Before/After
- 字幕
- 稳定总装配

### Concept / Emotion
**AI VIDEO 按需**

只在：
- Hook
- 情绪
- 抽象概念
- 视觉隐喻
- Capability Proof展示

显著增加表达价值时使用。

### Capability Proof
**REAL OUTPUT**

真实成片、真实生成结果、真实工具输出。

---

## 6. HyperFrames｜Tangyuan AI Logic Motion v1

> 定位：暗色编辑科技感。  
> 目标：像一个真正的视频镜头，而不是网页、后台、咨询PPT或赛博HUD。

### 6.1 Palette

默认起点：

- Canvas：`#111511` 深墨绿黑
- Surface：`#171C18`
- Surface Elevated：`#202620`
- Primary Text：`#F1F0E8` 暖白
- Secondary Text：`#AEB5AA`
- Keyword / Voltage：`#FFD54A`
- Correct / Flow：`#78B9A5`
- Error：`#D26A5C`

原则：

- 一帧只允许一个真正的“Voltage Moment”抢主视觉
- Correct / Error 是语义色，不和关键词争主角
- 中性颜色向墨绿/暖色偏，不使用死灰
- 默认不用纯黑 `#000000`
- 默认不用纯白 `#FFFFFF`
- 禁止AI默认紫蓝渐变 / 霓虹青紫作为无意义科技感

这是一套账号解释层的默认起点，不是每个视频永久锁色。题材需要时可以建立新的 `DESIGN.md`，但必须先设计再制作。

### 6.2 Typography

中文：
- Noto Sans CJK / 思源黑体类

技术索引 / 英文 / 数字：
- JetBrains Mono / 同类等宽字体

规则：

- Hero 与第二层信息必须形成明确大小/重量差
- 视觉主标题应足够大，不使用网页字号
- 技术标签只做索引，不写长句
- 不在画面中再次抄完整口播

### 6.3 Hierarchy

每个主要程序化场景：

- 主视觉约占画面 40%–60%
- 同时主焦点不超过2个
- 至少使用2种层级手段建立第一主角：
  - Size
  - Weight
  - Contrast
  - Position
  - Motion order

Squint Test：

> 模糊看画面，仍能知道第一眼该看哪里。

### 6.4 Depth

程序化场景至少有三层：

1. Background：低对比暗场 / 网格 / hairline /环境结构
2. Midground：路径 / 次级节点 / Evidence surface
3. Foreground：当前Anchor / Hero / 最终结论

禁止只有一小团卡片浮在空背景中央。

### 6.5 Shapes

禁止默认所有信息都做成相同圆角卡片。

不同信息应使用不同视觉身份：

- 文件/Prompt → document / artifact surface
- 音频 → waveform / audio object
- 流程 → path / connector
- 核心对象 → anchor object
- 状态 → small label / indicator
- 结果 → artifact / hero output
- 结论 → typography / held read

卡片是容器之一，不是唯一视觉语言。

---

## 7. HyperFrames Motion Grammar

### Development Is Teaching

旁白讲到哪里，画面才发展到哪里。

禁止：

> 前25%把整张图全部摆完，后面只剩轻微漂浮。

### Build → Breathe → Resolve

- Build：逐步建立当前关系
- Breathe：关系可读，同时只保留一个主要环境运动
- Resolve：核心变化完成，最终关系清楚，并允许真正静止

比例按口播自由变化，不机械套百分比。

### Stillness

结论阶段允许静止。

禁止为了“高级”继续：
- 呼吸Zoom
- 无意义漂移
- 无意义Pan
- 所有节点持续悬浮

### Signature Move

一个场景只设一个真正的大动作。

它必须等于本段的逻辑动作：

- 顺序换位
- 线路断开重连
- 因果链生长
- 状态同步改变
- Camera Journey
- Rule进入系统
- Output生成

装饰动作不能与Signature Move争夺注意力。

---

## 8. 9:16 HyperFrames Layout

### Portrait First

竖屏从Storyboard阶段就按1080×1920设计。

### 默认规则

- 流程：纵向堆叠
- 两项比较：上下 / 前后 / 对角层级优先
- Hero视觉中心可围绕画高约42%的区域组织，但按内容调整
- 大字、短句、减少每行字数
- 主视觉40%–60%
- 三层深度
- 安全区避开平台UI和底部字幕区域

### Framing Variety

同一条视频至少使用3种不同framing，例如：

- Centered Hero
- Vertical Rule-of-Thirds
- Layered Depth
- Vertical Step Stack
- Full-Width Stacked Bands
- Portrait Asymmetric 60/40

禁止连续两个主要语义段使用完全相同framing。

---

## 9. Anti-Homogeneity v1.1

连续第三个语义段检查视觉语法重复。

不是每段换色、换字体、换设计语言，而是换“讲法”。

### 额外检查三个失败模式

#### Slideshow
- 内容前25%全部出现
- 后面只等旁白

#### Screensaver
- 所有元素各自漂浮
- 无明确主次

#### Card Wall
- 每个概念都长成同一种卡片
- 画面像后台或PPT

出现任一项：不得Lock。

---

## 10. AI Cinematic Preset

Day1 Hook/Outro曾使用：

- 黑绿 / 深青
- 少量暖金
- 真实生活科技场景
- 浅景深
- 雨夜/城市反射
- 细胶片颗粒

状态：

**SCENE_PRESET_ONLY**

不是账号永久主视觉。

未来视频只有语义适配时才使用。

AI电影段与HyperFrames解释段不要求完全同风格，但必须共享：
- 基础色温关系
- 视觉节奏
- 字幕系统
- 主次纪律

避免出现“AI电影 → 突然切进一页PPT”的视觉断层。

---

## 11. 证据数字

所有真实数字，例如：
- 37
- 1092
- 719
- 后台数据

必须来自真实截图或明确标注后期文字。

不能让生成模型“重画成真实数据”。

HyperFrames同样不能通过程序化重绘伪装成平台真实证据。

---

## 12. HyperFrames Visual QA

每个主要HF段至少通过：

### Logic
- 关系与口播一致
- 先后没有画反
- 没有新增口播没有说的结论

### Clarity
- 3秒内知道看哪里
- 不看字幕也能大致理解关系
- 手机上的文字可读

### Beauty
- Squint：第一主角清楚
- Silence：有负空间
- Restraint：强调色和装饰克制
- Reference：像视频镜头，不像网页/PPT

### Motion
- Reveal跟着口播
- 没有Slideshow
- 没有Screensaver
- 只有一个Signature Move
- 结论敢停

只有全部通过，才能APPROVED。
