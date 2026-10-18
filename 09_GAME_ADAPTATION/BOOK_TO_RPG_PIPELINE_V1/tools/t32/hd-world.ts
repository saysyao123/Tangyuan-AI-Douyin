/** Original T32 raster art, painted inside native canvas and native depth order.
 * Original frames remain the simulation and pointer contracts. Only drawing changes.
 * Missing art falls back to native sprites; ?art=baseline is a reversible QA switch.
 */
import type {IsometricMapContent} from '@type-pal/content';
import type {Camera,CellRect,SpriteDraw} from './render.js';
import {projectMapTilesInView} from './project-map.js';
import {ROOM_VIEW,drawRoomGround,drawRoomForeground} from './room-world.js';
const act=new Set(['fair','backstage','street','courtyard','home-room']);
const images=new Map<string,HTMLImageElement>();
const portraits=['hero','child','merchant','neighbor','stranger','visitor','officer','performer'];
const filenames=['house','stage','stall','backstage','back-panel','back-panel-window','crate-indoor','wall','tree','stove','terrain-snow','terrain-stone','terrain-earth','terrain-wood','lamp','sign','crate','garden','wood',...portraits.map(role=>'portrait-'+role)];
let activeScene='';
function img(key:string){
 let v=images.get(key);if(!v){v=new Image();v.decoding='async';v.src=new URL(`./t32-art/${key}.webp`,window.location.href).href;images.set(key,v)}
 return v.complete&&v.naturalWidth>0?v:undefined;
}
export function firstActReady(scene:string){
 activeScene=scene;
 if(!act.has(scene)||new URLSearchParams(location.search).get('art')==='baseline')return false;
 const roomFiles=['room-wall-left','room-wall-right','room-floor','room-bed','room-tv','room-meal','room-basin','room-cupboard','room-lamp','room-memento','room-mat'];
 const extra=scene==='home-room'?roomFiles:scene==='fair'?[...Array.from({length:24},(_,i)=>`crowd-${Math.floor(i/4)}-${i%4}`)]:scene==='backstage'?['action-carriers-unique-0','action-carriers-unique-1',...['a','b','c'].flatMap(role=>Array.from({length:12},(_,i)=>`sub-${role}-${Math.floor(i/3)}-${i%3}`)),...Array.from({length:4},(_,i)=>`crowd-0-${i}`)]:[];
 const all=[...filenames,...extra,
  ...['hero','child'].flatMap(role=>Array.from({length:12},(_,i)=>`lead-${role}-${Math.floor(i/3)}-${i%3}`)),
  ...['merchant','neighbor','stranger','visitor','operative','performer'].flatMap(role=>Array.from({length:4},(_,i)=>`npc-${role}-${i}`)),
  ...Array.from({length:12},(_,i)=>`guard-${Math.floor(i/3)}-${i%3}`),
  ...Array.from({length:6},(_,i)=>`action-performer-${i}`),'action-carriers-0','action-carriers-1','action-child-crouch'];
 const ready=all.map(img).every(Boolean);document.documentElement.dataset.t32Art=ready?'ready':'loading';return ready;
}
/** Keep native dialogue identities, slots, text layout and 64x72 logical footprint.
 * The source is 4x dense; it must never use its physical size as a UI size.
 * Scene restriction also preserves original portraits outside the first act.
 */
export function firstActPortrait(asset:string){
 if(!act.has(activeScene)||new URLSearchParams(location.search).get('art')==='baseline')return undefined;
 const role=asset.startsWith('portrait.')?asset.slice(9):'';
 return portraits.includes(role)?img('portrait-'+role):undefined;
}
export function roomViewActive(scene:string){return scene==='home-room'&&activeScene===scene&&document.documentElement.dataset.t32Art==='ready'&&new URLSearchParams(location.search).get('art')!=='baseline'}
export function artScreenPoint(scene:string,camera:Camera,x:number,y:number){
 const v=roomViewActive(scene)?ROOM_VIEW:{scale:1,camera};return {x:(x-v.camera.x)*v.scale,y:(y-v.camera.y)*v.scale};
}
export function artWorldPoint(scene:string,camera:Camera,x:number,y:number){
 const v=roomViewActive(scene)?ROOM_VIEW:{scale:1,camera};return {x:x/v.scale+v.camera.x,y:y/v.scale+v.camera.y};
}
export function roomView(){return ROOM_VIEW}
export function renderHDForeground(ctx:CanvasRenderingContext2D,scene:string,camera:Camera){if(scene==='home-room')drawRoomForeground(ctx,camera,img)}
let floor:{scene:string,map:IsometricMapContent<number|null>,canvas:HTMLCanvasElement,x:number,y:number}|undefined;
export function renderHDGround(ctx:CanvasRenderingContext2D,scene:string,map:IsometricMapContent<number|null>,room:CellRect,camera:Camera){
 if(scene==='home-room'){drawRoomGround(ctx,camera,img);return}
 if(!floor||floor.scene!==scene||floor.map!==map){
  const tiles=projectMapTilesInView(map,room,new Set());
  const x=Math.min(...tiles.map(t=>t.centerX))-17,y=Math.min(...tiles.map(t=>t.centerY))-9;
  const right=Math.max(...tiles.map(t=>t.centerX))+17,bottom=Math.max(...tiles.map(t=>t.centerY))+9;
  const canvas=document.createElement('canvas');canvas.width=(right-x)*4;canvas.height=(bottom-y)*4;
  const c=canvas.getContext('2d')!;c.scale(4,4);c.translate(-x,-y);
  function material(c:CanvasRenderingContext2D,kind:string,span:number){
   const texture=img('terrain-'+kind)!;
   const corners=[[x,y],[right,y],[x,bottom],[right,bottom]];
   const us=corners.map(([a,b])=>a!/2+b!),vs=corners.map(([a,b])=>b!-a!/2);
   c.save();c.transform(1,.5,-1,.5,0,0);
   for(let v=Math.floor(Math.min(...vs)/span)*span;v<Math.max(...vs);v+=span)
    for(let u=Math.floor(Math.min(...us)/span)*span;u<Math.max(...us);u+=span)c.drawImage(texture,u,v,span,span);
   c.restore();
  }
  material(c,'snow',192);
  for(const kind of ['stone','earth','wood']){
   const selected=tiles.filter(t=>(t.tileId>=22?'snow':t.tileId>=12?'earth':'stone')===kind);
   if(kind!=='wood'&&!selected.length)continue;
   if(kind==='wood'&&scene!=='backstage')continue;
   const layer=document.createElement('canvas');layer.width=canvas.width;layer.height=canvas.height;
   const l=layer.getContext('2d')!;l.scale(4,4);l.translate(-x,-y);
   material(l,kind,kind==='stone'?48:kind==='wood'?64:128);
   l.globalCompositeOperation='destination-in';l.filter='blur(2px)';l.fillStyle='white';l.beginPath();
   if(kind==='wood'){
    // Actual authored backstage dressing floor under the existing actor route.
    l.moveTo(400,205);l.lineTo(511,147);l.lineTo(643,217);l.lineTo(526,278);l.closePath();
   }else for(const t of selected){const a=t.centerX,b=t.centerY;l.moveTo(a,b-8.2);l.lineTo(a+16.3,b);l.lineTo(a,b+8.2);l.lineTo(a-16.3,b);l.closePath()}
   l.fill();l.filter='none';c.drawImage(layer,x,y,layer.width/4,layer.height/4);
  }
  floor={scene,map,canvas,x,y};
 }
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(floor.canvas,floor.x-camera.x,floor.y-camera.y,floor.canvas.width/4,floor.canvas.height/4);ctx.restore();
}
type Prop={key:string,w:number,foot?:number,depth?:number,dx?:number};
const byScene:Record<string,Record<string,Prop>>={
 'home-room':{'room-bedside':{key:'room-bed',w:96,foot:.97},'room-television':{key:'room-tv',w:56,foot:.97},'meal-table':{key:'room-meal',w:80,foot:.97},washbasin:{key:'room-basin',w:36,foot:.98},'kitchen-cupboard':{key:'room-cupboard',w:48,foot:.98},'room-lamp':{key:'room-lamp',w:44,foot:.98},memory:{key:'room-memento',w:16,foot:.98}},
 fair:{theater:{key:'stage',w:174,foot:.87,depth:-38},'market-stall-0':{key:'stall',w:84},'market-stall-1':{key:'stall',w:84},'market-stall-2':{key:'stall',w:84},'market-tree':{key:'tree',w:94}},
 backstage:{'rear-curtain':{key:'backstage',w:280,foot:.583,depth:-65,dx:-165},'rear-wall':{key:'wall',w:112}},
 street:{'street-rental-0':{key:'house',w:184,foot:.84},'street-rental-1':{key:'house',w:184,foot:.84},'street-rental-2':{key:'house',w:184,foot:.84},'street-tree':{key:'tree',w:93},'street-tree-2':{key:'tree',w:93},'street-wall':{key:'wall',w:110}},
 courtyard:{'west-courtyard-house':{key:'house',w:184,foot:.84},'middle-courtyard-house':{key:'house',w:184,foot:.84},'home-courtyard-house':{key:'house',w:184,foot:.84},'yard-wall':{key:'wall',w:112},'yard-wall-2':{key:'wall',w:112},'court-winter-tree':{key:'tree',w:103},'medicine':{key:'stove',w:40,foot:.96}}
};
const npcKeys=new Set(['merchant','neighbor','stranger','visitor','operative','performer-action']);
const direction:Record<string,number>={down:0,left:1,up:2,right:3};
export function enhanceSprites(scene:string,sprites:readonly SpriteDraw[]):SpriteDraw[]{
 return sprites.map(s=>{
  if(scene==='home-room'&&['moonlit-room-window','winter-coat-by-wall','room-door','room-yard'].includes(s.artId??''))return {...s,drawHD:()=>{}};
  if(scene==='backstage'&&s.artId==='rear-wall')return {...s,drawHD:()=>{}};
  if(scene==='backstage'&&s.artId==='rear-curtain'){
   const panel=img('back-panel'),windowPanel=img('back-panel-window');if(!panel||!windowPanel)return s;
   return {...s,sortOffset:-100,drawHD:(c,camera)=>{
    const A={x:400,y:205},B={x:511,y:147},C={x:643,y:217};
    const wall=(source:HTMLImageElement,a:typeof A,b:typeof A)=>{c.save();c.imageSmoothingEnabled=true;c.transform((b.x-a.x)/source.naturalWidth,(b.y-a.y)/source.naturalWidth,0,65/source.naturalHeight,a.x-camera.x,a.y-camera.y-65);c.drawImage(source,0,0);c.restore()};
    wall(panel,A,B);wall(windowPanel,B,C);
   }};
  }
  const prop=s.artId?byScene[scene]?.[s.artId]:undefined;
  let key=prop?.key,w=prop?.w,h=0,foot=prop?.foot??.94;
  if(!prop&&s.artKey&&npcKeys.has(s.artKey)){
   // Preserve native collapse/carry/action artwork until corresponding HD actions exist.

   key=`npc-${s.artKey==='performer-action'?'performer':s.artKey}-${direction[s.artFacing??'down']??0}`;
   h=s.frame.height;foot=1;
  }
  if(!prop&&s.artKey==='operative'){key=`guard-${direction[s.artFacing??'down']??0}-${(s.artFrame??0)%3}`;h=s.frame.height;foot=1}
  if(!prop&&['lantern','sign','crate','vegetables','snow-wood'].includes(s.artKey??'')){
   const mapping:Record<string,[string,number]>={lantern:['lamp',20],sign:['sign',24],crate:['crate',28],vegetables:['garden',48],'snow-wood':['wood',48]};
   const selected=mapping[s.artKey!]!;key=selected[0];w=selected[1];foot=.94;
   if(scene==='backstage'&&s.artKey==='crate')key='crate-indoor';
  }
  if(!prop&&(s.artKey==='hero'||s.artKey==='child')){
   key=`lead-${s.artKey}-${direction[s.artFacing??'down']??0}-${(s.artFrame??0)%3}`;
   h=s.frame.height;foot=1;
  }
  if(!prop&&s.artKey==='child-crouch'){key='action-child-crouch';h=s.frame.height;foot=1}
  if(!prop&&s.artKey==='performer-action'){key=`action-performer-${s.artFrame??0}`;h=s.frame.height;foot=1}
  if(!prop&&s.artKey==='carriers'){key=`action-carriers-unique-${(s.artFrame??0)%2}`;h=s.frame.height;foot=1}
  if(scene==='fair'&&s.artId==='rumor'){key=`crowd-3-${direction[s.artFacing??'down']??0}`;h=s.frame.height;w=0;foot=1}
  if(scene==='fair'&&s.artId?.startsWith('audience-')){const i=Number(s.artId.slice(9));const role=s.artKey==='child'?4+(Math.floor(i/5)%2):i%4;key=`crowd-${role}-${direction[s.artFacing??'down']??0}`;h=s.frame.height;w=0;foot=1}
  if(scene==='backstage'&&s.artId==='silent-witness'){key=`crowd-0-${direction[s.artFacing??'down']??0}`;h=s.frame.height;w=0;foot=1}
  if(scene==='backstage'&&['operative-2','operative-3','operative-4'].includes(s.artId??'')){const role=({'operative-2':'a','operative-3':'b','operative-4':'c'} as Record<string,string>)[s.artId!]!;key=`sub-${role}-${direction[s.artFacing??'down']??0}-${(s.artFrame??0)%3}`;h=s.frame.height;w=0;foot=1}
  if(!key)return s;
  const source=img(key);if(!source)return s;
  if(w)h=source.naturalHeight*w/source.naturalWidth;else w=source.naturalWidth*h/source.naturalHeight;
  const width=w!,height=h;
  return {...s,sortOffset:prop?.depth??s.sortOffset,drawHD:(c,camera)=>{
   const x=s.worldX-camera.x-width*.5+(prop?.dx??0),y=s.worldY-camera.y-height*foot+7;
   c.save();c.imageSmoothingEnabled=true;
   if(!prop&&((s.artKey??'').startsWith('performer')||npcKeys.has(s.artKey??'')||['hero','child','operative','child-crouch','carriers'].includes(s.artKey??''))){
    c.fillStyle='rgba(10,16,28,.25)';c.beginPath();c.ellipse(s.worldX-camera.x,s.worldY-camera.y+6,Math.min(width*.27,15),2.1,0,0,Math.PI*2);c.fill();
   }
   c.drawImage(source,x,y,width,height);c.restore();
  }};
 });
}
