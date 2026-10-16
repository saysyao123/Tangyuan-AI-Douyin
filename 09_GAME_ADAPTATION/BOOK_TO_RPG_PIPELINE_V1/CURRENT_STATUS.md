# 当前状态与唯一续作入口

更新时间：2026-10-17。历史报告按原验收范围保留，不能用本页把旧证据升级为新的通过。

- T1 完整原创短篇：已发布，真实任务、双场景、战斗、跨页存档与编辑保存重开已通过。
- T1.1：失焦输入、显示插值和轻量缓冲已发布；短时回调测试不等于引擎长期稳定证明。
- T1.2：可靠性基底已验收并发布。成功 CI 38891702378：7项新定向单测、16项浏览器可靠性检查、10项受影响故事回归、4项编辑保存重开回归通过；155个完整运行文件与CI逐项一致。下载源码干净目录重建同样155文件一致；正式部署归档已全量核对。最新发布与边界：[RELEASE.json](evidence/T12_FOUNDATION_20261016/RELEASE.json)，复盘：[FAILURE_NOTES.md](evidence/T12_FOUNDATION_20261016/FAILURE_NOTES.md)。
- T1.3：人物四向/三帧重绘、独立双人开篇模板与私有书籍小阶段。新完整流程 Run38894355314（11项）通过；最终画面/旧屋顶反例 Run38895732925 通过；实际私有工程已官方校验与机制比对，私有对白排版等待用户试玩。新发布见 [T13 RELEASE](evidence/T13_OPENING_20261016/RELEASE.json)，失败经验见 [T13复盘](evidence/T13_OPENING_20261016/FAILURES_AND_LIMITS.md)。
- T1.4：GPT原创冬景与人物、四斜向原生步态、真实队伍同伴/NPC显示平滑、头像与可读对白框、四场景归家开篇。新增范围分段通过，最终成功 Run38931605753；283个运行文件与CI路径一致，257个逐字节一致，26个仅私有文字呈现差异；私有工程54文件机制/二进制一致。发布及完整边界见 [T14 RELEASE](evidence/T14_POLISH_20261017/RELEASE.json)，原始对照见 [美术比较](docs/PAL98_ART_COMPARISON_20261017.md)。用户美术/私有对白观感验收待反馈。
- T2 通用 IR→content22：尚未实现/验收。旧 pipeline.mjs 与轻量 HTML 只为参考测试夹具。
- 已收到用户书籍，先做开篇短阶段内部测试；不得再次索书。原书与私有角色剧情不进入公开GitHub。EXE后置。

开篇私有试玩：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/pilot/

原原创试玩保留：https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site

## 当前开篇构建

`node tools/t14/build.mjs <upstream> <output>`；私有内容用 `T14_CONFIG=<config.json>`。公共CI默认使用原创脱敏配置，公开仓库不含书籍正文。下载源码包包含实际配置与当前T14构建说明。

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

续作先读本页→docs/T13_OPENING_TASK.md→最新 RELEASE 记录→对应失败经验，按未通过项继续。P0/旧首场景冒烟不重跑。引擎/恢复改动才回归受影响的原完整故事，作者入口改动才回归编辑保存重开。

## 后续优先级

先收集用户对开篇移动、对白节奏、庙会密度与演出反馈，再决定下一阶段内容；本次不提前增加觉醒、战斗或全书转换。像素风与网页优先继续保留。长期内存泄漏、Safari/Firefox及真实手机未被本轮证明解决。勿将60秒CI活动测试当作全设备稳定承诺。
