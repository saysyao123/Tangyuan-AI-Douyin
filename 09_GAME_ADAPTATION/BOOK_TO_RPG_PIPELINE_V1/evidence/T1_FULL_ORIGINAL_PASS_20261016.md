# Type PAL T1 完整原创网页 RPG 验收

日期：2026-10-16（Asia/Shanghai）

## 原始目标与本轮结果

沿用固定 Type PAL 上游，把《雾灯驿站》从已通过的单场景原型，推进到可从接任务玩到结局的原创网页 RPG。没有索要或读取书籍，没有转向自制引擎，没有制作 EXE。

**完整故事、真实战斗、存档和编辑保存闭环：PASS。**

成功回归：[Run 38857559015](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38857559015)。测试源码提交 `3f56b2255987babc9a9c05e3168df07c2906ad71`。只运行本轮新增需求；未重跑旧 P0 首场景加载冒烟。

证据单独归档：[Run 38858007838](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38858007838)；仅拆分上一轮产物，没有重玩或重新宣称测试通过。

上游：`IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246`。content22 / SAVE12。

## 已经证明的行为

| 验收项 | 实测方式 | 结果 |
|---|---|---|
| NPC 实际交谈 | 新局方向朝向 + 空格，观察原生对白及 quest_started | PASS |
| 跨场景传送 | 实际走到路牌，按键进入雾林、再返回驿站 | PASS |
| 实体道具 | 与蓝色灯芯交互，原生背包出现 lamp-core ×1 | PASS |
| 明雷与回合战斗 | 走近可见雾狼，原生战斗选攻击、选目标、逐回合执行 | PASS |
| 战后任务状态 | wolf_defeated=true，金钱 10；敌人消失 | PASS |
| 完整结局 | 回守灯人处交物、灯芯扣除、金钱 30、ending_seen=true，显示“第一章·完” | PASS |
| 重入幂等 | 再次交谈不重复发奖励 | PASS |
| 玩家存档 | F5 → 关闭页面 → 新页面新局 → F9；场景、位置、flag、背包一致 | PASS |
| 结局存档 | 保存后刷新、读取，结局状态保留 | PASS |
| 真正静态运行 | Vite build 产物由普通 Python 静态服务器提供，无 dev-server，无 /extracted 数据 | PASS |
| 官方编辑器保存 | 明确点击创建真实 OPFS 目录；快捷编辑派发 canonical 命令并走官方保存 | PASS |
| 编辑关闭重开 | 关闭整个 Chromium，重用真实 profile，最近项目打开同一目录与 workspaceId，修改保留 | PASS |
| 修改进入真实游戏 | 从编辑器打开 workspace 试玩，Reforge 读取目录并显示修改后的 NPC 台词 | PASS |
| 正式发布所用运行文件一致 | CI 的 game/editor 共 136 个文件 SHA256 与本机发布目录逐个对比 | PASS：0 missing / 0 different |

测试没有向游戏注入 flag、奖励、坐标或胜利结果；使用只读快照核对真实状态。编辑使用真实 React UI 和官方保存事务，没有拦截 showDirectoryPicker 或伪造文件系统。

## 失败与修复（保留负证据）

1. 本机默认 pnpm 12 忽略旧 patchedDependencies 配置，frozen-lockfile 拒绝。恢复已验证 pnpm **10.17.1** 后安装通过；未擅改锁文件。
2. 本机 tsx CLI 尝试创建 IPC 管道被拒（EPERM）；改用 `node --import tsx`，仍通过 Vite SSR 加载官方 seed，而非恢复旧的直接 import 错误路径。
3. 第一轮完整剧情测试 [38856784440](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38856784440)：NPC、传送、道具、跨页读档通过，雾狼战败。根因是 Type PAL 敌攻叠加 `(level+6)*6`，不能沿用自制 demo 的小数值。按真实公式重新平衡主角与敌人，没有改引擎战斗公式。
4. 第二轮 [38857103233](https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38857103233)：击败雾狼后卡住，控制台明确报缺 `audio.bossVictoryMusic`。补齐原生音频切片的全部角色、原创 MIDI、合法音色库和 root worklet 路径；不以空白假资源掩盖。
5. 同轮编辑器测试中，临时 / incognito 上下文下创建目录后 Chromium 退出；捕获原始异常，而非让失败截图错误覆盖根因。使用真实持久 profile 后创建、保存、完整浏览器退出重开和试玩全部通过。这里只确认修复后的路径有效，**没有证明 Chromium 退出的更底层原因**。
6. 上游默认引擎 chrome 含 PAL 派生像素：完整替换 85 个 UI PNG、title、dialog cursor 和 favicon，保留合法字体及音色库许可。不能只检查项目 catalog 就宣称发布素材合法。
7. 成功 CI 原产物约 99MB，一次下载在本环境拿到截断 ZIP，未当作成功。另开归档工作流拆出约 3.9MB 成功证据，下载、解压、图片和 JSON 检查通过，没有重跑故事测试。
8. 发布 ZIP 去掉嵌套的源码/工程 ZIP，三个下载包并列提供；静态 ZIP 约 21MB。只改分发包装，game/editor 的 136 个已测运行文件逐字节不变。

## 准确边界

- 自动化验证的目录是 **OPFS 浏览器私有目录**。它有真实 FileSystemDirectoryHandle 和文件读写，但不等于用户电脑文件夹。
- 原生 OS 选夹与权限弹窗保留，需要用户自己操作；没有声称自动化已经替用户完成 OS 授权。
- 玩家存档与编辑器内容保存相互独立；编辑自己的工程不会覆盖固定发布版。
- 当前是两场景短篇完整原型，T2 通用 StoryGame IR 编译器和整本书籍改编尚未验收。
- 编辑器可能提示项目默认 #24 战场未配置；本章战斗显式绑定已验证的 #0 原创战场，不使用该默认项。这是编辑器默认提示的已知限制，不影响已通过的本章战斗。
- 浏览器工程与玩家存档随当前网站和浏览器保存；清理站点数据可能删除。编辑器“文件→导出 ZIP”或“另存为”用于备份。

正式 HTTPS 发布信息见 `T1_RELEASE_20261016.json`，只有部署服务返回 succeeded 后才写为成功。
