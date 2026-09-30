#!/usr/bin/env python3
import json, sys, yaml
from pathlib import Path

ROOT=Path(__file__).resolve().parent
s0=yaml.safe_load((ROOT/"S0_DELIVERY.yaml").read_text(encoding="utf-8"))["s0"]
s1=yaml.safe_load((ROOT/"S1_DELIVERY.yaml").read_text(encoding="utf-8"))["s1"]

checks=[]
errors=[]
def ck(name,cond,detail=""):
    checks.append({"check":name,"pass":bool(cond),"detail":detail})
    if not cond: errors.append(name)

ck("fresh_mode", s0.get("stage",{}).get("status")=="SEALED")
ck("s0_contract", s0.get("contract_version")=="0.3")
ck("s0_gate", s0.get("human_song_family_lock",{}).get("status")=="PASS")
ck("song_handoff_match", s0.get("selected_song_family")==s1.get("selected_song_family"))
ck("s1_contract", s1.get("contract_version")=="0.4")
ck("s1a_full_source", s1["s1a_material_acquisition"]["coverage_state"]=="FULL_SOURCE_ACQUIRED")
ck("s1b_pass", s1["s1b_source_version_verification"]["status"]=="PASS")
ck("s1c_section_pass", s1["s1c_segment_timeline_analysis"]["status"]=="PASS_SECTION_LEVEL")
ck("asr_not_promoted", s1["s1c_segment_timeline_analysis"]["lyric_timing_precision"]["line_level"]=="NOT_VERIFIED")
seg=s1["selected_production_segment"]
srcdur=float(s1["s1a_material_acquisition"]["duration_seconds"])
ck("segment_order", 0 <= float(seg["start_seconds"]) < float(seg["end_seconds"]) <= srcdur)
ck("segment_duration", abs((float(seg["end_seconds"])-float(seg["start_seconds"]))-float(seg["source_duration_seconds"])) < 0.01)
ck("s1_gate", s1["s1d_audio_lock"]["status"]=="PASS")
ck("s1_sealed", s1["stage"]["status"]=="SEALED")
ck("next_stage_director", s1["stage"]["next_stage"]=="DIRECTOR" and s1["stage"]["next_stage_allowed"] is True)

result={"validator":"FRESH_S0_S1_VALIDATOR_V0_1","status":"PASS" if not errors else "FAIL","checks":checks,"errors":errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
