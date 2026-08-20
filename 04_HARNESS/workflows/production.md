# Workflow｜Production & QA v1.0

## Responsibility
按已锁Director生产、验收、锁段、总装；不在生产中重写内容系统。

## Gate Flow
```text
ASSET QUALITY GATE
→ SEGMENT PRODUCTION
→ SEGMENT QA
→ HUMAN APPROVAL
→ SEGMENT LOCK
→ FULL CUT
→ FULL FILM QA
→ DELIVERABLE VERIFY
```

## Production Routing
- Evidence：真实原始素材 / 可验证抽取
- Complex Explanation：HyperFrames；必要时降级Remotion
- Simple Utility：已验证程序化组件
- Concept / Emotion：已有AI素材优先；新生成必须有明显表达价值

## Segment Lock
每个主要段落严格：
`Produce → QA → Approve → Lock`

已Approved段落不因后续局部问题随意重做。

## Full Film QA
### Technical
分辨率、fps、编码、音轨、时长、黑帧、文件存在。

### Visual
清晰度、裁切、漂移、文字居中/可读、转场、最终停帧、AI变形。

### Narrative
画面支持当前旁白；无“说A炫B”；无无意义空镜。

### Evidence
真实数字来自真实来源；不把目标画成结果；示意不冒充Evidence。

## Deliverable Verify
宣称完成前必须：
`exists → probe/ffprobe → QA → deliver`

## Efficiency Gate
目标：150分钟生产 + 30分钟异常缓冲。
累计超过120分钟仍未进入Full Cut时：先取消非必要AI镜头，再降低HF装饰/Camera复杂度，再降级简单程序化方案；禁止降低真实证据质量。

## Output Contract
- 已锁段落状态
- Full Cut
- QA报告
- 最终文件技术信息
- `STATUS = PRODUCTION_LOCKED`
