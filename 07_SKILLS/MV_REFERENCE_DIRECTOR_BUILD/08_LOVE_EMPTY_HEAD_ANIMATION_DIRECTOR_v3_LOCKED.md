# 《爱让人脑袋空空》｜Animation Director Plan v3｜LOCKED MULTI-SHOT

> Upstream Timeline: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
> Segment Plan: `06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md`
> Reference Map: `07_LOVE_EMPTY_HEAD_REFERENCE_DECONSTRUCTION_v1.md`
> Supersedes: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v2.md`
> Status: `DIRECTOR_LOCKED_V3`

## 1. Core director rule

当前 MV 明确采用 **multi-shot / 多镜头**，不采用“一条生成视频 = 一镜到底”。

借鉴此前高动态“疯批打戏”测试中有效的导演方法，但转译为情绪动画 MV：

`歌词 / Beat → 人物动作 → Camera 变化 → Environment 响应 → CUT / next visual event`

必须保留：

- action progression；
- camera progression；
- shot-scale contrast；
- follow / track / push / pull / side-move 等镜头运动；
- close-up / insert / partial detail；
- foreground-background parallax；
- lyric/beat visual punctuation；
- physical body mechanics；
- dynamic peak followed by residue。

镜头动感服务歌词与音乐，不为炫技而切镜。

---

## 2. K0 ASSET CONTRACT｜HARD

K0 不是只为了“第一帧美观”，而是每条生成素材的 **first-shot anchor + persistent asset contract**。

K0-A / K0-B 第一帧必须直接可见并建立：

1. 同一原创主角；
2. 主角核心服装轮廓与识别色；
3. 同一高地湖岸世界的关键地形关系；
4. 小型微光风灵；
5. 人物可运动的地面与方向；
6. 该段主要光线 / 天气 / 风向。

后续镜头允许变化：景别、机位、人物朝向、动作状态、子场景位置、风与光强度。

后续镜头默认**不得临时新增**：第二主角、新人群、新大型生物、新大型道具、完全不同空间系统、全新服装体系。

局部特写必须来自已建立资产，例如眼睛、手、衣角、风灵、草叶、湖面反光；不依赖模型临时发明新物件。

目的：丰富的是 `shot language / motion / framing`，不是 `asset count`。

---

## 3. Unified visual world / persistent assets

### Character

同一原创年轻女性冒险者：高辨识轮廓、利落中短发、短披肩/短斗篷、腿部动作可读；暖红 / 暗珊瑚为识别色，深蓝灰 / 墨青为辅助色。

只借少年冒险动画的轮廓与姿态张力，不复制现成角色。

### World

同一高地湖岸世界，可在同一地理空间内切换：草坡、高地边缘、湖岸石径、风口平台、山脊、远山雪线、远方道路。

A：暖黄昏逐渐偏冷；B：更深蓝调但保留天边暖余光。

### Companion / motif

小型微光风灵：同一形态、同一尺度、同一光感。只承担视线引导、运动层次、Ending 消散，不抢主角。

---

# 4. Segment A｜Final BGM 0.000–8.700｜Generation 12s

Generated A: `0.000–12.000s`

Pre-handle: `0.000–1.200s`

Core: `1.200–9.900s` ↔ BGM `0.000–8.700s`

Post-handle: `9.900–12.000s`

导演目标：`爱反复发生 → 空掉 → 受伤 → 身体重新动起来 → 步履匆匆`。

## A0｜K0 / pre-handle establishing asset shot

**Gen** `0.000–1.200`

- Shot: 中景偏中全景；人物、腿部、风灵、草坡/湖岸、远山、天光全部可见。
- Character: 位于右侧三分区，身体朝左前方；重心偏后腿，前腿可启动。
- Camera: 稳定但有极轻前移；不要从纯脸部特写起。
- Environment: 发丝、披肩、草叶、湖面细微风动。
- Purpose: 一次性建立本段 persistent assets，避免后面模型补出无关内容。

**CUT / tighten framing** at Gen 1.200 = BGM 0.000.

## A1｜Hook emotional close-up

**BGM** `0.000–1.567` ｜ **Gen** `1.200–2.767`

歌词：`爱 爱 / 爱总是`

- Shot: 由中景迅速切入中近景 / 近景，略低机位、侧逆光。
- Character: 头微低，第一次“爱”眼神轻抬；第二次“爱”风灵擦过前景，眼神被短暂吸引。
- Camera: 轻推近 + 很小的横移；保留脸部可读性。
- Insert option: 句中可用极短眼神局部特写，但只来自已建立角色。
- Environment: 发丝、披肩、前景草叶形成微弱视差。

**CUT** at 1.567.

## A2｜“好了疤 / 忘了痛” spatial + hand detail

**BGM** `1.567–3.400` ｜ **Gen** `2.767–4.600`

- Hard cut to 中远景 / 中全景，人物来到同一湖岸石径子区域。
- Character: 抬手看掌心/腕部，再把手收回；不出现伤口展示。
- Camera: 前侧低机位横移跟随，人物移动 1 步以内；前景草穗/石块产生 parallax。
- Local insert: 可在“好了疤”短切手部局部特写，再切回中远景；局部元素必须来自 K0 已建立角色。
- Environment: 湖面反光、云影和风灵短促掠过。

**CUT** at 3.400.

## A3｜“让人脑袋空空” space burst

**BGM** `3.400–4.933` ｜ **Gen** `4.600–6.133`

- Hard cut to 极远景 / 高位广角。
- Visual event: 人物骤然缩小，天空与湖面占比陡增，空间突然“空”出来。
- Character: 停住并抬头，身体轻微失衡但脚底真实稳住。
- Camera: 快速 pull-back / rise，然后明显减速。
- Environment: 风灵被风卷向远处，草浪与云层共同增强空间动势。

**CUT** at 4.933.

## A4｜“直到心破了洞” emotional impact + partial close-up

**BGM** `4.933–6.633` ｜ **Gen** `6.133–7.833`

- Hard cut回中近景 / 三分之四侧面。
- Character: 吸气，肩胸起伏，一只手压住胸口；身体前倾半步再稳住。
- Camera: 短促 push-in，再轻绕 20–35°；不做长时间无目标环绕。
- Local close-up: 可短切胸前手部 / 衣襟 / 眼睛局部，作为歌词重击；必须回到同一角色连续状态。
- Environment: 风突然增强，发丝与短披肩形成明显惯性；风灵绕胸前后甩向侧后方。
- Peak: 人物、Camera、Environment 三层同时增强。

**CUT** at 6.633.

## A5｜“见了红 → 换来步履匆匆” kinetic finish

**BGM** `6.633–8.700` ｜ **Gen** `7.833–9.900`

- `见了红`: 夕阳红光 / 暖红光斑 / 少量红色花瓣或风灵短暂染红作为非血腥视觉标点。
- Hard cut to低位侧跟中全景，脚步可见。
- Character: 真实完成 2–3 步：抬脚→落脚→蹬地→重心转移→加速；无滑行。
- Camera: 低位 tracking 跟随，短暂落后→并行→略超前，形成速度层次。
- Optional insert: 极短鞋底落地 / 手握紧后放松的局部特写，可卡重音后立即回跟拍。
- Environment: 草浪、碎光、风灵与人物同向加速，前后景形成明显视差。
- Final punctuation: Gen ~9.900 必须是一脚落稳 / 抬眼完成 / 身体完成转向中的一种，不能卡在半步。

### A post-handle `9.900–12.000`

延续 A5 完成后的减速、呼吸、衣摆和风的余势；不新增剧情或资产。

---

# 5. Segment B｜Final BGM 8.700–15.370998｜Generation 10s

Generated B: `0.000–10.000s`

Pre-handle: `0.000–1.500s`

Core: `1.500–8.170998s` ↔ BGM `8.700–15.370998s`

Post-handle: `8.170998–10.000s`

导演目标：`情有独钟 → 泪眼汹涌 → 承诺被风带走 → 空间吞没人`。

## B0｜K0 / pre-handle re-establish assets

**Gen** `0.000–1.500`

- Shot: 中景偏中远景，三分之四侧后方；人物全身/大部分腿部、风灵、山脊/湖岸、远山、天光全部可见。
- Character: 同一服装和识别色，前腿承重、后腿准备跟上；朝左前远处。
- Camera: 新机位建立，不追求接 A5 动作。
- Environment: 蓝调更深，天边保留暖余光；风更明显。
- Purpose: 重新向模型声明同一资产与世界，同时让硬切成为明确新视觉句子。

**CUT** at Gen 1.500 = BGM 8.700.

## B1｜“从开始情有独钟” moving restart

**BGM** `8.700–10.533` ｜ **Gen** `1.500–3.333`

- Hard cut到新的中景 / 三分之四侧前方。
- Character: 停下、回望，再做一个真实的小步转向；手从胸口慢慢松开。
- Camera: 先短跟人物重心变化，再轻绕到侧前方并稳住。
- Environment: 风灵从远处回到人物视线前方；远山暖余光形成“开始”的残留。

**CUT** at 10.533.

## B2｜“到最后泪眼汹涌” close-up peak

**BGM** `10.533–12.333` ｜ **Gen** `3.333–5.133`

- Hard cut到近景 / 面部特写，必要时使用眼部局部特写。
- Character: 快速吸气、眨眼、眼眶湿润；风迫使她略偏脸，手抬起又停住，没有夸张哭喊。
- Camera: 短促 push-in → 很小侧移；前景风灵 / 光点擦过形成动态层次。
- Environment: 背景景深压缩，发丝和衣料高速掠动。
- Peak: 全片人物情绪最近的一刻。

**CUT** at 12.333.

## B3｜“承诺全被风吹得” hand / environment takeover

**BGM** `12.333–13.767` ｜ **Gen** `5.133–6.567`

- Hard cut到较开侧后中远景。
- Character: 伸手想抓，手伸到一半停住，然后主动放下。
- Local insert: 极短手指 / 风灵擦过掌心局部特写，随后切回环境镜头。
- Camera: 横移跟手势后立即 crane-out / pull-out，让人物权重下降。
- Environment: 风灵带少量已建立的光尘/碎光被卷向湖面/山谷；不要生成可读文字或新道具系统。

**CUT** at 13.767.

## B4｜“无影无踪” wide ending

**BGM** `13.767–15.370998` ｜ **Gen** `6.567–8.170998`

- Hard cut到极远景 / 高位开放镜头。
- Character: 人物缩小，停住或只保留极慢一步，不再追逐。
- Camera: pull-back / rise，然后明显减速并趋稳。
- Environment: 风灵飞远并裂成几点同色微光消失；草浪、云层、湖面继续运动。
- Ending: “被风带走后，世界仍然明亮”，不是黑场或强悲剧终止。

### B post-handle `8.170998–10.000`

只延续极远景和环境余韵，供剪辑自由选尾；不新增人物/生物/道具。

---

## 6. Shot-language balance

最终 15.37s 主要核心镜头仍为：

- A = 5 principal core shots + A0 pre-handle establishing；
- B = 4 principal core shots + B0 pre-handle establishing；
- 允许在 principal shot 内出现极短 local insert / partial close-up，但 insert 不另起新剧情、不新增资产。

镜头语言组合：

`establishing → medium/close emotion → tracking/follow → wide spatial expansion → partial insert → close peak → environment takeover → extreme-wide residue`。

这不是固定模板，而是当前歌曲按歌词/Beat 推导出的导演结果。

---

## 7. Coverage rule

如果 Seedance 2.5 在单条 A12s / B10s 内无法稳定完成某个关键镜头，不把失败硬塞回同一条视频。

允许额外生成 `5–15s coverage clip`，但只有在它解决具体问题时才加，例如：

- 某个局部特写不稳定；
- 某个跟拍动作质量差；
- 关键歌词缺一个可用 visual punctuation；
- A/B 可用剪辑点不足。

Coverage 只补镜头，不改变锁定 BGM Timeline。

---

## 8. Director Lock / downstream contract

当前 Director 锁定以下内容：

- multi-shot，不是一镜到底；
- A12s / B10s 是本项目生成素材长度；
- A core 5 shots，B core 4 shots；
- K0 第一帧必须建立 persistent assets；
- 近景、面部特写、眼部/手部/脚步等局部特写允许并鼓励，但只使用已建立资产；
- 人物移动使用真实步法，Camera 可跟随、侧跟、推拉、轻绕、升降；
- 镜头/动作/环境变化服务歌词和 Beat；
- A→B Final 仍 `Hard Cut @ BGM 8.700s`；
- 必要时用 coverage 补镜头，不扩张世界与角色资产。

Next Stage: `Phase H｜K0-A / K0-B formal first-frame assets + Human K0 Gate`。
