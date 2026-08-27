# CODEX R2｜Zero-Context Start Prompt

把下面这段直接交给 Codex。长期规则已经放在分支的 `AGENTS.md`，不要再复制整套 SOP 到提示词里。

```text
你现在要执行 Tangyuan Music MV 的 Codex R2 独立复用测试。

目标仓库分支必须是：
`test/mv-codex-r2`

目标真实测试 slot：
`D03-B / Lane S`

这是全新独立 MV，不要继承 D02-B《有几次想你了》的具体人物、海边建筑、浅色石材、白衣、纱帘、雨后世界、道具、构图或“握住→松手→世界打开”的视觉进程；只能复用已经进入 Rule / Workflow / Knowledge / Runtime 的通用能力。

请遵守仓库自动加载的 AGENTS.md，并先只读取：
1. `06_TESTS/MV/CODEX_R2/CODEX_EXECUTION_CONTRACT.md`
2. `06_TESTS/MV/CODEX_R2/CODEX_TEST_MATRIX.md`

不要扫描整个仓库，不要读取旧 `CODEX_R1` 当作当前流程，不要让我重新解释 R1/R2/R3/Lean R1。

然后从仓库根目录直接执行：

`python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py preflight`

再执行：

`python 06_TESTS/MV/CODEX_R2/scripts/codex_mv_operator.py resume --slot D03-B`

如果 fresh Runtime truth 返回 `ALLOCATE_NEW_SLOT / D03-B / Lane S`，立即用本地 Operator 合法 INIT；如果已经是 Canonical，则不要重复 INIT。任何冲突都以 fresh Canonical Runtime 为准，禁止凭这段提示词覆盖仓库真值。

完成初始化/恢复后，立即执行当前 resolved executor 的 HG01 machine preflight，按 JIT 原则只读取它要求的文件。给我少量最值得选择的歌曲候选和必要证据/实际参考链接，让我只做 HG01 歌曲审美决定。

从此以后：
- 使用 Codex 本地 Operator，不走 ChatGPT Web 的 request -> Actions -> response transport；
- 仍然只认同一套 Canonical S00-S18 Runtime；
- 五个 Human Gate 一个不能少；
- Gate 之间尽可能自动连续执行；
- 缺外部生图/Seedance/登录能力时按 `CODEX_HANDOFF_PROTOCOL.md` 输出最小可恢复 handoff；
- 不新建第二套状态机；
- 不手改 CURRENT_STATE / receipts；
- 不为 D03-B 写 core 专用 helper；
- 不为保险建立第二歌词时间轴；
- 不每首歌重新安装生产模型；
- 不提交大视频/音频/密钥/登录状态；
- 修改文件后运行对应测试，做有意义的 Git commit，并保持结果可审计。

本轮目标是让这首全新 MV 尽可能完整跑到：
`S16_RELEASE_PACKAGE_READY`

未真实发布前禁止进入 S17 / PUBLISHED。

现在直接开始，不要先向我提问。第一次回复只需要简洁汇报：
- branch / HEAD；
- preflight 结果；
- Runtime mode；
- slot / lane；
- current stage；
- resolved executor；
- next action；
- 当前 Human Gate 或唯一真实 blocker；
然后立即给出 HG01 的实际候选（若环境允许）。
```
