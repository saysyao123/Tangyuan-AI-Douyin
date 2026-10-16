/* Original night props and deterministic native pixel frames, GPL-3.0. */
import fs from 'node:fs/promises'
import {compressGzip,decompressGzip,encodeSpriteChunk,parseSpriteChunk} from '@type-pal/reforge'
type F={width:number;height:number;pixels:Uint8Array;opaque:Uint8Array}
const blank=(width:number,height:number):F=>({width,height,pixels:new Uint8Array(width*height),opaque:new Uint8Array(width*height)})
const dot=(f:F,x:number,y:number,c:number)=>{x=Math.round(x);y=Math.round(y);if(x>=0&&y>=0&&x<f.width&&y<f.height){f.pixels[y*f.width+x]=c;f.opaque[y*f.width+x]=1}}
const paste=(f:F,a:F,ox:number,oy:number)=>{for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++)if(a.opaque[y*a.width+x])dot(f,x+ox,y+oy,a.pixels[y*a.width+x])}
const gz=async(frames:F[])=>Buffer.from(await compressGzip(encodeSpriteChunk(frames)))
export async function buildNightArt(project:string,packFile:string){
 const pack=JSON.parse(await fs.readFile(packFile,'utf8')),palette=pack.palette as number[][],art:Record<string,Buffer>={}
 const col=(r:number,g:number,b:number)=>{let n=0,d=Infinity;for(let i=0;i<255;i++){const a=palette[i],v=(a[0]-r)**2+(a[1]-g)**2+(a[2]-b)**2;if(v<d){d=v;n=i}}return n}
 const white=col(237,237,220),blue=col(105,189,223),gold=col(241,184,78),dark=col(33,43,58),wood=col(103,79,57),red=col(160,54,43)
 for(const [id,data] of Object.entries(pack.sprites))art[id]=await gz((data as any[]).map(f=>({...f,pixels:Uint8Array.from(Buffer.from(f.pixels,'base64')),opaque:Uint8Array.from(Buffer.from(f.opaque,'base64'))})))
 const bytes=await fs.readFile(project+'/assets/generated/sprites/hero.rle'),hero=parseSpriteChunk(await decompressGzip(new Blob([bytes]))) as F[]
 art['hero-blood']=await gz(hero.map(a=>{const f={...a,pixels:a.pixels.slice(),opaque:a.opaque.slice()};for(const [x,y]of [[a.width/2+3,15],[a.width/2+2,16],[a.width/2-2,27],[a.width/2-1,28]])dot(f,x,y,red);return f}))
 art['hero-invisible']=await gz([blank(1,1)])
 const base=hero[9],poses:F[]=[]
 for(let i=0;i<3;i++){const f=blank(72,64);if(i===0)paste(f,base,18,8);else for(let y=0;y<base.height;y++)for(let x=0;x<base.width;x++)if(base.opaque[y*base.width+x]){if(i===1)dot(f,18+x,Math.min(59,18+Math.round(y*.7)),base.pixels[y*base.width+x]);else dot(f,7+Math.round((base.height-y)*.95),55-Math.round(x*.48),base.pixels[y*base.width+x])}poses.push(f)}art['hero-night-pose']=await gz(poses)
 for(const id of ['seed-light','white-heart']){const frames:F[]=[];for(let p=0;p<6;p++){const f=blank(40,64);for(let y=4;y<58;y++)for(let x=3;x<37;x++){const d=(x-20)**2/(id==='seed-light'?20:150)+(y-36)**2/(id==='seed-light'?38:500);if(d<1.2&&d>.5&&(x+y+p)%3!==0)dot(f,x,y,p%2?white:blue)}frames.push(f)}art[id]=await gz(frames)}
 const snow:F[]=[];for(let p=0;p<8;p++){const f=blank(320,200);for(let i=0;i<105;i++){const x=(i*83+Math.floor(i/3)*11+p*2)%320,y=(i*47+p*4)%200;dot(f,x,y,white);if(i%5===0)dot(f,x+1,y,white)}snow.push(f)}art.snowfall=await gz(snow)
 const tiles:F[]=[];for(let id=0;id<16;id++){const f=blank(32,16);for(let y=0;y<16;y++)for(let x=0;x<32;x++){if(Math.abs((x-15.5)/16)+Math.abs((y-7.5)/8)>1)continue;let c=dark;const n=(x*7+y*13+id*31)%23;if(id<4)c=col(n<3?79:91,n<3?84:98,n<3?90:111);else if(id<8)c=col((x+y+id)%7===0?69:104,(x+y+id)%7===0?54:80,(x+y+id)%7===0?44:63);else if(id<12)c=col(210+n%8,219+n%7,226+n%8);else c=col(n===0?54:23,n===0?75:34,n===0?111:54);dot(f,x,y,c)}tiles.push(f)}art['night-tiles']=await gz(tiles)
 const wheel:F[]=[];for(let p=0;p<8;p++){const f=blank(40,64);for(let y=8;y<48;y++)for(let x=2;x<38;x++){const dx=x-20,dy=y-29,r=Math.hypot(dx,dy),a=Math.atan2(dy,dx);if(r<17&&r>14)dot(f,x,y,gold);else if(r<14&&Math.abs(Math.sin(a*4-p*.7))<.13)dot(f,x,y,blue)}for(let y=47;y<61;y++)for(let x=17;x<23;x++)dot(f,x,y,wood);if(p>=6){for(let y=23;y<36;y++)for(let x=14;x<27;x++)if((x-20)**2+(y-29)**2<30)dot(f,x,y,p===7?red:dark)}wheel.push(f)}art['draw-wheel']=await gz(wheel)
 for(const [id,kind]of [['income-terminal',0],['star-terminal',1],['tree-mark',2],['pendant',3]] as const){const f=blank(32,56);for(let y=33;y<52;y++)for(let x=4;x<28;x++)if(y>33+Math.abs(x-16)/3)dot(f,x,y,dark);for(let y=5;y<34;y++)for(let x=5;x<27;x++){if(kind===0&&x>7&&x<24&&(y===8||y===30||x===8||x===23||y%5===0))dot(f,x,y,white);if(kind===1&&(x-16)**2+(y-20)**2<70)dot(f,x,y,y<17?gold:blue);if(kind===2&&(Math.abs(x-16)<1||Math.abs(Math.abs(x-16)-(26-y)/2)<1))dot(f,x,y,white);if(kind===3&&(x-16)**2/60+(y-21)**2/100<1)dot(f,x,y,wood)}art[id]=await gz([f])}
 const table=blank(80,48);for(let y=17;y<37;y++)for(let x=3;x<77;x++)if(Math.abs((x-40)/37)+Math.abs((y-26)/11)<1)dot(table,x,y,wood);for(const cx of[24,54])for(let y=13;y<27;y++)for(let x=cx-10;x<cx+11;x++)if((x-cx)**2/100+(y-18)**2/25<1)dot(table,x,y,y<18?gold:white);for(let y=35;y<47;y++){dot(table,13,y,wood);dot(table,67,y,wood)}art['noodle-table']=await gz([table])
 const shelf=blank(88,64);for(let y=6;y<60;y++)for(let x=3;x<85;x++){if(x<7||x>80||y%16<3)dot(shelf,x,y,wood);else if(y%16>6&&x%14>2)dot(shelf,x,y,(x+y)%3?red:gold)}art['shop-shelf']=await gz([shelf])
 const snowmen:F[]=[];for(let p=0;p<3;p++){const f=blank(48,64);const circles=p===0?[[24,51,15]]:p===1?[[24,49,15],[21,29,11],[24,13,8]]:[[25,51,13],[27,34,9],[25,21,7]];for(const [cx,cy,r]of circles)for(let y=cy-r;y<=cy+r;y++)for(let x=cx-r;x<=cx+r;x++)if((x-cx)**2+(y-cy)**2<r*r)dot(f,x,y,x<cx?white:blue);if(p>0){dot(f,22,p===1?12:20,dark);dot(f,26,p===1?12:20,dark);dot(f,24,p===1?15:23,gold)}snowmen.push(f)}art.snowman=await gz(snowmen);for(const [id,i]of [['snow-pile',0],['snow-big',1],['snow-small',2]] as [string,number][])art[id]=await gz([snowmen[i]])
 const tracks=blank(64,24);for(let i=0;i<7;i++)for(let y=0;y<3;y++)for(let x=0;x<2;x++)dot(tracks,4+i*8+x,5+(i%2)*7+y,dark);art.footprints=await gz([tracks])
 return art
}
