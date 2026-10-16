# 内容合同 V1：引擎无关，禁止假装已经接入 Type PAL

目标是稳定的原创“故事内容包”，内有 id/source、playable角色、二维场景地图、NPC/怪物/物品、events、战斗定义与结局。由工具检查引用；当前示例 `examples/lantern-inn/game.json`。

## 与上游关系
- 上游 Type PAL Reforge **current** 接口是 content22 / SAVE12；本项目的 `book-rpg-game-v1` 不是其官方 manifest 结构。
- 本轮提供原型运行器证明用户内容→可玩简单网页；**正式适配必须新增 exporter，读取官方 content22 schema 并通过 Type PAL实际程序验收**。
- 不能直接把这个JSON扔进Type PAL宣称制作完成。
- 内容包至少包含 kind/id/title/rights、flags、player、scenes、characters、encounters、events、ending；实际字段以样本和 `tools/pipeline.mjs` 的完整校验为准。
- 游戏运行器源代码和数据文件分离；第二本书只替换JSON，测试时对比引擎源提交哈希不变。

## 交互说明（V1示例运行器）
`world.startScene`, `world.startPos`；`world.scenes[]` 包括 `terrain` 等宽字符串、`exits` 和 `entities`；
实体类别 npc/item/enemy；事件 `conditions`、`onSuccess`、`onFail`、`effects`；
`encounters` 中包含敌HP与伤害；
`player` 包括可玩角色、HP/MP、攻击/防御；
`ending` 含结局ID/文案。
此结构**有意仅覆盖最小闭环**；不声称装备、五灵、三人战斗已经在V1运行器实现。

## 适配路径
`story facts` → `beat graph` → `game.json` → `validate` → `build` → `HTML playable`。
适配Type PAL时另做 `adapter/type-pal`，输入仍是内容事实，输出 content22，包括稳定AssetId、地图/场景/角色/事件脚本/入口和项目素材；只有官方引擎读入并通过试玩才可替换 demo 作为正式运行路径。
