# T20 第一幕美术重制｜执行进度（目标模式契约）

日期：2026-10-17。**此文是执行报告，不代表已完成第一幕。** 范围仅第一幕四图，不新增剧情/人物/地图，Type PAL + T18正式站点保持稳定。

## 当前门控状态

| Gate | 状态 | 证据和未完成项 |
|---|---|---|
| G0 实际源码/相机基线 | **PASS** | GitHub Actions [Run39019761748](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39019761748)：固定Type PAL T18构建、原T15 street SAVE12读档、真实320×200原生`street`截图、runtime参数/位置抓取与0 pageerror |
| G1 `street` 完整高细节母版 | **NOT_PASSED** | 本轮多次生成的繁华城镇图出现`余杭镇`等新UI、酒馆、摊位/桥/新人物，虽审美较细但**完全偏离现有归家街道**；全部拒绝，不能作为母版 |
| G2 `street` 可玩分层接入 | NOT_STARTED | 地面/建筑/遮挡/照明的索引资源/RLE和运行对照尚未做 |
| G3 其他三图 | NOT_STARTED | `fair/backstage/courtyard` 尚未制作新母版/接入 |
| G4 NPC/角色与演出 | NOT_STARTED | 延用旧角色，不把T19步态未通过草稿视为完成 |
| G5 第一幕完整试玩与发布 | NOT_STARTED | 目前正式站点仍为T18；公开和私有流程需分别验证 |

## 真实第一幕场景和相机证据

- 引擎/存档：T18公共fixture、`tests/fixtures/t15-street.native-save.json`（SAVE12，`sceneId='street'`），项目`book-pilot-cinematic`，正式Site未修改。
- 运行镜头：`320×200`原生、导出`1280×800`最近邻，`sceneId='street'`，相机`x=480,y=112`，玩家`col=34,row=-6`，观察到11个actor/entities，pageerror=0。
- 与玩家互动有关的当前镜头脚点：陌生人 `(32,112)`，孩子 `(144,104)`，去小院出口 `(288,112)`（原生屏幕px）；庙会返回点 `(-144,104)`在当前镜头外，不允许擅自移动到镜头里。
- GitHub Actions artifacts：名`t20-first-act-street-baseline`，包含`01-street-native-screen.png`、`02-street-browser-camera.png`、`REPORT.json`；Run39019761748的artifact为`12096217570`（原始CI将按GitHub设置在30天后过期）。
- 本轮对话另制作`T20_ACT1_START_PACK_20261017.zip`，含实际截图、进度JSON、真正已获批准的旧屋参考图副本、旧街空间锚点图和同镜头目标差距看板；该ZIP是**对话附件**，未上传成GitHub二进制资产。
- **第一幕正确游戏剧情顺序仍为`fair→backstage→street→courtyard`**。`street` 先制是为室外工艺样板，绝不改开场入口或story flags。

## 真实失败与复盘（不得以静态图忽略）

- Run39019299747：截图脚本在开场对白尚未关闭时发送F9，被原生对话模态阻断，超时且截图仍停留在`fair`；修复为先结束公开合成开场对白，不改正式游戏。
- Run39019599793：已成功恢复`street`，但测试错误地期待主角runtime ID 必须为 `party:hero`；旧引擎没有该映射。修为检查`sceneId`、`position`及既有陌生人/小院出口；Run39019761748通过。不要再次重跑这两处已定位错误。
- AI概念图尝试继续错误添加`余杭镇`、酒馆、桥梁、小摊、UI/无关路人等；**判为REJECTED**。错误不是图不够美，而是与`street`真实空间和事件不一致。不得把这类新图做缩小/拆素材以求进度。下一次画面生成只可参照真实`street`镜头与已锁定文档执行，更要以现有人物位置及通道为准。

## 下一轮唯一任务（G1）

对真实320×200`street`旧街**一屏**做高完成度的原创母版，围绕三处民居墙面/屋檐/转角（仅当前镜头可见的一到两处）、一致的石路边界、左侧陌生人、双主角、右侧旧路灯和原有出口，保留相机、可行走道路和遮挡。必须提供母版＋对应同机位标记图，人工审美确认后才能启动G2拆图；不推到fair/backstage/courtyard，更不能宣称第一幕制作完成。

**首图不是正式游戏素材**，只有通过G2原生RLE、遮挡/碰撞/点击/静态/动态验收才算真正可玩。已确认的T18正式网页与私有书籍内容继续不动。
