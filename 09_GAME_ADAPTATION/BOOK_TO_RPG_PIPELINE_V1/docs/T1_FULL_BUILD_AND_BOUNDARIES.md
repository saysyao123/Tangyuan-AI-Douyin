# T1 完整原创 Type PAL 网页原型：构建和边界

固定上游：`IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246`，content22 / SAVE12，GPLv3。

## 实际制作内容

- 《雾灯驿站》两张地图：驿站、雾林；人物阿笙、守灯人；原创地图、像素人物、雾狼、道具、战场、标题、菜单图块、光标。
- 剧情链：NPC 接任务 → 路牌进雾林 → 灯芯入原生背包 → 明雷触碰进入原生回合战斗 → 胜利奖励和 flag → 回驿站交物 → 结局。重复结局不会重复领钱。
- 运行和战斗都是官方 Reforge。没有另写小游戏引擎或用页面按钮替代任务状态。
- 原生 IndexedDB 玩家存档，F5 / F9；与编辑器保存内容工程分开。
- 官方网页编辑器保留完整功能；新增显式 OPFS 浏览器目录创建入口，以及单句 NPC 对白快捷修改。快捷修改派发官方 `UpdateEntityBehaviorCommand`，保存使用官方 workspace policy、writeProject、保存日志和事务。
- 标准电脑文件夹 FSA 仍需用户手势、原生选夹和权限。浏览器目录是 OPFS，不伪装为用户电脑文件夹，不拦截或模拟选夹 API。

## 复现

1. Checkout 固定上游（保持此 SHA，禁止自动升级）。
2. Node 22.19+，`pnpm@10.17.1 install --frozen-lockfile`；Python 3 + Pillow。
3. 从本目录运行：

```bash
node tools/type_pal_t1_build.mjs /absolute/type-pal /absolute/output
python3 -m http.server 8080 --directory /absolute/output
```

通过 `http://localhost:8080/` 打开；正式发布使用 HTTPS。构建产物包含玩家页、官方编辑器、完整 canonical 项目、对应源码 ZIP、静态网页 ZIP。无 Vite 开发服务器依赖，不能把 file:// 双击作为网页运行验收。

CI：`.github/workflows/book_rpg_typepal_t1_full.yml`。只测试本轮新增的完整故事、真实战斗、跨页读档与编辑保存闭环，不再次运行旧 P0 首场景冒烟。完整故事变更或已发现失败修复后才回归相应链路。

## 合法资源闭包

上游引擎默认 chrome 的 `PROVENANCE.md` 明示默认标题、85 个 UI PNG 和对话光标含 PAL 派生像素。**原创项目资产不代表引擎 bundle 可以原样分发。** `type_pal_t1_prepare.py` 将这些默认 chrome 全部替换为独立程序绘制的像素画，连 favicon 一并替换。不得跳过此步骤。

GNU Unifont 保留上游字体及许可。原创胜利 MIDI 由脚本合成，TimGM6mb 音色库单独按 GPL2 分发并附上游说明。用户书籍全文、PAL 商业角色、图片或音乐均不进入发布包。

GPL 对应源码 ZIP 包含实际修改后的 content/shared/reforge/editor、配置、依赖锁文件、资源、原创工程和全部构建/测试脚本。下载入口随网页提供，避免只有压缩 JS 而缺源码。

## 不能混同的边界

- `type_pal_t1_full.mts` 是 T1 原创短篇的具体作者适配器；**不是**任意小说→完整 RPG 的通用编译器。T2 尚未验收。
- “浏览器目录保存重开”与“原生选择用户电脑目录”分别记录。自动测试不静默申请电脑目录权限，也不把 OPFS 测试说成原生 OS 选夹测试。
- 网页静态目录独立可运行与正式 HTTPS 部署分别记录；CI 通关不能替代部署成功证据。
- 不做 EXE；不增加模型付费 API；未读取、索要或公开书籍。
