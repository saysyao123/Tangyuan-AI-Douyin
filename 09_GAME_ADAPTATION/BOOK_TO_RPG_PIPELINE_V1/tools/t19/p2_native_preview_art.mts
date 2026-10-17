/** T19 P2 standalone preview-only sprite bundle. Does not touch scenes or actor IDs. */
import fs from 'node:fs/promises'
import {compressGzip,encodeSpriteChunk} from '@type-pal/reforge'
type F={width:number;height:number;pixels:string;opaque:string}
export async function t19DraftSprites(packPath:string):Promise<Record<string,Buffer>>{
 const p=JSON.parse(await fs.readFile(packPath,'utf8')) as {sprites:Record<string,F[]>}
 const out:Record<string,Buffer>={}
 for(const [role,w,h] of [['adult',36,56],['child',32,44]] as const){
  const src=p.sprites?.[role]
  if(src?.length!==12)throw Error('T19 preview frames must be SW/NW/NE/SE × 3')
  const frames=src.map((f,i)=>{
   if(f.width!==w||f.height!==h)throw Error('T19 frame dimension '+role+'/'+i)
   const pixels=Uint8Array.from(Buffer.from(f.pixels,'base64'))
   const opaque=Uint8Array.from(Buffer.from(f.opaque,'base64'))
   if(pixels.length!==w*h||opaque.length!==w*h)throw Error('T19 frame byte count')
   for(let j=0;j<pixels.length;j++)if(opaque[j]!==Number(pixels[j]!==255))throw Error('T19 alpha mask')
   return {width:w,height:h,pixels,opaque}
  })
  out['t19-preview-'+role]=Buffer.from(await compressGzip(encodeSpriteChunk(frames)))
 }
 return out
}
