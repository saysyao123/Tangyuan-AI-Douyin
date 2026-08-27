# Rules｜MV First-Frame Prompt Precision Optimization v1.0

Status: `ACTIVE / HARD BEFORE FIRST-FRAME GENERATION / OSS_OPT_R1`

## Purpose

After Director Plan lock and before first-frame image generation, every formal MV first frame MUST pass one prompt-precision optimization step. Do not send raw Director prose directly to the image model.

## Mandatory references

1. External visual prompt reference library: `freestylefly/awesome-gpt-image-2` (Prompt-as-Code / photography / character / architecture / scene cases). Use it as a structural and image-quality reference, not as a style-copy source.
2. User-supplied deep character-detail prompt method: extract and adapt its useful granularity for bone structure, eyes/brows/nose/lips, hair construction, skin micro-texture, body proportion, wardrobe material and lighting-volume continuity. Do not mechanically copy the source character, gender, styling or scene.
3. Locked Director Plan / lyric-hit requirement remains creative authority.
4. `mv_first_frame_qa.md` remains the HG03 visual QA authority.

## Required optimization modules

Each production first-frame prompt MUST resolve, at minimum:

1. `OUTPUT CONTRACT` — one independent 9:16 still; no collage/poster/text/logo/watermark.
2. `LYRIC VISUAL HIT` — the lyric-specific visual answer that cannot be replaced by a generic beauty shot.
3. `K0 PERFORMANCE STATE` — body orientation, weight, hands, gaze/head direction, current action phase.
4. `CHARACTER PHYSIOLOGY` — age band, body proportion, head/face structure target, hair construction, stable identity cues.
5. `SKIN / HUMAN REALISM` — specific micro-texture and reflection behavior where visible/appropriate; avoid plastic CGI smoothness.
6. `WARDROBE MATERIAL` — cut, fiber, weight, folds and environmental response.
7. `CAMERA OPTICS` — shot scale, lens/focal language, camera height, perspective purpose, depth of field.
8. `LIGHTING PHYSICS` — source/direction/softness, highlight/shadow logic, exposure and environment reflection.
9. `ENVIRONMENT & DEPTH` — foreground/midground/background, material hierarchy, negative space and world continuity.
10. `ACTION ENTRANCE & RESIDUE` — what moves next and which physical remainder can continue after the main event.
11. `QUALITY + NEGATIVE GUARD` — clarity, anatomy, exposure, material authenticity, duplicate-person/text/poster failures.
12. `FACE PRIVACY GRID` when required — standard 2D orthogonal square black grid, straight horizontal/vertical lines, high-contrast dense coverage, no contour-following 3D face mesh.

## Quality principle

Do not rely on adjective stacking (`masterpiece / beautiful / 8K`) as the primary quality strategy. Describe WHY the image should look high quality: optics, focus, skin/material micro-detail, light direction, depth layers, realistic irregularity and physical response.

## Character-detail adaptation rule

The user's deep character prompt is a granularity template, not a literal identity template. Adapt its descriptive depth to the current character and song world. For a male character, preserve equivalent detail depth while changing facial/body/hair/wardrobe attributes as required by the Director Plan.

## Hard sequence

`DIRECTOR PLAN LOCK -> FIRST-FRAME PROMPT PRECISION OPTIMIZATION -> SINGLE-IMAGE GENERATION -> MACHINE IMAGE QA -> HG03`

Batch first-frame generation is NOT the default. Generate/review sequentially when image-gen reliability or visual drift risk is material.

## Acceptance

A formal first frame must simultaneously pass:

`LYRIC HIT + STANDALONE BEAUTY + CHARACTER/WORLD QUALITY + DYNAMIC PERFORMABILITY`.

Pretty but generic = FAIL.
Correct but visually weak = FAIL.
Beautiful but static/non-performable = FAIL.
