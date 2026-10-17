/* T25 HD world painter. Completely original decorative output in physical pixels.
   Type PAL keeps the real map, entity positions, 320x200 game logic and event routing.
   No commercial sprites or private narrative data embedded in this renderer. */
import type { Camera } from './render.js'
import type { EntityDef } from '@type-pal/content'
import type { ProjectMapTileDraw } from './project-map.js'

const SCALE=4
const worldX=(p:{col:number;row:number})=>16*(p.col-p.row)
const worldY=(p:{col:number;row:number})=>8*(p.col+p.row)
const clamp=(v:number,a:number,b:number)=>Math.max(a,Math.min(b,v))
const hash=(x:number,y:number,k=0)=>{let n=Math.imul(x+67,374761393)+Math.imul(y+31,668265263)+Math.imul(k+1,2147483647);n=Math.imul(n^(n>>>13),1274126177);return ((n^(n>>>16))>>>0)/4294967296}
const color=(r:number,g:number,b:number,a=1)=>'rgba('+Math.round(clamp(r,0,255))+','+Math.round(clamp(g,0,255))+','+Math.round(clamp(b,0,255))+','+a+')'
type ArtKind='house'|'market'|'stage'|'backstage'
const cache=new Map<string,HTMLCanvasElement>()
const sceneArts:Record<string,Record<string,ArtKind>>={
 fair:{theater:'stage','market-stall-0':'market','market-stall-1':'market','market-stall-2':'market'},
 backstage:{'rear-wall':'backstage'},
 street:{'street-rental-0':'house','street-rental-1':'house','street-rental-2':'house'},
 courtyard:{'west-courtyard-house':'house','middle-courtyard-house':'house','home-courtyard-house':'house'}
}
export function replacesNativeSprite(scene:string,id:string){return !!sceneArts[scene]?.[id]}
function polygon(ctx:CanvasRenderingContext2D,p:number[][],fill:string,outline?:string,width=1){
 ctx.beginPath();p.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fillStyle=fill;ctx.fill()
 if(outline){ctx.lineWidth=width;ctx.strokeStyle=outline;ctx.stroke()}
}
function line(ctx:CanvasRenderingContext2D,x:number,y:number,xx:number,yy:number,c:string,w=1){
 ctx.strokeStyle=c;ctx.lineWidth=w;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(xx,yy);ctx.stroke()
}
function lit(ctx:CanvasRenderingContext2D,x:number,y:number,r:number,bright=1){
 const g=ctx.createRadialGradient(x,y,0,x,y,r)
 g.addColorStop(0,color(255,210,120,.34*bright));g.addColorStop(.42,color(251,155,67,.16*bright));g.addColorStop(1,'rgba(245,154,65,0)')
 ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2)
}
function lantern(ctx:CanvasRenderingContext2D,x:number,y:number,s=1){
 ctx.save();ctx.translate(x,y);ctx.scale(s,s)
 line(ctx,0,-26,0,-13,'#1b171b',2)
 polygon(ctx,[[-7,-12],[7,-12],[9,-7],[6,5],[-6,5],[-9,-7]],'#622e27','#241b20',2)
 const g=ctx.createRadialGradient(0,-5,1,0,-4,14);g.addColorStop(0,'#fff1bd');g.addColorStop(.42,'#ffcc6a');g.addColorStop(1,'#c95724')
 ctx.fillStyle=g;ctx.fillRect(-6,-10,12,13)
 for(const v of [-5,0,5])line(ctx,v,-11,v,5,'rgba(90,36,28,.65)',1)
 line(ctx,-8,-12,8,-12,'#35252a',3);line(ctx,-7,5,7,5,'#432929',3)
 line(ctx,0,7,0,17,'#9c4d2e',2)
 ctx.restore()
}
function roof(ctx:CanvasRenderingContext2D,pts:number[][],seed:number){
 polygon(ctx,pts,'#253849','#17232b',5)
 ctx.save();ctx.beginPath();pts.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.clip()
 // Matte blue-grey slate shingles: irregular seams and high-frequency hand-painted pixels.
 for(let j=-3;j<30;j++)for(let i=-3;i<36;i++){
  let x=i*26+(j%2)*13+4,y=j*15+8
  if(x<-12||y<-10)continue
  const t=hash(i,j,seed),v=42+Math.floor(t*25)
  polygon(ctx,[[x,y],[x+22,y+8],[x+21,y+13],[x-1,y+5]],color(v,v+12,v+24),'rgba(22,29,36,.40)',.8)
  if(t>.63)line(ctx,x+5,y+3,x+14,y+7,'rgba(207,222,227,.30)',.8)
 }
 for(let i=0;i<400;i++){
  const x=hash(i,seed,7)*620,y=hash(i,seed,8)*360
  ctx.fillStyle=hash(i,seed,9)>.72?'rgba(214,222,232,.58)':'rgba(12,23,29,.33)'
  ctx.fillRect(x,y,.8+hash(i,seed,11)*2,.65)
 }
 ctx.restore()
 line(ctx,pts[0]![0],pts[0]![1],pts[1]![0],pts[1]![1],'#d1dce2',5)
 line(ctx,pts[2]![0],pts[2]![1],pts[3]![0],pts[3]![1],'#9baebc',3)
 for(let i=0;i<18;i++){
  const u=i/18,x=pts[0]![0]+(pts[1]![0]-pts[0]![0])*u,y=pts[0]![1]+(pts[1]![1]-pts[0]![1])*u
  ctx.fillStyle=hash(i,seed,33)>.4?'#c9d6dc':'#aabdc9';ctx.fillRect(x,y-2,9,3+hash(i,seed,34)*4)
 }
}
function wood(ctx:CanvasRenderingContext2D,p:number[][],seed:number,base=[94,60,43]){
 polygon(ctx,p,color(...base),'#2d2422',4)
 const xs=p.map(v=>v[0]),ys=p.map(v=>v[1])
 ctx.save();ctx.beginPath();p.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.clip()
 for(let i=0;i<650;i++){
  let x=Math.min(...xs)+hash(i,seed,2)*(Math.max(...xs)-Math.min(...xs))
  let y=Math.min(...ys)+hash(i,seed,3)*(Math.max(...ys)-Math.min(...ys))
  const shade=hash(i,seed,4),len=2+hash(i,seed,5)*25
  line(ctx,x,y,x+len,y+hash(i,seed,6)*3,color(base[0]+(shade-.5)*65,base[1]+(shade-.5)*55,base[2]+(shade-.5)*50,.68),.65)
 }
 ctx.restore()
}
function house(id:string):HTMLCanvasElement{
 const c=document.createElement('canvas');c.width=680;c.height=540
 const a=c.getContext('2d')!;const seed=[...id].reduce((v,s)=>v+s.charCodeAt(0),0)
 const windowWarm=seed%2===0
 // Stable contact shadow and raised stone base.
 a.fillStyle='rgba(16,14,20,.45)';a.beginPath();a.ellipse(352,480,300,41,0,0,Math.PI*2);a.fill()
 polygon(a,[[37,364],[332,493],[640,349],[337,247]],'#332c2d','#151a23',5)
 polygon(a,[[38,348],[335,462],[335,496],[37,375]],'#655653','#322e2f',5)
 polygon(a,[[335,462],[638,339],[638,363],[335,496]],'#4e4545','#27292e',5)
 // Fleshed-out old timber frame, two continuous wall planes.
 wood(a,[[62,178],[334,289],[334,464],[62,355]],seed,[104,67,48])
 polygon(a,[[334,289],[619,180],[619,344],[334,464]],'#9b816a','#3f3331',5)
 // Warm plaster grain, cracks, age stains and edge oxidation.
 a.save();a.beginPath();a.moveTo(334,289);a.lineTo(619,180);a.lineTo(619,344);a.lineTo(334,464);a.closePath();a.clip()
 for(let i=0;i<560;i++){
  let x=332+hash(i,seed,14)*295,y=160+hash(i,seed,15)*320
  a.fillStyle=hash(i,seed,16)>.47?'rgba(36,30,36,.20)':'rgba(222,187,139,.24)'
  a.fillRect(x,y,1+hash(i,seed,17)*5,1+hash(i,seed,18)*8)
 }
 a.restore()
 for(const [x,y,xx,yy] of [[58,179,58,355],[194,233,194,415],[334,288,334,465],[473,234,473,407],[620,178,620,345]])
 {line(a,x+3,y,xx+3,yy,'#281f23',14);line(a,x-2,y,xx-2,yy,'#c49a6a',3)}
 for(let i=0;i<7;i++) {
  let y=252+i*25;line(a,59,y,330,y+110,'rgba(48,30,30,.70)',2);line(a,337,y+105,617,y-5,'rgba(81,57,46,.65)',2)
 }
 // Window on front wall and side frame, 2.5D mullions with glowing panes.
 function windowFrame(x:number,y:number,w:number,h:number,slant:boolean) {
  if(slant){
   polygon(a,[[x,y+18],[x+w,y-14],[x+w,y+h-14],[x,y+h+18]],'#29272b','#1e1d22',7)
   polygon(a,[[x+7,y+23],[x+w-7,y-5],[x+w-7,y+h-23],[x+7,y+h+11]],windowWarm?'#c89a58':'#93a8a9','#473323',4)
   line(a,x+w*.52,y+5,x+w*.52,y+h-8,'#422d29',8)
   line(a,x+9,y+h*.5+16,x+w-9,y+h*.5-13,'#3b2727',7)
  } else {
   polygon(a,[[x,y],[x+w,y+Math.round(w*.35)],[x+w,y+h+Math.round(w*.35)],[x,y+h]],'#28232b','#1a1920',8)
   polygon(a,[[x+7,y+9],[x+w-7,y+w*.35+9],[x+w-7,y+h+w*.35-8],[x+7,y+h-8]],windowWarm?'#e0ab63':'#809aa8','#422d23',4)
   line(a,x+w*.5,y+12,x+w*.5,y+h+w*.35-5,'#463029',8)
   line(a,x+9,y+h*.52,x+w-9,y+h*.52+w*.35,'#49302b',6)
  }
  lit(a,x+w*.48,y+h*.72,68,.50)
 }
 windowFrame(116,272,108,85,false)
 windowFrame(406,289,104,76,true)
 // Lived-in double doors, stone sill, door knocker and shelving.
 polygon(a,[[247,325],[317,355],[317,457],[247,430]],'#352828','#201b21',7)
 for(let k=0;k<7;k++)line(a,251+k*10,327+k*4,251+k*10,430+k*4,'#9d704e',2)
 a.fillStyle='#d2ac6d';a.fillRect(301,395,4,6)
 polygon(a,[[236,432],[315,460],[330,455],[255,428]],'#958276','#504748',4)
 // Foliage, wood crates and ordinary domestic possessions.
 for(let z=0;z<5;z++){let x=73+z*13,y=357+z*3;polygon(a,[[x,y],[x+17,y+6],[x+17,y+23],[x,y+18]],'#6d4c35','#382c29',2)}
 roof(a,[[13,184],[294,53],[670,169],[348,326]],seed)
 line(a,13,184,348,327,'#2c2324',17);line(a,348,327,670,168,'#3c2b26',16)
 line(a,13,178,348,319,'rgba(230,235,240,.85)',6)
 for(let i=0;i<28;i++){
  let x=22+i*22,y=185+i*5
  a.fillStyle=i%4?'#d6dee6':'#98acb8';a.beginPath();a.ellipse(x,y,10,3,0,0,7);a.fill()
 }
 lantern(a,552,280,1.7);lit(a,552,270,98,.60)
 return c
}
function market(id:string):HTMLCanvasElement{
 const c=document.createElement('canvas');c.width=450;c.height=355
 const a=c.getContext('2d')!,seed=[...id].reduce((s,ch)=>s+ch.charCodeAt(0),0)
 a.fillStyle='rgba(18,13,19,.43)';a.beginPath();a.ellipse(221,322,186,23,0,0,7);a.fill()
 for(const [x,y] of [[57,116],[350,116],[72,252],[364,252]]){
  line(a,x,y,x,324,'#322126',15);line(a,x+3,y,x+3,320,'#b17b4c',4)
 }
 // Two isometric walls of a raised produce counter.
 wood(a,[[56,234],[220,289],[383,231],[218,179]],seed,[115,71,46])
 polygon(a,[[58,234],[218,288],[218,315],[57,261]],'#664331','#32232c',4)
 polygon(a,[[218,288],[382,231],[382,257],[218,315]],'#50372c','#2b1f24',4)
 for(let i=0;i<50;i++){
  const x=65+hash(i,seed,23)*285,y=210+hash(i,seed,24)*47
  const hue=['#e6b866','#c85639','#d98b45','#6c7b48','#9c322c'][i%5]!
  a.beginPath();a.fillStyle=hue;a.ellipse(x,y,3+hash(i,seed,25)*6,2+hash(i,seed,26)*4,0,0,7);a.fill()
  line(a,x-2,y-2,x+2,y-2,'rgba(255,223,165,.60)',1)
 }
 // Heavy tiled cloth awning; scallops and seams.
 polygon(a,[[22,136],[203,44],[431,133],[245,228]],seed%2?'#9f5839':'#d2ae75','#48352b',12)
 for(let i=0;i<9;i++){
  let x=27+i*46;line(a,x,135+i*11,x+184,51+i*11,'rgba(67,45,39,.38)',3)
 }
 for(let i=0;i<15;i++){
  const x=29+i*27,y=144+i*5.7
  a.fillStyle=i%2?'#cda975':'#8a3935';a.beginPath();a.ellipse(x,y,12,7,0,0,7);a.fill()
 }
 lantern(a,79,204,1.7);lantern(a,363,187,1.7);lit(a,77,205,81,.45)
 return c
}
function stage():HTMLCanvasElement{
 const c=document.createElement('canvas');c.width=760;c.height=565;const a=c.getContext('2d')!
 const seed=713
 a.fillStyle='rgba(13,10,18,.5)';a.beginPath();a.ellipse(385,520,354,43,0,0,7);a.fill()
 // Grand overhead eaves and ornate stage platform.
 polygon(a,[[34,429],[370,500],[719,413],[385,346]],'#6f4d38','#251d23',10)
 for(let i=0;i<20;i++)line(a,70+i*31,419+i*3,365+i*11,476-i*2,'#a0794d',1.4)
 for(const [x,y] of [[85,171],[655,164]]) {
  a.fillStyle='#3c2726';a.fillRect(x,y,25,281)
  line(a,x+6,y+4,x+6,y+271,'#bf8753',4)
 }
 polygon(a,[[105,175],[654,175],[654,421],[105,421]],'#302633','#1b171f',8)
 for(let i=0;i<9;i++) {
  let x=107+i*61;polygon(a,[[x,183],[x+62,183],[x+54,411],[x+6,411]],i%2?'#6c3330':'#903f3b','#572d34',1)
  for(let k=0;k<5;k++)line(a,x+5+k*9,200,x+5+k*9,399,'rgba(203,116,79,.20)',2)
 }
 polygon(a,[[123,205],[287,206],[282,426],[120,421]],'#843c3a','#3e252b',5)
 polygon(a,[[467,205],[644,207],[645,422],[480,425]],'#843b38','#3e252b',5)
 for(let i=0;i<16;i++){
  const x=149+i*30
  line(a,x,212,x+(i%2?4:-4),407,'#be6c53',1.5)
 }
 roof(a,[[12,171],[379,12],[755,157],[386,297]],seed)
 line(a,12,178,387,301,'#3a2b29',22);line(a,388,302,753,165,'#56352f',22)
 for(let i=0;i<22;i++){const x=50+i*31;line(a,x,176+i*4,x+10,181+i*4,'#f0c7a0',1.5)}
 for(const [x,y] of [[92,295],[649,271],[388,180]]){
  lantern(a,x,y,1.85);lit(a,x,y,91,.44)
 }
 return c
}
function backstage():HTMLCanvasElement{
 const c=document.createElement('canvas');c.width=560;c.height=460;const a=c.getContext('2d')!
 wood(a,[[20,48],[430,10],[534,115],[112,182]],514,[85,57,41])
 polygon(a,[[116,170],[509,89],[510,440],[114,458]],'#86674e','#291d20',8)
 for(let i=0;i<10;i++){
  const x=128+i*38;line(a,x,179-(x-128)/5,x,443,'#4d3027',9);line(a,x+3,175-(x-128)/5,x+3,439,'#b18359',2)
 }
 polygon(a,[[149,214],[314,174],[314,440],[149,453]],'#923d3d','#55242a',7)
 for(let i=0;i<20;i++){const x=154+i*8;line(a,x,212-i*2,x+5,443,'rgba(224,150,111,.23)',1)}
 polygon(a,[[344,150],[486,115],[486,424],[352,438]],'#a04e43','#55262c',6)
 for(let i=0;i<18;i++){let x=350+i*7;line(a,x,150-i*2,x+6,417,'rgba(234,149,114,.22)',1)}
 for(const [x,y] of [[146,226],[468,191]])lantern(a,x,y,1.4)
 return c
}
function art(id:string,kind:ArtKind){
 const key=kind+':'+id;let c=cache.get(key);if(c)return c
 c=kind==='house'?house(id):kind==='market'?market(id):kind==='stage'?stage():backstage()
 cache.set(key,c);return c
}
const floorCache=new Map<string,HTMLCanvasElement>()
function floorTexture(scene:string,variation:number):HTMLCanvasElement{
 const key=scene+':'+variation;let c=floorCache.get(key);if(c)return c
 c=document.createElement('canvas');c.width=128;c.height=64
 const a=c.getContext('2d')!
 const ground=scene==='backstage'?'#654832':scene==='fair'?'#71636a':scene==='street'?'#515c65':'#87929c'
 polygon(a,[[0,30],[62,0],[128,31],[63,64]],ground,'rgba(22,29,36,.6)',2)
 a.save();a.beginPath();a.moveTo(0,30);a.lineTo(62,0);a.lineTo(128,31);a.lineTo(63,64);a.closePath();a.clip()
 if(scene==='backstage'){
  for(let j=0;j<13;j++){
   let y=j*7,shade=hash(j,variation,8)
   line(a,-20,y,150,y+18,color(65+shade*80,42+shade*48,28+shade*30,.58),2)
   for(let k=0;k<11;k++){let x=k*13+hash(k,j,variation)*4;a.fillStyle='#2d261f';a.fillRect(x,y+1,1.4,.8)}
  }
 }else{
  for(let j=0;j<11;j++)for(let i=0;i<17;i++){
   const xx=i*8+(j%2)*4,yy=j*7
   const n=hash(i+variation,j,variation),p=20+(1-n)*38
   polygon(a,[[xx,yy],[xx+7,yy+.5],[xx+6,yy+5.5],[xx-1,yy+5]],color(p+65,p+71,p+79,.35),'rgba(22,29,35,.21)',.55)
  }
 }
 for(let i=0;i<150;i++){
  const x=hash(i,variation,7)*128,y=hash(i,variation,8)*64
  a.fillStyle=hash(i,variation,9)>.58?'rgba(228,230,231,.33)':'rgba(18,27,29,.27)'
  a.fillRect(x,y,.5+hash(i,variation,12)*2,.6)
 }
 // Differing irregular windward snow drifts, nonuniform to avoid checkerboard.
 if(scene!=='backstage'&&variation%7===0){
  a.fillStyle='rgba(220,228,237,.58)'
  polygon(a,[[-5,7],[16,8],[31,17],[12,20],[-5,14]],'rgba(227,238,246,.58)')
  polygon(a,[[108,46],[138,47],[135,65],[96,59]],'rgba(217,227,241,.53)')
 }
 a.restore()
 floorCache.set(key,c);return c
}
export function renderDetailedFirstAct(ctx:CanvasRenderingContext2D,sceneId:string,camera:Camera,
 entities:readonly EntityDef[],tiles:readonly ProjectMapTileDraw[]):void {
 const replaced=sceneArts[sceneId];if(!replaced)return
 ctx.save();ctx.imageSmoothingEnabled=true
 // Canvas has already been scaled by worldScale=4 before invocation.
 const seen=new Set<string>()
 for(const t of tiles){
  if(t.height!==0||t.layerIndex!==0)continue
  const key=t.centerX+','+t.centerY;if(seen.has(key))continue;seen.add(key)
  const variation=Math.floor(hash(t.col,t.row,59)*38)
  const img=floorTexture(sceneId,variation)
  const x=t.centerX-camera.x-16,y=t.centerY-camera.y-8
  ctx.drawImage(img,x,y,32,16)
 }
 for(const e of entities){
  const kind=replaced[e.id];if(!kind)continue
  const p=e.pos, x=worldX(p)-camera.x,y=worldY(p)-camera.y+7
  const img=art(e.id,kind)
  // Physical sprite pixel resolution 4x. World coordinates and foot anchors unchanged.
  ctx.drawImage(img,x-img.width/(SCALE*2),y-img.height/SCALE,img.width/SCALE,img.height/SCALE)
 }
 ctx.restore()
}
