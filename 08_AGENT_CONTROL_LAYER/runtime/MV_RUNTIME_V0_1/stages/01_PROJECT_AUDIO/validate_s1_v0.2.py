#!/usr/bin/env python3
import json, sys
from pathlib import Path

TOL = 0.001

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "S1_TEST_INPUT_RUN02_v0.2.json"
    x = json.loads(Path(path).read_text(encoding="utf-8"))
    checks = {}
    checks["D01_segment_order"] = x["segment_end_seconds"] > x["segment_start_seconds"]
    derived = x["segment_end_seconds"] - x["segment_start_seconds"]
    checks["D02_duration_match"] = abs(derived - x["locked_duration_seconds"]) <= TOL
    checks["D03_audio_version_present"] = bool(x["selected_audio_version_ref"].strip())
    units = x.get("timeline_units") or []
    checks["D04_timeline_bounds"] = bool(units) and abs(units[0]["start"] - x["segment_start_seconds"]) <= TOL and abs(units[-1]["end"] - x["segment_end_seconds"]) <= TOL
    ordered = True
    contiguous = True
    for i, u in enumerate(units):
        ordered &= u["end"] > u["start"]
        if i:
            contiguous &= abs(u["start"] - units[i-1]["end"]) <= TOL
    checks["D05_timeline_order_and_continuity"] = bool(units) and ordered and contiguous
    checks["D06_human_lock"] = x.get("human_audio_lock",{}).get("status") == "PASS"
    out = {
      "pass": all(checks.values()),
      "tolerance_seconds": TOL,
      "derived_duration_seconds": derived,
      "checks": checks
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out["pass"] else 1)

if __name__ == "__main__":
    main()
