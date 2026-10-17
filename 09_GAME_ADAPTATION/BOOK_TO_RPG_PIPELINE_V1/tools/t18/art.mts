import fs from 'node:fs/promises'
import { compressGzip, decompressGzip, encodeSpriteChunk, parseSpriteChunk } from '@type-pal/reforge'
export async function environmentArt(packFile:string,project:string){
 const pack=JSON.parse(await fs.readFile(packFile,'utf8')),result:Record<string,Buffer>={}
 for(const [name,f]of Object.entries(pack)as[string,any][]){const frame={...f,pixels:Uint8Array.from(Buffer.from(f.pixels,'base64')),opaque:Uint8Array.from(Buffer.from(f.opaque,'base64'))};result[name]=Buffer.from(await compressGzip(encodeSpriteChunk([frame])))}
 // Existing native floor texture: quieter grain and coherent board seams, unchanged opacity.
 const palette=JSON.parse(await fs.readFile(project+'/assets/generated/colors/project-standard.json','utf8')).colors as number[][]
 const color=(rgb:number[])=>{let best=Infinity,index=0;for(let i=0;i<255;i++){const d=palette[i].reduce((sum:number,c:number,k:number)=>sum+(c-rgb[k])**2,0);if(d<best){best=d;index=i}}return index}
 const wood=color([105,81,62]),seam=color([97,75,57]),grain=color([102,79,60])
 const tiles=parseSpriteChunk(await decompressGzip(new Blob([await fs.readFile(project+'/assets/generated/tilesets/night-tiles.rle')])))
 for(let id=4;id<8;id++){const f=tiles[id];for(let y=0;y<f.height;y++)for(let x=0;x<f.width;x++)if(f.opaque[y*f.width+x])f.pixels[y*f.width+x]=y===8?seam:(x*7+y*13)%41===0?grain:wood}
 result['night-tiles']=Buffer.from(await compressGzip(encodeSpriteChunk(tiles)))
 return result
}
