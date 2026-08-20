# Knowledge → Rule Promotion Policy v1.0

## Why
避免“每发现一次问题就往SKILL里加一条”，导致规则膨胀和历史冲突。

## Lifecycle
```text
Observation
→ Lesson / Experiment
→ Repeated Validation
→ Proposed Rule
→ Rule Review
→ PRODUCTION_VALIDATED or PERFORMANCE_VALIDATED
→ Active Rule
→ Deprecate when disproved
```

## Observation / Lesson
单次制作发现、审片偏好、工具表现、失败案例先写入当日 `LESSONS_LEARNED` 或 `03_DATA/EXPERIMENTS.md`。

## PRODUCTION_VALIDATED
适用于工程稳定性：QA、音频、素材、导演执行、文件验收、确定性渲染。

可以由重复制作/技术验证升级，不要求平台流量证明。

## PERFORMANCE_VALIDATED
适用于增长规律：Hook、时长、封面、标签、视觉形式、内容模型。

必须有重复真实发布数据支持。单条结果默认不升级。

## Promotion Check
升级前回答：
- 规则解决的具体失败是什么？
- 是否至少跨多个案例仍成立？
- 它属于哪个现有Rule文件？
- 是否已存在语义重复规则？
- 能否写成可验收条件，而不是模糊偏好？

如果不能明确回答，不升级。

## Deprecation
旧规则失效时不要在后面追加“例外”。直接在同一权威Rule文件替换或标记废止，并在 `00_CONTROL/CHANGELOG.md` 记录原因。
