# R2.6｜Dola Expert 多彩图参考失败复盘 + K0/线稿故事板实验

Status: READY_FOR_NEW_TEST
Date: 2026-09-03
Primary surface: DOLA_EXPERT_AGENT
Engine: Seedance 2.5
Duration: 15s
Aspect: 9:16

## 1. Observed source

Input video: user-generated 15.04s Dola Expert output using multiple high-fidelity color reference images for one surreal courtyard sequence.

Technical metadata observed from the returned MP4:
- 720 × 1280
- 24 fps
- 361 frames
- ~15.04 seconds

## 2. Main finding

Multiple fully-rendered color references behaved more like competing target images than a low-level ordered motion plan.

The model preserved visual atmosphere reasonably well, but did not execute the intended four-state director progression as a coherent continuous transformation.

Observed behavior:
- roughly 0–6.2s: first visual state dominates; camera slowly pushes while the next-state inverted architecture gradually appears;
- roughly 6.2–6.6s: major spatial reset / morph-like transition;
- roughly 6.6–11.1s: second visual state dominates with relatively weak development;
- roughly 11.1–11.6s: another morph-like spatial reset;
- roughly 11.6–15s: final state stabilizes and motion decays strongly;
- the intended third-state “crossing / breakthrough” visual peak was not clearly executed as an independent director event.

This is consistent with a failure mode in which high-detail images each contribute their own composition, geometry and finished rendering, causing the model to interpolate between image states instead of following a single-world motion grammar.

## 3. What worked

- overall palette and cinematic atmosphere remained attractive;
- wet-stone reflections, mist and architectural material were fairly coherent;
- first state and final state each produced usable atmospheric footage;
- the video reached a stable, clean final hold.

## 4. What failed for MV use

### 4.1 Reference-role conflict

Every color image simultaneously implied:
- world appearance;
- composition;
- geometry;
- lighting;
- camera state;
- target time-state.

That creates stronger competing signals than a prompt-level chronology can reliably resolve.

### 4.2 Morph instead of event

The upside-down-world change often reads as an opacity / geometry morph rather than a physical or spatially motivated event.

### 4.3 Missing peak

The most important planned state — camera crossing a clear boundary — was largely compressed between reference-state transitions instead of becoming a distinct 2–4s MV peak.

### 4.4 Camera inconsistency across phases

The first ~6s contain a relatively strong push-in; later phases become progressively weaker. Motion energy therefore falls instead of following the intended `observe -> awaken -> reveal -> settle` curve.

### 4.5 Finished-image overconstraint

High-fidelity reference images over-specify what intermediate and later frames should look like. They are useful as visual targets but poor as pure motion/camera instructions when several are supplied together.

## 5. New default hypothesis

Use two assets with deliberately separated responsibilities:

### @Image 1 — HERO K0 / visual authority
Controls:
- final visual identity of the world;
- architecture/materials;
- palette and lighting family;
- first-frame composition;
- main subject/scale when present.

### @Image 2 — LINE STORYBOARD / motion authority
Controls only:
- shot order;
- subject blocking;
- camera path;
- transformation geometry;
- time-phase progression;
- end-state relation.

Do not inherit from the line storyboard:
- line-art rendering;
- grayscale/color treatment;
- sketch texture;
- simplified architecture appearance;
- character appearance.

Authority order:
`HERO K0 visual appearance > LINE STORYBOARD geometry/timing > prompt semantic detail`

## 6. Why line storyboard should be superior

A low-detail storyboard carries strong geometry with weak rendering competition.

The model receives:
- one rich visual answer for “what this film looks like”;
- one simplified spatial answer for “how this 15s shot evolves”.

This is closer to traditional layout / previs separation and matches Seedance multimodal asset-scope principles.

## 7. R2.6 test design

Do NOT reuse the previous upside-down-city sequence for the first validation because its surreal event was already very aggressive.

Test a new Healing Surreal Epic scene with one restrained miracle.

### Creative target

Lyric archetype: `风会来 / 世界轻轻回应我`

World:
- dawn lakeside meadow or flooded quiet terrace;
- cool pearl atmosphere;
- warm low-angle sunlight;
- one very small human silhouette optional;
- grass / shallow water / cloud / long fabric as living-natural motion sources.

Miracle:
A single band of warm wind-light becomes visible only near the peak, traveling through grass/water/fog and revealing a distant luminous path.

### 15s state chain

0–4s `OBSERVE`
- calm credible world;
- slow observe/approach camera;
- natural micro-motion only.

4–9s `AWAKEN`
- one directional wind system begins;
- grass, mist, water and fabric respond coherently;
- camera gently approaches the source direction.

9–13s `REVEAL`
- wind-light becomes visible as the single surreal miracle;
- it passes through the environment and opens a luminous path toward distant horizon;
- strongest 2–4s MV peak.

13–15s `SETTLE`
- light passes away;
- environmental motion continues as residue;
- camera settles into a clean end state.

## 8. Line storyboard format

Preferred: 2×2 monochrome line storyboard, no finished color rendering.

Panel 1 — establish composition and depth.
Panel 2 — wind direction / environmental response arrows.
Panel 3 — reveal geometry and camera approach / passage.
Panel 4 — final composition and clean end.

The storyboard should visibly encode:
- camera arrow/path;
- dominant wind direction;
- foreground/midground/background layers;
- location of the single surreal event;
- final camera endpoint.

Avoid decorative text beyond minimal shot/time labels if labels are necessary.

## 9. Prompt assembly rule for Dola Expert

Header:
- Seedance 2.5
- 15 seconds
- 9:16
- @Image 1 = visual/K0 authority
- @Image 2 = ordered line storyboard controlling motion/camera only

Then:
1. lyric/emotional target;
2. one visual thesis;
3. four-phase state chain;
4. one main camera relationship per phase;
5. physical causality;
6. clean end;
7. max 2–3 true hard constraints.

## 10. Acceptance

R2.6 wins over multi-color reference if it produces:
- no obvious reference-to-reference spatial reset;
- one continuous visual world;
- readable 4-phase progression;
- a clear 2–4s visual peak;
- >= 8 usable seconds OR exceptional >=4s peak plus useful atmospheric material;
- stable visual style inherited from K0 rather than storyboard rendering.

## 11. Production rule status

`K0 + LINE STORYBOARD` remains TRIAL until at least two successful Dola Expert 15s runs show the same advantage.

The prior `multiple high-fidelity color images as ordered storyboard` method is DEMOTED for current Dola Expert MV production because the first observed run showed reference-role conflict and morph-like state resets.