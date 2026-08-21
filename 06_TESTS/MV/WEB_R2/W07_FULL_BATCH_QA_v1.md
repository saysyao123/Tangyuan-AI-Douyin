# WEB R2｜W07 Full Batch QA v1

> Source: user-returned Seedance 2 mini raw MP4 set `2S1`–`2S9`, each ~5.04s / 720×1280 / 24fps.
> Status: `VISUAL_BATCH_PASS_WITH_TRIM / NO FULL-BATCH REGEN REQUIRED`.

## 1. Batch-level conclusion

The nine generated clips now form a genuinely mixed directing structure rather than one repeated template:

- S1: multi-shot
- S2: one-take Arc / orbit
- S3: 2-shot close-up → medium
- S4: 3-shot dance / lateral movement
- S5: one-take spatial breathing shot
- S6: 3-shot person → bird → person
- S7: multi-shot motion peak
- S8: one-take rooftop / sky reset
- S9: one-take cloud release

This structure diversity is a major improvement over the rejected `one primary camera per 5s clip` interpretation.

No clip currently justifies full-set regeneration. The correct next stage is **material-pool editing + selective trim**, with only S7 kept on a watchlist for possible isolated regeneration if its usable window proves insufficient during final edit.

## 2. QA status vocabulary

- `PASS_FULL`: visually safe enough to enter edit as a full source clip.
- `SOURCE_USABLE / TRIM_REQUIRED`: good footage exists; local repetition/artifact should be removed in edit rather than regenerating the whole clip.
- `REGEN_WATCH`: do not regenerate yet; only regenerate if edit cannot obtain enough clean usable duration.

## 3. Per-clip review

### S1 — `SOURCE_USABLE / TRIM_REQUIRED`

Strengths:
- successful recovery from original fixed one-take failure;
- clear scale/angle progression: monumental wide → low-angle person → eye close-up → canopy/sky;
- camera language is now visible and useful;
- opening and final upward tree shot are strong edit anchors.

Issues:
- around the middle, two adjacent low-angle character shots are too similar in shot size / angle / upward performance;
- actual visual transition activity is concentrated around ~2.04s / 2.42s / 3.13s / 3.88s;
- the two low-angle middle fragments should not both survive the final cut.

Edit policy:
- choose the stronger of the two similar middle low-angle fragments;
- preserve wide opening + one low-angle character fragment + eye detail + canopy resolve;
- no full regeneration.

### S2 — `PASS_FULL / POSITIVE ONE-TAKE SAMPLE`

Strengths:
- single continuous Arc/orbit remains one of the best camera results in the batch;
- foreground trunk / character / curved wall create persistent parallax;
- simple reach/look-up performance keeps generation load controlled;
- endpoint lands on a more flattering three-quarter relation;
- proves one-take is strong when it has sustained visual progression.

Issues:
- no major structural issue found.

Policy:
- retain as the current positive one-take benchmark;
- do not add cuts merely for density.

### S3 — `PASS_FULL`

Strengths:
- close-up emotional anchor is strong;
- veil, eyes, hair and backlight are stable;
- one clear cut around ~1.75s creates useful contrast from intimate detail to medium portrait;
- this clip adds a needed emotional/portrait layer to the batch.

Issues:
- first section is intentionally restrained; do not overextend it if the BGM needs more forward motion.

Policy:
- usable full; final edit may shorten the first close-up slightly.

### S4 — `PASS_FULL / STRONG DYNAMIC SAMPLE`

Strengths:
- one of the best multi-shot results;
- full-body movement is readable without becoming chaotic dance choreography;
- first section uses tree + character + fabric well;
- middle wide shot creates real scale and body movement;
- final closer portrait gives a clean emotional landing;
- adjacent shots differ clearly in scale and camera relationship.

Issues:
- trailing fabric is active but remains visually acceptable in current review.

Policy:
- strong candidate for near-full use;
- no regeneration.

### S5 — `PASS_FULL / BREATHING SHOT`

Strengths:
- effective monumental scale reset;
- one-take remains readable because character/environment relationship gradually opens;
- sunlight shaft + giant tree + small person gives premium visual pause.

Issues:
- visual family overlaps with S1 opening (giant tree + light shaft + small person).

Policy:
- keep as a shorter breathing insert rather than using all 5s if S1 already uses a long opening;
- repetition should be solved in edit, not generation.

### S6 — `PASS_FULL / STRONG LYRIC-HIT SAMPLE`

Strengths:
- strongest semantic/lyric match in the batch;
- actual 3-stage visual grammar is clear: person notices → bird detail → relation returns;
- cuts around ~1.42s and ~3.71s are easy to read;
- bird insert is stable, attractive and directly supports the lyric;
- face/veil continuity remains good when returning to character.

Issues:
- bird hold can feel slightly long depending on final music timing.

Policy:
- keep full source; trim bird hold by a few tenths if needed.

### S7 — `SOURCE_USABLE / TRIM_REQUIRED / REGEN_WATCH`

Strengths:
- correctly functions as the batch motion peak;
- low-angle body scale, hand, bird/sky direction and stronger camera movement create the intended energy increase;
- early section (~0–2.7s) is strong;
- final canopy/sky section provides a clean escape/resolve.

Issues:
- mid/late section lets pale fabric become extremely large and visually dominant;
- around roughly ~2.8–4.0s the fabric can read as a loop / detached ribbon rather than a clearly connected veil/garment element;
- this is the batch's highest topology-risk moment.

Edit policy:
- first choice: use clean early peak + clean final canopy resolve, and remove the most ambiguous fabric loop frames;
- only regenerate S7 if final BGM timing requires more clean peak duration than the source can provide;
- do not regenerate now.

### S8 — `PASS_FULL / SHORTEN IN SEQUENCE`

Strengths:
- quiet high-space one-take provides a useful reset after the motion peak;
- human scale is tiny, geometry and negative sky dominate;
- simple walking/stop behavior is stable;
- camera restraint is appropriate here.

Issues:
- S8 and S9 share very similar rooftop + giant sky + tiny person language;
- using both at full 5s back-to-back would make the ending feel repetitive.

Policy:
- shorten S8 significantly in final edit and let it function as spatial reset;
- preserve S9 for the longer release.

### S9 — `PASS_FULL / FINAL RELEASE`

Strengths:
- strong final-release image;
- cloud, sky, curved architecture and tiny person are calm and legible;
- minimal motion is appropriate after S7 peak;
- good tail-hold behavior.

Issues:
- visual family overlaps with S8.

Policy:
- prioritize S9 as the longer final hold;
- shorten S8 rather than S9.

## 4. Whole-set repetition findings

### A. S1 middle repetition
Adjacent low-angle character shots are too similar. Solve by selecting only one.

### B. S1 vs S5
Both use giant tree + light shaft + small character. They are not duplicates, but should not both occupy long durations.

### C. S8 vs S9
This is the most important whole-set repetition issue. Both are rooftop/curved concrete + giant sky + tiny person. Final edit should use S8 as a shorter bridge and S9 as the long release.

## 5. Director structure result

Actual mixed structure demonstrates the current Director Shot-Structure Selector is directionally correct:

- one-take can work: S2, S5, S8, S9;
- 2-shot can work: S3;
- 3-shot can work: S4, S6;
- denser multi-shot can work: S1, S7;

The learning is NOT to promote a fixed shot count. The stronger rule remains:

`lyric task → first-frame performance potential → choose shot count → per-shot Camera Contract → motion-load check → edit-value check`.

## 6. Audio QA — HARD FAIL AT SOURCE LEVEL, NOT VISUAL REGEN

All nine returned MP4 files contain an AAC audio stream.

This means every clip is technically `SOURCE_AUDIO_PRESENT` and must be treated as audio-policy failure at source level, even if the visual is accepted.

S1 has already been audibly identified by the user as containing unintended music-like background. Batch analysis also shows several clips have continuous tonal audio characteristics inconsistent with a pure silent source workflow.

Hard workflow consequence:

1. **Do not use any Seedance source audio in final edit.**
2. On ingest, strip/detach the source audio track, not merely turn timeline volume down.
3. The W02 locked song master is the only music truth for timing / rhythm / subtitles.
4. AI source audio must never influence beat detection or edit decisions.
5. Prompt-level rule remains: forbid BGM / music / melody / beat / humming / singing / dialogue / narration / voices; only minimal physically motivated ambience may be requested, but final pipeline still removes the track.

## 7. Watermark QA

All returned clips visibly contain a lower-right platform mark (`豆包AI生成`).

This is a post-production cleanup requirement and does not invalidate the visual generation.

Before final delivery, remove/cover/inpaint this consistently across all retained source segments; do not leave mixed watermark states between clips.

## 8. Recommended edit priorities

Keep / favor:
- S2: orbit one-take
- S4: dynamic body/multi-shot
- S6: bird discovery
- S7: clean peak fragments
- S9: final release

Trim selectively:
- S1: one of two similar middle low-angle fragments
- S5: shorten if S1 opening is long
- S6: optional shorter bird hold
- S7: remove ambiguous large-fabric loop region
- S8: shorten to avoid S9 repetition

## 9. Current stage decision

`W07 = VISUAL QA PASS WITH TRIM`.

No full-batch regeneration.

Next production stage should be W08 editing preparation:
- strip all source audio;
- map clean usable windows;
- place clips against locked 37.120s BGM;
- trim repetition and topology-risk frames;
- remove platform watermark;
- only then decide if S7 alone needs a surgical regeneration.
