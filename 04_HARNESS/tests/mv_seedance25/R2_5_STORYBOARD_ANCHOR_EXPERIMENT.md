# R2.5｜Dola Expert 15s Storyboard Anchor Experiment

Status: `DESIGN_READY / IMAGE_NOT_YET_CREATED`
Date: 2026-09-03
Provider surface: DOLA_EXPERT_AGENT
Engine: Seedance 2.5
Duration: 15s
Aspect: 9:16

## Hypothesis

A single accepted first-frame/K0 is good at anchoring appearance but weak at describing 15 seconds of future visual evolution.

A four-panel storyboard reference may improve phase readability, shot variety and lyric-hit execution by giving Seedance 2.5 visual anchors for the complete 15s arc.

This experiment is derived from the multi-grid storyboard pattern documented by `liyue-aigc/seedance-2-5-video-director` and must be validated independently on Dola Expert.

## Controlled comparison

Use the same lyric/emotional thesis for both runs.

### CONTROL — SINGLE_ANCHOR
- one normal 9:16 opening image;
- 15s Dola Expert prompt with 4 chronological phases;
- no multi-grid storyboard.

### TRIAL — FOUR_GRID_STORYBOARD
- one 2x2 storyboard image containing four ordered shot panels;
- prompt explicitly states that the image is an ordered storyboard, each panel is one complete shot, and the collage layout must not appear in final video;
- same total duration, lyric intent, world, visual peak and end state as CONTROL.

Do not compare two different creative concepts.

## Recommended first concept

Use the R2-C surreal-space thesis because it benefits most from showing multiple states visually:

Lyric/emotion: `做了一场梦 / 梦醒以后世界已经改变`

### Panel 1 — REAL WORLD / 0-4s
Still flooded stone courtyard at dawn. Architecture and reflection behave normally. Calm pearl-gray light.

### Panel 2 — REFLECTION DETACHES / 4-9s
The reflected architecture begins separating upward from the water as a transparent inverted duplicate world. Real courtyard remains stable below.

### Panel 3 — BOUNDARY CROSSING / 9-13s
Camera approaches and passes through the suspended reflection plane. The two worlds overlap around the lens. This is the only hero transformation.

### Panel 4 — NEW WORLD / 13-15s
The former reflection has become the stable real world. Architecture is now inverted/reoriented yet physically coherent; light and water settle into a beautiful final composition.

## Storyboard image requirements

The 2x2 image is a control asset, not a final MV frame.

- all four panels share one visual world, materials, palette and architecture;
- obvious chronological progression from panel 1 → 2 → 3 → 4;
- no text inside panels if avoidable;
- no real human actor required;
- each panel has a distinct composition/state rather than tiny cosmetic differences;
- panel 3 must communicate the transformation clearly;
- panel 4 must be a clean ending state;
- keep the grid visually readable but do not decorate it as a poster.

## Dola Expert prompt skeleton

```text
使用 Seedance 2.5，生成15秒、9:16竖屏视频。

当前参考图是一张按左上→右上→左下→右下顺序阅读的四格连续分镜板。每一格代表视频中的一个完整阶段/镜头，不把四格拼贴、边框或分镜板布局生成进最终视频。四格共同锁定同一个世界、建筑材质、冷珍珠晨光和镜面水面。

歌词情绪：做了一场梦，梦醒以后世界已经改变。
核心视觉事件：水面倒影逐渐脱离现实，升成第二个透明世界，摄影机穿过两层世界的边界，最终倒影世界成为真实世界。

0-4秒：对应左上格。建立安静、真实的积水庭院，倒影正常，摄影机极慢靠近水面。
4-9秒：对应右上格。倒影中的建筑整体缓慢脱离水面并向上升起，形成透明的倒置世界；水面和真实建筑保持清晰空间关系。摄影机继续接近边界。
9-13秒：对应左下格。摄影机穿过悬浮的倒影平面，现实与倒影短暂重叠，这是全片唯一的主要视觉高潮。
13-15秒：对应右下格。穿越完成，原本的倒影世界成为稳定的新现实；运动逐渐停止，水光和薄雾只保留轻微余韵，落在干净唯美的最终构图。

整个变化遵循连续空间因果：正常倒影 → 脱离 → 形成边界 → 穿越 → 新世界稳定。每个阶段只使用一个主要摄影机运动，不新增第二个竞争性视觉事件。
```

## Evaluation

Record for both CONTROL and TRIAL:
- EXPERT_COMPATIBILITY;
- LYRIC_VISUAL_HIT;
- PHASE_READABILITY;
- SHOT_VARIETY;
- VISUAL_PEAK;
- USABLE_SECONDS;
- MOTION_COHERENCE;
- CLEAN_END;
- COLLAGE_LEAK (whether grid/panel layout appears in output).

## Decision

Promote `STORYBOARD_ANCHOR` only if the storyboard run materially improves phase/shot readability or usable material without introducing dominant collage leakage or discontinuity.

If the storyboard leaks visibly into the output, do not patch it with a large negative list. First test whether a cleaner borderless storyboard image or separate sequential references solve the problem.
