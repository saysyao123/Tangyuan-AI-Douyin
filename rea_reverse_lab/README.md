# REA / 2048: reproducible open-source game pilot

## 目标
用 REA 6.4.0 在 GitHub Actions Ubuntu + Node 24 环境对真实 MIT 许可游戏 gabrielecirulli/2048 进行静态分析；再对游戏移动/合并/计分/随机方块/输赢规则实施 **1,240 组** 可复现、独立实现 vs 原版程序的差分测试。无需额外付费 AI 订阅、无需本地 Ghidra。

## 样本与许可
官方仓库 https://github.com/gabrielecirulli/2048
锁定原始提交 478b6ec346e3787f589e4af751378d06ded4cbbc
License MIT，样本只用于合法的开源研究，CI 保留许可证副本。

## 边界
首轮只验证一个子系统，并不生成完整游戏；原始游戏公开源码，属于可审计的 **白盒对照**，不能冒充未知游戏的黑盒逆向。此轮 REA 是否可有效分析浏览器源代码，必须以真实运行结果证明。

## 运行与结果
workflow: .github/workflows/rea_2048_pilot.yml
限定实验分支 experiment/rea-2048-pilot-20261014，手动 workflow_dispatch 也可。
CI 分步运行真正的 REA CLI 和独立测试，并将完整 Evidence/错误日志/进程退出码/STATUS.md 保存为 Actions artifact 14 天，不要求写入任何 secrets。

## 三项验收
1. REA 真实退出码 0。
2. Evidence JSON 可解析，明确包含 game_manager.js。
3. 独立实现与锁定原版对照测试 1240/1240 一致。
全部通过才是 P0 PASS。任何一步失败均标记 NOT PASSED。

## 本地复现
1. node --version，使用符合 REA 要求的 Node 24（REA 6.4.0 至少 Node 22.19）。
2. git clone https://github.com/gabrielecirulli/2048.git rea_reverse_lab/upstream
3. git -C rea_reverse_lab/upstream checkout 478b6ec346e3787f589e4af751378d06ded4cbbc
4. UPSTREAM_2048=rea_reverse_lab/upstream node --test rea_reverse_lab/04_diff_tests/parity.test.mjs
5. npx --yes rea-agents@6.4.0 analyze-javascript-application ./rea_reverse_lab/upstream --json > rea-evidence.json
