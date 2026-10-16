# Type PAL × Book-to-RPG P0 实际测试验收

测试日期：2026-10-16（UTC记录见GitHub Action）
GitHub Action: https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38853212658
Job: 116818813877
源码基准：`IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246`，对应上游GPLv3；用户仓库仅保留测试工作流/文字研究，未复制引擎源码或游戏版权素材。

## 验证通过（实际执行，非推测）
1. 在GitHub ubuntu-24.04 runner上checkout固定Type PAL源版本，SHA完全匹配：`PIN_AND_CONTENT_22_SAVE_12=PASS`。
2. 上游 `@type-pal/content` 官方 TypeScript typecheck SUCCESS（确认contentVersion22/SAVE12当前实现）。
3. 上游 `@type-pal/reforge` 构建成功，输出 `packages/reforge/dist/index.html`。
4. 上游 `@type-pal/editor` 构建成功，输出 `packages/editor/dist/index.html` 和 `packages/editor/dist/play.html`。
5. Chromium真实页面（非静态解析）导航到官方编辑器开发服务`http://127.0.0.1:6011/?picker`：能够看到`type-pal 编辑器`、`新建空白项目`和`打开项目`，`pageerror=[]`，`BROWSER_EDITOR_PROJECT_PICKER=PASS`。
6. Chromium加载上游真实Reforge dev服务`http://127.0.0.1:6052/`，`VITE_PROJECT_ID=e2e-own`，读取project manifest和场景JSON通过；浏览器Canvas为1280×800、非黑样本数6400，页面脚本异常为空：`BROWSER_REFORGE_SCENE_RENDER=PASS {"gameId":"e2e-own","sceneId":"start","width":1280,"height":800,"nonBlackSamples":6400}`。
7. 整个GitHub Actions job最终`conclusion=success`。

## 强制未验收项
- `e2e-own` 的资产catalog有 `sprite.pal.002` 的 `legacy-migrated` 来源，因此此证明的是引擎内部场景链正常，**不是全部原创版权资源的可发行成品**。
- 本轮未点击“新建空白项目”并完成真实操作系统文件选择器授权、磁盘工程持久化、保存→关闭→重开→重新试玩。仅显示真实入口，不得当作编辑操作完整通过。
- `/projects` 在上游Vite里是本地开发代理，不代表GitHub Pages/S3/CDN静态发布天然可拉取所有project和asset文件。
- 现有V1样例`game.json`非官方content22格式，尚无可运行的StoryGame IR到content22完整适配器。
- 未用用户的《仙剑98》商业资源在本流程里公开部署/复制/重新发布；任何示例项目派生原版权素材不得进入公开发行包。
- 未测试真实书籍自动改编/完整回合制玩法保真与玩家存档。

## 下一步验收 G1（明确拒绝以源码存在冒充验收）
1. 浏览器Type PAL编辑器创建**空白原创项目**，包含自生成且许可证明确的色表、tileset、角色、动画、战斗与文本。
2. 浏览器中编辑“原创旅店”一场景，NPC一人、可见敌人一只、一次战斗、一次对话和结局，再真实保存，重开/再试玩，自动比对玩家状态。
3. Reforge加载该项目的完整content22工程，视频/截图证明画布、人移动、NPC/战斗都真正生效。
4. 形成可公开或私有托管的静态玩家网页，不依赖Vite/本地开发中间件和未授权PAL资产；检查音色库、字体和GPLv3源代码提供义务。
5. 通过后再做书籍 S1/S2 → content22适配与第二故事内容重用。

## 文件定位
- 探针：`.github/workflows/book_rpg_type_pal_probe.yml`
- 源码审读：`docs/TYPE_PAL_DEEP_REVIEW_20261016.md`
- 新架构：`docs/WEB_FIRST_PLATFORM_V2.md`
- 新书适配提示：`prompts/S4_TYPE_PAL_CANONICAL_ADAPTER.md`
