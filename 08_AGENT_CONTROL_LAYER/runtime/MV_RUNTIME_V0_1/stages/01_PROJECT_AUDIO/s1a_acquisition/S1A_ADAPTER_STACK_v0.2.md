# S1A Acquisition Adapter Stack v0.2

## Goal

Turn a sealed S0 Song Family into an actual analyzable media object without making user upload the default path.

## Adapter order

### A1 APPLE_ITUNES_PREVIEW_V0_1

Purpose:
Acquire official 30-second Apple/iTunes preview media when the exact title + artist/version is present in the public catalog.

Why reliable:
- official public search endpoint;
- preview URL is a real media asset;
- no browser scraping;
- no login;
- no hidden stream extraction.

Hard rule:
same-title different-artist result is NOT accepted.

### A2 DEEZER_PREVIEW_V0_1

Purpose:
Acquire the service's 30-second preview when exact title + artist match exists.

Hard rule:
preview is internal analysis material only; do not treat it as a distributable production master.

### A3 DIRECT_PUBLIC_MEDIA_V0_1

Purpose:
Acquire a source URL only when the source itself exposes a normal public HTTPS audio/video asset.

Checks:
- HTTPS only;
- Content-Type must be audio/video/octet-stream;
- no login/cookie/token bypass;
- SHA-256 recorded;
- ffprobe required.

### A4 CONNECTED_URL_MEDIA_ADAPTER

Future:
A connected app may satisfy acquisition if it can ingest a public URL and expose analyzable audio/video or timestamped transcript.

Current installed AccurateScribe flow requires a user-selected uploaded file, so it does not yet satisfy autonomous S1A.

## Explicitly excluded default paths

- stream ripping;
- DRM/decryption;
- login/session extraction;
- private API credential harvesting;
- unofficial MP3 aggregation as the production default;
- silently replacing a missing version with a different cover/remix/live recording.

## Success states

MEDIA_ACQUIRED:
actual bytes/object acquired and probed.

MEDIA_ACQUIRED_VERSION_UNVERIFIED:
bytes exist but exact version identity still needs S1B.

NO_EXACT_PREVIEW_MATCH:
adapter works but catalog lacks target version.

SOURCE_NOT_DIRECT_MEDIA:
URL is only a webpage/player.

ACQUISITION_BLOCKED:
all allowed adapters exhausted for the requested version.

## Important architectural result

An adapter can PASS technically even when one song returns NO_EXACT_PREVIEW_MATCH.

S1A reliability is measured by:
- correct source classification;
- correct version protection;
- actual-media verification;
- graceful fallback between adapters;
- no false MEDIA_ACQUIRED.
