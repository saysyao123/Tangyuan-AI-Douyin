# 39 个关联仓库逐项技术笔记

[返回入口](README.md) · [对应资源案例](RESOURCE_REVIEW.md) · [README blob 版本记录](evidence/README_SOURCES.json)

每个仓库均取得公开 README，检查其技术分工、复现条件与许可说明。少数深入到代码／导演文件，其余不声称已读完整代码；所有工程均未独立运行。下面为本次归纳，不是作者原文复制。

## billpwchan/neon-zenith

[已读取 README](https://github.com/billpwchan/neon-zenith/blob/main/README.md)；blob `65a4137d44c0a30b0db809439dd96f31bba205a8`。

- **技术与制作思路**：three.js TSL 同一材质源编译到 WebGPU／WebGL2；城市布局、独立对象随机流、近景模型／远景立面层次、烘焙街灯与运行时音频共同组成城市。
- **学习经验与边界**：学习独立随机流、实例化与 LOD，而不是只复制雨和霓虹。首次桌面资产约 130 MB、Blender 源素材另取；作者 GPU 测量不是本次测试。

## cclank/lanshu-create-ai-presenter-video

[已读取 README](https://github.com/cclank/lanshu-create-ai-presenter-video/blob/c24720a85d63b1bd494f6447e48a59384733647b/README.md)；blob `71649dfe0c696c49b8829cf8de2b41ec8daaa7cb`。

- **技术与制作思路**：讲解视频有 presenter 与 styled 两条路线；批准音频作为主时钟，按阶段保存脚本、ASR、视觉计划、渲染和 QA 证据。
- **学习经验与边界**：九种 KV Cache 风格是同主题的不同表达；能借鉴音频锁定与逐阶段收据，不能把数字人、TTS 与知识事实核验省略。

## FavioVazquez/showtime

[已读取 README](https://github.com/FavioVazquez/showtime/blob/main/README.md)；blob `22237709ef64a0f338a26f0f436ad9abf7f547d1`。

- **技术与制作思路**：给 coding agent 使用的本地视频工作室，覆盖分镜、渲染、检查与交付；文档将可见证据、静帧与短预览组织到导演流程。
- **学习经验与边界**：渲染在具体机器发生；无需 API key 的部分不代表所有语音／外部媒体都免费。README 版本较源作品更新，必须分清工具现状和当时案例。

## alexgreensh/anidoodle

[已读取 README](https://github.com/alexgreensh/anidoodle/blob/main/README.md)；blob `d0477826faccf4d49fbf48065c651959f9ada6e5`。

- **技术与制作思路**：将绘画步骤、风格和演奏细节编码；可选多种笔触／材质风格，强调确定性绘制、画面和代码音乐。
- **学习经验与边界**：风格菜单不能替代动作设计；纸张、笔触与绘制曝光应统一。作者的确定性与音频表现声明本次没有执行验证。

## JohnHeibel/ClaudeAnimationBase

[已读取 README](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/main/README.md)；blob `53816fa825aad75212c43f6145abdd77d55c2064`。

- **技术与制作思路**：p5.js／p5.brush 角色模板与导演指南；Chrome 逐帧、ffmpeg 编码、sheet／strip／局部追踪检查。
- **学习经验与边界**：重点深读 core 与 render；统一相机和时间最适合现有问题。软件 GPU 水彩昂贵，先做最难动作短样，风格规则按任务筛选。

## Salmisaari/eudoom-video

[已读取 README](https://github.com/Salmisaari/eudoom-video/blob/a7bb5ed43644cb214bd3546266c8492914177f98/README.md)；blob `6e77d69b34be8afedace70692598b87418af78df`。

- **技术与制作思路**：歌曲改写、音频对齐与印刷式视觉；README 记录初版通宵后十次跟进版本，以及声音方法失败后更换路线。
- **学习经验与边界**：最有用的是保存上个好版本、小步静帧→检查→预览→全片，而不是宣传“一句话”。音轨、歌词、字体和图片各有许可；作者机器多次崩溃不能忽略。

## JohnnyWang8802/songbie

[已读取 README](https://github.com/JohnnyWang8802/songbie/blob/97225eb54a351c9938ad896e04bef7a7020393fb/README.md)；blob `3e0bfa0de14a395acacebb4334d55d3fdc0e9fb8`。

- **技术与制作思路**：厘米建模、针孔投影与蜡笔 Canvas；score.js 同时驱动音频和击键，人物按深度绘制，融化参数作用于多个相关对象。
- **学习经验与边界**：可研究接触与共同事件时钟；Apple 采样不提供，音频重建条件不完整。实际源码重点阅读，不把作者电脑耗时当本次收据。

## charlie947/motion-graphics-skills

[已读取 README](https://github.com/charlie947/motion-graphics-skills/blob/4cd156acdad0483884867c2d5a22268db66099d1/README.md)；blob `3bd7c16c8ddca31a4f57ba8dd2ab4227acae006e`。

- **技术与制作思路**：13 项动效工作流先建立 brand.md 与 MOTION.md，再用于发布片、图表、reel 等；从被拒草稿中形成规则。
- **学习经验与边界**：能借鉴把品牌输入写成明确数据与可见验证。这里是工具包，不是所有展示视频的完整工程；本次没安装其中技能。

## shinshin86/aituber-onair

[已读取 README](https://github.com/shinshin86/aituber-onair/blob/bf3452d0e4b743a40119c9d86ae02ff6bf1c0972/README.md)；blob `a483642bc78f71bf7bedff5179d3672ecb9c6e55`。

- **技术与制作思路**：TypeScript 的 PNG／VRM／Live2D／Inochi2D 等实时角色路线；音频输出驱动口部，模板和资源要求各不相同。
- **学习经验与边界**：加载既有 Live2D 模型与从一张 PNG 自动生成完整 Live2D 不同。需具体模型文件和 LLM／TTS provider；音量驱动嘴动不等于音素同步。

## drcollect/demolition-derby

[已读取 README](https://github.com/drcollect/demolition-derby/blob/f559fc60a7f2ee3a21a4faf77e998ae31ad67c43/README.md)；blob `dd0ab0a16fbae280bfdaebb37475fb5abf8d2976`。

- **技术与制作思路**：Three.js、Rapier 车辆物理、Blender 资产准备、损伤材质与 Web Audio 引擎／碰撞声音。
- **学习经验与边界**：学习动作与音效事件因果；需要准备模型，五辆车不包含在代码许可内。浏览器输入后的音频开启也属于真实验收条件。

## haxzie/p-doom-ft-genmotion

[已读取 README](https://github.com/haxzie/p-doom-ft-genmotion/blob/9e37882332bd132ed0ebf02512c0b3f67ef2a795/README.md)；blob `0eb22e946e9856a3d20b30e3efcb0619d1330238`。

- **技术与制作思路**：project.json 管理场景、时长、画幅与音轨；TypeScript Three.js 场景按帧数求值，共享 beat、字幕、HUD、镜头组件。
- **学习经验与边界**：清楚区分 GenMotion 工具与这段项目；需要编辑器环境和素材。可取单一节拍表，不采用无目的的 camera kick。整体许可缺失时不能默认为 MIT。

## okonio/felt-dot-gpt-vs-opus

[已读取 README](https://github.com/okonio/felt-dot-gpt-vs-opus/blob/7fbaf862bc8b92e481137fc11723a67cd7f881dc/README.md)；blob `d2d93a941826c50814523d48a336849619cf97d9`。

- **技术与制作思路**：同提示、同参考图、相互隔离的模型工程，以程序几何和 shader 创建交互毛毡角色；README 列出形变、眼镜附着与输入比较。
- **学习经验与边界**：比较应固定指针轨迹、设备、窗口和输出要求。单次结果不能概括模型排名；相机和角色造型对比要分开。

## L1vsun/BLOCKWORLD

[已读取 README](https://github.com/L1vsun/BLOCKWORLD/blob/4d33550c023661beda4a012630e5d93819a6677e/README.md)；blob `f42ff54b8fc1149a9efa563f720a40b350f46703`。

- **技术与制作思路**：小型 Three.js 体素世界，程序地形、洞穴、灯光、水与实时输入，分辨率按帧率调节；固定 view URL 可用于截图。
- **学习经验与边界**：静态截图路线和有状态游戏路线不同。自适应分辨率适合交互，离线导出则应固定交付参数，并确定重放方式。

## stefanomainardi/omacrt

[已读取 README](https://github.com/stefanomainardi/omacrt/blob/8a643fdeffc79f7cf965e68c5699caa0e1280771/README.md)；blob `b64bf86bb3d7b493e45b6d21c6ef74dc5b8e1300`。

- **技术与制作思路**：Rust 的真实 CRT 驱动／媒体系统，包括 DRM/KMS、15 kHz 时序、DAC 和 PipeWire；动画展示与运行硬件系统并存。
- **学习经验与边界**：可以研究启动、状态与 UI 叙事，不能把硬件系统当普通浏览器影片直接移植。作品片段不是完整电视运行环境。

## decompwlj/decompwlj3dopus

[已读取 README](https://github.com/decompwlj/decompwlj3dopus/blob/main/README.md)；blob `df3047b852c25e867ee29f42bb9ba94ef3bd2097`。

- **技术与制作思路**：three.js 解释整数序列的 log k、log L、log d；比较视图共享相机，二维／三维过渡和确定时刻导出服务数据理解。
- **学习经验与边界**：视角变化应解释关系，而不是装饰推拉；还需核对数据和 OEIS 条件。README 与数据源许可不能混为一个整体授权。

## iamtechartist/memory-fading-into-watercolor

[已读取 README](https://github.com/iamtechartist/memory-fading-into-watercolor/blob/main/README.md)；blob `0813c3bd797bbeea2a0ab1817c2d920f69ef0932`。

- **技术与制作思路**：README 很短，指出 Tone.js、Web Audio 与 Salamander Piano；源目录关联水彩淡化钢琴作品。
- **学习经验与边界**：现有文档不足以解释完整画面管线和制作过程。可作为材质与音乐联动候选，未查看完整工程源码，不能补写其实现。

## Leonxlnx/claude-launchvideo

[已读取 README](https://github.com/Leonxlnx/claude-launchvideo/blob/claude/launch-video-fictional-product-hdoo2f/README.md)；blob `9d378cbe287996ecb1f509a6fbb2ed43f1e06991`。

- **技术与制作思路**：Remotion 画面与 Python 合成声音共享 timeline 和 cues；子帧累积产生运动模糊，最后独立 mux 并检查同步。
- **学习经验与边界**：先快速预览再高成本子帧；声画同源仍要检查成品对齐。运动模糊可能掩盖错误，接触与文字应另看清晰帧。

## lemomo-ai/lemo-opuscar

[已读取 README](https://github.com/lemomo-ai/lemo-opuscar/blob/main/README.md)；blob `2c609cd004c1dad32ee673c48cd0cfca5f87f3fb`。

- **技术与制作思路**：DIRECTOR 与 TECHNIQUE 分离创作意图和技术工具；Canvas／WebGL 时间函数、事件表、音效、TTS、混音与审看流程。
- **学习经验与边界**：已深读两个说明。保留相机目的、一次投影、动作条带与声画事件，筛除固定镜头数量等不适合汤圆的风格配额；媒体许可单独核对。

## xikhar/spiderbench

[已读取 README](https://github.com/xikhar/spiderbench/blob/main/README.md)；blob `76c746465883b8b62441e1c9ca69a691af24c1b4`。

- **技术与制作思路**：Three.js 浏览器摆荡游戏，Blender 资产、贴图和大量后期；作者通过参考图与反馈指导生成。
- **学习经验与边界**：并非无资产一次指令；离散 GPU 更适合。View-only／非商用／不许再分发的限制意味着它不能按通常开源代码直接合并。

## Nickdevcode/dawnroll

[已读取 README](https://github.com/Nickdevcode/dawnroll/blob/main/README.md)；blob `512a958b991ae33501f3a4082c1587a150c34cfb`。

- **技术与制作思路**：程序生成模型、材质、天空和 Web Audio；游戏还包含教程、保存、商店、多设备与在线功能，README 展示大量开发细节。
- **学习经验与边界**：长 README 表明完整产品远超一段展示。学习反馈与角色动作系统即可；不把在线账户、后端与商业功能纳入本次研究操作。

## wy51ai/floorplan-3d

[已读取 README](https://github.com/wy51ai/floorplan-3d/blob/master/README.md)；blob `c697038b5eb51e10ee41bf6101ae790772d208c5`。

- **技术与制作思路**：Three.js 户型设计，OrbitControls、PointerLock、房间环境与 CSS2D 标签，提供定义户型和漫游。
- **学习经验与边界**：空间理解和从平面到三维的切换可参考。目录较早许可未指定，当前实际 LICENSE 已读到 MIT；两个时间点分别记录。

## bizarro/evangelion

[已读取 README](https://github.com/bizarro/evangelion/blob/main/README.md)；blob `9fbbd8f097940c9b3b8f7c89000f503ec773ec9c`。

- **技术与制作思路**：16 个 HUD plate 读取节拍、onset、包络、mel 和 chroma，按 song time 独立绘帧；原曲需另外获取。
- **学习经验与边界**：适合研究声音可视化，不能直接当完整角色叙事 MV。原始 waveform 可重建但未分发，因为它本身是可播放歌曲副本。

## JimLiu/taohuayuan

[已读取 README](https://github.com/JimLiu/taohuayuan/blob/main/README.md)；blob `b3ab63b0aa07c682197152429caea7971f959f7c`。

- **技术与制作思路**：Vite／WebGL2 场景、导览与自由漫游；资产原件与压缩成品分开，README 提供浏览器测试范围和录屏路线。
- **学习经验与边界**：不是所有场景都从零代码建模；人物模型许可未找到，公开交付应替换。导览剧情和自由漫游的验收指标不同。

## achrefelouafi/ProceduralBuildingsThreeJS

[已读取 README](https://github.com/achrefelouafi/ProceduralBuildingsThreeJS/blob/main/README.md)；blob `0daee62ffb3ac7a8d61ef169b88317ac26b63637`。

- **技术与制作思路**：将 Blender 几何／材质图转为实例化模块和 GLSL，保留多类建筑、室内映射、灯光与天气。
- **学习经验与边界**：程序化建筑不等于没有资产；源图、kit.glb、贴图和 shader 属性都参与。学习分层资产生成和性能成本，不能把渲染风格当模型精度。

## Edd-io/Workspace

[已读取 README](https://github.com/Edd-io/Workspace/blob/dev/README.md)；blob `c66e5835d7734e187de1c8e445b47700ab2185e8`。

- **技术与制作思路**：React/r3f 客户端与 Fastify/Node 服务将 agent 活动、终端、统计和空间关联；Blender／声音资产由脚本生成。
- **学习经验与边界**：可借鉴清楚状态显示，但需要真实代理记录与服务。未读取用户私有会话或启动监控；代码、CC0 声音与 OFL 字体许可分开。

## WinterArc21/Battle-of-Austerlitz-Film

[已读取 README](https://github.com/WinterArc21/Battle-of-Austerlitz-Film/blob/main/README.md)；blob `e99477368d49e96a308e4228ba1a30fc8582a4a6`。

- **技术与制作思路**：WebGL2 地形、军队、雾、粒子、Kuwahara 绘画后期；离线 Kokoro 旁白；音效考虑距离延迟和声像，渲染可续块。
- **学习经验与边界**：镜头与声音解释战场空间值得研究。软件 GPU 报告每帧约 1.7 秒；历史叙述需史料，整体许可与模型文件条件要另核。

## Aureliengmz/clearwater

[已读取 README](https://github.com/Aureliengmz/clearwater/blob/main/README.md)；blob `fb040884358e0e30ac0e2e3baf3a058177e58dad`。

- **技术与制作思路**：单 HTML 原生 WebGL2 水体，使用浮点 render target、Fresnel、吸收、海床与折射焦散；分辨率自动调整。
- **学习经验与边界**：GPU 需求和状态求解不可忽略。任意时刻确定帧需重放或检查点，不能仅把 render(t) 接口包在现有模拟外面。

## JohnHeibel/PDoomVideo

[已读取 README](https://github.com/JohnHeibel/PDoomVideo/blob/main/README.md)；blob `6218e6b7265c54e17a73bd2dee96412e2d422ef3`。

- **技术与制作思路**：章节、角色、歌词和 timeline 共享模块，p5.brush、studio.html 与 Chrome→ffmpeg 分工；支持帧序列续渲。
- **学习经验与边界**：后续 starter 基于这次制作经验。能学章节复用和统一角色，但歌曲与整体授权不能由另一个 MIT starter 反向推定。

## buildwithhanif/claude-animation-skill

[已读取 README](https://github.com/buildwithhanif/claude-animation-skill/blob/main/README.md)；blob `033a0291e204927381165059e4c3298978582dc1`。

- **技术与制作思路**：轻量 Node Canvas 短片、合成声音、sheet／strip／verify 和分阶段 render；例片主蚂蚁沿叶面、蚁道和地下巢穴推进。
- **学习经验与边界**：深读 ant-colony 例片。空间变化有揭示信息的目的；无 GPU 路线可以列为候选，但作者耗时未在本次环境复测。

## ledbetterljoshua/functional-emotions-video

[已读取 README](https://github.com/ledbetterljoshua/functional-emotions-video/blob/main/README.md)；blob `64144d4818de841bbdc4ddd15d7dc5c4f523f00c`。

- **技术与制作思路**：自定义 WebGL2 笔触而非 p5，底画与光层，音频对齐和章节共享库；帧由歌曲时间决定。
- **学习经验与边界**：重点读角色／相机库与动画指南。章节短镜头策略属于作者风格；保持固定镜头也可以有生命感，不照搬“相机永远在动”。

## ChetasLua/little-neighbourhood

[已读取 README](https://github.com/ChetasLua/little-neighbourhood/blob/main/README.md)；blob `be14b3cce9cb59b11806339619f512886706ba94`。

- **技术与制作思路**：单 HTML Canvas 小世界，角色身体执行画线、写字、修水泵等工作；工具尖端与图形揭示一致，有步骤进度和反馈。
- **学习经验与边界**：接触与动作后果优于空转形变。实时模拟与离线随机定位不同；低运动偏好和键盘可访问性也是可借鉴的交付条件。

## qshanx/docs-governance

[已读取 README](https://github.com/qshanx/docs-governance/blob/main/README.md)；blob `a2b1569349345ef07dd74203e826827c21e26925`。

- **技术与制作思路**：文档治理工具，用小型控制骨架、任务流程和证据边界帮助 agent 管理项目文档。
- **学习经验与边界**：关联的是被宣传产品／工具，不能称为该宣传片源工程。可对照本仓库已有治理流程，避免另建重复权威规则。

## Knutsi/app-dplanner

[已读取 README](https://github.com/Knutsi/app-dplanner/blob/d429f176b3b332a14c4909ef51ca5b8b7fc4baa2/README.md)；blob `ef6c50fcf351109915d515ce20ded6cf58a4290f`。

- **技术与制作思路**：Qt 规划软件把步骤、分支、审核、测试、文档、资产和成本关联，代理运行状态也有明确来源。
- **学习经验与边界**：可学习状态和覆盖可追踪性；这是 GPL 产品，不是展示影片引擎。没有安装软件、启动终端或读取实际 agent ledger。

## deckflow/deckuse

[已读取 README](https://github.com/deckflow/deckuse/blob/main/README.md)；blob `e353cbfa0e8d8240056b3654c7e7198b7403debe`。

- **技术与制作思路**：以可追踪选择器与修订编辑 PPTX，尽量保留未知 XML；有 monitor／render，但明说不是完整 PowerPoint 布局或审美引擎。
- **学习经验与边界**：语义变更和视觉检查分开非常有用；工具不能自动证明幻灯片美观。许可为 AGPL，产品演示与其源码范围要分清。

## mrdoob/three.js

[已读取 README](https://github.com/mrdoob/three.js/blob/2db428484342e13fdfa9c2af62d5347da9426d9b/README.md)；blob `7237aa514f305d2e3011a984673c07921076e2b6`。

- **技术与制作思路**：通用三维库，支持 WebGL／WebGPU，另有 SVG／CSS3D addon；示例创建相机、场景、立方体和渲染循环。
- **学习经验与边界**：上游 case 的 three.js 链接是基础库，不是作者游戏工程。离线帧时间、资源和输入重放都需要另外设计。

## heygen-com/hyperframes

[已读取 README](https://github.com/heygen-com/hyperframes/blob/9a27b9f9349b43b9fd194a95ace830d7cbe38b42/README.md)；blob `973727c5af7ea2c8163a95a463f8627c3f8d8495`。

- **技术与制作思路**：HTML／CSS／media 与可定位动画转确定性 MP4；agent 工作流包括计划、编写、lint、预览与渲染。
- **学习经验与边界**：核心可以与角色绘制页整合，但必须证实具体运行环境和时钟接口。这里未执行安装或渲染，不能用框架能力代替项目复现收据。

## heygen-com/hyperframes-community-skills

[已读取 README](https://github.com/heygen-com/hyperframes-community-skills/blob/master/README.md)；blob `0a019dd5c25cbc3b74964938eba72a25c7351f1c`。

- **技术与制作思路**：公开社区技能包含 p5 绘画、字幕与会话故事等不同输入条件；session-story 要让实际消息参与动画与配乐。
- **学习经验与边界**：重点读 session-story 的数据与网络边界。只研究公开源码，不把真实用户对话当素材，不自动执行内部命令。

## alesha-pro/tools

[已读取 README](https://github.com/alesha-pro/tools/blob/main/README.md)；blob `3c566b7f187921b1454ab0a490be76f6694584be`。

- **技术与制作思路**：其中 hand-drawn-canvas-animation 用整姿态、breakdown、曝光表和接触约束做 Canvas 短片；同仓库还有其他图像／视频工具。
- **学习经验与边界**：已读对应说明。适合解决关键姿态问题；不应通过任意骨骼拉伸补接触。本次没有安装同仓库的其他工具。

## simonw/tools

[已读取 README](https://github.com/simonw/tools/blob/main/README.md)；blob `8219541cb09dd14dcc67eefafa94db3739404b32`。

- **技术与制作思路**：通用单页工具集；目录指向 kakapo-party.html，实际读取到该 HTML，使用代码构成鸟、舞步与浏览器互动。
- **学习经验与边界**：只将具体 HTML 作为案例实现入口；不能从工具集首页推断所有作品生成过程。交互输入与音频开启条件需运行时另验。
