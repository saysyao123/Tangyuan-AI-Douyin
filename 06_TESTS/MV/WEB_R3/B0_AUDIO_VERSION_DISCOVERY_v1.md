# WEB R3｜B0 Audio Version Discovery v1

Status: `TREND_REFERENCE_AUDIO_LOCKED / HG02_REFERENCE_BUILDING`
Upstream: `D02 / HG01 PASS`
SONG_FAMILY: `如果风会替我说话`

## 1. Core-account audio verification

Three selected core-account works were independently parsed, fully downloaded, decoded and compared with Chromaprint fingerprints.

All three expose the **same Douyin music asset**:

- Douyin music asset id: `7670880580757867270`
- displayed music title: `@林叙（错位秋天已上线）创作的原声`

Works:
- 火乐烁 — aweme `7674213606980010597` — video duration `24.286621s`
- XIANGJISHI — aweme `7674182530162440933` — video duration `11.900667s`
- 乐 ♩青春 — aweme `7673915982527960265` — video duration `12.073991s`

Pairwise Chromaprint similarity:
- 火乐烁 vs XIANGJISHI: `0.994583`
- 火乐烁 vs 乐 ♩青春: `0.986020`
- XIANGJISHI vs 乐 ♩青春: `0.986250`

All best alignments are `shift=0`.

Decision:
`SAME_AUDIO_FAMILY_CONFIRMED`.

## 2. B0 lock

The trend-native reference for the first R3 production test is now:

`AUDIO_VERSION_REFERENCE = DOUYIN_MUSIC_ASSET:7670880580757867270`

This is stronger than a title-label match because the exact music asset URL/id and the decoded audio fingerprints agree across all three core accounts.

## 3. Full-track identity discovery

Public indexed listening references identify the full song as:

`如果风会替我说话 — 张蓓蓓、林叙`

A public Bilibili indexed upload is approximately `2:28` long and uses the hook text `如果风会替我说话 / 如果雨会替我回答`.

This establishes a plausible full-length release identity, but the full-length source is **not yet the production BGM lock**. The first test should preserve the exact Douyin trend asset unless the user explicitly prefers a longer cut after HG02 listening.

## 4. Length decision for HG02

Observed behavior is useful:
- two visual/music accounts use roughly the first `12s` of the shared asset;
- 火乐烁 uses roughly `24.3s` from the same start point;
- fingerprint alignment indicates the shorter works are truncations of the same beginning, not alternate edits.

Therefore HG02 will first present a `~24s` trend-native listening reference extracted from the 火乐烁 work.

User decision after listening:

### Option A｜Trend-native short MV
Lock the ~24s shared Douyin version.

Pros:
- exact version already repeated across the three core accounts;
- strongest trend fidelity;
- fits high-completion short music-promotion format;
- avoids unnecessary full-track/version drift.

### Option B｜Extended MV
Continue to obtain/validate the full `张蓓蓓、林叙` release and choose a `30–40s` excerpt containing the same hook.

Pros:
- more lyrical space / more visual beats.

Risk:
- adds an extra source/version alignment step and may move away from the exact trend-native audio asset.

## 5. Gate

- `SONG_FAMILY_LOCKED = YES`
- `TREND_REFERENCE_AUDIO_VERSION_LOCKED = YES`
- `HG02_BGM_LOCKED = NO`

Next: user listens to the generated ~24s HG02 reference and chooses short trend-native vs extended full-track route.
