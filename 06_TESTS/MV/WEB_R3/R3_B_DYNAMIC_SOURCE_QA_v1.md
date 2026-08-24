# WEB R3｜Dynamic Source QA v1

Status: `PARTIAL PASS / PATCH REQUIRED`
Song: `如果风会替我说话`
Source batch: 8 x Seedance 2 mini / 5s / 9:16
Prompt package: `R3_B_DYNAMIC_PROMPTS_v2_CAMERA_CALIBRATION.md`

## 0. Source mapping
Browser duplicate naming maps to production order:
- S01 = `AI动画人物雨夜窗边视频生成.mp4`
- S02 = `...(1).mp4`
- S03 = `...(2).mp4`
- S04 = `...(3).mp4`
- S05 = `...(4).mp4`
- S06 = `...(5).mp4`
- S07 = `...(6).mp4`
- S08 = `...(7).mp4`

## 1. Technical QA
All 8 sources are consistent:
- 720x1280
- 24 fps
- 121 video frames
- video stream duration ≈ 5.041667s
- container duration ≈ 5.088005s
- AAC stereo 44.1kHz audio stream present in every source

Policy consequence:
- `SOURCE_AUDIO = REMOVE` remains mandatory before picture edit.
- Visible `豆包AI生成` provenance overlay appears in generated sources; final delivery must use an authorized clean export if available, or otherwise treat the overlay as a known final-edit constraint rather than silently assuming a clean source.

## 2. Executive result

### Source-level usable now
`S02 / S03 / S04 / S05 / S07 / S08`

### Must patch before shot-library lock
`S01 / S06`

Reason for both hard failures:
`VEIL_CONTINUITY_FAIL` — lower face becomes visibly exposed, violating the locked masked-character rule.

### Camera-calibration headline
This batch is valuable because visual success and camera-command success are not identical.
- Some sources are strong final-edit candidates even when the requested camera grammar was only partially executed.
- Camera grammar promotion must therefore use `CAMERA_EXECUTION`, not beauty alone.

## 3. Per-source QA

| Seg | Camera target | Camera execution | Identity | Veil | Space topology | Lyric fit | Editability | Clean end | Camera grammar verdict | Source verdict |
|---|---|---|---|---|---|---:|---:|---|---|---|
| S01 | Micro Dolly-in <=5% | `PARTIAL / OVER-AMPLIFIED` | PASS | **FAIL** | PASS | 4.5/5 | 2/5 | YES but invalid | camera moves toward subject, but much stronger than requested; not reusable yet | **FAIL / REGENERATE** |
| S02 | Lateral slider along glass | `PARTIAL / UNDER-EXECUTED` | PASS | PASS | PASS | 5/5 | 4.5/5 | YES | rain/reflection event excellent; slider itself not clearly proven | PASS SOURCE / CAMERA UNPROVEN |
| S03 | Slow Dolly-out reveal | `PASS-PARTIAL` | PASS | PASS | PASS | 5/5 | 5/5 | YES | mild retreat successfully gives more weight to empty warm space; positive evidence | **PASS** |
| S04 | Foreground occlusion slide/reveal | **PASS** | PASS | PASS | PASS | 5/5 | 5/5 | YES | strongest camera proof in batch; foreground occlusion creates real reveal and depth | **PASS / POSITIVE EVIDENCE** |
| S05 | Mini arc/orbit 6–10° | `PARTIAL / SUBTLE` | PASS | PASS | PASS | 5/5 | 4.5/5 | YES | reflection geometry stays stable; camera arc is much weaker than requested | PASS SOURCE / CAMERA PARTIAL |
| S06 | Locked-off MMP control | camera **PASS** | PASS-PARTIAL | **FAIL** | PARTIAL | 3/5 | 1/5 | NO for locked character | fixed camera is stable, but hand+veil performance causes mask removal/exposure | **FAIL / REDESIGN PERFORMANCE** |
| S07 | Diagonal slider + rack focus | `PARTIAL / DRIFTS INTO PUSH-IN` | PASS | PASS | PASS | 5/5 | 4.5/5 | YES | object action/rack-focus idea works; intended short slider is not cleanly proven | PASS SOURCE / CAMERA UNPROVEN |
| S08 | Slow crane-retreat | **PASS-PARTIAL** | PASS | PASS | PASS | 5/5 | 5/5 | YES | clear vertical opening + world expansion; retreat component is less precise but emotional goal lands | **PASS / POSITIVE EVIDENCE** |

## 4. Detailed findings

### S01｜HOOK
What works:
- character eye identity remains attractive and recognizable;
- wind / hair / fabric event is immediate and emotionally legible;
- push-toward-viewer feeling exists.

Hard failure:
- veil rapidly turns into a loose foreground ribbon and exposes nose/mouth/lips for most of the clip.
- this violates the project hard rule even if the shot is aesthetically strong.

Camera finding:
- image-plane enlargement is visibly much stronger than the requested micro 5% budget; the model interprets `dolly-in + face + wind` as a stronger beauty push-in.

Patch direction:
- remove any instruction that lifts the veil across the face;
- lock an opaque inner face covering as immovable, and allow only a separate outer scarf tail / hair strands to move;
- reduce dolly language to `almost imperceptible camera creep` or fall back to locked-off + optical wind event if necessary.

### S02｜RAIN RESPONSE
What works:
- strongest semantic rain event: large droplets merge / travel across reflection;
- mirror identity remains coherent;
- veil stays on;
- excellent lyric-to-image fit.

Camera finding:
- the requested lateral slider is far less visible than the prompt specifies; the model spends motion budget on the rain event instead.

Decision:
- keep as source;
- do not yet claim lateral-slider grammar as validated.

### S03｜MEMORY / ABSENCE
What works:
- no second human appears;
- empty chair / warm doorway remains the memory carrier;
- mild retreat increases negative space rather than pushing into beauty portrait;
- character and room remain stable.

Decision:
- usable as-is;
- `slow dolly-out reveal` receives positive evidence, although the magnitude is gentler than the planned 8–12%.

### S04｜HOME / HOLD
What works:
- best director-camera match of the batch;
- foreground structural column actually crosses the frame and reveals the warm corridor;
- wet-floor reflection strengthens depth;
- no extra person;
- model uses occlusion to hide a small pose/orientation transition, but the edit remains visually coherent.

Decision:
- strong pass;
- `foreground occlusion slide/reveal` is the clearest reusable camera candidate from R3 so far.

### S05｜DREAM / AMBIGUITY
What works:
- same-person mirror/reflection topology remains surprisingly stable;
- veil continuity survives in both real and reflected image;
- water streak / glass distortion produces strong dream-vs-reality ambiguity.

Camera finding:
- requested 6–10° mini-orbit is only weakly visible; this is closer to a stable reflection shot with subtle camera drift than a proved orbit.

Decision:
- keep source;
- do not promote mini-orbit grammar yet.

### S06｜HEALING / MMP-01
Camera control result:
- locked-off camera itself is stable, proving that camera complexity is not the failure source.

Performance failure:
- hand interaction causes the veil to slide away and expose the lower face;
- the model interprets `hand + cheek + veil + pressure + release` as a face-reveal / veil-removal action;
- by later frames the original masked-performance contract is broken.

Important R3 learning:
`hand physically manipulating veil near mouth/cheek` is currently too high-risk for this character system.

Patch direction:
- do NOT regenerate by adding more detailed hand-pressure prose;
- remove hand-to-veil manipulation entirely;
- keep locked camera and micro-expression layer;
- express `融化` through an external small object / condensation / ice-water transition while the face covering remains untouched.

### S07｜IMPERFECT US
What works:
- two paper wind objects remain stable and non-anthropomorphic;
- staggered response gives a convincing `we` metaphor;
- focus hierarchy shifts from objects toward the character;
- veil remains intact.

Camera finding:
- movement becomes more like a push/reframe than a clean short diagonal slider.

Decision:
- source is edit-usable;
- `diagonal slider` itself is not validated.

### S08｜RELEASE
What works:
- very strong final emotional release;
- world opens up as the shot progresses;
- sky / wet ground / sunlight become more dominant;
- character remains a smaller part of the environment;
- veil / dress / hair produce useful physical residue.

Camera finding:
- vertical crane component is clear;
- backward-retreat component is less exact than requested but the combined emotional objective is achieved.

Decision:
- strong source pass;
- `slow crane-retreat` receives positive evidence, but should remain medium-risk until reproduced on another scene/song.

## 5. Camera-library learning from this batch

### Positive evidence now
- `FOREGROUND OCCLUSION SLIDE / REVEAL` — strongest.
- `SLOW DOLLY-OUT REVEAL` — stable at mild amplitude.
- `SLOW CRANE / WORLD-OPENING RETREAT` — emotionally successful, still medium-risk.
- `LOCKED-OFF PERFORMANCE` — camera itself stable; performance design failed for separate reason.

### Not yet validated
- `MICRO DOLLY-IN` — model over-amplifies on close face.
- `LATERAL SLIDER ALONG GLASS` — under-executed.
- `MINI ARC / ORBIT` — mostly under-executed.
- `DIAGONAL SLIDER + RACK FOCUS` — drifts into push-in/reframe.

## 6. Next action
Do not enter shot-library lock yet.

Patch only nearest causes:
1. regenerate S01 with immutable inner veil + outer moving fabric/hair, and lower camera-motion budget;
2. redesign S06 so hand never manipulates veil; use locked-off micro-expression + external melting/condensation event;
3. keep S02/S03/S04/S05/S07/S08 unchanged for now;
4. rerun source QA only on S01/S06;
5. once both pass, lock normalized shot library and enter Picture Edit / HG04.

`DYNAMIC_SOURCE_QA = PARTIAL_PASS`
`PATCH_REQUIRED = S01,S06`
`SHOT_LIBRARY_LOCKED = NO`
