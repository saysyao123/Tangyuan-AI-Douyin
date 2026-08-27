# OSS_OPT_R1｜End-to-End MV Execution Audit v1

Status: `AUDIT COMPLETE / REMEDIATION IN PROGRESS`
Date: `2026-08-27`
Scope: Canonical MV Runtime `S00` through `S18` on `test/mv-oss-optimization-r1` only.
Stable production branch `test/mv-web-r3` is not modified by this audit.

## 1. Trigger

During D02-B after HG02, the Agent read the Audio Timeline Rule, noticed Xingyu as an allowed alignment implementation, and began building a slot-specific helper / GitHub Actions execution path before first reading the repository's already-existing canonical Audio Timeline executor.

This caused unnecessary tool calls, Actions runs, dependency/model setup, Tokens, and temporary artifacts.

This is classified as a **process architecture failure**, not merely a one-off operator mistake.

## 2. Root cause

The repository already had the intended guardrail:

- `04_HARNESS/SKILL.md` = thin router;
- `04_HARNESS/MANIFEST.md` = task load matrix + Audio Timeline executable JIT path;
- `04_HARNESS/tools/mv_audio_timeline/*` = canonical implementation;
- `alignment_runtime.lock.json` = locked dependency/model identity;
- regression workflows = executable correctness evidence.

However, the newer Canonical Runtime startup path optimized around state truth and JIT rules. `MV_30D_60_NEW_CHAT_START_PROMPT.md` and `mv_resume_contract.json` did not make the existing executor map a first-class Runtime object. In particular, S02's Runtime JIT only named `rules/mv_audio_timeline.md`.

Therefore the Runtime reliably answered **WHAT stage is next**, but not strongly enough **HOW that stage is already implemented**.

## 3. Correct architectural split

From now on:

- `mv_stage_registry.json` = WHAT evidence defines each stage.
- `mv_resume_contract.json` = WHAT action follows current state.
- `mv_stage_executor_registry.json` = HOW that action is executed using existing repository truth.
- `mv_executor_first.md` = hard admission rule preventing premature new implementation.
- Stage Rules = constraints / quality contracts.
- Tools / deterministic recipes / capability handoffs = executors.
- Human Gate Registry = user decision boundary.

A Rule is not an Executor.
A reference to an external project is not permission to install it.
Absence of a Python script does not imply an implementation gap.

## 4. Full stage audit

| Current stage | Next work | Registered execution class | Existing production path | New tool/model default? | OSS overlay? | Audit result |
|---|---|---|---|---|---|---|
| S00 SLOT_CREATED | HG01 song selection | DATA_ORCHESTRATION | Core Benchmark Data Center -> repeat/value candidate set -> direct creator MV delivery | NO | NO | KEEP; HG01 already restored to original R3 strategy |
| S01 SONG_LOCKED | exact BGM/HG02 | EVIDENCE_ORCHESTRATION | Douyin-first asset identity -> listening variant -> HG02 | NO slot-specific workflow | NO | KEEP; use prior validated resolver/fingerprint paths before adding implementation |
| S02 BGM_LOCKED | Audio Timeline | CANONICAL_TOOLCHAIN | `tools/mv_audio_timeline/*` + package template + locked alignment runtime | NO; doctor/cache first | NO | **ROOT FAILURE FOUND; canonical executor existed but was not routed first** |
| S03 AUDIO_TIMELINE_LOCKED | Natural Beat | CREATIVE_SYNTHESIS | locked line/music-event truth -> Natural Beat | NO | NO | KEEP; no second lyric clock/model |
| S04 NATURAL_BEAT_LOCKED | Director Plan | CREATIVE_SYNTHESIS | R3 Workflow/Golden/Editing/Camera knowledge | NO | YES | Main OSS test entry: Director Thesis / visual engine / audiovisual relation / camera/montage |
| S05 DIRECTOR_PLAN_LOCKED | First Frames/HG03 | CAPABILITY_HANDOFF | existing image-generation capability + R3 K0 QA | NO backend install | YES | OSS may improve drift/performability reasoning; HG03 unchanged |
| S06 HG03 FIRST_FRAMES_LOCKED | Dynamic prompts | CREATIVE_SYNTHESIS | accepted K0 -> R3 bounded I2V prompt grammar | NO | YES | OSS camera/montage/stop-condition overlay allowed |
| S07 DYNAMIC_PROMPT_SET_READY | Generate + source QA | CAPABILITY_HANDOFF | existing Seedance/Doubao path -> RAW SOURCE -> QA map | NO new generator backend | YES reasoning only | H3/RunningHub execution remains out of scope |
| S08 DYNAMIC_SOURCE_QA_LOCKED | normalization/WEB rough-cut | DETERMINISTIC_MEDIA_TRANSFORM | source normalization rule + WEB rough-cut rule + existing media tooling | NO new library | NO | KEEP; check ffmpeg/capability first |
| S09 SOURCE_NORMALIZATION_READY | editor audio revalidation | TECHNICAL_VALIDATION | reuse Audio Timeline final gate against current audio | NO | NO | KEEP; never realign here |
| S10 EDITOR_AUDIO_GATE_PASS | Edit Map | CREATIVE_SYNTHESIS | editing rule + three clocks + normalized sources | NO | YES | OSS `WHY CUT HERE` can be evaluated here |
| S11 EDIT_MAP_LOCKED | Preview + HG04 | MEDIA TRANSFORM + HUMAN GATE | existing render capability + machine QA + HG04 | NO new edit engine | YES quality evaluation | Renderer is not the experiment variable |
| S12 HG04 PICTURE_EDIT_PASS | subtitles | DETERMINISTIC_MEDIA_TRANSFORM | locked R2 subtitle baseline + canonical SRT + geometry QA | NO model/style loop | NO | KEEP; implementation bug local only |
| S13 SUBTITLE QA PASS | final render/tech QA | TECHNICAL_VALIDATION | existing render/ffprobe/ffmpeg capability | NO AI model | NO | KEEP |
| S14 FINAL TECH QA PASS | HG05 | HUMAN_GATE | Runtime `RECORD_HUMAN_GATE` -> separate `ADVANCE` | NO | NO | KEEP |
| S15 HG05 PASS | release package | CREATIVE_SYNTHESIS | `PUBLISH_SYSTEM.md` | NO | NO | KEEP |
| S16 RELEASE PACKAGE READY | publish sync | TRANSACTIONAL_PUBLISH | `mv_runtime_publish.py` / Bridge `PUBLISH_SYNC` | NO | NO | Strong canonical executor already exists; do not manually edit Tracker/state |
| S17 PUBLISHED DATA ACTIVE | metrics/review | DATA_REVIEW | observed data only, no invented checkpoint | NO | NO | KEEP |
| S18 REVIEWED | terminal | DATA_REVIEW | preserve evidence / next slot | NO | NO | KEEP |

## 5. Dependency audit

### Persistent/locked production dependency

Audio alignment is not a per-song experimental model choice. The repository already pins:

- Xingyu Lyrics Aligner version/commit;
- WhisperX version;
- Chinese CTC model identity/revision;
- secondary aligner identity;
- regression thresholds.

Correct behavior:

`doctor -> reuse cache/preheated environment -> BLOCK if missing -> explicit controlled environment setup only when approved`.

Incorrect behavior:

`new song -> fresh runner -> discover model -> download model -> create one-off helper`.

### Media tools

FFmpeg/ffprobe are system capabilities for deterministic media work. Stages must check availability before implementing a replacement library.

### Creative/external generation

First-frame and dynamic generation are capability handoffs. Their lack of a repo-local Python script is intentional and must not be interpreted as permission to build a new image/video backend.

## 6. Runtime purity audit

`r3-mv-runtime-web-bridge.yml` must remain a transport for Runtime commands only.

The D02-B one-off Audio Timeline builder being attached to the active bridge was a violation of that separation. It is removed as part of this remediation.

Future stage experiments must not be hosted inside the authoritative state bridge.

## 7. New-tool admission rule

Before creating any helper/workflow/adapter, the executor-first checklist must prove:

1. current stage executor registry read;
2. existing tool/recipe/capability checked;
3. prior PASS sample/workflow checked;
4. dependency doctor/cache checked;
5. concrete implementation gap documented;
6. experiment scope allows the change;
7. new implementation is isolated outside core until promotion;
8. Runtime correctness/Gates remain unchanged.

If any item is false: **do not create the tool**.

## 8. D02-B remediation boundary

Authoritative state stays:

`S02_HG02_BGM_LOCKED / BGM_LOCKED`.

The one-off builder created partial files under `03_AUDIO_TIMELINE`, but did not produce the canonical final authority pair:

- valid sealed `alignment_qa_report.md`;
- `package_manifest.json` written by the registered Final Gate with `AUDIO_TIMELINE_PACKAGE_LOCKED=true`.

Therefore those files are **NOT S03 truth** and must not be reused merely because they look complete.

Their Git history remains durable evidence at the pre-cleanup branch history around commit `34f5229304b0d1f0e6f9a35adade78b6203e459c`.

Canonical D02-B S03 will be rebuilt only through the registered Audio Timeline executor after this audit passes.

## 9. One-off artifacts classified for cleanup

Core pollution to remove from current tree:

- `04_HARNESS/tools/d02b_audio_timeline_build.sh`
- `04_HARNESS/tools/d02b_hg02_audio_probe.sh`
- `.github/workflows/d02b-bgm-asset-probe.yml`
- non-authoritative partial files under `D02-B/03_AUDIO_TIMELINE/`

Immutable Runtime request/response history is NOT deleted.
Experiment request sentinels may remain as audit history but are not executors.

## 10. Promotion candidate

Finding: `EXECUTOR_DISCOVERY_GAP`

Candidate promotion:

`PROMOTE_RUNTIME` after regression evidence proves:
- every S00-S18 stage resolves to a registered executor class;
- all declared canonical paths exist;
- S02 resolves to the canonical Audio Timeline toolchain;
- missing dependency produces BLOCK, not automatic installation;
- Runtime Bridge remains stage-agnostic;
- external OSS overlays are accepted only on allowlisted stages.

This is independent of whether the creative `mvmaker-h3-skills` experiment eventually improves visual quality.
