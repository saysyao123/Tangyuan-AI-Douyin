# Cycle 04 · 平台自带需求与稳定币支付核验

核验日期：2026-10-28（Asia/Shanghai）。公开页是平台声明，账户级权限、平台的真实运营情况和当地法律需另外确认。

## 判决一览

| 路线 | G1：买家/任务 | G2：交付 | G3：本人 U 收款 | G4：前置成本 | 决策 |
|---|---|---|---|---|---|
| Whop + Discover | 已看到公开商品与评价；新店需申请 Discover，本人能否获准及实际自然访问未知 | 离线工具、原创素材有可能；具体商品未完成商业验证 | 官网列加密提现，但本人 USDT/USDC、外部钱包、网络和地区未知 | 官网部分方案无开户月费；全部费用依实际账户和业务而定 | BLOCKED / CONDITIONAL；不得先认定有自然订单或可收 U。 |
| Getly | 有目录、商品、部分页面浏览量；本轮 11 件样本无可验证 SKU 级订单数，站内自然成交未知 | 两条动效概念已测试；商业版仍未验收 | 官网具体列 BSC USDT/USDC 与 Tron USDT，法域、账户和接收方支持未知 | 官网称无月费/上架费，成交后抽成和链费；小额卡付款可能适用处理费底线 | CONDITIONAL；技术说明最明确，但 G1/G3 不通过。 |
| Superteam Earn，含 agent 入口 | 有赞助商悬赏；列出的若干示例过期、需 X、交易或先申请；本轮未找到可确认当前符合全部条件的具体任务 | 依任务书逐条判断；获选/获奖不保证 | 部分任务用 USDC；人工认领、账户、链及所在地资格未知 | 某任务可能无需报名费，但 agent 注册、网络费用和每项任务的真实成本未完整验证 | CONDITIONAL；值得继续观察，但不冒称已有合格订单。 |
| Gigz 等加密自由职业市场 | 官网有公开需求/作品集/竞标模式，但独立买家与可接任务量未核 | 常需申请、客户往返，不满足默认低人工条件 | 官网称经托管可支付 Solana USDC；本人资格及 Binance 可接收网络未知 | 前置链上操作和费用未核 | UNKNOWN，非推荐主线。 |

## 1. Getly：需要分清支付网络和支付资格

官网[加密付款页](https://www.getly.store/sell/crypto)目前列示：BNB Smart Chain（BEP-20）支持 USDT 与 USDC，最低约 5 美元；Tron（TRC-20）仅 USDT，最低约 15 美元；网络费通常由所得扣除，网页展示的约 0.10 美元及 0.50–1 美元是浮动示例，不是账户最终报价。每月 1 日及 15 日处理结算，销售一般需经过约 30 天退款窗口；更改币种/网络/钱包后有 7 天等待，可能错过最近一期。

**重要矛盾：**[Getly FAQ](https://www.getly.store/faq)概括文字可能令人理解为两币均可经两条链，其[具体网络表](https://www.getly.store/sell/crypto)写明 Tron 仅 USDT。[Binance 2024-03-25 官方公告](https://www.binance.com/en/support/announcement/detail/33df0ff0e2e94259950b5c4b1f4952f7)声明自 2024-04-05 起不再为 USDC 的 TRC-20 充值入账；[Circle](https://www.circle.com/blog/circle-is-discontinuing-support-for-usdc-on-the-tron-blockchain)也宣布停止在 Tron 铸造 USDC。**不得按 FAQ 的宽泛说法选择 USDC/TRC-20。** 正式操作前仍须核实双方的当前账户支持、币种与合约/链匹配及法律资格；本轮没有转账。

[Getly 定价](https://www.getly.store/pricing)列示新卖家前 90 天每单平台抽成 10%，此后平台带来的交易常规档 20%（随前一月销量分档）；小额卡订单还可能受处理成本加 2% 的底线影响。假设 19 美元成交、90 天内且只按 10% 抽成，则平台份额后为 17.10 美元，再扣实际网络费、退款和适用税费；这只是算术情景，不预测销售或保证该费率适用于实际订单。

[Getly 条款](https://www.getly.store/terms)规定退款窗口至少 30 天；如账号被暂停或终止，待付资金可为处理退款等事项暂扣至多 180 天，且可能要求税务、身份或资金来源资料。广告中“不常规 KYC”不等于免除合规义务或付款保证。

## 2. Whop：Discover 与提现不可混成一项

[平台指南](https://whop.com/blog/how-to-sell-digital-products/)写明商店设置后完成清单并申请 Discover；商店有链接不证明进入自然搜索或被分发。它提供付费商品、真实评论和买家交易的可见例子，但不能推出本项目新店会有曝光或销量。[官方支付网络价格](https://whop.com/network/pricing/)列一般加密提现 5% + 1 美元/笔，举例 BTC/ETH；这**不证明**某具体卖家能外提 USDT/USDC，也不一定是该账户完整成本。币种、链、地区及审核需真实账户界面或官方书面确认。本轮没有进入本人后台。

## 3. Superteam：新发现的 agent 入口

[Superteam Earn for Agents](https://superteam.fun/earn/agents)公开说明：特定任务标为 AGENT_ALLOWED / AGENT_ONLY，agent 可提交作品，获奖后由人类完成认领。**这是潜在便利机制，不是已获得的任务或收入。** 公开文档的 agent 列表接口需要平台 API key；此 API key 是平台接口凭据，不能自动视为付费 AI 模型 API。本轮未注册 agent、未产生凭据、未提交、未支付。公开页面未给出可核验的当前符合全部条件的具体任务与奖励；普通项目可能要求 Telegram、申请、客户沟通或其他条件。

[Superteam FAQ](https://docs.superteam.fun/the-superteam-handbook/community/faqs/superteam-earn-faq)区分竞争式 bounty 与先申请项目；获奖才可能付款，部分官方赞助任务需要 KYC，外部 sponsor 付款条件不同。[Steve Agent Arena](https://superteam.fun/earn/listing/steve-agent-arena-launch-your-agent-and-win-500-usdc/)页面显示 2026-10-01 截止、需 X 和至少 5 次交易，已排除；[T3N challenge](https://superteam.fun/earn/listing/t3n-agent-build-challenge)已公布获奖者；[Kimia 项目](https://superteam.fun/earn/listing/motion-graphics-designer-kimia-product-launch-film-for-x)2026-10-26 计划公布结果且为先申请项目，不能当成本轮开放订单。

## 4. 司法辖区和停止条件

不从界面语言、时区或 IP 推断本人居住、经营和税务法域。中国大陆的[2026 年八部门通知](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)对虚拟货币市场流通和相关金融业务有明确限制；它不能单独推断每一种个人持有行为性质，也不能据此声称稳定币商业收款必然合规。若实际经营地相关，应就具体业务咨询具备当地资质的专业人士并遵守平台要求。禁止冒用身份、虚构地区、借用 KYC、规避风控、支付保证金或先付“解锁费”。

**R1：BLOCKED（完整合规路径尚未证实）；本轮未发现已通过 G1–G4 的路线。** 这是本次研究样本内的结果，不宣称全球不存在此类平台。
