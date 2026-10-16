/* Original GPT standing art, authored native walk rig, and deterministic winter ground. GPL-3.0. */
import fs from 'node:fs/promises'
import {compressGzip,encodeSpriteChunk} from '@type-pal/reforge'
import {buildOriginalArt} from './type_pal_t1_art.ts'
type F={width:number;height:number;pixels:Uint8Array;opaque:Uint8Array}
async function gz(frames:F[]){const b=await compressGzip(encodeSpriteChunk(frames));return b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength)}
export async function buildPolishedArt(packFile:string){
 const pack=JSON.parse(await fs.readFile(packFile,'utf8')),art:any=await buildOriginalArt()
 art.palette={colors:pack.palette,cycles:[]}
 const decode=(f:any):F=>({...f,pixels:Uint8Array.from(Buffer.from(f.pixels,'base64')),opaque:Uint8Array.from(Buffer.from(f.opaque,'base64'))})
 const rig=(src:F,dir:number,phase:number):F=>{
  if(!phase)return src
  const f:F={...src,pixels:new Uint8Array(src.pixels.length),opaque:new Uint8Array(src.opaque.length)}
  const hip=Math.floor(src.height*.69),centre=src.width/2,sign=phase===1?1:-1
  for(let y=0;y<src.height;y++)for(let x=0;x<src.width;x++){
   const i=y*src.width+x;if(!src.opaque[i])continue
   let dx=0,dy=0
   if(y>=hip){const t=(y-hip)/(src.height-hip),leg=x<centre?-1:1;dx=Math.round(sign*leg*t*2);dy=Math.round(sign*leg*t*(dir===0||dir===3?1:-1))}
   else if(y>src.height*.43&&(x<src.width*.28||x>src.width*.72)){dy=sign*(x<centre?1:-1)}
   const xx=x+dx,yy=y+dy;if(xx>=0&&xx<src.width&&yy>=0&&yy<src.height){f.pixels[yy*src.width+xx]=src.pixels[i];f.opaque[yy*src.width+xx]=1}
  }
  return f
 }
 for(const [id,raw] of Object.entries(pack.sprites)){
  const frames=(raw as any[]).map(decode)
  art[id]=await gz(['hero','child'].includes(id)?frames.flatMap((f,dir)=>[0,1,2].map(phase=>rig(f,dir,phase))):frames)
 }
 // Native ISO tiles: seamless staggered cobbles, bare earth and broken snow, no painted screenshots.
 const tiles:F[]=[]
 for(let id=0;id<32;id++){
  const f:F={width:32,height:16,pixels:new Uint8Array(512),opaque:new Uint8Array(512)}
  for(let y=0;y<16;y++)for(let x=0;x<32;x++){
   if(Math.abs((x-15.5)/16)+Math.abs((y-7.5)/8)>1)continue
   const n=(x*13+y*31+id*47)%101,band=Math.floor((y+id%3)/4),seam=(x+(band%2)*5+id%5)%10===0||(y+id%3)%4===0
   let c=id<12?(seam?48:49+n%4):id<22?(56+n%2):(n<76?54+n%2:49+n%2)
   if(id>=22&&n>93)c=56+n%2
   f.pixels[y*32+x]=c;f.opaque[y*32+x]=1
  }tiles.push(f)
 }
 art.tiles=await gz(tiles)
 art.portraits=Object.fromEntries(Object.entries(pack.portraits).map(([k,v])=>[k,Uint8Array.from(Buffer.from(v as string,'base64')).buffer]))
 return art
}
