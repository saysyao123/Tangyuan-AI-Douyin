# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W06-X / W07`
- STAGE_NAME: `External Seedance generation + dynamic QA / director-structure calibration`
- STATE: `S1_V2_SOURCE_USABLE / S2_ONE_TAKE_PASS / DIRECTOR_SELECTOR_V1_RECORDED`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- W06_V1: `06_TESTS/MV/WEB_R2/W06_CAMERA_PROMPT_EXPERIMENT_v1.md`
- W06_S1_V2: `06_TESTS/MV/WEB_R2/W06_S1_MULTISHOT_CAMERA_TEST_v2.md`
- DIRECTOR_SELECTOR: `06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`
- S1_V2_QA: `06_TESTS/MV/WEB_R2/W07_S1_V2_QA_NOTE.md`
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
`S1 v1 proves a weak one-take can fail; it does NOT prove one-take is wrong.`

### S1 v2 — PASS_AS_SOURCE / TRIM_REQUIRED

User-returned raw clip:
- 5.088s / 720×1280 / 24fps;
- clear multi-shot execution with meaningful scale / angle / focal changes;
- visual level and camera energy are substantially better than S1 v1;
- extreme-wide opening, eye close-up and final canopy Tilt Up are usable source material;
- clip is accepted into the source pool, but not locked for full-length use.

Detected visual discontinuities approximately at:
`2.04s / 2.42s / 3.13s / 3.88s`.

Middle issue:
- `2.04–3.12s` contains two similar low-angle character beats;
- foreground occlusion differentiates them slightly, but shot size / angle / action state repeat enough to feel redundant;
- W08 should keep only the stronger portion or trim both aggressively; **do not regenerate solely for this**.

New source-material principle:
`Generated clip QA is not binary whole-clip accept/reject. A clip can be SOURCE_USABLE / TRIM_REQUIRED; final BGM and edit rhythm decide which internal shots survive.`

### S1 v2 Audio — SOURCE_AUDIO_POLICY_FAIL

Returned clip includes non-ambient music-like audio even though the prompt used soft wording similar to `不需要BGM`.

Extracted audio evidence:
- AAC stereo 44.1kHz;
- integrated loudness approx `-18.7 LUFS`;
- strongly harmonic continuous content, inconsistent with wind/leaves-only ambience.

Visual source remains usable because final MV uses the locked external song and removes AI source audio.

Core `04_HARNESS/rules/ai_video.md` upgraded to v1.2 with a stronger Source Audio HARD RULE:
- explicitly forbid BGM / music / melody / beat / chords / singing / humming / narration / dialogue / voices;
- allow only physically motivated natural ambience when useful;
- default `SOURCE_AUDIO = REMOVE`;
- if music still appears, mark `SOURCE_AUDIO_POLICY_FAIL`, keep good visuals and strip source audio in W08;
- AI source audio never determines edit Beat or subtitle timing.

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

The current experiment rejects both absolutes:
- `every 5s clip should be one take` — false;
- `every 5s clip should be 3–5 shots` — false.

Decision order:
`lyric task → first-frame performance potential → choose shot count → assign one Camera Contract per Shot → motion-load check → beauty/comfort gate`.

Shot-count options:
- `1 Shot`: continuous emotion / complete gesture / spatial reveal / release where camera motion itself provides sustained progression;
- `2–3 Shots`: setup → event → aftermath, character/detail shift, one semantic turn;
- `3–5 Shots`: dense lyric / motion peak / strong Hook where angle/scale contrast is actually needed.

Every Cut must add new emotion, information or viewpoint.

### Adjacent Shot Contrast Gate — EXPERIMENTAL

S1 v2 shows multi-shot prompts can still repeat themselves if adjacent shots are too similar.

Before generation, consecutive Shots should differ in at least 2 of:
- shot size;
- angle;
- subject scale;
- camera direction;
- focal plane;
- dominant action;
- dominant visual subject.

If not, merge or remove one Shot before generation.

Full experimental selector:
`06_TESTS/MV/WEB_R2/W06_DIRECTOR_SHOT_STRUCTURE_SELECTOR_v1.md`

## Current Direction

- S1 v2 stays in the source pool; trim repetition later rather than regenerate now.
- S2 remains the one-take positive sample and should not be rewritten merely to add cuts.
- S3–S9 must be reconsidered individually with the Director Selector.
- Future prompts use the strengthened Source Audio hard wording from `ai_video.md v1.2`.
- Camera/shot-count rules remain experimental; audio source policy is promoted because it strengthens an existing verified hard rule rather than inventing a new director formula.

## Next Allowed Action

Automatically redesign S3–S9 shot structures and prompts segment by segment using:
1. lyric task;
2. accepted first frame;
3. S1/S2 generated evidence;
4. Adjacent Shot Contrast Gate;
5. strengthened Source Audio hard rule.

Seedance execution remains `EXTERNAL_REQUIRED`; prompt/director analysis remains automatic.