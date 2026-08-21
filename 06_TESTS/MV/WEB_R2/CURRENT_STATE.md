# WEB R2｜CURRENT_STATE

> 网页端 R2 唯一状态入口。新 Chat / Agent 必须先读本文件。

## Current Status

- ROUND: `WEB_R2`
- MODE: `WEB_AUTOMATION_CALIBRATION`
- STAGE: `W04`
- STAGE_NAME: `Director concept + production-unit allocation`
- STATE: `DIRECTOR_PLAN_READY / AWAITING_AESTHETIC_GATE`
- BRANCH: `test/mv-web-r2`
- GOLDEN_REFERENCE: `06_TESTS/MV/ROUND_01/`
- WORKFLOW: `04_HARNESS/workflows/mv.md`
- UPDATED_AT: `2026-08-21 Asia/Manila`

## Golden Quality Floor

R1 Golden Sample remains the minimum quality floor: frame beauty, lyric hit, directing/camera diversity, dynamic QA and edit/subtitle accuracy must not regress.

## W00 Result — LOCKED

Actual state: `AUTO`. GitHub/Web/Files/Image interface/local ffmpeg stack verified. Dedicated Whisper/faster-whisper and direct Seedance execution are unavailable in the current exposed toolset.

## W01 Result — LOCKED

Research: `AUTO`; total: `HUMAN_GATE / PASSED`.
Selected song: `如果你也刚好抬头看树` — `孙天宇` official vocal version.

## W02 Result — LOCKED

Actual state: `PARTIAL`.
Locked BGM: `139.930s–177.050s`, rendered duration `37.120s`, fade in `0.020s`, fade out `0.950s`.
Final preview v3 passed. W02 one-shot clipping failed and the workflow was upgraded with Audio Boundary Gate v1.1.

## W03 Result — LOCKED

Actual state: `AUTO`.
No Whisper was claimed. Exact lyric sequence was cross-checked against same-song sources; locked-audio beat estimate is ~`103.36 BPM`.
Six Natural Beats:
1. title + leaf-dance entry;
2. cuckoo-call playful rise;
3. hidden-to-discovered bird;
4. `哎哟` + heart-over-treetop primary motion peak;
5. title reprise / spatial reset;
6. cloud-floating release.

## W04 Focused Benchmark Snapshot

Benchmark is external reference only, not copied surface design.

1. `AI MV导演曹斌Johnny｜如果你也刚好抬头看树 AIMV/Karaoke` — recent same-song adoption exists. Use only as homogeneity warning and current market-completion reference; do not copy its surface shots.
   - source: https://jingxuan.douyin.com/m/video/7639398350034576114
2. `AI MV导演曹斌Johnny｜你比夏天先到来` — recent full MV + short teaser packaging shows current summer-song AIMV is already active; our concept must have a stronger non-generic hook than “pretty summer person + scenery”.
   - source page: https://jingxuan.douyin.com/m/video/7630328582577539931
3. `AI MV导演曹斌Johnny｜Seedance2.5 MV test` — current market signal: 30s / 48-cut experiment highlights higher motion/cut density capability; do not mechanically imitate cut count, but R2 cannot regress to all-slow-push grammar.
   - source page: https://jingxuan.douyin.com/m/video/7639398350034576114
4. `丹鸾歌行｜current Seedance2.5 narrative/action tests` — current benchmark shows stronger spatial/action continuity is becoming normal; our lyric MV should use actual visual events, not only wind/rain/fog ambience.
   - source: https://jingxuan.douyin.com/m/video/7654248002437008646
5. Beauty references for W05 only: real-world upward canopy / dappled-film / macro-dew imagery. Learn light, scale and material; do not copy composition literally.

## W04 Director Concept — PROPOSED LOCK

### Concept title

`一棵树里的夏日宇宙`

### Core idea

No visible human protagonist. The **camera/viewer is the “你 / 我”** in the lyric.

The entire 37.12s MV stays around one distinctive old urban tree in a quiet summer courtyard. Looking up causes scale to expand:

`pavement / seed → bark → leaves → hidden bird → treetop → open sky → white cloud`

This makes “如果你也刚好抬头看树” a literal viewer action while avoiding the generic AI-MV pattern of a beautiful person standing in a forest.

### Character policy

- `NO HUMAN CHARACTER` for the full R2 MV.
- No background people, no faces, no crowd.
- One small realistic cuckoo-like bird is allowed only in the production segments whose first frames already contain it.
- Main recurring non-character motif: one small **golden winged seed** carried by wind. It becomes the metaphor for `一颗心...飞过了树梢` without showing a literal heart.
- Because no human appears, portrait-safe prefix is not needed for these segments unless W05/W06 design later introduces a person (not currently planned).

### World / palette / material

- location: quiet contemporary urban courtyard / lane, one old tree, no readable signs, no logos;
- tree identity lock: thick textured trunk, low Y-shaped split, one recognizable pale bark scar; same species / trunk architecture across first frames;
- palette: chlorophyll green + warm cream concrete + cyan-white summer sky + small amber/golden seed accent;
- light: humid midsummer daylight, moving dappled light, mild backlight / sun flare only when motivated;
- material priority: leaf veins, bark fissures, dew, fine feather detail, warm dust/pollen, cloud volume;
- image feel: cinematic naturalism, restrained 35mm-like grain, not fantasy-game illustration, not hyper-neon.

## Opening Hook — LOCK CANDIDATE

First ~1 second: on warm concrete below the tree, one golden winged seed **lifts upward against the expected falling direction**. The camera immediately accepts the invitation and follows it into a fast vertical reveal of the trunk/canopy.

Why this hook:
- visually readable with no text;
- contains a real event, not only a pretty frame;
- directly motivates the viewer to “抬头”; 
- establishes the recurring seed used again at the motion peak;
- provides a clean transition from ground scale to tree scale.

## Production Allocation

Natural conceptual Beats = `6`.
First frames = `9`.
Seedance 2 mini raw production clips = `9 × 5s = 45s`.
Locked BGM = `37.120s`.
Raw headroom = `7.880s`, about `21.2%` above final duration.

This is intentionally more headroom than the bare `8 × 5s = 40s` minimum; it allows selective trim / action completion / overlaps without forcing every source clip to contribute almost all 5 seconds.

### 9 Production Segments

| Seg | Draft final range | Lyric task | First-frame 0s anchor | Dominant visual event | Camera grammar | Structure |
|---|---:|---|---|---|---|---|
| S1 | `0.00–4.15` | 如果你也刚好抬头看树 | golden winged seed just beginning to lift from courtyard ground; trunk base enters upper frame | seed rises; camera follows rapidly from ground up the trunk | low macro → vertical tilt/crane reveal | 2-shot |
| S2 | `4.15–8.20` | 我要学着树叶翩翩起舞 | close branch with leaves already torsioned by a small vortex | leaves perform a coherent spiral/dance around branch rather than random wind | close arc/orbit around branch | single-shot |
| S3 | `8.20–12.10` | 喊几声布谷布谷 | dew-lined leaf / thin branch; no bird visible yet | offscreen call causes tiny dew/leaf vibration and spatial direction cue | macro lateral slider + rack focus | single-shot |
| S4 | `12.10–16.00` | 或许少有人知道 / 有鸟儿是这样叫 | small realistic bird already present, partly screened by leaves | hidden bird is revealed and calls; branch flexes with its movement | detail insert → reveal → medium branch | 3-shot |
| S5 | `16.00–20.20` | 好吧哎哟哎哟 | bird and nearby leaves in compressed telephoto depth | playful wing flick launches a burst of leaves across lens; visual punctuation | snap pan / short reframe, no slow push | 2-shot |
| S6 | `20.20–24.70` | 一颗心叽叽喳喳飞过了树梢 | same golden winged seed caught in a branch fork, about to release | **primary motion peak:** seed breaks free and races upward through layered canopy | fast chase/follow upward with controlled acceleration | single-shot |
| S7 | `24.70–28.80` | 如果你也刚好抬头看树 | symmetrical low-angle trunk/canopy opening; no moving camera at 0s | canopy parts radially under a clean gust, revealing a bright sky aperture | mostly locked low-angle; environment creates reveal | single-shot |
| S8 | `28.80–33.10` | 向一朵白云学习如何漂浮 | above-canopy wide view with tree crown below and white cloud entering | golden seed loses speed and begins floating with cloud-scale parallax | high wide lateral aerial drift | single-shot |
| S9 | `33.10–37.12` | release / tail | quiet open sky, crown edge low in frame, seed already floating | no new climax: seed and cloud separate slowly while leaf motion below continues | locked-off / minimal natural drift | single-shot final hold |

Draft ranges are director allocation, **not subtitle timing**. W08 subtitle timing still comes from locked audio evidence.

## Camera Repetition Gate — PASS

- no consecutive slow push structure;
- vertical reveal only S1, high-speed chase only S6;
- orbit used only S2;
- macro lateral slider only S3;
- 3-shot reveal only S4;
- snap-pan punctuation only S5;
- locked environment reveal only S7;
- aerial lateral drift only S8;
- static release only S9;
- environment motion is not the sole event across the set: seed lift, leaf spiral, sound-to-vibration, bird reveal, leaf burst, seed flight, canopy aperture and cloud float are distinct dominant events.

## Anti-Copy / Anti-Homogeneity Gate — PASS

Reject:
- generic forest beauty montage;
- beautiful woman standing under tree;
- every shot being upward canopy + slow push;
- literal glowing heart flying through sky;
- random leaf particles used as the only action;
- copying the current same-song AIMV’s unknown surface shots.

Learn only principles from benchmarks: first seconds need an event, current motion standards are higher, and full-set camera grammar must vary.

## W04 Production Feasibility

- all 9 first frames can be generated in ChatGPT at W05;
- no human identity continuity burden;
- bird only appears in segments where it is present in the first frame;
- tree/world continuity can be reinforced through repeated trunk architecture, bark scar, palette and light system;
- each 5s clip has one dominant event and one clear camera grammar, matching `rules/ai_video.md`;
- 45s raw material gives sufficient coverage for the 37.12s locked BGM.

## Next Allowed Action

`AESTHETIC_GATE` — user approves or locally revises this director direction.

If `PASS`:
1. lock W04;
2. enter W05;
3. generate complete first-frame prompt set automatically;
4. first generate 2–3 style-anchor images in ChatGPT Image Generation before completing all 9 frames;
5. stop again only when the W05 whole-set aesthetic gate is reached.

Do not enter W05 before this director gate passes.