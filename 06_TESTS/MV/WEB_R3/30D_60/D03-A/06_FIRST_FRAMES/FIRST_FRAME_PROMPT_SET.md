# D03-A｜First Frame Prompt Set v3｜Production Precision

Status: `READY_TO_GENERATE / HG03_PENDING_ACTUAL_PIXEL_QA`
Authority: `05_DIRECTOR/DIRECTOR_PLAN.md`
Precision rule: `04_HARNESS/rules/mv_first_frame_prompt_optimization.md`
Reference stack: `04_HARNESS/knowledge/MV_FIRST_FRAME_REFERENCE_STACK.md`
QA rule: `04_HARNESS/rules/mv_first_frame_qa.md`

## Production principle

These prompts are formal generation prompts, not Director notes. They deliberately preserve the validated D02-B prompt language: complete visual direction, exact K0 body phase, character physiology, skin/hair/wardrobe material, camera optics, lighting physics, environment depth, action entrance, residue and negative guards.

Generate sequentially as **six independent 9:16 vertical cinematic photorealistic stills**, not a collage/contact sheet/storyboard/poster.

## Shared protagonist lock

Same fictional East Asian adult man in all six frames, late 20s to early 30s, no celebrity likeness. Lean and naturally athletic rather than muscular-model exaggerated; approximately realistic 7.5–8-head adult proportion, shoulders moderately broad, neck long but natural, waist/hips narrow without stylization, long limbs with believable bone and muscle support. Stable oval-to-angular head silhouette, moderately high cheek structure, clean mandibular angle and coherent ear-jaw-neck transition. Short black hair with slightly grown-out top, natural side/front growth direction, irregular strand groups and a few flyaways, lightly damp from humid pool air; never glossy helmet hair.

Where skin remains visible, keep realistic adult male skin: pore-scale variation, fine vellus hair, subtle warm blood-tone and cool-gray transitions, natural ear/neck/forearm tonal continuity, restrained humidity sheen and physically plausible specular response; no over-smoothed beauty skin or plastic CGI gloss.

Same wardrobe in every frame: warm-ivory/off-white lightweight short-sleeve summer knit or thin textured top, relaxed clean collar, real fine cotton/linen-knit fiber, moderate weight, visible seams and soft folds, slight humidity response; charcoal loose straight trousers with believable hip/knee folds and natural drape. No logo, no brand, no jewelry hero prop, no costume change.

## Shared world lock

One modernist city indoor swimming club in midsummer evening shortly before closing. Pale-aqua ceramic tile, cool ivory lockers, brushed stainless-steel rails/trim, clear pale-cyan pool water, wet tile/concrete with controlled low-gloss reflections, amber glass brick and warm sun-white midsummer exterior light. Interior artificial light becomes progressively cooler and sparser from K01 to K06. One deep-red accent may appear only as the real lane rope. No beach, coast, resort, ancient styling, neon nightclub, rain-noir or supernatural winter.

## Face-Completion grid｜HARD

Whenever a readable facial-feature region exists, apply `STANDARD_2D_ORTHOGONAL_BLACK_SQUARE_GRID`: straight horizontal and vertical black lines forming dense regular square cells, flat and high-contrast over the visible facial-feature region. It is not a contour-following 3D face mesh, not pixel mosaic, not blur, not censor bar, not random scribble, not solid black mask, not helmet and not veil. Preserve hair, head silhouette, ear/jaw edges when visible, neck, body, clothing, hands, light and environment at full detail. If a mirror reflection clearly shows the same face, the same reflection must use the same orthogonal grid and remain one coherent reflection of the same protagonist. Rear/wide views do not invent a frontal face just to display the grid.

---

## K01｜REPAIR / EMPTY｜`爱总是 好了疤 忘了痛 / 让人脑袋空空`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

这是D03-A第一张正式K0首帧。同一名虚构东方成年男性，二十多岁末到三十岁初，修长自然的成年男性比例，肩宽适中、颈肩舒展、四肢偏长但有真实骨骼和肌肉支撑，不要九头身时装模特夸张比例。稳定的椭圆偏棱角头型、干净下颌轮廓、自然耳颌颈衔接；短黑发顶部稍长，真实发束方向和不规则碎发，因泳馆潮湿空气轻微湿润。穿固定的暖象牙白轻薄夏季针织短袖/薄衫和炭灰宽松直筒长裤；上衣必须能看见真实棉/亚麻针织纤维、接缝、柔软褶皱和轻微吸湿重量，不要光滑运动面料。颈部、前臂、手指保持真实成人皮肤细节：毛孔、轻微绒毛、自然色差和潮湿环境下克制高光，禁止塑料CG皮肤。

人物可读的面部特征区域覆盖标准二维正交黑色方格：笔直的水平黑线和垂直黑线形成密集、规则、平面的正方格，高对比但只处理面部特征信息；绝对不是顺着眼鼻嘴弯曲的3D贴脸网格，不是像素马赛克、模糊、黑色整块面罩、乱线、头盔或面纱。头发、头型、耳缘、下颌边缘、颈部、身体、衣服、手、镜子和环境全部保持高清完整。镜中若清楚出现同一个人的脸，也必须是同一身份、同样的二维正交方格，不能变成第二张脸或第二个人。

【歌词视觉命中】
把“好了疤，忘了痛”拍成一种非常具体的事实：镜子看似被修补过，但裂纹本身从未消失；“脑袋空空”的空不是抽象特效，而来自镜中人物背后大面积重复的空储物柜、空走道和冷静空间。画面必须先是值得停留的电影剧照，再让观众从裂纹和空空间读出歌词，不要拍成维修教学图。

【K0表演状态 / Primary Event】
地点是同一现代主义室内游泳馆的空更衣室镜面区。男人距离一面全身镜约半臂到一臂，身体不是正中央证件照式站立，而是轻微三分之二关系，重心自然压在一条腿上，另一条腿放松；肩背像刚刚停下来，呼吸克制。镜面只有一条窄、真实、非危险性碎裂的细裂纹，裂纹上贴着一小片透明防水修补膜。0秒时，修补膜已经有一个角翘起，他靠近镜面的那只手用拇指和食指轻轻捏住这个翘角，接触明确但还没有真正撕开；另一只手自然垂落或轻松靠近裤侧，不承担第二主动作。镜中倒影比例、方向、手的位置必须物理一致。

【Action Entrance / Motion Space】
下一秒只有一个主动作：拇指和食指缓慢把透明修补膜继续揭离镜面。必须在薄膜离开的方向留干净负空间，让后续5秒有真实动作路径。不要在首帧里已经把膜撕掉，不要玻璃继续破裂。动作完成后的可稳定终态是：透明膜离开主画面，镜面裂纹仍在，镜中空柜纵深比动作开始时更醒目。

【Camera / Optics】
亲密中景，平视，约50mm电影镜头感；摄影机距离足够让人物上半身、捏膜的手、裂纹和镜中倒影同时可读，而不是大头近景。轻微浅景深，焦点优先落在“手指—透明膜—裂纹—同一倒影”这一条视觉链上，但背景空柜不能完全化成奶油虚化，必须仍能读出大量空位。前景只允许很轻的镜框边缘或水汽层，中景是人物与镜面，背景是重复柜体和空走道。

【Lighting Physics】
盛夏傍晚的暖白金色自然光从画面一侧的琥珀玻璃砖进入，方向明确，真实擦过人物头肩、手背和镜面局部；更衣室内部人工光保持中性偏冷，因此形成暖外光切入冷室内的真实双色关系，而不是舞台打灯。湿瓷砖、镜面、金属边框只产生克制的真实反射；暖光高光必须保留纹理，不要过曝光晕。脸部方格不能改变光源方向，网格下的头部体积仍必须和环境光一致。

【Environment / Depth / Material】
前景：少量镜框/凝结水汽；中景：人物、手、透明膜、裂纹；背景：浅青与象牙色空储物柜重复向深处延伸，地面带真实潮湿低光泽。空间透视必须合理，不要多重镜像，不要无限镜廊。镜边可有一两条很轻的凝结水迹，但不能像雨夜窗户。

【Residue / Settled End】
静态基座是镜子、柜体和建筑；低幅余韵只有透明膜边缘轻颤、微湿发丝、镜缘凝结水汽。最终可以停在“膜已揭开，裂纹仍在”的稳定画面。

【Negative】
不要第二人物；不要镜中额外陌生人；不要破碎玻璃掉落；不要血、伤口、皮肤绷带；不要捂脸、哭喊、砸镜子；不要商业男模硬摆拍；不要大黑块遮脸；不要3D贴脸网格；不要像素马赛克；不要把整个画面降质；不要文字、号码、品牌标识；不要把空柜做成医院或地铁储物柜。
```

---

## K02｜RED UNDER REFLECTION / HURRY｜`直到心 破了洞 见了红 / 换来步履匆匆`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

保持与K01完全同一名虚构东方成年男性：二十多岁末到三十岁初，修长自然、成年人真实比例，短黑发微湿，暖象牙白轻薄针织短袖/薄衫，炭灰宽松直筒长裤；相同服装裁剪、纤维、颜色、体型与头发结构。高位镜头中若面部特征仍真实可读，只在可见面部特征区域使用标准二维正交黑色方格；如果因高位广角脸部自然很小或不可读，不要为了展示格子而扭正脸、放大头部或破坏真实透视。

【歌词视觉命中】
把“心破了洞，见了红”完全放进泳池的真实视觉物理里：水中同一人物倒影的胸口位置刚出现一个小而空心的圆形水纹，水下唯一一条深红色泳道线从附近经过，下一秒水纹扩大才会与红线相交并切开倒影。红色只能来自真实泳道线，不允许任何血、红液体、伤口或魔法光效。画面的另一层任务是给“步履匆匆”留出真实可走的池边路径，而不是首帧里已经奔跑。

【K0表演状态 / Primary Event】
摄影机位于泳池上方高位、近垂直俯视。男人真实站在湿润池边，身体完整可读，双脚都在安全池岸，不蹲下、不跳水；身体略有准备转身的潜在方向，但0秒仍停在水边观察倒影。双手自然，不承担主事件。他在浅青水中的倒影必须连续、方向正确，与真实身体是一人。0秒时，倒影胸口附近第一圈很小的圆形水纹刚刚开始向外扩展；深红泳道线在水下从附近经过，但首帧不要已经完美穿过水纹中心。

【Action Entrance / Motion Space】
下一秒：水纹自然向外扩展，逐渐和深红泳道线相交，短暂切碎胸口倒影；随后人物才转身沿池边进入稳定、目的明确的快速步行。为后续转身和池边侧向移动留下明显空地与方向。首帧不要跑起来，不要脚悬空，不要制造大水花。动作后的余韵可以是水纹逐渐衰减和少量湿鞋印继续向池边远处延伸。

【Camera / Optics】
高位近垂直俯视的广角构图，约28–35mm等效电影镜头感，但透视保持可信，禁止极端鱼眼。画面主要由浅青泳池几何、湿池岸、人物与倒影、唯一红线构成。人物占比不能过大；景深要足够让人物轮廓、水纹、红线和主要瓷砖边界同时清楚。构图中池边必须留出至少一条完整向前的行走通道。

【Lighting Physics】
清透浅青池水同时受到顶部中性室内灯和远端盛夏自然光照明，水面高光细碎而真实；红色泳道线在水下有合理折射、轻微色偏和波动，不发光、不霓虹。人物衣服受到水面微弱青色反射补光，但主光逻辑仍与整个泳馆一致。湿瓷砖低光泽，不要镜面般过度反射。

【Character / Material Realism】
暖象牙白上衣受潮空气影响略有重量，纤维和自然褶皱仍可读；炭灰裤腿在髋部、膝部形成真实垂坠褶皱。裸露颈部、前臂和手保持成人皮肤纹理。不要把人物做成泳衣运动员、健身广告模特或时尚Lookbook。

【Environment / Depth】
高位画面必须保持严格真实的泳池结构：浅青瓷砖网格、池边排水沟、少量不抢焦的不锈钢边件；不要加入救生员、人群、比赛旗、品牌广告、儿童游泳用品。红色只保留一条泳道线作为歌词视觉刀口。

【Negative】
不要血；不要伤口；不要红色液体；不要多条深红主线争焦；不要人物落水、游泳或跌倒；不要大水花；不要不可能的重复倒影；不要第二人物；不要黑色整脸面罩；不要像素马赛克或3D贴脸网格；不要文字、品牌、号码。
```

---

## K03｜ONLY ONE / PROMISE LEAVES｜`从开始情有独钟 / 到最后泪眼汹涌 / 承诺全被风吹得无影无踪`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

保持与前两张完全同一名虚构东方成年男性、同一成年比例、同一短黑湿发、同一暖象牙白轻薄针织上衣、同一炭灰宽松长裤。侧面可见的头型、耳颌颈关系和发丝结构保持稳定。可读侧脸的面部特征区域使用标准二维正交黑色方格：笔直水平/垂直黑线形成规则平面正方格，只处理面部特征信息，不顺着脸部轮廓弯曲，不变成像素马赛克或实体面罩。

【歌词视觉命中】
这一张不是“哭泣写真”。“情有独钟”通过人物只抓住一条细白色无字系带来表达单一执着；“泪眼汹涌”只由玻璃隔断上一条真实凝结水迹与同一人物侧面/反射关系形成克制呼应；“承诺被风吹走”通过白带已经处在可被通风气流带走的真实动作入口完成。整张图必须像干净、克制的电影记忆图，而不是道具演示。

【K0表演状态 / Primary Event】
场景在主泳池池畔的不锈钢扶手与玻璃隔断旁。人物侧向站立，身体与栏杆约成轻微夹角，重心稳定，一只手靠近栏杆：一条细、无品牌、无文字、真实织物/纸纤混合质感的白色窄带已经只绕过不锈钢扶手一次，松端被轻微拉直朝向他的指尖；0秒时，他的拇指和食指已经轻轻压住/捏住松端，但没有打结、没有从零系带。另一只手自然垂落，不握第二件道具。玻璃隔断上只有一条细长凝结水迹从较高位置缓慢下滑，在透视上可从人物侧面附近经过，但不能像真实眼泪直接画在脸上。

【Action Entrance / Motion Space】
下一秒：人物先维持一次很短的指尖压力，随后馆内通风气流对松端产生更清楚的拉力；手指自然打开，让白带沿画面预留的空方向离开。摄影机后续可短距离YIELD让路，但首帧必须给白带离开方向留干净空间。动作结束后的稳定终态是空扶手、松开的手与白带离去方向的空空间；不要追着白带满场飞。

【Camera / Optics】
中景侧面构图，约50mm电影镜头感，平视或略低于眼线但绝不英雄仰拍。人物胸肩、手、白带、不锈钢栏杆和玻璃水迹都可读；景深中等，人物与主道具清楚，泳池与玻璃后方保持真实空间层次。人物不要正中央，白带离开方向必须有明显负空间。玻璃里的反射若出现，只能是同一人物轻微、符合物理规律的单一反射，不能形成第二个人。

【Lighting Physics】
池水的浅青反射从下方/侧下方给衣服和下颌边缘非常克制的冷色补光，主照明仍来自顶部中性灯和远端盛夏暖白自然光。刷纹不锈钢产生线性真实高光，玻璃凝结水迹受光后略亮但不发光。白带材质保持哑光纤维质感，不像塑料丝带。

【Skin / Hair / Wardrobe】
侧面可见的耳缘、颈部、前臂和手指保持真实毛孔、轻微绒毛、色温变化与潮湿高光。微湿短发呈真实成束与碎发，绝不能油亮定型。上衣纤维、袖口、肩部褶皱和湿度响应连续稳定。

【Residue】
静态基座是栏杆、玻璃、泳池和人物站位；低幅余韵是白带被通风拉动、玻璃凝结水迹继续极慢下行、轻微湿发。最终可以停在空扶手和松开的手。

【Negative】
不要第二人物；不要情侣；不要戒指、情书、手机、照片；不要白带上出现文字；不要人物重新系结；不要大哭、眼泪喷涌、捂脸；不要大风吹乱整个场景；不要多条飘带；不要3D面部网格、像素马赛克、黑色整面罩；不要广告摄影姿势。
```

---

## K04｜OBSESSIVE CORRIDOR｜`我为你 着了魔 发了疯 / 落得心事重重`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

保持同一名虚构东方成年男性、同一二十多岁末至三十岁初年龄感、同一修长自然成年比例、同一短黑微湿发、同一暖象牙白轻薄针织短袖/薄衫和炭灰宽松直筒长裤。人物主要是背后三分之二角度；只有真实可读到的少量侧脸区域才使用标准二维正交黑色方格，绝对不要为了展示格子把头扭成正面。

【歌词视觉命中】
“着了魔、发了疯”不通过失控表演、奔跑或疯狂表情，而通过空间本身反复包围他：长而重复的储物柜通道像无法离开的循环；“心事重重”通过稳定但越来越急的前进步态和层层重复透视压迫成立。首帧必须已经是可跟拍的行走相位，而不是站好后准备走。

【K0表演状态 / Primary Event】
地点是同一游泳馆深处的长更衣柜通道。人物已背向摄影机沿通道稳定向前走，后三分之二可见；0秒时一只脚已经完成主要承重/落地，另一只脚正在自然向前摆动，身体重心真实向前过渡，肩背保持克制，不跑、不跳、不转圈。双手自然随步态摆动，其中任何一只手都不握道具。头部方向主要朝前，仅允许非常小的自然侧偏，不看镜头。

【Action Entrance / Camera Motion Space】
下一秒人物继续同一方向稳定快走。首帧必须给摄影机真实的纵向移动空间：后续可从后方FOLLOW，沿真实通道加速，在人物侧边OVERTAKE，再轻微领先到前侧三分之二关系；不能原地绕人物旋转。走廊地面、柜门透视和人物行走线必须支持这条真实摄影机路径。

【Camera / Optics】
中远景/中大全身，后方三分之二观察位，约35mm电影镜头感；摄影机高度接近胸口到眼线之间，保持自然人眼/跟拍透视。重复的青灰/象牙柜门形成强纵深但不能极端广角拉伸。人物不要居中填满；通道前方和侧边都留出移动余量。景深适中，人物清楚，近景柜门边缘和远端通道逐渐软化但结构仍可读。

【Foreground / Midground / Background】
前景：通道一侧只允许1–2条湿润的中性浅色毛巾/浴巾边缘进入画面，作为后续短暂遮挡的真实前景层，但0秒不能遮住人物主体；中景：行走人物；背景：重复储物柜和冷白顶灯深深延伸。不要增加鞋子、包、杂物堆或人群。

【Lighting Physics】
顶灯是线性中性偏冷光，随着通道延伸出现自然亮暗节奏；远端仍可残留一点暖夏日光，但不能把走廊做成霓虹隧道。人物上衣接受冷顶光与少量暖远光混合，褶皱体积与光源一致。柜门表面为半哑光，不像发亮金属。

【Skin / Hair / Wardrobe】
背颈、耳缘、前臂若可见，保持真实成人皮肤细节；短黑微湿发随步态产生低幅滞后，不飘成大风。上衣下摆和裤腿受行走惯性轻微滞后，纤维和折痕真实。

【Residue / Settled End】
静态基座是重复柜体、顶灯和通道；余韵是人物行走后衣摆/裤腿轻微滞后与前景湿毛巾短暂回摆。后续即使摄影机超越人物，重复柜体仍继续包围他，形成“空间没有逃出去”的稳定终态。

【Negative】
不要跑步；不要疯狂大笑、抓头、撞墙；不要人物突然回头正脸；不要摄影机绕圈暗示；不要柜门连续爆开；不要多人；不要镜子生成额外人物；不要杂乱衣物；不要霓虹；不要3D贴脸网格、像素马赛克或整脸黑罩；不要广告式走秀姿势。
```

---

## K05｜HIS LIGHT GOES OUT｜`你却要 失了魂 关了灯 / 和她情意浓浓`

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

保持与前四张完全同一名虚构东方成年男性、同一体型、短黑微湿发、暖象牙白轻薄上衣、炭灰宽松长裤、同一室内泳馆世界。这一张人物因建筑级远景而很小，脸部若自然不可读，不要强行生成正脸或夸张放大的黑格子；只保持同一头发/身体/服装轮廓和身份连续。

【歌词视觉命中】
用纯空间关系完成“关了灯 / 和她情意浓浓”：人物独自在泳池这一侧的冷区，他头顶/附近只有一盏尚未熄灭的中性灯；整个黑蓝水面把他和对岸隔开。对岸远角已经存在恰好两盏靠得很近的暖灯，下方恰好两张靠近的空躺椅，形成一种环境性的“成双”关系，但绝对没有第二、第三个人。观众应从“一盏孤灯 vs 两盏暖灯”直接读出关系，而不是通过情侣剪影。

【K0表演状态 / Primary Event】
超宽建筑级泳池空间。人物在画面一侧偏冷偏暗区域，身体站稳，朝对岸有非常克制的视线关系，双手自然，不指、不挥、不拿道具。他附近那一盏中性灯在0秒仍然亮着，因此后续“关灯”动作尚未发生；对岸两盏暖灯已经稳定亮着，两张空躺椅靠近但保持真实间距，不像摆成心形。

【Action Entrance / Motion Space】
下一秒只发生一次明确灯光事件：人物这一侧附近的中性灯熄灭一次，此后保持关闭，不闪烁；摄影机可沿池边做非常慢的横向DISCOVER，让对岸两盏暖灯/两张空椅在构图中逐渐更清楚，但不要让人物走过去。动作后的稳定终态：人物一侧持续暗，对岸暖双灯持续亮，水面仍隔开两者。

【Camera / Optics】
非常宽的建筑构图，约28–35mm电影广角感，平视到略高于池岸的观察高度，透视自然。人物占画面比例较小但服装亮度和轮廓足以辨认；大面积黑蓝水面是重要负空间和情绪距离。前景可有极少池岸边缘，中景是水面与人物所在冷侧，背景是对岸暖双灯/空椅/琥珀玻璃砖或建筑结构。不能把人物拍成完全看不见的小点。

【Lighting Physics】
盛夏外部暖光仍从玻璃砖/远端开口存在，但主池大厅已经接近闭馆。人物侧为中性偏冷顶灯和水面青色反射；对岸两盏灯是稳定、柔和的暖白/琥珀色实景灯，不是橙色霓虹。水面反射必须与灯位置一致，形成真实细长/破碎光带，不得出现不存在的人形倒影。

【Material / Depth】
清澈泳池在暗部变成深蓝黑但仍保留水质和轻微波纹层次；湿池岸、金属扶手、瓷砖材质仍真实。空躺椅是简洁现代泳馆家具，不带品牌，不堆毛巾、包或人物用品。

【Residue】
静态基座是建筑、水面、对岸双灯/空椅；人物侧灯熄灭后，唯一持续余韵是水面光带轻微晃动和远端夏日光仍存在。不要再发生第二次灯灭。

【Negative】
绝对不要第二或第三人物；不要情侣剪影、影子情侣、人形倒影；不要让两张椅子变成人；不要人物指向对岸；不要多灯闪烁；不要舞台灯、霓虹灯；不要心形构图；不要夸张黑暗到看不见人物；不要文字、标牌、品牌；不要为了黑格子强行给远景人物生成巨大正脸。
```

---

## K06｜SUMMER OUTSIDE / WINTER INSIDE / COVER SELF｜`明明是盛夏时分 / 心却冷的像寒冬 / 亲手把当初真的自己葬送` + tail

```text
只生成1张独立的9:16竖版电影感写实首帧，单一完整构图；禁止拼图、九宫格、分镜表、多联画、海报、信息图、文字、Logo、水印。

保持同一名虚构东方成年男性，二十多岁末至三十岁初，修长自然的成年男性比例，稳定椭圆偏棱角头型和下颌轮廓，短黑发微湿，暖象牙白轻薄夏季针织短袖/薄衫，炭灰宽松直筒长裤；人物身份、服装裁剪和材质不得改变。可见真人脸和镜中同一个人的可读面部特征区域都使用完全一致的标准二维正交黑色方格：直水平线与直垂直线形成规则平面正方格，不能变成3D贴脸mesh、像素马赛克、模糊、黑面罩或面纱。真人和镜中倒影必须保持同一身份、同一头发、同一身体和同一动作，不得生成第二个人。

【歌词视觉命中】
这一张同时承担全片最重要的三个视觉答案，但它们必须由同一个物理动作统一，而不是堆三个隐喻：外部玻璃砖后仍是强烈真实的金色盛夏；人物所在更衣室内部已经变成湿冷、克制的钢青色空间；他亲手把一条干净白浴巾从全身镜顶部往下覆盖自己的倒影，完成“亲手把真的自己葬送”。这里的“葬送”只能是身份/倒影被遮住，绝对不要墓地、棺材、死亡或雪。

【K0表演状态 / Primary Event】
人物站在一面完整全身镜前，身体与镜面保持自然距离，双脚稳定着地，肩背轻微下沉但没有崩溃姿势。双手都必须清楚、合理：左右手分别抓住一条干净白色浴巾的两个上角，浴巾已经被举到镜面顶部，0秒只覆盖镜面最上方很窄的一条区域，绝大部分镜中完整倒影仍然可见。手腕、手指和布料接触关系真实，不允许多手、多指、手穿布。人物头部方向朝镜面，不用哭喊；情绪由双手停顿、肩背重量和仍看见自己的倒影成立。

【Action Entrance / Motion Space】
下一秒唯一主动作：双手缓慢、连续、对称但不机械地把白浴巾沿镜面向下拉，让倒影从头部开始逐步被遮住，直到最终整个人的倒影被盖住。首帧必须为浴巾向下移动保留完整镜面路径，不要一开始就遮住大半。动作结束后，摄影机才可沿深更衣通道缓慢后退，让被白浴巾覆盖的镜面和人物逐渐变小；最后音乐尾息可停在稳定远一点的画面，不新增第二动作。

【Camera / Optics】
全身到中远景之间，平视，约35–40mm电影镜头感；摄影机位于更衣室通道轴线上但不要死板完全对称，人物和全身镜是中景主事件，身后/一侧必须留出真实的深通道用于最终摄影机后退。景深中等，人物、双手、浴巾边缘、镜中倒影和远端暖玻璃砖都必须可读；不能只把脸拍清楚而把动作手虚掉。

【Lighting Physics】
这是全片最明确的物理冷暖对比。远端/侧后方琥珀玻璃砖外仍是强烈、真实、偏白金的盛夏傍晚光，玻璃砖产生受控暖透光；人物所在室内人工光明显更少、更冷，为钢青/中性冷白，但不能变成蓝色霓虹。暖外光可以在地面、镜缘、人物一侧形成微弱暖反射，而主体大部分仍处在冷室内体积中。不要雪、冰霜、白气或超自然冻结。白浴巾受冷光和少量暖反射影响应呈真实布料明暗，而不是发光白板。

【Skin / Hair / Wardrobe】
耳缘、颈部、前臂、双手保持真实毛孔、细微绒毛、血色/冷灰过渡和潮湿环境下自然高光；面颈手臂色调连续。短黑发因潮湿略成束，仍有真实碎发。上衣棉/亚麻针织纤维、袖口、肩部和腰部褶皱真实；炭灰裤子垂坠自然。白浴巾有清楚织物纤维、厚度、边缘和重力下垂，不能像纸片或窗帘。

【Environment / Depth】
前景可有极少量湿地面或柜门边缘；中景是人物、全身镜和白浴巾；背景是深更衣柜通道和远端琥珀玻璃砖后的盛夏光。镜面必须是单一真实镜面，不要镜中镜无限复制；储物柜、湿地面、金属边缘保持同一泳馆材质体系。

【Residue / Settled End】
静态基座是镜面、柜体、玻璃砖和建筑；主要动作后余韵是浴巾因重力极轻回摆、微湿发丝和地面冷暖反射。最终稳定终态：镜中倒影完全被白浴巾覆盖，外部仍然是盛夏暖光，室内仍然冷，世界没有因为他而改变。

【Negative】
不要第二人物；不要镜中额外陌生人；不要墓地、棺材、坟墓、死亡尸体；不要雪、冰、白气、超自然冻结；不要人物把浴巾盖到自己真实脸上；不要首帧已经遮住大半镜子；不要多手、多指、手穿布；不要浴巾像纸或塑料；不要大哭、跪地、砸镜；不要3D贴脸网格、像素马赛克、整块黑面罩；不要文字、品牌、广告；不要过曝金光或霓虹冷光。
```

---

## Pre-generation precision check｜v3

All six prompts must pass before generation:
- lyric-specific visual answer: PASS by design;
- exact K0 action phase: PASS by design;
- character physiology / hair / skin / wardrobe granularity: PASS by design;
- camera optics and physical lighting: PASS by design;
- foreground/midground/background hierarchy: PASS by design;
- action entrance / available motion space / residue / settled end: PASS by design;
- Face-Completion grid policy: embedded per visibility;
- no second-person literalization in K05: locked;
- set differentiation: intimate mirror / overhead pool / side rail / rear corridor / architectural wide / full-body mirror finale;
- actual-pixel hands, reflection, geometry, beauty and identity remain mandatory after each generation.

Generation order: `K01 -> machine visual check -> K02 -> ... -> K06 -> set QA -> HG03`.
