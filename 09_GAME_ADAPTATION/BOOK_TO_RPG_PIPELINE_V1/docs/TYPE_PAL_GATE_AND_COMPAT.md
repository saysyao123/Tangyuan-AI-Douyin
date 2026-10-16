# Type PAL兼容性与交接门禁

## 静态核实完成（源码锚）
- 仓库的完整阶段介绍：`README.md`、`docs/phase2/READ-FIRST.md`、`docs/phase2/roadmap.md`
- 数据权威：`packages/content/src/character.ts` 的 `CONTENT_VERSION=22`, `CURRENT_PROJECT_MINIMUM_SAVE_VERSION=12`
- 原创样本目录：`projects/e2e-own/README.md` 明确仍含少量 PAL 派生资源（不能宣称完全自有）
- 编辑器：`packages/editor/src/main.tsx`、`packages/editor/vite.config.ts`、`packages/editor/src/ui/ProjectPicker.*`
- 作者工程与游戏：`packages/reforge/vite.config.ts` 有开发期 `/projects` 路由映射
- `docs/phase2/specs/content-schema.md`：SceneIndex/MapIndex/ProjectMap4/AssetCatalog完整依赖链
- `docs/phase2/capability-map.md`：A1、A8、完整Q1/Q2状态。以当前提交为准；不照搬历史完成率。
- `packages/editor/package.json` 和 `packages/reforge/package.json` 的 Vite 构建命令。

## 禁止误报
- 成功运行 `editor build` 不等于可编辑原创游戏；只有手动/自动 UI 建立工程、保存重开和Reforge游玩通过才是T1。
- `projects/demo` 不是版权清理模板；删除原游戏源码、换名称，不能算独立可发行。
- 能本地 `vite preview` 不等于可公网发布；dev server `serveDir` 路由代理未必打入静态 bundle。
- 只跑本项目V1小游戏的17项测试，不等于 Type PAL官方引擎集成成功。
- 上游第一阶段 `v1.0.0` 可通关，不等于 Reforge 第二阶段全量无缺陷。

## 构建测试（第一道实际验证）
GitHub Actions `.github/workflows/book_rpg_type_pal_probe.yml` 从固定 commit checkout 原仓库，运行 `pnpm --filter @type-pal/content typecheck`、`pnpm --filter @type-pal/reforge build`、`pnpm --filter @type-pal/editor build`，并尝试启动空编辑器的安全浏览器导航。如果构建因源码版本或依赖环境失败，记录日志并标FAIL；**不能只展示成功的V1小游戏测试来代替**。

## 后续需由用户真实体验的验收
Chrome/Edge打开真正的 Type PAL 编辑器：空白工程→创建图层/角色/NPC/对话→保存到自己选择的目录→关闭后重开→编辑器内试玩→切换浏览器会话再读档。发生浏览器文件权限提示应说明而不是绕过。
