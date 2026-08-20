# Workflow｜Director & Material Audit v1.0

## Responsibility
把真实时间轴转成可生产的导演表；决定每段“为什么这样拍”，而不是先决定用什么工具。

## Input Contract
- `SCRIPT_LOCKED`
- `AUDIO_LOCKED`
- 句级真实时间轴
- 当前真实Evidence与已存在Asset

## Visual Function Routing
- Evidence → REAL
- Complex Explanation / Logic Motion → HyperFrames优先
- Simple Explanation / Utility → Remotion/程序化简单组件
- Concept / Emotion → AI按需
- Capability Proof → REAL OUTPUT

## Per-Segment Contract
使用 `templates/director_segment.md`，每段必须写：
- Narrative Task
- Voiceover Range
- Evidence
- Visual Function
- Teaching Truth（解释段）
- Motion / Camera
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
连续第三个语义段必须检查是否重复“截图卡/放大/同构卡片”。变化的是镜头语法，不是每天重做整套视觉语言。

## Output Contract
- 完整Director表
- Material Audit
- 新增Asset清单
- 风险与Fallback
- `STATUS = DIRECTOR_LOCKED`
