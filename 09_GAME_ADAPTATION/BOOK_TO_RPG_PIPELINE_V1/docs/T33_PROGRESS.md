> 最新进度请先读 [T34_PROGRESS.md](T34_PROGRESS.md)。用户已于 2026-10-18 17:56（Asia/Shanghai）认可 T33 室内，当前按该标准完成第一幕四景美术更新；以下内容为当时的历史记录。

# T33 当前续作状态｜室内与人物独立形象

2026-10-18。承接 WORK_START_HERE.md 与 T32，项目最终完成仍为 FALSE，用户审美验收仍为 PENDING。

## 本轮反馈与实施

用户认可已改善的人物形象，要求主角室内继续接近此前画面参考，并禁止主角与特定人物模型充当普通 NPC。保留此前 98 张栅格资源的全部 SHA256，不重设计游戏。

对照用户室内参考，新增完整墙体、窗外雪村、旧木作、床被、CRT 电视、餐桌与两碗面、水盆、橱柜和灯具。整屋视角为统一显示变换，点击用同一逆变换；原坐标、地图、碰撞、路径与 SAVE12 不变。原“小核桃”吊坠保留原生形象，没有改成玉佩或新道具。

集市 21 名普通 NPC 改用六种群众形象（四方向）；主角、小满、摊主、邻居、问路青年保持独立。后台三名随从分别使用独立的四向三相位模型，抬走复合图保留同一领队与演员身份，另一抬人者改为对应灰帽随从。不是新增角色或剧情。

## 验收证据

- 来源 cd824cff6c5be26aa4eeb5b82eaeab448939a5bd；分支 feature/t33-home-room-identity-20261018。
- 实测运行 cb55699abe55005a5d1d008e7af9a1d26644ef93；分支 t33-room-candidate。
- Run39115653713 六项房间/人物身份检查与两项后台倒地、抬走、重开检查 PASS，零 pageerror。
- 两次前序验收脚本失败分别为离屏缓存绘图记录遗漏、尚未等待异步存读档完成；修正测试等待，没有修改存档逻辑。
- 109 个原生项目文件与 T30 字节一致；306 个部署 game 文件与实测运行字节一致；T22 chapter 五个网页文件保持一致。
- 已通过的完整第一幕九项与上一轮三引擎头像检查沿用，未重复未受影响的旧流程。
- 新房间、群众、后台倒地/抬走实机截图人工检视。上轮后台脚本 result.json 的 scope 文字沿用了旧“wall alignment”标签；本轮真实变化和验收范围以本页及 RELEASE.json 为准。

## 在线复核

房间直达：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/night/

参考与实机：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/#home-room

完整第一幕：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/

同一隔离 Site，仍为原 owner-private 访问。main 与原正式 Site 未覆盖。发布真值见 evidence/T33_20261018/RELEASE.json。最新完整网页 ZIP 已更新原交付文件，含全部本地下载与新审查页。

## 下一步

先读取本页与 RELEASE.json，按用户对现有实机画面的反馈继续优化。不可把技术通过标成最终审美认可。没有真实手机或 Safari 应用验证；已知 WebKit 隐私会话 Blob 存档限制保留。公共工程继续使用合成对白。
