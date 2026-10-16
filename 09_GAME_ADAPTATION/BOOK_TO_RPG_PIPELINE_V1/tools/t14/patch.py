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
