# Rules｜MV Stage Entry Checklist v1.1

> Status: `ACTIVE / HARD / HG01 DELIVERY HARDENED`
> Role: 在关键 Stage 开始前执行机器前置条件检查，防止“规则已经存在但执行时被跳过”。
> Principle: **Known gate must be machine-enforced before downstream work.**

---

## 1. General contract｜HARD

每个关键 Stage 在执行前必须生成/记录 `ENTRY_CHECK = PASS`。

任一 required prerequisite 缺失：
- 不得“先做一版看看”；
- 不得把技术缺口交给下一个 Human Gate 发现；
- 只能回到最近缺失的 Stage / Gate 补齐。

`Human Gate PASS` 不能替代机器技术 Gate。

---

## 2. Stage 1｜HG01 Song Aesthetic Gate entry

Required before asking the user to choose a song:
- `SONG_CANDIDATE_SET` exists as machine preflight;
- `SONG_CANDIDATE_SET.status = HG01_EVIDENCE_DELIVERY_PASS`;
- a persisted human-facing `HG01_CANDIDATE_EVIDENCE_PACK` exists and its path is recorded in `evidence_pack_path`;
- every formal candidate has at least 2 recent direct Douyin works from at least 2 independent accounts;
- every evidence item reports account / publish date / duration / evidence tier;
- core benchmark coverage is explicitly `CONFIRMED / PARTIAL / UNCONFIRMED`;
- external audio/search corroboration is not substituted for direct Douyin work evidence;
- every direct URL has been landing-work verified: the URL target itself is the cited work, not an older work/profile-like page that merely lists a newer relevant post;
- user handoff mode is `DIRECT_WORKS_FIRST`.

Block if any of the following is true:
- candidate set is only `HG01_PREFLIGHT_PREPARED` / `EVIDENCE_REPACK_REQUIRED`;
- the assistant can only provide song names, rankings or machine recommendation;
- any required evidence URL was inferred from an author page/recent-work listing rather than resolved to the concrete work;
- machine recommendation is being used as a substitute for first-ear user judgement.

Failure action:
`REPACK / REVERIFY DIRECT DOUYIN EVIDENCE -> SET HG01_EVIDENCE_DELIVERY_PASS -> THEN PRESENT HG01`.

Do not create `HG01_SELECTION_RECEIPT` before this entry check can pass.

---

## 3. Stage 5｜First Frames entry

Required:
- `BGM_LOCKED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- `DIRECTOR_BEAT_MAP` exists
- `DIRECTOR_PLAN_LOCKED` exists
- each production segment has a lyric/semantic role and dominant visual event

JIT:
- `rules/mv_first_frame_qa.md`
- `rules/ai_video.md`

Block if:
- Director only describes a functional action but cannot state the standalone beauty / visual memory point;
- two or more adjacent first-frame plans are effectively the same scale/composition/action grammar without explicit reason.

---

## 4. Stage 6｜Dynamic Prompt / I2V entry

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

---

## 5. Stage 8B｜Picture Edit entry｜WEB HARD

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

---

## 6. Stage 9｜Subtitle entry

Required:
- `EDIT_MAP_LOCKED = YES`
- `EDIT_PREVIEW_QA_PASS = YES` / HG04 PASS
- `AUDIO_TIMELINE_PACKAGE_LOCKED = YES`
- canonical SRT / line timeline available
- picture timing no longer being changed

Block if subtitle timing is being derived from picture cuts or a new free ASR clock.

---

## 7. Stage 10｜Final QA entry

Required:
- `EDIT_PREVIEW_QA_PASS = YES`
- `WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES` on WEB
- `SUBTITLE_IMPLEMENTATION_QA_PASS = YES`
- locked BGM identity still matches Stage 2/2A
- source audio leakage check prepared

Final render cannot be submitted to HG05 until all technical checks pass.

---

## 8. Close / Publish handoff

Production close requires:
- HG05 PASS
- `FINAL_TECH_QA_PASS = YES`
- final identity/hash saved
- publish package generated when the 30D/60 system is active

Actual publication is a separate real-world state transition. After the user confirms the post is live, execute `POST_PUBLISH_SYNC` rather than leaving the durable project at `READY_TO_PUBLISH`.

`POST_PUBLISH_SYNC` updates at minimum:
1. per-slot `CURRENT_STATE` -> `PUBLISHED / DATA_COLLECTION_ACTIVE`;
2. `MV_30D_60_TRACKER.csv` -> `PUBLISHED` and known timestamp/notes;
3. program/root live-data state if it tracks the same slot.

If the exact timestamp is not known, store `timestamp_pending_backfill`; do not invent a clock time.

---

## 9. Failure policy

Checklist failure is not a new Human Gate.

Use:
`PATCH THE MISSING TECHNICAL PREREQUISITE -> RE-RUN ENTRY CHECK -> CONTINUE`.

Do not cascade into already-passed aesthetic Gates unless the patch materially changes what the user approved.
