# 《爱让人脑袋空空》｜Generation QA Round 01

> Status: `REAL_GENERATION_EVIDENCE / VISUAL_PROMISING / DELIVERY_BLOCKED`
> Source clips: user-uploaded Dola / Seedance 2.5 outputs
> Mapping: A=`下载 (3).mp4` (~12s), B=`下载 (2).mp4` (~10s)
> Upstream Prompt: `10_LOVE_EMPTY_HEAD_MULTI_SHOT_PROMPTS_v1.md`

## 1. Technical probe

### Segment A
- Container duration: `12.096009s`
- Video: `HEVC / 720x1280 / 24fps / ~2.11 Mb/s`
- Audio: `AAC / 44.1kHz / stereo / ~128.6 kb/s`
- Overall bitrate: `~2.28 Mb/s`

### Segment B
- Container duration: `10.080000s`
- Video: `HEVC / 720x1280 / 24fps / ~1.47 Mb/s`
- Audio: `AAC / 44.1kHz / stereo / ~128.9 kb/s`
- Overall bitrate: `~1.65 Mb/s`

### Important implication
The actual generated/downloaded videos are `720x1280 / 24fps`, not 4K. A high-detail/4K-oriented K0 can improve source appearance and asset definition, but this current Dola delivery path downscales the final video to 720p.

---

## 2. Visual execution summary

Round 01 is visually successful enough to continue the route. The strongest result is that Seedance 2.5 did not collapse the multi-shot prompt into one continuous shot. It produced multiple shot-scale changes, close-ups, inserts, wides, tracking/running motion, and environment-led ending beats while retaining the same core character/world.

### Segment A observed execution
Approximate visual structure from frame inspection:

1. `~0.0–1.1s` full / establishing from K0 world;
2. `~1.1–3.6s` character close / medium-close emotional material;
3. `~3.6–4.8s` medium/full + hand insert/detail cluster;
4. `~4.9–6.5s` large-space / extreme-wide section;
5. `~6.6–8.3s` return to character, chest/eye/detail emotional impacts;
6. `~8.3–12.1s` leg/foot emphasis into readable forward running/tracking.

Prominent frame-change peaks were detected around `1.08`, `3.63–4.42`, `4.88`, `6.58`, `7.96–8.33s`.

**Assessment:** the intended sequence `emotion → hand/body detail → space burst → emotional impact → kinetic finish` was followed surprisingly well. The model also created useful insert shots beyond the coarse principal-shot list.

**Motion:** the final locomotion shows real leg cycling and grounded foot positions. No obvious whole-body ground sliding is visible in the sampled running sequence. This is a meaningful improvement relative to the previous sliding/drifting failure mode.

**Issue:** the post-handle does not really decelerate/settle; the run continues deep into the tail. This means the generated timecode should be treated as a soft choreography guide, not a frame-accurate edit contract. The handle strategy is therefore useful: final trim can shift within the redundant material to choose a clean footfall/action punctuation.

### Segment B observed execution
Approximate visual structure:

1. `~0.0–1.4s` re-establishing full/medium-wide;
2. `~1.4–2.6s` new medium/profile restart;
3. `~2.6–4.1s` face close-up with rising tears;
4. `~4.1–5.2s` eye / hand / wind-spirit detail cluster;
5. `~5.2–6.3s` wider hand-release/environment transition;
6. `~6.3–10.1s` extreme-wide environment-led ending.

Prominent changes were detected around `1.42`, `2.63`, `3.63`, a dense `4.1–5.2s` detail cluster, and `~6.25s` into the wide ending.

**Assessment:** B follows the semantic arc very well: restart → tears/emotional peak → reaching/releasing → disappearance/wide ending. The detail cluster is more aggressive than planned but is visually effective and clearly serves `泪眼汹涌 / 承诺被风吹得`.

**Consistency:** the red/coral cape, dark outfit, short-haired heroine and highland-lake world remain recognizable. The face becomes somewhat younger/rounder in the tightest close-ups, and the wind-spirit shifts between a creature-like form and a more abstract luminous trail. This is acceptable for the current test, but it is a real asset-consistency weakness if the wind-spirit is intended as a fixed companion character.

---

## 3. Exact timing lesson

The prompt's explicit timestamps were **not executed frame-accurately**. They did, however, strongly influence order, density and relative placement of visual events.

Therefore current workflow should treat generated prompt timecodes as:

`SOFT TEMPORAL CHOREOGRAPHY`

not:

`FINAL EDIT TIMECODE`.

Final lyric/beat alignment must still happen in post against the locked BGM timeline. This validates the decision to generate redundant 5–15s material with handles instead of forcing exact final-duration generation.

---

## 4. Watermark blocker

Both clips contain a dynamic `Dola AI` watermark that changes position across the video.

This is not a fixed corner logo. Frame inspection shows the mark migrating between edges/corners and, in some close/detail frames, overlapping important image content.

Concrete examples:
- Segment B around `~4.5s`: `Dola AI` overlaps the left side of the heroine's face/cheek region during a close-up.
- Segment B around `~5.0s`: watermark overlaps the wind-spirit / hand-detail region.
- Segment A around the locomotion/detail sequence: watermark appears at different top/bottom edge positions rather than remaining in one crop-safe corner.

### Consequence
- fixed crop is not viable;
- one static mask is not viable;
- frame-by-frame/inpaint removal would touch moving face/hand/environment detail and risks shimmer/artifacts, especially at only 720p.

**Preferred resolution:** obtain an official/original clean media source upstream. Do not treat post-removal as the default production path.

Watermark status: `BLOCKER_FOR_FINAL_DELIVERY`.

---

## 5. Audio / unwanted BGM blocker

Both generated files contain stereo AAC audio.

Measured levels:
- A mean volume ~`-18.8 dB`, max ~`-1.7 dB`;
- B mean volume ~`-23.4 dB`, max ~`-5.6 dB`.

Audio energy is nearly continuous across the clips (A ~99.8% and B ~94.3% of analysis frames above a -45 dB RMS threshold). Harmonic energy dominates percussive energy by roughly 10–12x, consistent with the user's observation that an unwanted musical/BGM bed was generated rather than only sparse environmental SFX.

### New Audio Contract｜HARD FOR NEXT ITERATION
Allowed audio only:
- wind;
- grass/cloth rustle;
- footsteps;
- distant lake/water ambience;
- subtle wind-spirit whoosh / airy environmental effect.

Explicitly disallow:
- BGM / music / score;
- melody;
- singing / humming;
- dialogue / voice / vocalization;
- rhythmic percussion or beat track.

If any disallowed music/voice remains after generation, **strip the entire generated audio track** for final editing and use the locked project BGM plus separately controlled scene SFX. Do not depend on source separation to rescue the generated track.

Audio status: `NEEDS_SINGLE_VARIABLE_PROMPT_FIX`.

---

## 6. Round-01 QA classification

- Song/Timeline: `PASS / LOCKED`
- Segment redundancy/handles: `PROMISING / VALIDATED_BY_TIMING_DRIFT`
- Multi-shot Director: `VISUAL PASS CANDIDATE`
- K0 asset establishment: `PASS CANDIDATE`
- Dynamic Prompt visual structure: `PASS CANDIDATE`
- Exact generated timestamps: `SOFT ONLY / NOT FRAME-ACCURATE`
- Character consistency: `GOOD WITH MINOR CLOSE-UP DRIFT`
- Locomotion / anti-sliding: `PASS CANDIDATE`
- Watermark: `FINAL DELIVERY BLOCKER`
- Audio: `FAIL FOR CURRENT CONTRACT / ADD NO-MUSIC RULE`
- Final project QA: `NOT PASS YET`

## 7. Next controlled iteration

Do **not** rewrite the successful visual Director/Prompt wholesale.

Next prompt iteration should change only the audio contract first:

`same visual instructions + explicit scene-SFX-only / no-music / no-voice contract`.

In parallel, investigate the upstream Dola delivery path for a legitimate clean/no-watermark original source. Watermark resolution is a delivery-path problem, not a reason to discard the visually successful generation logic.
