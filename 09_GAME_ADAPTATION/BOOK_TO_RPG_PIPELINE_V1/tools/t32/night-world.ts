/** T36 second act display only. No world, collision, script, SAVE12 or action timing writes. */
import type {Camera,SpriteDraw} from './render.js';
type GetImage=(key:string)=>HTMLImageElement|undefined;
export const nightScenes=new Set(['night-road','night-shop-room','mind-tree','snow-yard']);
export const nightArtFiles=['storefront','truck','snow-big','snow-small','snow-pile','tracks','shop-left','shop-right','shelf-a','counter','shelf-b','fridge',...['driver','keeper'].flatMap(k=>Array.from({length:4},(_,i)=>k+'-'+i)),'hero-down','hero-rise','portrait-driver','portrait-keeper','mind-tree','draw-basin','income-book','star-orb','fruit','white-flame',...Array.from({length:12},(_,i)=>`driver-walk-${Math.floor(i/3)}-${i%3}`)].map(k=>'v36-'+k);
export function nightView(scene:string,camera:Camera){return scene==='night-shop-room'?{scale:.60,camera:{x:205,y:10}}:{scale:.8,camera:{x:camera.x-40,y:camera.y-(scene==='mind-tree'?45:60)}}}
let floor:{scene:string,canvas:HTMLCanvasElement}|undefined;
export function drawNightGround(ctx:CanvasRenderingContext2D,scene:string,camera:Camera,get:GetImage){
 if(!floor||floor.scene!==scene){const canvas=document.createElement('canvas');canvas.width=2560;canvas.height=1280;const c=canvas.getContext('2d')!;c.scale(2,2);c.imageSmoothingEnabled=true;
  if(scene==='night-shop-room')paintShop(c,get);else if(scene==='mind-tree')paintMind(c,get);else paintSnow(c,scene,get);
  floor={scene,canvas};
 }
 ctx.save();ctx.imageSmoothingEnabled=true;ctx.drawImage(floor.canvas,-camera.x,-camera.y,1280,640);ctx.restore();
}
function texture(c:CanvasRenderingContext2D,im:HTMLImageElement,span:number){c.save();c.transform(1,.5,-1,.5,0,0);for(let v=-1400;v<1000;v+=span)for(let u=-200;u<2100;u+=span)c.drawImage(im,u,v,span,span);c.restore()}
function paintSnow(c:CanvasRenderingContext2D,scene:string,get:GetImage){
 c.fillStyle='#8195a7';c.fillRect(0,0,1280,640);texture(c,get('v34-snow')!,224);
 if(scene==='night-road'){c.save();c.beginPath();c.rect(0,240,1280,64);c.clip();texture(c,get('v34-stone')!,80);c.fillStyle='rgba(13,26,43,.38)';c.fillRect(0,240,1280,64);c.restore();for(const y of [239,303]){c.fillStyle='rgba(222,234,242,.3)';c.fillRect(0,y,1280,2)}}
 c.fillStyle='rgba(20,43,76,.19)';c.fillRect(0,0,1280,640);
 for(const [x,y,r]of scene==='night-road'?[[464,192,80],[752,272,95],[560,240,54]]:[[448,224,72],[592,240,72]]){const g=c.createRadialGradient(x!,y!,3,x!,y!,r!);g.addColorStop(0,'rgba(255,184,85,.22)');g.addColorStop(1,'rgba(255,184,85,0)');c.fillStyle=g;c.fillRect(x!-r!,y!-r!,r!*2,r!*2)}
}
function paintShop(c:CanvasRenderingContext2D,get:GetImage){
 const A={x:240,y:176},B={x:480,y:96},C={x:704,y:171};c.fillStyle='#080e16';c.fillRect(0,0,1280,640);c.save();c.beginPath();c.moveTo(A.x,A.y);c.lineTo(B.x,B.y);c.lineTo(C.x,C.y);c.lineTo(704,340);c.lineTo(240,340);c.closePath();c.clip();texture(c,get('room-floor')!,160);const glow=c.createRadialGradient(480,224,10,480,224,220);glow.addColorStop(0,'rgba(244,172,79,.20)');glow.addColorStop(1,'rgba(244,172,79,0)');c.fillStyle=glow;c.fillRect(200,0,540,380);c.restore();
 const wall=(im:HTMLImageElement,a:typeof A,b:typeof A)=>{c.save();c.transform((b.x-a.x)/im.naturalWidth,(b.y-a.y)/im.naturalWidth,0,78/im.naturalHeight,a.x,a.y-78);c.drawImage(im,0,0);c.restore()};wall(get('v36-shop-left')!,A,B);wall(get('v36-shop-right')!,B,C);
 // Simple low cutaway sill leaves the native door aisle open.
 c.fillStyle='#3d2b20';c.fillRect(240,334,64,6);c.fillRect(362,334,342,6);
}
function paintMind(c:CanvasRenderingContext2D,get:GetImage){
 c.fillStyle='#0c1527';c.fillRect(0,0,1280,640);c.save();c.beginPath();c.ellipse(440,220,235,110,0,0,Math.PI*2);c.clip();texture(c,get('v34-stone')!,100);c.fillStyle='rgba(8,22,45,.82)';c.fillRect(100,40,750,350);c.restore();
 const glow=c.createRadialGradient(448,208,8,448,208,240);glow.addColorStop(0,'rgba(104,141,178,.24)');glow.addColorStop(.6,'rgba(40,68,102,.18)');glow.addColorStop(1,'rgba(10,21,39,0)');c.fillStyle=glow;c.fillRect(160,0,620,440);
 c.save();c.strokeStyle='rgba(179,159,108,.15)';c.lineWidth=.5;for(const [x,y]of [[304,184],[512,208],[432,264]]){c.beginPath();c.moveTo(448,176);c.quadraticCurveTo(440,y!,x!,y!);c.stroke()}c.restore();
 for(let i=0;i<125;i++){const x=195+(i*137)%510,y=60+(i*47)%310;c.fillStyle=`rgba(190,209,226,${.10+(i%5)*.04})`;c.beginPath();c.arc(x,y,i%6===0?.8:.35,0,Math.PI*2);c.fill()}
}
const direction:Record<string,number>={down:0,left:1,up:2,right:3};
export function nightSprite(scene:string,s:SpriteDraw,get:GetImage):SpriteDraw|undefined{
 if(!nightScenes.has(scene))return undefined;
 const none=()=>({...s,drawHD:()=>{}});
 if(['road-house-0','road-house-1','shop-facade'].includes(s.artId??''))return none();
 if(scene==='night-shop-room'&&['shop-moon-window','shop-lamp'].includes(s.artId??''))return none();
 if(s.artKey==='snowfall'){return {...s,drawHD:(c,camera)=>{const p=s.artFrame??0;c.save();c.fillStyle='rgba(222,236,248,.42)';for(let i=0;i<70;i++){const x=s.worldX-camera.x-160+(i*83+p*2)%320,y=s.worldY-camera.y-200+(i*47+p*4)%200;c.fillRect(x,y,i%5===0?.65:.35,i%5===0?1:.45)}c.restore()}}}
 const props:Record<string,[string,number,number?]>={
  'west-street-cottage':['v34-house-0',184,.84],'east-street-cottage':['v34-house-1',184,.84],'lit-storefront':['v36-storefront',162,.94],truck:['v36-truck',112,.96],tracks:['v36-tracks',45,.9],
  'yard-rental':['v34-house-2',184,.84],'yard-wall':['v34-wall',112,.94],'yard-west-tree':['v34-tree',94,.94],'yard-east-tree':['v34-tree',86,.94],
  'road-west-winter-tree':['v34-tree',94,.94],'road-east-winter-tree':['v34-tree',86,.94],
  'shelf-1':['v36-shelf-a',68,.98],'shelf-2':['v36-fridge',46,.98],'store-back-shelf':['v36-counter',76,.98],'store-side-shelf':['v36-shelf-b',60,.98],'shop-stock-cupboard':['room-cupboard',44,.98],
  income:['v36-income-book',34,.98],'star-shop':['v36-star-orb',29,.98],lottery:['v36-draw-basin',50,.98],'fruit-help':['v36-mind-tree',110,.98],
  'snow-large':['v36-snow-pile',40,.96],'snow-small':['v36-snow-pile',32,.96],'big-finished':['v36-snow-big',38,.96],'small-finished':['v36-snow-small',28,.96],
 };
 let prop=props[s.artId??''],key=prop?.[0],w=prop?.[1]??0,h=0,foot=prop?.[2]??1;
 if(s.artId==='driver'){key=`v36-driver-walk-${direction[s.artFacing??'down']??0}-${(s.artFrame??0)%3}`;h=s.frame.height}
 if(s.artId==='shopkeeper'){key=`v36-keeper-${direction[s.artFacing??'down']??0}`;h=s.frame.height}
 if(s.artKey==='hero-night-pose'){key=(s.artFrame??0)===0?'lead-hero-3-0':(s.artFrame??0)===1?'v36-hero-rise':'v36-hero-down';h=(s.artFrame??0)===0?44:40;w=0}
 if(['seed-light','white-heart'].includes(s.artKey??'')){key='v36-white-flame';w=s.artKey==='seed-light'?15:25;foot=.98}
 if(s.artKey==='stone-lantern'){key='v34-lamp';w=22;foot=.94}
 if(!key)return undefined;const im=get(key);if(!im)return none();if(w)h=im.naturalHeight*w/im.naturalWidth;else w=im.naturalWidth*h/im.naturalHeight;
 return {...s,drawHD:(c,camera)=>{const x=s.worldX-camera.x-w*.5,y=s.worldY-camera.y-h*foot+7;c.save();c.imageSmoothingEnabled=true;
  if(s.artId==='driver'||s.artId==='shopkeeper'){c.fillStyle='rgba(8,16,29,.28)';c.beginPath();c.ellipse(s.worldX-camera.x,s.worldY-camera.y+6,w*.25,2,0,0,Math.PI*2);c.fill()}
  if(s.artId==='lottery'&&(s.artFrame??0)!==7){const cut=.43;c.drawImage(im,0,im.naturalHeight*cut,im.naturalWidth,im.naturalHeight*(1-cut),x,y+h*cut,w,h*(1-cut));const f=s.artFrame??0;if(f>0&&f<6){c.fillStyle='#f5db9b';for(let i=0;i<4;i++){const a=(f+i)*Math.PI/3;c.beginPath();c.arc(s.worldX-camera.x+Math.cos(a)*12,s.worldY-camera.y-14+Math.sin(a)*4,1,0,Math.PI*2);c.fill()}}}
  else {if(['seed-light','white-heart'].includes(s.artKey??''))c.globalAlpha=.78+((s.artFrame??0)%3)*.07;c.drawImage(im,x,y,w,h)}c.restore();}};
}
