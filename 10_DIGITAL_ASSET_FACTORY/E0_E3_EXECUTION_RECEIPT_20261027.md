# USDT/USDC 项目第一轮执行交付（2026-10-27）

项目约束：现有 GPT Plus、零新增现金/付费 API、平台自带消费者、可交付原创数字商品、优先 USDT/USDC；按本项目 STEP-0、VISUAL-0、质量门槛执行。此公开文件不放入完整待售 HTML、样品源码或私人账户资料。完整内部预发布 ZIP 已在当轮对话中交付。

## E0 平台和收款核查

- [Whop 官方创作者收款说明](https://whop.com/blog/getting-paid-on-whop/)确认支持向加密钱包提现；[Whop 网络费率](https://whop.com/network/pricing)公开显示加密提现 5% + $1/笔，出售商品的支付手续费及可能的风险准备金另计。
- [Whop Payout Help](https://help.whop.com/en/articles/10336709-how-to-setup-payouts-withdrawal)要求完成本人 KYC/身份与地址、国家等审核后才可提现。
- [Whop Wallet Terms](https://whop.com/wallet-terms)出现 USDT，然而这与本人 Whop 账户中卖家 payout 是否支持 USDT 或 USDC、具体网络、转入 Binance 不是同一项资格；目前未知。某些 [Whop 稳定币收益条款](https://whop.com/whop-wallet-terms/)还涉及 Aave/Veda 等 DeFi 借贷及本金风险，不自动选择此项。
- 中国大陆实际经营涉及 2026 年虚拟货币业务限制。已有 Binance 钱包可转账是用户提供的事实，不能替代本人法域合规、Whop 财务审核和实际 payout 资格。不给出绕过 KYC、假居住地、借用账户等方案。
- 当前 E0 状态：官方通用加密提现存在 VERIFIED；本人 USDT/USDC 币种网络、Whop 个人 KYC 与合规 UNKNOWN；真实币安到账 NOT_TESTED。

## E1 五件真实竞品与市场反证

Whop 在售页及可见挂牌价（非实际销量/转化保证）：
1. [AI Video Generation Toolkit](https://whop.com/discover/ai-prompt-power-pack/ai-prompt-power-pack/) — $25，模板、提示词与课程。
2. [Sora Viral Motion Kit](https://whop.com/kyzyma/sora-viral-motion-kit/) — $36，短视频公式与模板，公开 1 份评分。
3. [AI Video Ad Generator](https://whop.com/imdialed/ai-video-ad-generator-0d/) — $47，36+ 公开评分，声称处理分镜与视频并依赖多个付费 API。
4. [The Sora Prompt Toolkit](https://whop.com/creatortoolkit/products/the-sora-prompt-toolkit/) — $49，提示词与教程。
5. [Text-to-video storyboards](https://whop.com/ai-art-storyboard/ai-art-storyboard/) — $99，100+ 提示词包。

初步推断：卖普通提示词很难构成可防御差异化，因此试验真实可操作的离线分镜 + 连续性 + 人工 QC 工具，不承诺生成视频、自动观看 MP4、保证流量。仍未完成 10 个独立商品详情深度核查、任何买家访谈或真实点击/销量验证；E1 商业 Gate 尚未通过。

## STEP-0 第一性原理及苏格拉底八问摘要

1. 目标是能获取真实 U 而非代码数量；所以先核平台付款、买家、产品独特价值。
2. 纯提示词包免费替代多，必须真正可编辑操作并导出，防止虚假功能。
3. 选择浏览器本地工具，因没有 API 订阅、服务器与售后费用；若真实买家不要这样的工具，按数据转型。
4. Whop 平台有用户不等于自然流量分给我们；需要曝光/订单证明。
5. 用户币安会收币也不等于 Whop 当前账号通过 stablecoin payout 审核。
6. 获取营销评分与产品评论不等于知道对方销量；不伪造销量预测。
7. 内容与 UI 的审美需要外部参照和本人 QA，不能凭首次生成就假装完成。
8. 如果真实收款合法资格不成立就停止上架；本地少量技术样品可保留。

## E2 开源设计参考和许可

- [Penpot](https://github.com/penpot/penpot) MPL-2.0：界面信息层级、表单设计与空间系统的参考。
- [Excalidraw](https://github.com/excalidraw/excalidraw) MIT：可理解的图形/工作流交互参考。
- [Fabric.js](https://github.com/fabricjs/fabric.js) MIT：可编辑画布的备选，但本轮不引入以减少依赖和技术复杂度。
- 已核查仓库 LICENSE 元数据与适用性，未复用以上项目源码、图标或第三方图片，也未逐文件执行其源代码测试，不能声称已完整审查所有源代码或获得独立买家审美合格证。
- FRAMEWISE UI 采用原创暗色后台、淡青绿强调色和清晰分组；已生成桌面/移动截图，需实际目标客户视觉验收才能过 VISUAL-0 商业定稿。

## E3 本地软件已经真实生成和测试

软件：FRAMEWISE v0.1 英文离线网页 AI Shorts Director & QA Kit，约 41 KB 原生单页 HTML，零运行外部网络/CDN/字体/API。
功能：项目目标 Brief、视频时长和每镜头时长、景别与摄像机运动、实际人物任务和环境事件、角色/服装/场景连续性规范、6 个需人类确认的硬质检门槛、4 种导出（Markdown Director/QA、CSV Shotlist、JSON Project）、错误 JSON 提示、本地草稿。
内容：虚构雨夜站台三镜头样板、英文说明、授权草案、英文商品页面文案、QA 报告、桌面与窄屏预览。
实测：Chromium Playwright DOM 真运行；镜头由 5s 改为6s 时出现目标时长错误，改回清除；添加/删除镜头、6 个硬门槛、JSON/CSV 真正浏览器下载、QA报告、错误及有效 JSON 导入、模拟 LocalStorage 恢复、移动截图均 PASS。受沙箱浏览器导航限制，测试通过 set_content 装载 HTML；不把模拟 LocalStorage 当真实浏览器跨重启验证。用户使用自己的桌面浏览器仍须确认 file 协议下载权限。
本轮输出完整 ZIP 在 ChatGPT 当前对话提供；因公开 GitHub 可能泄露尚未上架的完整商品，不上传 ZIP 或可售代码到当前 Public 仓库。
E3 状态：LOCAL_SOFTWARE_CREATED / FUNCTIONAL_TEST_PASS / VISUAL_INTERNAL_REVIEW / BUYER_QA_PENDING / MARKETPLACE_NOT_PUBLISHED / INCOME_ZERO。

## Superteam Earn 真实机会反欺骗核查

[Superteam](https://superteam.fun/earn) 有 USDC、USDG 等奖金任务，通常属于竞争悬赏不保证报酬。[Era Wallet Video Editing Challenge](https://superteam.fun/earn/listing/video-editing-challenge) 详情页面显示已截止、宣布 $150 USDC 获奖者；有些索引仍显示剩余天数，所以拒绝将旧任务算作当前可接或即将赚钱的机会。其他任务需逐个核准真实剩余时间、地区、AI许可、零额外成本、币种及可提交资格。

## 下一 Gate 与阻塞

1. Whop 创作者账号本人实名/KYC、所属法域规则与实际可用 USDT/USDC payout 币种、网络、完整费用。当前无法代用户完成本人验证，也不能虚构到账。
2. Whop 10 件竞品深度比对、真实用户测试、商业英文文案与作者支持联系人签署。
3. 通过准入后才可合法上架产品（不增加广告/付费服务），测量平台的实际自然曝光与转化。
4. 第一单、可用平台余额、币安真正收到 USDT/USDC 三者分开验收；只有最后一步完成后才报告赚到 U。
5. 若 Whop 不能给出稳定币付款批准，必须重新考虑 Getly 等明确 USDT/USDC 平台，但要单独证明真实自然买家，不能为接 U 而放弃商业验证。

结论：本轮确实完成一个可运行软件原型以及浏览器功能 QA，没有完成销售或收款；下一阶段聚焦平台资格和买家证据，不盲目批量生产。