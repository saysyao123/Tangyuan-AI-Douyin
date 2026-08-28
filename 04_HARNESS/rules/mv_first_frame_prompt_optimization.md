# Rules｜MV First-Frame Prompt Precision Optimization v1.1

Status: `ACTIVE / HARD BEFORE FIRST-FRAME GENERATION / PROMOTED_FROM_OSS_OPT_R1`

## Purpose

After `DIRECTOR_PLAN_LOCKED` and before any formal first-frame generation, every production prompt MUST pass this precision-optimization layer. Raw Director prose or the lightweight structural template alone is not sufficient.

This rule exists to preserve the visual quality already validated in D02-B while keeping the first frame performable as a 0-second video anchor.

## Authority

Creative authority order:

`LOCKED DIRECTOR PLAN / LYRIC HIT -> THIS PROMPT OPTIMIZATION RULE -> GENERATED K0 PIXELS -> HG03 QA`

After HG03 acceptance:

`ACCEPTED K0 PIXELS > old prompt > old Director prose`

## Mandatory prompt references

1. Use `freestylefly/awesome-gpt-image-2` only as a structural/high-quality image-prompt reference library: photography, character, architecture and scene prompt construction. Do not copy a specific copyrighted style or scene.
2. Use the previously validated deep-character-detail method as a granularity reference: age band, skull/face proportion, eyes/brows/nose/lips when visible, hair construction, skin micro-texture, body proportion, wardrobe fiber/cut/fold behavior and lighting-volume continuity. Adapt to the current character; never copy the old identity.
3. The locked Director Plan remains the lyric/world authority.
4. `mv_first_frame_qa.md` remains the post-generation HG03 machine QA authority.

## Required optimization modules｜HARD

Every formal first-frame prompt MUST resolve all applicable modules below in generation-ready natural language. Section labels may be used for authoring, but the final prompt must read as a complete visual instruction rather than a checklist.

1. `OUTPUT CONTRACT`
   - exactly one independent 9:16 cinematic still;
   - single complete composition;
   - no collage, storyboard, poster, text, logo or watermark.

2. `LYRIC VISUAL HIT`
   - state the lyric-specific, non-generic visual answer;
   - pretty-but-generic is a failure.

3. `K0 PERFORMANCE STATE`
   - body orientation;
   - weight distribution / gait phase;
   - both hands and what each hand is doing;
   - gaze/head direction when visible;
   - precise phase of the current action at frame 0.

4. `CHARACTER PHYSIOLOGY / IDENTITY`
   - age band, build and body proportion;
   - stable head/face silhouette and jaw/cheek structure when visible;
   - hair length, texture, parting/wetness and silhouette;
   - identity cues that must remain stable across the set;
   - no celebrity likeness.

5. `SKIN / HUMAN REALISM`
   - realistic pore-scale variation and natural tonal irregularity where visible;
   - physically plausible moisture/specular response;
   - avoid plastic CGI skin or over-smoothed beauty retouching.

6. `WARDROBE MATERIAL`
   - garment cut, fiber, weight, seams/folds and drape;
   - how humidity/wind/body motion affects the fabric;
   - continuity with previous frames.

7. `CAMERA OPTICS`
   - shot scale;
   - approximate focal-length language;
   - camera height/angle;
   - perspective purpose;
   - depth-of-field behavior and what must remain readable.

8. `LIGHTING PHYSICS`
   - actual light source and direction;
   - softness/hardness;
   - highlight/shadow logic;
   - exposure protection;
   - reflections from water/glass/stone/metal when relevant.

9. `ENVIRONMENT & DEPTH`
   - foreground / midground / background hierarchy;
   - major materials and their physical state;
   - negative space for the next action;
   - continuity with the same world.

10. `ACTION ENTRANCE & RESIDUE`
    - what moves next;
    - available motion space;
    - static base that must not move;
    - physical remainder that can continue after the main action;
    - plausible settled end state.

11. `QUALITY + NEGATIVE GUARD`
    - anatomy, hands, reflections and geometry must be coherent;
    - no duplicate person/reflection-person;
    - no random prop drift;
    - no commercial model-pose default;
    - no text/UI/brand contamination;
    - no excessive adjective stacking as a substitute for optical/material detail.

12. `FACE PRIVACY / COMPLETION GRID`｜HARD FOR CURRENT WEB/SEEDANCE FACE-COMPLETION PATH
    - use a **standard 2D orthogonal black square grid** over the visible facial-feature region;
    - straight horizontal and vertical black lines forming regular square cells;
    - high-contrast, dense and clearly readable as a flat square grid;
    - preserve head silhouette, hair, ears/jawline when visible, body, wardrobe, lighting and composition at full detail;
    - the grid is NOT a contour-following 3D face mesh;
    - NOT pixel mosaic, blur, censor bar, black solid mask, helmet, veil or random scribble;
    - do not degrade the whole image;
    - for rear/side frames, apply the same orthogonal grid only to the visible facial-feature area if a face is readable;
    - if no face is readable because the accepted camera angle naturally hides it, do not invent a frontal face solely to show the grid.

## Prompt-writing principle

Do not reduce the production prompt to abstract labels such as “sad”, “cinematic”, “high-end”, “beautiful”. Convert intent into visible physical facts:

- exact body phase;
- exact hand position;
- exact dominant visual event;
- exact lens/camera relation;
- material response;
- light direction;
- depth hierarchy;
- motion entrance and residue.

The final production prompt should resemble a detailed cinematography/production instruction that an image model can render directly.

## Set-level continuity lock

Before writing K01...Kn, define once and preserve:

- same protagonist physiology/hair/body proportion;
- same wardrobe construction/material/colors;
- same face-grid policy;
- same world/architecture/material language;
- same time-of-day and controlled light progression;
- permitted accent colors/props;
- forbidden people/brands/text/world drift.

Each individual prompt must still repeat enough of the identity/world lock to be self-contained when generated separately.

## Hard sequence

`DIRECTOR PLAN LOCK -> PROMPT PRECISION OPTIMIZATION -> SINGLE-IMAGE GENERATION -> ACTUAL-PIXEL MACHINE QA -> HG03`

Sequential generation/review is preferred when identity drift, hand/reflection geometry or image-generator reliability is material. A collage/grid is never a valid substitute for independent first-frame files.

## Acceptance

Every formal first frame must simultaneously pass:

`LYRIC HIT + STANDALONE BEAUTY + CHARACTER/WORLD QUALITY + K0 PERFORMABILITY + FACE-GRID POLICY (when active)`

- Pretty but generic = FAIL.
- Semantically correct but visually weak = FAIL.
- Beautiful but static/non-performable = FAIL.
- Correct action but low-detail/plastic character or weak lighting/materials = FAIL.
- Wrong face treatment (mosaic / 3D mesh / solid mask / blur) = FAIL on the current Face-Completion path.
