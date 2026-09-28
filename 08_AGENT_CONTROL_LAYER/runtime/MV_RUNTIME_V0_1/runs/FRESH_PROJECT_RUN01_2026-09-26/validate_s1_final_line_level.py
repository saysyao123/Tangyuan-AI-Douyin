#!/usr/bin/env python3
import json,sys,yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parent
d=yaml.safe_load((ROOT/"S1_DELIVERY_FINAL_LINE_LEVEL.yaml").read_text(encoding="utf-8"))["s1"]
errors=[]; checks=[]
def ck(name,cond):
    checks.append({"check":name,"pass":bool(cond)})
    if not cond: errors.append(name)
a=d["s1c_timeline"]["selected_segment_alignment"]
lines=a["line_timings"]
ck("s1a_full_source", d["s1a_material_acquisition"]["coverage_state"]=="FULL_SOURCE_ACQUIRED")
ck("trusted_lyrics_28", d["s1b_source_version_verification"]["trusted_lyrics_line_count"]==28)
ck("global_defect_explicit", d["s1c_timeline"]["overall_alignment"]["status"]=="PARTIAL_LOW_CONFIDENCE")
ck("selected_status", a["status"]=="PASS_LINE_LEVEL_SELECTED_SEGMENT")
ck("eight_lines", len(lines)==8 and [x["line_id"] for x in lines]==list(range(21,29)))
ck("monotonic", all(lines[i]["start"]>=lines[i-1]["end"]-0.05 for i in range(1,len(lines))))
ck("durations", max(x["end"]-x["start"] for x in lines)<=8.0)
ck("segment_bounds", abs(lines[0]["start"]-a["source_start_seconds"])<0.001 and abs(lines[-1]["end"]-a["source_end_seconds"])<0.001)
p=d["selected_production_segment"]
ck("handles", p["render_start_seconds"]<p["lyric_source_start_seconds"] and p["render_end_seconds"]>p["lyric_source_end_seconds"])
ck("expected_duration", abs((p["render_end_seconds"]-p["render_start_seconds"])-p["expected_render_duration_seconds"])<0.002)
ck("audio_lock", d["s1d_audio_lock"]["status"]=="PASS")
ck("sealed", d["stage"]["status"]=="SEALED" and d["stage"]["next_stage"]=="DIRECTOR")
result={"validator":"S1_SELECTED_SEGMENT_LINE_LEVEL_VALIDATOR_V0_1","status":"PASS" if not errors else "FAIL","checks":checks,"errors":errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
