# 当前状态与唯一续作入口

> **最新 T36 2026-10-18**：用户已授权既有第二幕按同标准优化。本轮雪街/便利店/意识空间/雪院与专属人物动作已上线，13项受影响检查及雪院精修4项通过，已认可家中和第一幕保持。先读 [T36_PROGRESS](docs/T36_PROGRESS.md) 与 [RELEASE](evidence/T36_20261018/RELEASE.json)。第二幕最终用户复验待反馈，整体完成仍为 FALSE；以下旧状态保留作历史。


> **最新 T35 2026-10-18**：第一幕效果获正面反馈；开场/切场景旧画面闪回已修复并发布，素材 decode 后再提交场景，加载提示与重试已补测。已认可室内、203张美术和109个原生工程文件保留。先读 [T35_PROGRESS](docs/T35_PROGRESS.md) 与 [RELEASE](evidence/T35_20261018/RELEASE.json)，以下 T22 及更早说明为历史，不能覆盖最新状态。整体项目仍待用户最终验收。

> **T22 2026-10-17 回退修复（最新）**：用户反馈T21新网页比原来差且美术没有可感知提升；核对确定T21更换了完整T18网页Shell为简化iframe测试页，只换11处且部分劣于原版的简化建筑，道路地板/人物动画/光照基本未动；此外公开CDN站点的SAVE12浏览器存储与原ChatGPT Site不同域。已在独立`t22-restored-preview`上恢复T18完整页面的HTML/CSS/JS/config，默认原T18美术与原剧情，T21低质素材移入`/art-review/`隔离对照；原生`fair`渲染帧与旧页面UI真实浏览器测试、固定SHA外网资源检查已通过。详见 [T22回归审计与当前可测链接](docs/T22_T21_REGRESSION_AUDIT.md)。T18正式Site/main未覆盖，高精细重制目标仍未完成。

> **最新T21目标：第一幕四场景按获准高细节美术重制，并交付真实线上可玩的网页；不能以概念图/单件格式通过替代美术验收。** 当前已构建并独立发布真实Type PAL公网试玩技术版，外部CDN与四场景页面CI、受影响剧情SAVE12路线CI通过，但高精细美术标准仍明显未达到，下一轮先做高分辨率分层场景视觉与原逻辑整合，不扩新剧情。见 [T21唯一目标、网页测试版及QA边界](docs/T21_FIRST_ACT_PLAYABLE_GOAL.md)。正式 T18 和 main 均未修改。


> **T20 第一幕整体美术重制正在独立分支执行（2026-10-17）**：用户把目标从 T19 旧屋局部精修升级为**第一幕四场景统一高精细像素重制且最终可玩**；目前先做 `street` 室外工艺样板，不改变真实剧情入口 `fair`。T20 G0 真实街景+SAVE12+相机截图已在 [CI Run39019761748](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/39019761748) 通过；G1 高品质街道母版尚未通过（连续概念生成误加酒馆、桥、额外NPC与UI，拒绝入库）；G2–G5尚未开始。续作必须先读 [T20目标/美术圣经](docs/T20_ACT1_GOAL_AND_ART_BIBLE.md)、[旧街锚点](docs/T20_STREET_CAMERA_BRIEF.md)、[最新进度](docs/T20_PROGRESS.md)，不要回头盲目批量生图。正式T18 Site、SAVE12和剧情均未修改，本标注仅属于T20开发分支。


更新时间：2026-10-17。历史报告按原验收范围保留，不能用本页把旧证据升级为新的通过。

- T1 完整原创短篇：已发布，真实任务、双场景、战斗、跨页存档与编辑保存重开已通过。
- T1.1：失焦输入、显示插值和轻量缓冲已发布；短时回调测试不等于引擎长期稳定证明。
- T1.2：可靠性基底已验收并发布。成功 CI 38891702378：7项新定向单测、16项浏览器可靠性检查、10项受影响故事回归、4项编辑保存重开回归通过；155个完整运行文件与CI逐项一致。下载源码干净目录重建同样155文件一致；正式部署归档已全量核对。最新发布与边界：[RELEASE.json](evidence/T12_FOUNDATION_20261016/RELEASE.json)，复盘：[FAILURE_NOTES.md](evidence/T12_FOUNDATION_20261016/FAILURE_NOTES.md)。
- T1.3：人物四向/三帧重绘、独立双人开篇模板与私有书籍小阶段。新完整流程 Run38894355314（11项）通过；最终画面/旧屋顶反例 Run38895732925 通过；实际私有工程已官方校验与机制比对，私有对白排版等待用户试玩。新发布见 [T13 RELEASE](evidence/T13_OPENING_20261016/RELEASE.json)，失败经验见 [T13复盘](evidence/T13_OPENING_20261016/FAILURES_AND_LIMITS.md)。
- T1.4：GPT原创冬景与人物、四斜向原生步态、真实队伍同伴/NPC显示平滑、头像与可读对白框、四场景归家开篇。新增范围分段通过，最终成功 Run38931605753；283个运行文件与CI路径一致，257个逐字节一致，26个仅私有文字呈现差异；私有工程54文件机制/二进制一致。发布及完整边界见 [T14 RELEASE](evidence/T14_POLISH_20261017/RELEASE.json)，原始对照见 [美术比较](docs/PAL98_ART_COMPARISON_20261017.md)。用户美术/私有对白观感验收待反馈。
- T1.5：按原书开篇两章重读后重做地图尺度与景观，新增原生剧情演出；九项完整新章检查Run38940074923通过，镜头/倒地修正Run38940771024通过，锅旁站位与轮廓最终Run38942172446通过。433运行路径一致，381文件逐字节相同，52个私有呈现差异；新工程65文件机制/资产一致、63cue绑定。保留真实失败与画面复核发现，见 [T15 RELEASE](evidence/T15_CINEMATIC_20261017/RELEASE.json) 与 [失败复盘](evidence/T15_CINEMATIC_20261017/FAILURES_AND_LIMITS.md)。本轮只精修开篇，读者观感等待试玩反馈。
- T1.6：第二幕雪夜觉醒（第3—5章小阶段）已发布。5张新图、51条私有cue；新增原生剧情12项Run38977914977、受影响画面Run38978451341、/night旧档任务栏反例Run38978669964分段通过。未重跑旧套件。509运行文件与最终CI路径一致，449字节一致，60仅私有呈现；原生工程101文件机制/资产一致。见 [T16发布](evidence/T16_NIGHT_20261017/RELEASE.json) 与 [失败复盘](evidence/T16_NIGHT_20261017/FAILURES_AND_LIMITS.md)。
- T1.7：已修复旧档覆盖房屋摆位、室内床/电视出画、第二幕地面接缝与网页画面下移/缩小。第一幕家门结尾同一次交互直接进入第二幕；统一入口/chapter/，可从第一幕查看调整后连续试玩。7项受影响原生流程Run38996982442通过，最终4项窗口尺寸检查Run38997390686通过；Run38997195261虽边界全绿但人工发现300px缩图，已记录并修正。见 [T17发布](evidence/T17_DISPLAY_20261017/RELEASE.json) 与 [复盘](evidence/T17_DISPLAY_20261017/FAILURES_AND_LIMITS.md)。
- T1.8：原生点击地面绕障、点击精灵可见像素/脚边标记靠近交互，方向键与失焦取消导航；第二幕室内新增家具区域的真实旧档位置可就近恢复，保留剧情/库存/钱。6项定向导航/室内流程Run39004754229通过；截图复核后6类原创素材17处布景、柔和地板与真实入场视野调整，3项环境/局部通行Run39005192149通过。未重跑旧抽奖/道具/战斗/第一幕完整套件。见 [T18发布](evidence/T18_NAVIGATION_20261017/RELEASE.json)、[对照与实现](docs/T18_NAVIGATION_AND_ENVIRONMENT.md) 与 [复盘](evidence/T18_NAVIGATION_20261017/FAILURES_AND_LIMITS.md)。
- T19美术精修（2026-10-17最新阶段门）：P0代表性问题定位已完成；P1 V2原创仙剑式像素审美**已获用户认可**。现进入 P2，但仅完成两主角的候选4方向×3姿势静态资产及**原生RLE编码精确等价验证**（工作包02：42/42静态结构检查通过、双RLE与固定上游TS编码裸字节逐字节一致）；动作承重/摆臂**未通过**，尝试的旧屋自动拼装**已拒绝**，真实home-room原生可玩版本**未实现、未发布**。参见[进度记录](docs/T19_PROGRESS.md)、[P2工作包02与失败边界](docs/T19_P2_WORKBENCH_02.md)、[下一步工作路径](docs/T19_NEXT_IMPLEMENTATION_STEPS.md)。正式站点仍是T18。两幕连续剧情、projectId、SAVE12、寻路和键盘不变，暂停后续剧情。
- T2 通用 IR→content22：尚未实现/验收。旧 pipeline.mjs 与轻量 HTML 只为参考测试夹具。
- 已收到用户书籍，先做开篇短阶段内部测试；不得再次索书。原书与私有角色剧情不进入公开GitHub。EXE后置。

第二幕直接新开局：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/night/

两幕连续试玩（第一幕开始）：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/chapter/

上一版对照与旧进度：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/pilot/

原原创试玩保留：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site

## 当前开篇构建

`node tools/t18/build.mjs <upstream> <output>`；私有内容用T16_CONFIG、T15_CONFIG、T14_CONFIG分别指定三份配置。公开CI用合成对白，原书与私有对白不入公开仓库。下载源码包含实际配置与T18原生点击寻路、旧档卡位恢复与环境重建说明。从/chapter/第一幕开始，家门结尾对白后自动进入第二幕，页面和存档项目不变；真实旧完成档F9读取后仍可在家门继续。/night/仅为可选第二幕新开局，不自动覆盖快速档；F5仍会主动覆盖同项目快速档。

## 唯一正式构建路线

固定上游 IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246，Node22.19+、pnpm10.17.1、Python3/Pillow；在已安装依赖的上游 checkout 执行：

```sh
node tools/type_pal_t1_build.mjs /absolute/type-pal /absolute/output
python3 tools/release_inventory.py check /absolute/output
```

命令从本目录执行。产物用 HTTP/HTTPS 静态服务访问；不能把 file:// 双击当作运行保证。

开篇短阶段构建（默认使用公开原创模板，实际书籍配置仅在私有Site）：

```sh
T13_CONFIG=/private/config.json node tools/t13/build.mjs /absolute/type-pal /absolute/output
```

该模板只覆盖本次小阶段，不代表通用T2。独立projectId；两个游戏的进度分别保存。

当前美术续作先读本页→docs/T19_ART_POLISH_PLAN.md→docs/T19_PROGRESS.md（若存在）→docs/WEB_START_T19_ART_POLISH.md；原T18发布与失败经验按方案按需复用。P0/旧首场景冒烟不重跑。引擎/恢复改动才回归受影响的原完整故事，作者入口改动才回归编辑保存重开。

## 后续优先级

按用户2026-10-17最新要求，暂停后续剧情，先把当前两幕的场景、NPC、贴图、动画与整体审美打磨统一。首轮只做P0基线检查＋P1旧屋风格样板，不默认批量生图、重建九图或覆盖正式网页；样板审美通过后再进入可玩精修。用户已反馈完成现有阶段，不把旧卡点回查当作本轮默认主任务。保留已认可剧情与T18操作/存档成果；不重跑无关旧测试。完整计划与阶段门见T19方案，下一轮执行再创建T19_PROGRESS，不能预填通过。

像素风、网页优先和低配置友好继续保留；不宣称全书完成。长期内存泄漏、Safari/Firefox及真实手机仍未由现有证据证明解决。
