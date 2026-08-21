# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W06-X / W07`
- STAGE_NAME: `External Seedance generation + dynamic QA / director-structure calibration`
- STATE: `S2_ONE_TAKE_PASS / DIRECTOR_SELECTOR_V1_RECORDED`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- W06_V1: `06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`
- W06_S1_V2: `06_TESTS/MV/WEB_R2/W06_S1_MULTISHOT_CAMERA_TEST_v2.md`
- DIRECTOR_SELECTOR: `06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`
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
- MV uses non-linear lyrical fragments, not one continuous spatial story;
- first-frame principle: **unified emotional system + diverse camera system, not unified spatial narrative system**.

## W06/W07 Generated-video Evidence

### S1 v1 — FAIL

- 5.09s / 720×1280 / 24fps;
- fixed extreme-wide one-take read as stiff because tree / wall / light / character scale barely changed;
- insufficient visual progression pushed motion burden onto fabric;
- independent white scarf-like cloth detached from character and crossed frame: veil topology failure.

Important correction:

`S1 proves a weak one-take can fail; it does NOT prove one-take is wrong.`

### S2 v1 — PASS / POSITIVE SAMPLE

User-returned raw clip:
- 5.04s / 720×1280 / 24fps;
- continuous small Arc / orbit-like camera move;
- foreground tree trunk, character and curved wall produce readable parallax through the full clip;
- camera changes the character-space relationship continuously and resolves at a more flattering three-quarter angle;
- character action remains simple: reach / look upward; model load stays controlled;
- result reads fluid and visually progressive despite being one continuous shot;
- user judgement: `S2效果不错，环绕运镜的感觉挺好`.

S2 success hypothesis:

`strong first-frame depth + simple continuous performance + foreground/midground/background parallax + one clear camera path + a more beautiful endpoint = one-take can outperform unnecessary cuts.`

## Director Structure Correction

The current experiment no longer uses either of these false absolutes:
- `every 5s clip should be one take` — REJECTED;
- `every 5s clip should be 3–5 shots` — ALSO REJECTED.

New experimental decision order:

`lyric task → first-frame performance potential → choose shot count → assign one Camera Contract per Shot → motion-load check → beauty/comfort gate`.

Shot-count options:

### 1 Shot / One Take
Use when:
- lyric is one continuous emotion or one complete gesture;
- first frame already has strong depth / parallax anchors;
- one camera path can create sustained visual progression;
- continuity feels more musical than cutting.

Current positive sample: `S2 Arc`.

### 2–3 Shots
Use when:
- one main event needs `setup → event → aftermath`;
- lyric needs character/detail attention shift;
- one semantic turn exists.

### 3–5 Shots
Use when:
- lyric density or beat density is high;
- motion peak / Hook needs angle and scale contrast;
- one-take cannot provide enough MV visual density.

3–5 shots are not automatically better. Every Cut must add new emotion, information or viewpoint.

Full experimental selector:
`06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`

## Per-shot Camera Rule — Experimental

Regardless of total Shot count, each individual Shot gets one primary Camera Contract:

`shot size + angle + start frame + movement + speed + subject relation + endpoint`.

Motion budget per Shot:
- 1 primary camera move;
- 1 primary subject action;
- 1 secondary physical motion.

Do not simultaneously overload camera + large body action + large fabric + bird + focus shift + light event unless the shot specifically earns that complexity.

## Current Direction

- S2 is retained as a one-take positive sample; do not replace it merely to increase cuts.
- S1 v2 four-shot prompt remains an experimental repair option, not a new universal template.
- S3–S9 must be reconsidered individually using the Director Shot-Structure Selector before batch generation.
- Goal is not maximum camera vocabulary; goal is the most beautiful, comfortable and lyric-specific 5-second direction for each segment.
- No promotion to core `ai_video.md` until more generated one-take / multi-shot pass-fail evidence exists.

## Next Allowed Action

Before generating the rest of the batch, automatically redesign the **S3–S9 shot-structure map** segment by segment using the experimental Director Selector, preserving S2 as accepted positive evidence.

Seedance execution remains `EXTERNAL_REQUIRED`; prompt/director analysis remains automatic.
