# OSS MV Optimization Result Matrix v2.0

Status: `COMPLETE / D02-B S16 RELEASE_READY / CLOSE AUDIT PASS`

## Test identity

- Experiment branch: `test/mv-oss-optimization-r1`
- Stable baseline branch kept untouched during experiment: `test/mv-web-r3`
- Runtime baseline fork SHA: `89852ec5314e7579853683ef5eb40adb09f25753`
- Test MV slot: `D02-B / Lane S`
- Song: `有几次想你了`
- HG02 BGM: exact Douyin music object `7670104695834282815`, accepted B variant
- External OSS source: `penposs/mvmaker-h3-skills@796797030275fe57afaba736771e8510c848799d`
- Final accepted render: `D02-B_有几次想你了_最终候选_字幕版_v1.mp4`
- Final render SHA-256: `7f77a41a68db47d4f7992cb77161c86414eeb0fd1cf8233322956b4025bf43d9`
- Canonical Runtime final pre-publish state: `S16_RELEASE_PACKAGE_READY / RELEASE_READY`

## Comparison boundary

The Director A/B comparison was deliberately performed at plan level under controlled constants. Candidate B (`R3 + OSS overlay`) won that comparison and was then taken through the full downstream production chain. A separate full baseline-A final render was **not** produced; therefore this experiment can prove that B is viable and useful end-to-end, but must not pretend to have a pixel-level final-render A/B causal delta.

## Director A/B result

| Dimension | A R3 | B OSS overlay | Result |
|---|---:|---:|---|
| Lyric visual hit | 4.3 | 4.6 | B advantage |
| Whole-MV coherence | 3.9 | 4.8 | strong B advantage |
| Director / camera motivation | 4.4 | 4.9 | strong B advantage |
| Shot diversity without incoherence | 4.5 | 4.7 | B advantage |
| First-frame performability | 4.6 | 4.6 | tie |
| Expected dynamic stability | 4.7 | 4.6 | slight A advantage at plan stage |
| Edit-source usability | 4.4 | 4.8 | B advantage |
| Character / identity continuity | 4.7 | 4.7 | tie |
| Production burden | 4.8 | 4.5 | A simpler |
| Runtime compatibility | 5.0 | 4.9 | effectively equivalent; B is bounded overlay |
| Zero-context reproducibility | 4.3 | 4.9 | strong B advantage |

Authority for these scores: `D02-B/05_DIRECTOR/AB/AB_EVALUATION.md`.

## Downstream validation of selected B

### First Frame / HG03

`PASS`

- lyric-specific hit: PASS;
- standalone beauty: PASS;
- same character / wardrobe / coastal world: PASS;
- set differentiation: PASS;
- K0 performability: PASS;
- user accepted set for HG03;
- actual K0 pixels correctly overruled stale prose when they diverged.

### Dynamic generation / source QA

`PASS / NO REGEN REQUIRED`

Five raw ~5s sources were accepted. The generated material contained approximately 13 visible internal atoms:

- approach;
- hand/boundary;
- restraint;
- almost-speak;
- turn-away;
- post-rain travel;
- wet-stone foot detail;
- returning light;
- gust;
- linen residue;
- still holding;
- hand release;
- world opening.

All seven lyric lines obtained direct visual coverage. Identity, white-linen wardrobe and coastal world remained continuous. Decision: `TRIM/ATOMIZE; DO NOT REGENERATE`.

### Normalization / Edit

`PASS`

- raw sources: 5;
- detected visible atoms: 13;
- high/very-high edit-value atoms: >=11;
- all seven lyrics covered;
- internal cuts read as action/intention/information changes rather than random montage;
- Runtime context changed to `multi_shot=true` at the registered S08 point;
- normalized Shot Library and WEB Source Rough Cut Gates passed;
- final dense lyric-first picture preview used ~13 visible atoms instead of stretching four/five large source blocks;
- user accepted HG04 picture rhythm.

Final visible emotional progression:

`靠近 -> 边界/手部 -> 忍住 -> 想说 -> 转身算了 -> 雨后湿石 -> 脚步细节 -> 风穿过 -> 纱帘余韵 -> 仍握住 -> 松手 -> 世界打开`

### Subtitle / Final QA / HG05

`PASS`

- inherited locked R1 / WEB R2 subtitle baseline; no style re-exploration;
- 7/7 lines use fresh glyph-bbox-derived boxes;
- equal 10px padding on all four sides;
- text/box center error 0px;
- maximum 24fps timing quantization error < 1 frame;
- final render duration 15.375s / 369 frames;
- H.264 / 720x1280 / 24fps / SAR 1:1;
- final AAC stream identity matches accepted HG04 preview;
- user explicitly accepted final candidate at HG05;
- Release Package built under `MUSIC_FIRST` and Runtime advanced to S16.

## Runtime / process findings

### Finding 1 — Executor discovery gap

The experiment exposed a real architecture defect: Runtime previously answered WHAT stage is next more strongly than HOW that stage is already implemented. This led to premature one-off Audio Timeline tooling.

Remediation on the experiment branch:
- `mv_stage_executor_registry.json` covers S00-S18;
- `mv_executor_first.md` blocks premature helper/model creation;
- canonical executor/tool/capability paths are JIT-routed before new implementation;
- per-slot production model installation and slot-specific core helpers are rejected by default.

Decision: `PROMOTE_RUNTIME_CANDIDATE`, subject to explicit stable-branch promotion review.

### Finding 2 — Audio Timeline route

Validated priority:

`P0 SAME_VERSION_LRC -> P1 D01B_LIGHTWEIGHT_FASTER_WHISPER -> P2 XINGYU_CTC_FALLBACK`.

D02-B independently validated P1 with seven audited lines and 100% mapped lyric-character coverage. P2 remains heavier fallback only.

Decision: `PROMOTE_RULE_CANDIDATE`; do not add default second-model verification.

### Finding 3 — Partial creator caption is not lyric truth

The first four-line lyric state was proven incomplete and was formally rolled back. The corrected seven-line timeline became canonical truth.

Decision: `HARD REJECT` partial caption/description/hashtag text as complete lyric authority.

## OSS optimization decisions

| ID | Final decision | Evidence / boundary |
|---|---|---|
| OSS-01 Director Thesis | `PROMOTE_KNOWLEDGE` | strong plan-level coherence gain; downstream B completed successfully |
| OSS-02 Primary Visual Engine | `PROMOTE_KNOWLEDGE` | helped one-world continuity without changing source count |
| OSS-03 explicit audiovisual relation | `PROMOTE_KNOWLEDGE` | strengthened lyric arcs without one-shot-per-line illustration logic |
| OSS-04 motive-first camera-subject-space | `PROMOTE_KNOWLEDGE` | camera motivation remained readable through final edit |
| OSS-05 WHY CUT HERE / montage reason | `PROMOTE_KNOWLEDGE / RULE_CANDIDATE` | 13 useful atoms and dense lyric-first edit validated; needs another MV before hard rule promotion |
| OSS-06 optional-element trigger/function/stop condition | `PROMOTE_KNOWLEDGE` | bounded decorative risk without extra model dependency |
| OSS-07 Creative Drift QA | `PROMOTE_KNOWLEDGE / CHECKLIST` | useful across Director -> K0 -> Dynamic Prompt; actual K0 pixel authority retained |
| OSS-08 H3 10-15s integer containers | `REJECT FOR R3` | model-adapter constraint, conflicts with stable ~5s Seedance strategy |
| OSS-09 H3 16:9 four-panel Picture-1 | `REJECT FOR R3` | adapter packaging, not general director truth |
| OSS-10 RunningHub/H3 orchestration | `REJECT FOR THIS PATH` | unrelated execution boundary; no benefit to current Web/Seedance Runtime |

## Net verdict

`OSS_OPT_R1 = PASS WITH SELECTIVE PROMOTION PROPOSALS`.

What proved valuable is **not importing mvmaker-h3-skills wholesale**. The net-positive layer is a small bounded Director/Montage knowledge overlay:

1. Director Thesis;
2. one Primary Visual Engine;
3. explicit audiovisual relationship;
4. motive-first camera-subject-space reasoning;
5. WHY CUT HERE montage justification;
6. optional-element stop conditions;
7. Creative Drift QA.

The source project's H3 container/input/orchestration constraints remain rejected for R3.

The experiment also produced independent Runtime/process improvements (Executor-First routing and Audio Timeline route hardening). Those are promotion **candidates**, not silently deployed stable truth.

## Closure boundary

D02-B is closed at `S16_RELEASE_PACKAGE_READY` because the MV is accepted and publish-ready but has not been confirmed live. S17/S18 are real-world post-publish stages and remain intentionally untouched.

Stable branch `test/mv-web-r3` remains unchanged by this experiment until a separate explicit promotion action is approved.
