# WEB R2｜R1 vs R2 Process Comparison & Runtime Inheritance Fix v1

> Purpose: explain why R1 Golden lessons existed but were not fully reused in WEB R2, and define the safer combined process.
> Date: 2026-08-21

## 1. Executive conclusion

R1 knowledge was **documented**, but not all of it was **operationalized**.

The failure was not “R1 had no lesson”. R1 already recorded the exact subtitle-timing failure and fix. The failure was:

`historical lesson existed -> principle sentence promoted -> no mandatory artifact/gate -> R1 history excluded from default runtime -> WEB R2 could still bypass the principle`.

The correct fix is not to load all R1 history every round. The correct fix is:

`Golden history -> cross-round runtime contract + required state/artifact + self-audit gate`.

A new always-loaded rule now exists:
`04_HARNESS/rules/mv_golden_runtime.md`.

`04_HARNESS/MANIFEST.md v3.2` now requires it for every MV task.

---

## 2. What R1 actually did

R1 validated the full path:

`benchmark song selection -> actual audio lock -> music/lyric structure -> director -> first frames -> dynamic generation -> dynamic QA -> edit v1 -> edit v2 -> lyric system -> subtitle timing correction -> final polish`.

Important: R1 itself did NOT get subtitles right on the first try.

R1 subtitle failure:
- first lyric overlay used visual segment boundaries as approximate subtitle time;
- vocals and lyrics did not align.

R1 correction:
- return to the locked audio;
- use same-version LRC;
- convert LRC timestamps relative to exact source cut start (`01:23.800`);
- user reviewed corrected timing as accurate.

Therefore R1's *final successful process* contained a repair loop that was more reliable than its initial formal workflow.

---

## 3. What was promoted from R1

R1 correctly promoted several stable lessons:
- lock actual audio before downstream work;
- first frame = 0-second dynamic anchor;
- production units can exceed conceptual units;
- character prompt safety prefix;
- 2–3 shots are allowed, not mandatory;
- root-cause dynamic retry;
- preserve internal motion arcs instead of equal trimming;
- subtitle timing comes from locked audio, not picture segments.

However, some promotions were **semantic only**.

Example:
`subtitle timing comes from locked audio`
was present as a rule sentence, but there was no required runtime artifact named `LYRIC_TIMELINE_LOCKED` and no hard stop before picture editing.

That gap allowed the same failure to recur.

---

## 4. Why WEB R2 failed to fully reuse R1

### Cause A｜Golden was defined mostly as a quality floor, not a runtime inheritance contract

WEB R2 launch said R1 is a `Golden Quality Floor` and historical R1 files should be loaded JIT only.
This successfully prevented context bloat and creative copying, but it also meant the normal runtime did not automatically reload the exact R1 failure/fix evidence.

### Cause B｜Manifest intentionally excluded R1 history from default runtime

The old Manifest said:
- load workflow + current state + stage rules;
- R1 retrospectives/failure samples only for debugging.

That is good architecture **only if every correctness-critical lesson is already fully promoted into runtime rules/gates**.
It was not.

### Cause C｜Workflow v1.1 had correct principle but weak stage ordering

Old flow still had:
- Stage 8 = picture edit;
- Stage 9 = lyric/subtitle alignment.

This structurally encouraged `edit first -> solve timing later`.
R1 had succeeded only after correcting this behavior, but the workflow ordering did not embody the successful final behavior.

### Cause D｜No durable lyric-timeline artifact

R2 W03 produced:
- lyric text;
- emotional curve;
- Natural Beats;
- approximate phrase structure.

It did NOT produce a strong-evidence line-level timing asset.

At W08 the system treated:
`exact lyric text + waveform/phrase valleys`
as good enough.
That was an invalid downgrade.

### Cause E｜Automation-goal bias

WEB R2 was explicitly testing how much the web client could automate.
When Whisper/forced alignment was not immediately available, the system implicitly optimized for “keep W08 AUTO” instead of obeying the quality floor and marking the stage blocked.

This violated the launch principle:
`不得为了自动化而降低质量门槛`.

### Cause F｜Golden asset discoverability was weak

R1 Golden state references `lyrics_exact_v3_1.srt`, but the runtime start contract did not expose a canonical path/package for that asset and the subtitle visual spec lived mainly in acceptance/retrospective documentation.
A new round should not need to hunt through history to rediscover a Golden asset/spec.

---

## 5. R1 vs initial WEB R2

| Dimension | R1 final successful path | Initial WEB R2 | Better |
|---|---|---|---|
| Audio source lock | actual source, user-listened lock | stronger hash + boundary gate | R2 |
| Lyric text / structure | good semantic structure | good semantic structure | Tie / R2 slightly more explicit |
| Line-level lyric timing | eventually corrected with same-version LRC | not locked before edit | R1 final |
| Director / camera | good, but camera library limited | significantly richer mixed shot structures | R2 |
| First-frame system | 0s anchor validated | retained + stronger set-level diversity | R2 |
| Dynamic QA | root-cause retries | stronger status taxonomy + trim-vs-regen logic | R2 |
| Source audio policy | less explicit | stronger strip/ignore policy | R2 |
| Editing | v2 selective trim/overlap validated | retained, plus source-pool trim logic | R2 if timing truth is correct |
| Subtitle visual style | Golden accepted | drifted in first R2 cut | R1 |
| Subtitle sync | corrected and user-validated | failed first cut | R1 |
| Runtime gating | human iterative correction | originally weak; now v1.2 hard gates | new R2 v1.2 |
| Automation honesty | manual-heavy but failures visible | first cut overstated AUTO until user caught failure | R1 / new v1.2 improves |

---

## 6. Which process is actually best

Neither original R1 nor initial R2 should be copied wholesale.

Best path is a **hybrid**:

### Keep from R1
- actual-source-first discipline;
- subtitle timing correction based on locked audio / same-version timing evidence;
- Golden subtitle visual baseline;
- selective trim / overlap editing;
- human-visible final acceptance standard.

### Keep from R2
- audio identity/hash and boundary gate;
- stronger first-frame diversity;
- Director Shot-Structure Selector;
- richer Camera Contract system;
- source-video QA statuses (`PASS_FULL / TRIM_REQUIRED / REGEN_WATCH / REGENERATE`);
- stronger AI source-audio policy;
- no-skip runtime states.

### Add as the missing architecture
- always-loaded cross-round Golden runtime contract;
- every correctness-critical lesson must produce a required artifact/state and a self-audit gate;
- missing capability means `BLOCKED`, not silent downgrade.

---

## 7. Recommended future flow

### Current safe production flow (v1.2)

`REFERENCE_BGM_LOCKED`
→ `BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ director / first frames / dynamics
→ `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT`
→ `LYRIC_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ `EDIT_MAP_LOCKED`
→ `EDIT_PREVIEW_QA_PASS`
→ `SUBTITLE_STYLE_QA_PASS`
→ `SUBTITLE_SYNC_QA_PASS`
→ `FINAL_TECH_QA_PASS`
→ `DELIVERABLE_RENDERED`

This is already much safer than R1's original workflow because picture edit is blocked until timing truth exists.

### Recommended next-round experiment (candidate v1.3)

Move the line-level timeline acquisition earlier, immediately after BGM / lyric-text lock:

`BGM_LOCKED`
→ `LYRIC_TEXT_LOCKED`
→ `LYRIC_LINE_TIMELINE_LOCKED`
→ `BEAT_MAP_VERIFIED`
→ Director
→ First Frames
→ Dynamic
→ QA
→ Edit
→ Subtitle
→ Final QA

Why test this:
- director allocation can see true lyric durations;
- production segment coverage can be calculated against real phrase windows;
- no late W08 surprise when all visuals are already generated;
- cut points and lyric-hit planning share one audio truth from the beginning.

Why not instantly declare it a hard universal rule yet:
- moving timing alignment earlier changes production latency / tooling requirements;
- it should be validated on WEB R2 completion or next Round before final promotion.

Base subtitles need only reliable **line-level** timing. Word-level timing remains optional unless karaoke / per-word animation is requested.

---

## 8. New promotion standard

For future lessons:

### Creative preference
Store as Knowledge / Experiment until repeatedly validated.

### Production technique
Promote to Rule after repeated validation.

### Correctness failure
Must be promoted to all three:
1. Rule;
2. required artifact/state;
3. automated/self-audit Gate.

A correctness lesson is not fully promoted until the runtime can prevent the same failure without the user remembering it.

---

## 9. Runtime changes already applied

1. Added:
`04_HARNESS/rules/mv_golden_runtime.md`

2. Updated:
`04_HARNESS/MANIFEST.md v3.2`

Every MV task now loads the Golden Runtime Contract by default.
Full R1 history remains JIT-only.

This preserves context efficiency without losing inherited correctness rules.

3. Existing `workflows/mv.md v1.2` already adds the no-skip state chain and W08A lyric-timeline blocking gate after the current WEB R2 failure.

---

## 10. Final diagnosis

The core failure can be summarized as:

> **R1 was successfully复盘, but the project treated “written lesson” as equivalent to “runtime reuse”. They are not the same.**

Reliable reuse requires:

`Golden evidence -> normalized runtime rule -> canonical artifact -> mandatory Gate -> regression check`.

That is the architecture the project should use from now on.
