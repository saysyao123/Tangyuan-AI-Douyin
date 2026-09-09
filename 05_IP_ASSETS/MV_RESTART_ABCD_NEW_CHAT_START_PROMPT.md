# MV_RESTART_ABCD_NEW_CHAT_START_PROMPT v1.0

> 用于开启一个全新对话，从零重新测试此前未完整完成的“甲 / 乙 / 丙 / 丁”四条 MV 测试线。

请使用已连接的 GitHub，读取仓库：

`saysyao123/Tangyuan-AI-Douyin`

首先读取以下文件：

1. `04_HARNESS/MV_CURRENT_EXECUTION_HARNESS.md`
2. `04_HARNESS/DEPTH_MOTION_HARNESS.md`
3. `04_HARNESS/VIDEO_PRODUCTION_HARNESS.md`
4. `04_HARNESS/MV_MULTIMODAL_PIPELINE.md`（只作为历史 / 未来能力参考，不作为当前默认主线）
5. `04_HARNESS/MULTIMODAL_REFERENCE_HARNESS.md`（只作为历史 / 未来能力参考，不作为当前默认主线）

然后在仓库、测试记录、Tracker、06_TESTS 等现有资料中搜索并恢复此前“甲 / 乙 / 丙 / 丁”四条测试线的可靠定义和完成状态。

## 本轮原始目标

重新从头验证“甲 / 乙 / 丙 / 丁”四条测试线。

不要把上一轮未完成的生成结果当作已通过结果，不要为了续上旧进度而跳步骤。本轮是 clean restart。

本轮最终目标不是把流程写得越来越复杂，而是找到：

> 当前条件下，哪一种 MV 生产方式最稳定、最有审美质量、最能命中歌词 / 情绪、最容易重复生产。

## 当前硬状态

### 1. Dola 视频参考路线暂停

当前 Dola / 当前 image-to-video 入口不能可靠使用视频参考、音频参考与完整 `@Image / @Video / @Audio` 多模态绑定。

因此：

- 不继续围绕 Dola 测试视频参考；
- 不把“8 图 + Depth + BGM”作为当前默认输入方式；
- 不把复杂多模态 Prompt 当作当前必须路线。

### 2. 当前默认 MV 主线

读取并遵守：

`04_HARNESS/MV_CURRENT_EXECUTION_HARNESS.md`

默认执行逻辑：

```text
Audio Lock
→ Beat / Lyric Breakdown
→ Director Concept
→ Character Anchor
→ Scene Anchor
→ Shot List
→ First Frames
→ Dynamic Prompts
→ 15s Segment Generation
→ QA
→ One-variable Iteration
→ Final Assembly
```

### 3. DEPTH 必须完整保留

`DEPTH_MOTION_HARNESS.md` 已经实测成功，不能删除、降级或用旧 Proxy 替代。

当前 DEPTH 的定位是：

> 正式保留的 Motion Reference 资产生产路线，等待未来真正支持 Video Reference 的平台重新接回主线。

默认：

```text
GitHub Actions
→ Depth Anything V2 Small
→ Raw
→ Temporal
→ Original-vs-Depth Compare
```

Temporal 版优先作为未来 Motion Reference；30fps 为实用优先规格；≤60s 允许按有意义边界拆成约 15s 段。

## 关于“甲 / 乙 / 丙 / 丁”的第一步

不要凭记忆或猜测定义甲乙丙丁。

第一步必须：

1. 搜索 GitHub 当前可恢复的定义、测试记录和状态；
2. 输出一张非常简洁的“ABCD Recovery Table”：
   - 测试线
   - 原始目标
   - 已完成
   - 未完成
   - 当前是否仍值得测
3. 如果某一条无法从可靠资料恢复，明确写 `UNKNOWN / NEED REBUILD`，不要编造。
4. 如果四条定义无法完整恢复，则根据当前项目目标重新建立甲乙丙丁测试合同，但必须明确说明这是“重新定义”，不是“恢复旧定义”。

## 本轮测试纪律

### 一次只跑一条 Lane

顺序默认：

```text
甲
→ QA / 人工判断
→ 乙
→ QA / 人工判断
→ 丙
→ QA / 人工判断
→ 丁
→ QA / 人工判断
→ 最终横向比较
```

不要四条同时展开，不要一次生成大量素材。

### 每条 Lane 只需要回答四个问题

1. 画面是否明显好看？
2. 歌词 / 情绪是否明显命中？
3. 动作和镜头是否稳定、自然？
4. 这条路线是否值得重复生产？

### 当前动作硬规则

人物发生位移时：

```text
抬脚
→ 落脚
→ 蹬地
→ 重心转移
→ 加速 / 减速
```

禁止无足部逻辑的滑行 / 漂移。

当脚部信息不足时，不擅自创造大幅横向移动，优先稳定站位、转肩、转髋、躯干和重心变化。

### 当前视觉总原则

歌词视觉命中 > 轻叙事连续 > 炫技镜头。

首帧必须是“可表演的 0 秒动态锚点”，不是单纯漂亮静帧。

参考素材做减法：当前默认使用少量真正必要的参考图，不为丰富而堆图。

### 不要过度审核

完整流程可以存在，但只有影响下一步的核心 Gate 才停下来等人工确认。

不要每一个小步骤都问用户一次。

## 新对话开始后立即执行

请不要让我重新解释历史。

你需要直接完成：

### Step 1
读取上述 GitHub 文件。

### Step 2
恢复 / 重建“甲乙丙丁”四条测试线，并给出 ABCD Recovery Table。

### Step 3
明确指出：
- 哪些旧假设已经作废；
- 哪些规则仍有效；
- DEPTH 已保留但暂不强行接入当前 Dola 主线。

### Step 4
给出本轮 clean restart 的四条 Lane 顺序和最小测试方案。

### Step 5
直接从“甲”开始执行第一个真正需要产出的步骤。

如果甲需要先选音频 / 素材，就先完成选取与分析；如果需要首帧，就生成首帧；不要只停留在流程说明。

## 输出风格

- 中文
- 简洁但有足够执行细节
- 不重复历史背景长篇复述
- 不把未验证方案写成 LOCKED
- 真实工具结果优先
- 失败要明确说明失败，不假装完成
- 每轮尽量推进到一个实际可检查的产物或 Gate

## 一句话启动口令

> 读取当前 GitHub 状态 → 恢复 / 重建甲乙丙丁 → 作废 Dola 视频参考主线 → 保留 DEPTH → 按当前图生视频 MV Harness 从甲开始 clean restart → 一条 Lane 一个结果 → 最后横向比较。