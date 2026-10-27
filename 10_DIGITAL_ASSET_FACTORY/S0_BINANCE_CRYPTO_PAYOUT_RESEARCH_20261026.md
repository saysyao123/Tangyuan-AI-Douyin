# S0｜币安/稳定币作为海外数字商品平台收款方式：合规与市场检验（2026-10-26）

> 研究日期：2026-10-26。用户当前设定：中国大陆个人身份优先、最终收入应能合法使用或结汇、平台需自带买家、只用现有 GPT Plus、零新增现金订阅/充值。状态：CRYPTO_MARKETPLACE_PATH_FOUND / MAINLAND_RMB_CONVERSION_NOT_ELIGIBLE / BUYER_TRAFFIC_NOT_PROVEN。该文件不是法律意见、不是开户或提现的测试记录。

## 1. 第一性原理

**必须完整验证“买家付款→平台销售→合规支付创作者→用户能合法控制资产→可依法在中国大陆使用/结算并完税”**。如果稳定币仅到达钱包，之后无法合规使用或兑换成实际人民币，技术到账不是本项目要求的可兑现商业收益。币安钱包地址可用于某些链上付款的技术能力，与平台认可、币安真实 KYC、所在地法律合规、人民币出金完全不同。

## 2. 中国大陆 2026-02-06 最新监管红线（必须优先于第三方平台营销内容）

八部门《关于进一步防范和处置虚拟货币等相关风险的通知》银发〔2026〕42号，自发布日施行，明确：BTC、ETH、USDT 等不具备法定货币地位；**境内法币↔虚拟货币兑换、币币兑换、作为对手方买卖、虚拟货币交易中介等属于非法金融活动并禁止**；境外机构不得非法向境内主体提供相关虚拟货币服务。不能因为 USDT 是“稳定币”就当成合法外汇或一般银行卡款项。

官方原文：https://policy.mofcom.gov.cn/claw/clawContent.shtml?id=104982 ；证监会与人行联合问答：https://www.csrc.gov.cn/csrc/c100028/c7614320/content.shtml 。

**操作边界**：本项目若按中国大陆自然人境内路径实施，不能使用 Binance P2P/C2C 将 USDT 卖给境内人民币买家，不使用第三人过桥、虚假香港/海外身份、他人银行账户、隐藏交易来源等规避限制。是否在合法海外居住地拥有受支持的账户和当地合法税务身份，属于未来另一个独立问题，不能用中国大陆身份自动推断有境外资格。风险不意味着简单持币本身在任何场景都被同等定性；但资金兑换与经营活动路径构成重大红线。

币安通用条款本身将使用服务导致违反适用法律的辖区设为限制资格：https://www.binance.com/zh-CN/terms 。不能因已经有币安账户就推断有合规商业版税收款及本地法币出金权限。

## 3. 平台真实付款能力（市场流量和资金合规分开看）

| 选择 | 卖家合法 payout | 是否有内置市场发现 | 中国大陆路径初步判断 |
|---|---|---|---|
| Creative Market | PayPal / Wire，中国官方表支持两者、不支持 ACH | 有成熟设计商品目录、搜索和买家生态，**不保证曝光** | 继续作为优先商业主线；未支持向 Binance USDT/USDC 付款 |
| Creative Fabrica | PayPal / Payoneer / bank，银行汇款最低 $100 且有 $20 处理费（需至少 $120 可用余额） | 有设计商品/订阅搜索与平台客流 | 主流传统市场备选；未支持 Binance 稳定币 |
| itch.io | Collected by itch.io 以 PayPal / Payoneer 支付 | 游戏和开发素材市场有分类和搜索 | 用于 RPG 美术备选；平台默认未提供链上稳定币提现 |
| Getly (getly.store) | 官网写卖家收入 USDT/USDC，BNB Smart Chain 或 Tron，最低 $5/$15，半月付款；平台佣金默认20%，新店前90天营销10% | 有市场搜索/分类和网站自称的推荐功能；具体自然成交/规模缺少独立审计 | **技术上存在加密版税平台，但中国大陆加密交易/变现合规阻塞，且买家基础不成熟** |
| ExDFS (exdfs.com) | 官网自述向作者自持钱包支付 USDT，Tron/BSC | 新数字商品平台，未能取得可靠的独立有机流量/实际订单证据 | 更弱的小平台候选，不作为有现成客户的首选 |
| Summon+ (summon.plus) | 自述数字创作者 USDC 即时到账 | 有 marketplace 但宣传仍突出向自有粉丝分享支付链接 | 无可靠买家自然流量及境内合规验证，非优先 |

官方/来源：
- Creative Market 中国付款支持表：https://support.creativemarket.com/hc/en-us/articles/115004067573-Which-payout-methods-are-available-in-my-country 。
- Creative Fabrica 实际付款：https://help.creativefabrica.com/hc/en-us/articles/360029930872-How-do-I-make-a-payout-of-my-earnings 。
- itch.io 模式与税务：https://itch.io/docs/creators/payments 。
- Getly 卖家 USDT/USDC：https://www.getly.store/sell/crypto ；https://www.getly.store/terms ；https://www.getly.store/faq 。
- Getly 外部信任/流量线索：https://www.scamadviser.com/check-website/getly.store （域名年轻、低 Tranco 排名，非独立销量审计）；其 Trustpilot 评价主要谈开店简便，不能证明第三方买家活跃与商品销量：https://www.trustpilot.com/review/getly.store 。
- ExDFS：https://exdfs.com/sell/ ；Summon+：https://summon.plus/ 。

**特别风险**：Getly 虽称无需 KYC 的普通钱包收入，但服务协议仍保留 AML/KYC 触发和账户审查、180天暂扣待结算资金的条款；“无需 KYC”不是零风险、无合规义务或真实提现保证。其平台独立交易规模未取得可靠可核查报告。

## 4. 传统法币路线复核（更符合中国大陆实际资金需要）

**优先 A：Creative Market 官方 Wire → 中国大陆本人银行账户**。中国地区付款表明示支持 Wire；需向本人开户银行确认此类商业授权收入是否合法按个人账户入账、是否需要经营主体、版权合同/平台版税报表、SWIFT 中转及手续费、外汇申报与结汇条件。不能因平台支持 Wire 就宣布已可以到账。

**备选 B：Creative Market/Creative Fabrica PayPal → 中国大陆本人银行**。中国 PayPal 官方显示美元电汇到大陆银行最低 $150，通常 3–7 个工作日；个人账户公布每笔 $35 提现手续费，商业账户可能有不同费率，实际外汇汇兑费另算。因此小额收入应避免频繁提现，且实际收款需 KYC、支付平台和银行审核。官网：https://www.paypal.com/c2/cshelp/article/%E5%A6%82%E4%BD%95%E4%BB%8E%E6%88%91%E7%9A%84paypal%E8%B4%A6%E6%88%B7%E6%8F%90%E5%8F%96%E8%B5%84%E9%87%91%EF%BC%9F-help394?locale.x=zh_C2 ；https://api-c.paypal.com/c2/digital-wallet/paypal-consumer-fees?locale.x=en_C2 。

**注意**：银行 SWIFT 可能收电报/中转/结汇费；不能假设比 PayPal 一定便宜。收款合同、合法收入来源、税务身份验证都要本人完成。

## 5. 苏格拉底八问

1. 为什么要考虑币安？用户已有钱包，直觉认为 USDT 结算可减少 PayPal/银行门槛；但解决的只是“到数字钱包”而不是合法人民币兑现。
2. 为什么大陆法规是第一闸门？合规是不可用高收益或低手续费抵消的硬约束。
3. 可以只收币不换吗？技术上某些平台支持稳定币钱包，但“收益能安全持续使用”和真实买家仍然未验证，不符合当前大陆可兑现目标。
4. 替代路线有哪些？Creative Market 直接 Wire、PayPal 累积提现、Creative Fabrica 银行付款、国外允许稳定币支付的小型商品市场（因合规及流量问题暂停）。
5. 哪些事实会推翻当前推荐？用户未来确实合法迁移至允许相关业务的司法辖区，有该辖区真实合法身份及税务、平台 KYC、币安账号完整支持、当地可合法出金；需另立新 Gate。
6. 最大的不确定性？中国大陆个人银行能否接收持续商用数字素材版税；中国 PayPal Business 能否实际收此类付款以及附加费用；币平台自然付费流量有多少。
7. 如何确认真正赚钱？独立真实订单、平台可合法提款、实际人民币到账、费用税款、退款与人工维护时间。
8. 会不会规模后出现风险？稳定币平台/钱包/链安全、交易冻结、平台政策变动和买家不足都会放大；主线应选择合规法币商品市场。

## 6. 执行结论 / 当前状态

**CRYPTO_NATIVE_PAYOUT_EXISTENCE=VERIFIED**；**BINANCE_TO_MAINLAND_RMB_LEGAL_PATH=BLOCKED_UNDER_CURRENT_RULES**；**CRYPTO_MARKETPLACE_ORGANIC_DEMAND=NOT_PROVEN**；**CREATIVE_MARKET_CHINA_WIRE=OFFICIALLY_LISTED_BUT_NOT_TESTED**；**PAYPAL_TO_MAINLAND=OFFICIAL_MINIMUM_AND_FEE_KNOWN_BUT_NOT_TESTED**。

执行决策：不拿 Binance 作为当前中国大陆商业收入的默认收款工具；保留币平台市场资讯供非大陆合规辖区的未来另案研究。持续推进“成熟平台真实买家 + Wire/PayPal 合规法币收款”流程，不购买增值服务、不使用地下 C2C 或虚假信息过桥。

下一唯一动作：咨询本人境内开户银行是否接受持续的海外版权/数字设计商品平台 SWIFT 版税，并取得费用表；并向 Creative Market 商店支持确认中国大陆个人开户以及 Wire 的付款处理费、最小金额、具体税务资料与 AI 作品披露。随后才投入原创商品样板与竞品验证。


## S0-BINANCE-HOLD｜2026-10-27 用户明确只需将海外销售所得保存在币安，暂不法币提现

**最新目标修正**：收入完成标准不再要求兑换人民币或汇入境内银行卡。此项仅覆盖旧文件中“必须实际人民币到账才算第一阶段收入”之要求；仍然坚持用户仅 GPT Plus、无新增现金付费、真实自然买家和合规可执行。**真实商业收入完成状态应分离为 PLATFORM_SALE / PLATFORM_PAYOUT / EXCHANGE_CREDIT / LEGAL_USABILITY / RMB_CASHOUT_NOT_REQUIRED。**

### 技术可行性：Getly → 币安，条件成立时存在对应网络

- Getly 官方允许从数字商品市场结算 USDT/USDC，支付网络为 BNB Smart Chain（USDT 或 USDC）或 Tron（仅 USDT），每月 1/15 结算，在约 30 天退款窗口结束后进行。低于 BSC $5 / Tron $15 的余额结转。来源：https://www.getly.store/sell/crypto 、https://www.getly.store/faq 。
- Getly 官方价格与条款：普通作者约保留商品售价的 80–90%，自带流量可享更低抽成；卖家有自己的平台目录，但“平台有搜索分类”≠“成熟真实消费者流量”；官网自报约 9,585 个 listing、2,425 个 creator，**未取得独立真实销量、搜索转化和新店曝光证明**。来源：https://www.getly.store/ 、https://www.getly.store/terms 。
- Binance 官方说明从外部钱包存加密资产时，币种及网络必须完全匹配；BEP20=BSC，TRC20=Tron。选错网络可能无法追回资金。**只有账户在真实 KYC 所属国家/地区及实际使用地点获准接受此类来源，平台的托管充值信息且源款身份核验通过时，技术上才可组成交易所入账闭环**。来源：https://www.binance.com/en/support/faq/detail/85a1c394ac1d489fb0bfac0ef2fceafd 、https://www.binance.com/en-AU/support/faq/detail/6d7de22f918d4cf28d68a7079a10e254/ 。
- Getly 宣传通常无平台级 KYC，但 2026-10 的条款要求真实完整的 payout/tax 信息，平台保留索取额外材料及暂缓结算权。不能把“无需 KYC”当作匿名绕过地区限制的许可。来源：https://www.getly.store/terms 、https://www.getly.store/rules 。
- 其他技术候选 ExDFS 提供 USDT（BSC/Tron）到外部钱包的方案，最低 $25（部分创始店例外），但独立自然买家规模缺证据，不宜视为已拥有有效市场。来源：https://exdfs.com/sell/ 、https://exdfs.com/faq/ 。
- 根据中国 2026-02-06 银发〔2026〕42号，境内虚拟货币相关非法金融业务被禁止，并禁止境外主体非法向境内主体提供虚拟货币服务。因此如果实际居住/经营场景是中国大陆，**即使不做 RMB 兑换，接收境外平台结算并存入币安也不能直接视为合规**。原始法律来源：https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml 。个人仅持有虚拟资产的法律性质应与提供非法金融业务区分，但不足以推出“从事稳定币收款经营必然合法”。
- 币安用户协议：https://www.binance.com/zh-CN/terms ，要求真实地区及身份符合适用法律，不能通过更换 IP / 虚报居住地 / 借用 KYC / 代收款规避限制。
- 这次用户并未说出实际 Binance KYC 国别、居住地及帐号服务所属区域；**不得把聊天偏好“中国大陆注册方便”推断成已确定其当前法域**。实际获准的非大陆辖区可另行根据当期法律、交易所和税务政策审查，但不能据此假设用户已获相关资格。

### 更新后的两级商业 Gate

1. **LEGAL_AND_ACCOUNT_GATE（先行）**：确认本人币安实际 KYC 及常住/经营地对应支持的合法 crypto deposit 服务，Getly/ExDFS 是否允许向该类用户支付商业收益，双方的合规/税务及付款来源证明；无授权则 STOP，不指导绕过。
2. **REAL_BUYERS_GATE（后行）**：优先有真实平台消费者且按平台自然发现获得订单的市场。Getly 仅自报商品/卖家数，缺独立买家流量和新店自然成交证据，应先做只读竞品分析和小样而非批量生产。与 Creative Market/Fabrica 的成熟市场生态比较时明确：它们未提供币安直接稳定币结算。因此这是收益分配方式与自然获客之间的真实 tradeoff。

### 苏格拉底八问（本次新收款目标）
1. 去掉 RMB 提现解决什么？省去境内银行汇兑和提现费用，但不消除帐号 KYC 与地区政策、持币风险。
2. Getly 直接打 USDT 就是商业成功吗？仅平台真正结算且币安显示到账，再确认账户合法使用，才证明付款链路；平台有销售才是收入。
3. 可以把平台的“无 KYC”当规避地区限制吗？不能，条款保留税务/反洗钱及限制。
4. 币安能收所有网络吗？不能，按真实账户实时币种与网络支持判断，不跨链猜测。
5. 平台有上万产品就有客户？不能，供给/目录数不等于销售/买家。
6. 有比 Getly 更成熟的稳定币设计市场吗？当前未核实；ExDFS 同样缺市场证据，不应承诺一定销售。
7. 什么可推翻选择？身份法域不允许、币安账户禁止、Getly 平台拒绝商业付款、自然买家不可验证、提现/资金冻结。
8. 应怎样防重复低质生产？先做行业类别竞品证据、两个设计开源参考、最小高质量素材样板，独立 QA 和少量真实上架试验（仅在前序合规通过时）。

**状态**：GOAL_BINANCE_CUSTODY_ONLY_LOCKED / CRYPTO_TECH_ROUTE_IDENTIFIED / RESIDENCY_AND_KYC_UNKNOWN / GETLY_BUYER_DEMAND_UNVERIFIED / ACTUAL_TRANSFER_NOT_TESTED / NO_PRODUCT / NO_ORDER。

**下一阶段**：仅需确认用户真实 Binance 账户 KYC/居住司法辖区（只问国家或地区，不收具体身份文件与账号），先处理合法使用，再研究 Getly 及 ExDFS 平台在目标细分行业的真实自然消费者数据，之后才做可售样品。
