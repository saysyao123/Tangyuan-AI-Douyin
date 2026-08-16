# VIDEO_PRODUCTION_HARNESS v2.0

> 目标：在可持续的3小时日更窗口内，将锁定的真实内容稳定做成可发布视频。  
> 核心：先锁信息与声音，再做画面；先复用，再新增；先通过Gate，再往后走。

## Gate Flow

```text
G0  TOPIC LOCK
↓
G1  SOURCE / EVIDENCE LOCK
↓
G2  SCRIPT LOCK
↓
G3  AUDIO LOCK
↓
G4  TRANSCRIPT + TIMELINE LOCK
↓
G5  DIRECTOR LOCK
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

### Anti-Homogeneity
连续第三段检查是否重复“卡片/放大/截图”语法。

## G6｜Asset Quality Gate

每个素材至少记录：
- Type：SOURCE / MOTION / AI / AUDIO
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

## G7｜Segment Production

优先顺序：

1. 真实素材
2. Remotion组件复用
3. 程序化解释
4. 已有AI素材
5. 新生成AI素材

不是每条视频都必须生成AI电影镜头。

## G8｜Segment QA + Lock

每个主要段落完成：

`Produce → QA → Human Approve → APPROVED`

APPROVED后不得因其他段的小修改牵连重做。

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

### Narrative
- 画面是否支持当前旁白
- 是否出现“说A炫B”
- 是否存在无意义空镜

### Evidence
- 真实数字是否来自真实素材
- 是否虚构数据
- 是否把目标做成已完成

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

## G13｜Rule Upgrade

只把重复验证的性能规律升级到LOCKED_RULES。

---

# 日更效率预算 v2.0

## 目标

Day2开始：

**150分钟生产目标 + 30分钟异常缓冲。**

## 默认预算

| 环节 | 目标 |
|---|---:|
| 上一条数据 + Topic Lock | 15 min |
| Source / Evidence | 10 min |
| Script Lock | 20 min |
| Record + Audio Lock | 20 min |
| Timeline + Director | 20 min |
| Production | 45–60 min |
| Full QA | 15–20 min |
| Publish Package | 10 min |

## 超时降级规则

累计超过120分钟且仍未进入Full Cut：

按顺序降复杂度：

1. 取消非必要AI生成镜头
2. 使用已有Remotion组件
3. 减少装饰性转场
4. 合并语义重复段
5. 不降低真实证据质量

禁止用“再生成一套视觉试试”解决超时。
