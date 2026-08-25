# Template｜MV Zero-Context Start Prompt v1.2

> 用途：新 ChatGPT/Codex 对话零上下文启动一轮 MV，不要求用户重新解释 R1/R2/R3。

```text
你现在要执行 Tangyuan-AI-Douyin 仓库中的 AI MV 生产流程。

开始前严格读取：
1. 04_HARNESS/workflows/mv.md
2. 04_HARNESS/rules/mv_golden_runtime.md
3. 04_HARNESS/rules/mv_bgm_discovery.md
4. 04_HARNESS/rules/mv_audio_timeline.md
5. 当前 MV Round 的 CURRENT_STATE.md
6. 当前 Stage 需要时再 JIT 读取：
   - 04_HARNESS/rules/mv_human_gates.md
   - 04_HARNESS/rules/mv_editing.md
   - 04_HARNESS/rules/mv_source_normalization.md
   - 04_HARNESS/rules/mv_web_source_roughcut.md
   - 04_HARNESS/rules/mv_subtitle.md
   - 04_HARNESS/rules/ai_video.md

权威顺序：
workflow > runtime rules > current state > round summary/history。
历史 R1/R2/R3 不作为正常 Runtime 内容源；跨 Round 必须继承的经验已经晋升到 Workflow/Rule/Gate。

执行硬规则：
- 从 CURRENT_STATE 指定 Stage 继续，不重复已锁上游；
- 正常单一路径：选歌 -> Douyin-first BGM版本发现 -> BGM片段 -> Audio Timeline Package -> Natural Beat -> Director -> First Frames -> Dynamic -> Dynamic QA -> Shot Normalization -> WEB Source Rough-Cut Gate -> Editor Audio Gate -> Picture Edit -> Subtitle -> Final QA -> Close；
- BGM 原曲/母版获取默认第一方案必须先走真实抖音 music asset：优先从多个实际 aweme 反查 asset id / title / author / direct reference，并用实际解码音频 fingerprint / alignment 验证同版本；
- 只有 Douyin asset 找不到、不可获取、证据不足，或用户明确要求非抖音版本时，才退到公开完整版/其他平台；
- 用户需要更长版本时，也必须先以已验证 Douyin asset 为锚点，再对齐完整发行版后扩展，不能直接按歌名换母版；
- “抖音正在使用/平台原生可用”是版本与平台使用证据，不等同跨平台版权法律保证；
- BGM 锁定后，下一 correctness-critical 硬节点必须是完整 AUDIO_TIMELINE_PACKAGE；未 PASS 不进入任何 time-dependent 下游；
- 缺强证据/工具时明确 BLOCKED，不得用 waveform/BPM 猜测替代时间真值；
- 对 1–3镜/多镜动态素材，W07 后先建立 Atom/Arc Shot Library；无论一镜还是多镜，WEB 正式 Picture Edit 前都必须通过 WEB Source Rough-Cut Gate；
- WEB Rough-Cut 默认继承 R2 已验证基线：720×1280 源统一 `crop=576:1024:72:128 -> scale=720:1280`，即约 1.25× whole-source zoom；同批素材使用同一几何，SAR=1:1，保持9:16；
- WEB Rough-Cut 必须移除 source audio，并抽查第一段、左上最危险帧、右下最危险帧、近景代表帧、最后一段；仍有任一平台生成标记时 Gate 不得 PASS；
- 粗剪只生成 derived proxy，原始生成源永久保留；不得把水印处理拖到 HG04 后或最终润色阶段；
- 抒情/诗意 MV 默认 long-cut first；Anchor Word/歌词起点不等于必须切镜；
- 字幕默认直接复用已锁 R1/WEB R2 baseline，不做每首歌 A/B/C；只有用户明确要求新字幕风格才重开 Style Exploration；
- 字幕底框必须按每句实际 glyph bbox 全量重建，四边统一 padding 并经过全行 geometry QA；
- AI source audio 默认物理移除；锁定 BGM 是唯一音乐真源；
- 局部问题执行 Patch, Don't Cascade，只回最近根因层。

正常固定人工 Gate 只有 5 个：
1. 选歌审美；
2. BGM截取听感；
3. 首帧整组/视觉方向；
4. Picture Edit节奏；
5. Final最终验收。

WEB Source Rough-Cut Gate 是技术硬 Gate，不增加人工 Gate 数量。其余技术 QA 在提交用户之前自己完成。只有 Audio Alignment Exception / Dynamic Regeneration / New Subtitle Style 才增加条件人工 Gate。

每完成 Stage：
- 生成 durable artifact / receipt；
- 更新 CURRENT_STATE / AUTOMATION_MATRIX；
- 只有 Gate PASS 才进入下一 Stage。

不要让我重新解释 R1/R2/R3。按仓库当前权威 Runtime 直接执行。
```
