"""Install matching Playwright headless Chromium; official CfT fallback only."""
import json, os, stat, subprocess, urllib.request, zipfile
from pathlib import Path
root=Path(__file__).resolve().parent/'runtime'
try:
    result=subprocess.run(['npx','playwright','install','chromium','--only-shell'],cwd=root,timeout=180)
    fallback=result.returncode!=0
except subprocess.TimeoutExpired:
    fallback=True
if fallback:
    browsers=json.loads((root/'node_modules/playwright-core/browsers.json').read_text())['browsers']
    b=next(x for x in browsers if x['name']=='chromium-headless-shell')
    cache=Path(os.environ.get('PLAYWRIGHT_BROWSERS_PATH',str(Path.home()/'.cache/ms-playwright')))
    target=cache/f'chromium_headless_shell-{b["revision"]}';target.mkdir(parents=True,exist_ok=True)
    archive=target/'official-cft.zip'
    url=f'https://storage.googleapis.com/chrome-for-testing-public/{b["browserVersion"]}/linux64/chrome-headless-shell-linux64.zip'
    with urllib.request.urlopen(url,timeout=60) as r,archive.open('wb') as out:
        import shutil
        shutil.copyfileobj(r,out)
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            p=(target/item.filename).resolve()
            if not p.is_relative_to(target.resolve()):raise ValueError('Unsafe browser archive')
            z.extract(item,target)
            mode=item.external_attr>>16
            if mode and p.is_file():p.chmod(mode)
    archive.unlink();(target/'INSTALLATION_COMPLETE').touch()
subprocess.run(['node','doctor.mjs'],cwd=root,check=True)
