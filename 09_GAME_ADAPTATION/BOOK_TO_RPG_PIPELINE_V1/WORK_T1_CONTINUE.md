# WORK 模式接力执行｜Type PAL 纯原创网页游戏 T1

> **T1.4：原始MKF对照、GPT原创人物/场景、同伴显示平滑与四场景归家开篇已实现。先看 evidence/T14_POLISH_20261017/ 与 docs/PAL98_ART_COMPARISON_20261017.md。新范围分段验证：38930405574 的美术/同伴/旧档衔接通过；38931108760 新对白验证；38931605753 后段结局/读档/七步界面通过。保留前两轮真实失败记录，只继续未通过部分，没有重跑P0/T11/T12旧套件。私有书籍对白观感仍由用户试玩验收。**

> **T1.3续作：已收到用户书籍并制作私有开篇切片，四向人物修复与新增11项流程/最终画面反例通过。先看 CURRENT_STATUS.md、docs/T13_OPENING_TASK.md 和 evidence/T13_OPENING_20261016/；不要再索书，也不要重复旧套件。私有对白排版由用户试玩确认。**

> **当前状态以 [CURRENT_STATUS.md](CURRENT_STATUS.md) 为准。** T1.2 基底已验收发布（Run 38891702378），结果与失败复盘见 evidence/T12_FOUNDATION_20261016/；下方历史优先级不覆盖最新发布与验收。


日期：2026-10-16

> **最新 T1.1：保留像素风，已完成移动显示插值、失焦输入释放、低开销缓冲、加载反馈和编辑保存防连点。** 定向单测 18 项、真实浏览器稳定性 8 项，以及受改动影响的通关/编辑保存重开回归均通过；成功 Run 38862020435。完整 T1 既有验收继续有效，不重复 P0/单场景冒烟。最新交付与实测边界见 `evidence/T11_STABILITY_20261016/RELEASE.json`、`PERFORMANCE_SUMMARY.md`；失败经验见 `IMPLEMENTATION_NOTES.md`。下文保留历史，不得将历史“未测”当作现状。

> **2026-10-16 Work 续作更新：T1 完整故事、原生战斗、存档跨页恢复、官方编辑器真实浏览器目录修改保存→关闭浏览器→重开→Reforge 显示修改均已 PASS。** 成功 Run 38857559015；后续不要重复旧 P0 / 单场景冒烟。最新验收边界、失败复盘见 `evidence/T1_FULL_ORIGINAL_PASS_20261016.md`；发布状态见 `evidence/T1_RELEASE_20261016.json`。下方为原始接力记录，不能把历史“未测”当作最新状态。T2 尚未验收，EXE 仍后置。

## 任务方向（用户锁定）
完成“基于经典仙剑98游戏结构，将用户随后上传的书籍制作成真实可玩的网页RPG”。**优先网页端完成可玩游戏和创作编辑；Windows EXE 只是将来游戏完成后利用Tauri/Electron封装，当前不做。** 还不需要书，T1可玩原型通过后才让用户上传小说。

- 仓库：`saysyao123/Tangyuan-AI-Douyin`
- base: `main`
- 本次新工作分支：`feature/book-rpg-typepal-t1-original-20261016`
- 目录：`09_GAME_ADAPTATION/BOOK_TO_RPG_PIPELINE_V1`
- P0官方 Type PAL 项目成功验证：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38853212658
- **本轮T1核心成功验证**：https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38855073499
- 官方源码固定SHA：`IllegalCreed/type-pal@f98d0ddd89ebdee7b04502ee35de26ee82c6d246`，当前 content22 / SAVE12，GPLv3。
- 当前独立制作任务：https://github.com/saysyao123/Tangyuan-AI-Douyin/issues/25；后续内容编译任务：https://github.com/saysyao123/Tangyuan-AI-Douyin/issues/26

## 重要成功记录：不是小型自制引擎
通过 GitHub Actions 真正使用上游 `packages/editor/src/core/seed.ts` 的 `buildBlankProject`，在 Vite SSR 环境内编译两份书籍内容原型：
- `projects/book-lantern-inn` 与 `projects/book-river-ledger`，每份20个标准项目文件，包含上游自动生成、完全原创的色表/tileset/人物地图精灵/战斗精灵。未复制任何原版PAL资产。
- 使用本项目 `examples/lantern-inn/game.json` 与 `examples/river-ledger/game.json` 的人物名称、属性和一段NPC对话映射到官方`content22`工程。
- 官方 `pnpm check:content <projects/book-*>` 两份均通过。
- 真正Reforge Chromium加载这份自有工程，Canvas渲染非黑采样6032，零页面JS异常：
  `ORIGINAL_TYPE_PAL_BROWSER_RENDER=PASS {"nonBlackSamples":6032,"w":1280,"h":800}`。
- GitHub Action可下载两个合规原始工程和文本日志：Run 38855073499 的 `type-pal-t1-original-projects` artifact。

### 失败及修正经验
最初直接`tsx` import官方`seed.ts`：经过其依赖 `engine-chrome/registry.ts` 遇到`import.meta.glob is not a function`。已改为编辑器目录启动 Vite Server，`ssrLoadModule('/src/core/seed.ts')`，上游官方原始资源生成器成功执行。以后不要重用失败的tsx直接import路径。

## 2026-10-16 补充：官方 Editor 已成功打开真实原创工程

正式成功 GitHub Run 38855229699：`ORIGINAL_PROJECT_IN_OFFICIAL_EDITOR=PASS`，Chromium编辑器显示雾灯驿站、场景start、守灯人和脚本面板。Reforge原生界面同时已渲染。证据归档 `evidence/T1_ORIGINAL_TYPEPAL_CONTENT22_ENGINE_EDITOR_20261016.md`，两项目合法原创ZIP与浏览器截图已提供给用户。**下一步不要重复跑已经通过的P0/T1首场景加载，而应完成真实NPC按键交互、S5剧情任务战斗、FSA修改保存与重开、独立静态网页发布。**

## 核心文件
- `tools/type_pal_t1_make_original_project.mts`：T1首版正规工程转化器，目前只映射一个场景、一位NPC、事件首段对白、主角属性及原生合成素材；**不能宣称支持多场景/道具/战斗/结局**。
- `.github/workflows/book_rpg_typepal_t1.yml`：官方源码 checkout → pnpm依赖 → 两份原创工程 → 官方校验 → 浏览器真正 Reforge Canvas → 编辑器载入冒烟，原生工程产物上传 artifacts。
- `docs/WEB_FIRST_PLATFORM_V2.md`：北极星和EXE后置。
- `docs/TYPE_PAL_DEEP_REVIEW_20261016.md`：上游权威模块与API。
- `START_WEB.md`：收到书籍后S0–S7正式流程（现在不要要求用户给书）。
- `evidence/TYPE_PAL_P0_BROWSER_VERIFIED_20261016.md`：既有P0验证。

## 下一步严格优先级（尽量实际完成，不要改写成更复杂理论）
1. 从最新 `book_rpg_typepal_t1.yml` Action 观察真实编辑器能否加载 `book-lantern-inn`。失败就看log修复；形成证据与截图。
2. 使用 Type PAL 当前 canonical 事件编译逻辑，将“与NPC实际对话”在真实Reforge由键盘/游戏状态触发并观察，不仅数据校验通过。
3. 给第一份原创故事补第二场景、入口传送、实体物品、明雷敌人与回合战斗、任务flag和结局。按上游 `packages/content` 的定义及 `projects/demo` 参考制作，但**不要复制demo的PAL人物或美术**。
4. 验收真实浏览器存档与载入、NPC对话编辑、保存目录→关闭→重新打开→再次试玩，保留修改效果。注意浏览器File System Access必须安全上下文、用户手势和权限；不可无感绕过浏览器安全保护。
5. 形成无dev-server依赖的静态玩家网页：独立工程和assets必须随bundle部署，浏览器直接打开 HTTPS 后真能玩；从头到结局Playwright回归（截图/视频）和真实下载。
6. 达成T1后实现完全可重复的`StoryGame IR→content22`编译器T2；确保第二份原创故事仅换内容包、引擎SHA不变。
7. **只有T1网页完整原型通过而且能合法发布试玩时，才提示用户发第一本有权使用的书**。之后执行S0书源→S1人物剧情→S2章节玩法→S3资源→S4官方content22→S5引擎→S6试玩→S7交付。

## 测试状态（切勿虚报）
- T0 上游编辑器+Reforge真实浏览器：PASS。
- T1 两份原创**单场景内容22工程构建/官方校验**：PASS。
- T1 一份原创工程Reforge真实网页画面渲染：PASS。
- T1 官方编辑器实际加载用户生成工程：当前追加Action待复核。
- T1 NPC实际互动、地图切换、道具战斗、游戏结束、网页保存重开、静态发布：未通过/未测。
- T2 全书转换：未启动。
- EXE：后置。

**行动纪律**：用户只订阅GPT Plus；不增加付费云API或本地高配置负担。上传原仙剑商业资产/用户书籍全文到公开 GitHub 严禁。每一次失败记录证据并修复，未通过不继续称成功。下一次以实际网页试玩成片/工程为交付，而不是更多泛泛机制分析。
