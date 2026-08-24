# WEB R3｜Patch Plan v2｜Physics + Director Logic

Status: `READY FOR PATCH DESIGN`
Scope: `S02 / S04 / S05 / S06`
Keep unchanged: `S01 / S03 / S07 / S08`
Benchmark: `S08`

## S02｜如果雨会替我回答
Current issue: rain behavior lacks correct glass-side ownership.

### Keep
- close side-profile / reflection concept;
- rain as the answering actor;
- restrained camera movement;
- same character and warm/cool palette.

### Patch
Define the physical world BEFORE the camera instruction:
- camera = inside room;
- character = inside room;
- glass = fixed vertical boundary;
- rain = exterior-facing glass surface only;
- room-side glass = dry;
- no droplets between camera and character;
- water adheres to exterior glass and moves downward under gravity;
- reflection stays optically attached to the glass plane.

Primary event:
One exterior raindrop merges with another and runs vertically downward across the reflected eye.

Camera:
Keep a very small single-axis slider or even locked-off if physics loses priority.

## S04｜如果还能一起回家
Current issue: full foreground occlusion causes hidden topology/pose reset; second half becomes narratively unclear.

### Key learning
The camera grammar is valuable, but full occlusion should be treated as a hidden edit/transition device, not a casual same-scene reveal.

### Production patch for this song
Use `PARTIAL FOREGROUND REVEAL`, not full blackout.
- camera slides laterally behind a doorframe/column;
- foreground may cover 30–55% of frame, but never fully hides all stable topology cues;
- keep either the woman silhouette edge OR far warm lamp OR corridor vanishing line continuously visible;
- character pose stays unchanged;
- after reveal, same corridor geometry and same warm-light coordinate remain.

### Separate camera-library experiment
Preserve `FULL OCCLUSION TRANSITION` as a future grammar:
Scene A -> full foreground cover -> intentionally reveal Scene B.
Do not demand same-scene continuity when using this grammar.

## S05｜如果梦能模糊真假
Current issue: water/rain appears on the wrong spatial side of the glass/mirror.

### Redesign
Remove rain from the reflective surface entirely.
Use a physically dry interior mirror / dark reflective panel.
Rain may exist only on a separate exterior window in the background.

Primary event:
The camera performs a very small arc around the mirror axis so the real face and reflected face move from near alignment to slight misalignment.

Optional secondary event:
soft rack focus or background rain bokeh shifts, but the mirror itself stays dry.

This makes `真假偏移` come from real parallax, not impossible water behavior.

## S06｜如果痛能随之融化
Current issue: concept, performance and physical interaction all fail; do not patch the old action.

### Full concept rebuild
Director answer:
`痛不是从脸上被拿走，而是在她手里从“硬”变成“水”。`

New frame / action concept:
- medium-close, not extreme close;
- character remains seated by the rain window;
- both eyes and hands are visible in one stable composition;
- in her open palm rests one small, already-partially-melting clear ice fragment / frost-coated transparent object;
- warm practical lamp is nearby but not dangerously close;
- a real water droplet forms, grows, then falls from the object into her palm / onto the dark tabletop;
- her hand slowly relaxes from a slight grip to an open palm;
- eyes look down first, then slowly lift toward the window; no crying, no face-touching.

Primary event:
`solid -> droplet -> release`.

Camera:
locked-off or almost locked-off. Do not add camera complexity until the new physical metaphor proves stable.

Micro-performance:
- lower eyelid tension softens;
- brow center relaxes;
- one slow blink after the droplet falls;
- emotion is release, not pain acting.

Avoid:
- hand touching face/veil;
- magic glowing ice;
- rapid melting puddle;
- smoke/fantasy particles;
- object changing shape unrealistically;
- extra fingers / hand topology changes.

## Batch QA target
Patch sources must pass:
- PHYSICAL_PLAUSIBILITY;
- DIRECTOR_INTENT_LEGIBILITY;
- CAMERA_EXECUTION;
- IDENTITY_STABILITY;
- EDITABILITY;
- CLEAN_ENDPOINT.

Only after patch batch passes:
`SHOT_LIBRARY_LOCK -> PICTURE EDIT / HG04`.
