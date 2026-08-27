# Rules｜MV Stage Entry Checklist v1.3

> Status: `ACTIVE / HARD / EXECUTOR-FIRST + HG01 CORE DATABASE RESTORED`
> Role: 在关键 Stage 开始前执行机器前置条件检查，防止“规则已经存在但执行时被跳过”以及“已有执行器未检查就重新造实现”。
> Principle: **Known gate and known executor must be resolved before downstream work.**

---

## 1. General contract｜HARD

每个 Stage 在真正开始执行前必须先完成两层检查：

### A. Evidence entry check
- 当前 required upstream artifacts / Gate 必须满足；
- 任一 prerequisite 缺失，不得“先做一版看看”；
- Human Gate PASS 不能替代机器技术 Gate。

### B. Executor entry check｜NEW HARD
- 读取 `04_HARNESS/runtime/mv_stage_executor_registry.json`；
- 当前 `CURRENT_STATE.current_stage` 必须存在唯一 executor entry；
- 读取 entry 声明的 canonical Rules / Templates / Tools / prior PASS sample；
- 如果声明了 canonical toolchain，必须先复用该 toolchain；
- 如果 execution class 是 `CREATIVE_SYNTHESIS`，不得因为“没有脚本”而创建模型/工具；
- 如果 execution class 是 `CAPABILITY_HANDOFF`，必须使用已有产品/生成能力边界，不得默认开发新 backend；
- 如果存在依赖，先 doctor/check/cache；缺失时按 executor policy BLOCK 或进行明确允许的独立 environment setup；
- Rule 中出现的外部实现名称，只是 reference，除非 executor registry 明确把它锁为当前生产依赖，否则不得自动安装。

创建任何新 helper / workflow / model route 前必须满足 `rules/mv_executor_first.md` 的 New-tool admission gate。

每个关键 Stage 在执行前必须生成/记录 `ENTRY_CHECK = PASS`（可以由 Runtime preflight/CI/明确的执行检查体现）。

Failure action：
`PATCH NEAREST MISSING PREREQUISITE / EXECUTOR ENVIRONMENT -> RE-RUN ENTRY CHECK -> CONTINUE`。

---

## 2. Stage 1｜HG01 Song Aesthetic Gate entry

Required before asking the user to choose a song:
- 当前 Core Benchmark Data Center / song repeat data 可用；
- `SONG_CANDIDATE_SET` 已从核心 Benchmark 数据库构建，而不是从一次性全网搜索临时拼装；
- candidate set 明确 `source_mode = CORE_BENCHMARK_DATABASE`；
- 每个候选可以追溯到数据库中的对应账号 / work；
- human-facing `HG01_CANDIDATE_EVIDENCE_PACK` 已持久化；
- 用户交付内容保持简单：歌名 + 极短入选理由 + 对应博主的对应 Douyin MV 直链；
- 所有真正交付给用户的 direct URL 已验证 landing work 本身就是被引用的作品；
- `delivery_strategy = CORE_CREATOR_MV_DIRECT`。

Runtime compatibility: legacy validator may still require `user_gate_delivery_mode = DIRECT_WORKS_FIRST`; treat that as a compatibility marker only, not discovery/delivery business logic.

Default discovery rule:

`CORE BENCHMARK ACCOUNTS -> DATA CENTER -> SONG_FAMILY RANKING -> HG01`

Public Web / external Radar may only be used to:
- locate a concrete work that belongs to an already tracked/selected account or song;
- discover a genuinely useful supplemental benchmark account;
- corroborate freshness when needed.

They must not replace the core database as the default candidate source.

Block if any of the following is true:
- assistant is doing broad web-wide song search as the default HG01 discovery method;
- formal candidates are primarily chosen because their public-search metadata is easier to retrieve;
- candidate links point to an older landing work/profile-like page whose listing merely contains the desired new MV;
- assistant asks the user to evaluate evidence taxonomy instead of simply watching/listening to the candidate MVs;
- machine recommendation is being used as a substitute for user first-ear judgement.

Failure action:
`REFRESH / READ CORE DATA CENTER -> REBUILD CANDIDATES -> VERIFY DELIVERY LINKS -> PRESENT SIMPLE HG01`.

Do not create `HG01_SELECTION_RECEIPT` before this entry check can pass.

---

## 3. Stage 2A｜Audio Timeline entry｜HARD

Required after HG02 and before Natural Beat:
- `BGM_LOCKED = YES`;
- resolve executor `CANONICAL_AUDIO_TIMELINE_TOOLCHAIN` from executor registry;
- load `templates/mv_audio_timeline_package_contract.md` and `tools/mv_audio_timeline/*` required by the executor;
- run alignment environment `doctor` before any installation;
- reuse the pinned/preheated alignment environment when available;
- only `final_gate.py validate ... --write-manifest` may create the locked package manifest.

Block if:
- Agent creates a song/slot-specific aligner before checking canonical tools;
- Agent downloads a production model simply because the Rule mentions a reference implementation;
- engine/model is missing and Agent silently substitutes another model;
- any diagnostic/waveform estimate is promoted to exact timing;
- partial S03 files exist but Final Gate has not produced a valid locked manifest.

Failure action:
`CANONICAL TOOLCHAIN DOCTOR -> BLOCK OR CONTROLLED ENV SETUP -> REBUILD PACKAGE -> FINAL GATE`.

---

## 4. Stage 5｜First Frames entry

Required:
- `BGM_LOCKED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DIRECTOR_BEAT_MAP` exists
- `DIRECTOR_PLAN_LOCKED` exists
- each production segment has a lyric/semantic role and dominant visual event

JIT:
- `rules/mv_first_frame_qa.md`
- `rules/ai_video.md`
- `templates/ai_first_frame_prompt.md`

Executor class is `CAPABILITY_HANDOFF`: use existing image-generation capability + machine QA. Lack of a repo-local image SDK is not an implementation gap.

Block if:
- Director only describes a functional action but cannot state the standalone beauty / visual memory point;
- two or more adjacent first-frame plans are effectively the same scale/composition/action grammar without explicit reason;
- Agent starts building a new image backend instead of using the registered capability boundary.

---

## 5. Stage 6｜Dynamic Prompt / I2V entry

Required:
- `FIRST_FRAME_SET_LOCKED = YES` / HG03 PASS
- every dynamic source has an accepted actual first-frame asset / image reference
- actual accepted first frame has been inspected as K0 truth
- character closure / object closure resolved
- dynamic role and expected edit role resolved

HARD authority:
`ACCEPTED ACTUAL FIRST FRAME (K0) > older Director prose / abandoned first-frame prompt`.

If accepted pixels contradict an older text plan, rewrite the dynamic prompt around the accepted image. Never ask the model to reconstruct the obsolete plan.

Block if a character-containing prompt does not include the required portrait-safe prefix or omits the full prompt-control skeleton in `rules/ai_video.md`.

Dynamic generation executor is an existing capability handoff. Do not create a new generator backend unless generator integration itself is an explicitly approved experiment.

---

## 6. Stage 8B｜Picture Edit entry｜WEB HARD

Required:
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DYNAMIC_SOURCE_QA_LOCKED_FOR_EDIT = YES`
- `VISUAL_SOURCE_MAP` exists
- `SHOT_LIBRARY_READY = YES` when normalization is required
- `EDITOR_AUDIO_GATE_PASS = YES`
- **WEB only: `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`**
- clean WEB proxies have source audio physically removed

Formal HG04 preview MUST NOT render from raw WEB source with visible generator/platform corner marks.

If a rhythm-only diagnostic preview is intentionally made earlier, label it `DIAGNOSTIC_ONLY / NOT_HG04` and do not submit it as Human Gate evidence.

Media transform dependency preflight: check existing ffmpeg/ffprobe/render capability first; missing tool is not permission to introduce a new media framework ad hoc.

---

## 7. Stage 9｜Subtitle entry

Required:
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES` / HG04 PASS
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- canonical SRT / line timeline available
- picture timing no longer being changed

Block if subtitle timing is being derived from picture cuts or a new free ASR clock.

Subtitle executor inherits the locked R2 baseline. Lack of a style exploration step is intentional; do not create a new subtitle model/style workflow unless user explicitly reopens style.

---

## 8. Stage 10｜Final QA entry

Required:
- `EDIT_PREVIEW_QA_PASS = YES`
- `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES` on WEB
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
- locked BGM identity still matches Stage 2/2A
- source audio leakage check prepared

Final render cannot be submitted to HG05 until all technical checks pass.
No new AI model is part of Final Tech QA.

---

## 9. Close / Publish handoff

Production close requires:
- HG05 PASS
- `FINAL_TECH_QA_PASS = YES`
- final identity/hash saved
- publish package generated when the 30D/60 system is active

Actual publication is a separate real-world state transition. After the user confirms the post is live, execute registered executor `TRANSACTIONAL_PUBLISH_SYNC` through `mv_runtime_publish.py` / Bridge `PUBLISH_SYNC` rather than manually editing Tracker/state.

`POST_PUBLISH_SYNC` updates at minimum:
1. per-slot `CURRENT_STATE` -> `PUBLISHED / DATA_COLLECTION_ACTIVE`;
2. `MV_30D_60_TRACKER.csv` -> `PUBLISHED` and known timestamp/notes;
3. program/root live-data state if it tracks the same slot.

If the exact timestamp is not known, store `timestamp_pending_backfill`; do not invent a clock time.

---

## 10. Failure policy

Checklist failure is not a new Human Gate.

Use:
`PATCH THE MISSING TECHNICAL PREREQUISITE / EXECUTOR ENVIRONMENT -> RE-RUN ENTRY CHECK -> CONTINUE`.

Do not cascade into already-passed aesthetic Gates unless the patch materially changes what the user approved.
