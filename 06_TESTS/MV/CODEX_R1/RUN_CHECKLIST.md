# CODEX R1｜RUN CHECKLIST

> 给用户快速查看 Codex 当前执行效果。Codex 每完成一个 Stage 必须更新本表。

## Overall

- Current Mode: `MODE_A_ENGINEERING_REPRODUCTION`
- Current Stage: `C00`
- Overall State: `NOT_STARTED`
- Current Automation Score: `0/16`
- Human interventions: `0`
- Final publish-ready: `NO`

## Stage Board

| Stage | 内容 | 状态 | 自动化分 | 人工介入 | 关键结果 |
|---|---|---|---:|---:|---|
| C00 | 环境检查 | NOT_STARTED | 0/2 | 0 |  |
| C01 | BGM / Datasource | NOT_STARTED | 0/2 | 0 |  |
| C02 | 精确音频裁剪 | NOT_STARTED | 0/2 | 0 |  |
| C03 | Whisper字幕对齐 | NOT_STARTED | 0/2 | 0 |  |
| C04 | 无水印高清源替换 | NOT_STARTED | 0/2 | 0 |  |
| C05 | 剪辑时间线复刻 | NOT_STARTED | 0/2 | 0 |  |
| C06 | 字幕 / Final Render | NOT_STARTED | 0/2 | 0 |  |
| C07 | 自动QA | NOT_STARTED | 0/2 | 0 |  |
| C08 | 最终报告 | NOT_STARTED | N/A | 0 |  |

## 状态枚举

- `NOT_STARTED`
- `IN_PROGRESS`
- `PASS_AUTO`
- `PASS_AFTER_HUMAN_UNLOCK`
- `PARTIAL`
- `BLOCKED`
- `FAIL`

## Scoring

- `2/2` = Codex 全自动完成
- `1/2` = 用户只做一次最小解锁 / 输入后，Codex 自动完成
- `0/2` = 需要人工执行主体工作或未完成

## Human Intervention Log

| # | Stage | Codex 为什么停 | 用户做了什么 | 预计分钟 | 完成后是否自动继续 |
|---|---|---|---|---:|---|

## User Decision Gate

只有 C08 完成后才做最终判断：

- `READY_FOR_MODE_B_FRESH_R1`
- `REPEAT_MODE_A_AFTER_FIXES`
- `BLOCKED_BY_ENVIRONMENT`
- `BLOCKED_BY_EXTERNAL_SERVICE`
