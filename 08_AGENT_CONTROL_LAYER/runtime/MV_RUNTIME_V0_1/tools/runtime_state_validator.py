#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def load_yaml(rel):
    return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def read(rel):
    return (ROOT/rel).read_text(encoding="utf-8")

errors=[]
checks=[]

state=load_yaml("PROJECT_STATE_SCHEMA.yaml")
tracker=read("PROGRESS_TRACKER.md")
s0_contract=load_yaml("stages/00_SONG_SELECTION/S0_STAGE_CONTRACT_v0.3.yaml")
s1_contract=load_yaml("stages/01_PROJECT_AUDIO/S1_STAGE_CONTRACT_v0.4.yaml")
s0_judge=json.loads(read("stages/00_SONG_SELECTION/S0_STAGE_SEAL_JUDGE_RETEST01.json"))
s1_judge=json.loads(read("stages/01_PROJECT_AUDIO/S1_STAGE_SEAL_JUDGE_RETEST01.json"))
s0_delivery=load_yaml("stages/00_SONG_SELECTION/S0_DELIVERY_RETEST01_v0.3.yaml")
s1_delivery=load_yaml("stages/01_PROJECT_AUDIO/S1_DELIVERY_RETEST01_v0.4.yaml")

def ck(name, cond, detail=""):
    checks.append({"check":name,"pass":bool(cond),"detail":detail})
    if not cond: errors.append(name + (": "+detail if detail else ""))

ps=state["project_state"]

# State ↔ tracker
for stage_id, tracker_id in [("SONG_SELECTION","S0"),("PROJECT_AUDIO","S1"),("DIRECTOR","S2")]:
    st=ps[stage_id]["status"]
    pat=rf"\|\s*{tracker_id}\s*\|[^\n]*\|\s*{re.escape(st)}\s*\|"
    ck(f"tracker_status_{tracker_id}", bool(re.search(pat,tracker)), f"expected {st}")

# Contract versions / finality
ck("s0_contract_version", ps["SONG_SELECTION"]["contract_version"]=="0.3")
ck("s1_contract_version", ps["PROJECT_AUDIO"]["contract_version"]=="0.4")
ck("s0_contract_final", s0_contract["stage_contract"]["status"]=="FINAL")
ck("s1_contract_final", s1_contract["stage_contract"]["status"]=="FINAL")

# Delivery ↔ state
h0=s0_delivery["handoff"]
h1=s1_delivery["handoff"]
ck("s0_delivery_sealed", h0["stage"]["status"]=="SEALED")
ck("s0_delivery_contract", h0["stage"]["contract_version"]=="0.3")
ck("s0_gate_pass", h0["human_song_family_lock"]["status"]=="PASS")
ck("s1_delivery_sealed", h1["stage"]["status"]=="SEALED")
ck("s1_delivery_contract", h1["stage"]["contract_version"]=="0.4")
ck("s1_gate_pass", h1["human_audio_lock"]["status"]=="PASS")
ck("s0_judge_pass", s0_judge["route"]=="PASS")
ck("s1_judge_pass", s1_judge["route"]=="PASS")
ck("s0_judge_test_marker", s0_judge["independence"]=="NOT_FULLY_FRESH")
ck("s1_judge_test_marker", s1_judge["independence"]=="NOT_FULLY_FRESH")

# Dependency / next stage
ck("s0_state_sealed", ps["SONG_SELECTION"]["status"]=="SEALED")
ck("s1_state_sealed", ps["PROJECT_AUDIO"]["status"]=="SEALED")
ck("director_dependency", ps["DIRECTOR"]["depends_on"]==["PROJECT_AUDIO"])
ck("current_stage_director", state["project"]["current_stage"]=="DIRECTOR")

# Required refs are not stale draft refs
for sid in ["SONG_SELECTION","PROJECT_AUDIO"]:
    refs=ps[sid].get("artifact_refs",[])+ps[sid].get("evidence_refs",[])+ps[sid].get("input_handoff_refs",[])
    ck(f"no_draft_ref_{sid}", all("DRAFT" not in x.upper() for x in refs))

result={
  "validator":"MV_RUNTIME_STATE_VALIDATOR_V0_1",
  "status":"PASS" if not errors else "FAIL",
  "checks":checks,
  "errors":errors
}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
