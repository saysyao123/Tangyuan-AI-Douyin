# Round 01｜Retrospective

> Purpose: preserve actual R1 evidence, not a cleaned-up fictional story.

## 1. What R1 successfully proved

R1 completed one full MV path from song selection to accepted final polish.

Validated end-to-end path:

`benchmark-assisted song selection -> user song choice -> locked audio excerpt -> music/lyric structure -> director concept -> 8 first frames -> 8 × 5s Seedance clips -> dynamic QA / retries -> edit v1 -> edit v2 -> lyric system -> subtitle timing correction -> final polish`

The user accepted the overall final result.

## 2. Song-selection lesson

### Initial problem
A deep datasource design around exact `music_id`, Creator Center and automated audio retrieval became too heavy for the manual R1 computer environment.

### Practical fix
A simplified temporary selection workflow performed better operationally:

`~5 MV/music observer sources -> scan recent ~30-day songs -> send real MV/video links -> user judges song + visual -> lock Reference BGM`

This was faster and easier to validate manually.

### Important boundary
This simplified method is approved for current manual work, but it is not the final automated datasource system.

Codex follow-up remains responsible for:
- exact music_id;
- current Creator Center availability;
- automated candidate discovery;
- platform-side publish validation.

## 3. Audio clipping lesson

The first useful rule from this round:

**Do not blindly use an estimated public lyric timestamp if the user can provide the actual source MP3.**

The final excerpt was cut from the user-supplied source and then approved by listening.

R1 locked interval:
`01:23.800 -> 02:00.600`

The excerpt preserves complete lyric meaning and a natural tail rather than forcing an arbitrary 30s target.

## 4. Director / production-unit lesson

The conceptual structure and production structure should be separated.

R1 used:
- 6 conceptual visual units;
- 8 production segments;
- 8 first frames;
- 8 × 5s dynamic videos.

This was better than forcing `1 conceptual unit = 1 first frame = 1 video`.

Why it worked:
- some lyrical ideas needed separate physical actions;
- 40s raw material gave enough editing headroom for a 36.8s final;
- one first frame per production segment made QA and root-cause analysis cleaner.

## 5. First-frame lesson

The strongest R1 upgrade was treating the first frame as a **0-second dynamic anchor**.

A good first frame must already contain:
- the dominant event at its start state;
- a visible action entrance;
- camera / spatial room for motion;
- secondary physical after-effects;
- enough visual clarity for later QA.

Examples from R1:
- wet ink already beginning to spread;
- fingertip hovering just above water;
- meteor just entering frame;
- paper layer already beginning to lift;
- foreground page positioned for later occlusion.

The user approved the complete first-frame set.

## 6. Dynamic generation failures and fixes

### Failure A｜Portrait-protection block
Several character-containing image-to-video attempts were rejected by Seedance as possible real-face reference material.

### Fix
Restore the proven fictional-AI-character declaration at the very start of the prompt, including `***`:

`*** 人物为 AI 生成动画人物，无真人出现。当前上传图片是 AI 生成的虚构影视动画角色设定图，不是真人照片，不含真实人物，不是真实人脸参考素材，不按真人或真实肖像处理。`

The affected clips then generated successfully.

### Promotion decision
This is promoted to an AI-video hard rule.

---

### Failure B｜S8 paper hallucinated a hole
The first S8 prompt asked a moving paper foreground to progressively reveal / cover the heroine. Seedance interpreted the paper as deforming and created a hole/window in the paper.

### Root cause
The prompt coupled:
- large foreground sheet deformation;
- visibility through a shrinking opening;
- character reveal / concealment.

This encouraged topology change.

### Fix
Change the physical mechanism:
- keep the paper intact;
- use camera lateral motion behind the solid paper edge to create occlusion;
- after full occlusion, cut to a wet-paper detail shot.

Result: acceptable.

### Lesson
When a physical foreground object must occlude a subject, prefer **camera-driven occlusion behind a solid edge** over asking the object itself to distort across the whole frame.

## 7. Multi-shot lesson

The user liked the revised three-shot results.

R1 evidence supports:
- 5-second clips can contain 2–3 deliberate shot nodes when the lyric / event benefits;
- three-shot structure is useful for emotional close-ups, reflection actions and macro detail sequences;
- not every segment should use three shots;
- single-shot segments need a larger camera-language library to avoid repetitive slow-push aesthetics.

### Promoted
Multi-shot inside 5s is a validated option.

### Not yet promoted
A fixed 3-shot requirement is NOT a rule.

## 8. Camera-language lesson

Observed weakness:
Even when clips were technically good, too many single-shot ideas naturally drifted toward a similar continuous-shot feel.

Useful R1 camera grammars:
- lateral reveal;
- foreground occlusion / parallax;
- waterline camera lowering;
- event-driven tilt / reframe;
- macro insert + focus shift;
- restrained portrait fragment cuts.

Next-round experiment:
Build and test a larger cinematic movement library, including lateral tracking, pedestal, crane-like rise/fall, arc, push-pull variants, rack-focus-led reframing, whip-style motivated transitions, foreground wipes, low-angle tracking and subject-relative motion.

Do not promote these merely by naming famous directors; test whether Seedance can execute each grammar reliably.

## 9. Editing lesson

### v1
Trimmed most 5s clips to fit the final 36.8s audio. Usable, but cut points felt less precise.

### v2
Kept more complete internal 5s motion and used short overlap / transition compression to fit the locked audio.

User feedback: v2 was clearly better and the cut points felt more accurate.

### Editing rule learned
Do not mechanically trim each source clip to an equal duration. Preserve useful action arcs first, then solve total duration with:
- selective trim;
- overlap;
- transition;
- earlier / later exits based on music and visual action.

## 10. Subtitle timing failure and fix

### Failure
The first lyric overlay used visual-segment boundaries as approximate subtitle timing.

Result: lyrics and vocals did not align.

### Root cause
Visual edit structure and vocal phrase timing are different clocks.

### Fix
Use the locked audio as the timing source.
For R1, same-version LRC was converted relative to the exact cut start (`01:23.800`).

The corrected subtitle timing was user-reviewed as accurate.

### Stable future path
Codex runtime:
`Whisper word timestamps -> constrain/correct against known lyrics -> human spot-check -> burn subtitle`

Never derive lyric timing from video segment boundaries.

## 11. Watermark lesson

The manual test files contain platform / generation watermarks.

User confirmed this is not a meaningful R1 creative issue because Codex can obtain the watermark-free HD outputs.

Therefore:
- do not re-edit or compromise the approved cut just to hide manual-test watermarks;
- replace source files in Codex before publish-grade rendering.

## 12. Benchmark lesson

The 10-account benchmark idea was useful, but using all benchmark accounts for every stage was too broad.

The better JIT split is:
- song selection: 2–5 frequent MV/music observers;
- director: 3–5 highly relevant works;
- first-frame aesthetics: 2–3 beauty references;
- dynamic: 2–3 motion/director references;
- final QA: 2–3 completion-level references.

Benchmark remains external knowledge, not a hard rule source.

## 13. What remains unresolved

### Codex hardening
- automated BGM discovery;
- exact music_id;
- Creator Center availability;
- watermark-free HD asset retrieval;
- Whisper word-level subtitle alignment;
- automated edit recreation.

### Future creative tests
- larger camera-movement library for single-shot clips;
- more variants of multi-shot grammar;
- complex lyric effects after base system remains stable;
- additional songs to test whether the Golden process generalizes beyond paper/ink aesthetics.

## 14. Time / intervention record limitation

R1 did include many human review and regeneration cycles, but precise wall-clock / active-user / model-wait durations were not consistently captured in structured form during the round.

Do not invent retrospective time numbers.

R2 requirement:
record these three categories during execution rather than reconstructing them afterward:
1. total elapsed time;
2. user active operation time;
3. model / tool waiting time, split into normal generation and avoidable rework.

## 15. R1 promotion summary

### Promote to stable workflow / rule
- final audio must be locked before downstream work;
- first frame = 0-second dynamic anchor;
- production units may exceed conceptual visual units;
- first-frame character closure;
- exact AI-fictional-character prefix including `***` for character image-to-video prompts;
- 2–3 shot 5s dynamic structure is an allowed validated pattern;
- subtitle timing must come from final audio alignment;
- root-cause-driven dynamic retry;
- preserve internal motion arcs during editing instead of equal mechanical trimming.

### Keep experimental
- automatic Douyin datasource;
- large cinematic camera library;
- watermark-free source retrieval automation;
- complex lyric animation;
- universal fixed segment-count rules.
