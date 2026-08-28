# Rules｜MV First-Frame Prompt Precision Optimization v1.2

Status: `ACTIVE / HARD BEFORE FIRST-FRAME GENERATION / LEAN_R1`

## Purpose

After `DIRECTOR_PLAN_LOCKED` and before any formal first-frame generation, every production prompt MUST pass this precision-optimization layer. Raw Director prose, a lightweight template, or chat-memory-only knowledge is not sufficient.

This rule preserves the visual-generation quality validated in previous MV rounds while keeping every first frame usable as a performable 0-second video anchor.

## Authority stack

Before generation:

`LOCKED LYRIC + DIRECTOR PLAN -> PROMPT PRECISION RULE -> REQUIRED REFERENCE STACK -> FORMAL GENERATION PROMPT`

After HG03 acceptance:

`ACCEPTED K0 PIXELS > old prompt > old Director prose`

The required reference stack is:
`04_HARNESS/knowledge/MV_FIRST_FRAME_REFERENCE_STACK.md`

## Mandatory references｜HARD

Every formal first-frame prompt must use all applicable inputs below:

1. Current locked Director Plan / lyric-hit responsibility — creative truth.
2. `MV_FIRST_FRAME_REFERENCE_STACK.md` — mandatory reference stack containing:
   - open-source image-prompt construction reference (`freestylefly/awesome-gpt-image-2`);
   - the user's previously validated deep-character-detail granularity method;
   - the current Face-Completion grid policy.
3. `mv_first_frame_qa.md` — post-generation HG03 machine QA authority.
4. `ai_first_frame_prompt.md` — authoring structure only; it may not lower the quality requirements in this rule.

No reference above may be replaced by generic model knowledge or remembered prose when the repository version is available.

## Required optimization modules｜HARD

Every formal first-frame prompt MUST resolve all applicable modules below in generation-ready natural language. Labels may be used while authoring, but the final prompt must read as one coherent visual instruction rather than a checklist.

### 1. OUTPUT CONTRACT
- exactly one independent 9:16 cinematic still;
- one complete composition;
- no collage, storyboard, poster, typography, logo or watermark.

### 2. LYRIC VISUAL HIT
- define the lyric-specific visual answer that cannot be replaced by a generic beauty shot;
- `pretty but generic = FAIL`.

### 3. K0 PERFORMANCE STATE
Specify the exact physical phase at frame 0:
- body orientation;
- weight distribution / gait phase;
- both hands and their contact state when visible;
- gaze/head direction when visible;
- what action has already started but is not yet completed.

### 4. CHARACTER PHYSIOLOGY / IDENTITY
Use the reference-stack granularity:
- explicit adult age band;
- believable body/head proportion;
- shoulder-neck-waist-hip relationship;
- stable head silhouette, jaw/cheek structure where visible;
- hair construction, wetness and silhouette;
- stable identity cues across the set;
- no celebrity likeness.

Do not mechanically copy old character anatomy. The old user prompt defines descriptive depth, not the identity of the new protagonist.

### 5. SKIN / HUMAN REALISM
Where visible and applicable:
- pore-scale variation;
- fine tonal irregularity and vellus hair;
- realistic moisture/specular behavior;
- local translucency where physically plausible;
- face/ear/neck/arm tonal continuity;
- avoid plastic CGI smoothness and beauty-retouch skin.

### 6. WARDROBE MATERIAL
Specify:
- garment cut and silhouette;
- fiber/material;
- weight and drape;
- seams/folds/cuffs/collar behavior;
- humidity/wind/body-motion response;
- continuity across the set.

### 7. CAMERA OPTICS
Specify:
- shot scale;
- approximate focal-length language;
- camera height / angle;
- perspective purpose;
- depth-of-field behavior;
- which critical objects must remain readable.

### 8. LIGHTING PHYSICS
Specify:
- actual source;
- direction;
- hardness / softness;
- shadow logic;
- exposure protection;
- physically coherent reflected light from water/glass/stone/metal where relevant.

### 9. ENVIRONMENT & DEPTH
Specify:
- foreground / midground / background hierarchy;
- dominant materials and physical state;
- negative space / available action space;
- same-world continuity;
- no impossible perspective unless explicitly conceptual.

### 10. ACTION ENTRANCE & RESIDUE
Specify:
- what moves next;
- available motion direction/space;
- static base that remains stable;
- physical remainder that continues after the main action;
- plausible settled end state.

### 11. QUALITY + NEGATIVE GUARD
Hard checks:
- anatomy/hands/reflections/geometry coherent;
- no duplicate person or reflection-person;
- no random prop drift;
- no staged commercial model pose unless Director explicitly requires it;
- no text/UI/brand contamination;
- no adjective stacking as a substitute for optical/material detail.

### 12. FACE PRIVACY / COMPLETION GRID｜HARD FOR CURRENT WEB/SEEDANCE FACE-COMPLETION PATH
Whenever a readable facial-feature region exists:
- apply `STANDARD_2D_ORTHOGONAL_BLACK_SQUARE_GRID`;
- straight horizontal and vertical black lines forming regular square cells;
- flat, high-contrast and clearly 2D;
- dense enough to remove specific facial-feature identity information while preserving the head/scene at full quality;
- preserve hair, head silhouette, ear/jaw edges when visible, neck, body, wardrobe, lighting, hands and environment at full detail;
- mirror reflection of the same readable face uses the same grid treatment;
- NOT contour-following 3D face mesh;
- NOT pixel mosaic, blur, censor bar, random scribble, solid black mask, helmet or veil;
- rear/wide frames do not invent a frontal face merely to display the grid.

## Open-source reference usage rule

`freestylefly/awesome-gpt-image-2` is used only for transferable prompt-construction patterns such as:
- exact moment;
- camera height / lens / perspective;
- materials;
- light direction and shadow behavior;
- spatial hierarchy;
- physically grounded pose;
- explicit exclusions.

It must never override the current lyric/Director or cause direct copying of a specific protected image, character or visual scene.

## Prompt-writing principle

Convert emotion and Director intent into visible facts. Prefer:
- exact hand contact;
- exact gait/weight phase;
- exact dominant event;
- exact lens/camera relation;
- exact material response;
- exact light source/direction;
- exact motion space and residue.

Do not rely on vague words such as `beautiful / cinematic / premium / emotional / masterpiece` as the primary quality mechanism.

## Hard production sequence

`DIRECTOR PLAN LOCK -> LOAD PROMPT PRECISION RULE -> LOAD REFERENCE STACK -> SYNTHESIZE FORMAL PROMPT -> PRE-GENERATION PRECISION CHECK -> SINGLE-IMAGE GENERATION -> ACTUAL-PIXEL MACHINE QA -> HG03`

Batch generation is not the default when character/world drift risk is material. Generate/review sequentially when needed.

## Pre-generation precision gate

A prompt is `PROMPT_PRECISION_READY` only if all are true:
- lyric-specific visual answer is explicit;
- K0 body/action phase is executable;
- character anatomy/detail reaches the required reference granularity;
- hair/skin/wardrobe are physically specified;
- lens/camera/depth are purposeful;
- source/direction/behavior of light are specified;
- environment has depth/material hierarchy;
- next-action space and residue exist;
- Face Grid is exactly the validated orthogonal 2D treatment when required;
- negative guards cover duplicate-person, hands/reflection/geometry, poster/text and style drift failures.

Any failure means: `PROMPT_PRECISION_NOT_READY` and generation must not begin.

## Acceptance

A formal first frame must simultaneously pass:

`LYRIC HIT + STANDALONE BEAUTY + CHARACTER/WORLD QUALITY + DYNAMIC PERFORMABILITY`

- Pretty but generic = FAIL.
- Correct but visually weak = FAIL.
- Beautiful but static/non-performable = FAIL.
- Detailed but physically incoherent = FAIL.
- Correct prompt but failed actual pixels = REGEN/PATCH BEFORE HG03.
