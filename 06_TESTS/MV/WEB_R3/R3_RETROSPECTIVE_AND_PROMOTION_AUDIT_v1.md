# WEB R3｜Full Retrospective + Promotion Audit v1

> Date: 2026-08-25 Asia/Shanghai
> Branch: `test/mv-web-r3`
> Current production result: `R3-C FULL MV INTEGRATION PASS / HG05 PASS`
> R3 program status: `A PASS / B PASS FOR CURRENT CALIBRATION / C PASS / D NOT STARTED`
> Core conclusion: R3 successfully extended the R2 correctness pipeline into a trend-informed, higher-aesthetic, more director-aware full MV workflow, but R3 as originally chartered is **not fully closed** until Publish Packaging + Live Data Feedback are tested.

---

# 1. Executive summary

R3's most important success is not merely that `如果风会替我说话` looks good.

The stronger evidence is that the workflow now has a more complete upstream-to-downstream chain:

`Douyin observed evidence`
→ `Song-family selection`
→ `Exact Douyin audio-asset verification`
→ `BGM lock`
→ `Audio Timeline Package`
→ `Director / visual calibration`
→ `First-frame set`
→ `Dynamic camera / physics experiments`
→ `Selective source QA / trim`
→ `WEB source rough-cut gate`
→ `Picture Edit`
→ `Locked subtitle baseline`
→ `Final Tech QA`
→ `HG05`.

The final stages were materially smoother than earlier rounds. Once Picture Edit rhythm was accepted and the omitted WEB rough-cut Gate was restored, subtitle integration and final technical rendering passed without a new aesthetic loop. This is a sign that R2 correctness infrastructure is now doing its intended job: final-stage work is becoming implementation rather than repeated redesign.

At the same time, R3 also exposed an important discipline: **one successful song is enough to create reusable Knowledge, but not enough to freeze camera / physics / visual preferences into Golden Runtime.**

---

# 2. Original R3 goals vs outcome

The original Master Plan defined four modules:

| Module | Original question | Final status | R3 evidence |
|---|---|---|---|
| R3-A Music Radar | Can we find rising songs from repeated independent Douyin evidence? | **PASS** | Data Center + direct evidence + HG01 selection |
| R3-B Healing Visual Calibration | Can visual quality / healing feeling improve without destroying production stability? | **PASS FOR CURRENT CALIBRATION** | regenerated first-frame set + dynamic experiments + final accepted MV |
| R3-C Full MV Integration | Can new song discovery + new visual language run through the R2 pipeline? | **PASS / HG05** | final 24.33s accepted MV |
| R3-D Publish Packaging + Live Data | Can packaging and real post data become repeatable? | **NOT STARTED** | no real packaging/live-data calibration yet |

Therefore do not mark the entire R3 program `COMPLETE_LOCKED` yet.

R3-C is closed; the full R3 charter still has D-series work remaining.

---

# 3. R3-A｜Music Intelligence / Douyin Data Center

## 3.1 What changed from earlier song selection

Earlier workflows could discover songs, but R3-A created a durable evidence model instead of relying on one account, one search result, or subjective recommendation.

The current Douyin Data Center is explicitly:
`PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`.

Current locked R3 snapshot:
- 9 core accounts;
- 134 cumulative observed works;
- 98 AUTO_HIGH works in current window;
- 8 repeated SONG_FAMILY candidates;
- refresh cadence about every 15 days.

Missing public observations are treated as `UNKNOWN`, never as negative evidence.

This distinction matters because the Data Center is a **positive-signal radar**, not a claim of complete Douyin platform coverage.

## 3.2 Song selection success

`如果风会替我说话` was observed in 3 independent core accounts and received Data Center grade `STRONG`, including a 3-account 72h concentration signal.

This means HG01 was no longer:
`assistant thinks this song feels good`.

It became:
`observed repeat evidence -> evidence pack -> human aesthetic decision`.

That is a major structural improvement.

## 3.3 Stable data identity choices

R3 correctly separated:
- account external key = `sec_uid`;
- account internal key = `account_id`;
- work key = `aweme_id`;
- trend analysis unit = normalized `SONG_FAMILY`;
- exact production recording = separate `AUDIO_VERSION`.

This prevents nickname changes or multiple audio versions from corrupting trend analysis.

## 3.4 R3-A limitation

The Data Center is strong enough for the first R3 production loop, but it is not a universal popularity oracle.

Do not overclaim:
- complete Douyin coverage;
- negative evidence from missing works;
- performance causality from repeat count alone;
- permanent account weighting before additional refresh cycles.

The next maturity step is repeated refresh + real publication outcome correlation.

---

# 4. Exact BGM discovery｜One of R3's strongest runtime promotions

After HG01, R3 did not search by song title and assume a random full track was correct.

Three independent core-account works were parsed/downloaded/decoded and verified to use the same Douyin music asset:
`7670880580757867270`.

Pairwise Chromaprint similarities were approximately:
- 0.9946;
- 0.9860;
- 0.9863;
with best shift `0`.

This confirmed the same audio family directly from real trend usage.

This is a genuine production-runtime advancement:

`Douyin-native exact music asset first`
→ only then consider asset-anchored full-track extension
→ generic public song-title search becomes fallback.

This capability is already promoted through `rules/mv_bgm_discovery.md` and should remain active.

---

# 5. R3-B｜Visual system: the important improvement was not "prettier people"

## 5.1 Initial failure: visual compression into portraits

The first frame set initially became too close-shot-heavy.

Even when individual images were attractive, the sequence risked becoming:
`same beautiful woman + different light`
instead of a film.

The correction was to treat shot scale and environment as director variables.

After regeneration, the accepted set breathed as:

`EXTREME CLOSE`
→ `CLOSE / REFLECTION`
→ `MEDIUM`
→ `WIDE`
→ `MEDIUM / REFLECTION`
→ `CLOSE`
→ `MEDIUM`
→ `MEDIUM-WIDE / WIDE`.

This was one of the strongest aesthetic corrections in R3.

## 5.2 Environment became narrative

The final first-frame QA showed that:
- S03 used empty warm domestic space to express absence;
- S04 used architecture and distant warm light to express home;
- S05 used reflection geometry to express dream/truth;
- S07 used two imperfect objects to express `我们`;
- S08 used enlarged world space for release.

This moves the project away from "AI beauty portraits" toward actual visual directing.

## 5.3 Visual identity lesson

A distinctive eye region helped maintain character recognition, but R3 should not promote one exact facial recipe, one celebrity-associated reference, one color palette, or one veil look into global runtime.

These remain per-project visual-direction choices.

---

# 6. Camera language｜R3 produced a candidate library, not a finished camera system

R3 deliberately tested multiple camera grammars.

Strongest current positive evidence:
- S03: mild `SLOW DOLLY-OUT REVEAL`;
- S04: foreground partial occlusion / reveal;
- S04 edit: near-full occlusion as motivated hidden-cut opportunity;
- S06/S07: rack-focus as semantic transfer;
- S08: `WORLD-OPENING CRANE / RETREAT` — current benchmark.

Weak / unproven controls:
- exact glass-parallel slider;
- small orbit / arc amplitude;
- diagonal slider;
- micro portrait dolly-in accuracy.

Key lesson:
**a beautiful video does not prove the requested camera movement was actually controlled.**

The next camera tests must be isolated A/B tests on simple scenes and score actual camera execution, not only aesthetics.

R3 camera findings have therefore been stored in:
`04_HARNESS/knowledge/MV_CAMERA_LIBRARY_CANDIDATES.md`
with `POSITIVE_EVIDENCE` status, not as Golden Runtime rules.

---

# 7. Physical plausibility｜The biggest new dynamic-generation lesson

R3 exposed multiple visually attractive but physically wrong outputs:
- rain occupying the wrong side / plane of glass;
- moving rain becoming a large tube-like stream;
- reflection + water geometry becoming ambiguous;
- full foreground cover enabling scene reconstruction;
- hand / veil interaction losing causal clarity;
- ice / droplet behavior becoming unstable.

This changed the dynamic QA mindset.

A source can no longer PASS merely because:
`人物没崩 + 运镜好看`.

It also needs believable:
- surface ownership;
- gravity / flow direction;
- reflection geometry;
- occlusion continuity;
- object causality;
- light-source coherence.

The `ai_video.md` QA layer now explicitly includes physical plausibility checks.

---

# 8. Doubao / Seedance prompt rewrite｜Why the user's rewrite worked better

The user's later S02/S06 rewrite materially improved source usability.

The correct interpretation is not:
`we discovered perfect liquid prompting`.

The better model is:
`CONTAIN + DE-EMPHASIZE + SERIALIZE`.

Observed improvements came from:
- concise high-priority freezes early in the prompt;
- explicit static baseline;
- only one allowed event;
- low-amplitude / weak material verbs;
- quantified local bounds;
- freezing all non-target liquid states;
- finishing the difficult physical event before rack focus / camera action;
- keeping camera fixed when physics was the risky variable.

Exact liquid control was still not proven.

Therefore these have been placed into:
`04_HARNESS/knowledge/MV_DYNAMIC_GENERATION_R3_LESSONS.md`
as next-song hypotheses rather than hard rules.

---

# 9. Rain strategy｜A concrete production simplification

The repeated rain tests support one useful current default hypothesis:

`RAIN AS ATMOSPHERE > RAIN AS HERO PHYSICS`
for ordinary emotional MV scenes.

Prefer:
- fine mostly-static exterior marks;
- wet-glass sheen;
- bokeh and reflection;
- distant rain curtain;
- wet ground;
- subtle environmental response.

Avoid production-critical dependence on:
- droplet creation;
- droplet merge;
- obvious rivulet growth;
- macro fluid transformation.

This remains Knowledge until cross-song replication.

---

# 10. R3-C｜Full MV integration result

R3-C successfully completed the full chain and passed HG05.

Final accepted candidate:
`如果风会替我说话_R3_FinalCandidate_Subtitled_v1.mp4`

Final SHA-256:
`b96ddb81395772395ed8946b3fc30341f124bef14124f47a203dda87a3ef9f42`.

Technical state:
- H.264;
- 720×1280;
- 24fps;
- SAR 1:1;
- container/video ≈24.333s;
- locked BGM only;
- no AI source-audio leakage;
- subtitle geometry/timing PASS;
- watermark handling consistency PASS.

Most important integration evidence:
- the R2 Audio Timeline Package was reused rather than reinvented;
- subtitle style was not reopened;
- picture rhythm was approved without repeated structural re-edits;
- the final subtitle/tech stage completed without a new aesthetic redesign loop.

This is exactly what the R3-C integration test was supposed to prove.

---

# 11. One serious R3 process regression: WEB rough-cut Gate was forgotten

This is the main correctness regression in R3.

The first Picture Edit used raw sources and deferred source watermark/provenance-mark handling to later polish.

That contradicted WEB R2, which had already validated:
`crop=576:1024:72:128 -> scale=720:1280`
= ~1.25× batch-uniform whole-source zoom,
plus corner-risk QA before formal Picture Edit.

The user correctly identified the omission.

R3 then restored this as an explicit independent Gate:
`rules/mv_web_source_roughcut.md`.

The current hard WEB chain is now:

`Dynamic Source QA`
→ `Shot Normalization when needed`
→ **`WEB SOURCE ROUGH-CUT GATE`**
→ `Editor Audio Gate`
→ `Picture Edit / HG04`.

This is a good example of the project's correctness-promotion standard:
`failure -> root cause -> stable rule -> artifact -> independent gate -> regression evidence`.

The historical HG04 receipt should remain unchanged as evidence of the real mistake; the retrospective documents the correction rather than rewriting history.

---

# 12. Why the final stage was almost one-pass

The user reported that the final part was essentially accepted in one pass.

The main reason is architectural, not luck.

By the time Stage 9/10 began:
- BGM identity was already locked;
- lyric timeline was already canonical;
- Picture Edit rhythm was locked;
- WEB clean proxies were restored;
- subtitle style was inherited rather than redesigned;
- subtitle boxes were generated algorithmically from actual glyph bboxes;
- source audio had already been removed.

As a result, the last stage was mostly deterministic implementation and QA.

This is the strongest evidence so far that the project should continue moving technical correctness **upstream**, leaving Human Gates for taste and approval.

---

# 13. Promotion Audit｜What is now Runtime vs Knowledge vs Evidence

## A. ACTIVE / PROMOTED runtime

These are sufficiently mature to remain in active production:

| Capability / discipline | Status | Authority |
|---|---|---|
| Audio Timeline Package after BGM lock | ACTIVE HARD | R2 / `mv_audio_timeline.md` |
| Douyin-first exact BGM asset discovery | ACTIVE HARD PRIORITY | R3 / `mv_bgm_discovery.md` |
| 5 fixed normal Human Gates | ACTIVE | `mv_human_gates.md` |
| Raw source != final shot / trim-required philosophy | ACTIVE | R2 editing/runtime |
| Atom/Arc normalization for complex generated sources | ACTIVE | R2 source normalization |
| Long-cut first / visible-shot fragmentation QA | ACTIVE | R2 editing/runtime |
| WEB source rough-cut before Picture Edit | ACTIVE HARD WEB | R2 restored in R3 / `mv_web_source_roughcut.md` |
| Locked subtitle baseline + glyph-bbox box rebuild | ACTIVE | R1/R2 / `mv_subtitle.md` |
| Dynamic QA includes physical plausibility dimension | ACTIVE QA DIMENSION | `ai_video.md` v1.4 |

## B. POSITIVE EVIDENCE / Knowledge candidates

Reuse on the next song, but do not claim universal truth yet:
- Weakest Sufficient Motion;
- First-frame State Preload for high-risk objects;
- Static Base -> One Allowed Event;
- One Difficult Physics Event per source;
- Control Budget;
- Surface Ownership;
- Weak verbs for high-risk materials;
- serialize material event before camera/focus change;
- rain as atmosphere rather than hero physics;
- partial occlusion for continuity / near-full occlusion for hidden cut;
- S03/S04/S08 camera grammars;
- R3 prompt-control hierarchy.

Authorities:
- `knowledge/MV_DYNAMIC_GENERATION_R3_LESSONS.md`
- `knowledge/MV_CAMERA_LIBRARY_CANDIDATES.md`.

## C. Evidence only / do not promote

Keep only as R3 historical evidence:
- exact S01–S08 visual recipes;
- exact character face / veil / palette;
- exact rain-rivulet timing values;
- exact S06 ice-drop mechanics;
- individual prompt v1/v2/v4 text as universal templates;
- a claim that prohibitions always have lower model weight;
- a claim that prompt token order has a known numeric priority;
- exact camera amplitudes as proven stable;
- final-song performance / growth conclusions before real publication data.

---

# 14. Human Gate / automation review

The project is closer to the intended division of labor:

Humans should decide:
- song taste;
- BGM listening comfort;
- visual direction / first-frame set;
- picture rhythm;
- final acceptance.

Machine/runtime should own:
- exact audio identity;
- timing truth;
- source mapping;
- physical/technical QA;
- source-audio removal;
- watermark-safe WEB proxy generation;
- subtitle geometry;
- final codec / duration / SAR checks.

R3 still required valuable user correction in two areas:
1. aesthetic/director judgment of physical implausibility in generated sources;
2. catching the accidentally skipped R2 WEB rough-cut Gate.

The second one is now structurally fixed. The first should be reduced through Knowledge reuse and next-song validation rather than pretending it is already solved.

---

# 15. R3-D remains open

The original R3 success definition includes:
`trend discovery -> song selection -> healing AI visual MV -> publish packaging -> data feedback`.

We have completed through the MV.

We have **not yet validated**:
- `MUSIC_FIRST` vs `EMOTION_FIRST` packaging;
- cover text / post title / description / hashtags / pinned comment system;
- real post-performance feedback;
- whether Music Radar repeat signals correlate with publication performance;
- whether current healing visual choices improve retention / engagement.

Therefore the correct next R3 step is R3-D, not a false `R3 COMPLETE` label.

---

# 16. Main-branch Promotion Audit

Current Git comparison at closeout:
- `test/mv-web-r3` is `434 commits ahead` of `main`;
- `0 behind`;
- merge base = current main head.

A blind full merge would import a large amount of experiments, probes and historical test artifacts.

Recommended strategy:

### Promote curated production layer
Prioritize reviewed production assets under:
- `04_HARNESS/workflows/`
- `04_HARNESS/rules/`
- `04_HARNESS/templates/`
- selected `04_HARNESS/tools/`
- `04_HARNESS/knowledge/`
- only the GitHub Actions that remain required for production/runtime verification.

### Do not treat test history as runtime
Keep R1/R2/R3 probes, failed prompts, debug ferries and per-round evidence under `06_TESTS` as evidence/archive unless a specific artifact is required by production tooling.

### Data Center requires a deliberate product decision
The R3 Data Center is valuable, but before main promotion decide whether it remains:
- a calibrated R3 research subsystem; or
- becomes a permanent production `Music Intelligence` module in a non-test path.

Do not simply promote the entire `06_TESTS/MV/WEB_R3/database` tree by accident.

---

# 17. Recommended next sequence

1. Finish `R3-D1 Packaging Benchmark` for this accepted MV.
2. Publish one selected packaging direction.
3. Record `R3-D2 Live Data Feedback` after a meaningful observation window.
4. In parallel / next song, repeat the R3 dynamic-generation Knowledge hypotheses and Camera Candidate tests on a different song/world.
5. Promote only cross-song stable items into active rules.
6. Run a curated Runtime-to-main promotion PR instead of merging all 434 commits wholesale.
7. Only after R3-D + cross-song stability evidence decide whether to open R4 as scale/automation optimization.

---

# 18. Final R3-C verdict

`R3-C FULL MV INTEGRATION = PASS`.

What R3 proved:
- trend evidence can select a real production candidate;
- exact Douyin music asset can be verified rather than guessed;
- higher-quality healing visual direction can coexist with the R2 correctness pipeline;
- generated source flaws can often be salvaged through selective trim and motivated cuts;
- camera language is worth systematic testing;
- physical plausibility must be a first-class QA dimension;
- final-stage work can become near-deterministic when upstream truth and technical Gates are respected.

What R3 did **not** prove yet:
- universal liquid-control prompting;
- a universal camera recipe;
- a universal healing visual style;
- publication-performance gains;
- the full R3 packaging/data loop.

This distinction is the correct basis for the next iteration.
