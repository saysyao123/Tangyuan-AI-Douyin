"""Pinned presentation adapter: all moving native followers/NPCs, no gameplay writes."""
from pathlib import Path
import sys,shutil
root=Path(sys.argv[1]);here=Path(__file__).parent
shutil.copyfile(here/'actor-presentation.ts',root/'packages/reforge/src/actor-presentation.ts')
p=root/'packages/reforge/src/world-scene-presentation.ts';s=p.read_text()
def once(old,new):
 global s
 if s.count(old)!=1:raise RuntimeError('T14 anchor mismatch: '+old[:100])
 s=s.replace(old,new,1)
if 'T14_ACTOR_PRESENTATION' not in s:
 s="import { ActorPresentation } from './actor-presentation.js' // T14_ACTOR_PRESENTATION\n"+s
 once('  private gesture: number | null = null','  private readonly actorPresentation = new ActorPresentation(80)\n  private lastPartyStep = 0\n  resetMotion(): void { this.actorPresentation.reset() }\n  motionSnapshot() { return this.actorPresentation.snapshot() }\n  private gesture: number | null = null')
 once('    const sprites: SpriteDraw[] = []','    const sprites: SpriteDraw[] = []\n    this.actorPresentation.begin()\n    if (input.player.walking) this.lastPartyStep = input.player.stepFrame')
 once('      const gait = input.entityGait(entity.id)',"      const motionKey = 'entity:' + entity.id\n      const displayed = this.actorPresentation.sample(motionKey, entity.pos, input.now(), input.entityGait(entity.id) !== undefined)\n      const gait = this.actorPresentation.phase(motionKey, input.entityGait(entity.id), displayed.moving)")
 once('      const pixel = gridToPixel(entity.pos)','      const pixel = gridToPixel(displayed.pos)\n      this.actorPresentation.record(motionKey, entity.pos, displayed.pos, displayed.moving, frameIndex)')
 once('        worldY: spriteScreenY(entity.pos),','        worldY: spriteScreenY(displayed.pos),')
 once('      if (!follower || !visual) continue\n      const frameIndex = input.player.walking\n        ? walkFrameIndex(',"      if (!follower || !visual) continue\n      const motionKey = 'party:' + expectDefined(member).id\n      const displayed = this.actorPresentation.sample(motionKey, follower.pos, input.now())\n      const moving = input.player.walking || displayed.moving\n      const frameIndex = moving\n        ? walkFrameIndex(")
 # Only follower branch uses the cached last walking phase after the leader settles.
 once('            follower.facing,\n            input.player.stepFrame,\n            visual.frames.frames.length,','            follower.facing,\n            input.player.walking ? input.player.stepFrame : this.lastPartyStep,\n            visual.frames.frames.length,')
 once('      sprites.push(\n        partySprite(\n          frame,\n          follower.pos,\n          gridToPixel(follower.pos),\n          input.player.layer,\n          partyIndex,\n          true,', '      this.actorPresentation.record(motionKey, follower.pos, displayed.pos, moving, frameIndex)\n      sprites.push(\n        partySprite(\n          frame,\n          displayed.pos,\n          gridToPixel(displayed.pos),\n          input.player.layer,\n          partyIndex,\n          true,')
 once('    return sprites','    this.actorPresentation.end()\n    return sprites')
s=s.replace('entity.pos, input.now())','entity.pos, input.now(), input.entityGait(entity.id) !== undefined)')
p.write_text(s)
p=root/'packages/reforge/src/main.ts';s=p.read_text()
if 'T14_MOTION_OBSERVER' not in s:
 if s.count('displayPosition.reset()')!=2:raise RuntimeError('T14 expected scene/teleport reset anchors')
 s=s.replace('displayPosition.reset()','displayPosition.reset(); worldPresentation.resetMotion()')
 anchor='      presentationPosition: Object.freeze({ ...renderedPlayerPos }),'
 if s.count(anchor)!=1:raise RuntimeError('T14 observer anchor')
 s=s.replace(anchor,anchor+'\n      actors: worldPresentation.motionSnapshot(), // T14_MOTION_OBSERVER')
p.write_text(s)
print('T14_DISPLAY_ONLY_MOTION_PATCH_APPLIED')

# Optional pilot theme: keep native PAL dialogue style untouched for other projects.
p=root/'packages/reforge/src/dialog/dialog-box.ts';s=p.read_text()
if 'T14_FRAMED_DIALOGUE' not in s:
 def change(old,new):
  global s
  if s.count(old)!=1:raise RuntimeError('T14 dialogue anchor: '+old[:80])
  s=s.replace(old,new,1)
 change('    private readonly scroll?: BoxTiles,','    private readonly scroll?: BoxTiles,\n    private readonly framed = false, // T14_FRAMED_DIALOGUE')
 change('    const maxRight = MAX_RIGHT',"    const maxRight = this.framed ? (hasPortrait && slot === 'bottom' ? 232 : 304) : MAX_RIGHT")
 change('    // 该段话的头像(若有):spec §3 位置,bottom 右 / top 左。',"""    if (this.framed && (slotId === 'bottom' || slotId === 'top')) {
      const y = slotId === 'bottom' ? 102 : 2
      this.ctx.save()
      this.ctx.fillStyle = '#172630'
      this.ctx.fillRect(2, y, 316, 94)
      this.ctx.strokeStyle = '#b9a582'
      this.ctx.strokeRect(3.5, y + 1.5, 313, 91)
      this.ctx.restore()
    }
    // 该段话的头像(若有):spec §3 位置,bottom 右 / top 左。""")
 change('        maxChars: limit,',"        maxChars: limit,\n        ...(this.framed ? { forceRgba: [239, 233, 213] as [number, number, number] } : {}),")
 p.write_text(s)
p=root/'packages/reforge/src/main.ts';s=p.read_text()
if 'T14_DIALOGUE_THEME' not in s:
 old='    menuAssets.scroll,\n  )'
 if s.count(old)!=1:raise RuntimeError('T14 dialogue constructor anchor')
 s=s.replace(old,old.replace('\n  )',"\n    project.manifest.id === 'book-pilot-opening', // T14_DIALOGUE_THEME\n  )"))
 p.write_text(s)
