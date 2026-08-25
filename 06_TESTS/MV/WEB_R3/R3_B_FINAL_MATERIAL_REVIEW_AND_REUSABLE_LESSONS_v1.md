# WEB R3｜Final Material Review + Reusable Lessons v1

Status: `MATERIAL REVIEW COMPLETE / EDIT PLAN READY / AWAITING NEXT STAGE`
Song: `如果风会替我说话`
Batch: final 8-source pool uploaded 2026-08-25

## 0. Important source mapping
The current uploaded filenames do not perfectly match lyric segment numbering by content.
Use CONTENT mapping for edit, not filename suffix alone:

- S01 = `3S1.mp4` — wind / extreme close portrait
- S02 = `3S6.mp4` — rain-window / exterior rivulet
- S03 = `3S3.mp4` — seated memory / empty warm space
- S04 = `3S4(1).mp4` — corridor / foreground occlusion reveal
- S05 = `3S5(1).mp4` — dry mirror / double image
- S06 = `3S2.mp4` — foreground ice / rack focus to woman
- S07 = `3S7.mp4` — two paper wind objects
- S08 = `3S8.mp4` — dawn world-opening release

All 8 sources: 720x1280, 24fps, 121 frames, container ≈5.088s, AAC audio present. `SOURCE_AUDIO=REMOVE` remains required.

## 1. Executive decision
The batch is good enough to stop regeneration and proceed toward picture edit, but picture edit must be selective rather than using every 5s source from start to end.

Current principle:
`SOURCE != FINAL SHOT`

Use the stable, intelligible portion of each source; trim or hide physically/semantically weak regions when that can be done without damaging rhythm.

### Overall status
- Strong / largely clean: S01, S03, S05, S07, S08
- Usable with selective trim: S02, S04, S06
- No further generation required before first picture-edit test
- Shot library can be treated as `EDIT-CANDIDATE LOCK`, not yet final Golden runtime evidence

## 2. Per-source material review + suggested edit windows

### S01｜如果风会替我说话｜`3S1.mp4`
Verdict: `KEEP / STRONG HOOK`

Strengths:
- immediate eye/face recognition;
- wind, hair and veil create a readable opening event;
- camera push feels emotionally direct;
- facial identity remains stable enough.

Weaknesses:
- movement is stronger than a true micro-dolly;
- veil reveal is acceptable for this production and is not treated as a failure.

Suggested edit window:
- primary candidate: `~0.15–3.15s`
- preserve the early wind build and one slow blink/eye-state change;
- avoid extending merely because 5s source exists.

Camera learning:
- close-face dolly-in tends to amplify itself into a beauty push;
- usable aesthetically, but not yet a precise camera-control grammar.

### S02｜如果雨会替我回答｜`3S6.mp4`
Verdict: `KEEP WITH TRIM / RAIN EFFECT SHOULD BE WEAKENED`

Strengths:
- composition and reflection are coherent;
- woman and glass remain readable;
- later part of clip has natural rainy-window ambience.

Weaknesses:
- early rain track becomes over-large / tube-like and too visually salient;
- this demonstrates that making rain a hero physics event reduces realism.

Suggested edit window:
- preferred: `~1.9–4.9s` for the 3s lyric unit;
- this skips the most artificial oversized-rivulet phase while retaining rainy atmosphere and reflection.

Director/generation lesson:
- for ordinary emotional rain scenes, rain should be `ATMOSPHERIC TEXTURE`, not a foreground hero object;
- use small streaks, wet-glass sheen, bokeh, reflection and post sound instead of explicit droplet birth/merge/growth.

### S03｜如果我还会想起他｜`3S3.mp4`
Verdict: `KEEP / POSITIVE EVIDENCE`

Strengths:
- negative space and warm empty room successfully carry absence;
- mild dolly-out increases the emotional weight of empty space;
- no second person is needed;
- physical space remains stable.

Suggested edit window:
- `~0.6–2.6s` for the 2s lyric unit;
- exact trim may move slightly with musical phrasing.

Camera learning:
- mild `SLOW DOLLY-OUT REVEAL` is one of the more stable camera grammars in this R3 loop.

### S04｜如果还能一起回家｜`3S4(1).mp4`
Verdict: `KEEP AS PARTIAL SHOT + TRANSITION ASSET`

Strengths:
- foreground occlusion movement is visually strong;
- corridor depth, wet floor, distant warm light are excellent;
- camera movement itself has high reuse value.

Weaknesses:
- once the foreground structure covers most of the frame, the continuous scene becomes less useful as a same-shot narrative;
- full/near-full occlusion invites model reconstruction.

Suggested edit usage:
- `0.0–~2.8s`: clean continuous S04 material;
- `~2.8–3.4s`: treat occlusion as a motivated hidden edit/transition region;
- after near-full cover: do not insist on same-scene continuity.

Recommended edit strategy:
- use the foreground column as a natural wipe into S05 or another shot;
- cut while frame is substantially occluded, making the model weakness become an intentional editorial transition.

Camera learning:
- `PARTIAL FOREGROUND REVEAL` is good for same-scene continuity;
- `FULL OCCLUSION` should be treated as a hidden transition point, not a decorative move that must return to the identical scene.

### S05｜如果梦能模糊真假｜`3S5(1).mp4`
Verdict: `KEEP / CLEAN CONCEPT`

Strengths:
- dry mirror + separate rainy-world logic materially improves physical plausibility;
- real subject and reflected image remain coherent;
- ambiguity comes from geometry rather than magic water effects;
- visual motif is distinct from S02 despite same rainy world.

Suggested edit window:
- `~0.3–3.3s` for 3s lyric unit.

Generation lesson:
- when reflection itself carries the lyric, remove unnecessary fluid interaction from the same reflective surface;
- one difficult geometry problem per shot is safer than geometry + fluid + camera arc simultaneously.

### S06｜如果痛能随之融化｜`3S2.mp4`
Verdict: `KEEP WITH EDIT / CONCEPT READS BETTER THAN PREVIOUS VERSIONS`

Strengths:
- ice is clearly preloaded in frame 0 and visually legible;
- foreground object / background witness successfully differentiates this shot from window portraits;
- rack-focus direction naturally turns physical state into emotion;
- no hand/object manipulation means topology is much safer.

Weaknesses:
- the intended single water-drop event is not strongly legible enough to rely on as the sole narrative event;
- focus transition itself becomes the stronger event.

Suggested edit window:
- first edit test: `~1.0–4.0s` as one continuous 3s phrase;
- let clear ice foreground transition into the woman's eyes through rack focus;
- do not force the edit to prove a visible droplet if the generated source does not clearly show one.

Director lesson:
- the audience can read `melting` from wet ice + focus shift + emotional release without a spectacular drop;
- a weak but physically believable material cue is preferable to a strong but fake physics effect.

### S07｜如果我们还是傻瓜｜`3S7.mp4`
Verdict: `KEEP / GOOD METAPHOR`

Strengths:
- two simple objects successfully express `我们` without a second person;
- staggered object movement gives a tender imperfect rhythm;
- focus / reframing remains editable;
- visual motif is distinct.

Suggested edit window:
- `~0.8–2.8s` for the 2s lyric unit.

Camera learning:
- rack focus + small reframe is useful;
- do not yet label it a validated diagonal slider because the model tends to convert complex small camera paths into generic push/reframe.

### S08｜如果爱不只是童话｜`3S8.mp4`
Verdict: `KEEP / R3 CAMERA + EMOTION BENCHMARK`

Strengths:
- strongest integration of camera, environment and lyric;
- world becomes progressively larger than the character;
- wind direction, wet ground, horizon and sunlight remain coherent;
- visual release is readable without fantasy effects.

Suggested edit window:
- `~0.4–4.4s` for the 4s final lyric unit;
- preserve as much of the continuous world-opening motion as possible.

Camera learning:
- `WORLD-OPENING CRANE / RETREAT` is the current R3 benchmark;
- keep as positive evidence, not yet a global runtime rule until reproduced on another song.

## 3. Editing salvage rules learned in this batch

### A. Trim first, regenerate second
If the source has a clean 2–4s region and the bad physics occurs only at one edge, trim it away.
Do not regenerate a visually strong source merely because the full 5s is imperfect.

### B. Use model weakness as a motivated edit point
Blur, rack-focus transition, foreground occlusion and fast fabric crossing can hide an edit if the cut is motivated by the shot itself.
Do not hide errors with random flashy transitions.

### C. Occlusion is an editorial resource
When foreground coverage approaches full-frame, treat it as a latent cut point.
Cut A -> occlusion -> B instead of demanding the model restore identical topology after full cover.

### D. Never force final timeline to equal raw-source boundaries
The 5s source is a shot reservoir.
Final lyric segment duration remains controlled by the locked audio timeline.

## 4. Reusable generation lessons

### 4.1 Weakest Sufficient Motion
Use the weakest physical effect that communicates the lyric.
If atmosphere alone communicates rain, do not turn rain into a macro droplet simulation.

New default candidate:
`ATMOSPHERE > HERO PHYSICS` for rain, mist, dust, snow, steam unless the material event itself is the lyric's central subject.

### 4.2 FIRST-FRAME STATE PRELOAD
Transparent / reflective / deforming objects that matter to the lyric should already exist clearly at frame 0.
Do not ask I2V to invent the object mid-shot and then transform it.

### 4.3 ONE DIFFICULT PHYSICS EVENT PER SOURCE
Do not stack rain merge + reflection distortion + camera motion + face performance in one 5s source.

### 4.4 CONTROL BUDGET
If physics is difficult:
- camera complexity LOW;
- character performance LOW;
- one object track only.

If camera movement is difficult:
- scene physics SIMPLE;
- no object phase-change;
- no mirror+fluid stack.

### 4.5 SURFACE OWNERSHIP
Explicitly define which physical plane owns rain / reflection / condensation.
Positive spatial statements are more useful than only adding negative prohibitions.

### 4.6 PHYSICALLY BELIEVABLE > VISUALLY LOUD
A weak, believable rain texture or wet ice cue is preferable to a huge but fake water event.
This is especially important for healing/cinematic MV language.

## 5. Rain-specific strategy update

Rain is now classified as a high-risk effect when treated as a controllable foreground object.

### Default future hierarchy
P1 — environment-level rain texture:
- fine streaks on exterior glass;
- wet-surface sheen;
- distant rain curtain;
- bokeh and reflection;
- subtle ambient sound in post.

P2 — one pre-existing small surface-bound track:
Use only when a specific droplet/rivulet is narratively important.

P3 — droplet creation / merging / macro fluid transformation:
Avoid by default in Seedance text-only workflow.
Only use for deliberate R&D tests, not production-critical shots.

## 6. Camera-language series test plan

The next R3 camera experiments should be controlled A/B tests, not embedded randomly inside production shots.
Open-source control systems such as CameraCtrl, MotionCtrl and ByteDance ATI explicitly separate camera/object motion or provide trajectories/track points. R3 text-only workflow should emulate this by changing one variable at a time.

### Test families
1. Dolly-in / Dolly-out
   - micro / mild / medium amplitude
   - portrait vs medium-space scene

2. Lateral Slider
   - clean scene without rain/reflection first
   - then foreground parallax

3. Foreground Occlusion
   - 20–30% partial cover = continuity test
   - 40–60% cover = transition test
   - near-full cover = hidden edit only

4. Arc / Orbit
   - 3° / 6° / 10° on simple static environments
   - no mirror/fluid during first validation

5. Crane / Retreat
   - low / medium rise
   - open-space release scenes
   - S08 is benchmark reference

6. Rack Focus
   - object -> face
   - face -> empty space
   - foreground metaphor -> character

### Test protocol
- same first frame or closely controlled first-frame family;
- same subject identity;
- only one camera variable changes;
- no difficult physics during camera calibration;
- score CAMERA_EXECUTION / IDENTITY / TOPOLOGY / LYRIC_FIT / EDITABILITY;
- repeat on at least a second song before promotion.

## 7. Evidence status / promotion policy

Promote now only as R3 experimental guidance:
- trim-before-regenerate;
- weakest sufficient motion;
- first-frame state preload;
- one difficult physics event per source;
- control budget;
- surface ownership;
- partial occlusion for continuity / full occlusion for transition.

Do NOT yet promote specific camera grammars to global Golden Runtime except as positive evidence.
Cross-song replication remains required.

## 8. Recommended next gate

Current material is sufficient for a first Picture Edit test.

Next stage, only after human go-ahead:
1. build edit candidate using locked BGM + canonical lyric timeline;
2. use the suggested clean source windows above as starting ranges, not rigid cuts;
3. remove source audio;
4. exploit S04 occlusion as a motivated cut if rhythm supports it;
5. keep S08 continuous as the ending benchmark;
6. after picture edit, run HG04 on rhythm and narrative flow before subtitle/final polish.

`MATERIAL_REVIEW_COMPLETE = YES`
`EDIT_CANDIDATE_READY = YES`
`FINAL_SHOT_LIBRARY_GOLDEN = NO`
`NEXT = AWAIT HUMAN REPORT ACCEPTANCE -> PICTURE EDIT / HG04`
