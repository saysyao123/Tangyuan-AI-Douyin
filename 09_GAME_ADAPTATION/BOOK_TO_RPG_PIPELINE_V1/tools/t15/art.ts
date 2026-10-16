/* Original editable sprite inputs + bounded native pixel poses/effects. GPL-3.0. */
import fs from 'node:fs/promises'
import {compressGzip,encodeSpriteChunk} from '@type-pal/reforge'
import {buildPolishedArt} from './t14-art.ts'
type F={width:number;height:number;pixels:Uint8Array;opaque:Uint8Array}
const blank=(width:number,height:number):F=>({width,height,pixels:new Uint8Array(width*height),opaque:new Uint8Array(width*height)})
const dot=(f:F,x:number,y:number,c:number)=>{x=Math.round(x);y=Math.round(y);if(x>=0&&y>=0&&x<f.width&&y<f.height){f.pixels[y*f.width+x]=c;f.opaque[y*f.width+x]=1}}
const paste=(f:F,a:F,ox:number,oy:number)=>{for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++)if(a.opaque[y*a.width+x])dot(f,x+ox,y+oy,a.pixels[y*a.width+x])}
async function gz(frames:F[]){const b=await compressGzip(encodeSpriteChunk(frames));return b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength)}
const dec=(f:any):F=>({...f,pixels:Uint8Array.from(Buffer.from(f.pixels,'base64')),opaque:Uint8Array.from(Buffer.from(f.opaque,'base64'))})
function walk(src:F,dir:number,phase:number):F{if(!phase)return src;const f=blank(src.width,src.height),hip=Math.floor(src.height*.69),sign=phase===1?1:-1;for(let y=0;y<src.height;y++)for(let x=0;x<src.width;x++){const i=y*src.width+x;if(!src.opaque[i])continue;const t=Math.max(0,(y-hip)/(src.height-hip)),leg=x<src.width/2?-1:1;dot(f,x+Math.round(sign*leg*t*2),y+Math.round(sign*leg*t*(dir===0||dir===3?1:-1)),src.pixels[i])}return f}
export async function buildCinematicArt(oldPackFile:string,newPackFile:string){
 const old=JSON.parse(await fs.readFile(oldPackFile,'utf8')),pack=JSON.parse(await fs.readFile(newPackFile,'utf8')),art:any=await buildPolishedArt(oldPackFile),palette=old.palette as number[][]
 const color=(r:number,g:number,b:number)=>{let n=0,best=Infinity;for(let i=0;i<255;i++){const c=palette[i],d=(c[0]-r)**2+(c[1]-g)**2+(c[2]-b)**2;if(d<best){best=d;n=i}}return n}
 for(const [id,frames] of Object.entries(pack.sprites))art[id]=await gz(id==='operative'?(frames as any[]).map(dec).flatMap((f,dir)=>[0,1,2].map(p=>walk(f,dir,p))):(frames as any[]).map(dec))
 const people=(pack.sprites.operative as any[]).map(dec),performer=dec(old.sprites.performer[0]),fallen:F[]=[]
 for(let pose=0;pose<3;pose++){const f=blank(64,56);for(let y=0;y<performer.height;y++)for(let x=0;x<performer.width;x++){const k=y*performer.width+x;if(!performer.opaque[k])continue;if(!pose)dot(f,x+14,y,performer.pixels[k]);else if(pose===1)dot(f,x+14,Math.min(52,Math.round(y*.68)+17),performer.pixels[k]);else dot(f,5+Math.round((55-y)*.9),48-Math.round(x*.5),performer.pixels[k])}fallen.push(f)}
 const standing=fallen[0];for(const phase of [1,2]){const f=blank(64,56);paste(f,walk(performer,3,phase),14,0);fallen.push(f)}
 const bow=blank(64,56);for(let y=0;y<performer.height;y++)for(let x=0;x<performer.width;x++)if(performer.opaque[y*performer.width+x])dot(bow,x+14+(y<32?Math.round((32-y)/8):0),y+(y<32?4:0),performer.pixels[y*performer.width+x]);fallen.push(bow)
 art['performer-action']=await gz(fallen)
 const carriers:F[]=[]
 for(let dir=0;dir<4;dir++)for(let phase=0;phase<3;phase++){const f=blank(76,60);const body=fallen[2];for(let y=0;y<body.height;y++)for(let x=0;x<body.width;x++)if(body.opaque[y*body.width+x])dot(f,12+x,Math.round((y-30)*.7)+24,body.pixels[y*body.width+x]);paste(f,walk(people[dir],dir,phase),0,3);paste(f,walk(people[dir],dir,phase===1?2:phase===2?1:0),40,3);carriers.push(f)}
 art.carriers=await gz(carriers)
 const crouch=(old.sprites.child as any[]).map(dec).flatMap((a:F)=>[0,1,2].map(()=>{const f=blank(a.width,a.height);for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++)if(a.opaque[y*a.width+x])dot(f,x,Math.min(a.height-3,Math.round(y*.72)+10),a.pixels[y*a.width+x]);return f}));art['child-crouch']=await gz(crouch)
 const red=color(255,110,35),orange=color(255,185,61),blue=color(85,184,219),white=color(245,236,203),coal=color(48,55,60),wood=color(107,84,62),brick=color(133,121,105),leaf=color(82,112,76)
 for(const kind of ['body-fire','fireball','heart','steam']){const frames:F[]=[];for(let phase=0;phase<6;phase++){const f=blank(kind==='body-fire'?48:32,kind==='body-fire'?64:36);for(let y=0;y<f.height;y++)for(let x=0;x<f.width;x++){const cx=f.width/2,cy=kind==='heart'?19:kind==='steam'?24:kind==='body-fire'?37:21,rx=kind==='body-fire'?16:kind==='heart'?9+phase:kind==='steam'?6:9,ry=kind==='body-fire'?23:kind==='heart'?11+phase:kind==='steam'?16:9;const d=(x-cx)**2/rx**2+(y-cy)**2/ry**2;
 if(kind==='steam'){if(y<30&&Math.abs(x-cx-Math.sin((y+phase*3)/4)*3)<1&&(y+phase)%3!==0)dot(f,x,y,white)}
 else if(kind==='heart'){if(d>.75&&d<1.12&&(x+y+phase)%3!==0)dot(f,x,y,phase%2?orange:blue)}
 else if(kind==='body-fire'){if(d<1.2&&d>.6&&((x*7+y*3+phase*13)%17)<11)dot(f,x,y,y>40?blue:(x+y+phase)%4===0?white:(phase+x)%3?red:orange)}
 else {if(d<1)dot(f,x,y,d<.3?blue:d<.6?white:orange);if(x>18&&x<31&&Math.abs(y-20)<(31-x)/3&&(x+y+phase)%3!==0)dot(f,x,y,red)}
 }frames.push(f)}art[kind]=await gz(frames)}
 const needle=blank(16,8);for(let x=2;x<15;x++)dot(needle,x,4,x<6?blue:white);art.needle=await gz([needle])
 const treats:F[]=[];for(const count of [7,2,1,0]){const f=blank(16,36);for(let y=6;y<35;y++)dot(f,8,y,wood);for(let k=0;k<count;k++)for(let y=-1;y<2;y++)for(let x=-1;x<2;x++)dot(f,8+x,6+k*4+y,x+y<0?orange:red);treats.push(f)}art.skewer=await gz(treats)
 const wall=blank(96,40);for(let y=10;y<36;y++)for(let x=0;x<96;x++)if(y>=10+x/12&&y<28+x/12)dot(wall,x,y,(y%5===0||(x+(Math.floor(y/5)%2)*6)%13===0)?coal:brick);art.wall=await gz([wall])
 const patch=blank(72,36);for(let y=8;y<30;y++)for(let x=2;x<70;x++){if(Math.abs((x-36)/35)+Math.abs((y-18)/13)>1)continue;dot(patch,x,y,(x+y)%7?wood:coal);if(y%6===0&&x%6<2){dot(patch,x,y-2,leaf);dot(patch,x-1,y-3,leaf)}}art.vegetables=await gz([patch])
 const crate=blank(32,28);for(let y=6;y<26;y++)for(let x=2;x<30;x++)if(y>6+Math.abs(x-16)/3)dot(crate,x,y,x%6?wood:coal);art.crate=await gz([crate])
 // Late-winter dusk tint applies to this independent project's indexed art only.
 art.palette={colors:palette.map(([r,g,b],i)=>i===255?[r,g,b]:[Math.min(255,r+5),g,Math.max(0,b-4)]),cycles:[]}
 return art
}
