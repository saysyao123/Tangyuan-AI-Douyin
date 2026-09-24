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
