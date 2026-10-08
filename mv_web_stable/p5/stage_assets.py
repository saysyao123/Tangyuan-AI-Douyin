#!/usr/bin/env python3
"""P5 production GPT asset import. Accept verified individual PNGs OR one complete upload ZIP.
Fail closed on missing art, wrong digest, ZipSlip, extra entry, or synthetic fixture contamination.
"""
import hashlib,json,shutil
from pathlib import Path
from zipfile import ZipFile,BadZipFile
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
DEST=REPO/'08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/assets/gpt'
ZIP=HERE/'assets/GPT_NATIVE_ANCHORS_UPLOAD.zip'
EXPECTED=json.loads((HERE/'prepared_assets_expected_sha.json').read_text(encoding='utf-8'))
def verify(name,data):
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):raise SystemExit('FAIL_CLOSED_NOT_PNG: '+name)
    actual=hashlib.sha256(data).hexdigest()
    if actual!=EXPECTED[name]:raise SystemExit('FAIL_CLOSED_HASH_MISMATCH: '+name)
    if len(data)>12_000_000:raise SystemExit('FAIL_CLOSED_UNEXPECTED_IMAGE_SIZE: '+name)
    return data
def stage():
    contents={}
    if ZIP.is_file():
        try:
            with ZipFile(ZIP,'r') as z:
                allowed=set(EXPECTED)|{'UPLOAD_MANIFEST.json'}
                members=z.namelist()
                if len(set(members))!=len(members) or set(members)!=allowed:
                    raise SystemExit('FAIL_CLOSED_ZIP_ENTRIES: expected 5 PNG + manifest; no extras')
                manifest=json.loads(z.read('UPLOAD_MANIFEST.json').decode('utf-8'))
                if manifest.get('audio_included') is not False:
                    raise SystemExit('FAIL_CLOSED_AUDIO_MUST_NOT_BE_IN_PUBLIC_ASSET')
                for name in EXPECTED:
                    if manifest['items'][name]['sha256']!=EXPECTED[name]:
                        raise SystemExit('FAIL_CLOSED_MANIFEST_MISMATCH: '+name)
                    contents[name]=verify(name,z.read(name))
        except BadZipFile as exc: raise SystemExit('FAIL_CLOSED_INVALID_ZIP '+str(exc))
        provenance='UPLOADED_SINGLE_ZIP'
    else:
        for name in EXPECTED:
            f=HERE/'assets/prepared'/name
            if not f.is_file():raise SystemExit('FAIL_CLOSED_MISSING_GPT_ART: '+str(f))
            contents[name]=verify(name,f.read_bytes())
        provenance='INDIVIDUAL_PNG_FILES'
    DEST.mkdir(parents=True,exist_ok=True)
    fixture=DEST/'.SYNTHETIC_FIXTURE_ONLY'
    if fixture.exists():fixture.unlink()
    for name,data in contents.items():(DEST/name).write_bytes(data)
    print('PASS_GPT_PRODUCTION_ASSETS',len(contents),provenance,DEST,flush=True)
if __name__=='__main__':stage()
