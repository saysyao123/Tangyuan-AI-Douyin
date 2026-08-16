# VIDEO_PRODUCTION_HARNESS v2.1

> 目标：在可持续的3小时日更窗口内，将锁定的真实内容稳定做成可发布视频。  
> 核心：先锁信息与声音，再做画面；先复用，再新增；先通过Gate，再往后走。

## Gate Flow

```text
G0  TOPIC LOCK
↓
G1  SOURCE / EVIDENCE LOCK
↓
G1.5 MATERIAL COVERAGE CHECK
↓
G2  SCRIPT LOCK
↓
G3  AUDIO LOCK
↓
G4  TRANSCRIPT + TIMELINE LOCK
↓
G5  DIRECTOR LOCK
↓
G5.5 DIRECTOR MATERIAL AUDIT
↓
G6  ASSET QUALITY GATE
↓
G7  SEGMENT PRODUCTION
↓
G8  SEGMENT QA + HUMAN APPROVAL
↓
G9  FULL CUT
↓
G10 FULL FILM QA
↓
G11 PUBLISH PACKAGE
↓
G12 PERFORMANCE REVIEW
↓
G13 RULE UPGRADE
```

## G0｜Topic Lock

每天只允许一个主选题。

除非出现明显高价值新证据，不在制作中途换题。

## G1｜Source / Evidence Lock

先列真实证据，再写画面。

Evidence优先：
- 真实截图
- 真实工具结果
- Before/After
- 实际数据
- 实际Prompt/产物
- 失败案例

## G1.5｜Material Coverage Check

导演不能建立在“后面也许能找到素材”的假设上。

每个关键视觉必须归类：

- `REAL`：当前真实存在
- `EXTRACTABLE`：可从现有成片/文件真实抽取
- `PROGRAMMATIC`：可由 HyperFrames / Remotion 确定性生成
- `GENERATABLE`：计划新增 AI 素材，且已有明确 Director Intent + Fallback
- `MISSING / ASSUMED`：仅仅“应该有 / 以后再找”

`MISSING / ASSUMED` 禁止进入 Director Lock。

真实证据缺失时：
- 找回证据；或
- 重写导演；或
- 使用“真实记录 + 程序化解释”，并明确不是原始现场。

## G2｜Script Lock

使用 `KNOWLEDGE_SCRIPT_HARNESS.md`。

锁定后不因视觉炫技反向改核心逻辑。

## G3｜Audio Lock

使用 `AUDIO_PRODUCTION_HARNESS.md`。

没有最终Master Narration，不正式锁导演秒数。

## G4｜Transcript + Timeline Lock

生成：
- 实际逐字稿
- 清洁字幕稿
- 句级时间轴
- 总时长

Director以后只认真实音频。

## G5｜Director Lock

每个语义段写清：
- Narrative Task
- Evidence
- Visual Function
- Motion
- Text
- Transition
- Assets

视觉职能：
- Evidence
- Explanation
- Concept/Emotion
- Capability Proof
- Transition

### Explanation Routing v2.1

复杂逻辑解释默认读取：
`HYPERFRAMES_EXPLANATION_HARNESS.md`

路由：

- Evidence：真实素材
- Complex Explanation / Logic Motion：**HyperFrames优先**
- Simple Explanation / Labels / Title / CTA / Subtitle：Remotion
- Concept / Emotion：AI可用
- Capability Proof：真实产物

HyperFrames适用：
- 顺序
- 因果
- 状态变化
- 流程
- 循环
- 错误→修正
- 规则进入系统
- 多步骤机制

Remotion继续负责：
- 简单标题
- 数字强调
- 标签
- 截图卡
- CTA
- 字幕
- 最终稳定组装

### Anti-Homogeneity
连续第三段检查是否重复“卡片/放大/截图”语法。

HyperFrames 也必须检查：
- 是否变成Slideshow（前25%摆完，后面发呆）
- 是否变成Screensaver（所有元素各自漂浮）
- 是否变成Card Wall（所有概念都长成同一种卡片）

## G5.5｜Director Material Audit

正式 Director Lock 前检查：

> 导演表里的每一个镜头，现在真的做得出来吗？

必须满足：
- 关键事实100%有来源
- 主要旁白100%有对应视觉职能
- 不依赖未知文件
- 程序化解释不冒充真实Evidence
- AI生成镜头有Fallback
- HyperFrames场景有Teaching Truth + Anchor/Variable/Consequence + Signature Move

## G6｜Asset Quality Gate

每个素材至少记录：
- Type：SOURCE / MOTION / AI / AUDIO / PROGRAMMATIC
- Resolution
- Primary Use
- Can Upscale
- Contains Audio
- QA
- Status
- Used in Final

硬规则：
- Source高清图用于放大
- Motion录屏用于运动
- AI源音频默认删除
- 真实数字不被程序重造
- HyperFrames / Remotion 不重画真实证据冒充原始现场

## G7｜Segment Production

优先顺序根据 Visual Function 决定，不按工具炫技决定：

### Evidence
1. 真实原始素材
2. 真实成片可抽取素材

### Complex Explanation
1. HyperFrames
2. Remotion降级方案

### Simple Explanation / Utility
1. 已验证Remotion组件
2. 简单程序化解释

### Concept / Emotion
1. 已有AI素材
2. 新生成AI素材（只有显著增加表达价值时）

不是每条视频都必须生成AI电影镜头，也不是每个解释段都必须HyperFrames。

## G8｜Segment QA + Lock

每个主要段落完成：

`Produce → QA → Human Approve → APPROVED`

APPROVED后不得因其他段的小修改牵连重做。

HyperFrames新增：
- Logic QA
- Clarity QA
- Beauty QA
- Motion QA

详见：
`HYPERFRAMES_EXPLANATION_HARNESS.md`

## G9｜Full Cut

只在全部主要段落通过后合成。

最终只保留Master Narration Track。

## G10｜Full Film QA

四层：

### Technical
- 分辨率
- fps
- 编码
- 音轨
- 时长
- 黑帧
- 文件存在

### Visual
- 清晰度
- 裁切
- 漂移
- AI变形
- 转场
- 最终停帧
- HyperFrames 是否像“视频镜头”而非PPT/网页

### Narrative
- 画面是否支持当前旁白
- 是否出现“说A炫B”
- 是否存在无意义空镜
- 程序化关系是否与口播因果完全一致

### Evidence
- 真实数字是否来自真实素材
- 是否虚构数据
- 是否把目标做成已完成
- 是否把程序化示意冒充原始现场

只有：
`QA_PASS = TRUE`
才允许交付。

## G11｜Publish Package

读取：
`05_IP_ASSETS/PUBLISH_SYSTEM.md`

不在最后一刻重新研究整套发布体系。

## G12｜Performance Review

记录：
- 1h
- 3h
- 24h

生产体验好 ≠ 平台效果好。

HyperFrames相关额外记录：
- 是否提升观看理解
- 是否增加制作时间
- 是否值得复用为固定组件

## G13｜Rule Upgrade

只把重复验证的性能规律升级到LOCKED_RULES。

工具偏好先进入 Harness / Visual System；只有重复验证后才升级为长期硬规则。

---

# 日更效率预算 v2.1

## 目标

Day2开始：

**150分钟生产目标 + 30分钟异常缓冲。**

## 默认预算

| 环节 | 目标 |
|---|---:|
| 上一条数据 + Topic Lock | 15 min |
| Source / Evidence + Material Coverage | 10–15 min |
| Script Lock | 20 min |
| Record + Audio Lock | 20 min |
| Timeline + Director | 20–25 min |
| Production | 45–60 min |
| Full QA | 15–20 min |
| Publish Package | 10 min |

## 新视觉语言测试规则

第一次使用新的 HyperFrames 视觉语言：

```text
1个代表场景
→ Produce
→ QA
→ Human Approve
→ Lock
→ 批量扩展
```

禁止第一次就批量做6–10个复杂场景。

## 超时降级规则

累计超过120分钟且仍未进入Full Cut：

按顺序降复杂度：

1. 取消非必要AI生成镜头
2. HyperFrames保留Teaching Truth，减少装饰/Camera/次级Motion
3. 复杂HF场景必要时降级成简单Remotion解释
4. 使用已有Remotion组件
5. 减少装饰性转场
6. 合并语义重复段
7. 不降低真实证据质量

禁止用“再生成一套视觉试试”解决超时。
