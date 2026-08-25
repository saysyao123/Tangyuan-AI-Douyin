#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("06_TESTS/MV/WEB_R3/30D_60/D02-A")
REPORT = ROOT / "BGM_DISCOVERY" / "asset_probe_report.json"
MANIFEST = ROOT / "_hg02_audio_artifact" / "manifest.json"


def main() -> int:
    payload = json.loads(REPORT.read_text(encoding="utf-8"))
    works = payload.get("works") or []
    hashes = []
    for work in works:
        info = (work or {}).get("direct_music_asset") or {}
        h = info.get("sha256") if isinstance(info, dict) else None
        hashes.append(h)

    exact_content = bool(len(hashes) >= 2 and all(hashes) and len(set(hashes)) == 1)
    payload["direct_music_asset_hashes"] = hashes
    payload["exact_asset_content_identity"] = exact_content

    if exact_content:
        payload["asset_id_visibility"] = "UNAVAILABLE_FROM_OPAQUE_SIGNED_URL"
        payload["decision"] = "EXACT_ASSET_CONTENT_IDENTITY_CONFIRMED"
        payload["classification_note"] = (
            "Numeric music asset id is not exposed by the current signed Douyin URL format, "
            "but both independent works resolve to byte-identical direct music assets."
        )

    REPORT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        manifest["decision"] = payload.get("decision")
        manifest["exact_asset_content_identity"] = exact_content
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "decision": payload.get("decision"),
        "exact_asset_content_identity": exact_content,
        "direct_hashes": hashes,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
