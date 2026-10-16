# 2026-10-16 — V1 实际执行证据与状态

## GitHub Actions 最新通过记录
- Run ID **38851723543**
- https://github.com/saysyao123/Tangyuan-AI-Douyin/actions/runs/38851723543
- **Node 原创内容校验/引擎单测 17/17 PASS；Python 元数据审计合成测试 2/2 PASS；HTML 双故事内容包构建成功。**
- GitHub Actions artifact: `book-rpg-v1-playable-and-tests`，包含 `dist/lantern-inn.html`、`dist/river-ledger.html`、test-output、python-test-output、2份验证结果、2份构建日志和状态文件。
- 引擎源码在两份内容包之间未修改；不存在“换书后要改写故事名字”的硬编码。此处证明技术样本层的 JSON 内容切换，**不是两本真实长篇小说已被自动改编**。

## 真实 Chromium 浏览器操作（在本次执行环境进行）
采用 GitHub Actions 构建出的实际 HTML，使用 Playwright + Chromium `set_content` 导入页面；**不是只用 Node 测试**。
- `lantern-inn`：移动→NPC对话→雾林→拾取灯芯→雾狼战斗→回驿站→`lights_return`结局，页面 JS error 0。
- `river-ledger`：移动→船工对话→河岸→拾取手札→河泽野兽战斗→回码头→`letter_delivered`结局，页面 JS error 0。
- 两游戏存档序列化/恢复的 UI 事件均经**模拟 localStorage** 通过；由于执行环境浏览器禁止导航本地 `file://` / 本机HTTP，而 `about:blank` 没有可用存储源，不能据此宣称所有浏览器离线本地存储已实际验证。
- 两游戏 screenshot 在本次对话附加验收结果中，未纳入仓库。

## 本轮新书启动
`node tools/new_book_run.mjs <book-id> "书名"`：
- 创建隔离的S0–S7目录、来源清单与 STATUS.json。
- 所有阶段默认 NOT_STARTED，来源授权初始 NOT_VERIFIED；不自动上传原文，不覆盖现有运行项目。
- 要想创作游戏，S1事实与S2游戏导演仍由GPT/用户核实；V1没有自动读取并转换一本长篇小说的能力。

## 机制研究进度
- 《仙剑98》用户上传 RAR 实际只读统计：详见 `evidence/PAL98_UPLOAD_STATIC_AUDIT_20261016.md`。
- SDLPAL 源码机制初步覆盖 world/script/party/battle/equipment/magic/save/ending，见 `docs/MECHANICS_AND_GAPS.md`。
- 下一轮首要缺口：`0xFFFF`指令的实际含义、完整脚本事件关联、Data.mkf人物数值/成长提取、原98版本实机录像与 Type PAL schema 的真正适配。

## 当前各项目 Gate
| Gate | Status | 说明 |
|---|---|---|
| 机制知识档案建立 | PASS（研究目录层） | A/B证据已归档，不是全部机制百分百复原 |
| 原仙剑98实机行为验证 | NOT_TESTED | 原始资源未在目标引擎运行 |
| 两份原创示例内容包可验证 | PASS | Node17+Python2通过；Chomium脚本无异常，事件/战斗/结局真实互动 |
| 真正 Type PAL content22 正式导入 | NOT_TESTED | 本项目原创 JSON 尚无官方引擎适配 |
| GPT输入书籍自动转换完整章节 | NOT_TESTED | 等用户提供一本合法书籍，才可实际测 |
| 公版/授权真实书籍的完整 RPG | NOT_TESTED | 后续首本书试点目标 |
| 两本真实书无内核改动 | NOT_TESTED | 当前仅两份原创 synthetic content packs |

**绝不把独立轻量试玩包装成“仙剑98原样复刻引擎”或“自动把任意书变成RPG”的现成成熟产品。**
