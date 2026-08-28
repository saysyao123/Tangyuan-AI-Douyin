# Knowledge｜MV First-Frame Reference Stack v1.0

Status: `ACTIVE / REQUIRED BY S05 FIRST-FRAME EXECUTOR`
Purpose: preserve the proven visual-generation quality layer without turning the runtime into a giant monolithic skill.

## 1. Authority stack

Every formal MV first-frame prompt must be synthesized from all four layers below, in order:

1. `LOCKED LYRIC / DIRECTOR TRUTH` — what this frame must mean, what event must already exist at K0, and why this shot exists.
2. `PROMPT PRECISION RULE` — the mandatory visual/technical modules defined in `04_HARNESS/rules/mv_first_frame_prompt_optimization.md`.
3. `REFERENCE STACK` — open-source image-prompt construction patterns + the user's validated deep-character-detail granularity method.
4. `GENERATED / ACCEPTED K0 PIXELS` — after HG03 acceptance, actual pixels become downstream authority over old prose.

No single layer may substitute for another.

---

## 2. Open-source prompt construction reference｜HARD REFERENCE

Primary reference:
- `freestylefly/awesome-gpt-image-2`
- repository: `https://github.com/freestylefly/awesome-gpt-image-2`
- use only as a prompt-structure / image-quality construction reference; do not copy a specific protected artwork, character identity, copyrighted scene or named visual style.

Relevant categories for MV first frames:
- `Photography & Realism`
- `Characters & People`
- `Architecture & Spaces`
- `Scenes & Storytelling`

Required transferable lessons:
- describe the **exact visual moment**, not only the emotion;
- define camera height, viewpoint, shot scale, lens/perspective purpose and depth behavior;
- define spatial function and foreground/midground/background hierarchy;
- define material state and physically coherent reflections;
- define actual light source, direction, hardness/softness and exposure behavior;
- describe pose/body state as an executable physical phase, not a fashion pose;
- use concrete nouns and physical facts instead of adjective stacking;
- use negative constraints to suppress staged-ad, poster, duplicate-person, text and geometry failures.

The open-source reference answers: **how to phrase a high-quality image-generation instruction**. It never overrides the current song/Director.

---

## 3. User deep-character-detail granularity reference｜HARD REFERENCE

The user's previously supplied character-detail prompt method is a **granularity standard**, not a literal character template.

For every important human first frame, resolve the applicable details below.

### 3.1 Age / body proportion
- explicit adult age band;
- head-to-body proportion appropriate to the current character rather than generic AI-model proportions;
- shoulder / neck / waist / hip relationship;
- limb length with believable skeletal and muscular support;
- weight distribution and posture in the actual K0 action phase;
- avoid exaggerated fashion/anime anatomy unless the locked project explicitly requires it.

### 3.2 Head / face construction
When the face is visible underneath the current privacy/completion treatment, lock the underlying structural target:
- overall head silhouette;
- forehead-to-cheek-to-jaw relationship;
- cheekbone and jaw width;
- brow/eye spacing and eyelid construction where applicable;
- nose bridge/base proportion where applicable;
- lip volume/shape where applicable;
- ear / jaw / neck continuity.

For the current Face-Completion route, these are **underlying identity targets**; the visible face region still receives the required orthogonal black square grid.

### 3.3 Hair construction
- length and overall silhouette;
- parting / growth direction;
- strand grouping and irregular flyaways;
- dry/wet state;
- gravity, humidity and wind response;
- no glossy helmet-like salon hair unless specifically locked.

### 3.4 Skin / human realism
Where skin remains visible (forehead edge if allowed, ears, jaw edge, neck, arms, hands):
- pore-scale variation instead of uniform smoothness;
- fine vellus hair where physically plausible;
- eyelid/lip micro-fold detail only where visible and not covered by the grid;
- subtle blood-tone / cool-gray transitions rather than one flat skin color;
- local translucency / subsurface behavior at ear rim, nose/eyelid/lip regions only when visible;
- face/neck/ear/arm tonal continuity;
- humidity/water produces restrained specular response, never plastic CGI gloss.

### 3.5 Hands
- specify what each hand is doing at K0;
- believable wrist/finger articulation;
- correct contact with prop/surface;
- no duplicate fingers / fused fingers / impossible grip;
- hand action should support the lyric event, not become decorative posing.

### 3.6 Wardrobe construction
- garment cut and silhouette;
- fiber/material type;
- weight and drape;
- seams, cuffs, collar and fold behavior;
- humidity/wind/body-motion response;
- continuity across the set;
- no unexplained wardrobe drift for the sake of making one frame prettier.

### 3.7 Light / volume continuity
Character detail is not independent from lighting:
- face/head/body volume must agree with the locked source direction;
- skin, hair and fabric highlights must come from the same physical light field;
- reflections from water/glass/metal may tint or lift local planes, but may not create contradictory portrait lighting;
- environment and subject exposure must coexist in one physically believable shot.

The user-detail reference answers: **how much character-specific physical detail is required before a prompt is production-grade**.

---

## 4. Current Face-Completion grid policy

For the current Web/Seedance Face-Completion route:
- use `STANDARD_2D_ORTHOGONAL_BLACK_SQUARE_GRID` on any readable facial-feature region;
- straight horizontal + vertical black lines forming regular square cells;
- flat, high-contrast, clearly 2D;
- not contour-following face mesh;
- not pixel mosaic, blur, censor bar, scribble, solid black mask, helmet or veil;
- preserve hair, head silhouette, jaw/ear edges when visible, neck, body, clothing, hands, light and environment at full detail;
- mirror reflection of the same readable face follows the same grid policy;
- rear/wide views do not invent a frontal face merely to display the grid.

This is capability-specific but **HARD whenever the current project is using the validated Face-Completion path**.

---

## 5. Production synthesis rule

Formal first-frame prompt generation must follow:

`DIRECTOR / LYRIC -> choose exact K0 moment -> apply character granularity -> apply camera/space/material/light construction -> apply Face Grid if current capability route requires -> add action entrance/residue -> add negative guards -> single-image generation -> actual-pixel QA`

Do not write a checklist-like prompt that only names modules. The final prompt must be coherent natural-language visual direction with sufficient concrete information for the image model.

---

## 6. Pre-generation quality check

Before a prompt is sent to image generation, all answers below must be YES:
- Can the lyric-specific visual answer be identified without generic mood language?
- Is the exact 0-second body/action phase visible?
- Are both hands accounted for when visible?
- Is character anatomy/proportion deliberately specified rather than defaulted?
- Are hair, skin and wardrobe described at physically useful granularity?
- Are lens, camera height, perspective and depth purposeful?
- Are light source/direction and major material reflections physically coherent?
- Is foreground/midground/background hierarchy readable?
- Is there available motion space for the next action and a plausible residue/end state?
- Is the Face Grid exactly the validated orthogonal 2D square-grid treatment when required?
- Would the frame still be a strong film still if its semantic explanation were removed?

Any `NO` means `PROMPT_PRECISION_NOT_READY` and generation must not begin.
