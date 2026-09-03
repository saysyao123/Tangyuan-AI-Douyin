# R2｜Dola Expert 15s MV Visual Benchmark

Status: READY_FOR_K0_DESIGN
Date: 2026-09-03
Primary surface: DOLA_EXPERT_AGENT
Engine target: Seedance 2.5
Duration: 15s
Aspect: 9:16

## Goal

Judge Dola Expert Mode by the actual MV job: can it produce beautiful, dynamic, lyric-hit source material with enough usable seconds to edit into a music video?

This round deliberately does not use realistic human-performance difficulty as the primary acceptance bar. Human characters are optional. The benchmark focuses on environmental motion, symbolic objects and surreal spatial transformation.

## Why R1 is demoted

R1 tested FACE_HAND / MOVING_CAMERA / PHYSICS with a realistic female character. It produced useful provider evidence:
- A was blocked before confirmed video generation;
- B generated but gait/camera behavior was poor;
- C was blocked before confirmed video generation.

Those findings remain valid for diagnosing Expert-Agent wording and human-motion behavior, but they do not represent the core MV production goal.

## R2 acceptance metrics

For each 15s source record only:

1. LYRIC_VISUAL_HIT — does the image feel specifically born from the lyric/emotional intent?
2. VISUAL_PEAK — is there at least one strong 2–5s peak worth cutting around?
3. USABLE_SECONDS — total clean/editable duration, not binary whole-video success.
4. MOTION_QUALITY — are major motions readable, elegant and physically coherent?
5. SHOT_VARIETY — does the 15s source contain meaningful evolution rather than random change?
6. CLEAN_END — does the source settle into a usable end state?
7. EXPERT_COMPATIBILITY — did the request reach real video generation without irrelevant semantic refusal?

Do not score whether every sentence in the prompt was followed literally.

## R2-A｜ENVIRONMENTAL_MOTION

Lyric/emotion archetype: `风停了，你也无踪`

Visual thesis:
A vast rain-wet stone bridge and valley are driven by one clear wind system. Long pale fabric/ribbons, fog, rain residue and distant warm light all move in the same direction. The wind intensifies, creates a visual peak, then stops abruptly. The entire world loses motion and a distant light disappears into fog.

Why this is useful:
- strong lyric hit without a human actor;
- tests wind / cloth / fog / water residue;
- tests motion escalation and sudden stillness;
- creates natural transition and release footage.

15s structure:
- 0–4s: controlled directional wind establishes motion;
- 4–10s: wind and camera movement build to a strong visual peak;
- 10–13s: wind abruptly dies, cloth falls, fog swallows distant light;
- 13–15s: stable quiet residue / clean end.

## R2-B｜SYMBOLIC_OBJECT_EVENT

Lyric/emotion archetype: `爱像是一场小雨，滴入我回忆`

Visual thesis:
A quiet dark reflective water surface holds one luminous translucent glass flower / paper lantern-like symbolic object. Fine rain begins; every drop produces concentric rings that reveal brief warm fragments of reflected light beneath the surface. As rain intensifies, the rings overlap into a luminous memory field. Then the rain eases and one final ripple expands through the whole frame.

Why this is useful:
- direct lyric metaphor;
- object-centric, no human anatomy;
- tests rain, ripple, reflection and light causality;
- should deliver multiple edit roles: establishing / hit / residue.

15s structure:
- 0–4s: first drops and isolated rings;
- 4–10s: rain intensifies, reflections bloom and overlap;
- 10–13s: visual peak — luminous memory field across water;
- 13–15s: rain fades; one final wide ripple / clean end.

## R2-C｜SURREAL_SPATIAL_TRANSFORMATION

Lyric/emotion archetype: `做了一场梦 / 梦醒以后世界已经改变`

Visual thesis:
A serene impossible landscape begins as a still flooded corridor or stone courtyard at dawn. Reflections behave normally at first. Then the reflection separates from the real architecture, rises like a second transparent world, and the camera moves through the boundary. The inverted reflected world becomes the real world for the final shot.

Why this is useful:
- visually ambitious and shareable;
- tests coherent spatial transformation rather than human motion;
- gives Seedance 2.5 a 15s narrative arc where longer duration should matter;
- creates a clear breakthrough / transition moment useful for MV peaks.

15s structure:
- 0–4s: establish calm real world and reflection;
- 4–9s: reflection detaches and rises; camera approaches boundary;
- 9–12s: camera crosses into the reflected world — primary visual peak;
- 12–15s: new world settles into a stable, beautiful end composition.

## Prompt design contract

Every R2 Expert prompt should be compact and positive-first:

1. `使用 Seedance 2.5；15秒；9:16；使用当前参考图作为第0秒。`
2. One sentence: lyric/emotional target.
3. One primary visual event.
4. Three-phase progression (establish → peak → settle).
5. Camera relationship.
6. Physical residue / clean end.
7. Maximum 2–3 hard constraints if truly necessary.

Avoid:
- long policy-like negative lists;
- repeated anatomy/contact language irrelevant to the visual task;
- asking the Expert Agent to review safety, policy or feasibility before generating;
- multiple competing hero events in the same 15s source.

## Benchmark discipline

- First run only one generation per category.
- Do not patch prompts before reviewing all three first-pass outputs.
- Partial success counts: record usable and peak windows.
- The winning category should then receive a second controlled repeat.
- Only after a repeated success should its prompt pattern be promoted into the MV Harness.

## Decision rule

R2 is successful if at least two of the three categories produce:
- Expert video job successfully reached;
- >= 8 usable seconds out of 15, OR one exceptional >= 4s peak plus additional clean transition material;
- lyric visual hit >= 8/10;
- no dominant failure that makes the whole source unusable.

If that happens, Dola Expert 15s becomes a primary MV material lane even if realistic human-motion tests remain weak.
