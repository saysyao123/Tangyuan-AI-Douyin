# S1A MATERIAL_ACQUISITION v0.1

## Purpose

After S0 locks a Song Family, S1 must attempt to obtain the analyzable song/video material itself.

The normal workflow must not assume the user will manually download and upload media.

## Acquisition definition

`MEDIA_ACQUIRED` means:
- actual media bytes are available to the analysis runtime; or
- an integrated media tool exposes the media object sufficiently for audio/video analysis.

The following do NOT count:
- search result only;
- playable webpage only;
- title/artist metadata only;
- thumbnail;
- lyrics page without audio;
- a URL that the runtime cannot read as media.

## Adapter order

### A1 Direct/normal media access
Try S0 reference leads and official/public sources that expose a normal accessible media artifact.

### A2 Same-song alternate source
Search the same Song Family for an accessible source.

Version must be recorded:
- original;
- cover;
- remix;
- live;
- lyric-video audio;
- other.

Do not silently assume they are identical.

### A3 Tool-accessible media
If a connected tool can directly ingest the public source and expose analyzable media, that counts as acquisition even if no local download file is produced.

### A4 Block
If only streaming webpages/metadata are accessible:
`ACQUISITION_BLOCKED`

Do not send the task backward to S0.

## What happens after acquisition

MEDIA_ACQUIRED
-> probe duration/codec/audio
-> verify exact version
-> select useful segment
-> lyric/audio timeline
-> Human Audio Lock
-> S1 SEALED

## User involvement

The user is not expected to provide a file by default.

User upload is a fallback only when:
- all normal autonomous acquisition routes fail; and
- the user still wants to use that exact inaccessible version.

This fallback must be reported as an exception, not designed as the normal workflow.
