/* Original procedural pixel art, authored for Lantern Inn. No PAL image inputs. GPL-3.0. */
import {compressGzip,encodeSpriteChunk} from '@type-pal/reforge'
export const colors = ['101c27','172b38','22434a','315854','44705d','638168','879874','b7af8c','e2cfaa','f4e3b8','382e35','594046','80554d','a37658','ce9a63','e6bb7c','644953','946051','c88059','e7a45e','ffd387','fff0be','26384c','354e63','4d7180','6f999e','a2bec0','d2d9ca','28362f','354b3c','4b6246','72845c','201e2c','423446','6b4960','a16a77','362f28','615441','8a7556','b59b70','8e4b4b','c57564','e9a582','ffe1b0','53656c','82909a','b3bec3','e6e9df'].map(x=>[parseInt(x.slice(0,2),16),parseInt(x.slice(2,4),16),parseInt(x.slice(4,6),16)])
export const palette={colors:[...colors,...Array.from({length:256-colors.length},()=>[0,0,0])],cycles:[]}
function frame(w:number,h:number){
 const pixels=new Uint8Array(w*h),opaque=new Uint8Array(w*h)
 const dot=(x:number,y:number,c:number)=>{x=Math.round(x);y=Math.round(y);if(x>=0&&x<w&&y>=0&&y<h){pixels[y*w+x]=c;opaque[y*w+x]=1}}
 const rect=(x:number,y:number,rw:number,rh:number,c:number)=>{for(let j=y;j<y+rh;j++)for(let i=x;i<x+rw;i++)dot(i,j,c)}
 const ellipse=(cx:number,cy:number,rx:number,ry:number,c:number)=>{for(let y=cy-ry;y<=cy+ry;y++)for(let x=cx-rx;x<=cx+rx;x++)if((x-cx)**2/rx**2+(y-cy)**2/ry**2<=1)dot(x,y,c)}
 const line=(x0:number,y0:number,x1:number,y1:number,c:number)=>{const n=Math.max(Math.abs(x1-x0),Math.abs(y1-y0));for(let i=0;i<=n;i++)dot(x0+(x1-x0)*i/n,y0+(y1-y0)*i/n,c)}
 return {width:w,height:h,pixels,opaque,dot,rect,ellipse,line}
}
async function gz(frames:any[]){const bytes=await compressGzip(encodeSpriteChunk(frames));return bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)}
function tile(id:number){const f=frame(32,16);for(let y=0;y<16;y++)for(let x=0;x<32;x++){
 if(Math.abs((x-15.5)/16)+Math.abs((y-7.5)/8)>1)continue
 const noise=((x*17+y*23+id*19)%29),rim=Math.abs((x-15.5)/16)+Math.abs((y-7.5)/8)>.87
 let c=id<3?3+(noise<4?1:0):id===3?37: id===4?38: id===5?23: id===6?24:12
 if(id===3||id===4)c=rim?36:(noise<3?39:c)
 if(id===5||id===6)c=(x+y*3)%13<2?25:c
 if(id===7)c=y%5===0?10:12
 f.dot(x,y,c)
 }return f}
// Content22 direction order: down, left, up, right. Each uses idle / left / right step.
// Side views have a projecting nose and toe; the back has no face or coat buttons.
export function person(dir:number,pose:number,style:'hero'|'keeper'|'child'|'guard'='hero'){
 const f=frame(24,36),keeper=style==='keeper',child=style==='child',guard=style==='guard'
 const coat=guard?22:child?46:keeper?13:23,lit=guard?23:child?47:keeper?14:24
 const hair=keeper?44:10,scarf=child?35:guard?22:40,skin=42
 f.ellipse(12,33,8,2,1)
 const stride=pose===1?-2:pose===2?2:0
 if(dir===1||dir===3){
  // Author left; mirror the complete character for right, retaining the same foot anchor.
  f.rect(11+stride,25,3,7,22);f.rect(8+stride,31,6,2,10)
  f.rect(11-stride,24,4,8,23);f.rect(8-stride,31,7,2,10)
  f.rect(9,15,8,11,coat);f.rect(8,17,3,8,lit);f.rect(9,25,9,2,36)
  f.rect(8,6,9,8,skin);f.rect(5,9,4,3,skin);f.dot(7,9,0)
  f.rect(8,3,9,4,hair);f.rect(14,6,4,8,hair);f.rect(7,5,4,2,hair)
  f.rect(9,14,8,2,scarf);f.rect(15,15,3,7,child?34:41)
  f.rect(12+stride,17,4,9,coat);f.rect(12+stride,25,3,3,skin)
  if(keeper)f.rect(7,12,5,3,46)
  if(dir===3){const pixels=f.pixels.slice(),opaque=f.opaque.slice();for(let y=0;y<36;y++)for(let x=0;x<24;x++){f.pixels[y*24+x]=pixels[y*24+23-x];f.opaque[y*24+x]=opaque[y*24+23-x]}}
 }else{
  const back=dir===2,leftLift=pose===1?1:0,rightLift=pose===2?1:0
  f.rect(8,24,4,8-leftLift,22);f.rect(14,24,4,8-rightLift,22)
  f.rect(7+(pose===1?-1:0),31-leftLift,5,2,10);f.rect(14+(pose===2?1:0),31-rightLift,5,2,10)
  f.rect(6,15,13,12,coat);f.rect(7,17,11,6,lit);f.rect(6,25,13,2,36)
  f.rect(4,16+rightLift,3,10,coat);f.rect(19,16+leftLift,3,10,coat)
  f.rect(4,25+rightLift,3,3,skin);f.rect(19,25+leftLift,3,3,skin)
  f.rect(7,5,12,9,skin);f.rect(7,3,12,4,hair);f.rect(6,6,3,6,hair);f.rect(18,6,2,6,hair)
  if(back){f.rect(8,6,10,8,hair);f.rect(7,14,12,2,scarf);f.rect(11,17,2,8,coat);f.rect(14,15,3,5,child?34:41)}
  else{f.dot(10,9,0);f.dot(16,9,0);f.rect(12,11,2,1,18);f.rect(8,14,10,2,scarf);f.rect(16,15,3,9,child?34:41);f.rect(12,18,1,6,22);f.dot(13,19,15);f.dot(13,22,15)}
  if(keeper&&!back)f.rect(9,12,8,3,46)
 }
 if(child){const pixels=f.pixels.slice(),opaque=f.opaque.slice();f.pixels.fill(0);f.opaque.fill(0);for(let y=0;y<36;y++)for(let x=0;x<24;x++)if(opaque[y*24+x])f.dot(Math.round(12+(x-12)*.82),Math.round(34+(y-34)*.8),pixels[y*24+x])}
 return f
}
export function wolfFrame(dir:number,pose:number){
 const f=frame(40,48),stride=pose===1?-2:pose===2?2:0;f.ellipse(20,44,17,3,1)
 if(dir===1||dir===3){
  f.ellipse(22,29,13,9,23);f.rect(14+stride,33,4,9,22);f.rect(27-stride,33,4,9,22)
  f.ellipse(10,23,8,8,24);f.rect(2,24,10,5,25);f.rect(6,13,4,8,22);f.rect(11,16,4,6,23);f.dot(7,23,20);f.line(32,28,38,20,24)
  if(dir===3){const p=f.pixels.slice(),o=f.opaque.slice();for(let y=0;y<48;y++)for(let x=0;x<40;x++){f.pixels[y*40+x]=p[y*40+39-x];f.opaque[y*40+x]=o[y*40+39-x]}}
 }else{
  f.ellipse(20,29,10,12,23);f.rect(12,34,4,8-(pose===1?2:0),22);f.rect(24,34,4,8-(pose===2?2:0),22)
  if(dir===0){f.ellipse(20,23,10,9,24);f.rect(10,11,5,10,22);f.rect(25,11,5,10,22);f.rect(16,26,8,7,25);f.dot(14,22,20);f.dot(26,22,20);f.rect(18,30,4,2,0)}
  else{f.ellipse(20,18,8,7,24);f.rect(12,9,4,9,22);f.rect(24,9,4,9,22);f.rect(18,29,4,12,24)}
 }return f
}
export function previewFrames(){return ['hero','keeper','child','guard'].flatMap(style=>[0,1,2,3].flatMap(dir=>[0,1,2].map(pose=>({style,dir,pose,...person(dir,pose,style as 'hero')})))).concat([0,1,2,3].flatMap(dir=>[0,1,2].map(pose=>({style:'wolf',dir,pose,...wolfFrame(dir,pose)}))))}
function prop(kind:string,pose=0){const f=frame(kind==='house'?96:kind==='tree'?64:40,kind==='house'?90:kind==='tree'?86:48),cx=f.width/2
 if(kind==='tree'){
 f.ellipse(cx,81,23,4,1);f.rect(cx-3,45,6,35,36);f.rect(cx,49,3,28,37)
 for(let i=0;i<4;i++){const y=12+i*14,rx=12+i*6;for(let yy=0;yy<24;yy++)f.rect(cx-rx*yy/24,y+yy,rx*2*yy/24+1,1,i%2?29:28);f.line(cx-rx+4,y+22,cx,y+7,30)}
 }else if(kind==='house'){
 f.ellipse(48,85,44,4,1);f.rect(17,38,65,45,12);f.rect(20,42,58,38,13);for(let x=22;x<78;x+=11)f.rect(x,44,2,36,11)
 for(let y=0;y<32;y++)f.rect(48-y*1.4,8+y,2*y*1.4+1,1,y%6<2?22:23)
 f.rect(42,56,16,27,10);f.rect(22,51,13,15,19);f.rect(63,51,13,15,19);f.rect(27,51,2,15,12);f.rect(68,51,2,15,12);f.rect(22,57,13,2,12);f.rect(63,57,13,2,12)
 f.rect(41,40,19,10,11);f.line(43,43,56,43,20);f.line(43,46,56,46,20)
 }else if(kind==='lantern'){
 f.ellipse(cx,44,12,3,1);f.rect(cx-2,9,4,34,36);f.rect(cx-1,10,1,31,38);f.rect(cx-7,8,15,3,37);f.rect(cx+5,10,1,4,20)
 f.rect(cx+1,14,9,13,18);f.rect(cx+2,16,7,9,20);f.rect(cx+4,17,3,7,21);f.rect(cx,13,11,2,12);f.rect(cx+4,27,2,4,40)
 }else if(kind==='core'){
 f.ellipse(cx,43,12,3,1);for(let y=0;y<26;y++){const half=y<12?y/2:(26-y)/2;f.rect(cx-half,12+y,half*2+1,1,y<18?25:24)}f.line(cx,13,cx-3,32,27);f.dot(cx-12,15,20);f.dot(cx+10,22,20)
 }else if(kind==='sign'){
 f.rect(cx-2,19,4,26,37);f.rect(cx-14,9,27,15,36);f.rect(cx-12,11,23,10,38);f.line(cx-7,16,cx+7,16,8);f.line(cx+3,13,cx+7,16,8);f.line(cx+3,19,cx+7,16,8)
 }else if(kind==='stall'){
 f.rect(3,22,34,19,37);f.rect(2,16,36,7,40);f.rect(4,14,32,3,41);f.rect(5,23,2,20,36);f.rect(33,23,2,20,36)
 for(let x=9;x<32;x+=7){f.rect(x,26,1,12,39);for(let y=24;y<35;y+=4)f.rect(x-1,y,3,3,40)}
 }else if(kind==='stage'){
 f.rect(1,32,38,11,36);f.rect(2,33,36,3,18);f.rect(3,7,3,25,37);f.rect(34,7,3,25,37);f.rect(3,5,34,5,40);f.rect(7,10,5,17,34);f.rect(28,10,5,17,34)
 }else if(kind==='flame'){
 f.ellipse(cx,43,12,3,1);f.ellipse(cx+pose-1,30-pose,8,12,18);f.ellipse(cx,31-pose,5,10,20);f.ellipse(cx,34,3,6,26);f.line(cx-6,21,cx-9,14,19);f.line(cx+3,21,cx+6,9,20)
 }else if(kind==='wolf'){
 f.ellipse(cx,44,17,3,1);f.ellipse(cx+1,29,14,9,23);f.ellipse(cx-11,23,8,8,24);f.rect(cx-17,24,10,5,25);f.rect(cx-10,13,4,8,22);f.rect(cx-5,16,4,6,23);f.dot(cx-13,23,20)
 f.rect(cx-7,34,4,8-pose,22);f.rect(cx+8,34,4,8+pose,22);f.line(cx+12,28,cx+18,20,24);f.line(cx-17,28,cx-14,29,9)
 }return f}
function battle(f:any,pose=0){const out=frame(80,84),shift=pose>=7?5:0;for(let y=0;y<f.height;y++)for(let x=0;x<f.width;x++)if(f.opaque[y*f.width+x])out.rect(15+x*1.5+shift,20+y*1.5,2,2,f.pixels[y*f.width+x]);if(pose>=7)out.line(52,50,72,29,47);return out}
export async function buildOriginalArt(){
 const assets:any={palette}
 assets.tiles=await gz(Array.from({length:8},(_,i)=>tile(i)))
 assets.hero=await gz([0,1,2,3].flatMap(d=>[0,1,2].map(p=>person(d,p))))
 for(const style of ['child','guard'] as const)assets[style]=await gz([0,1,2,3].flatMap(d=>[0,1,2].map(p=>person(d,p,style))))
 assets.keeper=await gz([0,1,2,3].flatMap(d=>[0,1,2].map(p=>person(d,p,'keeper'))))
 for(const kind of ['tree','house','lantern','core','sign','stall','stage','flame'])assets[kind]=await gz([prop(kind)])
 assets.flame=await gz([0,1,2].map(p=>prop('flame',p)))
 assets.wolf=await gz([0,1,2,3].flatMap(d=>[0,1,2].map(p=>wolfFrame(d,p))))
 assets.fighter=await gz(Array.from({length:10},(_,i)=>battle(person(1,i%3),i)))
 assets.enemy=await gz(Array.from({length:4},(_,i)=>battle(prop('wolf',i%2))))
 const cursors=encodeSpriteChunk(Array.from({length:3},(_,i)=>{const f=frame(10,10);for(let y=2;y<8;y++)for(let x=2;x<8-Math.abs(y-5);x++)f.dot(x+i%2,y,20);return f}))
 assets.cursor={source:'Original authored triangle cursors, no PAL input',size:cursors.length,base64:Buffer.from(cursors).toString('base64')}
 return assets
}
