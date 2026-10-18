"""Display-only patch on the pinned upstream plus previously shipped T18 sources.
No map, script, collision, SAVE12 or native input changes.
"""
from pathlib import Path
import sys,shutil
root=Path(sys.argv[1]).resolve(); here=Path(__file__).resolve().parent
pkg=root/'packages/reforge/src'
def patch(name,a,b):
 p=pkg/name;s=p.read_text();assert s.count(a)==1,(name,a[:80],s.count(a));p.write_text(s.replace(a,b))
shutil.copy2(here/'hd-world.ts',pkg/'hd-world.ts')
patch('render.ts','export interface SpriteDraw {\n  frame: RleFrame','''export interface SpriteDraw {
  /** T32 visual metadata; never persisted or used by simulation/hit testing. */
  artId?: string
  artKey?: string
  artFrame?: number
  artFacing?: string
  drawHD?: (ctx: CanvasRenderingContext2D, camera: Camera) => void
  frame: RleFrame''')
patch('render.ts',"            : () => this.ctx.drawImage(image, x, y),","            : sprite.drawHD ? () => sprite.drawHD!(this.ctx, camera) : () => this.ctx.drawImage(image, x, y),")
patch('world-scene-presentation.ts',"  'map' | 'room' | 'palette' | 'tiles' | 'renderer' | 'rendererForWave'\n>","  'map' | 'room' | 'palette' | 'tiles' | 'renderer' | 'rendererForWave'\n> & Partial<Pick<ActiveScene<Renderer>, 'scene'>>")
patch('world-scene-presentation.ts','      sprites.push({\n        frame,\n        worldX: pixel.x,','''      sprites.push({
        artId: entity.id, artKey: definition?.id, artFrame: frameIndex, artFacing: entity.facing,
        frame,
        worldX: pixel.x,''')
patch('world-scene-presentation.ts','sprites.push(partySprite(leaderFrame, input.player.pos, pixel, input.player.layer, 0, true))','sprites.push({...partySprite(leaderFrame, input.player.pos, pixel, input.player.layer, 0, true), artKey: leaderDefinition.id, artFrame: leaderFrameIndex, artFacing: input.player.facing})')
patch('world-scene-presentation.ts','''        partySprite(
          frame,
          displayed.pos,
          gridToPixel(displayed.pos),
          input.player.layer,
          partyIndex,
          true,
        ),''','''        {...partySprite(
          frame, displayed.pos, gridToPixel(displayed.pos), input.player.layer, partyIndex, true,
        ), artKey: visual.def.id, artFrame: frameIndex, artFacing: follower.facing},''')
patch('world-scene-presentation.ts','        sprites: input.sprites,\n        worldScale: this.host.worldScale,\n','        sprites: input.sprites,\n        worldScale: this.host.worldScale,\n        sceneId: input.scene.scene?.id,\n')
patch('render-scene.ts',"import type { IsometricMapContent } from '@type-pal/content'","import type { IsometricMapContent } from '@type-pal/content'\nimport { renderHDGround, enhanceSprites, firstActReady } from './hd-world.js'")
patch('render-scene.ts',"  layers?: import('./render.js').RenderLayerOpts\n","  layers?: import('./render.js').RenderLayerOpts\n  sceneId?: string\n")
patch('render-scene.ts','  renderer.renderScene(map, room, camera, sprites, layers)\n','''  if (args.sceneId && !layers && firstActReady(args.sceneId)) {
    renderer.renderScene(map, room, camera, [], {skipCover: true})
    renderHDGround(ctx, args.sceneId, map, room, camera)
    renderer.renderScene(map, room, camera, enhanceSprites(args.sceneId, sprites), {skipBase: true})
  } else renderer.renderScene(map, room, camera, sprites, layers)
''')
print('T32_DISPLAY_ONLY_PATCH_APPLIED')

# Preserve 320x200 logic and native coordinates, increase only physical paint density.
p=pkg/'main.ts';s=p.read_text();anchor="const WORLD_SCALE = new URLSearchParams(location.search).get('quality') === 'sharp' ? 4 : 2";assert anchor in s;s=s.replace(anchor,'const WORLD_SCALE = 4');p.write_text(s)
