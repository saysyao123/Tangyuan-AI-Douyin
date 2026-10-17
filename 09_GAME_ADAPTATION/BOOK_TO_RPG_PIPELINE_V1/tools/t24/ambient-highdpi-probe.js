/* T24 isolated high-resolution scene-lighting renderer probe.
 * A noninteractive presentation layer, not an art-complete scene.
 * Draws @1280x800 without changing Type PAL's native 320x200 coordinates.
 */
(()=>{'use strict';
const screen=document.getElementById('screen');
if(!screen)return;
const c=document.createElement('canvas');
c.id='t24-atmosphere';
c.width=1280;c.height=800;
c.style.cssText='position:fixed;display:block;pointer-events:none;z-index:4;opacity:1;contain:strict;';
document.body.appendChild(c);
const ctx=c.getContext('2d',{alpha:true}), W=1280,H=800;
const fx={
 fair:{cool:[18,29,41],shade:0.10,gold:0.18,lamps:['market-lamp-0','market-lamp-1','market-lamp-2']},
 backstage:{cool:[28,18,19],shade:0.11,gold:0.24,lamps:['backstage-lamp','rear-wall']},
 street:{cool:[20,35,49],shade:0.16,gold:0.23,lamps:['street-lamp']},
 courtyard:{cool:[21,36,51],shade:0.14,gold:0.20,lamps:['courtyard-lamp','medicine','home']}
};
let frame=0,lastScene='',lastCamera='',lastState=null;
const particles=Array.from({length:70},(_,i)=>({
 phase:(i*719)%991/991, x:((i*71.73)%320), y:((i*91.47)%200),
 radius:i%9===0?1.8:0.6+(i%4)*.17,wind:0.15+(i%7)*.03,
 speed:.13+(i%5)*.075
}));
let errors=0,paintCount=0;
const ensureRect=()=>{
 const rect=screen.getBoundingClientRect();
 if(rect.width<2)return false;
 Object.assign(c.style,{left:rect.left+'px',top:rect.top+'px',
 width:rect.width+'px',height:rect.height+'px'});
 return true;
};
const light=(x,y,r,a,color)=>{
 const g=ctx.createRadialGradient(x,y,0,x,y,r);
 g.addColorStop(0,color.replace('ALPHA',String(a)));
 g.addColorStop(.24,color.replace('ALPHA',String(a*.62)));
 g.addColorStop(.67,color.replace('ALPHA',String(a*.19)));
 g.addColorStop(1,color.replace('ALPHA','0'));
 ctx.fillStyle=g;ctx.fillRect(x-r,y-r,2*r,2*r);
};
function draw(state,at){
 frame++;
 const scene=fx[state.sceneId];if(!scene||!state.camera){ctx.clearRect(0,0,W,H);return}
 const silent=!!state.dialogue||!!state.presentationBusy||state.battleActive||!!state.menuActive;
 ctx.clearRect(0,0,W,H);
 if(silent)return;
 const t=at/1000;
 // A low-intensity scene color wash, never cover the actors with opaque scenery.
 const grad=ctx.createLinearGradient(0,0,W,H);
 const [r,g,b]=scene.cool;
 grad.addColorStop(0,'rgba('+r+','+g+','+b+',0.055)');
 grad.addColorStop(.55,'rgba(24,24,28,0)');
 grad.addColorStop(1,'rgba('+r+','+g+','+b+',0.13)');
 ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
 // Architectural light locations from canonical scene entities, not painted
 // fake markers. Preserves the renderer's depth sorting and hit targets.
 const actors=state.actors||[];
 for(const key of scene.lamps){
  const a=actors.find(x=>x.id==='entity:'+key);
  if(!a||!a.canonical)continue;
  const p=a.canonical;
  const x=4*(16*(p.col-p.row)-state.camera.x);
  const y=4*(8*(p.col+p.row)-state.camera.y-10);
  if(x<-210||x>W+210||y<-210||y>H+210)continue;
  ctx.globalCompositeOperation='screen';
  const pulse=1+.06*Math.sin(t*2.6+(p.col+p.row));
  light(x,y,165*pulse,scene.gold,'rgba(255,161,64,ALPHA)');
  light(x,y,55,scene.gold*.80,'rgba(255,232,139,ALPHA)');
  ctx.globalCompositeOperation='source-over';
 }
 // Cold edge shade makes the original architecture read with a light hierarchy.
 const edge=ctx.createRadialGradient(W*.52,H*.37,H*.22,W*.52,H*.37,W*.66);
 edge.addColorStop(0,'rgba(4,11,19,0)');
 edge.addColorStop(.70,'rgba(8,17,28,'+(scene.shade*.29)+')');
 edge.addColorStop(1,'rgba(6,13,23,'+scene.shade+')');
 ctx.fillStyle=edge;ctx.fillRect(0,0,W,H);
 // World-coordinate snow is faint and does not read as UI particles.
 if(state.sceneId!=='backstage'){
  ctx.fillStyle='rgba(235,245,255,.52)';
  for(const p of particles){
   const x=((p.x+ (t*p.wind*2.2) -state.camera.x*.15)%330+330)%330 *4;
   const y=((p.y+t*p.speed*5)%210+210)%210 *4;
   ctx.fillRect(x,y,p.radius,p.radius*.68);
  }
 }
 paintCount++;
}
function tick(t){
 try{
  if(ensureRect()){
   const state=window.__tpObserve?.readRuntime?.();
   if(state){lastState=state;draw(state,t);}
  }
 }catch(e){errors++;if(errors===1)console.warn('[T24 ambient proof]',e);}
 requestAnimationFrame(tick);
}
window.__t24ArtProbe=Object.freeze({read:()=>({
 frame,paintCount,errors,scene:lastState?.sceneId,sceneKnown:!!fx[lastState?.sceneId],
 camera:lastState?.camera??null,canvas:[c.width,c.height],isPointerTransparent:c.style.pointerEvents==='none'
})});
requestAnimationFrame(tick);
})();
