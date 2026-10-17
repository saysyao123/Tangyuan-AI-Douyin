/* T30 image-backed scene architecture, replacing the rejected T25 geometry.
 * Runs in native Type PAL scene composition, underneath actors and dialogue.
 * Does not modify project content, original maps, SAVE12 or hit-testing.
 */
import type {Camera} from './render.js';
import type {EntityDef} from '@type-pal/content';
import type {ProjectMapTileDraw} from './project-map.js';
type Kind='house';
const scenes:Record<string,Record<string,Kind>>={
 street:{'street-rental-0':'house','street-rental-1':'house','street-rental-2':'house'},
 courtyard:{
  'courtyard-rental-0':'house','courtyard-rental-1':'house','courtyard-rental-2':'house',
  'west-courtyard-house':'house','middle-courtyard-house':'house','home-courtyard-house':'house'
 }
};
// Remove the old low-res structure sprites; otherwise a new prop is visibly
// pasted on top of the previous building rather than replacing it.
export function replacesNativeSprite(scene:string,id:string){return Boolean(scenes[scene]?.[id])}
const drawIds:Record<string,Set<string>>={
 street:new Set(['street-rental-0','street-rental-1','street-rental-2']),
 courtyard:new Set(['west-courtyard-house','middle-courtyard-house','home-courtyard-house'])
};
let building:HTMLImageElement|undefined;
const getBuilding=()=>{
 if(typeof Image==='undefined')return undefined;
 if(!building){
  building=new Image();building.decoding='async';
  building.src=new URL('./t30-hd-house.png',window.location.href).href;
 }
 return building.complete&&building.naturalWidth>0?building:undefined;
};
export function renderDetailedFirstAct(
 ctx:CanvasRenderingContext2D, sceneId:string, camera:Camera,
 entities:readonly EntityDef[], _tiles:readonly ProjectMapTileDraw[]
):void{
 const ids=drawIds[sceneId],img=getBuilding();if(!ids||!img)return;
 const selected=entities.filter(e=>ids.has(e.id)).sort((a,b)=>(a.pos.col+a.pos.row)-(b.pos.col+b.pos.row));
 ctx.save();ctx.imageSmoothingEnabled=true;
 for(const e of selected){
  const px=16*(e.pos.col-e.pos.row)-camera.x;
  const py=8*(e.pos.col+e.pos.row)-camera.y;
  const width=157, height=img.naturalHeight*width/img.naturalWidth;
  // World coordinates and actor depth remain native; this is a visual-only
  // source sprite with the same ground anchor as the previous house.
  const x=px-width*.52,y=py-height*.82+12;
  ctx.drawImage(img,x,y,width,height);
 }
 ctx.restore();
}
