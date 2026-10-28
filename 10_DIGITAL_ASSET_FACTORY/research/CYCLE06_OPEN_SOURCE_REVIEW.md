# Cycle06：从公共AI变现项目借鉴什么

核查日期：2026-10-28。审阅7个AI收入/运营公共仓库和1个指定设计项目；不是运行了8套系统，也不是验证了8条盈利路径。README中的收入为作者陈述，未独立审计到账。缺少明确许可证的公共代码不自动视为可复制的开源软件。

## 筛选结果

| 项目 | 实际观察 | 与我方目标的冲突/证据缺口 | 可吸收内容与决定 |
|---|---|---|---|
| [Ithiel-Labs/make-money-30-Day-experiment](https://github.com/Ithiel-Labs/make-money-30-Day-experiment) | README记载约4天实验、做出大量软件、收入0、推广引发账号问题；收入tracker也为0 | 付费Claude、服务器、完全自主外联；不是成功赚钱范例；未发现可直接依赖的授权许可 | 价值最高的失败案例：身份和结算前置、禁止把产量当收入、外部动作有边界；仅研究不运行代码 |
| [astonysh/zerostore](https://github.com/astonysh/zerostore) | 免费MIT静态店铺；`log/data.json`最新2026-10-03，0收入/0订单，仅day0 | 免费部分只解决展示与跳转收银台；获客/选品技能在29美元Pro；未展示持续30天盈利结果 | 借透明记录与配置失败检查，不采购Pro、不新建独立站主线 |
| [nicepkg/auto-company](https://github.com/nicepkg/auto-company) | README明确实验中、macOS、Claude Code与订阅/API、循环运行；跨周期读写共识文件 | 非Plus-only；不提供已核实收入；24/7循环会消耗额度 | 借单一状态交接和停止/预算边界；不装守护进程、不复制“无人干预”运行 |
| [bleedline/aimoneyhunter](https://github.com/bleedline/aimoneyhunter) | README开头自述仓库已作废、旧网站停运/域名变化；依赖社媒传播和运营 | 旧方法集合，不是新卖家平台买家证明；部分账号/API分销不符合我方边界 | 作为过时方法反证，只保留垂直小切口和标准化资产思想，不访问已变质旧域名 |
| [XiaomingX/ai-money-maker-handbook](https://github.com/XiaomingX/ai-money-maker-handbook) | Apache-2.0；方法、文章与独立开发资源索引 | “做流量”是核心策略，条目不是独立成交证据；未证明无受众即可赚钱 | 用于发现线索，每条仍回到原始案例和平台核查；不按清单直接开发 |
| [garylab/MakeMoneyWithAI](https://github.com/garylab/MakeMoneyWithAI) | README是工具+变现建议大表 | stars/工具能力不等于盈利；许多SaaS、API、部署、咨询需成本/客户；元数据未确认许可 | 仅做工具候选检索，不把“商业化建议”称为案例，不复制重售代码 |
| [Qiyd81/moneyclaw-py](https://github.com/Qiyd81/moneyclaw-py) | README为金融策略Agent，含交易、资金费率、定投、API成本，默认模拟 | 属于资金风险与计算成本路径，和卖数字商品目标不同；非零资本收入 | 排除商业路线，不连接币安API、不试真实交易；最多借预算/日志概念 |
| [joeseesun/qiaomu-design](https://github.com/joeseesun/qiaomu-design) | MIT；已读README、SKILL、preflight、中文排版、工艺环与工程检查；有真实示例与横评 | 设计方法不提供客户或收入；网站横评为作者同源评审、一次采样，非独立盲测 | 用于项目设计门槛，详见[DESIGN_QUALITY_GATE](../DESIGN_QUALITY_GATE.md) |

## 三个最有用的具体发现

### 1. 与我们最像的实验，没有证明“全自动赚钱”

Ithiel实验的README自报结果是0收入，而非代码能力不足。它记录了结算失败和对外推广失控。收入tracker只有一条0记录，不能把README的全部统计当作独立财务审计。该案例支持定向自主：AI充分完成研究与制作，人处理真实身份、发布和资金；它不证明只要补KYC就会有买家。

我方已吸收：维护收入证据边界；外部推广不默认授权；已有产物时先处理商业阻塞。没有复制该项目的自动发帖、GitHub推广、无限循环、权限跳过或交易指令。

### 2. “零受众店铺”仍可能把最难的部分放在付费包

ZeroStore免费代码是静态页面和收银链接，README明确选品、生产、发布技能在付费Pro。实读付款说明，收银依赖Gumroad/Lemon Squeezy/Payhip，仍需本人地区资格，并未由GitHub Pages带来内置买家。`log/data.json`只更新到day0，不能把日期跨度当作已执行30天。

我方不购买Pro，也不为展示已有商品另建网站；先验证素材/文档市场。可以借鉴它诚实记录零收入、缺配置拒绝构建的机制，但不据此宣称获得流量。

### 3. 能复用的是状态机制，不是另一套运行平台

Auto Company的循环依赖Claude订阅/API和macOS，不适合只用现有Plus直接运行。它“每轮先读同一共识状态”的思想可用普通Markdown/JSON实现。此次已落实为同目录的 `START_HERE.md`、`PROJECT_CONTRACT.md`、`PROJECT_STATE.json` 与连续性检查脚本，三种环境直接接力，无新增AI服务。

## 是否因此换产品/平台

没有找到能直接满足“零新增现金、平台有买家、本人只上传、AI完整交付、合法实际到账”的现成赚钱系统。开源证据不足以推翻平台买家和结算门槛。

| 方向 | 本轮判断 | 下一证据门槛 |
|---|---|---|
| 已有PPT的中文/英文非独家试销 | 保留一件库存，暂不扩产；国内AI与买家授权不明 | 获得内容准入及买家内部使用的明确规则；本人收款与自然订单 |
| 原创可编辑图表/图形/SVG素材 | 更值得核验的新候选：可离线制作、相同设计逻辑可多格式复用、售后相对固定 | 具体平台及相关竞品需求、质量、许可、本人支付成本；还没制作新商品 |
| 装修避坑全流程图解资料 | 历史上下文提及，保留候选，当前不是冻结选品 | 明确买家/平台证据、内容来源和专业准确性、更新维护与许可，不拼接他人课程 |
| AI代运营、定制开发、API/SaaS、自动金融策略 | 与当前分工或预算冲突，暂不采用 | 只有约束变化且有可靠新证据才复议 |

对SVG候选的官方预核：Adobe Stock公开接受AI标识内容与SVG矢量文件，要求可商业授权的权利；公开付款门槛25美元且首单后45天，支付机构另审。它不收通用PPTX冒充矢量素材。没有新增销售证据，故不把它升为已确定更赚钱的主线，也不恢复历史Stock批量生产计划。

## 设计项目的核查边界

用户给出的`joeseesun/qiao`返回404；经检索核对项目为`joeseesun/qiaomu-design`。main核查提交：`ccd9cecb5b1f1e994eebf7bd814f2f0c35fe3bea`，SKILL元数据3.10.0而正文标题仍写3.9，说明文内版本也要核对，不能只看横评网站的3.0/3.1说明。

横评展示80个页面，但作者承认评分同源、单次采样等局限，页面方法部分还保留“7任务/12代理”等早期文字。只把示例和机制当可观察参考，不把星级叫作独立权威排名。第三方网站设计样例许可不能由本项目MIT自动覆盖，品牌素材不能直接打包销售。

## 读取范围及来源锁定

- 上述7个收入仓库：均读当前README与仓库元数据，不声称逐个运行或审计全部代码。
- Ithiel：另读`revenue/tracker.md`、README结果/协调/复盘章节，master提交`dd61744721a8f872418021f5d4993fb639f946af`；未读取秘密目录或重放外联。
- ZeroStore：另读`log/data.json`、`kit/docs/payment-setup.md`及构建脚本的配置验证部分；日志blob `eca08e4678bec3996922e6bd32327050c59d6b9c`。免费包MIT，付费Pro不在本轮读取范围。
- qiaomu：核心/相关参考按上述提交取证；不把上游作者的`user-preferences.md`当成本人的偏好，不把本轮研究称为已安装所有技能。
- [Adobe AI内容规则](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/generative-ai-content-guidelines.html)、[矢量格式](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-vectors/vector-submission-overview.html)、[付款规则](https://helpx.adobe.com/stock/contributor/payments-earnings/payment-taxes/payment-requirements.html)。

调研结论：值得复用的优先次序为失败证据与有限实验、单一项目状态、任务适配的设计验收。尚无可直接复制的盈利保证或全条件通过路线。
