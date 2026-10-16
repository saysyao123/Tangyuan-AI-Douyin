# 质量门禁：证据优先，不允许凭流程文档自称交付游戏

## 可运行 demo（本轮）
- `node --test tests/*.test.mjs`：纯函数状态机、事件后果、战斗结算、读写快照、坏引用/死结局。
- `node tools/pipeline.mjs validate examples/lantern-inn/game.json`：数据/引用/地图/物体/结局检查。
- `node tools/pipeline.mjs build examples/lantern-inn/game.json dist/lantern-inn.html`：可离线浏览器页面，无远端 API。
- GitHub Actions 必须实际执行上述命令并产生 HTML artifact，不能仅写可执行方案。
- 浏览器实际观察测试：进入场景、方向移动、靠近 NPC 按 E、进入下一场景、与明雷战斗、返回完成剧情、存读档。没有做过的不标通过。

## 首本新书 Gate
- 内容端：有章节证据的剧情事实率、所有主线关卡可从起点到达终点、全部角色来源/授权链、事件不得在无目标场景触发、重要道具不得重复无限刷取。
- 引擎端：首场能移动/阻挡、NPC具有不同语言和触发效果、至少1场可见敌人触发的完整战斗、人物状态/背包变化、存取档一致、最后能够回到标题或结局。
- 资产端：统一角色外观与比例、场景配色、动画帧位移不漂浮、字体中文显示、图片原生分辨率不异常变化、音乐在剧情切换时不突兀。
- 回归端：上一本仍能运行、第二本只改内容包不改内核源代码。

## 报告结构
`qa_report.json` 至少标记：source_title/rights/status/sha/entry/scene/dialogue/battle/save/end、用例数、失败用例、证据链接、人工观察未测项。状态只允许 PASS / FAIL / BLOCKED / NOT_TESTED；存在一项核心 FAIL 就不是完整可玩交付。

## 尚未通过的主要事项
- 用户原版 Windows 仙剑的 REA/Ghidra实测未做。
- 用其资源完整游玩和 Type PAL 版本匹配未做。
- 原版所有43k脚本/全部伤害概率和每位人物属性表未完全抽取。
- V1 独立演示游戏仅是流程技术样本，不是“同等复杂度的仙剑引擎”。
