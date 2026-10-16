"""Targeted downloaded-pilot link regression and exact effective-config packaging."""
from zipfile import ZipFile
from pathlib import Path
import sys,json
root=Path(sys.argv[1]);config=Path(sys.argv[2])
with ZipFile(root/'downloads/lantern-inn-static.zip') as z:
 html=z.read('pilot/index.html').decode()
 assert 'href="https://lantern-inn-typepal-t1.ardentfern6.chatgpt.site/downloads/lantern-inn-project.zip"' in html
 assert 'href="../downloads/' not in html
 assert not any(n.lower().endswith('.epub') for n in z.namelist())
with ZipFile(root/'downloads/corresponding-source.zip') as z:
 assert json.loads(z.read('book-rpg/pilot-config.json'))==json.loads(config.read_text())
 assert 'book-rpg/tools/t13/build.mjs' in z.namelist()
 assert not any(n.lower().endswith('.epub') for n in z.namelist())
print('PILOT_DOWNLOAD_LINK_EFFECTIVE_CONFIG_NO_EPUB=PASS')
