# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W06-X`
- STAGE_NAME: `External Seedance generation`
- STATE: `EXTERNAL_REQUIRED / CAMERA_TEST_V1_READY`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- W06_EXPERIMENT: `06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Golden Quality Floor

R1 remains the minimum quality floor: frame beauty, lyric hit, directing/camera diversity, dynamic QA, edit and subtitle accuracy must not regress.

## W00 Result — LOCKED

`AUTO`. GitHub/Web/Files/local AV stack verified. No dedicated Whisper/faster-whisper and no direct Seedance execution in the current exposed web toolset.

## W01 Result — LOCKED

`HUMAN_GATE / PASSED`. Song: `如果你也刚好抬头看树` — 孙天宇 official vocal version.

## W02 Result — LOCKED

`PARTIAL`. Final BGM: `139.930s–177.050s`, rendered `37.120s`; workflow upgraded with Audio Boundary Gate v1.1 after two avoidable boundary corrections.

## W03 Result — LOCKED

`AUTO`. No Whisper claim. Same-version lyric evidence + locked audio established six Natural Beats; primary motion peak = `一颗心...飞过树梢`, final release = cloud line.

## W04 Result — LOCKED

`HUMAN_GATE / PASSED` after visual exploration and one rejected concept.

Final director direction: `树影之外`.

Core principles:
- not a continuous “tree story”; MV uses non-linear lyrical fragments;
- one fictional East Asian female protagonist;
- functional light sand/grey veil integrated into wardrobe and always covering nose/mouth/lower face;
- monumental scale: ancient tree + restrained grey-white curved concrete architecture + large sky negative space;
- low saturation, hard motivated natural backlight, real material texture;
- unified emotion/world, diverse camera viewpoints; do not turn the nine frames into one spatial one-take narrative.

## W05 Result — LOCKED

`HUMAN_GATE / PASSED`.

- Final first-frame set: `9 / 9` generated and accepted in conversation.
- The first pass of only three style anchors stopped instead of automatically continuing; user had to nudge and also flagged a soft/blurry result. Record this as one avoidable `TECHNICAL_RESCUE` for W05 execution discipline.
- After iterations, the accepted frame-set deliberately mixes: monumental extreme wide / medium reach / veil-eye close-up / full-body motion / bird relationship / worm’s-eye action peak / rooftop sky-release views.
- Final first-frame rule learned in this round: **unified emotional system + diverse camera system, not unified spatial narrative system**.
- Do not promote new hard rules solely from still-image acceptance; video results must validate them first.

## W06 Result — TEST PROMPTS READY

Actual state: `AUTO / EXPERIMENTAL`.

Research performed before writing prompts:
- `songguoxs/seedance-prompt-skill`
- `Emily2040/seedance-2.0` camera/cinematography references
- `yinxiaowai/awesome-ai-video-camera-movement-prompts`
- `fal-ai-community/skills` cinematography
- `maciejdzierzek/seedance-prompt-generator`
- supporting camera vocab from CinePrompt / cross-model director skills

Key test hypothesis:
- each 5s clip = one primary Camera Contract + one dominant event + one secondary physical aftermath + clear endpoint;
- diversity comes from the **whole set**, not by stacking many moves inside one 5s prompt;
- no precise timestamp segmentation for current 5s I2V test;
- no default slow-push template;
- complex high-risk moves are kept experimental, not forced into this song.

Prompt set and research note:
`06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`

Whole-set Camera Test v1:
1. S1 Locked extreme wide
2. S2 25–35° Arc shot
3. S3 Locked close-up + Rack Focus
4. S4 Truck-right lateral tracking
5. S5 Tilt Up
6. S6 Slow Dolly Pull-back
7. S7 Low-angle Pedestal Up — primary motion peak
8. S8 Slow horizontal Pan across rooftop geometry
9. S9 Small-amplitude optical Zoom Out — final release

Not used in current song but retained in research pool: Whip Pan, Dolly Zoom, Crash Zoom, FPV, strong handheld/shake, full 360 orbit, Camera Roll, Bullet Time, high-speed fly-through.

## Current External Boundary — W06-X

`EXTERNAL_REQUIRED`.

The web session cannot directly execute Seedance 2 mini. User action is limited to:
1. upload the matching accepted first frame;
2. paste the matching W06 prompt;
3. generate a 5s 9:16 raw clip in Seedance 2 mini;
4. return raw MP4(s) to this chat.

Recommended validation order before spending the full batch:
- `S1` — Locked camera compliance / atmosphere;
- `S3` — Rack Focus + veil/face stability;
- `S7` — strongest Pedestal Up / fabric / bird / identity stress test.

If these three pass, generate S2/S4/S5/S6/S8/S9. If one camera class fails, repair only that class; do not change the accepted first-frame set globally.

## Next Allowed Action

`EXTERNAL_TOOL` only: external Seedance generation and raw clip return.

After clips return: enter `W07` automatically for dynamic QA, root-cause classification and patch prompts. Do not promote W06 Camera Test v1 to core rules until W07 evidence exists.