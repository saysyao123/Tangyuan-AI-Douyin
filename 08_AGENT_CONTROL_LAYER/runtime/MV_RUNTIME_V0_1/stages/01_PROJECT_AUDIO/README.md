# Stage PROJECT_AUDIO

Status: DESIGNING / S1A_ACQUISITION_SEARCHING

Current full-stage candidate:
`v0.3-draft`

## Purpose

Starting from S0's user-selected Song Family, S1 owns the full audio-material path:

S1A MATERIAL_ACQUISITION
-> S1B VERSION_VERIFICATION
-> S1C SEGMENT_TIMELINE_ANALYSIS
-> S1D AUDIO_TIMELINE_LOCK

## New default

S0 does not need to deliver a local file.

S1 must first attempt to obtain analyzable media itself from normal public/authorized sources.

The user is not expected to manually download/upload media as the default workflow.

## S1A success condition

`MEDIA_ACQUIRED` requires actual analyzable media bytes/object.

A webpage, title, lyrics page, thumbnail or search result alone does not count.

## Current real case

Selected Song Family:
`若爱有尽头`

Current S1A state:
`ACQUISITION_SEARCHING`

See:
- S1_STAGE_CONTRACT_DRAFT_v0.3.yaml
- S1A_MATERIAL_ACQUISITION_v0.1.md
- S1A_ACQUISITION_CASE_001.md

## Preserved earlier work

S1 v0.2 successfully tested:
- timeline continuity;
- deterministic duration checks;
- compact timeline handoff;
- downstream Director consumption.

That work remains useful for S1C/S1D, but v0.2 is no longer the complete entry contract because media acquisition now belongs at the front of S1.

Do not start S2 until S1 is SEALED.
