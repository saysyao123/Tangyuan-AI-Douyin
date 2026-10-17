#!/usr/bin/env python3
"""Copy T23 exact game webpage, only inject a presentation probe in iframe."""
import shutil,sys,hashlib
from pathlib import Path
src,dst=[Path(x).resolve() for x in sys.argv[1:3]]
book=Path(__file__).resolve().parents[2]
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
p=dst/'chapter/game/index.html'
s=p.read_text()
assert s.count('</body>')==1 and 't24-ambient' not in s
p.write_text(s.replace('</body>','<script defer src="./t24-ambient.js"></script>\\n</body>'))
shutil.copy2(book/'tools/t24/ambient-highdpi-probe.js',dst/'chapter/game/t24-ambient.js')
# original T23 shell and game project data must be byte-identical
for f in ['chapter/index.html','chapter/style.css','chapter/shell.js','chapter/config.js','night/index.html','chapter/game/projects/book-pilot-cinematic/content/scenes/fair.json']:
 a,b=src/f,dst/f
 assert hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest(),f
print('T24_HIGH_DPI_ISOLATED_RENDER_PROBE_READY; all story, collision and shell bytes unchanged')
