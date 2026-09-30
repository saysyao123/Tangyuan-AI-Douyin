> **2026-09-30 最新变更：本文原来的“仅修 S1C、S0 不重开”指令已被用户后续要求替换。**
> 用户再次试听否决 V3，并要求重审选歌。当前 S0=REOPENED，原《告别》选择撤销，S1 未封存，S2 阻塞。
> 从 RUN_CURRENT_STATE.yaml、S0_CURRENT_STATUS.md、S0_REOPEN_REVIEW_2026-09-30.md 和 s0_reopen/S0_QUALIFICATION_ADDENDUM_v0.4.yaml 继续。
> 下方为当时交接正文，仅保留历史背景，不得按其 S1-only 路径继续重复切音频。

# Work Mode Handoff — MV Runtime Fresh Project Run01

> Date: 2026-09-30  
> Repository: `saysyao123/Tangyuan-AI-Douyin`  
> Branch: `main`  
> Runtime root: `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/`  
> Active run: `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/runs/FRESH_PROJECT_RUN01_2026-09-26/`

---

## 0. Work Mode Start Instruction

This file is the **current handoff and run-level source of truth** for the Fresh Project.

Continue the project from GitHub. Do not ask the user to re-explain prior history.

Important:

- Reuse the frozen S0/S1 runtime contracts and control principles.
- Do **not** reuse old project-specific song/audio decisions.
- Do **not** trust stale global project state for this Fresh Project.
- Do **not** enter S2 DIRECTOR yet.
- Continue **S1 PROJECT_AUDIO**, specifically S1C timeline analysis and final audio selection.
- The user wants the process to remain GitHub-centered: analysis, status, handoff and final delivery should be written back to this repo.

Primary execution principle:

`NO EVIDENCE -> NO STATE TRANSITION`

---

# 1. Original Goal

Build a staged MV production runtime:

```
S0 SONG_SELECTION
  ->
S1 PROJECT_AUDIO
  ->
S2 DIRECTOR
  ->
S3 FIRST_FRAME
  ->
S4 MOTION
  ->
S5 GENERATION
  ->
S6 VIDEO_QA
  ->
S7 ASSEMBLY_FINAL
```

Each stage should:

1. consume only the required upstream handoff;
2. produce concrete artifacts/evidence;
3. pass deterministic checks;
4. use a Judge / Gate where appropriate;
5. be sealed before the next stage begins.

The user prefers:

- one stage at a time;
- isolated tests;
- concrete delivery before review;
- local failure repair instead of restarting everything;
- compact handoffs;
- minimal context drift;
- human confirmation only for high-value creative/quality decisions.

---

# 2. Jev-like / Control Layer Principles To Preserve

The useful Jev influence is architectural, not a requirement to deploy the Jev model itself.

Keep using:

```
State
  ->
Evidence
  ->
Typed Decision
  ->
Action
  ->
New State
```

Key rules:

- GPT/model statements alone do not change stage state.
- `UNKNOWN / BLOCKED / INSUFFICIENT_EVIDENCE` are valid outcomes.
- Generator != Judge where practical.
- Deterministic facts should be checked in code.
- Human Gate is required where subjective listening/creative judgment matters.
- Failure should be localized to the smallest current stage.
- Do not repair S1 failure by silently changing S0.
- Tracker is a view; run-specific handoff/state is the real execution truth.

---

# 3. Important State Warning

The global files below still describe an older project (`若爱有尽头`) and are **not the current Fresh Project truth**:

- `PROJECT_STATE_SCHEMA.yaml`
- `PROGRESS_TRACKER.md`

Do not use their `current_stage=DIRECTOR` state to advance this Fresh Project.

For this Fresh Project, this handoff file overrides stale global state until the Work run updates project/run-specific state correctly.

---

# 4. Fresh Project S0 — Current Truth

Run:

`FRESH_PROJECT_RUN01_2026-09-26`

S0 Contract:

`stages/00_SONG_SELECTION/S0_STAGE_CONTRACT_v0.3.yaml`

Fresh shortlist:

1. `告别` — 桃子假象 Peach Illusion
2. `一个人在家` — 想想XiangXiang
3. `阁楼上的广广` — 张醒婵 / Nono

Selected Song Family:

`告别`

Artist:

`桃子假象 Peach Illusion`

S0 delivery:

`runs/FRESH_PROJECT_RUN01_2026-09-26/S0_DELIVERY.yaml`

S0 status:

`SEALED / PASS`

For this test run, the Song Family Gate was:

`AUTO_CONFIRMED_FOR_TEST`

Do not reopen S0 unless S1 proves the song itself unusable for the target MV mode and a deliberate upstream reopen decision is recorded.

---

# 5. Fresh Project S1 — What Is Actually Confirmed

S1 Contract:

`stages/01_PROJECT_AUDIO/S1_STAGE_CONTRACT_v0.4.yaml`

## S1A MATERIAL_ACQUISITION

Status:

`PASS`

Coverage:

`FULL_SOURCE_ACQUIRED`

Source:

`https://peachillusion.bandcamp.com/track/-`

Full source properties:

- duration: `201.978776s`
- format: MP3
- sample rate: `44100 Hz`
- channels: `2`
- bitrate: ~`128 kbps`
- bytes: `3,232,077`
- SHA256: `6463db1a27b6d3ebdd1541205796f42888cadc281fa2c45e14c07c4fcfaf4a43`

Important success:

This Fresh Project independently acquired the complete source from the public Bandcamp stream. No user upload was required.

The S1A source path is considered valid and should be retained.

---

## S1B SOURCE_VERSION_VERIFICATION

Status:

`PASS`

Verified identity:

`桃子假象 Peach Illusion — 告别`

Release date recorded:

`2026-05-15`

Official/public lyric page exists.

Trusted lyric parser successfully recovered:

- `28` lyric lines
- `178` lyric characters

Do not silently substitute another version/cover/remix.

---

# 6. S1C — Current Real Problem

The remaining problem is **not source acquisition**.

The remaining problem is:

> Build a reliable full-song lyric/audio timeline **before cutting** the production audio.

The user explicitly corrected the process:

```
FULL MP3
  ->
deep full-song timeline analysis
  ->
identify actual lyric / non-lyric / vocalise regions
  ->
choose the production region
  ->
only then cut MP3
```

Do not reverse this order.

---

# 7. Previous S1C Attempts And What Failed

## Attempt A — Structural chorus selection

Historical file:

`S1_DELIVERY.yaml`

It selected a high-energy region around:

`46.068–78.437s`

Reason at the time:

- structural repeat;
- high-energy section;
- assumed chorus.

Problem:

This was selected from structure before proving that concrete lyrics were audibly present.

Treat this as **historical test evidence**, not current truth.

---

## Attempt B — Forced-aligned Chorus 2

Historical file:

`S1_DELIVERY_FINAL_LINE_LEVEL.yaml`

Selected lyric range:

`122.747–138.410s`

Rendered range:

`122.547–138.710s`

Technical forced alignment looked good inside the selected section.

However, the user listened to the actual audio and reported:

> the segment was basically sustained "ah" vocalisation, with no concrete lyrics.

Therefore:

`REJECTED_BY_HUMAN`

This result must **not** be treated as S1 PASS.

Important lesson:

`CTC / forced alignment success != audible lyric truth`

A forced aligner can place known lyrics onto ambiguous/low-intelligibility vocals.

---

## Attempt C — Verse 1 Retest

Current retest files:

- `S1_RETEST_V2_FULL_TIMELINE_BEFORE_CUT.md`
- `S1_DELIVERY_RETEST_V2_CANDIDATE.yaml`

Candidate:

`29.805–46.048s`

Rendered:

`29.555–46.398s`

The user listened and again reported:

> there were still no concrete lyrics.

Therefore:

`REJECTED_BY_HUMAN`

The file still says `HUMAN_AUDIO_REVIEW_PENDING`, but the newest human result supersedes it.

Update this state before sealing anything.

---

# 8. ASR / Alignment Findings

The following methods have been tested:

- Whisper normal transcription
- Whisper tiny
- Demucs vocal separation + Whisper
- Xingyu Lyrics Aligner / WhisperX CTC forced alignment
- full-song structural self-similarity
- local acoustic lexical-change proxies

Results:

### Whisper

For this shoegaze / dream-pop mix:

`UNRELIABLE`

It hallucinated or failed to recover the official lyrics.

A later contrast test across:

- Verse 1 candidate
- Chorus 1
- Verse 2 candidate
- previous Chorus 2

also returned no reliable lyric match.

Therefore:

`Whisper ASR must not be a hard lyric-timeline truth source for this song.`

### Forced Alignment

The aligner successfully matched all 28 trusted lyric lines technically, but at least one line produced a clearly implausible duration outlier.

Whole-song line alignment is therefore:

`PARTIAL_LOW_CONFIDENCE`

Do not promote it to full truth.

### Human listening

Human listening has already rejected two algorithmically selected segments.

This is now mandatory evidence for S1.

---

# 9. Current S1 Truth — Use This

As of this handoff:

```
S1A MATERIAL_ACQUISITION
PASS

S1B SOURCE_VERSION_VERIFICATION
PASS

S1C FULL TIMELINE / LYRIC LOCATION
REVISE / NOT COMPLETE

S1D HUMAN AUDIO LOCK
FAIL / NOT PASSED

S1 STAGE
NOT SEALED

S2 DIRECTOR
BLOCKED
```

Do not use older `SEALED` S1 files as current state.

---

# 10. Files That Are Historical / Superseded

These files are useful evidence but must not be treated as current S1 truth:

- `FINAL_REPORT.md`
- `S1_DELIVERY.yaml`
- `S1_DELIVERY_FINAL_LINE_LEVEL.yaml`
- `S1_FINAL_AUDIO_META.json`
- previous `validator_result.json`
- previous S1 final audio artifacts
- global `PROJECT_STATE_SCHEMA.yaml`
- global `PROGRESS_TRACKER.md`

Why:

They were created before the latest human listening feedback proved that the selected audio did not contain useful concrete lyrics.

---

# 11. Files Work Should Read First

Read these in order:

1. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/00_SONG_SELECTION/S0_STAGE_CONTRACT_v0.3.yaml`
2. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/stages/01_PROJECT_AUDIO/S1_STAGE_CONTRACT_v0.4.yaml`
3. `08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/runs/FRESH_PROJECT_RUN01_2026-09-26/S0_DELIVERY.yaml`
4. this file: `WORK_MODE_HANDOFF_2026-09-30.md`
5. `S1_RETEST_V2_FULL_TIMELINE_BEFORE_CUT.md`
6. `S1_DELIVERY_RETEST_V2_CANDIDATE.yaml`
7. `s1_forced_alignment/alignment_summary.json`
8. full-source structural analysis files under:
   - `s1_runtime_v2/`
   - `s1_structure/`

Do not use old final reports as authoritative state.

---

# 12. Work Mode Next Task

Continue only S1.

Do not start S2.

The next task is:

> Rebuild S1C around the complete 201.978776s MP3 and produce a trustworthy lyric/audio timeline before any new production cut is accepted.

Required flow:

```
FULL_SOURCE_ACQUIRED
        ↓
FULL-SONG STRUCTURE ANALYSIS
        ↓
FULL-SONG VOCAL / INSTRUMENT / VOCALISE MAP
        ↓
TRUSTED-LYRIC EVIDENCE
        ↓
LOCATE WHERE CONCRETE WORDS ARE ACTUALLY SUNG
        ↓
CANDIDATE REGIONS
        ↓
AUDIBLE-LYRIC VERIFICATION
        ↓
SELECT PRODUCTION REGION
        ↓
CUT FINAL MP3
        ↓
HUMAN AUDIO REVIEW
        ↓
PASS -> S1 SEALED
FAIL -> REVISE S1C ONLY
```

---

# 13. Strong Recommendation For The S1C Repair

Do not optimize for "chorus" first.

Optimize for:

`a usable MV segment with concrete, audible, semantically meaningful lyrics`

A good candidate must satisfy all of the following:

1. actual source audio exists;
2. section boundaries are musically coherent;
3. concrete lyric content is audibly present;
4. lyric order matches the trusted official lyric source;
5. start/end do not cut through a phrase;
6. segment length is practical for MV production;
7. human listening confirms the segment really contains the expected lyrics.

If no segment passes this standard:

`S1 should reject the song for lyric-driven MV use.`

Do not force a PASS.

If rejected, reopen S0 intentionally and document the reason:

`LYRIC_INTELLIGIBILITY_UNSUITABLE_FOR_TARGET_MV_MODE`

---

# 14. New Required S1 Gate

Add a mandatory gate before S1D:

`AUDIBLE_LYRIC_VERIFICATION`

Suggested typed output:

```yaml
audible_lyric_verification:
  segment_start: float
  segment_end: float
  trusted_lyric_ids: [...]
  concrete_words_audible: TRUE | FALSE | INSUFFICIENT
  phrase_boundaries_clean: TRUE | FALSE
  asr_support: SUPPORTS | WEAK | CONFLICTS | UNAVAILABLE
  forced_alignment_support: SUPPORTS | WEAK | CONFLICTS
  human_audio_review: PASS | FAIL | PENDING
  route: PASS | REVISE | REJECT_SONG
```

Rules:

- ASR cannot independently PASS this gate.
- Forced alignment cannot independently PASS this gate.
- Human audio review can reject a technically green candidate.
- No S1 Seal until this gate is PASS.

---

# 15. GitHub Update Requirements

Work should continue to write changes into:

`08_AGENT_CONTROL_LAYER/runtime/MV_RUNTIME_V0_1/runs/FRESH_PROJECT_RUN01_2026-09-26/`

Recommended new files:

- `S1_CURRENT_STATUS.md`
- `S1C_FULL_TIMELINE_V3.md`
- `S1C_AUDIBLE_LYRIC_GATE_V1.yaml`
- `S1_DELIVERY_V3_CANDIDATE.yaml`
- final audio artifact metadata
- validator result

Once the new S1 is proven:

- update run-level status;
- then reconcile the global Project State / Tracker;
- only then allow S2.

Do not update global state to DIRECTOR until the user approves the final S1 audio.

---

# 16. Expected User-Facing Delivery From Work

The user wants the eventual S1 delivery to contain exactly these practical outputs:

## A. Full-song timeline

A readable timeline such as:

```
00.000–xx.xxx  intro / no usable lyrics
xx.xxx–xx.xxx  lyric line / semantic meaning
xx.xxx–xx.xxx  transition
...
```

It must distinguish:

- instrumental;
- atmospheric vocal;
- sustained "ah/oh" vocalise;
- concrete sung lyrics;
- transitions;
- usable MV candidate regions.

## B. Final selected lyric timeline

For the chosen production segment:

```
time start -> time end
lyric line / semantic cue
confidence
```

## C. Final cut audio

Provide the actual MP3 to the user.

## D. S1 final handoff text

Include:

- source;
- exact segment;
- duration;
- lyric timeline;
- validation evidence;
- Human Audio Lock;
- whether S1 is SEALED.

---

# 17. User Preference / Interaction Rule

For the next Work run, the user does **not** want repeated clarification questions.

Make reasonable decisions independently during testing.

Only stop for user confirmation when there is an actual concrete S1 audio candidate to review.

The user specifically wants:

> first deeply analyze the full song timeline, then choose and cut the MV segment.

This requirement has priority over old S1 implementations.

---

# 18. Current Bottom Line

```
Fresh Project: 告别 — 桃子假象 Peach Illusion

S0:
SEALED

S1A:
PASS / FULL_SOURCE_ACQUIRED

S1B:
PASS

S1C:
REVISE

Previous candidate 1:
REJECTED_BY_HUMAN
(reason: sustained vocalisation / no concrete lyrics)

Previous candidate 2:
REJECTED_BY_HUMAN
(reason: still no concrete lyrics)

S1D:
NOT PASSED

S1:
NOT SEALED

S2:
BLOCKED
```

The next Work action is **not** Director design.

The next Work action is:

`repair S1C full-song lyric timeline -> produce a genuinely audible lyric candidate -> deliver audio + timeline for human review.`


