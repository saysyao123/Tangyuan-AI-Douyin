# T1 原创标准网页 RPG 工程：首次真实贯通记录（2026-10-16）

## 复现实证
- GitHub Actions: https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38855229699
- pinned Type PAL: `f98d0ddd89ebdee7b04502ee35de26ee82c6d246`（content22 / SAVE12）
- 上游 `packages/editor/src/core/seed.ts` `buildBlankProject` 在 **Vite SSR** 中生成合法原创场景/assets，不再从原版 PAL 的 MKF 解压复制素材。
- 使用本项目 `examples/lantern-inn/game.json` / `examples/river-ledger/game.json`，当前仅转换第一场景、主角、NPC、首段对话；两项目均为 20 个规范目录文件 + 4种生成资产。源码见 `tools/type_pal_t1_make_original_project.mts`。
- 官方 `pnpm check:content projects/book-lantern-inn` 和 `pnpm check:content projects/book-river-ledger` 真正跑通。
- Reforge + Chromium 打开真实原创工程，画布 1280×800、非黑像素抽样 6032，截图 `t1-original-reforge.png`；`ORIGINAL_TYPE_PAL_BROWSER_RENDER=PASS`。
- React Editor + Chromium 在 `VITE_PROJECT_ID=book-lantern-inn` 环境直接加载**该原创工程**：编辑器显示项目`雾灯驿站`、场景`start`、`npc-welcome` / `守灯人`、脚本和相关右侧面板；页面无JS错误，日志 `ORIGINAL_PROJECT_IN_OFFICIAL_EDITOR=PASS`；截图`t1-original-editor.png`。
- GitHub 2026-10-16 run **38855229699 完全成功**；公开 artifact 为 `type-pal-t1-original-projects`（只有本轮原创生成资产及文本日志截图）。
- 工作归档没有上传仙剑98商业 EXE/MKF/DLL/对白及图片，也没有使用`projects/demo`/`e2e-own`的PAL派生资源。

## 已验证 vs 未验证

| 检验项 | 判定 | 客观证据 |
|---|---|---|
| 首版 StoryGame JSON → 规范 content22 工程 | **PASS（首场景窄版）** | 两个工程生成，官方检查 |
| 自有调色板/瓦片/地图、精灵、战斗帧占位资产 | **PASS** | 上游 seed-assets 生成，asset catalog origin=generated |
| Reforge 浏览器实际游戏画面绘制 | **PASS** | Chromium screenshot、Canvas pixel |
| Type PAL Editor 浏览器加载生成工程 | **PASS** | 编辑器项目名、场景、NPC、截图 |
| 通过真实用户键盘与 NPC 完整交互并确认对话演出 | **NOT_TESTED** | 只有定义及可见场景，未执行全过程 |
| 编辑器修改场景/对话，保存目录/关闭/重新打开 | **NOT_TESTED** | Dev HTTP 读项目与真实 FSA 保存是两件事 |
| 地图切换 / 道具 / 明雷战斗 / 任务flag / 剧情结局 | **NOT_IMPLEMENTED** | 当前生成器明确只支持首场景和NPC |
| 独立 HTTPS 玩家游戏、无需 Vite dev server | **NOT_TESTED** | 官方上游 A8 仍需最终收口 |
| 真实书籍自动生成完整 RPG | **NOT_STARTED** | 用户尚未交书，先做好真实引擎底座 |

## 过程失败复盘
初次直接用 Node/tsx 引用 seed.ts，因上游 Reforge 使用 Vite-only `import.meta.glob` 导致运行异常。现在在真正编辑器 Vite SSR 环境 `ssrLoadModule('/src/core/seed.ts')` 调用生成器，修复后同一云端流程成功。

## 审美/玩法客观差距
当前原创地图只是上游种子生成的交替草地菱形地砖，两名小人复用了相同的原创占位精灵。虽然在编辑器及 Reforge 都实际显示，但**美术非常简陋，距离仙剑98的叙事氛围、地图复杂度、角色动画和完整战斗体系仍有明显差距**。下一轮先做真正可玩的完整垂直切片，而非用新格式文件数替代实际游戏质量。

## 工作继续入口
- 工程文档：`WORK_T1_CONTINUE.md`（专供用户切换 Work 后接力）
- 生成代码：`tools/type_pal_t1_make_original_project.mts`
- GitHub Actions：`.github/workflows/book_rpg_typepal_t1.yml`
- 任务：#25 T1真实原创网页 RPG 全链；#26 S4编译器与第二书零改动复用

**结论：T1 目前只是部分通过；还没到需要用户交小说的阶段。**
