#!/usr/bin/env python3
"""Fail-closed material import for actual GPT-native art, never fallback to legacy."""
import hashlib, shutil
from pathlib import Path
THIS=Path(__file__).resolve().parent
DEST=THIS.parents[1]/'08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/assets/gpt'
SHA={
  "L01_clean.png": "b55ed043aa7b2ceb045805e175e91ed2fc69d07d5a6b30be928141b0ec950f23",
  "L04_hero.png": "e30f3dd4866d3fa72e9a84b14672ab2849c18700173e1d61e8cc58026459cb7b",
  "L07_clean.png": "bc9734bae6e79c350529ac1129addd7e44831c628102a81301ec5b25aea47d88",
  "L07_photo.png": "9bdaba8db9e28727b1d8459e5c8805e65222d33d52a0755176292e370cf85614",
  "L08_hero.png": "8c483dd2fdfe6688d9a04e8f9f9956c8ba650fea9068a876d99852c1c6c6c9cb"
}
def stage():
    # Fail before creating output directories so partial imports cannot masquerade as valid assets.
    verified=[]
    for name,expected in SHA.items():
        src=THIS/'assets/prepared'/name
        if not src.exists():raise SystemExit('FAIL_CLOSED_MISSING_GPT_ART: '+name)
        actual=hashlib.sha256(src.read_bytes()).hexdigest()
        if actual!=expected:raise SystemExit('FAIL_CLOSED_HASH_MISMATCH: '+name)
        verified.append((src,name))
    DEST.mkdir(parents=True,exist_ok=True)
    for src,name in verified: shutil.copyfile(src,DEST/name)
    fixture=DEST/'.SYNTHETIC_FIXTURE_ONLY'
    if fixture.exists(): fixture.unlink()
    print('PASS_GPT_IMAGE_IMPORT',len(SHA),'files to',DEST)
if __name__=='__main__':stage()
