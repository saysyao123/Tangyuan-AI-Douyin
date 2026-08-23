# WEB R2｜W08B V3 Edit Map + Picture Preview QA v1

> Status: `EDIT_MAP_LOCKED / PICTURE_PREVIEW_RENDERED / TECH_QA_PASS / AESTHETIC_VIEWING_PENDING`
> Timing truth: `AUDIO_TIMELINE_PACKAGE/` only.
> V1/V2 timing assets remain revoked and are not used here.

## 1. Why V3 picture order is materially different from V1/V2

The locked actual excerpt starts with:
`我要学着树叶翩翩起舞`

The title line:
`如果你也刚好抬头看树`
actually starts at `19.090s`.

Therefore the previous picture order cannot simply be reused. V3 deliberately reorders accepted visual assets so that:
- leaf / dance imagery opens the clip;
- the bird is revealed on the verified `鸟儿` anchor;
- S7 carries the verified `飞过树梢` motion peak;
- S1 monumental tree / look-up material moves to the real title-line region around 19s;
- cloud/sky imagery moves to the verified `白云 / 漂浮` and final release regions.

## 2. Locked editor inputs

Audio Timeline Package:
- BGM SHA-256: `bc41422b91588b5d62ad37ce37545bdf1b1b0ef0857a6731d6ceb9748b1fab33`
- content timeline: `37.120s`
- 10 lyric lines: PASS
- 10 semantic anchors: PASS
- 21 music events: PASS

Visual source hashes:
- `2S1.mp4` — `8e036920e787251bf24efcf4ab1fb24e19912e6374704fb64eacea34bd074ff7`
- `2S2(1).mp4` — `ef6bcb8a3401ef0830e31b6f1321a0a8f2e1d5d05291269945af295328adfaa1`
- `2S3.mp4` — `b263806a731ed1864a4ae8727a5e0d3fe9c31c0765890d2ea377eb223096d821`
- `2S4.mp4` — `abc395f41e3a23672392e04d86cf450cf5c4c08414126ebfcb4401b57e9dd942`
- `2S5.mp4` — `38bfd45c4ad4e880b9aeaa9b5e36e2d2c4f9e8ab074d8618d58f2f4986d84e43`
- `2S6.mp4` — `5a4bef562fadf48441997a6d0cf5bb4befee2c6c83ff83d81d2da7aaf3b9b1d9`
- `2S7.mp4` — `c3d84f517351a8b2c8ebb6f007a62d6a87e7cc6d3b1e3fcf103b0207b97ae23e`
- `2S8.mp4` — `0099b29417b9288a1e840374a37c0726966262ae9999c3fbcdefae795d101154`
- `2S9.mp4` — `bc1cc04c509d366f8ea0ccac177a6a3d191f1f33403c9f482be695cfe9d8f3a1`

All sources are `720×1280 / 24fps / ~5.041667s`.

Canonical edit map:
`W08B_V3_EDIT_MAP_v1.csv`

## 3. Frame-clock design

V3 uses a frame-quantized picture clock:
- fps: `24`
- total picture frames: `891`
- picture duration: `37.125s`
- locked audio content: `37.120s`
- expected end quantization delta: `+0.005s`.

Picture cuts do NOT rewrite lyric timing. The picture clock intentionally pre-enters several lyrics so the visual action can land on the verified semantic anchor.

## 4. Critical semantic-hit QA

### A01｜树叶
- locked anchor: `1.581–1.961s`
- picture: S2 hand/leaf Arc
- result: PASS.

### A03｜鸟儿
- locked anchor: `8.525–8.925s`
- S6 is pre-entered at picture `7.125s`;
- S6 internal person→bird cut occurs at source ~`1.416667s`;
- rendered bird reveal: ~`8.542s`;
- delta vs anchor start: ~`+0.017s`.
- result: PASS.

### A04｜飞过树梢
- locked anchor: `15.008–18.290s`;
- S7 clean peak starts at `14.958s`;
- risky S7 source frames `65–97` (~`2.708–4.042s`) are completely excluded;
- source resumes only at clean final canopy window `97–121`;
- result: PASS / topology-risk exclusion preserved.

### A05/A06｜抬头 / 看树
- `抬头`: `20.851–21.211s`;
- S1 begins at `18.667s`; its low-angle person section has already entered before the anchor;
- `看树`: `21.392–21.732s` lands inside S1 eye close-up;
- S1 repeated/similar low-angle source frames `58–75` are excluded;
- result: PASS.

### A07/A08｜白云 / 漂浮
- `白云`: `24.353–24.693s` lands in shortened S8 wide sky/cloud shot;
- `漂浮`: `26.054–26.454s` lands after transition to S3 wind/veil portrait;
- visual grammar: literal cloud -> physical floating fabric;
- result: PASS.

### A09｜清晨
- locked anchor: `30.697–31.077s`;
- picture: later S5 monumental tree / visible sun shaft;
- result: PASS.

### A10｜坐下来
- L10 vocal entry / anchor starts `32.838s`;
- final S9 cloud/sky release begins at `32.833s`, only ~`0.005s` before vocal entry;
- S9 runs ~`4.292s`, longer than S8 (~`2.917s`), preserving W07 ending-role distinction;
- result: PASS as emotional release rather than literal action illustration.

## 5. W07 trim rules preserved

- S1 duplicate low-angle middle: excluded (`source frames 58–75`).
- S7 ambiguous large-fabric loop: excluded (`source frames 65–97`).
- S8 vs S9 repetition: S8 shortened to ~`2.917s`; S9 gets ~`4.292s` final hold.
- S6 bird hold remains readable; no extra generation required at this stage.
- no visual source regeneration performed.

## 6. Source-audio / watermark handling

Source audio:
- every Seedance source audio stream is ignored at ingest;
- filter graph consumes video streams only;
- locked W02 v3 BGM is the sole audio mapped into Preview.

Preview safe crop:
- `crop=630:1120:20:72`;
- scaled back to `720×1280`;
- `SAR=1:1`;
- this reuses the previously validated consistent crop approach to keep generator marks outside the viewing area without changing timing.

## 7. Render technical QA

Output:
`如果你也刚好抬头看树_MV_WEB_R2_V3_PicturePreview.mp4`

Technical result:
- video: H.264 / `720×1280` / `24fps` / `SAR 1:1`;
- video frames: `891`;
- video duration: `37.125s`;
- audio: AAC / 44.1kHz;
- audio duration: `37.120s`;
- file SHA-256: `09e68c852d50fd43059fa70b8555ec7a742451af27ca2e3c177595ae5f240111`.

Audio identity implementation cross-check:
- decoded Preview audio vs locked v3 BGM best global lag: `0.000s`;
- normalized correlation: ~`0.99960`;
- result: PASS; no new FFmpeg/AAC global timing shift introduced.

## 8. Current Gate

`EDIT_MAP_LOCKED = YES`

`PICTURE_PREVIEW_RENDERED = YES`

`EDIT_PREVIEW_TECH_QA_PASS = YES`

`EDIT_PREVIEW_QA_PASS = NO / AESTHETIC_VIEWING_PENDING`

Reason:
The picture timing, asset identity, anchor hits and technical implementation are now internally verified, but this WEB R2 calibration still requires the user to view the actual music+picture preview before the edit is promoted to W09 subtitle implementation.

## 9. Next allowed action

Human viewing Gate on the V3 Picture+BGM Preview.

If accepted:
`EDIT_PREVIEW_QA_PASS -> W09 Subtitle Style + Implementation QA`, using canonical `AUDIO_TIMELINE_PACKAGE/lyrics_exact.srt` only.

If a specific visual rhythm issue is found:
modify only the identified W08B fragment(s); do not reopen W02A timing truth or approved visual generation by default.
