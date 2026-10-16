# Book → PAL98-style RPG｜可执行游戏生产线 V1

> 项目核心：完整学习《仙剑98》经典玩法，让 **其他书籍** 变成可运行的故事游戏；先不改变核心玩法、不复用仙剑受版权保护的原始资产。

## 当前入口

请先读 **[CURRENT_STATUS.md](CURRENT_STATUS.md)**。T1 完整短篇和 T1.1 已发布，T1.2 可靠性基底正在验收；T2 通用编译尚未通过。正式 Type PAL 构建、试玩地址和最新证据以该页为准。

下方保留早期研究与测试历史；其中旧的“未完成”与旧 HTML 构建命令不代表当前 T1 状态，也不是正式交付入口。

## 网页优先路线（2026-10-16 更新）

**正式游戏运行和可视化编辑目标统一迁向 [Type PAL Reforge + Editor](docs/WEB_FIRST_PLATFORM_V2.md)**。以浏览器创建/修改/试玩/保存原创书籍 RPG；此前原创轻量 HTML 只保留为内容编译测试夹具，不是新书游戏的正式引擎。

- [Type PAL 官方项目与代码审计](docs/TYPE_PAL_DEEP_REVIEW_20261016.md)
- [网页游戏制作平台 V2 完整架构](docs/WEB_FIRST_PLATFORM_V2.md)
- [真实接入门禁与未验证风险](docs/TYPE_PAL_GATE_AND_COMPAT.md)
- [官方 content22 适配制作提示](prompts/S4_TYPE_PAL_CANONICAL_ADAPTER.md)
- ✅ **Type PAL 官方实测 T0 已通过**：[GitHub Actions 38853212658](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38853212658) — 源码/类型检查、真正 Reforge+Editor 生产构建、Chromium 编辑器项目选择与 Reforge 作者场景加载渲染（Canvas 1280×800）均PASS。见 [完整测试证据](evidence/TYPE_PAL_P0_BROWSER_VERIFIED_20261016.md)。
- 下一阶段真实功能验收任务：[T1全原创可编辑网页RPG](https://github.com/saysyao123/Tangyuan-AI-Douyin/issues/25) 和 [T2书籍IR→content22编译器](https://github.com/saysyao123/Tangyuan-AI-Douyin/issues/26)。**保存/重开与独立静态部署仍未通过，不得误称成熟在线平台。**
- 云端官方引擎可复现探针：`.github/workflows/book_rpg_type_pal_probe.yml`。真正编辑/保存/原创游戏/发布必须逐关验收，不能误称已完成。

## T1 官方引擎原创工程实测进展（2026-10-16）

✅ [原始证据](evidence/T1_ORIGINAL_TYPEPAL_CONTENT22_ENGINE_EDITOR_20261016.md)：已经将两份原创小说式测试故事编译为 Type PAL 真正 content22 / SAVE12 标准工程（每份20文件，全部原创合成色盘/瓦片/人物占位资源），官方校验全部通过；在 Chromium 中真正通过 Reforge 渲染第一份原创场景，并通过官方 React Editor 加载第一份工程、显示NPC与脚本。GitHub Actions [run 38855229699](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38855229699) 实际成功。

⚠️ 当前未完成NPC端到端交互、编辑器修改保存与重开、多场景传送、任务物品、仙剑式战斗与结局、正式静态网页托管，因此不能宣布T1完成、也还不需要用户上传书籍。下阶段 [Issue #25](https://github.com/saysyao123/Tangyuan-AI-Douyin/issues/25) 仍保持打开。**[WORK_T1_CONTINUE.md](WORK_T1_CONTINUE.md)** 是 Work 模式的完整接力入口。

## 当前实际状态（2026-10-16）
- ✅ 已有 `../PAL98_BOOK_RPG_BASELINE_V0_1/` 机制/人物/源码锚点研究。
- ✅ V1 已具备固定阶段、输入输出清单、人工确认门禁、两部原创测试故事、纯 Node 测试、HTML 构建命令、GitHub Actions CI。
- ⏳ 用户上传的仙剑98文件尚未完成跨引擎实际游玩验证；全部战斗/脚本/数值真值尚未冻结。
- ✅ 2026-10-16 实证：GitHub Actions [run 38851723543](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38851723543)，Node 17/17 + Python 2/2 PASS，两份原创游戏内容包分别编译为 HTML，并完成真实 Chromium 剧情通关冒烟测试（存储采用模拟实现）。完整范围见 [evidence/V1_VERIFIED_EXECUTION_20261016.md](evidence/V1_VERIFIED_EXECUTION_20261016.md)。
- ✅ 可使用 `node tools/new_book_run.mjs slug "书名"` 一键建立 S0–S7 空白阶段文件夹和 STATUS.json（所有阶段从 NOT_STARTED 开始）。
- ⏳ 还没有上传第一本新书，尚未证明 AI 自动提取长篇小说及 Type PAL 内容包导入。
- ⚠️ V1 试玩是 **自有内容独立参考运行器**，仅测试「故事数据→互动浏览器游戏」管线，不冒充 Type PAL 或全部仙剑机制已完整实现。

## 最简入口
1. 下一次用户交书：读取 **[START_WEB.md](START_WEB.md)**，严格按照 S0 → S7 逐阶段执行。
2. 查看 [阶段合同](docs/STAGES.md)、[机制真值表](docs/MECHANICS_AND_GAPS.md)、[人物/编剧规范](docs/CHARACTER_AND_STORY.md)、[QA](docs/QA.md)。
3. 本次原创样本：`examples/lantern-inn/game.json`。执行：

```sh
node --test tests/*.test.mjs
node tools/pipeline.mjs validate examples/lantern-inn/game.json
node tools/pipeline.mjs build examples/lantern-inn/game.json dist/lantern-inn.html
node tools/pipeline.mjs build examples/river-ledger/game.json dist/river-ledger.html
```

网页浏览器直接打开生成的 `dist/lantern-inn.html`。方向键/WASD移动，E/空格互动；战斗使用按钮；浏览器保存/读档。

## 冻结策略
**机制稳定**：地图斜视角、可见敌人与接触战斗、碰撞与NPC脚本、三人队伍、经典回合指令、装备/成长/五灵/状态、任务/演出/背包/商店与读存档。新书内容只换角色、台词、地图、故事、技能皮肤和资源；机制差异需经规则门禁单独批准。

**安全与版权**：这个公开仓库中绝不保存上传的《仙剑》EXE/DLL/MKF/AVI/MIDI/人物/地图/剧本文本/存档及未授权书籍全文。仅保存参考代码链接、研究摘要、原创示例和具备授权的制作资产。引用引擎须遵循 GPLv3；不能因引擎开源就转售原版素材。

## 技术路线选择
- **SDLPAL**：解释和核对经典机制，源参考锚点 `f6236a0d0839b1cc8918e2abc54017e223938f1d`。
- **Type PAL Reforge**：首选未来可编辑独立 RPG 项目的引擎实验候选，`f98d0ddd89ebdee7b04502ee35de26ee82c6d246`，其 canonical schema 是 content22/SAVE12，**本项目 JSON 不是它的官方格式**。
- **REA 6.5.0+ / Ghidra**：仅当开源参考与实际仙剑98版本行为存在差异时，做授权范围内的补充分析；不要求每本书都运行逆向。
- **GPT Plus + Codex**：文本理解、结构化改编、数据产物生成、测试修复，优先网页/Actions、低配置 PC、零额外付费 API。
- **RPGJS v5**：仅作备选，不同时维护两套正式引擎。

## 新书的完成判据
第一部完成一个有开局、能探索、有人物差异、战斗和事件、存读档、可收束结局的**可玩章节**；
第二部 **仅替换数据包，不修改核心引擎源代码**，完成独立试玩与回归，才叫流水线闭环。

## 文档与代码
`START_WEB.md` 接力；`docs/` 研究/制作合同；`prompts/` 阶段产出提示；`examples/` 虚构原创样本；`src/rules.mjs` 可测试规则内核；`runtime/template.html` 演示界面；`tools/pipeline.mjs` 构建/验证；`tests/` 自动测试。机制研究主文件仍由前期研究分支保存，避免多源真值。

## 《仙剑98》用户原始资源研究补充
- 本轮只读检查上传的 RAR，发现 160 种脚本操作码取值（含 0xFFFF）、43557条8字节脚本、5077候选事件对象、13514消息索引。汇总见 [evidence/PAL98_UPLOAD_STATIC_AUDIT_20261016.md](evidence/PAL98_UPLOAD_STATIC_AUDIT_20261016.md)，工具为 [tools/pal98_audit.py](tools/pal98_audit.py)。原数据从未进入公开仓库。
