# 下一本书的零重做交接协议

## 操作入口
1. 书籍文件/用户自有故事由**当前对话上传**，不要直接上传公共 GitHub。
   本项目最终采用 **Type PAL Reforge 游戏网页 + Type PAL Editor 浏览器内容工作台**，先读 `docs/WEB_FIRST_PLATFORM_V2.md` 与 `docs/TYPE_PAL_DEEP_REVIEW_20261016.md`。
2. 使用 `node tools/new_book_run.mjs <id> "作品标题"` 创建空白8阶段工作目录。
3. 打开 `runs/<id>/STATUS.json`，从 S0 起依次完成各阶段。不允许先填 S7 为 PASS。
4. 先阅读 START_WEB.md 和 docs/STAGES.md。原著事实与改编新增事项要有来源与专门标记。
5. 每阶段只在真实产物及质量门禁通过后更新STATUS，再进行下一阶段。
6. S4正式内容应由AI/人工审核按协议生成，再运行 `node tools/pipeline.mjs validate <content.json>`。
7. S5用 `node tools/pipeline.mjs build <content.json> <output.html>` 运行原创示例内核验证；Type PAL 官方适配需要额外的引擎实测。
8. S6真实操作/自动测试须覆盖场景、剧情、战斗、后果、存取档、结局。收尾提交可运行游戏和完整 QA 结果。
9. S7归档差异：完成一个新书验证后，用**第二本书只换内容包**进行复用评估。

**数据管理**：runs/及 dist/ 默认不进入公共仓库；发布前只提交获授权的改编内容。任何未授权全文、仙剑原游戏资源和个人敏感信息不得公开上传。

## 使用仅现有 Plus + Codex
GPT网页用于阅读用户所提供原文及导演设计；GitHub connector用于项目管理；Codex接入时使用用户自己的ChatGPT登录，不预设额外Claude或第三方API token。构建/测试尽量在GitHub Actions运行，减少低配置电脑负担。

## 当前完成等级
- 机制研究与固定制作合同：已建档（非100%）。
- 有2份原创小故事内容包、一套轻量试玩运行器、GitHub Actions测试。
- 没有正式的长篇小说转换工具，也没有Type PAL adapter/整个仙剑规则的忠实执行器。下轮先验证这些缺口，不许自动宣布完整商业游戏生成。
