# REA 游戏逆向复刻 P0 — 实际验收（2026-10-14）

## 任务契约
**目标**：在不增加大模型订阅、不依赖低配电脑运行逆向引擎的前提下，验证 GPT + REA + GitHub Actions 可否分析真实游戏并独立重建一个可验证的核心玩法子系统。

**样本**：MIT 原版游戏 [gabrielecirulli/2048](https://github.com/gabrielecirulli/2048) 固定 478b6ec346e3787f589e4af751378d06ded4cbbc；当前为开源白盒实验，不是破解商业游戏。

## 实验结果
实际 Actions 完成：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38537563976

| Gate | 实测证据 | 状态 |
|---|---|---|
| REA 6.4.0 实际运行 | CLI exit 0；Evidence 3,671,866 bytes | PASS |
| 源码证据覆盖 | 10 JS 文件、3,881 AST、10 源模块节点、game_manager 21 个函数节点 | PASS |
| 图语义 | 23 程序图节点、33 边；2,238 语义节点、1,444 关系，908 个保留未知 | 已记录局限 |
| 行为重建 | 310 棋盘状态 × 4 方向 = **1,240/1,240** 对照一致 | PASS |
| 单文件试玩版 | Action Artifact 中 PLAY_2048_OFFLINE.html；已完成浏览器脚本冒烟测试 | PASS（有限范围） |

**P0 结果：PASS（范围限于本试点）**。

REA 的静态模块统计字段 `statistics.modules=0` 是 CommonJS/ESM 计数；本游戏是浏览器全局脚本，真实 `javascript-module` 图节点为 10，故不能误判为零输出。语义分析报告仍有 908 个未知项，不能将静态结构等同于运行时全部已知。

## 严格限制
- 本次复刻规则在开发时参考过公开的原版代码，同时真实运行 REA 导出了结构化分析 Evidence，**并非仅靠 REA Evidence 完成盲逆向**。
- 云端工作流直接运行 Node/REA/测试代码，本轮**没有实际调用 Codex CLI 或 Codex Agent**。这证明低成本云端分析和对照验证链条可行，不代表 Codex MCP 已在用户电脑配置成功。
- 验证的是 2048 核心移动、合并、计分、随机生成、输赢，不是完整游戏所有 UI/持久化/音效。
- 未验证 Windows PE 原生程序、Ghidra、DRM、联网游戏或任何未经授权目标。

## 交付位置
- `03_reconstruction/engine.mjs`：独立功能重建
- `04_diff_tests/parity.test.mjs`：锁定原始游戏行为 oracle，自动差分验证
- `02_evidence/summarize.mjs`：REA Evidence 强校验
- `demo/index.html` + `demo/build_offline.mjs`：生成可玩单文件
- `.github/workflows/rea_2048_pilot.yml`：实际云端执行，Actions Artifact 保存源证据、日志和单文件 HTML
- 下载完整结果：在 Actions run 38537563976 的 Artifact 中选择 `rea-2048-pilot-evidence`。

## 下一阶段
P1 必须重新定义为“不给复刻 Agent 原始源码，仅提供 REA Evidence 与测试接口，让它独立实现，再进行封闭差分评分”。如后续逆向 Windows 原生游戏，另做 Ghidra/Windows 执行权限和资源门禁，不继承 P0 通过状态。
