# S1A MATERIAL_ACQUISITION — Validation Report v0.2

Date: 2026-09-24

## Component verdict

`S1A COMPONENT = VALIDATED`

S1A can now autonomously:
1. query normal public/official preview catalogs;
2. protect exact Song/Artist version identity;
3. obtain actual public preview media when a valid URL exists;
4. verify Content-Type;
5. download media bytes in GitHub Actions cloud;
6. calculate SHA-256;
7. run ffprobe;
8. publish structured acquisition state;
9. upload short-lived media artifacts;
10. return a clean blocked state when the exact target version is unavailable.

## Adapter stack

### A1 — APPLE_ITUNES_PREVIEW_V0_1
Status: `ADAPTER_VALIDATED`

Target test:
`若爱有尽头 / 张蓓蓓 / 林叙`

Result:
`NO_EXACT_PREVIEW_MATCH`

The API returned same/near-title catalog entries including 于一, but no artist match.
Correct behavior:
NO DOWNLOAD / NO SILENT SUBSTITUTION.

### A2 — DEEZER_PREVIEW_V0_1
Status: `ADAPTER_VALIDATED`

Target test:
`若爱有尽头 / 张蓓蓓 / 林叙`

Result:
`NO_EXACT_PREVIEW_MATCH`

Returned catalog candidates included 于一 and 张东林, but no 张蓓蓓/林叙 match.
Correct behavior:
NO DOWNLOAD / NO SILENT SUBSTITUTION.

### A3 — DIRECT_PUBLIC_MEDIA_V0_1
Status: `END_TO_END_PASS`

Self-test input:
a normal public Deezer 30-second preview URL used only to validate media transport/probe mechanics.

Result:
`MEDIA_ACQUIRED`

Verified:
- Content-Type: audio/mpeg
- Bytes: 480245
- SHA-256: 62e1955e98a30279cf7b22b6f87517457ffb8bebc6dcf9199e9003fae347269c
- Codec: mp3
- Duration: 30.014688s
- Sample Rate: 44100 Hz
- Channels: 2
- Bitrate: 128002 bps

This proves:
`PUBLIC MEDIA URL -> CLOUD DOWNLOAD -> HASH -> FFPROBE -> ARTIFACT`
works end-to-end.

### A4 — S1A_ACQUISITION_ROUTER_V0_1
Status: `ROUTER_VALIDATED`

Order:
1. Apple exact preview
2. Deezer exact preview
3. verified direct-media URLs only

Current target result:
`CATALOG_COVERAGE_BLOCKED`

This is a valid terminal state, not a component failure.

## Current Case 001

Song Family:
`若爱有尽头`

Required version hints:
- 张蓓蓓
- 林叙

Public evidence confirms this version/song identity exists on current Douyin / lyric / music-index pages.

However, current compliant autonomous adapters do not expose analyzable media bytes for that exact version.

Case state:
`CATALOG_COVERAGE_BLOCKED`

## Why this is not S1A failure

The acquisition mechanism has already demonstrated MEDIA_ACQUIRED on a normal public preview source.

For Case 001, the missing condition is:
`EXACT_VERSION_SOURCE_AVAILABLE_TO_ALLOWED_ADAPTER`

not:
`DOWNLOADER_BROKEN`

## Allowed future source adapters

A source can be added when it provides one of:
- official/public preview URL;
- normal direct public audio/video media URL;
- authorized platform export;
- connected app/tool that exposes an analyzable media object from an authorized source.

## Excluded default approaches

- DRM/decryption;
- stream ripping;
- login/session/cookie extraction;
- private/undocumented credential harvesting;
- unofficial free-MP3 aggregator as production source;
- automatic use of a same-title different-artist recording.

## Stage integration

S1A component state:
`SEALED_COMPONENT_V0_2`

Current project acquisition case:
`BLOCKED_SOURCE_COVERAGE`

This distinction must be preserved.

S1B may begin only when an exact/approved media artifact reaches:
`MEDIA_ACQUIRED` or `MEDIA_ACQUIRED_VERSION_UNVERIFIED`.
