# WEB R3｜HG02 BGM Lock Receipt v1

Status: `PASS / BGM_LOCKED`

## Human decision

User acceptance:
`这个BGM我觉得没问题，下一步该做什么了`

Interpretation under `mv_human_gates.md`:
`HG02 BGM Excerpt Listening Gate = PASS`

## Locked BGM identity

- SONG_FAMILY: `如果风会替我说话`
- exact production version: `Douyin trend-native music asset`
- Douyin music asset id: `7670880580757867270`
- Douyin display: `@林叙（错位秋天已上线）创作的原声`
- listening artifact: `如果风会替我说话_R3_HG02_抖音同款24秒试听.mp3`
- source basis: actual 火乐烁 core work / aweme `7674213606980010597`, cross-validated against two additional core works
- duration: `24.320000s`
- codec: `MP3`
- sample rate: `44100 Hz`
- channels: `2`
- speed/time-stretch: `none after HG02 artifact creation`
- SHA-256: `f128163c62f16eb94e5e302d2f97f725bcaa775a457fc09ffd21b9c4f65a8553`

## Upstream evidence

- `B0_IF_WIND_AUDIO_PROBE/audio_probe_report.json`
- three core works use exact same asset id
- pairwise Chromaprint similarity minimum `0.986020`
- all best fingerprint alignments `shift=0`

## Gate state

- `REFERENCE_BGM_LOCKED = YES`
- `TREND_REFERENCE_AUDIO_VERSION_LOCKED = YES`
- `HG02_BGM_LISTENING_PASS = YES`
- `BGM_LOCKED = YES`
- `AUDIO_TIMELINE_PACKAGE_LOCKED = NO`

## Invalidation

Any change to the actual locked artifact bytes, duration, speed/time-stretch, lead-in/out, or chosen audio version invalidates this lock and all timing-dependent downstream assets.

## Next

Enter `Stage 2A / AUDIO_TIMELINE_PACKAGE`.
No formal Director timing allocation, First Frames, Dynamic, Picture Edit, or Subtitle production may begin before Stage 2A PASS.
