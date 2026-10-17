"""Idempotent native-input integration; never patch compiled output or synthesize held keys."""
from pathlib import Path
import sys
root=Path(sys.argv[1]);here=Path(__file__).parent;p=root/'packages/reforge/src/main.ts';s=p.read_text()
if 'T18_NATIVE_NAVIGATION' not in s:
 def replace(a,b):
  global s
  assert s.count(a)==1,('anchor',a,s.count(a));s=s.replace(a,b)
 s="import { navigationPath, nearestStandable, type NavigationStep } from './point-navigation.js'\nimport { motionTerrainSweepBlocked, motionSweepsConflict } from './entity-motion.js'\n"+s
 replace('  const keyboard = new Keyboard()','  const keyboard = new Keyboard()\n'+(here/'native.inc').read_text())
 replace('    const inputDirection = playerInputAllowed ? heldDir() : null', '    if (!playerInputAllowed || heldDir()) cancelPointNavigation()\n    const inputDirection = playerInputAllowed ? heldDir() ?? nextPointDirection() : null')
 replace('col: player.pos.col + delta.dcol,', 'col: pointGoal && pointRoute[0] ? pointRoute[0].pos.col : player.pos.col + delta.dcol,')
 replace('row: player.pos.row + delta.drow,', 'row: pointGoal && pointRoute[0] ? pointRoute[0].pos.row : player.pos.row + delta.drow,')
 replace('        allowSidestep: true,','        allowSidestep: pointGoal === null,')
 replace('      health: runtimeHealth.snapshot(),', '      health: runtimeHealth.snapshot(),\n      camera: Object.freeze({...camera}),\n      navigation: Object.freeze({active:!!pointGoal,target:pointGoal?.entityId??null,route:pointRoute.map(step=>({...step.pos}))}),')
 replace('    // debug 碰撞叠加层','    drawPointNavigation()\n    // debug 碰撞叠加层')
 replace('    commitSceneSwitch(plan, world, false, restoreActions)','    cancelPointNavigation()\n    commitSceneSwitch(plan, world, false, restoreActions)')
 anchor='    applyWorldToScene() // 实体隐现/挡路按存档世界态重放(读档不重跑 onEnter,对齐原版)'
 replace(anchor,anchor+'''
    // Only the furnished open room: recover a real saved foot trapped by a new interior prop.
    // Walls/exterior gates are excluded. No flags, currency, inventory or save bytes are rewritten.
    if (pointNavigationEnabled && activeScene.scene.id === 'home-room' && isBlockedAt(activeScene.map,player.pos)) {
      const pixel = gridToPixel(player.pos)
      if (pixel.x >= 208 && pixel.x <= 560 && pixel.y >= 144 && pixel.y <= 240) {
        const safe = nearestStandable(player.pos,pos => pointCanStep(pos,pos),pointCanStep)
        if (safe) { player.pos = safe; renderedPlayerPos = {...safe}; trail = seedFormationTrail(safe, facing); displayPosition.reset(); worldPresentation.resetMotion(); deriveFollowers(); updateCamera(); showToast('已将落在家具内的旧档位置移到旁边空地，剧情进度保留。') }
        else showToast('当前位置被家具挡住，未找到安全落点；请保留备份后反馈此存档。')
      }
    }''')
 p.write_text(s)
(root/'packages/reforge/src/point-navigation.ts').write_text((here/'navigation.ts').read_text())
print('T18_NATIVE_INPUT_READY')
