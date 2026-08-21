# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W06-X`
- STAGE_NAME: `External Seedance generation / camera prompt validation`
- STATE: `EXTERNAL_REQUIRED / S1_MULTISHOT_TEST_V2_READY`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- W06_V1: `06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`
- W06_S1_V2: `06_TESTS/MV/WEB_R2/W06_S1_MULTISHOT_CAMERA_TEST_v2.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Locked Results

- W00: `AUTO / LOCKED`
- W01: `HUMAN_GATE / PASSED` — selected `如果你也刚好抬头看树` / 孙天宇
- W02: `PARTIAL / LOCKED` — final BGM `139.930s–177.050s`, rendered `37.120s`
- W03: `AUTO / LOCKED` — six Natural Beats, no false Whisper claim
- W04: `HUMAN_GATE / PASSED` — final director direction `树影之外`
- W05: `HUMAN_GATE / PASSED` — accepted first frames `9/9`

## W04/W05 Visual Lock

Final visual system:
- one fictional East Asian female protagonist;
- light sand/grey functional veil integrated into wardrobe, always covering nose/mouth/lower face;
- monumental ancient tree + restrained grey-white curved concrete architecture + large sky negative space;
- low saturation, motivated natural backlight, real material texture;
- MV uses **non-linear lyrical fragments**, not one continuous spatial story;
- first-frame principle validated: **unified emotional system + diverse camera system, not unified spatial narrative system**.

## W06 Research — Experimental Only

Research sources include `songguoxs/seedance-prompt-skill`, `Emily2040/seedance-2.0`, `yinxiaowai/awesome-ai-video-camera-movement-prompts`, `fal-ai-community/skills`, `maciejdzierzek/seedance-prompt-generator`, CinePrompt and supporting cross-model camera references.

### v1 hypothesis — REJECTED FOR THIS MV

The v1 interpretation used `one primary Camera Contract per 5s clip` and distributed camera diversity across the nine clips.

S1 external generation disproved this interpretation for the current MV target:
- returned raw clip: `5.09s`, `720×1280`, `24fps`;
- giant tree / curved wall / light beam / character scale remain almost unchanged through the clip;
- result reads as a fixed one-take and lacks the desired 3–5-shot MV dynamics;
- motion burden shifted onto fabric instead of camera/edit rhythm;
- an independent white scarf-like strip detached from the character and crossed the upper frame, a veil topology failure.

Root-cause correction:

`one camera movement per shot` **does not mean** `one camera movement per 5s clip`.

Correct test model:
- keep the proven `3–5 shot` dynamic structure when the lyric/director task benefits from it;
- inside **each Shot**, use only one clear camera movement / Camera Contract;
- overall clip energy comes from `hard cuts + shot-size/angle contrast + one move per shot + subject/environment action`;
- do not make every 5s clip a one-take merely to use professional camera language.

## S1 v2 — READY

Test file:
`06_TESTS/MV/WEB_R2/W06_S1_MULTISHOT_CAMERA_TEST_v2.md`

S1 v2 uses four explicit hard-cut shots:
1. extreme wide + Dolly In;
2. low-angle medium close-up + small Arc/Truck;
3. veil/eyes close-up + Rack Focus;
4. worm’s-eye / low angle + Tilt Up into the canopy and sky aperture.

### Veil topology patch

- veil remains one continuous piece connected to neck/shoulder/wardrobe;
- do not call it a long scarf/ribbon/tail;
- fabric motion is medium/small amplitude;
- forbid any independent white cloth/scarf/ribbon appearing from sky, canopy or offscreen;
- forbid detached cloth crossing the frame or duplicate fabric strips.

## Current External Boundary — W06-X

`EXTERNAL_REQUIRED`.

For the next iteration, generate **S1 v2 only** in Seedance 2 mini with the same accepted S1 first frame and return the raw MP4.

Do **not** generate S2–S9 yet.

## Next QA Gate

After S1 v2 returns, automatically check:
1. whether four Shots are visually distinguishable;
2. whether each Shot executes its intended camera movement;
3. whether 3–5-shot structure restores MV dynamics without chaos;
4. whether character/wardrobe/world remain acceptably consistent across cuts;
5. whether the veil stays physically connected and the floating-scarf artifact is gone;
6. whether the final Tilt Up delivers the lyric action `抬头看树`;
7. whether the ending is clean enough for editing.

Only if S1 v2 passes should this camera logic be expanded to S2–S9. Do not promote it to core rules yet.