# AI Digital Asset Factory｜零新增费用数字资产工厂 V1.2

> 制定：2026-10-26｜修订：2026-10-26（V1.2 S0–S8 完整路线，保留 V1.1 前置审核）｜项目状态：PLAN_LOCKED / IMPLEMENTATION_NOT_STARTED  
> 仓库：saysyao123/Tangyuan-AI-Douyin｜分支：main  
> 本文件是本项目唯一启动入口。当前只提交方案，不创建代码、商品或其他文件。  
> 本项目与已有 MV、AI 早报、网页 RPG 等并列，**不覆盖**它们的既有工作流与锁定规则。

## 0. 一句话目标和任务契约

**原始目标**：仅使用用户已经付费的 ChatGPT Plus 及其当前可用的 GPT、Codex、Work 能力，结合免费、许可清楚的开源项目，生产可以反复销售/授权、尽量无需日常客服的原创数字资产；持续增加有效资产并争取真实净收益。

**最终目标**：能定期重复运行的「市场发现 → 小规模制作 → 机器/人工双层质检 → 平台发布 → 真实交易数据 → 继续/修正/停止」闭环。长期参考目标为净收入人民币 10,000 元/月，成熟阶段人工维护每周不超过 5 小时；这是**愿景而非承诺**。

**本轮交付**：一份零新增费用的执行方案；不是生产系统，更不是已经上架、已经取得收益。

**锁定约束**：

1. **新增现金支出预算 = 0**：不购买 API tokens/credits、额外 AI 订阅、付费软件、插件、云服务器、域名、字体/素材、广告、样书或第三方服务。Plus 既有订阅费用为唯一已存在的订阅前提。
2. 优先 GPT/ChatGPT 对话完成研究、文本与创意；Codex 编写、运行与维护脚本；Work 只在**当前账户已开放且使用包含额度**时用于多步执行。不得假设任一入口无限次、永远可用。
3. **ChatGPT Plus ≠ OpenAI API 额度**；不能用 Plus 浏览器会话冒充 API，不能保存或共享 cookie/session/token；不能使用第三方付费模型。
4. 正式产品必须是原创、合法可商用、用户真正能使用的作品。开源程序许可证与字体、图标、样例素材授权必须分别审查。
5. GitHub 主仓库为 Public：这里仅公开方法论、链接和非敏感执行规范；待售商品源文件、内部选题、销售数据、身份证明、平台会话不得提交到本公开库。
6. 以**真实订单/实际版税**为最高商业证据，不以文件数量、自动化程度、GitHub Stars、平台审核通过或浏览量替代盈利。
7. 自动化不得规避平台账户限制、验证码、人工发布确认或付款/审核流程；平台本人身份、税务和收款处理须由账号所有者负责。
8. 要求“低售后”，不是声称绝对零售后：可能发生拒稿、版权争议、质量投诉、退款、账号问题、税务义务。
9. **新增最高优先级流程规则：每个重要步骤开始前先通过 STEP-0 第一性原理、苏格拉底八问、GitHub 开源比选及反证（§5.3）。**
10. **视觉审美必须先通过 VISUAL-0：查至少两个相关开源设计项目、研究真实商业展示、制定可验收样板，严禁闭门造车（§5.3）。**

**本轮验收标准**：方案能指定免费技术、唯一第一批产物、成本硬门槛、可执行分阶段任务、各 Gate 证据、真实收入实验设计及下一轮直接可粘贴的执行指令。任何未运行项目均标记 NOT_TESTED。

## 1. 与主仓库已有能力的衔接

已经核查 main 分支：

- README.md：主仓库原则是 experiment → evidence → rule → gate → regression → promotion；本项目继承这一方法，不继承 MV 特有的音频、镜头和发片要求。
- 08_AGENT_CONTROL_LAYER/README.md：复用「No Evidence, No State Transition」「Generator != Judge」「Atomic Judgment」「Code owns deterministic control flow」「Stage seal / compact handoff」。这些是**设计原则**；不可声称本项目已实现独立 Judge。
- 09_AGENT_RUNTIME/README.md：复用 Plus-only 边界——GPT 提供真实输入，免费确定性代码执行，执行结果需要文件/测试/哈希证明；不把 ChatGPT 对话伪装成可跨日无人值守的 API Agent。
- 00_CONTROL/MASTER_CONTROL.md 与 00_CONTROL/LOCKED_RULES.md 主要服务既有抖音项目：不覆盖、不编辑、也不擅自将视频垂类限制复制到资产项目。
- 现有仓库无需更改根 README、旧目录、CI 配置。此新目录目前仅包含本计划文件。

**新项目命名空间**：10_DIGITAL_ASSET_FACTORY/。下一阶段开发时再按实际需要建立单独工作区/私有仓库，当前不擅自新建别的文件。

## 2. 第一性原则：如何赚钱而不是如何批量生成

一件资产的收入潜力近似取决于：

**可触达的真实购买需求 × 商品实际竞争力 × 平台可见性 × 单笔净版税 × 资产有效生命周期**。

批量生成只优化生产成本；不会自动获得需求、曝光和订单。

因此优先**有既有付费交易、平台履约、无需我们自己处理多数交付**的渠道。首期两个小实验，不四线全开：

| 轨道 | 角色 | 可售商品 | 为什么 | 首期产物 | 什么时候扩产 |
|---|---|---|---|---|---|
| A — Amazon KDP | **技术与收入验证主线** | 原创英文益智活动纸质书 | 平台按需印刷/配送；无需提前支付印刷和库存成本；题目可由代码生成且校验 | 一本有明确年龄/难度、真正不同题目、答案齐全的活动书（内页 PDF + 全幅封面 + 预览 + QA） | 账号具备准入、作品质量合格、真实上架；且存在真实成交或有证据的正向需求 |
| B — Adobe Stock | **低售后授权并行小样** | 可编辑原创 SVG 矢量素材 | 单份资产可多次授权；平台处理授权交易 | 5 件不同商业用途的 SVG + 预览 + 英文标题/关键词 + QA | 真实通过审核，作品有实际授权/曝光证据，能判定非重复创作方向 |
| C — Amazon Merch | 延后 | 原创透明底印花设计 | 平台负责制作/配送，但账户准入和设计竞争大 | V1 不生产 | A/B 测试结果有复用图案价值，再检查账号资格 |
| D — 免费工具站 | 延后 | 本地运行的免费网页工具 | 技术可复用，但收入依赖访问量/广告批准 | V1 不建站 | 已有可观察的真实搜索需求及流量获取方案 |

**路线调整原则**：A 的开源生产基础最明确，先测“能做出合格商品”；B 对低售后更有吸引力，并行少量投稿验证。**最终主线按真实商业数据重新选择**，不是预设 KDP 必定赚钱。零新增费用意味着**不买站外广告、不购买平台流量、不通过付费样书证明质量**。平台既有买家不代表平台承诺给新作者曝光。

### 2.1 首批内容选题原则

KDP 首批从迷宫算法切入，目标可定义为“英文儿童某年龄段的视觉与路径挑战活动书”**暂定选题，仅用于技术测试**。正式题材必须结合平台现售作品、买家用途、差评痛点与差异化重新筛选：不能以“普通迷宫合集 + 换封面”作为长期商业壁垒。年龄适宜性/难度须有明确规则和校验样本。

Adobe 首批分别做家居维修流程、家庭整理、服务流程等**用途互不相同**的原创可编辑矢量作品；不以换色、换朝向、近似图大量刷量。

## 3. 免费能力与费用防线（ZERO-SPEND GATE）

| 环节 | 允许 | 明确不允许/注意 |
|---|---|---|
| 选题、研究、标题、审稿 | 现有 GPT/ChatGPT Plus、开放额度内的研究/文件能力 | 付费调研数据库、外挂付费模型 |
| Coding、调试、审计 | Codex（Plus 可用额度）、现有 ChatGPT 工具、免费开源依赖 | Codex 额外 credits、独立 API 充值、第三方 AI 订阅 |
| 云端运行 | 仅已有免费额度内的 Codex 环境；必要时免费 GitHub Actions/可用执行环境 | 超出配额自动收费；不确保某云端长期/无限免费 |
| 图形 | 自写 SVG、Python/Pillow/ReportLab、SVGO、sharp；现有套餐内原生生图可用于辅助创意 | 付费素材站、商业字体、未授权图标与抄袭/描摹第三方作品 |
| PDF | ReportLab 或经许可审核的免费 PDF 工具 | 付费 Acrobat/设计软件 |
| 发布 | KDP 免费自助出版；Adobe Stock 按当期规则投稿 | 样书购买、付费推广、自动购买 ISBN、付费中转或商业代理 |
| 代码/资产保管 | 既有 Public 仓库放公开 SOP；必要时 GitHub Free 私有仓库存非敏感生产源码/作品 | 将私有商品和身份证明上传 Public；Private Actions 超额使用 |
| 收款与税务 | 使用平台支持的合规付款路径，先检查是否能够**零前置费用**建立 | 如果账户所在地、提现工具或税务流程产生必要新增费用，则该通道置 BLOCKED 并寻找其他**免费**合规渠道；不绕过身份核验 |

**硬停止**：遇到必须充值、升级套餐、输入付费 API Key、付费域名/服务器、Paid runners、短信代收验证码、购买素材/字体、样书费用等提示，立即 STOP 并报告。不要先消费再解释。

**注意**：GitHub Public Actions 标准托管 runner 一般免费，但 Public 不适合保存未发布的商业资产；Private 仓库有免费配额、超过可能收费，所以第一版**不建立自动定时云端批量任务**。本地/当前会话执行只在已有工具能力支持下进行，实际可用性逐项核实。

**额度耗尽**：停止当轮 agent 操作，保留状态和可复现文件，等待包含额度恢复；不得默认购买 flex credits 或虚构后台执行。不能承诺不用 API 时 GPT 自己跨日醒来持续制作，若无合适的计划任务/授权，必须由用户在可用会话触发。

官方说明：
- https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans
- https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories

## 4. 调研开源项目逐一落地：借鉴什么、不借鉴什么

截至 2026-10-26 已复核所列 GitHub 仓库存在及仓库级许可证；**尚未克隆执行、审计完整依赖/测试，不能声称已稳定运行**。

| 项目 | 许可证（仓库级） | 本项目取用 | 排除/待核查 |
|---|---|---|---|
| https://github.com/vijaxx/kdp-puzzle-engine | MIT；2026-07 最近推送；约 7 Stars | **KDP 主参考**：mazes.py、cover_maze.py、PDF 与 preflight 的设计，先审阅 tests/requirements | gen_themes.py 使用本地 Ollama（低配电脑负担大）；publish_tools 的 CDP 会话发布/改元数据脚本全部禁用；auto_factory 不启用无人值守；检查算法和布局正确性 |
| https://github.com/pdfme/pdfme | MIT | 后续模板编辑器、JSON 数据驱动 PDF 方案 | V1 不上完整网页编辑器 |
| https://github.com/py-pdf/fpdf2 | **LGPL-3.0** | 若 ReportLab 排版受限，可选 PDF 辅助模块 | 许可证及依赖义务需确认，勿误标 MIT |
| https://github.com/Wasserpuncher/sudoku | MIT，极小型仓库 | 后续独立数独测试参考 | V1 先做迷宫；不能把该项目当成熟生产依赖 |
| https://github.com/svg/svgo | MIT | **Stock 核心候选**：清理 SVG，保证没有无用/异常结构 | 自动优化不代表素材原创、可编辑或符合平台美术质量 |
| https://github.com/lovell/sharp | Apache-2.0 | SVG 渲染预览、透明底 PNG 导出、像素尺寸检查 | 审核依赖与运行环境；不要把 PNG 当 SVG 交付 |
| https://github.com/UmutHasanoglu/meta-gen | Apache-2.0 | 借鉴 Adobe CSV 字段、标题/关键词整理与去重 | 原项目使用 OpenAI/Gemini API；**不部署原有付费生成端点** |
| https://github.com/Ars-Mond/Attributor | AGPL-3.0 | 借鉴人工复核、关键词工作流的**思路** | V1 不拷贝其源代码进入商业私有模块，避免未计划的 AGPL 合规义务 |
| https://github.com/yakew7/DesignHub | MIT（第三方素材另授权） | Merch 阶段参考图案模板与 Mockup | 不复制内置第三方字体/图标直接售卖 |
| https://github.com/osmaar/openmerch-engine | MIT；小型项目 | Merch 阶段参考输出工艺尺寸 | 不引入 Docker/数据库重型服务 |
| https://github.com/iib0011/omni-tools | MIT | 未来免费工具站参考浏览器本地计算与单功能构建 | V1 不建免费站；无流量证据不部署 |
| https://github.com/CorentinTh/it-tools | GPL-3.0 | 只研究体验/分类思想 | 不直接复制 GPL 代码进计划闭源的工具站 |

**先做「读源码 → 跑原测试 → 最小适配 → 新增自有验证」**；禁止直接把 12 个仓库整合成巨型依赖链。第三方的 README 不是质量、授权和盈利的证明；若源代码、依赖许可或技术架构不合适，允许**自行重写最小功能**并记录原因。

## 5. 技术架构：GPT 创作，确定性代码执行，独立质检

~~~text
[GPT 选题/需求与原创设计 brief]
             │ 结构化输入（主题、买家、用途、尺寸、禁止项）
             ▼
[Codex 维护的免费 Python / Node 生产代码]
      ├── KDP: 迷宫/答案 → 内页 PDF / wrap cover PDF
      └── Stock: 原创 SVG → SVGO → sharp 预览
             │
             ▼
[确定性自动 QA：尺寸/越界/结构/重复/答案/哈希/文件清单]
             │ PASS
             ▼
[新上下文独立视觉+语义复核（GPT）]
             │ PASS / REVISE / UNKNOWN
             ▼
[投稿包：成品+元数据+权益说明+证据+审核状态]
             │
             ▼
[账号所有者在平台进行合法发布/审核确认]
             │
             ▼
[真实审核结果、销量与收入] → GPT 复盘 → 下一批/停止
~~~

设计要点：

- **模型不负责计数与数学正确性**：迷宫连通性、是否存在唯一路径、文件存在、页数、二维码/出血/尺寸等尽可能交给代码；无法机械验证的审美、市场需求、版权语义由 GPT + 人复核。
- **同一个模型生成和审稿不构成真正独立的能力证明**：尽量使用独立的新上下文只拿作品及规则进行审核，并显式允许 UNKNOWN；重要结构另用程序独立验证。
- 每一件资产有唯一 asset_id、源文件版本、随机种子、配置、许可证材料、SHA256、QA 报告、修改记录。只有通过 Gate 的版本可以进入下一阶段。
- 生产过程应能在中途断开后继续，不重新生成已锁定并验收的内容。内容变更导致下游文件失效时，仅重跑受影响步骤。

### 5.1 首批 KDP 的可复现最小流程

1. 选择一组用户/年龄/场景假设；实际查 10～20 本可比现售商品，记录定价、内容结构和真实差评/痛点（不得采集或照搬他人题目、封面）。
2. 首先审查 kdp-puzzle-engine 的许可证、依赖、测试与 mazes.py 的实际算法；要求不用 Ollama、浏览器登录和付费接口即可运行。
3. 以固定 seed + 唯一 ID 生成不同迷宫。程序独立求解并核验路径存在、路径唯一性、难度、重复度；记录算法定义和限制。
4. 排版英文标题/说明、正文、答案区、页码和版权信息。明确 PDF 装帧、页数、开本、出血和安全区，再生成内页和 full-wrap 封面。
5. 自动检查 PDF 文件可读取、页面大小/数量、字体嵌入、文本溢出、图形越界、裁切线、安全区；逐页预览，并由 GPT 独立视觉/内容复核。
6. 输出完整 submission_package：interior.pdf、cover.pdf、preview contact sheet、listing.md、rights_manifest.json、qa_report.json、build_manifest.json。若平台当前规则与本机假设不一致，**不得标 READY_TO_PUBLISH**。
7. 用户完成 KDP 账号/税务/收款/正式上传的必要人工步骤；记录真实审核状态与订单版税。**不购买纸质样书**，使用平台免费数字预览和导出的逐页检查；无法排除印刷问题时明确记风险，不虚称印刷实物验收。

KDP 官方参考：
- https://kdp.amazon.com/en_US/help/topic/GHKDSCW2KQ3K4UU4 （可免费出版）
- https://kdp.amazon.com/en_US/help/topic/G201834340 （按需印刷费用从版税扣除）
- https://kdp.amazon.com/en_US/help/topic/G200672390 （内容及 AI 生成披露）
- https://kdp.amazon.com/en_US/help/topic/GGE5T76TWKA85DJM （益智活动书通常不属于简单低内容书，但有例外）
- https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6/ （封面规范）
- https://kdp.amazon.com/en_US/help/topic/G202187850 （内页/出血规范）

### 5.2 首批 Adobe Stock 的最小流程

1. 从商业实际用途出发，产出 5 张差异明显的 brief（对象、使用者、版面用途、构图、禁止项），不要重复换色。
2. 用 GPT 设计并输出原创 SVG 元素与合理图层/组、可编辑节点、清晰语义命名；真实无权素材不得使用。可使用原生生图**辅助创意**，但不能把 raster 扩展名改成 SVG 伪装矢量。
3. 通过 SVGO 静态优化，sharp 渲染预览；机器验证 SVG XML、viewBox、基本尺寸、异常嵌入/外链、输出前后视觉差异；独立检查确实可编辑。
4. GPT 审核英文标题/关键词是否与作品真实内容一致、是否引入商标/人名/误导描述；按平台要求正确标 AI 生成属性和权利说明。
5. 输出每张 .svg、preview、CSV/metadata、QA、权利清单。用户本人提交；记录通过/拒稿及授权情况。

Adobe 官方参考：
- https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/vector-submission-overview.html
- https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-vector-submission-guidelines.html
- https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/adobe-stock-generative-ai-faq.html
- https://helpx.adobe.com/stock/contributor/get-started/manage-your-account/account-submission-guidelines.html

特别警示：图库允许 AI 生成内容**不等于**任何 GPT 输出都保证具备向第三方再许可所需的权利；提交前逐一核实当前服务条款、内容原创性及平台的 AI 标识要求。Adobe 对高度类似素材有反垃圾要求。


### 5.3 V1.1｜强制开发前置闸门：第一性原理 × 苏格拉底式提问 × GitHub 开源方案对照 × 审美研究

> 2026-10-26 用户新增的项目级核心约束。对本项目后续所有重要步骤生效：选题、技术选型、开发、调试、视觉、排版、生产、测试、投稿、数据复盘及后续重构。新增步骤也必须遵守。本次不修改仓库其他既有项目的锁定规则。
>
> 不允许先实现、再寻找理由；必须按顺序：**先审目标和必要性 → 提问反证 → 开源对照 → 比较决策 → 定义验收 → 正式制作 → 独立核验**。所谓“最佳方案”，仅指在零新增费用、Plus 现有额度、有限人力、版权和平台规则下，有证据支持且可逆的当前最合适方案，而非未经证明的绝对最优。

#### 5.3.1 STEP-0：每一步动工之前先写出前置决策卡（硬性）

**一、第一性原理审核：从挣钱所需的真实结果往回推**

- 问题究竟是什么、谁为其付费？本步骤对成交概率、作品价值、曝光、减少售后或降低成本哪个要素有直接影响？
- 如果直接删掉本步骤，商业目标会怎样？能否用最小代码、已有工具或 GPT 手工完成？避免为了技术复杂而复杂。
- 区分可核实事实、市场假设、技术假设、个人偏好；列出物理/平台/法律/许可/预算硬边界。
- 最小可验证产物是什么？成功必须有哪些客观证据？失败样例、边界条件与回滚方式是什么？
- 时间、模型额度、长期维护负担、复用度和新增现金支出分别是多少？额外现金预算恒为零。
- 明确现在做、暂时不做、绝对不做。避免因局部技术优化偏离长期真实净收益目标。

**二、苏格拉底式自问自答：至少回答以下八问**

必须按“问题 → 回答 → 实证/依据 → 反证或 UNKNOWN”记录，不能只写“已深度思考”。

1. 为什么用户需要这项成果、愿意付费的证据是什么？如果没有，这是怎样一个待证伪假设？
2. 为什么当前最应该解决的是这一步，而不是市场需求、包装美术、准入、曝光或交付质量？
3. 省略这一步会有什么后果？是否存在更简单、更容易验证的替代方法？
4. 有哪些不同路径？至少比较当前常规做法、开源借鉴、最小自研/人工+GPT 方案中适用的几种。
5. 有哪些事实会推翻我眼下认为最好的办法？是否存在反例、平台变动、隐形费用、版权问题？
6. 哪个假设最不可靠？能否用最便宜、最小的实验先验证它？
7. 如何独立证明真实有效？给出测试指标、失败样本、核查手段，而不是只让生成模型自评。
8. 未来每周重复生产，能否仍然保持质量、差异化、低售后及零成本？最可能产生哪个新瓶颈？

答案不足标 UNKNOWN，说明下一条可执行的核实行动；不能把主观推断写成已验证。

**三、每一步都调查 GitHub 开源项目（不是只调用旧清单）**

- 基于本步骤的实际功能重新检索 GitHub，同步寻找相似问题的成熟开源设计、实现、评测与失败案例；原则上比较 2–3 个候选，不存在合适候选则记录关键词、检索时间、找不到的结果，不可虚构。
- 记录每个候选的准确 URL、项目定位、更新时间或 commit/release、许可证、示例与测试、相关源码位置、依赖和运行成本、维护状况、限制/缺陷。
- 优先认真阅读直接相关的源码、示例和测试；可以免费实际运行就先跑最小 smoke test；不把 README 描述、GitHub Stars 或效果图视为可靠性证明。
- 比较“直接复用、只借鉴方法/视觉设计、自研最小实现、不采用”四种结论。保留被否决项目及理由。
- 必须核查商用权限：仓库 LICENSE 不等于其字体、图片、图标、样本、素材、数据均可再分发。GPL/AGPL、专有素材及依赖另行核验。
- 无法访问代码或缺少证据时标为 BLOCKED_RESEARCH；可以做低风险本地探索，但不声明完整比选完成，不越过正式商业发布 Gate。
- **严禁“先找个高星项目就复制”**；借鉴成果须证明针对本步骤实际提高了可靠性、产出质量或效率。

**四、备选方案比较与选型**

统一比较：实际买家价值、零新增费用、可验证性、工程稳定性、审美水平、开源许可、平台审核风险、Plus 额度依赖、操作复杂度、后期维护与可复制性。先剔除硬约束冲突方案，再给出当前首选、次选、拒绝原因和何时换方案。对结果不确定的选项，先用最小可逆实验验证；不要用貌似精确的评分代替可靠证据。

**五、STEP-0 前置验收**

只有完成以上四项，且形成明确目标、候选开源方案、首选理由、实测方法、停机条件及费用/授权检查的记录，才能标记 PRECHECK_PASS，才允许进入该步骤正式制作；其余状态为 PRECHECK_UNKNOWN / PRECHECK_BLOCKED。轻量的机械子步骤可以合并在父步骤的卡片中，不需要重复写长报告；但新技术选型、新题材、新设计风格及高风险修复绝对不能跳过。

#### 5.3.2 VISUAL-0：凡涉及审美的步骤，都必须对照开源项目并建立样板

**适用范围**：KDP 书籍封面、整本内页、迷宫图案、插图，Stock 矢量素材、预览图，Merch 印花，未来网页工具 UI、营销图和信息图。程序能生成 SVG/PDF 不代表作品美观、能卖或符合平台要求。

1. 先锁定目标用户与应用场景：儿童/成年人、印刷/移动端、封面缩略图/原大图、行业买家实际用途；拆成可观察的视觉目标。
2. **至少研究两个与该任务直接相关的 GitHub 开源视觉/排版/设计项目**：阅读实际 examples/demo/设计系统/源码中的排版或几何规范，同时参照目标商业平台上真实同类商品的市场展示和平台技术规范。开源工程是学习对象，真实市场是商业对标；两者不可互相替代。
3. 从参照提取可审查的设计规范：信息层级、构图比例、网格与留白、配色、字体与行距、图形笔画与形状语言、视觉密度、风格一致性、原创辨识度、可编辑性、印刷和缩略图可读性；解释为什么选择该风格。
4. 在正式批量生产前制作 **至少一套完整视觉样板**，合适时生成 A/B 两种排版；对照参照项目及真实使用场景检查，而不是口头声称“高端、大气、精致”。
5. 在新上下文使用统一 rubric 独立审核：信息层级 / 构图均衡 / 阅读清晰 / 视觉一致 / 差异化原创 / 平台适配 / 商业用途（分别 PASS/REVISE/UNKNOWN，写具体原因）。重大视觉缺陷即 REVISE。
6. KDP 封面同时检查平台缩略图与实际印刷尺寸，内页逐页检查并模拟灰度阅读；Stock 素材检查缩放前后细节和 SVG 节点编辑性。保留真实图像/PDF 可视检查证据，不把代码检查替代视觉验收。
7. 严禁直接临摹竞争对手付费商品，不把开源 demo 中的字体、图标、插图未经单独许可核实就当作自己的可再授权素材。
8. 若找不到适合该品类的美术参照，先继续研究与测试；不允许闭门定风格后直接批量生成。

**已核实存在的 GitHub 审美与排版参考库（2026-10-26 仓库级许可，使用前需核查具体素材/依赖）**

| 项目 | 仓库级许可 | 在本项目可参考的能力 | 使用边界 |
|---|---|---|---|
| https://github.com/penpot/penpot | MPL-2.0 | 版式、组件、一致性与视觉设计流程，封面/信息图/网页 UI | 学习规范，不要求部署、不直接出售示例 |
| https://github.com/typst/typst | Apache-2.0 | 出版级版面、字体层级、页边距、数学及 PDF 排版原理 | 仍要核验 KDP 尺寸、出血与字体许可 |
| https://github.com/fabricjs/fabric.js | MIT | 矢量元素、画布编辑、导入导出、构图一致性 | SVG 导出不自动满足图库美术标准 |
| https://github.com/yakew7/DesignHub | MIT（第三方素材另授权） | 排版配色、Mockup 和图案输出工作流 | 不直接转售项目内第三方字体与图标 |
| https://github.com/carbon-design-system/carbon | Apache-2.0 | 界面层级、对比度、信息密度、交互统一 | 不拿企业 UI 风格硬套儿童益智书封面 |
| https://github.com/tabler/tabler-icons | MIT（具体资源再复核） | 图标笔画、负空间与统一形状语言的设计方法 | 不将他人开源图标直接当 Adobe Stock 原创商品 |

在具体制作阶段仍必须按当前任务继续搜索更精确的项目和审美参考。上表仅为可开始学习的参考池，不代表已经证明适合所有视觉产品。

#### 5.3.3 每个执行步骤必须留下的最小决策记录

以下字段为标准，可存在当前交接/私有工作区；**模板不是实际完成证据**。

~~~yaml
step_id: "G1-KDP-01"
goal_and_value: "要解决的真实商业/技术问题"
locked_rules: ["zero_new_cash_spend", "plus_only", "commercial_rights"]
first_principles: "必要性、最小有用产物、可反证的验收条件"
socratic_qa:
  - question: "为什么这是当前最重要的瓶颈？"
    answer: "..."
    evidence: []
    counterevidence_or_unknown: "..."
github_research:
  keywords: []
  checked_at: "YYYY-MM-DD"
  candidates: []
  source_and_license_checks: []
alternatives_and_tradeoffs: []
selected_approach_and_reason: "..."
switch_or_stop_triggers: []
visual_review:
  required: false
  visual_open_source_references: []
  platform_market_references: []
  sample_comparison_and_quality: "N/A / PASS / REVISE / UNKNOWN"
cost_gate: "PASS / BLOCKED"
rights_gate: "PASS / UNKNOWN / BLOCKED"
precheck_status: "PRECHECK_PASS / PRECHECK_UNKNOWN / PRECHECK_BLOCKED"
build_and_test_evidence: []
final_status: "NOT_STARTED / PASS / REVISE / BLOCKED"
next_step: "..."
~~~

**统一原则**：每次先记录为何选择当前路径，执行后再追加实际文件/测试/审美证据。生成者与审查者分开上下文；可以用代码验证的事实绝不由模型主观判断。单个阶段失败只回滚相关部分。没有 STEP-0 通过不正式动工；视觉类没有 VISUAL-0 通过不定稿，不批量生产，不称为可上架商品。


## 6. 五段 Stage Gate 与明确状态机

**跨阶段强制规则**：G0–G4 每个重要子步骤都须先取得 §5.3 的 STEP-0 PRECHECK_PASS；涉及视觉、排版、风格的步骤还需 VISUAL-0，二者不能替代实际技术测试、版权核查、平台审核与真实收入证据。

状态：IDEA → RESEARCHED → BUILDING → TECH_QA_PASS → CONTENT_QA_PASS → SUBMISSION_READY → SUBMITTED → APPROVED / REJECTED → SOLD / NO_SALE。任何阶段可进入 BLOCKED 或 REVISE；未获实际审批不能声明 APPROVED。

| Gate | 阶段产物 | 必须有的客观证据 | 失败动作 |
|---|---|---|---|
| G0 免费与权益预检 | 题材、市场假设、依赖清单、预算表 | cost_new_cash=0；开源/字体/素材许可已登记；平台账号通道可用性已检查或标 UNKNOWN | 收费/许可不可解 → STOP；未知 → 不进入正式投稿 |
| G1 生产可复现 | 可运行代码、构建命令、真实文件 | 版本号、seed、SHA256、实测命令/退出码；不能仅有 README | 修最小模块 |
| G2 技术质量 | PDF/SVG、可读预览、机械 QA | 机器报告 PASS；迷宫解与重复性；PDF 尺寸/出血；SVG 编辑性 | 只重跑失败资产 |
| G3 内容与合规 | 独立审稿记录、原创性/AI 标识 | 新上下文审稿、引用依据、授权台账；不允许“AI 觉得没问题”作为唯一证据 | REVISE / ESCALATE |
| G4 上架与商业验证 | 审核记录、净版税、销量 | 平台审核邮件/后台状态（隐私脱敏）、订单/版税真实数据 | 拒稿优化一次；无收入时停止盲目扩量 |

状态不得凭计划文本直接升级。每次单阶段结束的交接只带：Result / Evidence / Locked Rules / Open Issues / Next Action。

## 7. 数据协议：每件商品必须留下证据而非只有图片

以下是**未来生产文件的字段规范示例**，不是声称现在已经生成该文件：

~~~json
{
  "asset_id": "KDP_MAZE_TEST_001",
  "channel": "KDP",
  "version": "0.1.0",
  "status": "BUILDING",
  "theme": "TO_BE_VALIDATED",
  "buyer_hypothesis": "TO_BE_VALIDATED",
  "source_repo_commit": null,
  "seed": 20261026,
  "dependencies_and_licenses_checked": false,
  "third_party_rights_checked": false,
  "extra_spend_usd": 0,
  "paid_api_calls": 0,
  "qa": {
    "tech": "NOT_TESTED",
    "content": "NOT_TESTED",
    "platform_spec": "NOT_TESTED"
  },
  "outputs": [],
  "evidence": [],
  "submitted_at": null,
  "approved_at": null,
  "orders_count": null,
  "actual_royalties": null
}
~~~

测算必须区分：
- 列表价格 != 作者版税；纸书版税需扣印刷成本；实际提现还涉及平台/收款/税务规定。
- 平台曝光 != 销售；审核通过 != 可持续卖出；下载量不能用估算替代。
- 对于新资产，按周记录：候选数、完成数、通过技术检查数、实际提交数、通过审核数、获得授权/订单数、实际版税、被拒原因、每件制作时间。
- 健康指标：每件已上架资产累计版税、过去 30 天每件活跃资产版税、全部资产中的有收入比例、退款/拒稿/返工率、人工介入小时数。
- **不允许用宣传性的「预计月入」作为真实成绩。**

## 8. V1.1 初始 30 / 60 / 90 天设想（最新顺序见 §12）

本安排是**在额度和真实操作许可的条件下的实验目标**，不是保证在日历上自动运行。

### Day 1–7：验证原项目与环境
- 检查 A/B 投稿地区、平台账户与合法收款可行性；可能产生新增必要费用的渠道立即标 BLOCKED，允许先做技术样品但不承诺上架。
- 读取 kdp-puzzle-engine 的真实源码、requirements、LICENSE、tests；运行最短命令，建立复现报告；选择极简迷宫题型。
- 先完成 3 道可机器验证的不同迷宫 + 其独立求解，证明算法正确。
- **退出标准**：免费执行环境可用、真实生成结果、测试有输出、已知依赖成本为零。

### Day 8–21：做一个完整 KDP 样本 + 五个 Stock 小样
- 根据具体市场调研决定英文目标读者和差异化内容（不是只做低价值泛用迷宫）。
- 把迷宫扩展成完整合格内页、答案、封面、接近实物体验的 PDF 预览；出具 QA。
- 制作 5 个独立商业场景 SVG，导出预览与元数据，并核对官方 SVG 投稿规范。
- **退出标准**：按 G0–G3 验收，留下原始证据；只完成文件不视为可卖。

### Day 22–30：真实上架与审核
- 由平台账号所有者完成必要的实名、税务、收款及发布确认；不自动操作登录会话。
- 记录上架审核、拒稿和修复原因；**首要商业事件是实际首单或首次授权**，而不是发布成功。
- **退出标准**：至少完成真实提交/有审核结果，或明确记录客观 BLOCKED 原因。无收入如实标为 NO_SALE。

### Day 31–60：只围绕正向证据迭代
- 已获得实际订单/授权的方向：制作少量不同用途新作品，比较每件净版税与每件时间成本。
- 已上架但无订单：优先检查选题/呈现/市场需求，而不是继续自动批量生产。
- 拒稿：先解决权利、内容与技术，避免积累账号风险。
- 每周一次轻量复盘，由 GPT 输出「继续 / 修正 / 暂停 / 换渠道」。

### Day 61–90：决定是否扩产
- **可扩产条件**：明确可重复的制作质量 + 真实用户付费证据 + 低售后工作量 + 不增现金支出。
- **不扩产条件**：无授权/订单、连续拒稿、原创质量差、账号资格不可行、人工时间显著超预算。
- 如果两条轨道均失败，保留生产基础能力，复盘原因，另选可免费验证的垂直数字资产渠道，而非投入付费广告强行推动。

## 9. AI / 人 / 平台职责边界

| 任务 | GPT / Codex 能做 | 用户必须保留的动作 | 平台负责 |
|---|---|---|---|
| 选题与市场研究 | 搜集证据、竞品分析、提假设 | 必要商业方向确认 | 提供公开商品页面 |
| 内容/程序/排版 | 原创设计、代码、PDF/SVG、校验、批量模板 | 无需逐件手工制作；抽查高风险项 | 无 |
| 上架准备 | 商品描述、关键词、授权/AI 披露检查清单、投稿包 | 确保申报真实 | 提供审核工具 |
| 正式发布 | 在能力/权限范围内协助准备，不越过人工控制 | 账户注册、实名、税务、收款、平台要求的同意/最终提交 | 审核、展示、交易 |
| 售后 | 可以准备解释/修正方案 | 版权争议/高风险账号事项必须本人处理 | 平台处理其明确承担的配送/普通交易服务 |
| 定期续产 | **被触发时**运行既定生产与复盘任务 | 发起新会话或使用当前套餐内可用且授权的计划任务 | 记录真实销售 |

**不作出「完全无人值守/终生零售后/必定月赚一万」的承诺。** 产品开发由 AI 主要承担，不代表 GPT 能脱离当前会话一直在后台工作。

## 10. V1.1 历史技术启动指令（最新启动见 §12.15）

**注意：本段属于历史技术参考；现已调整为首先执行 §12.15 的 S0/S1。**

**请按本文件继续，不得越过 Gate：**

> 读取 10_DIGITAL_ASSET_FACTORY/PROJECT_MASTER_PLAN_V1.md。仅使用 ChatGPT Plus 包含的 GPT / Codex / 已开放 Work 用量、免费且许可证明确的开源工具；新增现金支出必须为零。不得调用 OpenAI API 或其他付费 AI API，不得购买 credits、增订阅、购买素材/字体、建付费服务器或绕过平台登录。
>
> **每一个正式开发步骤必须先做 §5.3 的 STEP-0：第一性原理拆解、苏格拉底八问自答、GitHub 候选项目搜索和源码/测试/许可对照、备选方案反证与选择。视觉类步骤还要做 VISUAL-0（至少两个开源审美项目 + 平台竞品展示 + 视觉样板与对比验收）。未过 PRECHECK_PASS 不动工，未过 VISUAL-0 不定稿。**
>
> 从阶段 G0/G1 开始：审核 vijaxx/kdp-puzzle-engine 的 LICENSE、requirements、mazes.py、preflight.py、cover_maze.py、现有测试与依赖风险；明确禁用 Ollama 和 publish_tools/CDP 自动登录发布。实际运行能用的最短原版测试，记录代码版本与命令输出。以单个迷宫为最小单元，建立独立求解与唯一解验证。若源码有问题，重新实现最小 Python 模块并给出原因。
>
> 只交付实测证据，不急于完整上架、不批量生产、不触发其他路线。达到 G1 才可进入全书 PDF/封面阶段；质量检查通过后再试做 5 件 Stock SVG。保持所有原有项目文件不变；必要新增生产文件优先存用户授权的私有工作区，Public 主仓库只同步非敏感方法与脱敏验收记录。最后报告当前状态、实际生成物、测试结果、费用核查、阻塞项与下一 Gate。

## 11. 当前事实、风险与最终验收

**已验证（截至 2026-10-26）**：
- main 分支原有结构、Public 可见性、可复用的 08 Agent Gate 与 09 Plus-only 原则。
- 12 个候选开源仓库存在，并查看其仓库级许可证；重点 kdp-puzzle-engine 的 README 和 LICENSE 已核查：它确实包含题目生成、封面/预检、Ollama 词表及 CDP 账户操作组件。
- 官方文档确认：Plus 与 API 分开计费；Codex 受套餐用量限制；KDP 免费出版但纸书印刷从版税扣除；Adobe 接受符合规范的 AI/矢量文件，需权利与 AI 标识。

**尚未验证 / 不能宣称完成**：
- 任一候选代码可在当前云端/本地环境成功运行；
- 数独/迷宫生成、独立 QA、PDF 与 SVG 成品的真实质量；
- 用户所在地/账户的 KDP、Adobe Stock 投稿资格、税务与收款路径是否为零前置费用；
- Adobe 对提交作品实际审核结果与 KDP 实际上架状态；
- 任何销量、授权、收入、实际净利润及每周人力投入。
  
**本阶段完成条件**：GitHub 中存在这一份清晰、独立、可执行的方案文件，并可被 Work/Codex 作为单一入口读取。**文件已存在 ≠ 商业模式已验证。**

---
核查日期：2026-10-26；官方规则与工具额度会调整，每次正式投稿/部署前须再次查官方最新政策。

## 12. V1.2｜完整商业项目路径：S0–S8（2026-10-26）

> 本节为当前唯一权威的阶段执行顺序。与 §8 原始时间安排或 §10 历史启动提示发生冲突时，**以本节先商业验证、后生产开发的顺序为准**；§0 零新增现金预算与 §5.3 每步骤 STEP-0、视觉步骤 VISUAL-0 的最高优先级规则不变。更新方案不代表系统已开发或有实际销售。

### 12.1 第一性原理修订与核心业务假设

真正要获得的不是软件、文件或作品数量，而是**低售后、可持续且可验证的实际净收益**。只有渠道可合法收款、买家有购买动机、商品有差异化、质量达标、商品真正上架且被购买，才存在收入。复杂自动化只能降低已验证商品的边际制作成本，不能凭空创造市场需求。

因此首先做平台资格/零成本可行性与选品，再审计开源、设计样板、制造产品、上架与销售。初期 A 路线为 Amazon KDP 原创益智活动书、B 路线为 Adobe Stock 可编辑原创 SVG 素材；先完整跑通 A 的一件商品，B 只做 5 件不同用途样品。若 S0/S1 结果支持 B 更有商业可能，应调整优先级并写明证据。Merch 和免费广告工具站暂不做。

零新增费用范围：禁止购买 API、其他 AI 会员、额外 credits、插件、软件、服务器、域名、字体/素材、广告、样书。Plus、Codex/Work 的可用额度有上限；不足则停机交接。KDP 按需印刷的出版不需预先垫付成本，但印刷会从每次版税扣除；平台标准版税扣减、必要税费需在收入测算如实列示。身份、税务、合规收款与最终平台审核不可由代码绕过。现有 Public GitHub 只放计划/许可与脱敏方法，不公开待售创意和敏感信息。

### 12.2 总流程与状态控制

~~~text
计划与零费用锁定
  ↓
S0 渠道和收款可行性 → 不可行则 STOP/换合法免费渠道
  ↓
S1 客户购买问题与竞品证据 → 不成立则改选题
  ↓
S2 STEP-0 + 同题开源比选 + 最小源码运行 → 不合格则换方案
  ↓
S3 VISUAL-0 + 真实市场视觉参照 + A/B 样板 → 审美不通过不批量
  ↓
S4 最小可重现生产代码 → 失败只修影响模块
  ↓
S5 完整商品 + 技术/内容/美术/许可四重 QA → 不通过不投稿
  ↓
S6 本人授权上架 + 平台真实审核 → 拒稿按原因修复
  ↓
S7 真实订单/版税/售后/人工时间记录 → 无需求则暂停扩产
  ↓
S8 仅复用经市场证明有效的商品路线
  └── 下一批重回 S1，仍需每步骤 STEP-0，涉及视觉重过 VISUAL-0
~~~

**单步骤执行协议**：先读取原目标和锁定约束 → 第一性原理拆解 → 苏格拉底至少八问自问自答与反证 → 当次 GitHub 研究 2–3 个相关候选、实际源码/examples/tests、LICENSE 和第三方素材权利 → 比较开源复用、最小自研、GPT 人工方案 → 提交推荐路线与可证伪验收条件 → 视觉任务额外做两个开源审美项目+平台真实商品对标 → 运行最小实验 → 机器测试与独立审稿 → 保留文件、SHA256、状态与交接。简单机械子动作可共享父级 STEP-0，重要选题/架构/视觉变更不可跳过。

### 12.3 S0：先证明渠道具备“可兑现收入”能力

**目标**：不要制作一百件商品后才发现无法开作者账户或提现。

S0.1 从 KDP 和 Adobe 官方核实注册/地区/年龄/税务/收款/提现和协议条件，不能根据浏览器 IP 或聊天推断本人国籍、所在地和账号资格；用户敏感资料绝不写入 Public GitHub。S0.2 核实真正的零前置费用：KDP 免费出版和版税中的印刷成本；Adobe Stock 的标准授权/提现要求；任一新增必需现金支出触发 BLOCKED。S0.3 核实 KDP 的 AI-generated 与 AI-assisted 申报区别、Adobe 的生成式 AI 投稿和再授权义务。S0.4 核实 Work/Codex 包含额度以及免费源码存储方案。S0.5 输出 CHANNEL_FEASIBILITY，分别标 ELIGIBLE / UNKNOWN / BLOCKED，注明官方 URL、查询日期、尚未核实项。

**第一性反问**：“平台免费出版=一定能提现？”不成立；必须满足真实收款与税务条件。“能否用开源脚本绕过账号审核？”不能。

**退出 Gate**：至少有一条经充分核实的合法、零前置现金渠道；均 UNKNOWN 时只可进行限量可复用的技术学习，不能承诺上架或商业收益。

### 12.4 S1：先找买家和付费理由，再锁定商品

S1.1 KDP 对标至少 10 本有相同读者和用途的真实上架作品；Stock 对照约 10 件同类商业素材，保留公开链接、日期、真实价格/页数/展示、评论和可观察的问题，**不从评价数虚构销量**。S1.2 定义 Buyer（谁买）、Job（想解决什么）、Occasion（什么时候需要）和现有替代方案。S1.3 至少提出两条可能有真实差异化的路线，并使用第一性原理反证“普通迷宫书”“通用图标集”是否值得做。S1.4 输出单一 PRODUCT_BRIEF：目标受众、独特利益、内容规格/年龄/语言、定价区间假设、视觉目标、不可复制内容、待验证假设。S1.5 若需求证据不足，改细分选题，不进入商品批量制造。

**出口**：有链接支持的购买场景和一个具有可测试卖点的具体产品定义。**没有收入与市场证据，不能仅凭“我能生成”判定这个主题有潜力。**

### 12.5 S2：开源学习、选型与最小运行证据

S2.1 先完成 STEP-0（第一性原理+八问自答+反证）再决策。S2.2 KDP 检查 vijaxx/kdp-puzzle-engine 的 LICENSE、requirements、mazes.py、cover_maze.py、preflight.py、tests、样例和实际依赖；禁用其本地 Ollama 模型、无监督 auto_factory、publish_tools/CDP 会话自动登录。S2.3 同题比较 typst/typst、pdfme/pdfme、py-pdf/fpdf2 等排版技术；Stock 比较 svg/svgo、lovell/sharp、fabricjs/fabric.js、DesignHub；meta-gen 只借鉴元数据，不启用付费 API。S2.4 实际读取源码、examples、issues、测试及许可证；最小 smoke test 记录 commit、命令、退出码、SHA256、文件。S2.5 选择 REUSE / LEARN_ONLY / MINIMAL_REWRITE / REJECT 并说明弃选理由、版本风险、回退条件。

**出口**：成本为零、真实运行可复现、版权/许可风险已识别。GitHub Stars 和 README 不能替代运行测试。

### 12.6 S3：视觉体系先过样板，再允许批量

**视觉范围**：KDP 封面/内页/答案/插图，Adobe 素材构图与预览、以后网页工具 UI 和营销图。必须启动 VISUAL-0，不能闭门造车。

S3.1 锁 PRODUCT_SPEC（KDP 目标读者、语言、难度、总页数、开本/纸张/出血、完整封面；Stock 文件格式、画板、RGB、分组与实际商业用途）。S3.2 KDP 对照 typst/typst、penpot/penpot 和谜题引擎的设计例子，Stock 对照 fabricjs/fabric.js、yakew7/DesignHub、Penpot；**至少两个任务相关的开源项目**，阅读真实 demo 与设计原理。S3.3 同时对照目标平台真实同类商品，提取网格、留白、配色、字体层级、线条、缩略图辨识、阅读/编辑体验，且不复制竞争对手。S3.4 先出一套封面+代表性内页+答案的视觉样板，或 Stock 的 SVG 样板；适合时做 A/B。S3.5 GPT 在新上下文独立评估清晰度、层级、平衡、风格、差异化、商业用途与平台规格，实际渲染查看文件；缺陷修复后再冻结设计。

**退出 Gate**：SPEC_LOCKED + VISUAL_PASS + 权利检查通过；否则只修样板。注意 KDP 正式封面必须按实际页数产生背封+书脊+正封的完整 PDF，Adobe SVG 必须真正可编辑、分组合理并按最新画板规范检查。

### 12.7 S4：Codex 最小生产引擎（不建大系统）

S4.1 唯一输入合同为 brief、spec、seed、视觉规范、合法素材/字体与许可证；输出真实文件、预览、build_manifest、SHA256、测试报告。S4.2 KDP 先单个迷宫，独立求解器验证路径/唯一性/难度，再渲染答案、内页、整书、全幅封面。S4.3 Stock 先一个原创商业场景，生成分组 SVG、SVGO 清理、sharp 预览，机器检测异常外链、文字、结构、重复性和优化前后偏差。S4.4 做固定种子回归、错误输入、边界样本及自动 QA；不要无必要引入 Web 后端、复杂数据库、Docker、大型本地 AI 和收费 API。S4.5 修正仅重建受影响的工件，避免整批重做。

**退出 Gate**：真实文件可打开、正确、可复现、无额外支出；技术通过并不意味着商品质量或销售通过。

### 12.8 S5：完整商品交付与四重验收

**A 线 KDP**：一整本原创、适龄、真正不同题目和正确答案的活动书；交付 interior.pdf、full-wrap cover.pdf、逐页/关键页预览、英文 listing、权利清单、QA、构建说明。按 KDP 官方纸书规格检查完整封面、出血、书脊、内页边距、字体、图像与单页顺序。未买实物样书时，诚实说明纸质成品未亲自检验，依赖数字预览和文件 QA。

**B 线 Stock**：首批仅 5 件互不雷同的原创可编辑 SVG，逐件预览、英文标题/关键词、原始文件编辑性证明、AI 标记和授权检查。严禁简单改色、翻转、换比例视为新商品。

**强制四重 QA**：
- TECH：文件存在/可读、PDF/画板技术规范、字体、结构、谜题答案与唯一性、重复性、哈希和可追溯性。
- CONTENT：真实买家用途、文案语言、题目/答案、内容完整性。
- VISUAL：外部开源设计参考、缩略图/原尺寸/灰度与可编辑性、独立审美评估。
- RIGHTS/POLICY：源码/字体/图标/素材许可及生成式 AI/平台提交要求。

**退出 Gate**：四层 PASS 才是 SUBMISSION_READY；任何 UNKNOWN/REVISE 不投稿。

### 12.9 S6：合法上架、审核和定价

S6.1 GPT 生成平台允许的标题、描述、关键词、适当分类、价格与实际版税估算依据；禁止伪造销量或评价。S6.2 用户本人完成账号身份、税务、收款、平台协议与必要发布确认；GPT/Work 只能在获授权且产品支持的操作范围内协助。S6.3 使用平台免费预览/投稿入口，记录真实 SUBMITTED/APPROVED/REJECTED 与拒稿原因、商品页、实际日期。S6.4 审核失败只按原因有限修复，遵守平台新书提交限额及 Adobe 反相似政策，不批量绕过审核。

**退出 Gate**：真实审核/上架证据或明确的客观阻塞；“已上传”不等于“已批准”，也不是收入。

### 12.10 S7：首单、版税、维护时间与证伪

S7.1 每周记录 asset_id、平台批准日期、公开可查的展示数据、真实订单/授权数、实际净版税（平台费/印刷及税费另列）、退稿/退款、人工时长。S7.2 证据分级 E0 文件生成→E1 品质合格→E2 实际上架→E3 首次真实收入→E4 多位不相关买家/跨批次复购或授权→E5 可持续正向单位经济性。只有 E3+ 才证明有人付费；E4/E5 才考虑扩大生产。S7.3 分别诊断没曝光、有人浏览却不买、质量投诉、收入长期停滞；每次只改最有可能有效的一个关键变量。S7.4 决策 CONTINUE / IMPROVE / PIVOT / STOP 并保留原因。30 天无单不能自动证明长期无需求，但也绝不能靠无限发更多产品掩盖问题。

**退出 Gate**：真实商业数据和明确决策，不用预测收入伪装已盈利。

### 12.11 S8：先证明复制有效，再按小批次持续生产

S8.1 只把验证成功的市场定位、视觉系统、题目算法/SVG 模块、独立测试、元数据处理固化成模板，避免新的题材重新发明全部系统。S8.2 初期每周一次市场复盘与最多一小批差异化新样品，由当前会话/实际可用的 Work、Codex 执行；每个新主题、画风、技术改动仍先 STEP-0，视觉变化重做 VISUAL-0。S8.3 追踪旧商品贡献、新商品边际版税、工作时长、质量、拒稿与退款；库存扩大但收入不升，则 STOP 扩产。S8.4 不承诺无需额外 API 的 GPT 跨日无人值守运行，用户授权触发下一轮；零成本的脚本只负责确定性任务。S8.5 多个真实周期证明收入与售后可控后才能宣告 REPEATABLE_BUSINESS_VALIDATED。

### 12.12 两轨技术/审美复用矩阵

| 内容 | KDP（完整首件优先） | Adobe Stock（5 件小样） |
|---|---|---|
| 买家价值 | 独特、适龄、可解且有正确答案的纸质活动书 | 可用于实际设计任务的清晰原创矢量 |
| 主要开源 | vijaxx/kdp-puzzle-engine；typst、pdfme/FPDF 备选 | svg/svgo + lovell/sharp；Fabric.js 备选 |
| 审美参考 | Penpot、Typst、真实 KDP 同类商品 | Fabric.js、DesignHub、真实 Adobe 同类商品 |
| 必要产物 | 整书 PDF、全幅封面、答案、元数据和 QA | 5 个独立 SVG、预览、元数据和 QA |
| 不能自动证明 | 题目有市场、印刷真实效果、收入 | 投稿资格、独立授权权利、客户购买 |

### 12.13 未来建议生产目录（此轮不创建）

~~~text
当前 Public 主仓库：
10_DIGITAL_ASSET_FACTORY/PROJECT_MASTER_PLAN_V1.md  # 唯一持续更新的公开计划

未来需要时再授权创建 Private / 本地工作区：
digital-asset-factory/
├─ briefs/             # 买家问题与竞品证据
├─ research/           # 开源源码/测试/许可证与市场研究
├─ design-system/      # 视觉参考、规范、自有原创样板
├─ engines/kdp/        # 生成、独立求解、PDF/封面
├─ engines/stock/      # SVG、优化和预览
├─ qa/                 # 四重 QA、回归、独立 Judge
├─ products/           # 待售商业私有文件
├─ receipts/           # 脱敏平台审核、销售证据
└─ state.json          # Gate 状态/回滚记录
~~~

Private GitHub 的免费 Actions 有使用额度，超出可能计费；不要把存储商用资产和 Public 无限免费 Actions 混为一谈。

### 12.14 建议 90 天阶段窗口（以 Gate 为准而非时间自动执行）

| 工作窗口 | 主要阶段 | 必须拿到的证据 |
|---|---|---|
| Week 1 | S0 + S1 | 官方准入/收款/预算状态、10+ 同类竞品记录、1 份真实商品 Brief |
| Week 2 | S2 + S3 | 开源项目源码/许可/最小运行日志、至少 2 个开源美术对照、A/B 样板 QA |
| Week 3 | S4 + S5 | 实际可重复运行的生成模块、正确性测试、完整可投稿 KDP 包 |
| Week 4 | S6，视准入再做 Stock 五件 | 真正上架/拒稿凭证和首批 Stock 原创小样 |
| Days 31–60 | S7 | 真实订单/版税或无单数据、一轮小范围可证伪迭代 |
| Days 61–90 | S7 → S8 或 PIVOT | 可重复商业证据和是否扩产的明确信号 |

窗口可随平台审核、账户条件、工作额度和实际用户数据调整；不是无条件限时交付或自动后台运行。

### 12.15 完整路径的总验收标准和第一轮启动指令

**分开四种不同成功**：流程完善 ≠ 代码跑通；代码跑通 ≠ 商品好看且可合法上架；商品上架 ≠ 有人付费；有一单 ≠ 已形成可重复的持续收入。必须分别标 PLAN_READY、TECH_VALIDATED、PRODUCT_APPROVED、SALES_EVIDENCE、REPEATABLE_BUSINESS_VALIDATED。

**下一轮唯一优先任务是 S0/S1 商业预检，不是先写迷宫引擎**：

> 读取此文件 §0、§5.3、§12，执行 S0 平台准入、税务/收款合法性、zero-spend、AI/版权规则核查，以及 S1 买家/竞品与差异化研究。每个子步骤先提交第一性原理审核、苏格拉底八问、可用开源比选和可反证证据。不得要求用户提供个人敏感信息到 Public GitHub，不能推断账号资格；无法核实的标 UNKNOWN。产出至少一个有公开证据的商品 Brief、两个渠道 ELIGIBLE/UNKNOWN/BLOCKED 状态和下一 Gate 决策。暂不进行 S2–S5 的批量开发，不增加任何付费。结束时反馈真实证据/未解决问题/唯一后续动作。

**当前真实状态**：PLAN_V1_2_READY；S0_NOT_EXECUTED；S1_NOT_EXECUTED；TECH_NOT_TESTED；PRODUCT_NOT_BUILT；NOT_SUBMITTED；NO_SALES_EVIDENCE。

**当前官方参考**：
- KDP 免费出版：https://kdp.amazon.com/en_US/help/topic/GHKDSCW2KQ3K4UU4
- KDP 印刷/版税：https://kdp.amazon.com/en_US/help/topic/G201834340
- KDP AI 内容：https://kdp.amazon.com/en_US/help/topic/G200672390
- KDP 封面与打印规范：https://kdp.amazon.com/en_US/help/topic/G201857950
- KDP 内容质量/重复：https://kdp.amazon.com/en_US/help/topic/G200952510
- Adobe SVG：https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/vector-submission-overview.html
- Adobe 可编辑设计：https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/design-requirements-for-vector-submissions.html
- Adobe 内容相似：https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/distinct-generative-ai-submission-best-practices.html
- OpenAI Work/Codex 使用额度：https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex
- GitHub Actions 使用费用：https://docs.github.com/en/actions/concepts/billing-and-usage
