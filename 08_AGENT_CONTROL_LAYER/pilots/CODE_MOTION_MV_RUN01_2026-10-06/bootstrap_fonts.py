"""Fetch only the two licensed font assets from the pinned upstream revision."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
ROOT=Path(__file__).resolve().parent/'engine/lib/fonts'
ROOT.mkdir(parents=True,exist_ok=True)
REV='26dba25b2b495c2138848c29a2c90df356a20325'
FONTS={'NotoSansSC-500.woff': '928d841b1ec663ebce82593568cbc19749fe652f88b8ec960723b7d87b551512', 'LXGWWenKai-500.woff': '734bd187392579417ac83effe31d37b9de43c7b290bcb400800456511ed79e8f'}
for name,digest in FONTS.items():
    p=ROOT/name
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest:
        print('verified',name);continue
    url=f'https://raw.githubusercontent.com/alchaincyf/huashu-art-motion/{REV}/scripts/engine/lib/fonts/{name}'
    data=urlopen(url,timeout=60).read()
    if hashlib.sha256(data).hexdigest()!=digest:raise RuntimeError(f'font hash mismatch: {name}')
    p.write_bytes(data);print('saved',name)
