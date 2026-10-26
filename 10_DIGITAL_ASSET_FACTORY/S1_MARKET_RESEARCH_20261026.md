# S1 真实商品与买家需求首轮验证｜2026-10-26

状态：MARKET_SCAN_DONE / PRODUCT_BRIEF_PROVISIONAL / PAID_DEMAND_UNKNOWN；目前没有作品、上架、订单或任何收入。这是可公开的脱敏研究记录，未公开尚未设计的专有题目和可直接复制的完整商品素材。S0 官方规则完成，但个人渠道资格仍 UNKNOWN。

## 第一性原理
核心不是“AI 可以生成100个迷宫”，而是“有人为何选择支付购买我们的商品而非已有大量低价竞争品”。从用户场景、真实买家价值、内容差异化、平台曝光与可兑现净版税反推。当前必须先研究市场，不允许以技术容易实现代替需求验证。

## A｜Amazon 旅行/儿童迷宫与益智书：10 条直接商品线索

记录标准：D=已经读取详细商品文案，I=搜索索引可见但详细页未完整核查；不是销量榜，也没有虚构成交数据。价格/完整内页/评论真实性目前未逐一核实。

| 序号 | Amazon 商品直达链接 | 可见定位 | 验证深度 |
|---|---|---|---|
| 01 | https://www.amazon.com/dp/B0H4C3MSNW | 6–8 岁旅行活动，迷宫、单词搜索、寻物、旅行日记 | D |
| 02 | https://www.amazon.com/dp/B0D86ZXCB4 | 4–8 岁旅行，35+ 活动、大开本、迷宫和逻辑 | D |
| 03 | https://www.amazon.com/dp/B0H2RV4VN4 | 4–8 岁，40+ 无屏幕游戏、宾果和日记 | I |
| 04 | https://www.amazon.com/dp/B0H6RXDJFQ | 4–8 岁，100+ 活动与游戏 | I |
| 05 | https://www.amazon.com/dp/B0H57628PT | 4–8 岁，50 无屏幕旅行活动 | I |
| 06 | https://www.amazon.com/dp/B0GTF1DDDM | 4–8 岁，108 页、迷宫、单词搜索和简单数独 | I |
| 07 | https://www.amazon.com/dp/B0GTY5JJF9 | 旅行情境的涂色、迷宫、描线与小游戏 | I |
| 08 | https://www.amazon.com/dp/B0H79QWJR7 | 旅行活动/游戏/书写 | I |
| 09 | https://www.amazon.com/dp/B0H341KTV8 | 4–8 岁、多类型无屏幕活动 | I |
| 10 | https://www.amazon.co.jp/dp/B0CX547XJL | 6–10 岁旅行，16 种活动约80页 | I |

来源：上方十个 Amazon ASIN 的直接商品 URL、搜索引擎截至 2026-10-26 的结果。部分 Amazon 商品页访问返回 500/503；不能将索引描述当成已逐页检查。不得推定任何一本的实际销量。

初步观察：普通迷宫合集缺少明显独特价值，旅行活动书也有大量供给；真实的付费场景是孩子旅途中长时间的无屏幕活动和家长方便安排，不是随机网格本身。这是买家 Job 假说，不是我们已能获得订单的证据。

## B｜Adobe Stock 装修/维修场景：公开供应侧扫描

- https://stock.adobe.com/search?k=home+improvement+icons ：家居通用图标类已有大量供给。
- https://stock.adobe.com/search?k=icons+home+renovation ：装修图标类供给丰富。
- https://stock.adobe.com/search?k=construction+quality+control ：施工质检图像素材广泛存在。
- https://stock.adobe.com/search/templates?k=construction+safety+icons ：更具体的施工安全视觉场景及模板。
- https://stock.adobe.com/search/templates?k=construction+quality+control ：专项质量控制模板现有供给，但搜索结果数量不能直接证明需求缺口。

注意：检索页面混合照片、模板、矢量和视频，数量随时间变动；当前还没有完成 10 个单独素材 ID、具体授权竞争力和买家需求分析，因此 Stock 维持 RESEARCH_ONLY，而不是商业 PASS。

## 路线比较与决策

- 普通“100道迷宫”图书：技术简单，但既有大量替代，首轮 REJECT。
- 有年龄分层、旅途场景、画面统一、能独立完成并包含必要答案和说明的完整纸质益智活动书：PROVISIONAL_FIRST_SAMPLE；需求场景真实，差异化和销量尚未知。
- 普通装修工具图标 SVG：高度同质，REJECT_AS_GENERIC_STOCK_PRODUCT。
- 面向具体服务流程/施工验收的可编辑原创信息图 SVG：专业使用价值假设，RESEARCH_ONLY，需要下一轮单作品市场核查。
- 提前建设批量“无人值守工厂”：并不能产生买家，REJECT_NOW。

## S1 试验版 PRODUCT_BRIEF（公开且非最终商品锁定）

Buyer：为 6–8 岁儿童准备旅行、候车或居家安静活动的英语市场家庭。
Job：无需屏幕和复杂额外材料，可以方便孩子独立开展有难度梯度的活动。
Occasion：长途车程、飞机/候车、安静休息时间。
待测试差异化：在真正不同的谜题之外有清晰年龄指令、连贯的使用体验、可验证答案以及专业排版。必须通过真实商品视觉/细节对照证明比普通合集好。
暂定技术样本：以数道独立算法可验证的迷宫作为生产引擎 smoke test；不能把整个商品简化成纯迷宫合集。
不做：套用竞品封面、复制题目、生成一堆仅换色的近重复图、增加付费 API、提前批量上架。
实际零售价格、页数和封面形式暂不锁定，须经 KDP 官方版税计算与完整竞品细节确认。
Commercial Gate：PROVISIONAL / NO_SALE_EVIDENCE，不得声称已完成选品商业验证。

## STEP-0 苏格拉底八问及反证

1. 为什么买？有真实上架同类品和明确使用场景；但新商品付费意愿未知。
2. 为什么先研究需求？通用迷宫已竞争拥挤，写算法不能解决买家为什么选我们。
3. 不研究可以吗？不行；否则只会增加无效库存。
4. 替代是什么？普通迷宫（易做但弱差异化）、场景化活动书（更复杂可小样验证）、专业 SVG（买家证据未足）、停止（零成本）。
5. 何种反证会否定选择？无法合法收款、同类已有更优体验、设计/内容质量达不到、美术无差异、版税太低、实际上架无销售反馈。
6. 最弱假设？新品牌能在拥挤类别获得可见性及真实购买，UNKNOWN。
7. 如何证明？进一步复核 3–5 本详情页内页/定价、制作可实际使用的高质小样、上架审核、首单/净版税，缺项不能升级状态。
8. 每周扩产瓶颈？选题同质化、设计疲劳、平台反垃圾、AI 套餐额度、逐件独立 QA 时间。

## S1 步骤级 GitHub 开源参考（2026-10-26）

- https://github.com/vijaxx/kdp-puzzle-engine ：MIT、题目生成与封面/版式主参考。其存在并不证明书有销量；仅等 S2 做源码和运行检验。
- https://github.com/Ashremm/kdp-niche-analyzer ：小型实验工具，仓库未见可确认 LICENSE、可选付费 Anthropic；只借鉴“竞品/BSR/评论”的研究维度，销量估算不能替代真实支付数据。
- https://github.com/nkiro33/kdp-calculator ：无明确仓库级许可证的静态版税/BSR 工具，只学思路，最终价格以 KDP 官方计算器为准。
- https://github.com/hellohukam/stock-metadata-csv-generator ：MIT，未来可用于无 API 的投稿文件表格整理，本步骤不安装。
已读仓库信息及相关 README，尚未执行/通过项目测试，不能声称实现已稳定。

## S1 当前 Gate 与阶段交付

已交付：10 条 Amazon 商品线索及核实深度、Stock 多个官方分类、通用品类反证、首个可逆商品样本、八问自审、开源对照、下一轮验收点。
未完成：10 本全部详尽核价/内页/评论核查、10 件 Stock 具体素材的单品比较、正式差异化产品定稿；更没有可证明我们的订单。
因此本阶段状态为 S1_RESEARCH_DELIVERED / BRIEF_PROVISIONAL / COMMERCIAL_GATE_NOT_PASSED。

下一步：先确定用户可以合规收款的具体国家/地区路径，再深读至少 3–5 本可比商品的完整详情/封面、验证官方版税；以有限决策样本冻结具体 PRODUCT_BRIEF，之后才进入 S2 的开源代码实际运行。S3 才进行 VISUAL-0（至少两个设计开源项目和真实商家视觉对标）；不能自认为审美通过。
