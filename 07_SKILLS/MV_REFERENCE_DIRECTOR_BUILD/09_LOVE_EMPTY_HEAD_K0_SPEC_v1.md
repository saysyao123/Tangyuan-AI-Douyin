# 《爱让人脑袋空空》｜K0 Spec v1

> Upstream Timeline: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
> Segment Plan: `06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v2.md`
> Director: `08_LOVE_EMPTY_HEAD_ANIMATION_DIRECTOR_v3_LOCKED.md`
> Status: `K0_SPEC_READY / IMAGES_PENDING_HUMAN_GATE`

## 1. K0 role｜HARD

K0 = **first-shot dynamic anchor + persistent asset contract**。

K0 不是海报，也不是要求后续 10–12s 一镜到底。它只负责第一镜头起点，同时把该条生成素材后续持续需要的核心资产一次性建立清楚。

每张 K0 必须可见并锁定：

- 同一原创年轻女性主角；
- 同一服装轮廓与识别色；
- 同一高地湖岸世界；
- 可运动地面与人物运动方向；
- 同一小型微光风灵；
- 主光线、天气、风向；
- 后续近景/局部特写会使用到的既有元素。

后续多镜头可以切换景别、机位、动作、子空间、光线强度，但默认不得临时新增第二主角、新人群、新大型生物、新大型道具、全新世界或全新服装体系。

---

## 2. Shared persistent asset contract

### Character

原创年轻女性冒险者，动画电影质感；利落中短发；脸部清楚、年轻但不幼态；情绪克制；高辨识轮廓和姿态张力；短披肩/短斗篷；暖红/暗珊瑚为识别色，深蓝灰/墨青为辅助色；下装简洁，腿部与脚步必须可读；不复制任何现成角色。

### World

9:16 竖屏。高地湖岸 / 草坡 / 湖岸石径 / 远山 / 层云属于同一世界系统。空间通透、明亮、治愈，有强空气感、天气层次和真实风向；不复制具体影视或动画场景。

### Companion

小型微光风灵：半透明、轻盈、同一尺度和形态，作为视线引导和运动层次，不抢主角。

---

## 3. K0-A｜Generation A first-shot anchor

### Segment context

- Final BGM A: `0.000–8.700s`
- Generated A: `12s`
- K0 / pre-handle: Gen `0.000–1.200s`
- Emotional start: `空掉 / 发懵 / 情绪尚未完全回到身体`

### Composition

- Shot size: 中景偏中全景，避免纯脸部大特写。
- Character: 右侧三分位，身体微朝左前方。
- Camera: 平视略低，稳定，后续可轻推。
- Body mechanics: 后腿承重，前腿轻触地面并具备下一秒启动条件；一手靠近胸口/衣襟，另一手自然下垂略收紧。
- Face: 头微低，眼神轻微失焦，不夸张哭喊。
- Assets visible: 主角完整核心轮廓、腿部/运动地面、风灵、草坡、湖面、远山、层云、黄昏天光。
- Wind: 发丝、短披肩、草叶出现一致风向。
- Wind spirit: 人物身侧略前方，作为后续引导。

### Next-motion entrance

`抬眼 → 呼吸/肩胸变化 → 轻微重心前移 → 后续切镜`。

### Generation prompt intent

原创动画电影首帧；丰富但克制；核心资产完整；不要新增额外人物或无关大型物件；不要把人物做成静态海报；不要让长衣遮掉腿部动作逻辑。

---

## 4. K0-B｜Generation B first-shot anchor

### Segment context

- Final BGM B: `8.700–15.370998s`
- Generated B: `10s`
- K0 / pre-handle: Gen `0.000–1.500s`
- Function: A→B hard cut 后的新视觉句子，不做 match action。

### Composition

- Shot size: 中景偏中远景。
- Camera: 三分之四侧后方，明显区别于 A 的开场关系。
- Character: 同一主角、同一服装体系；位于中偏右；朝左前远处。
- Body mechanics: 前腿承重，后腿准备跟上；身体比 A 更打开；一手刚从胸前放开或处于回望后收手状态。
- Face / gaze: 视线方向明确，情绪仍翻涌但已经进入“继续往前”的状态。
- Assets visible: 主角、腿部与运动地面、同一风灵、湖岸/山脊、远山、蓝调天空、天边暖余光。
- Wind: 比 A 更明显，但仍保持同一物理方向逻辑。
- Wind spirit: 位于人物前方更远一点，作为后续引导与 Ending 消散铺垫。

### Next-motion entrance

`小步转向/继续一步 → Camera 跟随 → Gen 1.500 后 CUT 进入正式 B1`。

### Generation prompt intent

同一角色和世界必须稳定；用机位/景别/蓝调时刻建立新段差异；不新增额外人物、新动物、新大型道具或新场景体系。

---

## 5. Human K0 Gate

K0-A / K0-B 图生成后，只检查：

1. 同一主角是否稳定、好看、辨识度足够；
2. 第一帧是否已把后续持续核心资产交代完整；
3. 人物是否有明确可执行动作入口，腿部/重心是否可读；
4. 场景是否支持后续近景、局部特写、跟随和大景切换；
5. 风灵是否稳定且不抢戏；
6. A/B 是否同世界但能明显作为两个不同视觉句子；
7. 是否存在模型后续需要“自己补大资产”的缺口。

Gate PASS 后才进入 `Multi-shot Dynamic Prompt`。