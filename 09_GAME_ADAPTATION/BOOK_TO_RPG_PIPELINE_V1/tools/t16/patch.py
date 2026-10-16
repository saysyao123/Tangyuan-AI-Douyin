"""Read-only native observations for the second-act shell and deterministic input QA."""
from pathlib import Path
import sys
p=Path(sys.argv[1])/'packages/reforge/src/main.ts';s=p.read_text()
if 'T16_READONLY_PROGRESS' not in s:
 old='flags: {...canonicalScript.flags}, inventory:'
 assert s.count(old)==1,'T16 story observation anchor'
 s=s.replace(old,'flags: {...canonicalScript.flags}, vars: {...canonicalScript.vars}, inventory:')
 old='\n      menuActive: menus.active,'
 assert s.count(old)==1,'T16 modal observation anchor'
 s=s.replace(old,"\n      // T16_READONLY_PROGRESS: no input or gameplay mutation.\n      confirmation: scriptConfirmModal.view ? {selectedYes:scriptConfirmModal.view.selectedYes,presentedFrames:scriptConfirmModal.view.presentedFrames} : null,\n"+old)
 p.write_text(s)
print('T16_READONLY_PROGRESS_OBSERVER_READY')
