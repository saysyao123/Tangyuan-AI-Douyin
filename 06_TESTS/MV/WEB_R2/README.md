# WEB R2｜网页端 MV 自动化能力测试

## 目的

本轮不是单纯再做一条 MV，而是测试网页端 ChatGPT 在没有 Codex 的情况下，能把 R1 Golden Sample 流程自动推进到什么程度。

核心问题：

> 哪些 Stage 可以完全自动？哪些只需要用户做审美确认？哪些必须依赖外部平台人工操作？

## 与其他测试隔离

- 人工 Golden R1：`06_TESTS/MV/ROUND_01/`
- Codex 工程复刻：`06_TESTS/MV/CODEX_R1/`
- 本轮网页端自动化：`06_TESTS/MV/WEB_R2/`
- 分支：`test/mv-web-r2`

禁止覆盖人工 R1。

## 三类执行状态

- `AUTO`：网页端可以自行完成，不要求用户操作。
- `HUMAN_GATE`：网页端完成生产，只需要用户做一次选择/审美确认。
- `EXTERNAL_REQUIRED`：需要用户在外部平台执行，例如 Seedance 图生视频。

额外记录：
- `BLOCKED`：当前网页端工具无法完成。
- `PARTIAL`：部分自动，但仍有非审美型人工工作。

## 本轮目标

完整测试：

`选歌 -> BGM截取 -> 音乐/歌词结构 -> 导演 -> 首帧 -> 动态提示词 -> 外部视频生成 -> 动态QA -> 剪辑 -> 字幕对齐 -> Final -> 复盘`

最终必须输出一张真实 Automation Matrix，不能因为最终有视频就把整个流程写成自动化。

## 启动

新网页对话直接使用：
`06_TESTS/MV/WEB_R2/WEB_START_PROMPT.md`

任何新对话先读：
`06_TESTS/MV/WEB_R2/CURRENT_STATE.md`
