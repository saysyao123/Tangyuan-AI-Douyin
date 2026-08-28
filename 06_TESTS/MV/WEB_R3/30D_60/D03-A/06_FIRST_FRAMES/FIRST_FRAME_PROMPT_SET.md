# D03-A｜First Frame Prompt Set v2｜Precision-Optimized

Status: `READY_TO_GENERATE / HG03_PENDING_PIXEL_QA`
Authority: `05_DIRECTOR/DIRECTOR_PLAN.md`
Prompt rule: `04_HARNESS/rules/mv_first_frame_prompt_optimization.md`
QA rule: `04_HARNESS/rules/mv_first_frame_qa.md`

## Shared character / world / face-grid lock｜K01–K06

All six frames are generated as **six separate independent 9:16 vertical cinematic photorealistic stills**. Never generate a collage, contact sheet, storyboard, multi-panel composition, poster, typography, logo or watermark.

### Same protagonist
- one fictional East Asian adult man only, late-20s to early-30s appearance;
- lean, naturally athletic adult male proportion, long relaxed limbs, shoulders defined but not bodybuilder-broad;
- oval-to-angular head silhouette, clean jaw and cheek structure, natural adult male neck/shoulder ratio;
- short black hair, slightly grown-out top, soft irregular strands, lightly damp from humid pool air, never glossy salon styling;
- restrained physical presence: gaze, breath, hand pressure, gait and pauses carry emotion; no fashion-model pose and no exaggerated crying;
- visible neck, forearms and hands keep realistic skin micro-texture, subtle tonal variation, fine pores/hair, natural humidity sheen and non-plastic specular response;
- no celebrity likeness.

### Same wardrobe
- off-white / warm-ivory lightweight summer knit shirt or thin short-sleeve textured top, relaxed clean collar, no logo;
- fabric reads as real fine cotton/linen-knit blend: visible soft fiber, moderate weight, natural seam and fold behavior, slight humidity response, never shiny synthetic sports fabric;
- charcoal loose straight trousers with realistic drape and knee/hip folds;
- same clothing construction and colors in all six frames; only small natural dampness progression is allowed;
- no jewelry hero prop, no branded sportswear, no costume change.

### Same world
One modernist city indoor swimming club, midsummer evening shortly before closing:
- pale aqua ceramic tile;
- ivory / cool neutral locker faces;
- brushed stainless-steel rail and trim;
- clear pale-cyan pool water;
- wet concrete / wet tile with physically coherent low-gloss reflections;
- amber glass brick and warm sun-white midsummer exterior light;
- interior artificial light gradually becomes cooler and sparser from K01 to K06;
- one controlled deep-red accent may appear only as the lane rope;
- no beach, sea, coastal resort, ancient styling, rain-night noir, neon nightclub or supernatural winter.

### Face privacy / Face-Completion grid｜HARD
For the current Web/Seedance Face-Completion path, whenever a facial-feature region is readable, apply a **standard 2D orthogonal black square grid** directly over that visible face region: straight horizontal and vertical black lines forming dense regular square cells, flat/high-contrast and clearly geometric. It must NOT follow the contours of eyes/nose/mouth like a 3D face mesh. It is NOT a pixel mosaic, blur, censor bar, random scribble, black solid mask, helmet or veil. Hair, head silhouette, ears/jawline when visible, body, wardrobe, lighting, hands and environment remain fully detailed and sharp. Rear/wide frames should not invent a frontal face just to show the grid. Mirror reflections that clearly show the same face must use the same orthogonal grid treatment and remain one coherent reflection of the same protagonist, never a second person.

### Global image-quality logic
- cinematic photorealism based on physical optics/materials, not adjective stacking;
- realistic perspective and anatomy;
- coherent hands/fingers;
- coherent mirror/water reflection geometry;
- protect highlight detail in warm glass-brick daylight and wet surfaces;
- natural fine grain, not digital noise;
- no over-smoothed CGI skin;
- no readable signage/numbers, text, logo, watermark or extra people.

---

## K01｜REPAIR / EMPTY｜`爱总是 好了疤 忘了痛 / 让人脑袋空空`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

这是D03-A第一张正式K0首帧。保持统一角色：同一名二十多岁末至三十岁初的虚构东方成年男性，修长自然的运动型身材，短黑发微湿、发丝有真实不规则层次，米白偏暖的轻薄夏季针织短袖/薄衫，炭灰宽松直筒长裤。衣料必须能看到真实纤维、接缝和自然褶皱，潮湿空气只带来极轻微吸湿感，不要做成光滑运动服。颈部、前臂、手指为真实成人皮肤，有细微毛孔、色差和湿润环境下克制的高光，不要塑料CG皮肤。

当前可见的面部信息采用标准二维正交黑色方格处理：笔直的水平黑线和垂直黑线形成密集、规则、平面的黑色正方格，高对比覆盖可见面部特征区域；不是顺着眼鼻嘴轮廓弯曲的3D面部网格，不是像素马赛克、模糊、黑色整块面罩或乱线。若主要脸部来自镜中倒影，则格子正确覆盖镜中同一人的可见脸部，真人与倒影必须是同一身份，不得生成第二张脸或第二个人。

【歌词视觉命中】
这一张必须把“好了疤，忘了痛”拍成“看似修补过，但裂痕从未消失”，同时让“脑袋空空”的空感来自更衣室深处成排的空柜和镜面里的空空间，而不是抽象粒子或梦境特效。画面本身必须像值得停留的电影剧照，而不是维修动作说明图。

【K0表演状态 / 主视觉事件】
地点是同一现代主义室内游泳馆的更衣室镜面区。人物站在一面全身镜前，身体与镜面保持自然近距离，重心稳定落在一条腿上，肩背有刚停下来的细微放松；镜面只有一条窄而真实的细裂纹，裂纹上覆盖一小片透明防水修补膜。0秒时修补膜的一角已经翘起，他一只手的拇指与食指已经轻轻捏住这个翘起角，是真实“已经开始但尚未剥离”的动作相位；另一只手自然放松，不承担第二主事件。镜中倒影连贯、比例正确，后方成排浅青/象牙色储物柜形成深纵深和大量空位。

【动态入口】
下一秒最自然的动作只有一个：手指缓慢把透明修补膜继续揭开。给薄膜离开镜面的方向留出干净空间；不要让玻璃破碎，不要出现血、伤口、皮肤绷带。动作完成后，薄膜可以离开画面，但镜面的细裂纹仍留在原处，空更衣室在倒影中变得更明确。

【镜头 / 光学】
亲密中景，平视，约50mm电影镜头感，摄影机不贴脸，人物上半身、手指、裂纹、镜中倒影都可读；轻微浅景深但不能把镜面裂纹和手指虚掉。前景可有极少量镜框/湿气层，中景是人物与镜面主事件，背景是重复的空柜纵深。构图不要把人物正中摆成证件照，镜面裂纹与手的动作应成为第一视觉落点。

【光线物理】
盛夏傍晚的暖白金色自然光从一侧琥珀玻璃砖进入，真实穿过/反射到冷一点的更衣室；暖光切过人物头肩和镜面局部，另一侧保持中性偏冷，不做舞台聚光。镜面与潮湿瓷砖出现真实、克制的反射，保护高光细节，不要过曝光晕。

【余韵 / 静态基座】
镜子、储物柜和建筑保持稳定；只有透明薄膜边缘、轻微湿发和镜缘凝结水汽可保留低幅物理余韵。最终可以停在“膜已离开、裂纹还在”的稳定终态。

【禁止】
不要第二人物；不要镜中多一个陌生人；不要破碎玻璃掉落；不要血、伤口、皮肤绷带；不要用手捂脸；不要商业男模摆拍；不要大黑块遮脸；不要3D贴脸网格；不要像素马赛克；不要文字、号码、品牌；不要把整个画面做成低清或故障图。
```

---

## K02｜RED UNDER REFLECTION / HURRY｜`直到心 破了洞 见了红 / 换来步履匆匆`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、文字、Logo、水印。

保持与K01完全同一名虚构东方成年男性、同一短黑湿发结构、同一米白轻薄针织上衣和炭灰宽松长裤、同一现代主义室内游泳馆。人体比例、服装材质和颜色不可变化。人物若在高位机位中脸部仍可辨认，则可见面部区域继续使用标准二维正交黑色方格；若脸部因真实高位广角而自然很小，不要为了展示格子强行放大或扭正脸。

【歌词视觉命中】
把“心破了洞、见了红”转化为水中倒影的胸口被一圈刚起的水纹打开，并让深红色泳道线从水下接近/切入这个位置；红色只能来自真实泳道线，不能是血、红液体或伤口。画面同时必须为下一句“步履匆匆”预留人物可以转身快速离开的真实池边路径。

【K0表演状态 / 主视觉事件】
镜头从泳池上方高位俯视，严格的浅青瓷砖、水面、池边几何成为主要视觉结构。人物真实站在湿润池边，身体完整可读，不要蹲下或跳水；他在水中的同一人倒影必须连续、方向合理。0秒时，倒影“胸口”附近刚出现一个尺寸很小的圆形水纹，处于第一圈刚向外扩展的相位；水下只有一条深红色泳道线经过附近，但此刻不要正好完全穿过水纹中心，给下一秒“红线被水纹揭出/切开倒影”留动作空间。

【动态入口】
下一秒：水纹继续扩散，逐渐与深红泳道线相交，短暂破坏胸口倒影；之后人物才可转身并沿池边进入稳定、目的明确的快走。首帧本身不要已经跑起来，不要跳水，不要制造大水花。湿地面可以在后续留下少量连续脚印，水纹逐渐衰减作为余韵。

【镜头 / 光学】
高位近垂直俯视的广角构图，约28–35mm等效电影镜头感，但避免超广角畸变。画面重点是泳池严格几何、人物与倒影关系、唯一红线。人物不能占满画面；池边必须留出清楚的行走方向和后续侧向跟拍空间。景深足够让人物、水纹、红线和主要瓷砖边界都可读。

【光线物理】
清透浅青池水受到顶部中性灯和远端夏日自然光共同照明；水面高光细碎而真实，红线在水下有自然折射，不要做成发光霓虹。湿瓷砖反射克制，不能像镜子一样过度光滑。

【人物 / 材质真实】
衣服受潮空气影响有真实重量和垂坠，炭灰裤腿在膝部和髋部有自然褶皱；裸露手臂/颈部保持自然皮肤纹理。不要把人物做成游泳选手或运动广告模特。

【禁止】
不要血；不要伤口；不要红色液体；不要多条红线争夺焦点；不要人物落水/游泳；不要大水花；不要第二人物或第二个不一致倒影；不要把水纹做成魔法光环；不要文字、号码、品牌；不要3D面部网格、像素马赛克或整块黑脸。
```

---

## K03｜ONLY ONE / RELEASE｜`从开始情有独钟 / 到最后泪眼汹涌 / 承诺全被风吹得无影无踪`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、文字、Logo、水印。

保持与K01/K02完全同一名虚构东方成年男性：相同头型、短黑微湿发、修长自然比例、相同米白轻薄针织上衣和炭灰宽松长裤。可见侧脸使用标准二维正交黑色方格：直水平线与直垂直线构成规则黑色方格，平面化覆盖可见面部特征区域，不沿鼻梁/眼窝/嘴部轮廓弯曲；不要像素化、模糊、黑色面罩或科幻头盔。

【歌词视觉命中】
“情有独钟”不是甜蜜双人镜头，而是“只有这一条白色系带、只有他一直抓着”；“泪眼汹涌”只用玻璃上的一条真实凝结水痕作为情绪回声，不让人物大哭；“承诺被风吹得无影无踪”则通过同一条无字白带即将被通风气流拉走。整个画面必须高级克制，不能像道具演示。

【K0表演状态 / 主视觉事件】
地点是池边不锈钢扶手与玻璃隔断区域。人物以侧面到侧前方中景站在扶手旁，身体不完全正对镜头；一条很细、无品牌、无文字的白色织物系带已经只绕扶手一次，松开的自由端被轻微气流拉向画面一侧。0秒时，他的手指已经触到并轻轻夹住自由端，手掌没有握拳，力度克制，是真实“仍然舍不得松开”的动作相位；不要画成正在从头打结。另一只手自然下垂。玻璃隔断上有稀疏真实凝结水汽，其中一条很细的竖向水痕可以恰好经过其反射附近，像泪的回声但不是脸上真的流泪。

【动态入口】
下一秒只有一个主动作：通风气流稍微增强，白带的张力增大；手指先停一拍，再自然打开，白带沿预留空方向离开。镜头后续可以短距离向侧边YIELD，让白带有真正离开的画面空间，不追着白带飞。动作结束后只剩空扶手、玻璃水痕和轻微扰动的空气/衣料余韵。

【镜头 / 光学】
侧面中景，约50mm电影镜头感，平视；人物、手指、钢扶手、白带和玻璃水痕都清晰可读，背景泳池形成柔和但真实的空间深度。不要极浅景深到只剩脸；手部必须清楚。构图一侧为人物与扶手，另一侧留出白带退出的负空间。

【光线 / 材质】
暖一点的泳池反射光与远端夏日玻璃砖光落在不锈钢和米白衣料上，钢材高光细而真实；玻璃水汽半透明，不能做成雨窗；衣料纤维和手部皮肤细节自然。水面保持低动态，不抢白带主事件。

【禁止】
不要第二人物；不要情侣倒影；不要信件、戒指、项链、文字承诺；不要在白带上写字；不要夸张哭泣；不要手捂胸口；不要大风把整件衣服吹飞；不要把白带变成长围巾；不要3D脸网格、像素马赛克或黑色整面罩。
```

---

## K04｜OBSESSIVE CORRIDOR｜`我为你 着了魔 发了疯 / 落得心事重重`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、文字、Logo、水印。

保持完全同一名虚构东方成年男性、同一短黑微湿发、同一米白轻薄针织上衣、同一炭灰宽松长裤。人物从后3/4方向为主；只有在侧脸真实可读时，才在可见面部区域应用标准二维正交黑色方格，不要为了显示格子让人物回头看镜头。

【歌词视觉命中】
“着了魔、发了疯”不通过疯癫表演、乱跑或旋转镜头表达，而是用“他一直沿重复的更衣柜通道往前走，空间却反复复制、怎么都走不出去”的空间压力表达；“心事重重”来自稳定步态与重复环境的压迫，而不是捂头或崩溃。

【K0表演状态 / 主视觉事件】
同一游泳馆深更衣柜通道，两侧浅青/象牙色柜门规则重复，纵深很长。人物已经在0秒处处于稳定向前行走的真实步态：身体背向摄影机略偏三分之四，一只脚已经承重、另一只脚正在自然迈向下一步，骨盆和肩膀符合真实行走相位；双臂自然配合步态，不甩手，不跑。画面绝不能让他像站着摆pose。走廊近前景一侧可以有1–2条中性色、微湿的干净毛巾自然垂挂，只作为后续短暂前景遮挡的物理对象，此刻不要遮住主体。

【动态入口】
下一秒人物继续稳定前行；摄影机可沿真实空间轨迹执行FOLLOW -> OVERTAKE -> LEAD，先跟随，再从侧边平移超越，最后略领先到前3/4关系，绝不原地环绕。人物只允许一个很小的视线变化，不允许奔跑、回头多次或情绪爆发。毛巾可在摄影机经过时产生一次短暂自然遮挡，然后回落，成为余韵；储物柜和建筑必须稳定。

【镜头 / 光学】
中远景/中大全景，约35mm电影镜头感，摄影机高度接近胸口到眼线，后3/4观察；强透视引导线从重复柜门延伸到深处。前景毛巾、中景人物、后景无限重复柜门形成明确三层深度。给摄影机侧向超越留出一条真实通道，不要把人物塞在狭窄正中央。

【光线 / 材质】
顶部更衣室灯仍亮但比前面略冷，夏日暖光只在走廊远端或侧面形成少量残余；柜门是哑光涂层，不是镜面；湿地面只有低亮反射。人物衣料在行走中保持真实重量、下摆和裤腿有自然滞后褶皱，湿发只轻微移动。

【禁止】
不要跑步；不要旋转摄影机暗示；不要人物跳跃、撞柜或砸东西；不要柜门自动开合；不要第二人物；不要大量毛巾像幽灵；不要时尚广告走秀；不要夸张低机位英雄感；不要3D面网格、像素化、整脸黑块；不要文字或柜号可读。
```

---

## K05｜HIS LIGHT GOES OUT｜`你却要 失了魂 关了灯 / 和她情意浓浓`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、文字、Logo、水印。

保持同一名虚构东方成年男性、同一服装和同一游泳馆世界。因为这一张是跨越整个泳池的建筑级大全景，人物脸部自然很小，不要强行制造正脸；只有当面部区域真实可辨时才使用标准二维正交黑色方格。人物身份主要通过头发轮廓、身材比例、米白上衣和炭灰长裤连续识别。

【歌词视觉命中】
“关了灯”要有真实单次灯光事件的入口；“和她情意浓浓”绝对不能生成第二人物、情侣影子或暧昧人形，而是用环境中的“成对”表达：远端恰好两盏相邻暖灯 + 两张彼此靠近的空躺椅。人物这边只有一个人、一盏即将熄掉的中性灯，巨大水面把“一个”与“成对”隔开。

【K0表演状态 / 主视觉事件】
非常宽的建筑级构图跨越整座主泳池。人物体量较小但清楚站在画面一侧偏冷区域，姿态稳定，不走动，不指向对岸；他附近上方/侧上方只有一盏仍然亮着的中性偏冷灯，0秒时这盏灯仍亮，作为下一秒唯一灯光动作入口。隔着大面积深蓝黑色水面，对岸远端建筑角落已经存在两盏彼此靠近的暖色灯，其下只有两张靠近放置的空躺椅，没有人。这个成对暖区目前可见但不要占据绝对中心，留给后续镜头横向DISCOVER时逐渐显得明确。

【动态入口】
下一秒人物这边的单盏灯只熄灭一次，不闪烁；人物只做一个很轻的看向对岸动作。摄影机可缓慢横移，让对岸的两盏暖灯和两张空椅关系变得更清楚。灯灭后人物一侧保持暗，不重新点亮；对岸暖区持续稳定，水面倒影轻微晃动作为余韵。

【镜头 / 光学】
超广建筑大全景但避免畸变，约28–35mm电影镜头感，平视或轻微高位，横跨水面的深空间。前景/中景主要是黑蓝水面和低亮反射，人物位于冷侧三分线，远端成对暖区为小而清晰的视觉记忆点。不要近景人物，不要把镜头做成情侣广告。

【光线 / 材质】
馆内整体正在降亮，水面变成深蓝黑但保留真实层次；人物附近中性灯在K0仍给他一点轮廓和米白衣料细节；远端两盏暖灯有真实反射，不做霓虹橙色。湿瓷砖、不锈钢、玻璃砖保持物理材质连续。

【禁止】
绝对不要第二或第三人物；不要情侣、剪影、影子情侣、镜中人；不要灯光闪烁；不要人物指向对岸；不要用爱心形状；不要酒吧/酒店氛围；不要额外暖灯超过明确需要；不要文字、品牌；不要为展示面部方格而把远景人物突然变成大头近景。
```

---

## K06｜SUMMER OUTSIDE / WINTER INSIDE / COVER SELF｜`明明是盛夏时分 / 心却冷的像寒冬 / 亲手把当初真的自己葬送` + tail

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、文字、Logo、水印。

保持与前五张完全同一名虚构东方成年男性、同一短黑微湿发、同一米白轻薄针织上衣和炭灰宽松长裤。可见真实脸部或镜中可见脸部统一使用标准二维正交黑色方格：直水平/垂直黑线形成密集规则方格，不贴合五官曲面，不是3D面网格、像素马赛克、模糊、黑条或整块面罩。镜中倒影必须是同一人物、同一格子处理和同一服装结构，不得生成第二人。

【歌词视觉命中】
“明明是盛夏时分，心却冷得像寒冬”必须由真实建筑光线矛盾完成：远端琥珀玻璃砖外仍是强而温暖的金色盛夏，室内却已经冷青、潮湿、空；不能真的下雪、结冰或出现白气。“亲手把当初真的自己葬送”不拍坟墓、棺材或死亡，而是让他亲手用一条白浴巾逐步覆盖镜中自己的倒影，最终只剩一块安静的白色负空间。

【K0表演状态 / 主视觉事件】
地点回到同一更衣室的全身镜与深柜廊区域。人物全身到中大全身可读，正面对镜子但不是商业摆拍；双脚稳定，肩背略有疲惫的自然下沉。0秒时，一条干净、厚度真实、无字的白色棉质浴巾已经被他用双手举到镜子最上沿，左右手分别抓住浴巾两个上角/边缘，手指结构清楚，浴巾只覆盖镜面最上方一条很窄的区域，镜中大部分同一人物倒影仍然清楚存在。不要一开始就把脸或整面镜子盖住，必须保留“下一秒还可以持续往下覆盖”的动作空间。

【动态入口】
下一秒他用双手稳定、缓慢、连续地把浴巾沿镜面向下放，不甩、不抖、不快速遮挡，直到镜中倒影完全被白色浴巾隐藏。人物本体不消失、不变形。完成后摄影机可以沿更衣柜通道非常缓慢地后退，让人物和被覆盖的镜子逐渐缩小，利用29.780–31.922秒尾奏形成呼吸感。白浴巾边缘在停止后有极轻微自然垂坠，外部盛夏暖光继续存在，这是最终余韵。

【镜头 / 光学】
全身到中大全身，约35–40mm电影镜头感，平视，保持人物、镜面、双手、浴巾和远端玻璃砖同时可读。构图必须留下摄影机后退的深通道；前景可以有少量冷色柜体边缘，中景人物+镜子，后景是深柜廊与远处金色玻璃砖。镜面几何必须严格，不要镜中肢体错位。

【光线物理】
最关键是物理冷暖分区：远端玻璃砖受到强烈但不过曝的盛夏金白光；人物所在室内由冷青顶灯/环境反射主导，皮肤与米白衣料仍保留真实中性色，不要整个人蓝化。湿地面和镜面有低亮冷反射；暖光不能魔法般照亮整个室内。没有雪、霜、可见呼气或超自然冻结。

【人物 / 材质】
白浴巾必须是真实棉织物，有可见纤维、厚度、重力垂坠和边缘，不是纸片或发光白布；人物衣服和皮肤继续维持前五张的材质连续。手指不能融合、不能多指，镜中手的位置必须对应真人动作。

【禁止】
不要坟墓、棺材、葬礼、血或死亡画面；不要下雪、冰霜、白气；不要第二人物；不要镜中生成另一张脸；不要浴巾一开始就盖住整面镜子；不要把人物本人抹掉；不要超自然消失；不要文字、品牌；不要像素马赛克、3D脸网格或黑色整面罩。
```

---

## Pre-generation precision QA｜HARD

Before any image call, verify that every K prompt resolves:

- `OUTPUT CONTRACT`;
- `LYRIC VISUAL HIT`;
- `K0 PERFORMANCE STATE` including body / weight / hands / gaze / action phase;
- `CHARACTER PHYSIOLOGY / IDENTITY`;
- `SKIN / HUMAN REALISM` where visible;
- `WARDROBE MATERIAL`;
- `CAMERA OPTICS`;
- `LIGHTING PHYSICS`;
- `ENVIRONMENT & DEPTH`;
- `ACTION ENTRANCE / STATIC BASE / MOTION SPACE / RESIDUE / SETTLED END`;
- `QUALITY + NEGATIVE GUARD`;
- `STANDARD 2D ORTHOGONAL BLACK SQUARE FACE GRID` when a face is readable.

## Set-level differentiation QA

| Frame | Scale / angle | Dominant visual event | Memory point |
|---|---|---|---|
| K01 | intimate medium / eye-level mirror | fingertips already hold lifted repair film | cracked mirror + empty lockers |
| K02 | overhead wide | first ripple at reflected chest near red lane | aqua geometry + one red line |
| K03 | side medium | fingers already hold one taut white strip | steel rail + white strip + condensation |
| K04 | rear 3/4 medium-wide | established walking gait | repeating locker tunnel |
| K05 | architectural very wide | one cold lamp vs paired warm zone | dark water gap + two lamps/two empty loungers |
| K06 | full medium-wide / mirror-depth | towel already begins covering reflection | hot summer glass brick + cold room + white mirror cover |

No two frames may share the same camera duty + dominant event + spatial scale.

## HG03 actual-pixel rule

Text compliance is not HG03 PASS. After each image is generated, actual pixels must be reviewed for:

`LYRIC HIT + STANDALONE BEAUTY + IDENTITY/WARDROBE/WORLD CONTINUITY + FACE-GRID POLICY + HAND/REFLECTION/GEOMETRY COHERENCE + DYNAMIC PERFORMABILITY`.

Accepted pixels become downstream K0 truth even when they differ slightly from this prompt.
