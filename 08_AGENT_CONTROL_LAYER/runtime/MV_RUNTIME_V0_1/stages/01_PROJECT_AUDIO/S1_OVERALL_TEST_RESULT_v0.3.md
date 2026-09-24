# S1 PROJECT_AUDIO — Overall Test Result v0.3

Date: 2026-09-24
Selected Song Family: 若爱有尽头

## 1. Test objective

Validate the complete S1 chain:

S1A autonomous material acquisition
-> S1B version verification
-> S1C segment/audio analysis
-> S1D final audio/timeline lock

The user explicitly allows a suitable alternate version, but not an unrelated same-title song.

Therefore alternate-version acceptance requires:
1. title relationship is clear;
2. composition/lyrics are verified as the same intended work or explicitly accepted as a valid alternate;
3. actual analyzable media exists.

## 2. Current source states

### Source A — 张蓓蓓 / 林叙 version

Public evidence:
- current Douyin work identifies 林叙/张蓓蓓《若爱有尽头》;
- public lyric video provides a full lyric text;
- public music-index evidence lists 张蓓蓓、林叙 - 若爱有尽头.

Media state:
`METADATA_AND_LYRICS_VERIFIED / MEDIA_NOT_ACQUIRED`

Public-video acquisition fallback:
FAILED because the platform requested sign-in/bot confirmation.

The runtime deliberately did NOT add cookies/session/login bypass.

### Source B — 于一 version

Catalog evidence:
- Apple Music: 于一《若爱有尽头》, 2025-02-25;
- Audiomack: same release identity;
- Deezer: same title/artist with 216s track and public 30s preview.

Media state:
`ANALYSIS_PREVIEW_ACQUIRED`

Actual acquired artifact:
- format: MP3
- bytes: 480245
- duration: 30.014688s
- sample rate: 44100Hz
- channels: 2
- bitrate: 128002bps
- SHA256: 62e1955e98a30279cf7b22b6f87517457ffb8bebc6dcf9199e9003fae347269c

Important:
No reliable public evidence found yet proving that 于一 version and 张蓓蓓/林叙 version share the same lyrics/composition.

Therefore:
`ALT_VERSION_IDENTITY_UNVERIFIED`

It is usable as an S1 technical analysis sample, but not yet as the authoritative production version.

## 3. Audio analysis of acquired 于一 preview

Estimated tempo:
`~129.2 BPM`

The 30s preview contains sustained rhythmic density rather than a quiet intro.

### Candidate T1 — late high-density window

Preview-relative:
`14.756s -> 29.698s`

Duration:
`14.942s`

Observed:
- 40 onset events
- 33 beats
- average RMS approx -4.52 dB relative to preview max
- includes strong late energy around 18s, 22–26s and final seconds

Technical suitability:
`HIGH`

Why:
- close to 15s target;
- beat-aligned boundaries;
- dense enough for multiple animation/motion beats;
- stronger ending energy than the first half.

### Candidate T2 — middle continuous window

Preview-relative:
`4.644s -> 19.807s`

Duration:
`15.163s`

Observed:
- 36 onset events
- 33 beats
- average RMS approx -4.44 dB relative to preview max
- strong local energy around 7s and 18s

Technical suitability:
`MEDIUM-HIGH`

Why:
- slightly smoother energy arc;
- gives more lead-in before the later rise;
- less ending drive than T1.

### Technical preference

For motion-heavy 15s MV testing:
`T1 = 14.756–29.698s`

For a more gradual emotional build:
`T2 = 4.644–19.807s`

## 4. What cannot yet be claimed

The acquired preview does not provide enough evidence to claim:
- its lyrics equal the selected 张蓓蓓/林叙 version;
- T1 or T2 contains a complete intended lyric sentence;
- the preview-relative timestamp maps to the full song's original timestamp;
- T1 is the best section across the entire song;
- the production Audio Version is locked.

Therefore these windows are:
`TECHNICAL_CLIP_CANDIDATES`
not:
`FINAL_PROJECT_SEGMENTS`

## 5. S1 phase verdict

### S1A MATERIAL_ACQUISITION
`PASS / COMPONENT SEALED`

Evidence:
- Apple adapter validated;
- Deezer adapter validated;
- direct-public-media E2E download/probe PASS;
- public-video fallback correctly fails closed when sign-in/cookies are required.

### S1B VERSION_VERIFICATION
`PARTIAL`

Target 张蓓蓓/林叙 identity:
metadata/lyrics supported.

Acquired 于一 media:
real artifact exists, but equivalence to target work is unverified.

### S1C SEGMENT_TIMELINE_ANALYSIS
`PARTIAL PASS`

Technical audio segmentation:
PASS on acquired preview.

Semantic lyric/timeline lock:
BLOCKED by alternate-version identity and preview-only coverage.

### S1D AUDIO_TIMELINE_LOCK
`NOT PASSED`

No authoritative final segment may be sealed yet.

## 6. Overall S1 verdict

`S1_OVERALL = PARTIAL_PASS_NOT_SEALED`

What is proven reliable:
- S0 can hand a Song Family to S1;
- S1 can autonomously search multiple source types;
- S1 can acquire real media without user upload when catalog coverage exists;
- S1 can distinguish exact vs same-title wrong versions;
- S1 can probe and analyze a real audio artifact;
- S1 can produce technically reasonable 15s clip candidates;
- S1 stops before falsely claiming semantic/timeline truth.

What is not yet proven:
- automatic acquisition of a production-usable version for every Chinese short-video song;
- automatic proof that alternate singer versions are the same composition;
- authoritative lyric timing when only a preview is available.

## 7. Recommended S1 acceptance rule

A practical S1 production path should allow a "suitable alternate version", but require:

`SAME_WORK_VERIFIED`

where at least one is true:
- lyrics/composition credits match;
- reliable lyric text matches;
- trusted metadata explicitly identifies the version as cover/remake of the same work;
- user explicitly approves the alternate after comparison.

Then media coverage must be:
- TARGET_SEGMENT_SOURCE_ACQUIRED, or
- FULL_SOURCE_ACQUIRED.

Only then may S1D seal.

## 8. Current conclusion for 若爱有尽头

Song direction remains valid.

The 于一 preview is a useful technical acquisition sample, but not yet a safe production substitute.

Current stage should remain:
`S1 PARTIAL_PASS / NOT_SEALED`

Do not return to S0.
Do not start S2 yet.
