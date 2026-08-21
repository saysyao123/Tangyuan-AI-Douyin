# WEB R2｜MASTER PLAN v1.0

## Goal

测试网页端 ChatGPT 在不依赖 Codex 的情况下，能否从新歌开始完整推进 AI MV，并记录真实自动化边界。

R1 Golden Sample 只作为质量下限，不限制 R2 的歌曲、人物、世界或视觉概念。

---

# W00｜Bootstrap / Capability Baseline

网页端自动执行：
- 读取当前分支与 `WEB_R2/CURRENT_STATE.md`；
- 读取 `04_HARNESS/workflows/mv.md`；
- 只按 JIT 加载当前阶段需要的规则；
- 列出本对话实际可用能力：GitHub、Web、Image Generation、文件分析、音视频本地处理等；
- 不假设能控制用户本机或 Seedance 外部网站。

Output：
- 更新 `AUTOMATION_MATRIX.md`
- 更新 `CURRENT_STATE.md -> W01`

---

# W01｜Song Discovery / Benchmark Selection

目标：在网页端尽可能自动完成选歌前置研究。

流程：
1. 刷新约 5 个 MV / 音乐观察源的最近约 30 天作品；
2. 优先寻找多个观察源重复出现、并向普通抖音内容扩散的歌曲；
3. 输出 3–5 首强候选；
4. 每首只给用户最必要的信息：歌名 + 真实视频链接 + 简短热度/适配判断；
5. 用户只做审美选择，不要求用户自己研究榜单。

Expected state：`HUMAN_GATE`，因为最终歌曲喜好属于审美决定。

Gate：一首具体 Reference BGM 被选中。

---

# W02｜Reference BGM / Exact Clip Lock

优先级：
1. 网页端可合法获得的实际音频文件；
2. 用户上传完整 MP3/WAV；
3. 公开试听仅用于定位，不伪装成可重新分发音频。

一旦有实际源文件，网页端自动：
- 分析歌曲结构；
- 选择语义完整、适合短 MV 的区间；
- 裁剪试听版；
- 做自然 fade；
- 输出给用户试听。

用户只需判断：`PASS / 重新选段`。

Gate：锁定实际音频文件、起止点、时长、fade。

---

# W03｜Music / Lyric / Beat Analysis

网页端自动完成：
- 精确歌词；
- 情绪曲线；
- 音乐结构；
- Natural Beats；
- 强弱分布；
- 关键歌词视觉机会；
- Opening Hook 候选。

不得为了 5 秒生成单元机械硬切歌词。

Expected state：`AUTO`，用户可选择是否审阅。

---

# W04｜Director + Production Allocation

网页端自动完成：
- 统一视觉概念；
- 世界 / 色彩 / 材质；
- 人物政策；
- Opening Hook；
- 每个 Beat 的主视觉事件；
- 概念视觉单元数量；
- 首帧数量；
- 5 秒动态视频数量；
- 原始动态素材时长与最终成片时长覆盖关系；
- 运镜差异化计划。

必须显式计算动态素材是否足够覆盖锁定 BGM，并保留合理剪辑余量。

用户只做导演方向审美 Gate。

Expected state：`HUMAN_GATE`。

---

# W05｜First Frames

网页端自动：
1. 生成整组完整首帧提示词；
2. 每条都是独立可复制 Prompt；
3. 角色 / 世界锁写进每条；
4. 每张必须是 `0-second dynamic anchor`；
5. 直接使用 ChatGPT Image Generation 生成首帧；
6. 先生成 2–3 张风格锚点，再补齐整组；
7. 自检整组美感、身份、重复度和动态可执行性。

用户只需整组审美确认。

Expected state：`HUMAN_GATE`，生产本身应 `AUTO`。

---

# W06｜Dynamic Prompt Design + External Generation Gate

网页端自动：
- 为所有动态段生成 Seedance 2 mini 5 秒提示词；
- 人物图生视频第一行必须原样使用 `rules/ai_video.md` 的 `***` 前缀；
- 根据歌词与镜头任务选择单镜 / 2–3 镜结构；
- 做整组 Camera Repetition Gate；
- 扩展测试电影常用运镜，但不得全片套同一种结构。

当前网页端若没有直接 Seedance 生成工具：
- 状态标记 `EXTERNAL_REQUIRED`；
- 用户只负责把首帧 + 对应 Prompt 送到 Seedance，并把生成的原始 5 秒视频上传回来；
- 不把这一步伪装成全自动。

Expected state：Prompt `AUTO`；Video generation `EXTERNAL_REQUIRED`。

---

# W07｜Dynamic QA + Retry

收到原始动态视频后，网页端自动：
- 检查人物 / 面纱 / 肢体 / 新增人物 / 场景漂移；
- 检查主视觉事件；
- 检查运镜是否与计划一致；
- 检查整组重复度；
- 判断是否可剪；
- 根因归类：Prompt / First Frame / Model Randomness / Director / Physics Mechanism；
- 只重写失败段，不连带推翻通过段。

Expected state：`AUTO`；用户只负责外部重生成失败段。

---

# W08｜Edit + Subtitle + Final Polish

前提：锁定 BGM + 全部可用视频素材。

网页端自动：
- 建立剪辑时间线；
- 先做 v1；
- 根据动作完整性与音乐卡点做 v2；
- 不机械平均分配每段时长；
- 优先保留 5 秒内部完整动作，必要时用 selective trim + short overlap / transition；
- 生成基础歌词字幕；
- 字幕时间必须来自最终音频，不得按画面段落边界估算；
- 优先 ASR / Whisper；没有本地 ASR 时可使用同版本可靠 LRC + 音频起点换算，并明确方法；
- 烧录字幕；
- Final Polish；
- 生成 ZIP 交付。

Expected state：在素材齐全时 `AUTO`。

---

# W09｜Automation Retrospective / Close

网页端自动输出：
- `AUTOMATION_MATRIX.md` 最终版；
- 完全自动阶段；
- 只需审美 Gate 的阶段；
- 外部平台阻塞阶段；
- 用户实际人工操作列表；
- 可在下一轮消除的人工环节；
- 与 Codex R1 的职责分工建议；
- 是否达到 R1 Golden quality floor；
- 下一轮应提升的 Camera / Subtitle / BGM / Source pipeline 项目。

Round 只有在用户最终验收后才能 `COMPLETE_LOCKED`。
