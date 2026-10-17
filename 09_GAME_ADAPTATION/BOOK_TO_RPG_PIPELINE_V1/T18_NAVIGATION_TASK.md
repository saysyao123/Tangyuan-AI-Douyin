# T18 · 第二幕室内与原生点击寻路

Status: done; Coding Owner: root; independent source reviewer: t16_review. 2026-10-17.

用户范围：第二幕室内无法继续；丰富环境，参考仙剑与开源JRPG改善寻路。保持已认可剧情和owner-private访问。

## 前提真值

| 方向 | 一手证据 | 结论 |
|---|---|---|
| PAL/现代参考 | sdlpal/sdlpal; Grid Engine官方move-to示例; RPGJS官方Move命令 | 层次/碰撞/目标移动作参考，不复制商业资产、不迁移框架 |
| 第一阶段 | upstream/docs/phase2/reference/phase1-knowledge-harvest.md W3/W4, content/src/grid.ts | 菱形轴坐标与真实相机映射，脚底锚点 |
| 当前原生 | main.ts heldDir/findTrigger/advanceMoves; entity-motion.ts motionTerrainSweepBlocked/motionSweepsConflict | 仅键盘移动；point事件只启音频；原生player dynamic intent为唯一正常移动写入者 |
| 当前内容 | T17 room collision与washbasin脚本 | 所有室内交互邻格静态可达；moveParty authored bypass，未复现家具令洗漱runner等待 |
| 已证风险 | 合法旧布局位置(26,-1)落在T17床脚印内，四向sweep仍在blocked cell | 仅家具内部就近恢复；不能称已证明用户实况 |

最强替代解释：失焦、未靠近目标、等待对白/确认/库存使用，而非引擎死锁。真用户档缺失，根因保持未复现；以真实native输入与合法旧档位置反例验证新增恢复。

审查：t16_review独立读exact主源，premise verified/design agree。初审counter指出fraction start+NPC连续body与恢复镜头；已采用motionSweepsConflict及原生partial-axis intent对齐，恢复同步renderedPlayerPos。禁止shell写剧情。继续等待实现复核与CI。

## 实现与验收

bounded四向BFS共用原生terrain sweep/body sweep；点击地面绕障、点击目标在原生range内交互，键盘/模态/失焦/切场/读档取消。原生player intent提交partial/full步；不使用剧情bypass行走、不合成按键。只有本项目home-room内家具落点用有限4格恢复，保留故事/库存/钱/原档。

新增原创六类像素环境素材，家具与边缘景物分组，维持主通道。作者overlay可重复构建、原生SAVE12标识保留。

只测新增导航合同与受影响第二幕出门购买/返家洗漱/用真实post-fruit旧档回屋吃饭到庭院。已通过抽奖、道具、战斗和第一幕老套件不重跑。public fixture文字用于CI，private文字只作绑定/机械等价验证。

## 失败经验（持续记录）

- 不能把用户卡点直接归因新增家具：静态检查与authored bypass反证。
- 点路不能仅用sameGrid：原生动态人物有连续body sweep；分数坐标需要通过正常partial步对齐。
- 旧档恢复除了逻辑位置，还需同步显示脚点、队形与镜头。

- 首轮CI 39004516077：构建/类型/合同通过；旧档恢复、fraction靠近、键盘取消通过；出门目标未命中。截图显示测试点在门牌透明脚部附近，原矩形hit选到餐桌。修复为可见像素alpha命中 + 可点击脚边marker；鼠标测试点击显式marker。并收紧safe free为零位移native连续sweep，排NPC半格重叠。

实现独立审查：t16_review accept。pointHit使用当前渲染帧与原生脚底+7换算，先边界后opaque；明确marker优先。最终fresh源码已重建，包含pointCanStep(pos,pos)、renderedPlayerPos同步、null反馈。

- 成功导航CI：39004754229，commit32f2573a1066ace088bd9e869442943581ee0e67。6项定向浏览器检查通过、pageerror 0；authentic post-fruit checkpoint跳过抽奖/道具旧套件。
- 截图复核发现另一种“测试绿但美术未达标”：初版新树/柴堆放在地图边缘，entry camera仍空。调整为真实entry视野中的树木侧框、前景柴堆/石灯，室内窗下移并减弱地板高对比斜纹。native代码未变，后续39005192149只跑环境显示与局部通行，不重播已接受剧情。

环境CI39005192149通过；原生可执行bundle与已接受导航CI39004754229逐字节一致。最终私人发布候选109 native文件机制/二进制等价，525运行文件路径一致，其中465逐字节一致，60仅私有文字/展示差异，51条night cue绑定。发布receipt另见RELEASE.json。

正式owner-private发布成功：Site source572c19dfe44bcf35da8b8ccf5e76781ae71c135e，deployment appgdep_6ad305163d0c81918c0e135368beca56。全部运行与ZIP/部署归档校验通过。用户具体旧档卡点观感仍待试玩确认；本轮不声称已复现同一用户故障。
