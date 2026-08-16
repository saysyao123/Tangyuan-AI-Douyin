# VISUAL_SYSTEM v1.0

> Day1生产验证后的最小稳定视觉系统。  
> 只固化“稳定生产”部分，不把Day1某一种电影风锁成账号永久风格。

## 1. 画幅

- 9:16
- 1080×1920
- 默认30fps

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

## 3. 镜头运动

必须有：
- 起点
- 单一方向
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

## 5. Visual Function

- Evidence：真实
- Explanation：Remotion
- Concept/Emotion：AI可用
- Capability Proof：真实产物
- Transition：按需

## 6. Anti-Homogeneity

连续第三个语义段检查视觉语法重复。

不是每段换色、换字体、换设计语言，而是换“讲法”。

## 7. AI Cinematic Preset

Day1 Hook/Outro使用：

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

## 8. 证据数字

所有真实数字：
- 37
- 1092
- 719
- 后台数据

必须来自真实截图或明确标注后期文字。

不能让生成模型“重画成真实数据”。
