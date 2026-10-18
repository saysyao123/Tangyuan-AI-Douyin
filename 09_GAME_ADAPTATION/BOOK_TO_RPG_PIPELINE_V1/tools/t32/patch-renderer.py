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
shutil.copy2(here/'room-world.ts',pkg/'room-world.ts')
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
patch('render-scene.ts',"import type { IsometricMapContent } from '@type-pal/content'","import type { IsometricMapContent } from '@type-pal/content'\nimport { renderHDGround, enhanceSprites, firstActReady, roomView, renderHDForeground } from './hd-world.js'")
patch('render-scene.ts',"  layers?: import('./render.js').RenderLayerOpts\n","  layers?: import('./render.js').RenderLayerOpts\n  sceneId?: string\n")
patch('render-scene.ts','  renderer.renderScene(map, room, camera, sprites, layers)\n','''  if (args.sceneId && !layers && firstActReady(args.sceneId)) {
    const view = args.sceneId === 'home-room' ? roomView() : {scale: 1, camera}
    ctx.scale(view.scale, view.scale)
    renderer.renderScene(map, room, view.camera, [], {skipCover: true})
    renderHDGround(ctx, args.sceneId, map, room, view.camera)
    renderer.renderScene(map, room, view.camera, enhanceSprites(args.sceneId, sprites), {skipBase: true})
    renderHDForeground(ctx, args.sceneId, view.camera)
  } else renderer.renderScene(map, room, camera, sprites, layers)
''')
print('T32_DISPLAY_ONLY_PATCH_APPLIED')

# First-act high-density portraits are display overrides; content assets and
# dialogue cues stay byte-identical, and the original image remains fallback.
patch('dialog/dialog-box.ts',"import { advanceCue, type DialogueState } from '../dialogue.js'", "import { advanceCue, type DialogueState } from '../dialogue.js'\nimport { firstActPortrait } from '../hd-world.js'")
patch('dialog/dialog-box.ts', '''      const px = pos.portrait.x - portraitImg.width / 2
      const py = pos.portrait.y - portraitImg.height / 2
      this.ctx.drawImage(portraitImg, px, py)''', '''      const hd = cue?.portrait ? firstActPortrait(cue.portrait.asset) : undefined
      const width = hd ? 64 : portraitImg.width
      const height = hd ? 72 : portraitImg.height
      const px = pos.portrait.x - width / 2
      const py = pos.portrait.y - height / 2
      if (hd) {
        this.ctx.save()
        this.ctx.imageSmoothingEnabled = true
        this.ctx.drawImage(hd, px, py, width, height)
        this.ctx.restore()
      } else this.ctx.drawImage(portraitImg, px, py)''')

# Preserve 320x200 logic and native coordinates, increase only physical paint density.
p=pkg/'main.ts';s=p.read_text();anchor="const WORLD_SCALE = new URLSearchParams(location.search).get('quality') === 'sharp' ? 4 : 2";assert anchor in s;s=s.replace(anchor,'const WORLD_SCALE = 4');p.write_text(s)

# Uniform room overview and its inverse are presentation only; native coordinates,
# motion writers, legal cells, opaque hit masks and keyboard commands are unchanged.
patch('main.ts', "import { PresentationPosition } from './presentation-position.js'", "import { PresentationPosition } from './presentation-position.js'\nimport { artScreenPoint, artWorldPoint } from './hd-world.js'")
patch('main.ts', "return {x:(event.clientX-rect.left)*320/rect.width+camera.x,y:(event.clientY-rect.top)*200/rect.height+camera.y}", "return artWorldPoint(activeScene.scene.id,camera,(event.clientX-rect.left)*320/rect.width,(event.clientY-rect.top)*200/rect.height)")
patch('main.ts', "const p = gridToPixel(e.pos), x=p.x-camera.x, y=p.y-camera.y+5", "const p = gridToPixel(e.pos), screen=artScreenPoint(activeScene.scene.id,camera,p.x,p.y+5), x=screen.x, y=screen.y")
patch('main.ts', "const p=gridToPixel(step.pos);ctx.fillStyle='#e7bd7970';ctx.fillRect(Math.round(p.x-camera.x),Math.round(p.y-camera.y),2,1)", "const p=gridToPixel(step.pos), screen=artScreenPoint(activeScene.scene.id,camera,p.x,p.y);ctx.fillStyle='#e7bd7970';ctx.fillRect(Math.round(screen.x),Math.round(screen.y),2,1)")
patch('main.ts', "ctx.strokeStyle='#efca86';ctx.beginPath();ctx.ellipse(p.x-camera.x,p.y-camera.y,5,2.5,0,0,Math.PI*2);ctx.stroke()", "const screen=artScreenPoint(activeScene.scene.id,camera,p.x,p.y);ctx.strokeStyle='#efca86';ctx.beginPath();ctx.ellipse(screen.x,screen.y,5,2.5,0,0,Math.PI*2);ctx.stroke()")
