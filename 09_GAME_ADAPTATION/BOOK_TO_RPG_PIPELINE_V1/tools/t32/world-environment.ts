/** T34 raster environment composition, display only; no authored scene/motion/save mutation. */
import type {Camera} from './render.js';
type GetImage=(key:string)=>HTMLImageElement|undefined;
export const worldEnvironmentFiles=[...Array.from({length:3},(_,i)=>`v34-house-${i}`),...Array.from({length:3},(_,i)=>`v34-stall-${i}`),'v34-stage','v34-back-left','v34-back-right','v34-snow','v34-stone','v34-earth',...['lamp','sign','wall','tree','stove','garden','wood','crate'].map(k=>'v34-'+k),'room-floor'];
export function drawBackstageWalls(ctx:CanvasRenderingContext2D,camera:Camera,get:GetImage){
 const left=get('v34-back-left'),right=get('v34-back-right');if(!left||!right)return;
 const A={x:400,y:184},B={x:528,y:120},C={x:752,y:232};
 const wall=(im:HTMLImageElement,a:typeof A,b:typeof A)=>{ctx.save();ctx.imageSmoothingEnabled=true;ctx.transform((b.x-a.x)/im.naturalWidth,(b.y-a.y)/im.naturalWidth,0,78/im.naturalHeight,a.x-camera.x,a.y-camera.y-78);ctx.drawImage(im,0,0);ctx.restore()};
 wall(left,A,B);wall(right,B,C);
}
export function paintEnvironmentGround(ctx:CanvasRenderingContext2D,scene:string){
 ctx.save();
 // Cool night ambient is below sprites/UI; source colors of accepted people and room stay intact.
 ctx.fillStyle=scene==='fair'?'rgba(24,41,66,.10)':'rgba(20,35,57,.14)';ctx.fillRect(0,0,2000,1000);
 const lights:Record<string,number[][]>={fair:[[464,200,44,.19],[608,256,42,.17],[832,242,65,.19],[560,171,40,.13],[640,210,42,.13]],street:[[384,187,57,.16],[608,187,57,.18],[832,187,57,.15],[720,184,35,.16]],courtyard:[[480,216,53,.15],[704,216,53,.16],[896,246,58,.19],[592,248,24,.15]],backstage:[[452,187,60,.20],[650,196,63,.17]]};
 for(const [x,y,r,a]of lights[scene]??[]){const g=ctx.createRadialGradient(x!,y!,2,x!,y!,r!);g.addColorStop(0,`rgba(229,154,70,${a})`);g.addColorStop(1,'rgba(229,154,70,0)');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(x!,y!,r!,r!*.48,0,0,Math.PI*2);ctx.fill()}
 // Broad contact shadows tie complete buildings/stalls to the same native feet.
 const feet:Record<string,number[][]>={street:[[384,176,74,18],[608,176,74,18],[832,176,74,18],[288,256,24,9],[848,184,24,9]],courtyard:[[480,208,74,18],[704,208,74,18],[896,240,74,18],[592,248,17,6]],fair:[[560,168,36,12],[640,208,36,12],[336,280,36,12],[832,224,72,18],[384,176,24,9]],backstage:[[528,168,17,6],[560,168,17,6]]};
 for(const [x,y,rx,ry]of feet[scene]??[]){const g=ctx.createRadialGradient(x!,y!+7,0,x!,y!+7,rx!);g.addColorStop(0,'rgba(14,20,28,.25)');g.addColorStop(1,'rgba(14,20,28,0)');ctx.save();ctx.translate(x!,y!+7);ctx.scale(1,ry!/rx!);ctx.fillStyle=g;ctx.translate(-x!,-y!-7);ctx.beginPath();ctx.arc(x!,y!+7,rx!,0,Math.PI*2);ctx.fill();ctx.restore()}
 ctx.restore();
}
