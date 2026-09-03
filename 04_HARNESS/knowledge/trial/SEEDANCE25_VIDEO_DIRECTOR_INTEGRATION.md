# Seedance 2.5 Video Director → Lean MV Harness Integration

Status: `TRIAL / DO NOT PROMOTE WITHOUT DOLA EXPERT EVIDENCE`
Date: 2026-09-03
Source project: `liyue-aigc/seedance-2-5-video-director`
Target: Dola Expert Mode → Seedance 2.5 → 15s MV visual material

## Executive decision

Do **not** import the external Skill as the MV runtime or copy its full loading order.

Use it as a Seedance-2.5-specific pattern library. Its strongest reusable ideas fit our Lean Harness when extracted into small conditional modules.

Primary reason:
- external `SKILL.md` is already large and conditionally loads several 4-10KB references;
- our current project is deliberately reducing prompt/context/audit debt;
- many external capabilities (30s exact timeline, Long Video, human acting, dialogue, edit, Clay Renderer) are outside the current Dola Expert 15s MV benchmark.

## High-value patterns to adopt as TRIAL

### 1. ASSET_SCOPE

Reference media must have a scoped role instead of vague `参考这张图` semantics.

Internal contract:

`source + what to borrow + target + active time + protected traits + what not to inherit`

For current Dola Expert image-reference MV use, keep the emitted text short:

`当前参考图只负责世界构图、材质、色调和第0秒视觉状态；后续动态按以下时间链发展。`

If the attachment is a storyboard rather than a literal first frame:

`当前参考图是一张按顺序阅读的四格分镜板，每格代表一个完整镜头，不把四格拼贴当成最终画面。`

Do not emit a full asset table to Dola unless multiple references actually need disambiguation. The table is internal compiler metadata.

### 2. BEAT_STATE_CHAIN

For 15s MV material, prefer readable sequential states over a flat list of actions.

Default MV shape:

- `0-4s ESTABLISH` — establish world / motion rule;
- `4-9s ESCALATE` — increase one main visual relationship;
- `9-13s PEAK / TRANSFORM` — one unmistakable lyric-hit event;
- `13-15s RESIDUE / CLEAN END` — no new hero event; preserve physical residue and editable ending.

Alternative 3-phase form is allowed when the visual event is simpler.

Rules:
- intervals are continuous and equal the requested duration;
- reduce event count before compressing many events into short time;
- every phase ends in a visible state that hands off to the next phase;
- do not score literal timestamp obedience; score whether the intended state chain is readable.

### 3. ONE_PRIMARY_CAMERA_MOVE_PER_BEAT

The external director Skill explicitly favors physically compatible camera/framing and one primary move per beat.

Integrate as a planning heuristic, not a hard prompt rule.

Example:
- establish: locked / slow drift;
- escalate: slow push or lateral track;
- peak: pass through boundary / controlled pullback;
- residue: settle / lock.

Do not simultaneously request orbit + push + crane + whip + zoom in the same beat.

### 4. PHYSICAL_CAUSALITY

For wind, rain, water, cloth, fog, particles, reflection and spatial transformation, write the event as cause → response → outcome.

Examples:

`wind strengthens → long fabric aligns with wind → fog is pushed in same direction → wind stops → fabric loses lift and settles`

`raindrop strikes water → local impact → concentric ripple expands → multiple ripples overlap → rain stops → remaining rings decay`

This is more useful to current MV than anatomy-heavy human-performance modules.

### 5. END_STATE

Every 15s source must intentionally land somewhere.

Acceptable ending:
- motion settles;
- light disappears;
- final ripple expands;
- transformed world becomes stable;
- fog closes space;
- camera stops on a clean composition.

Do not start another major event in the final 2 seconds.

### 6. TRANSITION_VOCABULARY AS CONDITIONAL TOOL

Potentially useful MV transitions from the external library:
- dissolve for dream/memory;
- occlusion for spatial passage;
- match-object for lyrical montage;
- motion relay for continuous transformation;
- zoom-through for nested worlds;
- ink diffusion for eastern poetic imagery.

Rule: transition is loaded only when it performs a lyric/narrative job. Never add one merely to sound cinematic.

### 7. STORYBOARD_ANCHOR — highest-value new experiment

The external project documents a Seedance 2.5 pattern where one multi-grid image is declared as an ordered storyboard and each panel is treated as one complete shot.

This may solve a core 15s MV control problem:
- single K0 locks appearance well but poorly specifies future visual evolution;
- text-only timestamps can drift;
- a four-panel visual storyboard can show the model the intended evolution directly.

This is not yet validated on Dola Expert. Treat it as a dedicated experiment, not a production rule.

## What NOT to import

### Do not import the whole Skill runtime
Reason: duplicates our Director, Runtime, Provider and QA layers and reintroduces context bloat.

### Do not promote Dreamina upload limits as Dola Expert truth
The external capability snapshot is useful Seedance/Dreamina evidence, but current Dola Expert submission behavior remains provider-surface truth for our workflow.

### Do not import human-realism modules by default
Current benchmark optimizes lyric-hit visual material, not face/hand/dialogue realism.

### Do not import broad prohibition lists
Our existing constraint compiler remains authority:
- rewrite positive when possible;
- move parameters to provider controls;
- move detectable defects to QA;
- keep only a small number of high-cost hard constraints.

### Do not infer generation quality from textual test cases
The external repository tests are behavior-contract tests for its Skill. They do not call Seedance and do not prove rendering success. We must validate all adopted patterns on real Dola Expert outputs.

## Prompt Compiler v0.2 candidate

Current six semantic blocks remain intact, with four new internal planning fields:

1. `INTENT / LYRIC HIT`
2. `REFERENCE SCOPE` (new internal module)
3. `START STATE`
4. `BEAT STATE CHAIN` (new internal module)
5. `PRIMARY VISUAL EVENT + PHYSICAL CAUSALITY`
6. `CAMERA RELATIONSHIP`
7. `RESIDUE / CLEAN END`
8. `HARD CONSTRAINTS`

The final Dola prompt does **not** need eight printed headings. Compiler may merge them into compact chronological prose.

## Dola Expert 15s recommended emitted shape

```text
使用 Seedance 2.5，15秒，9:16。当前参考图用于[明确角色]。

歌词/情绪目标：[一句话]
核心视觉事件：[一句话]

0-4秒：[建立状态 + 一个主运动规则 + 相机]
4-9秒：[升级同一关系 + 相机]
9-13秒：[唯一视觉高潮/空间变化 + 因果结果]
13-15秒：[余韵 + 稳定结束]

连续性：[必要时1-2句]
声音：[需要时]
```

Hard negatives remain optional and small.

## Promotion evidence required

A pattern may move from TRIAL to PROVEN only after repeated Dola Expert 15s runs show a material improvement in at least one of:
- lyric visual hit;
- usable seconds;
- visual peak quality;
- motion coherence;
- shot/phase readability;
- repair rate.

No promotion based only on source-project authority or one attractive output.
