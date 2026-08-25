# 汤圆音乐映像｜30天60条｜D01-B B0 Audio Version Discovery v1

Status: `PASS / HG02_READY`
Slot: `D01-B`
Lane: `S / Stable-Fast`
SONG_FAMILY: `我救自己于人间水火`

## 1. Douyin-native verification

Two independent core Benchmark works were parsed from their real Douyin work URLs, their actual media/direct music assets were downloaded, decoded and compared.

### Aura
- aweme: `7673460363010018611`
- displayed music: `@Aura创作的原声`
- direct music asset id: `7673460389337762610`
- direct asset duration: `15.986938s`
- audio: MP3 / 44.1kHz / stereo / 128kbps

### XIANGJISHI
- aweme: `7673442358406957285`
- displayed music: `@𝑿𝑰𝑨𝑵𝑮𝑱𝑰𝑺𝑯𝑰创作的原声`
- direct music asset id: `7673442361086610233`
- direct asset duration: `15.960813s`
- audio: MP3 / 44.1kHz / stereo / 128kbps

## 2. Acoustic identity result

Pairwise Chromaprint comparison of the actual work audio:
- similarity: `0.995327`
- best shift: `0`
- overlap: `107`

Decision:
`SAME_RECORDING_DIFFERENT_ASSET_IDS = YES`

Interpretation:
The two creators re-uploaded the same underlying short recording as separate Douyin original-sound assets. They are not the same asset ID, but the actual recording is acoustically the same with zero alignment shift.

This meets the BGM discovery rule's high-confidence standard through direct Douyin assets plus independent acoustic corroboration.

## 3. Production reference

Recording family lock:
`DOUYIN_RECORDING_FAMILY / 我救自己于人间水火 / 15.96s TREND-NATIVE`

Known Douyin asset aliases:
- `7673460389337762610` — Aura
- `7673442361086610233` — XIANGJISHI

HG02 reference source:
`DOUYIN_MUSIC_ASSET:7673442361086610233`

Reason:
- direct music asset, not video-derived audio;
- same recording as the independent Aura asset;
- exactly matches the XIANGJISHI core work whose caption explicitly foregrounds the song's self-rescue hook;
- `15.960813s` is naturally aligned with Lane-S short production.

Reference SHA-256:
`ec6c178e30bf6c910ba4080bf1d3db31b708a7b7003430cb506630b21ac08b65`

## 4. HG02 variants

### A｜Trend-native exact
- no timing modification;
- exact `15.960813s` direct Douyin music asset;
- keeps the trend-native ending exactly as used by the source asset.

### B｜Soft-fade candidate
- same source and same beginning;
- no version change;
- only adds a gentle final `~0.8s` fade-out for the user to compare ending comfort;
- no Audio Timeline work begins until the user chooses A/B or requests a boundary adjustment.

## 5. Machine QA completed before HG02

- both core works parsed successfully;
- both direct music files downloaded successfully;
- both decode successfully;
- 44.1kHz stereo confirmed;
- source is direct Douyin music asset, so no source-video dialogue/ambient track leakage is introduced;
- independent work fingerprint agreement confirmed at `0.995327`, shift `0`;
- exact reference hash recorded;
- no generic full-track substitution was used;
- no visual work has begun.

Important ending note:
The raw trend asset remains acoustically active at its final boundary rather than containing a built-in fade. Therefore the machine does **not** claim the raw ending is aesthetically final; HG02 includes a soft-fade comparison candidate, and ending comfort remains the user's intended Gate decision.

## 6. Gate

- `HG01_PASS = YES`
- `SONG_FAMILY_LOCKED = YES`
- `AUDIO_VERSION_HIGH_CONFIDENCE = YES`
- `HG02_READY = YES`
- `BGM_LOCKED = NO`

Next human decision:
Listen to A and B and decide which ending feels correct, or state that the segment boundary itself needs adjustment.

Only after HG02 PASS:
- lock final BGM hash/transform;
- build trusted Audio Timeline Package;
- continue Natural Beat / Director / First-frame stages.
