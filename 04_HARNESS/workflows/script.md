# Workflow｜Knowledge Script v1.0

## Responsibility
把真实Source变成可录制口播稿。只处理内容逻辑与口语表达，不处理画面。

## Input Contract
使用 `templates/script_contract.md` 锁定：受众、核心观点、Must Keep、Evidence、因果链、目标时长。

## State Flow
`RAW → SOURCE_LOCKED → CONTRACT_LOCKED → INSIGHTS_LOCKED → HOOK_LOCKED → STRUCTURE_LOCKED → DRAFTED → EVALUATED → PATCH(max2) → HUMANIZED → FINAL_QA → SCRIPT_LOCKED`

## Process
1. **Source Analyzer**：先理解原始内容，不立即写Hook。
2. **Contract Locker**：锁定受众、讲述关系、核心观点、Must Keep、证据、因果链、时长。
3. **Insight Miner**：提炼核心观点、支撑点、信息差、记忆点。
4. **Hook Director**：生成3–5个候选；只能包装核心观点，不能发明主题；正文必须兑现。
5. **Structure Architect**：允许价值前置/轻倒叙，但因果链不能断。
6. **Spoken Draft**：第一稿直接按时长预算写。
7. **Evaluator**：检查原意、因果、受众、可执行、留存、口语、记忆、人称、时长。
8. **Patch Editor**：默认最多2轮，只修被指出位置。
9. **Humanizer**：只优化口语、停顿、活人感，不新增观点。
10. **Final Gate**：通过后锁稿。

## Hard Gates
- 观点漂移
- 因果断裂
- Hook不兑现
- 人称漂移
- 超硬时长
- 把研究内容伪装成亲测

## Output Contract
- `SCRIPT_FINAL`
- `CORE_POINT`
- `HOOK_PAYOFF_MAP`
- `EVIDENCE_REFERENCES`
- `TARGET_DURATION`
- `STATUS = SCRIPT_LOCKED`

最高规则：Source Before Hook / Logic Before Retention / Locked Means Locked / Patch, Don't Rewrite / Budget Never Regresses。
