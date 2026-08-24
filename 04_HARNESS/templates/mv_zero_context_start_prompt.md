# Template｜MV Zero-Context Start Prompt v1.0

> 用途：新 ChatGPT/Codex 对话零上下文启动一轮 MV，不要求用户重新解释 R1/R2。

```text
你现在要执行 Tangyuan-AI-Douyin 仓库中的 AI MV 生产流程。

开始前严格读取：
1. 04_HARNESS/workflows/mv.md
2. 04_HARNESS/rules/mv_golden_runtime.md
3. 04_HARNESS/rules/mv_audio_timeline.md
4. 当前 MV Round 的 CURRENT_STATE.md
5. 当前 Stage 需要时再 JIT 读取：
   - 04_HARNESS/rules/mv_human_gates.md
   - 04_HARNESS/rules/mv_editing.md
   - 04_HARNESS/rules/mv_source_normalization.md
   - 04_HARNESS/rules/mv_subtitle.md
   - 04_HARNESS/rules/ai_video.md

权威顺序：
workflow > runtime rules > current state > round summary/history。
历史 R1/R2 不作为正常 Runtime 内容源；跨 Round 必须继承的经验已经晋升到 Workflow/Rule/Gate。

执行硬规则：
- 从 CURRENT_STATE 指定 Stage 继续，不重复已锁上游；
- 正常单一路径：选歌 -> BGM片段 -> Audio Timeline Package -> Natural Beat -> Director -> First Frames -> Dynamic -> Dynamic QA -> Shot Normalization -> Editor Audio Gate -> Picture Edit -> Subtitle -> Final QA -> Close；
- BGM 锁定后，下一 correctness-critical 硬节点必须是完整 AUDIO_TIMELINE_PACKAGE；未 PASS 不进入任何 time-dependent 下游；
- 缺强证据/工具时明确 BLOCKED，不得用 waveform/BPM 猜测替代时间真值；
- 对 1–3镜/多镜动态素材，W07 后先建立 Atom/Arc Shot Library，再进入最终 Picture Edit；
- 抒情/诗意 MV 默认 long-cut first；Anchor Word/歌词起点不等于必须切镜；
- WEB 带角落水印时，在 Normalization 层整批统一 zoom/crop，保持 9:16 / SAR1:1，并在交付前做左右角风险 QA；
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

其余技术 QA 在提交用户之前自己完成。只有 Audio Alignment Exception / Dynamic Regeneration / New Subtitle Style 才增加条件人工 Gate。

每完成 Stage：
- 生成 durable artifact / receipt；
- 更新 CURRENT_STATE / AUTOMATION_MATRIX；
- 只有 Gate PASS 才进入下一 Stage。

不要让我重新解释 R1/R2。按仓库当前权威 Runtime 直接执行。
```
