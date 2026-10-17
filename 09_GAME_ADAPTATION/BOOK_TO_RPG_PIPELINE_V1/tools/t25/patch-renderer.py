#!/usr/bin/env python3
"""Patch the pinned Type PAL source only inside T25 CI checkout.
No mutation of upstream repository, user Site, or saved-game payload.
"""
from pathlib import Path
import sys,shutil
root=Path(sys.argv[1]).resolve()
book=Path(__file__).resolve().parents[2]
pkg=root/'packages/reforge/src'
assert (pkg/'render-scene.ts').exists()
shutil.copy2(book/'tools/t25/hd-world.ts',pkg/'hd-world.ts')
p=pkg/'render.ts';s=p.read_text()
anchor="export interface SpriteDraw {\n  frame: RleFrame"
assert s.count(anchor)==1
s=s.replace(anchor,"export interface SpriteDraw {\n  /** Stable entity art anchor for optional original high-DPI scenery substitution. */\n  artId?: string\n  frame: RleFrame")
p.write_text(s)
p=pkg/'world-scene-presentation.ts';s=p.read_text()
anchor="  'map' | 'room' | 'palette' | 'tiles' | 'renderer' | 'rendererForWave'\n"
assert s.count(anchor)==1
s=s.replace(anchor,"  'scene' | 'map' | 'room' | 'palette' | 'tiles' | 'renderer' | 'rendererForWave'\n")
anchor="      sprites.push({\n        frame,\n        worldX: pixel.x,"
assert s.count(anchor)==1
s=s.replace(anchor,"      sprites.push({\n        artId: entity.id,\n        frame,\n        worldX: pixel.x,")
anchor="        sprites: input.sprites,\n        worldScale: this.host.worldScale,\n"
assert s.count(anchor)==1
s=s.replace(anchor,"        sprites: input.sprites,\n        worldScale: this.host.worldScale,\n        sceneId: input.scene.scene.id,\n        entities: input.scene.scene.entities,\n")
p.write_text(s)
p=pkg/'render-scene.ts';s=p.read_text()
anchor="import type { IsometricMapContent } from '@type-pal/content'"
assert s.count(anchor)==1
s=s.replace(anchor,"import type { IsometricMapContent, EntityDef } from '@type-pal/content'\nimport { projectMapTilesInView } from './project-map.js'\nimport {renderDetailedFirstAct, replacesNativeSprite} from './hd-world.js'")
anchor="  layers?: import('./render.js').RenderLayerOpts\n"
assert s.count(anchor)==1
s=s.replace(anchor,"  layers?: import('./render.js').RenderLayerOpts\n  /** Optional first-act architecture. No game logic or Save schema affected. */\n  sceneId?: string\n  entities?: readonly EntityDef[]\n")
anchor="  renderer.renderScene(map, room, camera, sprites, layers)\n"
assert s.count(anchor)==1
s=s.replace(anchor,'''  if (args.sceneId && args.entities && !layers) {
    // Original game painter still owns tiles and depth-sorted actors. The
    // high-DPI pass only improves authored environment layers, and does not
    // change input targeting / collision / dialogue / cutscene sequencing.
    renderer.renderScene(map, room, camera, [], {skipCover: true})
    renderDetailedFirstAct(ctx, args.sceneId, camera, args.entities,
      projectMapTilesInView(map, room, new Set()))
    renderer.renderScene(map, room, camera,
      sprites.filter(sprite => !sprite.artId || !replacesNativeSprite(args.sceneId!, sprite.artId)),
      {skipBase: true})
  } else {
    renderer.renderScene(map, room, camera, sprites, layers)
  }
''')
p.write_text(s)
p=pkg/'hd-world.ts';s=p.read_text()
s=s.replace("polygon(ctx,p,color(...base),'#2d2422',4)","polygon(ctx,p,color(base[0]!,base[1]!,base[2]!),'#2d2422',4)")
p.write_text(s)
print('T25_RENDERER_PATCH_DONE')
