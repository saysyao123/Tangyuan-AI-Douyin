# S1A MATERIAL_ACQUISITION v0.2

Status: `SEALED_COMPONENT`

## Responsibility

Autonomously turn an S0 Song Family selection into a real analyzable media object whenever a compliant source is available.

## Router

`S1A_ACQUISITION_ROUTER_V0_1`

Adapter order:
1. Apple/iTunes official preview
2. Deezer public preview
3. verified normal public direct-media URL
4. future authorized connected media adapter
5. BLOCKED_SOURCE_COVERAGE

## Definition of success

MEDIA_ACQUIRED requires:
- actual media bytes/object;
- source provenance;
- version identity state;
- successful media probe;
- stable artifact/report reference.

A webpage or playable streaming UI alone is not acquisition.

## Version safety

Same title is insufficient.

A target version must match the required artist/version evidence or be explicitly approved as an alternate version.

No silent cover/remix/live substitution.

## Autonomous default

User file upload is not part of the normal path.

It remains an exception fallback only when:
- the exact selected version is unavailable to all compliant adapters;
- and the user explicitly wants to preserve that inaccessible exact version.

## Validation

See:
`S1A_VALIDATION_REPORT_v0.2.md`

The direct-media selftest has demonstrated:
URL -> cloud download -> SHA256 -> ffprobe -> artifact.

## Current selected-song case

`若爱有尽头 / 张蓓蓓 / 林叙`

Component:
PASS

Current exact-version source coverage:
BLOCKED

Do not redesign S0 or S1A because of this case.


## Media coverage classes

S1A must distinguish media coverage from mere byte acquisition.

### ANALYSIS_PREVIEW_ACQUIRED

A real analyzable preview/sample exists, but it does not cover the full song or all candidate regions.

Allowed downstream use:
- codec/duration/probe validation;
- identity/voice/version comparison;
- lyric/audio alignment only inside the preview window;
- acquisition adapter validation.

Not sufficient for:
- searching the whole song for the best MV segment;
- claiming the final production master is locked.

### TARGET_SEGMENT_SOURCE_ACQUIRED

The acquired media fully covers a user/agent-selected target segment with enough lead-in/out for accurate cutting.

Allowed downstream use:
- precise segment timeline;
- cut-point analysis;
- S1D segment lock.

### FULL_SOURCE_ACQUIRED

The acquired media covers the complete selected song/version.

Allowed downstream use:
- full-song structure analysis;
- global best-segment search;
- authoritative full timeline if needed.

## Transition rule

For S1C:

- full-song best-section search requires FULL_SOURCE_ACQUIRED;
- analysis of a known target segment requires TARGET_SEGMENT_SOURCE_ACQUIRED or FULL_SOURCE_ACQUIRED;
- ANALYSIS_PREVIEW_ACQUIRED alone may not silently advance into full-song segment selection.

This prevents an official 30-second preview from being mistaken for a full production master.
