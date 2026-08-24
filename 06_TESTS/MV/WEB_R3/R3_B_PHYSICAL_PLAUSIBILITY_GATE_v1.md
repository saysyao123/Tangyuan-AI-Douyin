# WEB R3｜Physical Plausibility Gate v1

Status: `EXPERIMENTAL / R3-B`
Purpose: prevent visually attractive but physically impossible AI video shots.

## 1. Core principle
Before writing camera motion, first define the physical world.

Every generated shot must explicitly lock:
1. CAMERA SIDE — where the camera physically exists;
2. CHARACTER SIDE — where the subject exists;
3. BOUNDARY PLANES — glass / mirror / door / wall / water surface / foreground object;
4. EFFECT OWNERSHIP — which side/surface owns rain, condensation, reflection, mist, light, shadow;
5. GRAVITY / FLOW DIRECTION — what direction water, cloth, hair and objects can naturally move;
6. OCCLUSION CONTINUITY — what is allowed to change while the frame is partially/fully blocked;
7. POST-OCCLUSION TARGET — if the frame becomes fully hidden, the next visible state must be explicitly defined or treated as a deliberate transition.

## 2. Surface Ownership Contract
For any transparent/reflective surface, write positive spatial statements instead of only negative constraints.

Example for interior rain-window shot:
- camera is inside the room;
- character is inside the room;
- glass is a fixed vertical boundary between interior and exterior;
- rain exists only on the exterior-facing surface of the glass;
- interior-facing glass remains dry except for optional interior condensation if explicitly requested;
- no free-floating droplets exist between camera and character;
- water adheres to the exterior glass surface and moves downward under gravity;
- reflection remains optically attached to the glass plane.

Do not merely write `不要让雨在室内`; define where rain DOES exist.

## 3. Reflection / Mirror contract
- reflection cannot move independently of the real subject;
- reflected motion has the correct mirrored direction;
- reflection remains constrained to its physical surface plane;
- water distortion deforms the reflected image only where water crosses the optical path;
- camera motion must preserve a coherent mirror axis / glass plane.

## 4. Occlusion Continuity Gate
Full occlusion is high-value but high-risk.

### Partial occlusion
Recommended for continuous same-scene shots.
- foreground object may cover part of the frame;
- keep at least one stable topology cue visible when possible;
- subject pose / environment geometry must remain continuous.

### Full occlusion
Treat as a latent edit point.
The model may use full blockage as permission to rebuild the scene.
Therefore full occlusion should be used only when either:
A. the exact post-occlusion state is separately specified and materially similar; or
B. the director INTENDS a hidden transition from shot/scene A to shot/scene B.

Do not use full occlusion as a casual flourish and then expect perfect same-scene continuity.

## 5. Physics-first prompt ordering
Recommended order for complex I2V prompt:
1. scene topology / physical planes;
2. character location and allowed movement;
3. material ownership (rain / glass / cloth / water / light);
4. primary visual event;
5. camera grammar;
6. secondary residue;
7. clean endpoint;
8. avoid list.

Reason: if camera motion is specified before physical topology, the model may spend coherence budget on camera motion and hallucinate spatial physics.

## 6. One difficult physics interaction per 5s source
Avoid stacking multiple unstable interactions in one source.

High-risk combinations include:
- camera orbit + reflection + rain distortion;
- full foreground occlusion + same-scene continuity + character pose change;
- hand + face covering + facial deformation + micro-expression;
- moving transparent cloth + exposed face + strong push-in;
- water surface + reflection + camera arc + second moving object.

If a lyric requires multiple ideas, assign one as primary and move the rest to edit or another source.

## 7. New QA axis
Add to W07-style QA:
`PHYSICAL_PLAUSIBILITY: PASS / PARTIAL / FAIL`

Subchecks:
- SURFACE_OWNERSHIP
- GRAVITY_FLOW
- REFLECTION_GEOMETRY
- OCCLUSION_CONTINUITY
- OBJECT_CAUSALITY
- LIGHT_SOURCE_COHERENCE

A beautiful shot with obvious physical impossibility cannot receive final source lock.

## 8. R3 evidence from current batch
- S02: rain/glass ownership ambiguous or wrong -> surface ownership failure.
- S04: foreground occlusion camera move strong, but post-occlusion scene continuity breaks -> occlusion continuity failure.
- S05: rain appears on interior/wrong side of glass -> surface ownership failure.
- S06: performance interaction is physically/readably incoherent -> object causality / performance-design failure.
- S08: world-opening camera + wind + wet ground remain physically coherent -> benchmark positive evidence.

## Promotion policy
This is an R3 experimental rule. Promote to runtime only after it materially improves at least the S02/S04/S05/S06 patch batch and survives another song/scene test.
