/** T33 home-room presentation. Canonical grid, actors, collision and SAVE12 stay native.
 * One reversible, uniform view transform is shared by world draw, markers and pointer inverse.
 */
import type {Camera} from './render.js';
type GetImage=(key:string)=>HTMLImageElement|undefined;
export const ROOM_VIEW={scale:.60,camera:{x:144,y:-24}} as const;
const A={x:160,y:138},B={x:400,y:58},C={x:656,y:143};
function floorPath(c:CanvasRenderingContext2D){c.beginPath();c.moveTo(A.x,A.y);c.lineTo(B.x,B.y);c.lineTo(C.x,C.y);c.lineTo(656,290);c.lineTo(160,290);c.closePath()}
let cachedRoom:HTMLCanvasElement|undefined;
export function drawRoomGround(ctx:CanvasRenderingContext2D,camera:Camera,get:GetImage){
 if(!cachedRoom){const canvas=document.createElement('canvas');canvas.width=2600;canvas.height=1680;const c=canvas.getContext('2d')!;c.scale(4,4);c.translate(-80,90);paintRoomGround(c,get);cachedRoom=canvas}
 ctx.save();ctx.imageSmoothingEnabled=true;ctx.drawImage(cachedRoom,80-camera.x,-90-camera.y,650,420);ctx.restore();
}
function paintRoomGround(ctx:CanvasRenderingContext2D,get:GetImage){
 const camera={x:0,y:0};
 const wood=get('room-floor'),left=get('room-wall-left'),right=get('room-wall-right');if(!wood||!left||!right)return;
 ctx.save();ctx.translate(-camera.x,-camera.y);ctx.fillStyle='#080c13';ctx.fillRect(80,-90,650,420);
 ctx.save();floorPath(ctx);ctx.clip();ctx.imageSmoothingEnabled=true;
 // Project a neutral top-down plank texture into the same 2:1 ground plane as props.
 ctx.save();ctx.transform(1,.5,-1,.5,0,0);
 for(let v=-480;v<400;v+=160)for(let u=0;u<880;u+=160)ctx.drawImage(wood,u,v,160,160);
 ctx.restore();
 let glow=ctx.createRadialGradient(350,174,12,350,174,180);glow.addColorStop(0,'rgba(239,152,53,.22)');glow.addColorStop(1,'rgba(239,152,53,0)');ctx.fillStyle=glow;ctx.fillRect(160,10,496,280);
 glow=ctx.createRadialGradient(340,96,5,340,96,126);glow.addColorStop(0,'rgba(111,163,222,.26)');glow.addColorStop(1,'rgba(89,133,184,0)');ctx.fillStyle=glow;ctx.fillRect(160,10,496,280);ctx.restore();
 // Both full wall elevations include plaster, dado, posts and the roof cut beam.
 const wall=(im:HTMLImageElement,a:typeof A,b:typeof A)=>{ctx.save();ctx.transform((b.x-a.x)/im.naturalWidth,(b.y-a.y)/im.naturalWidth,0,78/im.naturalHeight,a.x,a.y-78);ctx.drawImage(im,0,0);ctx.restore()};wall(left,A,B);wall(right,B,C);
 // Ground shadows connect the old authored feet to the new floor; no simulation footprint changes.
 for(const [x,y,rx,ry]of [[432,200,46,15],[512,192,26,10],[320,240,38,12],[240,184,23,9],[352,176,20,8],[528,232,17,8]]){ctx.fillStyle='rgba(16,10,6,.24)';ctx.beginPath();ctx.ellipse(x!,y!+4,rx!,ry!,0,0,Math.PI*2);ctx.fill()}
 const mat=get('room-mat');if(mat){ctx.drawImage(mat,263,216,50,25);ctx.drawImage(mat,535,239,50,25)}
 ctx.restore();
}
export function drawRoomForeground(ctx:CanvasRenderingContext2D,camera:Camera,get:GetImage){
 const panel=get('room-wall-right');if(!panel)return;ctx.save();ctx.translate(-camera.x,-camera.y);ctx.imageSmoothingEnabled=true;
 // Cut-away front sill with two open threshold aisles. It never paints over the central route.
 const rail=(x:number,w:number)=>ctx.drawImage(panel,0,panel.naturalHeight*.76,panel.naturalWidth*.18,panel.naturalHeight*.24,x,270,w,25);
 rail(160,110);rail(310,230);rail(580,76);
 // Exposed timber end posts and low side returns use the same raster material.
 for(const x of [160,646])ctx.drawImage(panel,0,0,panel.naturalWidth*.035,panel.naturalHeight,x,138,10,157);
 ctx.restore();
}
