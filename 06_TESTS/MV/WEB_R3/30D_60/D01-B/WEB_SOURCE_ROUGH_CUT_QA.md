# D01-B｜WEB Source Rough-Cut QA

Status: `PASS`

## Batch geometry

R2 validated WEB baseline applied uniformly to all four final sources:

`crop=576:1024:72:128 -> scale=720:1280 -> setsar=1`

Equivalent visual zoom: approximately `1.25x`.

## Technical outputs

All four clean proxies:
- output geometry: `720x1280`
- frame rate: `24fps`
- SAR: `1:1`
- source audio: physically removed
- no per-shot repositioning
- no local blur/patch masking

Local clean-proxy SHA-256:
- S01: `90c0818d132d5f08a26bb1a147381cbf18f5dc43c5753af1496a3367703be68a`
- S02: `023853a8efe586c66228afdb4863b2216125269abd9666c9e3e94845343d78cf`
- S03: `62d8a62b2f665e54041923af2990a0364653dd946b5deaea934310a6fa322599`
- S04: `7f410cb4dbc7a759fdde5153505eb24408b099beb5a62cb979e0341a43bc9ae0`

Same-EDL clean picture render:
- local file: `D01-B_PICTURE_EDIT_V1_CLEAN_HG04_LOCKED.mp4`
- SHA-256: `ad13de99db7703117be1f7f6e577333840780d4688e5b30e4d78322d6985495e`
- container duration: `16.000s` (24fps/video+AAC mux quantization; locked musical content remains the approved BGM timeline)

## Corner-risk QA

Representative samples checked at approximately `0.2s / 2.5s / 4.7s` for every source.

PASS:
- no visible generator mark at left-top risk zone;
- no visible generator mark at right-bottom risk zone;
- no mixed watermark state;
- no stretch/SAR error;
- S01 wide-space composition remains readable;
- S02 hands/water event remains readable;
- S03 white-flower visual center remains readable;
- S04 ascent/negative-space composition remains readable.

## Retrofit / HG04 regression

This gate was retrofitted after the first rhythm preview. The exact approved EDL was preserved. Uniform crop changes framing only and does not materially change the accepted rhythm or semantic sequence, so HG04 remains locked under the runtime `Patch, Don't Cascade` rule.

`NO_VISIBLE_GENERATOR_MARK = YES`
`WEB_SOURCE_ROUGH_CUT_GATE_PASS = YES`
`HG04_REOPEN_REQUIRED = NO`
