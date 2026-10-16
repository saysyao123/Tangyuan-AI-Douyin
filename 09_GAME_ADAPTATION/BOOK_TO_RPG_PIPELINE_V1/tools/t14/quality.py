"""Check changed production dependency closure, not unavailable commercial-fixture tests."""
from pathlib import Path
import json,sys,subprocess
root=Path(sys.argv[1]).resolve();cfg=root/'packages/reforge/tsconfig.t14.json'
cfg.write_text(json.dumps({'extends':'./tsconfig.json','include':['src/vite-env.d.ts','src/main.ts','src/actor-presentation.ts','src/world-scene-presentation.ts']})+'\n')
try:subprocess.run(['node',str(root/'node_modules/typescript/bin/tsc'),'--noEmit','-p',str(cfg)],check=True)
finally:cfg.unlink()
print('T14_PRODUCTION_CLOSURE_TYPECHECK_PASS')
