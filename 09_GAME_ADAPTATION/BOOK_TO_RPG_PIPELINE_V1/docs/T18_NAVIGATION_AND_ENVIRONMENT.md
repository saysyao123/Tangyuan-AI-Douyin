# T18 · 场景与寻路对照（2026-10-17）

目标：在当前Type PAL基底上改善可玩性，不更换引擎、不复制仙剑商业素材。小说剧情保留。

| 一手参考 | 借鉴内容 | 在本工程的落点 |
|---|---|---|
| [Type PAL pinned source](https://github.com/IllegalCreed/type-pal/tree/f98d0ddd89ebdee7b04502ee35de26ee82c6d246) | 菱形坐标、脚底锚点、分层遮挡、native dynamic player intent、terrain/body sweep | 寻路提供目标与方向，正常行走由原生planner提交；不拿剧情moveParty bypass代替玩家移动 |
| [SDLPAL](https://github.com/sdlpal/sdlpal) | 用场景分区、物件与建筑组织空间的经典PAL参考；资源与地图语义对照 | 室内家具沿边组合，保留主要行走区；外景用树木、柴堆、灯作为道路边缘与地标。没有抽取或分发PAL美术 |
| [Grid Engine moveTo](https://annoraaq.github.io/grid-engine/examples/move-to/index.html) | 目标移动与最短路径；键盘移动保留 | 本轮bounded BFS、不可达反馈、动态阻挡后重规划/有限停步；方向键立即接管 |
| [RPGJS Move commands](https://docs.rpgjs.dev/commands/move) | 明确移动命令与事件交互的分离 | 点击目标先靠近原生交互半径，再核当前scene/session/visibility/manual gates后启动现有脚本 |

## 具体结果

- 点击地面自动绕路；点击可见精灵像素或脚边金色标记，走到能交互的格子后启动原有对话/门事件。
- 路线用原生terrain sweep与连续body sweep，不以端点sameGrid代替人物体积。分数起点通过正常partial axis步对齐。
- 每段由原生player dynamic intent提交；键盘、菜单、剧情、失焦与换场取消点路。不可达或持续被挡有反馈，不无限busy。
- 本项目第二幕室内新增家具内部的旧档落点，读档时在4格内找可站且有可行邻步的位置；不改剧情、库存、钱或原始存档。普通可走落点原样保留。
- 六类新原创素材组成17处装饰：橱柜、月光窗、冬衣架、雪树、柴堆、石灯。author overlay二次执行109文件零diff。9张场景所有既有实体与剧情脚本逐项一致。

## 明确限制

用户的具体卡住存档未提供，当前静态未复现洗漱runner死锁；其脚本走位是authored bypass，不能归因地图阻挡。已证实并处理的是“点击不走”和合法旧布局位置落入新家具占地的风险。帧率采样来自CI桌面浏览器，不代表所有移动设备。尚无跨地图自动寻路，场景转换仍由原有门事件负责。

## 美术可重复构建

权威输入：art/t18/{cupboard,moon-window,coat-rack,winter-tree,snow-wood,stone-lantern}.png；prepare_art.py只编译这些indexed PNG。import_atlas.py仅机械提取原始生成图，不参与常规构建。原始atlas在私人对应源包保留；GitHub发布六张规范化素材与生成说明。built-in image_gen模式，无第三方游戏图作输入。

截图复核后的布局：街道入场可见左侧雪树、前景柴堆与石灯；庭院用两侧雪树、前景石灯/柴堆形成取景。木地板只调低对比与板缝，不改地图可走语义。环境验收独立于已通过的导航剧情流程。
