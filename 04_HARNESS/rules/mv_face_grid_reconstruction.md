# Rules｜Square-Grid Face Degrade -> Face Reconstruction v1.0

> Status: `ACTIVE / EXPERIMENT-BRANCH VALIDATED / PROMOTE_RULE_CANDIDATE`
> Scope: `test/mv-oss-optimization-r1` only until OSS close audit.
> Validation source: D02-B S2 generated source accepted by user after direct video review.
> Parent rule: `04_HARNESS/rules/ai_video.md`.

## 1. Purpose

This rule defines the production-safe portrait adaptation path for fictional human characters when the selected image-to-video generator rejects or destabilizes a normal readable face reference.

The validated path is:

`STANDARD SQUARE BLACK GRID FIRST FRAME`
`->` `FIRST ~1.0s FACE RECONSTRUCTION PRIORITY WINDOW`
`->` `NORMAL DIRECTOR ACTION / CAMERA MOTION`

Do not replace this with a face-following mesh, facial-topology wireframe, contour-aware grid, translucent grey mesh, or free-form facial mask unless separately tested.

## 2. Validated finding

D02-B testing showed that a standard square black grid can be treated by the generator as a removable anonymization/occlusion layer more reliably than a grid that follows facial topology.

The successful combination was not merely “make the grid darker”. The full combination was:

1. standard orthogonal square cells;
2. deep black, coarse/dense, high-contrast coverage;
3. visible face identity substantially unreadable at K0;
4. prompt explicitly defines the grid as a temporary independent anonymization layer, not skin/makeup/mask identity;
5. the first ~1.0s is reserved primarily for face reconstruction;
6. large body action and motivated camera motion begin only after face reconstruction is established;
7. the target fictional face is specified in text;
8. after reconstruction, grid residue must be zero and the completed identity must remain stable.

The earlier contour-following / curved facial mesh is NOT the preferred production form for this path because the generator may preserve it as a permanent facial feature.

## 3. First-frame square-grid standard｜HARD RULE

When this path is selected, the accepted first frame must use a standard orthogonal square black grid over every readable face.

Required visual properties:
- straight horizontal and vertical grid lines;
- approximately square cells;
- no curvature designed to trace nose, lips, eyes, cheekbones or jaw topology;
- deep black lines with strong contrast against skin;
- coarse/dense enough that exact facial identity and detailed feature geometry are not reliably readable;
- cover the full visible facial region from forehead through brows/eyes, nose, cheeks, lips, chin and visible jaw area;
- preserve hair, ear outline, head silhouette, neck, body, wardrobe, pose, scene, camera and lighting at full quality;
- the grid is a privacy/anonymization layer only, not a fashionable mask, wireframe VFX, tattoo, makeup, cyber effect or permanent character design.

Reject / regenerate the first frame if:
- eyes/nose/lips remain clearly identifiable through the grid;
- grid lines bend to match facial topology;
- grid is light grey, low-contrast or too transparent;
- coverage is partial when the full face is readable;
- grid becomes a cloth mask or a three-dimensional prop that changes the intended silhouette.

## 4. Face Reconstruction prompt contract｜HARD RULE

For readable-face shots, place face reconstruction before the normal dynamic action blocks.

The prompt must explicitly state:

- the black square grid is a temporary independent anonymization/occlusion layer;
- it is not skin, tattoo, makeup, mask, permanent styling or scan effect;
- during the first approximately `0.0–1.0s`, reconstruct a complete fictional adult face in the same head position and lighting;
- remove the black grid completely;
- by ~1.0s, grid residue = 0%;
- after reconstruction, the grid never returns;
- the reconstructed face remains the same identity through later head turns and motion;
- no face swap, age drift, feature jump, line-art residue, mask peel effect or digital scan VFX.

Do NOT rely only on phrases such as:
- “the grid naturally fades”;
- “complete the face”; or
- “remove the mesh”.

The model must be given both:
1. an explicit removal/reconstruction task;
2. a constrained `FACE IDENTITY TARGET`.

## 5. Reconstruction priority window｜HARD RULE

For normal close / medium human shots:

### Phase 0｜0.0–1.0s
Priority: `FACE RECONSTRUCTION`.

During this window:
- subject motion = `S`;
- camera motion = `S` or near-static;
- environment motion = `S`;
- allow only breathing, tiny weight shift, minimal hair/garment response;
- no large walking step;
- no large turn;
- no strong camera track/yield/orbit;
- no second narrative event.

The purpose is to reduce simultaneous load and let one task resolve first.

### After ~1.0s
Only after the face is established may the prompt execute the source-specific Director action, camera grammar and environmental response.

This does NOT mean every source must visibly freeze for one second. The body remains alive through micro-motion, but the large action is sequenced after reconstruction.

## 6. Face identity target requirements

The target face description should constrain identity without overloading the prompt.

Recommended fields:
- age band / adult status;
- ethnicity / fictional character framing;
- overall face shape;
- brow and eye geometry;
- nose geometry;
- lip geometry;
- natural skin tone and real texture;
- hair structure;
- emotional baseline;
- current scene-light continuity.

Do not use a real person's name or ask the generator to reproduce a real person's face.

For D02-B male baseline, the validated target family is:
- fictional adult East Asian male, late-20s appearance;
- long oval face with slight diamond tendency;
- clean restrained cheekbone and narrow jaw;
- naturally spaced elongated almond eyes, dark-brown iris, only slight outer-corner lift;
- mostly straight natural brows;
- slender straight nose with restrained tip/alar width;
- natural medium lips, lower lip slightly fuller, relaxed mouth corners;
- neutral-warm adult East Asian skin tone with real pores/texture, low-reflective semi-matte finish;
- natural layered black short-to-medium hair;
- calm, warm, restrained, mature attractiveness; no exaggerated idol acting.

Lighting must be reconstructed from the accepted K0 scene, not replaced with beauty-studio lighting.

## 7. Difficult angles

Side / rear-three-quarter / looking-back faces are higher risk than front or mild-three-quarter views.

For these shots:
- keep the current K0 head angle during the first reconstruction window;
- do NOT force the head to turn front just to rebuild the face;
- reconstruct the visible eye relationship, nose perspective, near/far cheek, lip perspective and jaw for the current angle;
- only after reconstruction is stable may the head continue its planned turn;
- do not allow a second face to appear during the turn.

If the face is too small to be meaningfully readable, do not force a visible reconstruction event. Preserve identity through hair/head/body continuity instead.

## 8. Dynamic prompt skeleton integration

This rule does not replace the existing `ai_video.md` control skeleton.

For square-grid character I2V, use this integrated order:

1. `PORTRAIT-SAFE PREFIX`
2. `DIRECTOR TASK / LYRIC HIT`
3. `FACE RECONSTRUCTION / HIGHEST PRIORITY`
4. `FACE IDENTITY TARGET`
5. `FACE LIGHTING CONTINUITY`
6. `HARD FREEZE / NON-NEGOTIABLES`
7. `FRAME-0 STATE / K0`
8. `STATIC BASE`
9. `ONE ALLOWED EVENT`
10. `BOUND / MOTION LIMIT`
11. `MOTION LOAD`
12. `PHASE A = reconstruction priority window`
13. later `PHASES = Director action`
14. `CAMERA`
15. `ENVIRONMENT / PHYSICAL FEEDBACK`
16. `RESIDUE`
17. `SETTLED END STATE / CLEAN ENDPOINT`
18. `SOUND HARD RULE`
19. short `AVOID`

All existing first-frame character-closure, one-event, clean-endpoint and source-audio rules remain active.

## 9. Failure classification

A generation is `FACE_RECONSTRUCTION_FAIL` if any of the following materially persists after the intended reconstruction window:
- black grid remains as the face appearance;
- grid becomes tattoo / makeup / permanent mask;
- incomplete grid removal leaves large residual lines;
- face remains unreadable;
- face changes identity after reconstruction;
- head turn creates a different face;
- reconstruction causes body/scene topology failure severe enough to make the source unusable.

When the rest of the source is usable, classify the failure locally. Do not redesign unrelated Director beats.

## 10. Current promotion status

`SQUARE_GRID_FIRST_FRAME = VALIDATED_ON_D02-B_S2`
`FACE_RECONSTRUCTION_PRIORITY_WINDOW = VALIDATED_ON_D02-B_S2`
`CONTOUR_FOLLOWING_FACE_MESH_AS_DEFAULT = REJECT`
`STABLE_R3_PROMOTION = DEFER_TO_OSS_CLOSE_AUDIT`

Before stable promotion, prefer one additional successful non-front-angle reproduction (D02-B S3 is the current intended cross-angle validation).
