# 《爱让人脑袋空空》｜Segment Production Plan v2

> Upstream: `05_LOVE_EMPTY_HEAD_TIMELINE_LOCK_v1.md`
> Supersedes: `06_LOVE_EMPTY_HEAD_SEGMENT_PRODUCTION_PLAN_v1.md`
> Status: `SEGMENT_PLAN_LOCKED / MULTI_SHOT / GENERATION_NOT_YET_VALIDATED`
> Principle status: `EXPERIMENT`

## 1. Hard distinction

`FINAL BGM DURATION != GENERATED MATERIAL DURATION != SHOT DURATION`。

最终成片严格服从 Timeline：

- Segment A final: `0.000–8.700s` = `8.700s`
- Segment B final: `8.700–15.370998s` = `6.670998s`
- A→B final transition: `Hard Cut @ BGM 8.700s`

生成素材长度由导演/剪辑需求决定，只要求单条在当前平台允许的 `5–15s` 范围内。

本项目导演决定：

- Generation A = `12.000s`
- Generation B = `10.000s`
- Optional C = only when edit/scene/coverage requires it; not mandatory.

这不是全局 Skill 固定值。

---

## 2. Multi-shot policy｜HARD FOR CURRENT ROUTE

当前 MV 不采用“一条生成视频 = 一镜到底”。

每条生成素材内部允许并鼓励多镜头：

- shot count 由歌词单元、Beat/Accent、情绪转折和场景需要决定；
- 当前 10–12s 素材建议约 `4–6 shots`，但不是固定配额；
- 每个主要歌词/情绪节点应尽量有明确视觉事件；
- 镜头可以使用 hard cut / motivated cut；不要求模型做丝滑 morph/无缝转场；
- K0 只锚定生成素材的第一个镜头，不代表整条视频保持同一机位；
- Dynamic Prompt 必须包含 shot timeline / cut cues，而不是只描述连续动作。

原则：`LYRIC / MUSIC POINT → VISUAL EVENT → SHOT / ACTION / CAMERA CHANGE`。

---

## 3. Segment A｜12s generation

### Final BGM task

`0.000–8.700s`

歌词：

`爱 爱 → 爱总是 → 好了疤 → 忘了痛 → 让人脑袋空空 → 直到心破了洞 → 见了红 → 换来步履匆匆`

### Handle / core mapping

- Generated A: `0.000–12.000s`
- Pre-handle: `0.000–1.200s`
- Core usable: `1.200–9.900s` = `8.700s`
- Post-handle: `9.900–12.000s`

Mapping:

`Gen A 1.200 ↔ BGM 0.000`

`Gen A 9.900 ↔ BGM 8.700`

### Core BGM markers mapped into generated A

- BGM 0.000 → Gen 1.200
- 1.567 → 2.767
- 3.400 → 4.600
- 4.933 → 6.133
- 6.633 → 7.833
- 7.333 → 8.533
- 8.700 → 9.900

### Recommended internal shot density

A 的核心内容较密，导演目标约 `5 principal shots`，前后 handle 可自然延续首尾镜头，不强制增加剧情事件。

A 结尾在 Gen ~9.900 必须形成 completed action punctuation，供最终 BGM 8.700 硬切。

---

## 4. Segment B｜10s generation

### Final BGM task

`8.700–15.370998s`

歌词：

`从开始情有独钟 → 到最后泪眼汹涌 → 承诺全被风吹得 → 无影无踪`

### Handle / core mapping

- Generated B: `0.000–10.000s`
- Pre-handle: `0.000–1.500s`
- Core usable: `1.500–8.170998s` = `6.670998s`
- Post-handle: `8.170998–10.000s`

Mapping:

`Gen B 1.500 ↔ BGM 8.700`

`Gen B 8.170998 ↔ BGM 15.370998`

### Core BGM markers mapped into generated B

- BGM 8.700 → Gen 1.500
- 10.533 → 3.333
- 12.333 → 5.133
- 13.767 → 6.567
- 15.371 → Gen 8.171

### Recommended internal shot density

B 推荐约 `4 principal core shots` + pre/post handle composition。

B 的任务不是保持 A 的连续机位，而是在 BGM 8.700 之后以新镜头语句重新建立角色，并在后半主动让环境接管 Ending。

---

## 5. A→B final edit

Final edit remains:

`A core → HARD CUT @ 8.700s → B core`

No crossfade / morph / forced match action.

Minimum continuity only:

- same original character identity;
- same world / palette logic;
- emotional causality.

At the cut, intentionally change at least one dimension: shot size / camera angle / facing / light / spatial layer.

---

## 6. Optional additional generated clips

Do not force the project to only 2 generated videos.

Add a third or further `5–15s` source clip only when it solves a concrete edit/director problem, such as:

- a required scene change cannot be reliably contained in A/B;
- a key lyric needs a stronger insert/detail/establishing shot;
- generated A/B lacks a usable cut point;
- shot density or visual hierarchy is insufficient;
- an environment/creature/object insert materially improves the lyric hit.

Additional source clips are coverage, not automatic new narrative segments. Final BGM Timeline remains unchanged.

---

## 7. Skill hypothesis to validate

Candidate future rule, not yet promoted:

`Timeline decides final duration; Director decides generated duration and shot count; editor trims handles.`

`Multi-shot density is driven by lyric/music events, not by a fixed “one clip = one shot” convention.`

Validate through current generation + edit + QA before Promote.