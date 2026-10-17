#!/usr/bin/env python3
"""Adds an optional guide to an *existing* T22 restored site. All game files, shell.js,
config.js, SAVE12 and both chapter/night native runtimes remain byte-for-byte untouched."""
from pathlib import Path
import hashlib, shutil, sys
src=Path(sys.argv[1]).resolve()
dst=Path(sys.argv[2]).resolve()
book=Path(__file__).resolve().parents[2]
assert (src/'chapter/index.html').exists()
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)
target=dst/'chapter'
html=target/'index.html'
markup=html.read_text(encoding='utf-8')
assert markup.count('</body>')==1
assert 'journey-guide.js' not in markup
markup=markup.replace('</body>', '<script src="journey-guide.js"></script>\n</body>')
html.write_text(markup,encoding='utf-8')
shutil.copy2(book/'tools/t23/journey-guide.js',target/'journey-guide.js')
css=target/'style.css'
css.write_text(css.read_text(encoding='utf-8')+'\n'+'''/* T23_JRPG_OPT_IN_GUIDE — no changes to original shell layout */
.t23-guide{margin-top:11px;border-top:1px solid #65543d;padding-top:10px}
.t23-guide-button{font:inherit;font-size:12px;letter-spacing:.02em;border:1px solid #88704f;color:#dec6a2;background:transparent;padding:6px 11px;border-radius:3px;cursor:pointer}
.t23-guide-button:hover,.t23-guide-button:focus-visible{background:#403a2e;outline:1px solid #c7a770}
.t23-guide p{color:#cabda5;font-size:12px;line-height:1.8;margin:9px 0 0}
.t23-guide-marker{position:fixed;width:16px;height:16px;border:2px solid #f9d68b;border-radius:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:9999;box-shadow:0 0 0 3px #291f19aa,0 0 12px #f9cd65a8;animation:t23-guide-breathe 1.2s ease-in-out infinite}
.t23-guide-marker[hidden]{display:none}
@keyframes t23-guide-breathe{50%{opacity:.55;scale:1.13}}
@media(prefers-reduced-motion:reduce){.t23-guide-marker{animation:none}}
''',encoding='utf-8')
for rel in [
 'chapter/shell.js','chapter/config.js','chapter/game/index.html',
 'night/index.html','night/style.css','night/shell.js','pilot/index.html']:
 a,b=src/rel,dst/rel
 if a.exists() and b.exists():
  assert hashlib.sha256(a.read_bytes()).digest()==hashlib.sha256(b.read_bytes()).digest(),rel
changed=[]
for f in src.rglob('*'):
 if not f.is_file():continue
 g=dst/f.relative_to(src)
 if not g.is_file() or f.read_bytes()!=g.read_bytes():changed.append(f.relative_to(src).as_posix())
assert changed==['chapter/index.html','chapter/style.css'],changed
print('T23_T22_ORIGINAL_SHELL_PRESERVED; Only chapter HTML/CSS additive changes; native game unchanged.')
