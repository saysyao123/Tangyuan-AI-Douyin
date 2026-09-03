# Seedance 2.5 R1 K0 Generation Brief v1

> Status: `READY_TO_GENERATE / ASSET REGISTRATION REQUIRED AFTER GENERATION`
> Purpose: produce three controlled K0 images for `R1_LEGACY_VS_LEAN`.
> These images are benchmark inputs, not a new MV aesthetic template.

## 1. Control principle

All three K0s must share:
- the same original fictional adult East Asian woman;
- the same wardrobe and hair identity;
- the same overall world/material/light family;
- 9:16 vertical cinematic photorealism;
- no text, logo, watermark or second person.

Only the **tested motion condition** changes.

This reduces confounds when comparing Legacy vs Lean prompts.

## 2. Shared identity / world lock

### Character
Original fictional adult East Asian woman, approximately late 20s, not based on or resembling a named real person or celebrity.

Identity anchors:
- oval face with calm clear eyes;
- straight dark eyebrows;
- natural realistic skin texture;
- long black hair tied in a low structured knot with a few controlled loose strands;
- no face covering for this benchmark, because face/hand and head-angle stability are explicit test targets;
- restrained neutral expression, capable of subtle emotional change.

Wardrobe:
- charcoal-blue long coat/robe with clean modern-Eastern tailoring;
- pale gray inner layer;
- narrow silver fastening detail at the collar;
- sleeves long enough to show cloth response but never hide the hands completely;
- no ornate jewelry or high-detail accessory clutter.

### World
A fictional quiet pale-stone water courtyard at early morning:
- pale limestone floor and low walls;
- shallow mirror-water basin or channel;
- dark bronze structural accents;
- cool pearl daylight with very soft warm reflected edge light;
- clean depth cues suitable for camera-motion evaluation;
- restrained atmosphere, no fantasy particles or dramatic VFX.

## 3. K0-A — FACE_HAND

### Goal
Create a frame-0 state that already contains a difficult but readable hand/face spatial relationship.

### Image prompt
Create one original 9:16 vertical cinematic photorealistic still in the shared benchmark world and character identity above.

Medium-close three-quarter portrait. The woman is framed from roughly mid-torso upward, with both shoulders and both hands readable. Her right hand is already raised beside the lower cheek/temple region, fingers naturally separated and anatomically clear, approximately a few centimeters from the face; the hand is not blocking the eyes. Her left hand rests lower in frame and remains visible. Her head is already turned slightly three-quarter toward the raised hand rather than facing perfectly forward. Her eyes look toward the hand with restrained concentration.

The composition must leave a little breathing room in front of the face and raised hand so the next motion can continue forward, sideways, or gently toward the camera. The background remains simple pale stone and soft water reflection, with enough depth for a small camera approach but no distracting objects.

Frame-0 should feel like the action is already underway and can continue immediately, not like a posed beauty portrait.

Critical constraints:
1. exactly one fictional adult character;
2. raised hand and all visible fingers are clean and readable;
3. no text, logo or watermark.

## 4. K0-B — MOVING_CAMERA

### Goal
Create a frame-0 state where the subject is already in locomotion and the environment exposes real camera translation/parallax.

### Image prompt
Create one original 9:16 vertical cinematic photorealistic still using exactly the same fictional woman, wardrobe, hair identity and courtyard world as K0-A.

Medium-wide to full-body composition. The woman is already walking along a long pale-stone path beside a shallow linear water channel. One foot is planted while the other is visibly transferring forward into the next step; hips, shoulders and coat fabric reflect an active continuous gait rather than a standing pose. She moves diagonally away from the camera toward the upper-right depth of frame.

Camera starts from a rear-three-quarter / side-rear relationship at approximately waist-to-chest height. The environment contains clear near/mid/far geometry—low bronze rail, repeated pale-stone joints, water-channel edge, distant doorway—so future FOLLOW, YIELD or OVERTAKE motion will produce obvious parallax.

Keep the character large enough for identity and face-angle stability to remain judgeable. The frame must look like a real captured instant during motion, not a fashion pose.

Critical constraints:
1. exactly one fictional adult character;
2. walking phase is already active at frame 0;
3. no text, logo or watermark.

## 5. K0-C — PHYSICS

### Goal
Create one simple physical-causality setup where a single material event can continue from frame 0.

### Image prompt
Create one original 9:16 vertical cinematic photorealistic still using exactly the same fictional woman, wardrobe, hair identity and courtyard world as K0-A and K0-B.

Medium shot at a shallow oval pale-stone basin. The woman is calm and comparatively still. Both hands are clearly visible over the basin; one cupped hand already holds a small coherent amount of clear water, while the other hand is positioned below/nearby to guide the release. A few droplets have just begun to leave the fingertips, but the main water release and ripple event have not yet completed. The basin surface is mostly calm with only the first tiny disturbance directly below the hand.

Camera remains stable and observational. The visual design makes one causal chain obvious: hand opens -> water falls -> basin receives impact -> ripples expand -> residue settles. Body/head motion should remain secondary so the water/contact event is the only dominant physics task.

Critical constraints:
1. exactly one fictional adult character;
2. both hands, water mass and basin contact area are clearly readable;
3. no text, logo or watermark.

## 6. Acceptance before video benchmark

Each K0 must pass only these checks:
- same character identity and wardrobe family across A/B/C;
- tested spatial condition is clearly visible at frame 0;
- hands/body/object topology is already usable;
- enough motion space exists for the intended video task;
- no second person/text/logo/watermark;
- no obvious image-generation defect that would contaminate the video comparison.

Do **not** over-review micro-aesthetic differences. These are controlled benchmark anchors, not final HG03 artwork.

## 7. Asset registration

After each actual image exists, register durable identity before R1 runs:
- `asset_id`;
- SHA-256;
- byte size;
- provenance kind (`generated` if generated in this project);
- locator kind/value;
- generation prompt/seed/provider if available.

Then update:
- `R1_INPUT_MANIFEST.yaml`;
- `R1_PRODUCTION_CARDS.yaml` reference asset IDs;
- all paired Legacy/Lean rows in `R1_RUN_LEDGER.csv`.

No R1 cell may run from a recreated image with only the same prompt. The exact K0 bytes are the comparison authority.
