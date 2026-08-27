# OSS MV Optimization Integration Test｜New Chat Start Prompt v1.0

```text
请使用已连接的 GitHub，读取 `saysyao123/Tangyuan-AI-Douyin` 仓库 `test/mv-oss-optimization-r1` 分支。

这是「汤圆音乐映像」Canonical MV Runtime 的独立开源优化实验线，不是正式生产线。

先读取：
1. `06_TESTS/MV/OSS_OPT_R1/EXPERIMENT_CONTRACT.md`
2. `06_TESTS/MV/OSS_OPT_R1/SOURCE_INTAKE.md`
3. `06_TESTS/MV/OSS_OPT_R1/RESULT_MATRIX.md`
4. `05_IP_ASSETS/MV_30D_60_NEW_CHAT_START_PROMPT.md`
5. 当前 Canonical Runtime / Web Bridge 最小启动文件。

实验基线固定来自正式 Runtime fork SHA：
`89852ec5314e7579853683ef5eb40adb09f25753`

锁定规则：
- 不修改 `test/mv-web-r3`；
- 不为了适配外部项目放松 Runtime correctness；
- 不整体照搬外部仓库，先做 source-level 分析和最小优化映射；
- 外部优化先分类为 Runtime replacement / Stage overlay / Knowledge candidate / Tooling adapter / Out of scope；
- 先填写 SOURCE_INTAKE，再进入代码、规则或流程修改；
- 任何实验结论必须进入 RESULT_MATRIX；
- 单次视觉更漂亮不等于可晋升，必须同时检查稳定性、复现性、成本和维护复杂度；
- 只有完成整轮对比后，才可以提出 PROMOTE_RUNTIME / RULE / KNOWLEDGE / TOOLING；正式生产分支的晋升另开明确变更，不在实验中静默合并。

如果用户已经提供开源仓库 URL / 项目文件 / 优化说明：
- 直接读取并深度分析；
- 锁定具体 source commit / 文件；
- 建立与当前 MV Runtime Stage 的逐项映射；
- 找出冲突、重复、真正增益和最低成本的集成点；
- 输出推荐的最小测试集；
- 然后开始本轮实验，不要求用户重新解释正式 Runtime。

如果用户还没有提供 source：
- 当前状态保持 WAITING_FOR_SOURCE_PROJECT；
- 不自行搜索一个替代项目填进去。
```
