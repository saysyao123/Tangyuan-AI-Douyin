# T1.3 四向修复与开篇短阶段

状态：build allowed；作者 Codex；独立审阅待完成。用户 2026-10-16 明确反馈人物基本单面，并上传书籍要求小阶段内部测试。

## 前提与范围

| 真值 | 一手证据 | 判断 |
|---|---|---|
| 原版 PAL 机制 | 不更改机制；本卡不复制商业资产 | N/A |
| 官方当前 Type PAL | pinned f98d0ddd；reforge/src/sprite-anim.ts FACING_TO_DIR | down=0,left=1,up=2,right=3；3帧走路0/1/0/2 |
| 本项目旧图 | type_pal_t1_art.ts person / wolf | 右视图近似正面；狼忽略dir；迈步差异过小 |
| 本次目标 | 原创代码像素美术；人物鼻尖/后脑/衣襟/脚步分明 | 修美术与布局数据，不改输入/碰撞/存档协议 |

最强替代解释是键位/帧组映射错误；现有 sprite-anim 的明确顺序与生成顺序一致，单面源于图像本身。若真实按键位移方向与 facing 不一致，需重开输入层调查。

## 小阶段边界

两张地图、原生双人队伍、一次购买/消耗、演出、后台发现、返回离场。内容由独立JSON提供；这是固定小阶段模板，不宣称T2通用转换器。上传书籍和私有书籍角色/剧情数据不进入公开GitHub；公开CI使用独立原创脱敏模板。实际书籍切片只在用户已有owner-private Site源码及部署包中。

独立 projectId book-pilot-opening；原 book-lantern-inn 不变。新角色四向三帧；新增摊位、舞台、火光原创像素；所有NPC使用同一官方转向机制。

## 针对性验收

- 四向图像不同、侧视镜像、背面无眼睛、每方向三帧不同。
- Chromium真实方向键位移/facing/走停截图；两个成员同行。
- 新短阶段购买幂等、剧情入口门控、消耗道具、跨图、离场、独立保存重开。
- 官方 content22 校验实际私有工程；公共CI同结构脱敏工程。分别声明验证范围。
- 检查冻结部署内容与CI通用运行时/素材一致，列出纯剧情替换文件。
- 不重复已通过的T1/T11/T12测试套件和P0冒烟。

## 失败经验（滚动记录）

1. 外部工具脚本直接 node --import tsx 会从错误目录解析依赖；复制进 pinned upstream 的 editor/scripts 再运行。
2. 当前 SpriteLayout TS 声明虽含 loop，官方 content22 validator 拒绝 loop。改用合法 static + poses 时间线 + entity page animation，不放宽校验器。
