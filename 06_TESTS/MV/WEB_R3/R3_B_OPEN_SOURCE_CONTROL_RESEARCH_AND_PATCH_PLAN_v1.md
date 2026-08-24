# WEB R3｜Open-source Control Research + S02/S06 Patch Plan v1

Status: `R3-B ANALYSIS COMPLETE / TOMORROW TEST READY`
Song: `如果风会替我说话`
Scope: v3 patch outputs `3S02 / 3S04 / 3S05 / 3S06`

## 0. Human result
- S04: `PASS ENOUGH FOR CURRENT LOOP` — partial foreground occlusion solved the previous hidden scene rebuild well enough; retain as evidence.
- S05: `PASS ENOUGH FOR CURRENT LOOP` — dry mirror + separate background rain window materially improved surface ownership; retain.
- S02: `FAIL / RAIN PHYSICS` — rain remains visually over-large / tubular / spatially ambiguous; the event is still being synthesized rather than preserved as a stable surface-bound track.
- S06: `FAIL / CONCEPT + OBJECT PHYSICS` — the new transparent object is not legible as a stable ice object and the interaction drifts back toward face/hand ambiguity; lyric event is not instantly readable.

## 1. External open-source learnings
Relevant control projects:
- CameraCtrl: explicit camera trajectories rather than relying on prose to imply motion.
- MotionCtrl: separates camera motion and object motion as independent control dimensions.
- CamI2V / RealCam-I2V: camera-controlled I2V emphasizes geometry-aware camera paths and real-world camera movement.
- ByteDance ATI: image-to-video trajectory control starts from explicit frame-0 track points / trajectories; camera pan and object tracks are specified as motion paths.
- SG-I2V: controls motion from frame-0 object regions and trajectories rather than asking text alone to invent a complex object path.

R3 adaptation for Seedance 2 mini (text-only control surface):
1. emulate trajectory conditioning with one simple `TRACK CONTRACT` per hard event;
2. preload difficult objects/material states into the first frame;
3. do not ask the model to CREATE + TRANSFORM + MOVE a transparent object in the same 5s source;
4. camera motion and object motion should not both be high-risk in the same shot;
5. if physics is the research target, freeze or simplify the camera.

## 2. Physics research implication
Current physical-video benchmarks (PhyGenBench / VideoPhy / Physics-IQ) show that fluid/material interactions and physical commonsense remain weak points across video generators. Prompt rewriting alone is not a reliable cure for difficult dynamic physics.

R3 consequence:
`REDESIGN THE PHYSICAL TASK` before `ADD MORE PROMPT DETAIL`.

## 3. S02 root-cause analysis
### What v3 still asks the model to do
- infer which side of the glass owns rain;
- create/merge droplets;
- preserve a reflection;
- move the camera;
- distort the reflection only through water;
all within one short close shot.

The phrase `two large droplets merge` strongly encourages the model to invent a visually salient blob/rivulet. In the generated output the water becomes too large and tube-like, with weak scale cues and ambiguous surface ownership.

### New S02 strategy: `PRE-EXISTING THIN RIVULET`
Do NOT ask for droplet birth or merging.

New first-frame requirement:
- one or two already-visible thin irregular rain trails on the EXTERIOR face of the window;
- trails are narrow, realistic, and clearly attached to the glass plane;
- character/reflection already exists;
- no large spherical macro droplet.

Dynamic event:
- one existing thin trail simply descends along the glass under gravity;
- constant approximate width/volume; no growth into a giant blob;
- no new droplets appear;
- no lateral drifting into the room.

### Camera grammar change
For the S02 physics test, DROP the lateral slider.
Use:
`LOCKED CAMERA + ONE SLOW RACK FOCUS`

Reason:
S02 should test surface physics, not camera controllability. S04/S08 already provide stronger camera experiments.

### Text-only pseudo-trajectory contract
`RAIN_TRACK: existing thin rivulet starts near upper third of the exterior pane and moves straight downward about 25–35% of frame height over 5s; attached to the same glass plane; no lateral drift; no size explosion; no free-floating droplets.`

## 4. S06 root-cause analysis
The v3 redesign still failed because the first frame did NOT actually contain a clearly established ice object. The prompt tried to introduce a small transparent object into a face/hand-heavy I2V shot. Transparent materials + fingers + face covering + phase-change language create too many simultaneous topology/material demands.

Key rule learned:
`IF THE OBJECT CARRIES THE LYRIC, IT MUST EXIST CLEARLY AT FRAME 0.`

### New S06 strategy: full first-frame rebuild mandatory
Do not reuse the old face-close first frame.

New first frame composition:
- foreground lower-third: a small transparent ice shard / ice cube resting on a matte dark stone or ceramic saucer on the windowsill;
- the ice is already wet and a single small water bead is visibly formed at its lower edge at frame 0;
- mid/background: same woman in soft focus, still and watching the object;
- no hand touches the ice;
- no hand touches the veil;
- warm practical lamp creates one real highlight through the ice; rain window remains background only.

### Dynamic event
Do NOT ask for visible large-scale phase transformation.
The audience can infer melting from one physically stable event:
1. pre-existing bead slowly swells a little;
2. bead detaches;
3. bead falls vertically onto saucer;
4. woman makes one slow blink / gaze lifts slightly;
5. ice remains mostly the same geometry but wetter at the edge.

This avoids requiring conservation-heavy geometry change in 5 seconds.

### Camera grammar
Preferred:
`LOCKED CAMERA + SLOW RACK FOCUS FROM ICE BEAD TO EYES`

Optional later experiment after physics passes:
`MICRO DOLLY-OUT <=5%`.
Do not combine on the first retry.

### Text-only pseudo-trajectory contract
`DROP_TRACK: one already-visible bead at the bottom edge of the ice stays attached for ~2s, grows only slightly, detaches once, and falls straight down a short distance onto the saucer; no new droplets, no sideways motion, no object morphing.`

## 5. Why S04/S05 improved
### S04
Partial occlusion retained persistent spatial cues and reduced the model's opportunity to rebuild the hidden scene. This supports the R3 rule:
- same-scene continuity -> partial occlusion;
- full occlusion -> use only as intentional hidden transition with a defined target scene.

### S05
Separating the dry mirror from the rainy background window removed conflicting surface ownership. The reflection became a geometry problem instead of a geometry+water problem.

## 6. Tomorrow's minimal test plan
Do NOT regenerate S04/S05.

### Test A — S02 v4
- new/edited first frame with pre-existing thin exterior rain trail;
- locked camera;
- one rack focus only;
- one downward rain track;
- no droplet merging.

Acceptance:
- rain clearly belongs to the exterior pane;
- no giant tubular blob;
- no floating interior water;
- reflection remains optically attached;
- source remains visually strong.

### Test B — S06 v4
- generate a NEW first frame first;
- ice object already visible and wet at frame 0;
- one existing bead;
- no hand/object manipulation;
- locked camera + one rack focus;
- one bead detachment event only.

Acceptance:
- viewer immediately reads `ice / water / release`;
- object topology stable;
- drop obeys gravity;
- no magic glow / material morph;
- character remains secondary emotional witness.

## 7. New experimental rule candidates
### FIRST-FRAME STATE PRELOAD
Any small transparent / reflective / deforming object that carries a lyric event must be clearly established in the first frame. Do not ask I2V to invent it mid-motion.

### ONE PHYSICS EVENT PER SOURCE
One 5s source should contain at most one difficult material interaction.

### CONTROL BUDGET
When testing difficult physics:
- camera complexity = LOW;
- object/material complexity = ONE;
- character performance = LOW.

When testing difficult camera motion:
- scene physics = SIMPLE;
- object transformations = NONE.

## 8. Promotion status
All rules above remain `EXPERIMENTAL / R3 POSITIVE-EVIDENCE CANDIDATES`.
Promote only after S02/S06 improve and at least one later song reproduces the gain.
