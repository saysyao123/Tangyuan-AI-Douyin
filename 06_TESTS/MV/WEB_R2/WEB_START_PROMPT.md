# WEB R2｜ZERO-CONTEXT START PROMPT v1.3｜ROUND CLOSED

> WEB R2 已于 2026-08-24 `COMPLETE_LOCKED`。
> 本文件保留用于 R2 回归/排错，不再作为新 MV 的默认启动入口。

## Future new MV

请使用：
`04_HARNESS/templates/mv_zero_context_start_prompt.md`

它会加载当前权威：
- `04_HARNESS/workflows/mv.md`
- `04_HARNESS/rules/mv_golden_runtime.md`
- `04_HARNESS/rules/mv_audio_timeline.md`
- current Round `CURRENT_STATE.md`
- stage-specific JIT rules，包括 Human Gates / Editing / Source Normalization / Subtitle / AI Video。

## R2 regression prompt

```text
你现在要对已关闭的 WEB R2 做回归/排错，不得把 R2 重新当成未完成生产 Round。

分支：test/mv-web-r2

读取：
1. 04_HARNESS/workflows/mv.md
2. 04_HARNESS/rules/mv_golden_runtime.md
3. 04_HARNESS/rules/mv_audio_timeline.md
4. 06_TESTS/MV/WEB_R2/CURRENT_STATE.md
5. 06_TESTS/MV/WEB_R2/W11_CLOSE_RECEIPT.json
6. 仅在定位具体回归问题时读取对应 R2 evidence/receipt。

R2 当前状态必须保持 COMPLETE_LOCKED，除非用户明确要求重新打开该 Round。
正常新 MV 不读取整套 R2 历史，而使用当前 Runtime Rules。
```
