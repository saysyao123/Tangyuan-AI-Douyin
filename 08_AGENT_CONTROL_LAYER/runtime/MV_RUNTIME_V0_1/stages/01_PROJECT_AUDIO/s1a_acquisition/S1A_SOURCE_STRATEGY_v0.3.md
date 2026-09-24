# S1A Source Strategy v0.3

Date: 2026-09-24

## Goal

Acquire production-usable audio for S1 without making user-supplied files the default.

The key distinction is:

- PREVIEW source: useful for identity / technical checks only
- FULL source: usable for whole-song analysis
- TARGET-SEGMENT source: usable when it fully covers the intended MV segment plus lead-in/out

## Tier 0 — Existing validated zero-credential adapters

### Apple/iTunes Search API

Capability:
- official 30-second preview URL
- metadata / artist / track duration

Use:
- version discovery
- audio identity comparison
- acquisition selftest

Limit:
- preview only
- Apple terms restrict preview assets to promotional/store contexts

Runtime role:
`PREVIEW_ONLY`

### Deezer public preview

Capability:
- public 30-second preview
- track metadata

Use:
- version discovery
- acquisition selftest

Limit:
- preview only

Runtime role:
`PREVIEW_ONLY`

### Direct Public Media

Capability:
- any source that itself exposes a normal public HTTPS audio/video asset
- downloads, hashes and probes it

Use:
- full or target-segment source when the source is legitimately public

Runtime role:
`PREVIEW | TARGET_SEGMENT | FULL`

## Tier 1 — Recommended authorized Full-Source adapters

### Audiomack Official API

Official docs:
- OAuth 1.0a
- consumer key / secret required
- track entity can return a short-lived `streaming_url`
- play endpoint returns the streaming source

Why valuable:
- can expose full MP3 stream when the track is available
- suitable for cloud acquisition
- strong fit for music explicitly published on Audiomack

Current blocker:
- Runtime has no Audiomack consumer key/secret
- anonymous request returns `Invalid consumer key`

Recommended implementation:
GitHub Actions secrets:
- `AUDIOMACK_CONSUMER_KEY`
- `AUDIOMACK_CONSUMER_SECRET`

Router role:
`FULL_SOURCE_CANDIDATE`

### SoundCloud Official API

Official docs:
- OAuth 2.1
- public tracks can be playable off-platform when access permits
- track streams endpoint returns streamable URLs
- some tracks expose `downloadable=true` + `download_url`
- restricted/paywalled/geo-blocked tracks may expose no stream URL

Why valuable:
- full playback can be available for public tracks
- download can be explicitly allowed by the uploader
- clear access states: playable / preview / blocked

Current blocker:
- requires an app/access token
- target Chinese-song coverage is unknown and must be searched after auth

Recommended secrets:
- `SOUNDCLOUD_ACCESS_TOKEN`

Router role:
`FULL_SOURCE_CANDIDATE`

### 7digital Media Delivery API

Capability:
- previews/media delivery
- consumer key / secret
- signed media requests

Why useful:
- catalog-oriented source with explicit media delivery API

Limit:
- catalog coverage for current Chinese short-video songs is unknown
- credentials required

Router role:
`FULL/PREVIEW_CANDIDATE`

## Tier 2 — Chinese licensed-catalog adapters

### Tencent / QQ Music official music service

Current official capability:
- QQ Music metadata and playback-link capability exists in Tencent music/IoT SDK products
- user/account authorization is required for many operations

Why strategically important:
- much stronger Chinese mainstream catalog coverage than Western preview catalogs

Limit:
- intended as licensed playback integration, not arbitrary raw-file download
- may require device/app onboarding, user authorization and commercial terms
- media may need to be analyzed as an authorized stream rather than exported MP3

Router role:
`AUTHORIZED_STREAM_SOURCE`

### Kugou Open Music Component

Official capability:
- large licensed music catalog
- online playback SDK
- pay-per-use model
- intended for apps/content scenarios

Why strategically important:
- strong Chinese catalog coverage

Limit:
- documented component is streaming-only
- not a raw-file download API
- integration/commercial account required

Router role:
`AUTHORIZED_STREAM_SOURCE`

### NetEase Cloud Music multi-terminal SDK

Evidence:
- official developer endpoint/SDK artifacts exist for multi-terminal playback

Why potentially useful:
- Chinese catalog coverage

Limit:
- exact backend media-export capability must be verified under official agreement
- do not use reverse-engineered community APIs as production default

Router role:
`RESEARCH / AUTHORIZED_STREAM_SOURCE`

## Tier 3 — Purchased / owned-file sources

### Bandcamp

Official behavior:
- purchases can be downloaded as actual files
- re-download supported
- files can be DRM-free/high quality depending on purchase

Use:
- excellent when the selected work is sold there
- user purchase/account may be required

Runtime role:
`OWNED_FULL_SOURCE`

### User-owned cloud/library file

Examples:
- Drive / Dropbox / OneDrive / Box / local upload

Use:
- not the default first step
- strongest fallback when the exact selected version is already legally owned

Runtime role:
`OWNED_FULL_SOURCE`

## Tier 4 — Royalty-free / explicitly downloadable catalogs

### Jamendo

Official API:
- full-track file endpoint
- download allowed only when `audiodownload_allowed=true`
- requires developer client_id

Use:
- excellent for royalty-free / creator-authorized music

Limit:
- poor fit for current mainstream Chinese song selection

Runtime role:
`FULL_SOURCE_FOR_LICENSED_LIBRARY`

## Explicitly excluded from production default

- unofficial free-MP3 aggregators
- reverse-engineered QQ/NetEase/Kugou private APIs
- extracting browser cookies/session tokens
- DRM decryption
- stream-ripping paths that require bypassing platform restrictions
- same-title substitution without SAME_WORK verification

## Recommended S1A Router v0.3

```
S0 Song Family
  ↓
Owned/Purchased full source already available?
  ├─ YES → FULL_SOURCE_ACQUIRED
  ↓ NO
Authorized Full-Source Adapters
  1 Audiomack OAuth
  2 SoundCloud OAuth
  3 7digital / other licensed media delivery
  4 Chinese licensed catalog SDK/stream adapter
  ↓
Direct public media?
  ├─ YES → classify PREVIEW/TARGET/FULL
  ↓ NO
Preview adapters
  Apple / Deezer
  ↓
Use for identity only
  ↓
If no FULL/TARGET source:
SOURCE_COVERAGE_BLOCKED
```

## Practical priority

For the current project:

1. Add Audiomack developer credentials if available.
2. Add SoundCloud developer access and search the selected Song Family.
3. Investigate a licensed Chinese-catalog adapter as the long-term production solution.
4. Keep Apple/Deezer as zero-cost metadata/preview fallbacks.
5. Do not lower S1C standards just because only a preview is available.

## Acceptance rule

S1C may begin formal clipping only when:

`FULL_SOURCE_ACQUIRED`

or

`TARGET_SEGMENT_SOURCE_ACQUIRED`

Preview-only media never qualifies.
