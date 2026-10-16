# Type PAL 深度核查：网页端仙剑式 RPG 制作平台

- 上游： https://github.com/IllegalCreed/type-pal
- 固定源版本 `f98d0ddd89ebdee7b04502ee35de26ee82c6d246`（2026-10-15）；GPL-3.0。
- 截至本轮，仓库 README 写明第一阶段 `@type-pal/game` 浏览器版可通关；第二阶段 `@type-pal/reforge` 新运行时、`@type-pal/editor` React 编辑器、`@type-pal/content` 统一内容模型正在迭代。第一阶段打通原版不等于第二阶段可制作并发行独立新游戏。
- 演示地址 https://pal.illegalscreed.cn/ 是 PAL 在线试玩；它**不是**我们的新书编辑后台或公版新游戏自动发布平台。
- 官方 README 表示第二阶段在“不依赖源码仓库的独立可玩包”上仍待收口；A1 版本化预制素材库、A8 可分发包及 Q1/Q2 回归尚待完成。不能凭 UI 截图和 test pass 声称产品成熟。

## 真实代码结构与职责

| 上游包/目录 | 用途 | 对我们项目的意义 |
|---|---|---|
| `packages/game` | 第一阶段原仙剑 TS 实现，事件脚本和战斗基线 | 对比传统仙剑玩家体验的证据，不作为新书底层直接维护 |
| `packages/content` | CurrentManifest/场景/事件脚本/地图/角色/资源与引用检查 | 小说编译器的**唯一目标格式** |
| `packages/reforge` | 可读取新内容工程的浏览器运行时 | 玩家页面核心引擎 |
| `packages/editor` | React 可视化编辑器、地图/剧本/NPC/角色/资产/战斗/试玩 | 未来网页内容修改与验收面板 |
| `packages/migrate` | 原 PAL 数据向现代内容迁移 | 仅技术参考，不让新小说依赖原版数据 |
| `packages/pal-extract` | 原 MKF 解码 | 只用于合法的原版分析，避免新书生产绑 MKF |
| `projects/demo` / `projects/e2e-own` | 开发样本，**包含部分 PAL 派生资源** | 不得直接复制到公开可分发的书籍游戏模板 |

## 现行内容合同：contentVersion22 / SAVE12

直接参阅上游：
- https://github.com/IllegalCreed/type-pal/blob/f98d0ddd89ebdee7b04502ee35de26ee82c6d246/docs/phase2/specs/content-schema.md
- https://github.com/IllegalCreed/type-pal/blob/f98d0ddd89ebdee7b04502ee35de26ee82c6d246/packages/content/src/character.ts
- https://github.com/IllegalCreed/type-pal/blob/f98d0ddd89ebdee7b04502ee35de26ee82c6d246/docs/phase2/specs/script-system.md
- https://github.com/IllegalCreed/type-pal/blob/f98d0ddd89ebdee7b04502ee35de26ee82c6d246/docs/phase2/specs/project-lifecycle.md

`manifest.json` 包含 `id`, `name`, `contentVersion:22`, `minimumSaveVersion:12`, `defaultEntryId`, `entryPoints`, `content`, `assets`。独立入口 `entryPoints[i].startWorld` 为开场队伍、背包和金钱等初始状态；剧情脚本是场景事件，不属于 startWorld。场景索引 `content/scenes/index.json` 给定稳定 `id` 与相对文件路径，`SceneDef` 引用稳定地图ID，地图索引 `content/maps/index.json` 拥有独立身份；地图采用 `ProjectMap v4`，二维菱形坐标、图层、tile source、heights、collision。瓦片 PNG导入会量化，变为包含 gzip 与索引色的规范资源，AssetId→catalog→FileSource 资源链与内容引用须闭合；不得直接把我们的简易 `terrain` 行数组扔给引擎。
`SAVE12` 保存世界与NPC脚本续跑进度；新书必须区分 *静态内容工程* 与 *玩家的运行存档*。开发期上游拒绝旧 schema 版本，不维护兼容分叉。

## 网页编辑真实实现限制
- `packages/editor/vite.config.ts` 使用 Vite 开发期中间件，将 `/projects/*` 映射到仓库根真实工程目录；`/extracted/*` 处理原提取目录。**只上传 editor/dist 到 GitHub Pages 并不会自动提供真实工程数据 API 或映射**。
- 编辑器支持 Chromium 安全上下文的 File System Access、IndexedDB最近目录句柄、克隆本地工程、保存与另存；`play.html` 做同源试玩。普通非安全站点或非兼容浏览器不能假设能原样保存目录。
- 上游 `packages/editor/vite.config.ts` 标明 `localhost` 被浏览器视作安全上下文、普通 LAN HTTP 不行；网站应该上 HTTPS，并提供不能使用 FSA 时的 ZIP 导入导出与权限提示。
- 资源闭包、文件持久化、版本化、引用删除保护，不是简单的“网页能改一个JSON”。
- 上游目前并未承诺即开即用的“全云端在线存储+一键分享”；我们可以先做 **静态托管编辑器 + 浏览器本地文件工程 + 静态玩家网页**，再单独建设可发布托管层。

## 学到的重大经验（用于本项目）
1. 以完整 canonical 项目目录为原子可编辑对象，`manifest/content/assets` 三者不分家；禁止引擎依赖外部 PAL 文件。
2. 角色/技能/剧情/场景/资源全部使用稳定语义 ID（不是数组下标/原版资源序号）。
3. 向 Type PAL 导出先按 `@type-pal/content` 的类型、资源引用闭包校验，失败时停止写盘，不用空白假资源偷偷补缺。
4. 剧情应表示可回放的 **事件条件/世界状态/后果**，静态保存与游戏存档边界分离。
5. 可视化创作要能**创建→引用→预览/试玩→保存→重开→删除/引用保护**全闭环。
6. 后续引擎部署以实际干净环境 E2E 为验收；线上公开需要清理任何PAL派生素材及GPL源许可义务。
7. 不维护自己的完整RPG引擎作为正式新书线路；现有V1轻量demo降级为内容编译器单测与备用回归夹具。真实小游戏走 Reforge，状态 G1 未完成时必须标未测试。

## 首选架构决策
**制作与试玩都放网页：**

GPT书籍理解 → 授权事实档案 → StoryGame中间语义模型 → `adapter/type_pal_content22` → Reforge 标准工程目录 → `@type-pal/content` 校验 → Editor（网页调整）↔ Reforge（同源试玩）→ 正式玩家页（静态HTTPS版，有清洁版权资产）→ 验收/回归。

现阶段不 fork 或复制上游整仓到我们的公开仓库；使用固定 commit 从 upstream Checkout 再独立测试。真正需要补丁时，尽量以最小补丁+来源说明保留 GPLv3 许可与对应源可用性。
