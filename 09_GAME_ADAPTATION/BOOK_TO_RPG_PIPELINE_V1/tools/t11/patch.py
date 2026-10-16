"""Small, idempotent Type PAL T1.1 input/render/boot stability patch."""
from pathlib import Path
import sys,shutil
r=Path(sys.argv[1]);here=Path(__file__).parent
p=r/'packages/reforge/src/input.ts';s=p.read_text()
if 'T11_RELEASE_KEYS' not in s:
 s=s.replace("    target.addEventListener('keyup',", """    // T11_RELEASE_KEYS: OS/app focus changes can swallow keyup. Never keep a ghost input.
    const clear = () => { this.held.clear(); this.pressed.clear() }
    target.addEventListener('blur', clear)
    target.addEventListener('pagehide', clear)
    target.document?.addEventListener('visibilitychange', () => {
      if (target.document.hidden) clear()
    })
    target.addEventListener('keyup',""")
p.write_text(s)
shutil.copyfile(here/'presentation-position.ts',r/'packages/reforge/src/presentation-position.ts')
p=r/'packages/reforge/src/main.ts';s=p.read_text()
if 'T11_PRESENTATION' not in s:
 s="import { PresentationPosition } from './presentation-position.js'\n"+s
 s=s.replace('const WORLD_SCALE = 4 //',"const WORLD_SCALE = new URLSearchParams(location.search).get('quality') === 'sharp' ? 4 : 2 // T11_PRESENTATION; same 320x200 pixel art, 75% fewer backing pixels.\n  canvas.width = 320 * WORLD_SCALE; canvas.height = 200 * WORLD_SCALE\n  //")
 s=s.replace('  const cameraSession = new WorldCamera(',"  const displayPosition = new PresentationPosition(80)\n  let renderedPlayerPos = { ...player.pos }\n  const cameraSession = new WorldCamera(",1)
 s=s.replace('    () => player.pos,\n    () => activeScene.bounds,','    () => renderedPlayerPos,\n    () => activeScene.bounds,',1)
 s=s.replace('    updateCamera() // 相机跟随玩家',"""    const displayed = displayPosition.sample(activeScene.scene.id, player.pos, performance.now(),
      !runner && !menus.active && !dialogBox.active && !presentation.busy() && !motion.partyMove)
    renderedPlayerPos = displayed.pos
    updateCamera() // Camera follows the same displayed feet, while gameplay remains canonical.""",1)
 s=s.replace('player: { pos: player.pos, facing, walking, stepFrame, layer: partyLayer },','player: { pos: renderedPlayerPos, facing, walking: walking || displayed.moving, stepFrame, layer: partyLayer },',1)
 s=s.replace('      position: Object.freeze({ ...player.pos }),','      position: Object.freeze({ ...player.pos }),\n      presentationPosition: Object.freeze({ ...renderedPlayerPos }),',1)
 # Remove public world mutation/debug entry points from production; preserve read-only observer.
 s=s.replace("  ;(window as unknown as { __reforge?: unknown }).__reforge = {","  if (import.meta.env.DEV) {\n  ;(window as unknown as { __reforge?: unknown }).__reforge = {",1)
 s=s.replace("  /** 当前按下的方向键 → 朝向", "  } // end DEV-only mutable debug surface\n\n  /** 当前按下的方向键 → 朝向",1)
p.write_text(s)
p=r/'packages/reforge/src/boot.ts';s=p.read_text()
if 'dataset.bootError' not in s:s=s.replace("  console.error('[reforge]', e)","  document.documentElement.dataset.bootError = msg\n  console.error('[reforge]', e)")
p.write_text(s)
print('T11_STABILITY_PATCH_APPLIED')

# A partial adapter must fail before it can be packaged.
for relative, expected in {
 'packages/reforge/src/input.ts': ['T11_RELEASE_KEYS','this.held.clear(); this.pressed.clear()'],
 'packages/reforge/src/main.ts': ['T11_PRESENTATION','player: { pos: renderedPlayerPos','presentationPosition: Object.freeze','if (import.meta.env.DEV) {\n  ;(window as unknown as { __reforge'],
 'packages/reforge/src/boot.ts': ['dataset.bootError'],
}.items():
 text=(r/relative).read_text()
 for anchor in expected:
  if anchor not in text:raise RuntimeError('Incomplete T1.1 adapter: '+relative+' / '+anchor)
