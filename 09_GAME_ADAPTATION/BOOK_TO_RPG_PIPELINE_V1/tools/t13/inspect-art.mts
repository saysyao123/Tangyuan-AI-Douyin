import fs from 'node:fs/promises'
import path from 'node:path'
import {createServer} from 'vite'
const root=path.resolve(process.argv[2],'packages/editor')
const vite=await createServer({root,configFile:path.join(root,'vite.config.ts'),server:{middlewareMode:true},appType:'custom'})
try{
 const m=await vite.ssrLoadModule('/scripts/type_pal_t1_art.ts')
 const api=await vite.ssrLoadModule('/@fs/'+path.resolve(root,'../reforge/src/index.ts'))
 const animation=await vite.ssrLoadModule('/@fs/'+path.resolve(root,'../reforge/src/sprite-anim.ts'))
 const project=path.resolve(process.argv[4]??path.resolve(root,'../../projects/book-pilot-opening'))
 const catalog=JSON.parse(await fs.readFile(path.join(project,'assets/index.json'),'utf8')).assets
 const authored=m.previewFrames()
 for(const style of ['hero','keeper','child','guard']){
  const record=catalog['sprite.'+style],data=await fs.readFile(path.join(project,record.path))
  const decoded=await api.decodeWorldSpriteAssetBytes(record,data.buffer.slice(data.byteOffset,data.byteOffset+data.byteLength))
  const expected=authored.filter((f:any)=>f.style===style)
  if(decoded.frames.length!==12)throw Error(style+' encoded frame count')
  for(let i=0;i<12;i++){
   const a=decoded.frames[i],b=expected[i]
   if(a.width!==b.width||a.height!==b.height||[...a.opaque].some((v,k)=>v!==b.opaque[k])||[...a.pixels].some((v,k)=>a.opaque[k]&&v!==b.pixels[k]))throw Error(style+' encoded frame differs '+i)
  }
  for(const [facing,dir] of Object.entries({down:0,left:1,up:2,right:3}))for(let step=0;step<4;step++)if(animation.walkFrameIndex({kind:'directional',framesPerDir:3},facing,step,12)!==Number(dir)*3+[0,1,0,2][step])throw Error('native frame mapping differs')
 }
 await fs.writeFile(process.argv[3],JSON.stringify({encodedDecodedVerified:true,colors:m.colors,frames:authored.map((f:any)=>({...f,pixels:[...f.pixels],opaque:[...f.opaque]}))}))
 console.log('FINAL_RLE_DECODE_AND_NATIVE_FRAME_MAPPING=PASS')
}finally{await vite.close()}
