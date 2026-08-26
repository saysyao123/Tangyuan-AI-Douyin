# P1 Media Asset Identity Receipt v1

Status: **PASS / CANDIDATE / NOT YET A HARD STAGE REQUIREMENT**

Branch: `refactor/mv-runtime-consolidation-v2`

## Implemented

- `04_HARNESS/runtime/mv_media_asset_contract.json`
- `04_HARNESS/tools/mv_asset_manifest.py`
- canonical slot scaffold now includes `00_STATE/ASSETS/`
- `.github/workflows/r3-mv-runtime-p1-media-asset-tests.yml`

GitHub Actions:
- run id: `32983274121`
- job id: `98224950052`
- conclusion: `success`

## Core model

Large media bytes do not need to live in Git. Each real media object receives one immutable asset record under:

`00_STATE/ASSETS/<asset_id>.json`

The record carries:
- media type and production role;
- stage of origin;
- SHA-256 and byte size;
- durable locator/reference;
- provenance;
- parent asset IDs / derivation lineage;
- metadata;
- registration timestamp.

Acceptance is intentionally not stored by mutating the asset record. HG/Stage manifests reference immutable asset IDs instead.

## CI evidence

PASS cases:
1. canonical slot creates the immutable asset record directory;
2. local asset registration computes SHA-256 from actual bytes;
3. external media can carry durable identity even when bytes are not stored in the slot;
4. derived assets can reference already-registered parent IDs;
5. duplicate asset ID registration is blocked;
6. missing-parent derivation is blocked;
7. stage-scoped asset manifests bind shot/use meaning to immutable asset IDs;
8. duplicate manifest binding is blocked;
9. missing referenced asset is blocked;
10. later local-media byte changes are detected as SHA mismatch.

## Architectural decision

Do not use one mutable slot-wide `MEDIA_ASSET_MANIFEST.json`. A monolithic manifest would change hash every time a new image/video is created and would invalidate earlier transition snapshots.

Use immutable per-asset records plus immutable stage-scoped manifests instead.

## Promotion status

`P1_MEDIA_ASSET_IDENTITY = PASS_CANDIDATE`

This receipt validates the identity layer only. It is intentionally not yet added as a mandatory requirement to S02/S06/S08/S09/S14/S16. Hard Stage integration should happen only after Revision/Rollback semantics are defined, because replacement assets must have a controlled invalidation path.
