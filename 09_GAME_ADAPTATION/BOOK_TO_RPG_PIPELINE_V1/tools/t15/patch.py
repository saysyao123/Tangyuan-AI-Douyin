"""Enable the existing opt-in dialogue theme for the new independent content project."""
from pathlib import Path
import sys
p=Path(sys.argv[1])/'packages/reforge/src/main.ts';s=p.read_text();old="    project.manifest.id === 'book-pilot-opening', // T14_DIALOGUE_THEME";new="    ['book-pilot-opening', 'book-pilot-cinematic'].includes(project.manifest.id), // T15_DIALOGUE_THEME"
if new not in s:
 assert s.count(old)==1,'T15 theme anchor changed';s=s.replace(old,new)
p.write_text(s);print('T15_CINEMATIC_DIALOGUE_THEME_ENABLED')
