# Book → PAL98-style RPG｜可执行游戏生产线 V1

> 项目核心：完整学习《仙剑98》经典玩法，让 **其他书籍** 变成可运行的故事游戏；先不改变核心玩法、不复用仙剑受版权保护的原始资产。

## 当前实际状态（2026-10-16）
- ✅ 已有 `../PAL98_BOOK_RPG_BASELINE_V0_1/` 机制/人物/源码锚点研究。
- ✅ V1 已具备固定阶段、输入输出清单、人工确认门禁、原创示例游戏、纯 Node 测试、HTML 构建命令、GitHub Actions CI。
- ⏳ 用户上传的仙剑98文件尚未完成跨引擎实际游玩验证；全部战斗/脚本/数值真值尚未冻结。
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
