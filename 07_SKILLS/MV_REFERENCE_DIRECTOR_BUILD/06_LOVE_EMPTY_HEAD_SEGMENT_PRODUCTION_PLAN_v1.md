# 《爱让人脑袋空空》｜Segment Production Plan v1

> Upstream: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
> Status: `SEGMENT_PLAN_LOCKED / GENERATION_NOT_YET_VALIDATED`
> Principle status: `EXPERIMENT`（本项目先验证，不直接 Promote 为全局 Skill 硬规则）

## 1. 关键区分

**Final BGM Segment Duration != Generated Clip Duration**。

本项目最终成片仍严格服从锁定 BGM：

- Segment A final content：`0.000–8.700s`，长度 `8.700s`
- Segment B final content：`8.700–15.370998s`，长度 `6.670998s`

为了给后期剪辑留安全余量，本轮两段均生成 **10.000s** 视频素材。核心有效动作放在生成素材中段，前后保留 handle；最终只剪取核心区对齐 BGM。

---

## 2. Segment A｜10s generation

### Final BGM task

`0.000–8.700s`

歌词/情绪任务：

`爱 爱 → 爱总是 → 好了疤 → 忘了痛 → 让人脑袋空空 → 直到心破了洞 → 见了红 → 换来步履匆匆`

### Generation layout

- Generated clip: `0.000–10.000s`
- Pre-handle: `0.000–0.600s`（0.600s）
- Core usable window: `0.600–9.300s`（8.700s）
- Post-handle: `9.300–10.000s`（0.700s）

### Edit mapping

`Generated A 0.600s` ↔ `BGM 0.000s`

`Generated A 9.300s` ↔ `BGM 8.700s`

A 段 10s 只提供最小但可用的剪辑冗余：约 18 帧前余量 + 21 帧后余量（按 30fps）。若真实生成后 A 段切点不稳定，再测试 12s 素材；本轮不提前加复杂度。

### Cut-friendly ending

A 的核心区结尾必须形成一个**可硬切的动作标点**，例如：

- 一步明确落地 / 重心完成；
- 人物完成一次转身或抬眼；
- 衣摆/发丝在动作后仍有余韵；
- 镜头达到一个完整构图，而不是卡在半动作。

不要求为 B 做连续匹配动作。

---

## 3. Segment B｜10s generation

### Final BGM task

`8.700–15.370998s`

歌词/情绪任务：

`从开始情有独钟 → 到最后泪眼汹涌 → 承诺全被风吹得 → 无影无踪`

### Generation layout

- Generated clip: `0.000–10.000s`
- Pre-handle: `0.000–1.500s`（1.500s）
- Core usable window: `1.500–8.170998s`（6.670998s）
- Post-handle: `8.170998–10.000s`（1.829002s）

### Edit mapping

`Generated B 1.500s` ↔ `BGM 8.700s`

`Generated B 8.170998s` ↔ `BGM 15.370998s`

B 段尾部保留更长余量，因为它承担整条 MV 的 Ending；后期可从 `无影无踪` 后的动作/风/光余韵中选择最合适的最后一帧，而不必被模型 10s 物理结束点绑死。

---

## 4. A→B Transition｜HARD CUT

正式衔接点固定使用 Timeline 的语义/音乐边界：`BGM 8.700s`。

### Transition policy

- 默认 **Hard Cut / 硬切**。
- 不做 crossfade。
- 不做 morph。
- 不要求首尾动作连续。
- 不为了“丝滑转场”牺牲每段独立画面质量。

### Continuity minimum

硬切仍保留最低连续性：

- 同一原创主角身份锚点；
- 同一整体世界观 / 色彩逻辑；
- 情绪因果连续。

但 B 应主动改变至少一个镜头维度，让硬切看起来是导演选择而不是生成事故：

- 景别变化；或
- 机位角度变化；或
- 人物朝向变化；或
- 光线/空间层次变化。

推荐：A 在“步履匆匆”结束时形成较开构图 / 明确动作完成；B 在“从开始情有独钟”以一个新的中景或三分之四角度重新起势。

---

## 5. 为什么当前项目选择 10s + 10s

### Segment A

最终需要 8.700s。10s 素材留下 1.300s 总余量，虽然不宽裕，但按 30fps 仍有约 39 帧可用于前后裁切，足以完成第一轮验证。

### Segment B

最终需要 6.671s。10s 素材留下约 3.329s 总余量，剪辑自由度充足，尤其适合 Ending。

### 结论

当前项目使用：

`10s Generation A + 10s Generation B → trim handles → hard cut at BGM 8.700s → final 15.370998s MV`

这是当前项目的合理方案，不等于“所有 MV 每段都必须 10 秒”。未来 Skill 只在跨项目验证后决定是否推广“生成素材大于最终有效时长”的 handle 规则。

---

## 6. Next Stage Contract

下一步进入 `Phase F｜Reference Deconstruction`。

必须分别为 A/B 提取：

- lyric/emotion task；
- reference camera grammar；
- movement/weight logic；
- energy curve；
- cut-friendly ending/start；
- 哪些原视频元素只作结构参考、不能照搬。

之后才进入 Animation Director，产出两段对应的 Director Plan，再设计 `K0-A / K0-B`。
