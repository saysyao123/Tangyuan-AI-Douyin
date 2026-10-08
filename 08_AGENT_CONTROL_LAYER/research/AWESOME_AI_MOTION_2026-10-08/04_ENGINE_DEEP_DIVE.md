# 引擎和关键源码深读

[返回入口](README.md) · [14 个文件的路径与 blob SHA](evidence/KEY_SOURCE_FILES.json)

本章依据作者 README、导演说明与关键源码重点阅读，未安装或运行这些工程。作者报告的性能和时长只作条件记录。外部 skill 文件仅作研究资料，不自动执行其安装、批准、联网或分工指令。

## 1. ClaudeAnimationBase：角色、相机、检查工具

来源：[仓库](https://github.com/JohnHeibel/ClaudeAnimationBase)。重点文件：`ANIMATION_GUIDE.md`、`src/core.js`、`render.mjs`。p5.js 与 p5.brush 负责绘制，headless Chrome 逐帧输出，ffmpeg 编码。

`core.js` 的关键学习点是以时间为输入组织动作、角色朝向、姿态与相机；跳跃包含预备、伸展、腾空和恢复，不只是修改 y 坐标。随机纹理与绘画抖线按语义元素及绘画帧稳定取样，避免多画一个物体改变后续所有随机结果。相机开始／结束的坐标栈应只应用一次；画面字幕另设屏幕层。

`render.mjs` 明确区分 sheet（采样静帧）、strip（指定区间逐帧）、crop（屏幕裁切）、crop-at（追踪世界点裁切）、stills、clip、frames 和 encode。特别适合检查脚与地面、手与道具，而不是只看全片小图。并行帧与续渲的前提是每帧能独立求值；若含状态累积，就不能直接套用。

局限：水彩笔刷在集成显卡或软件渲染上可能达到每帧数秒。作者“无文字、处处转场”等美术约束只适用于该风格，不适合原封不动写入歌词 MV 规则。

## 2. songbie：一份乐谱驱动动作与声音

来源：[固定版本工程](https://github.com/JohnnyWang8802/songbie/tree/97225eb54a351c9938ad896e04bef7a7020393fb)。以实际取回文件 SHA 为准；目录资源保留其固定提交入口。重点：`score.js`、`render.js`。

房间、钢琴、人物和相机以厘米建模，通过针孔投影在 Canvas 上绘制；遮挡顺序取真实相机距离。音符表同时给采样器和击键动作使用，因而可以检查“听到的键”与“碰到的键”是否相同。故事中融化参数进一步影响脸、身体、围巾、水等相关对象，形成有共同原因的变化。

可以迁移的是事件表、投影和接触关系，不能迁移成“任何照片都可准确绑骨”。作者称 72 秒、24 fps、1080 正方形；README 说一整次渲染在 Apple Silicon 上约 13 分钟，这不是汤圆电脑上的测量。Apple Logic Pro 的采样不随 MIT 代码提供；仓库已有成品音频也不能直接理解为自由再发布。

## 3. Functional Emotions：时间函数与绘画层

来源：[仓库](https://github.com/ledbetterljoshua/functional-emotions-video)。重点：`ANIMATION_GUIDE.md`、`js/lib.js`。作者明确说最终绘画效果不是 p5，而是自定义 WebGL2 stroke renderer。Canvas 的底色层和发光层，经笔触、灯光与后期处理组成画面；共享角色和相机函数保持章节连续。

歌曲时间 t 决定帧，支持单帧独立渲染。歌词对齐使用音频分析与文字序列匹配；应检查原音轨而非相信稿件。README 中 8 章／168 镜头、多人并行与 GPU 加速属于该作者制作记录。本次没有复现其工具链或性能，不把其“镜头一直动”的风格偏好升级为汤圆规则。

## 4. Lemo-Opuscar：导演层与技术层分离

来源：[仓库](https://github.com/lemomo-ai/lemo-opuscar)。重点：`DIRECTOR.md` 和 `TECHNIQUE.md`。导演层回答主题、主角、变化、节奏、动作与声音意图；技术层回答 `render(t)`、时间表、逐帧输出、TTS、采样、合成、混音、字幕与检查。

可取做法：一个世界到屏幕函数；角色绘画曝光、相机运动与根运动分开；一份事件表驱动画面和声音；先联系表、关键动作连续帧，再正常速度带声检查；输出尺寸从布局开始一致，不能只把 16:9 成片裁成 9:16。音效的“动作发生时”比堆 whoosh 更重要。

需要筛除的默认：固定数量不同镜头、经常转场、旁白字幕统一停留公式，以及用听写例外代替原音轨核对。它们有具体风格与任务条件。对已有歌词和被认可镜头，汤圆先保留已确认内容，再做局部试验。代码、样片、风格说明及外部素材的许可范围需要分别核对。

## 5. ant-colony：带因果的镜头与轻量渲染

来源：[工程](https://github.com/buildwithhanif/claude-animation-skill)，重点 `examples/ant-colony/film.mjs`。叶面、蚁道、巢穴剖面有稳定位置关系；主蚂蚁与镜头由时间函数调度，镜头下降是为揭示地下结构。动机来自叙事，而不是规定每隔几秒缩放。音效 cue 与场景动作共用事件时间。

Node 与 ffmpeg 路线可避免浏览器 GPU，适合先研究低成本 2D 动作。不过 README 报告的几十秒渲染属于作者环境；本次没跑，不承诺同样性能。行走动画还要检查路径速度与步幅、脚的接地，不能只采用周期摆腿。

## 6. hand-drawn-canvas-animation：整姿态与曝光

来源：[作者资料](https://github.com/alesha-pro/tools/tree/main/skills/hand-drawn-canvas-animation)。指令强调整姿态图、关键姿态、breakdown、接触和有限曝光表；骨骼可帮助构图，但最终画面要读得出姿态。保持一张图时，线条也应保持；新随机种子属于新的绘画帧，不属于每次重画。

重要边界：接触 IK 到不了目标时，应修动作和位姿，不能通过拉长骨头掩盖错误。先做最难动作，通过正常速度、连续帧和全尺寸局部检查，再扩展其他镜头。有限人物姿态适合汤圆已有动作方向，但淡入淡出只能解决切换外观，不能证明形成了解剖正确的中间姿态。

## 7. 真实交互系统不能一概写成 render(t)

Clearwater 的水面、BLOCKWORLD 和车辆物理依赖前态或输入。若需要任意时间导出，应从固定初态按固定步长重放，或保存检查点。Little Neighbourhood 的工作动作、路径与工具接触值得学习，但实时模拟与离线随机定位是两个问题。

Neon Zenith 的 README 另提示一个工程陷阱：随机 sort 的 comparator 会因执行次数变化消耗不同随机序列。独立对象随机流与 Fisher-Yates 可避免“改一个对象，整座城市变了”；本次依据作者说明，未重跑其统计。

## 8. 其他很具体的经验

- Tessel launchvideo：同一 timeline 输出画面 cue 和合成声音；运动模糊子帧与 mux 后同步检查是有成本的精细项，先预览再全质量。
- Austerlitz：军队／粒子可按时间求值，声音传播延迟与空间声像服务于距离感；历史事实仍需来源，渲染真实感不等于史料准确。
- Evangelion：波形、mel、chroma、节拍等分析数据可驱动 HUD，但分析文件与可播放原始波形的权利不同。
- felt comparison：同提示、同参考、同输入轨迹才是可比较的试验；一次对比不能代表模型在所有任务上的优劣。
- session-story：真实聊天、画面文字和外部分析调用涉及明确数据边界。本次只研究结构，没有读取私人历史、安装该技能或把用户对话上传给第三方。

本章的可采纳项均作为候选假设，具体试验与成功判据见 [05_TANGYUAN_ADOPTION.md](05_TANGYUAN_ADOPTION.md)。
