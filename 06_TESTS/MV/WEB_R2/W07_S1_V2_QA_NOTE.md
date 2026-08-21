# WEB R2｜W07 S1 v2 QA Note

> 状态：`GENERATED EVIDENCE / SOURCE_USABLE / TRIM_REQUIRED`。

## Input

User-returned S1 v2 raw clip:
- duration: `5.088s`
- video: `720×1280`, `24fps`, H.264
- audio: AAC stereo 44.1kHz

## Visual QA

### Overall judgement

`PASS_AS_SOURCE / NOT_FULL_LENGTH_LOCK`.

Compared with S1 v1, the camera/director level improved substantially:
- clear shot-size and angle changes are actually executed;
- the clip no longer reads as a static fixed-camera one-take;
- extreme-wide scale, low-angle character relation, eye close-up and canopy release are all usable material;
- the ending Tilt Up / canopy-sky release is readable and lyric-relevant.

This clip should enter the source-material pool rather than be rejected.

### Detected cut / transition points

Approximate visual discontinuities:
- `2.04s`
- `2.42s`
- `3.13s`
- `3.88s`

### Repetition issue

The middle area around `2.04–3.12s` contains two visually similar low-angle character shots. The second is partly differentiated by foreground tree/occlusion, but the subject scale, angle and action state are too similar, so the sequence reads as a repeated beat.

Current handling:
- **do not regenerate solely for this**;
- during W08, keep only the better portion or shorten both aggressively;
- generated 5s raw clips are **source coverage**, not mandatory 5s continuous final-use blocks.

New editing insight:

`Generated clip QA ≠ must accept/reject the whole 5 seconds.`

A visually strong clip can be `SOURCE_USABLE / TRIM_REQUIRED`; final BGM and edit rhythm decide which internal shots survive.

## Audio QA

The returned clip contains a clearly non-ambient music-like soundtrack.

Technical observation after extracting the 5.1s audio:
- integrated loudness approx `-18.7 LUFS`;
- harmonic component strongly dominates the waveform; this is inconsistent with a simple wind/leaves-only ambience bed;
- therefore this is treated as model-added BGM / musical audio, not merely environmental sound.

This does **not** invalidate the visual source because the MV pipeline uses the locked external song and strips source audio, but it is a prompt-policy failure and should be prevented upstream.

## Sound-rule correction

For AI MV image-to-video, prompts must not use soft wording such as only `不需要BGM`.

Use explicit hard prohibition:

`声音硬规则：禁止生成任何BGM、配乐、音乐、旋律、节拍、和弦、歌声、哼唱、旁白、对白或人声。只允许与当前画面物理事件直接对应的自然环境声，例如轻风、树叶摩擦、衣料轻响；不得出现任何音乐性声音。最终MV统一删除所有AI源音轨，并以后期锁定BGM为唯一音乐。`

If even this still produces music:
- classify `SOURCE_AUDIO_POLICY_FAIL`;
- keep visually good footage;
- strip source audio in W08;
- never let AI-generated audio determine cut timing or subtitle timing.

## Director implication

S1 v2 proves that multi-shot + per-shot Camera Contract can significantly raise camera energy, but also shows a new risk:
- when two adjacent Shots use similar low-angle subject scale/action, the model may produce a repeated visual beat even if the prompt labels them as different Shots.

Therefore future multi-shot prompts need an **Adjacent Shot Contrast Gate**:
- consecutive shots should differ in at least 2 of: shot size / angle / subject scale / camera direction / focal plane / dominant action / visual subject;
- if not, merge them or delete one before generation.

This gate remains experimental until more generated clips validate it.
