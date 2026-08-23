# WEB R2｜W02A Strong Route Recovery Note v1

Date: `2026-08-24 Asia/Manila`

Status: `PROGRESS / PACKAGE STILL BLOCKED`

## Purpose

Preserve the new-chat recovery evidence while continuing the mandatory Stage 2A `AUDIO_TIMELINE_PACKAGE` Gate. This note does **not** promote the candidate timeline or mark the Package PASS.

## 1. Exact locked audio recovered and revalidated

The exact WEB R2 locked excerpt was recovered from the user's ChatGPT file library without requiring a re-upload:

- filename: `如果你也刚好抬头看树_WEB_R2_W02_副歌扩展试听_v3.mp3`
- SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- ffprobe container duration: `37.146122s`
- canonical content timeline remains: `37.120s`

The SHA exactly matches `AUDIO_TIMELINE_PACKAGE/audio_identity.json`; therefore future alignment work in this recovered chat can operate on the real locked BGM rather than a substitute/candidate source.

The original master was also recovered:

- filename: `如果你也刚好抬头看树-孙天宇.mp3`
- ffprobe duration: `196.127347s`
- SHA-256 observed in recovered runtime: `ad30cefef4e4a5ffedab81b26b1e38a0b679bf2b32752b6ebd29f5d97f18d7ab`

## 2. Formal-release identity cross-check strengthened

Current public release pages from major services identify the commercial release as the same song/artist and approximately `3:16`, consistent with the recovered original master duration of `196.127347s`.

This strengthens version identity but is not, by itself, line-timing evidence.

## 3. Primary forced-alignment runtime identity confirmed

`04_HARNESS/tools/mv_audio_timeline/alignment_runtime.lock.json` pins:

- primary aligner: `xingyu-lyrics-aligner` `0.7.0`
- aligner Git commit: `ef5ad02a0059ab07f4cc92f608d373447c89b007`
- backend: `WhisperX CTC forced alignment`
- WhisperX: `3.8.6`
- Chinese model: `jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn`
- model reference revision: `d2af85f00e501bb8b8bcedef3b5c51eabb883088`

The xingyu source at the pinned commit confirms that the trusted lyric text is sent to WhisperX CTC alignment directly; it intentionally does not use ASR transcription as lyric truth.

## 4. Current runtime blocker independently reproduced

The current container cannot resolve model-host DNS (`huggingface.co` and related hosts). Direct model retrieval therefore fails before alignment execution.

This confirms the existing `CURRENT_STATE.md` diagnosis: the missing Strong Route result is presently a runtime/model-delivery blocker, not a missing-audio or missing-lyrics blocker.

No model substitution or evidence downgrade was performed.

## 5. Secondary forced-alignment candidate investigated

The installed Torchaudio runtime exposes `torchaudio.pipelines.MMS_FA`, an official multilingual CTC forced-alignment pipeline. Its official model URL is also unreachable from the current container because external DNS is restricted.

Classification for now:

`EXPERIMENTAL_SECONDARY_ROUTE / MODEL_NOT_AVAILABLE / NOT PROMOTED`

It must not replace the pinned production route without regression evidence and an explicit runtime-lock update.

## 6. Same-version timed-lyric fallback investigation

A new fallback candidate was identified: LRCLIB exposes track-signature lookup and can return hundredth-second `syncedLyrics` when a matching record exists. The route remains only a candidate until the exact song/version is retrieved and checked against the locked master.

Existing coarse public whole-second LRC remains supporting evidence only and stays rejected as timing truth.

## 7. Gate state remains unchanged

- `AUDIO_IDENTITY_LOCKED = YES`
- `LYRIC_TEXT_ACTUAL_EXCERPT_CORRECTED = YES`
- `HIGH_CONFIDENCE_LINE_TIMELINE_READY = YES`
- `LYRIC_TIMELINE_LOCKED = NO`
- `MUSIC_EVENT_MAP_VERIFIED = NO`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`
- `EDITOR_AUDIO_GATE_PASS = NO`
- `EDIT_MAP_LOCKED = NO`

## 8. Next valid work

Priority order:

1. obtain a Strong Route raw timing result against the recovered exact locked BGM using the pinned CTC model/runtime when model delivery is possible; or
2. obtain a high-precision same-version synced lyric record with stable provenance and verify it line-by-line against the locked audio;
3. retain raw evidence + provenance;
4. run Ground-truth QA;
5. only after that generate canonical `line_timeline.csv`, `lyrics_exact.srt`, anchors/music events, then pass both machine Gates.

Until then:

`AUDIO_TIMELINE_PACKAGE_BLOCKED`.
