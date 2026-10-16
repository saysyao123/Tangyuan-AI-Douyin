# 新书转经典 RPG — 网页端接力入口

> **先读 [CURRENT_STATUS.md](CURRENT_STATUS.md)。** 无书续作优先按 T1.2 任务卡和最新发布记录处理基底；T1/T1.1 已通过的内容不重复测试。本页后续 S0–S7 仅在用户提供有权使用的书后进入，不应主动先索书。


请使用已连接 GitHub 仓库 `saysyao123/Tangyuan-AI-Douyin`，读取本目录全部必读文件：
1. README.md
2. docs/STAGES.md
3. docs/MECHANICS_AND_GAPS.md
4. docs/CHARACTER_AND_STORY.md
5. docs/QA.md
6. docs/FORMAT_AND_ADAPTER.md
7. docs/RIGHTS_AND_ASSETS.md
8. prompts/S1_SOURCE_ANALYSIS.md、prompts/S2_GAME_DIRECTOR.md、prompts/S3_CONTENT_COMPILER.md
9. 上层 `../PAL98_BOOK_RPG_BASELINE_V0_1/` 的研究资料。

**项目目标**：给定用户有权使用的小说/书籍，保留仙剑98式的经典RPG机制，将**书籍内容**按阶段转化成全新的可玩游戏。**最终作品必须以浏览器网页呈现，并优先进入 Type PAL Reforge + Editor 官方内容工程**。不要把目标切回“复刻仙剑”，不要随意重设计游戏机制。

**新版必读（先于S4）**：`docs/TYPE_PAL_DEEP_REVIEW_20261016.md`、`docs/WEB_FIRST_PLATFORM_V2.md`、`docs/TYPE_PAL_GATE_AND_COMPAT.md` 和 `prompts/S4_TYPE_PAL_CANONICAL_ADAPTER.md`。

**收到书后的执行纪律**：
- S0权利与输入识别→S1章节、事实、人际关系与章节证据→S2游戏导演的可玩节拍和人物技能映射→S3原创/授权资源与一致性清单→S4内容包编译与引用校验→S5游戏引擎适配、构建→S6真实试玩/自动回归→S7交付与下一轮迭代。
- 每一步有单独输入、可核对的文件、门禁和停止条件；未通过的步骤不得标 PASS。优先 **原著结构→玩家行动→因果→机制**，不是逐段照搬对白。
- 明确区分原文事实、由原文推断、为游戏新增的演绎。未经原文支持的事实不得冒充原著。
- 若不是用户原创、公版或明确获授权的原作，在没有相应许可时不要把原文全文、受保护的人物图像、影视音乐等重新发布。
- 交付请包含真实能运行的游戏文件或准确说明受阻原因，保留测试日志和最新状态。
- 默认无新付费订阅。不能假设拥有任意 API key、Codex 的本地 Windows 访问或云浏览器执行能力。
- 若书籍较长，先自动分章节和构建全局事实索引，再按故事弧制作首个章节，不假设一次把整书塞入上下文。

**收到书之后的第一轮应产出**：S0 rights/source manifest、S1 chapter-index/fact-ledger/character-links、S2 首个故事弧最小可玩关卡设计，连同版权风险清单和门禁状态。按照阶段仅输出必要结果，不生成过多不可验收的文档。

**不可混淆**：
- `node tools/pipeline.mjs build` 为原创轻量试玩内核/数据测试夹具，仅证明输入与演示可连接，**不可作为新书正式 Type PAL 游戏交付**；
- 把整本书变成原版复杂度的 RPG、Type PAL/Reforge 正式内容适配，以及真实用户《仙剑98》参考运行，目前都不是已验收事实。官方 Type PAL 网页编译、项目选择页/场景冒烟测试须看本轮实际 GitHub CI，不能由演示代码推断。
