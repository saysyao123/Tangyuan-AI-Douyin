# Rule｜MV Face-Degrade → Face-Reveal Completion v1.0

> Status: `ACTIVE / OSS_OPT_R1 FIRST-FRAME STANDARD LOCKED / DYNAMIC REVEAL PATCH TESTING`
> Scope: character first frames and Seedance/Doubao image-to-video prompts when portrait-safe face degradation is required.
> Stable branch note: experiment branch only until D02-B dynamic tests close.

## 1. Purpose

Use a portrait-safe first frame that hides recognizable facial structure strongly enough for upload/reference acceptance, while preserving a reliable path to a stable fictional face during image-to-video.

The first-frame concealment rule and the dynamic reveal rule are separate concerns:
- first frame: maximize facial-identity concealment without damaging body/world quality;
- dynamic stage: explicitly remove the temporary concealment layer and reveal one stable fictional face before the main motion begins.

## 2. Locked first-frame black-grid standard｜HARD

When a character face must be degraded:
- use a **deep-black, coarse, dense, high-contrast curved mesh/grid** across the entire visible facial area;
- cover forehead, brows/eyes, nose, cheeks, lips, chin and visible jaw region;
- grid strength must be high enough that the underlying detailed facial structure cannot be confidently read;
- preserve only head outline, hair, ears when visible, jaw silhouette, body, wardrobe, pose, lighting and environment;
- do not use pale gray, thin, sparse, low-opacity or decorative beauty-grid treatment;
- do not blur the whole image;
- do not degrade body, hands, clothing, architecture or environment;
- for side/three-quarter faces, the grid must still cover the entire visible facial surface;
- for true distant/back-facing shots where the face is not readable, do not force an artificial visible grid.

The grid is a technical input-adaptation layer. It is not the character's permanent mask, tattoo, makeup, fashion accessory, cyber effect or story prop.

## 3. Why weak dynamic wording failed

Do **not** rely on abstract instructions such as:
- `网格自然消失`;
- `自动补脸`;
- `Face-Completion` alone;
- `网格淡出` while body/camera also perform large motions.

Seedance tends to preserve salient first-frame appearance. A strong black grid can therefore be treated as a permanent character feature unless the prompt defines a concrete state transition.

## 4. Dynamic face-reveal contract｜HARD

For a readable gridded face, the opening must be serialized before the main director action.

### 4.1 Front-load face instruction

Immediately after the portrait-safe prefix and K0 lock, state:

`The black facial grid is a temporary opaque privacy occluder positioned slightly in front of the fictional character's face. It is not attached to the skin and is not part of the character identity.`

### 4.2 Concrete physical removal, not morphing

Preferred behavior:
- 0.00–0.20s: preserve K0 exactly;
- 0.20–0.80/1.00s: the black grid separates from the facial surface as one temporary flexible occlusion layer and is pulled/slid cleanly toward one frame edge by existing scene motion/wind;
- it exits the visible facial area completely;
- underneath it, an already complete fictional adult face is revealed;
- do not transform black lines into skin;
- do not dissolve line-by-line across the skin;
- do not keep residual grid fragments.

The semantic model should solve **object removal/reveal**, not `grid morphs into face`.

### 4.3 Stable revealed-face hold

From approximately 0.8/1.0s to 5.0s:
- zero black grid lines remain on the face;
- the face stays fully visible and stable;
- no face swap, age drift, gender drift, facial-geometry oscillation, duplicated eyes/nose/mouth or mask return;
- keep the same hair, head silhouette and body identity;
- do not reintroduce the grid at cuts, turns or occlusions.

## 5. Motion-load rule for face reveal｜HARD

For S2/S3-like high-risk angles, use the previously validated stability principle:
- **face instruction first**;
- **motion load reduced during first ~1 second**;
- camera approximately HOLD / S during reveal;
- body only breathing/micro-motion during reveal;
- main turn/walk/yield/follow begins only after face stabilization.

Do not simultaneously request:
`strong face reveal + large head turn + walking + camera travel + fabric event`.

Default opening load:
- subject motion: `S` during reveal, then planned `M`;
- camera motion: `XS/S` during reveal, then planned `S/M`;
- environment motion: `S`.

## 6. Fictional face identity target｜recommended

A reusable face target should describe stable fictional identity without referencing a real person:
- adult East Asian male/female as required by the MV;
- face shape / jaw / cheekbone proportions;
- brow and eye shape;
- nose bridge/tip/alar width;
- lip shape;
- hair style and texture;
- natural skin tone and restrained real skin texture;
- emotional baseline.

The same identity block must be copied unchanged across all sources of the same character.

For current D02-B male target:
- fictional adult East Asian male, late-20s appearance;
- slightly long oval face with restrained cheekbones, clean narrow jaw and small defined chin;
- straight-to-softly arched brows;
- long almond-shaped dark-brown eyes, calm restrained gaze;
- straight narrow nose bridge, natural compact tip;
- medium natural lips, stable neutral mouth corners;
- warm-neutral East Asian skin with subtle pores/texture, no plastic smoothing;
- soft naturally voluminous black hair with light wind response;
- mature, clean, gentle, restrained attractiveness; no exaggerated smile or seductive pose.

## 7. Failure classification

`GRID_PERSISTENCE_FAIL`:
- grid remains after 1.0s;
- grid becomes permanent mask/tattoo;
- grid fades but repeatedly returns;
- facial structure never fully appears.

`FACE_REVEAL_IDENTITY_FAIL`:
- face appears but changes identity;
- facial geometry oscillates;
- head turn causes a new face;
- eyes/nose/mouth duplicate or collapse.

When failure is local to one source, patch/regenerate only that source. Do not reopen accepted first frames or other dynamic clips.

## 8. Current validation state

D02-B:
- strong black-grid first-frame standard: `USER_ACCEPTED / LOCKED FOR EXPERIMENT`;
- previous abstract `grid naturally disappears` dynamic wording: `FAILED` on S2/S3 due to grid persistence;
- new concrete occluder-removal / low-motion first-second contract: `TEST REQUIRED`.

Do not promote the dynamic reveal method to stable R3 until S2/S3 generation confirms the grid fully leaves and the fictional face remains stable.
