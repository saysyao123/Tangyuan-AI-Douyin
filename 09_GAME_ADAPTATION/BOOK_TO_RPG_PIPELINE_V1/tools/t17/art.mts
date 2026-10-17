/* Display-only author assets. Native indexed RLE, shared palette and lattice unchanged. */
import fs from 'node:fs/promises'
import {compressGzip,decompressGzip,encodeSpriteChunk,parseSpriteChunk} from '@type-pal/reforge'
type F={width:number;height:number;pixels:Uint8Array;opaque:Uint8Array}
const blank=(width:number,height:number):F=>({width,height,pixels:new Uint8Array(width*height),opaque:new Uint8Array(width*height)})
const dot=(f:F,x:number,y:number,c:number)=>{f.pixels[y*f.width+x]=c;f.opaque[y*f.width+x]=1}
const gz=async(frames:F[])=>Buffer.from(await compressGzip(encodeSpriteChunk(frames)))
export async function buildDisplayArt(project:string){
 const palette=JSON.parse(await fs.readFile(project+'/assets/generated/colors/project-standard.json','utf8')).colors as number[][]
 const color=(r:number,g:number,b:number)=>{let best=Infinity,out=0;for(let i=0;i<255;i++){const c=palette[i],d=(c[0]-r)**2+(c[1]-g)**2+(c[2]-b)**2;if(d<best){best=d;out=i}}return out}
 const frames=async(id:string)=>parseSpriteChunk(await decompressGzip(new Blob([await fs.readFile(project+'/assets/generated/sprites/'+id+'.rle')]))) as F[]
 const resize=(a:F,h:number)=>{const w=Math.round(a.width*h/a.height),f=blank(w,h);for(let y=0;y<h;y++)for(let x=0;x<w;x++){const i=Math.min(a.height-1,Math.floor(y*a.height/h))*a.width+Math.min(a.width-1,Math.floor(x*a.width/w));if(a.opaque[i])dot(f,x,y,a.pixels[i])}return f}
 const result:Record<string,Buffer>={'street-cottage':await gz((await frames('rental')).map(f=>resize(f,100))),'street-store':await gz((await frames('night-shop')).map(f=>resize(f,112)))}
 const shade={road:color(88,96,106),roadDot:color(76,82,90),snow:color(214,223,230),snowDot:color(204,216,226),wood:color(105,81,62),grain:color(88,67,51),wall:color(132,123,108),trim:color(81,65,50),mind:color(23,34,54),star:color(53,75,111)}
 const floor=(kind:string,x:number,y:number)=>kind==='wood'?((x+2*y)%16<2?shade.grain:shade.wood):kind==='road'?((x*7+y*13)%23<2?shade.roadDot:shade.road):kind==='snow'?((x*7+y*13)%31===0?shade.snowDot:shade.snow):kind==='wall'?shade.wall:kind==='trim'?shade.trim:((x*7+y*13)%47===0?shade.star:shade.mind)
 const tiles:F[]=[];for(let id=0;id<31;id++){const f=blank(32,16);for(let y=0;y<16;y++)for(let x=0;x<32;x++){if(Math.abs((x-15.5)/16)+Math.abs((y-7.5)/8)>1)continue;let kind=id<4?'road':id<8?'wood':id<12?'snow':id<16?'mind':id<20?'wall':'trim';if(id>=24&&id<28){const row=[29,30,38,39][id-24],worldY=row*8-8+y;kind=worldY>=236&&worldY<308?'road':'snow'}else if(id>=28){const worldY=[16,17,18][id-28]*8-8+y;kind=worldY<128?'wall':worldY<144?'trim':'wood'}dot(f,x,y,floor(kind,x,y))}tiles.push(f)}result['night-tiles']=await gz(tiles)
 return result
}
