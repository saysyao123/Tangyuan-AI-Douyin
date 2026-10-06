/* A locked painterly MV: camera direction + finite authored character poses.
 * All source PNGs are consumed unchanged; no image-model video or fake walking. */
(() => {
const A=window.MV_ART,W=1080,H=1920,PI=Math.PI;
const sat=x=>Math.max(0,Math.min(1,x));
const S=(a,b,t)=>{const p=sat((t-a)/(b-a));return p*p*(3-2*p);};
const lerp=(a,b,p)=>a+(b-a)*p;
let IM,G=[],R=[];
const mix=document.createElement('canvas');mix.width=512;mix.height=512;
function init(images){
 A.init(images);IM=images;if(G.length)return;
 for(let i=0;i<8;i++)G.push(cell(images['assets/gesture_atlas.png'],i,4,384,512,0));
 // Reach frame 3 extends past its cell; exclude it. A 48px transparent left
 // inset in the retained cells avoids that pose's spill into adjacent frame 4.
 for(const k of [0,1,2,4,5])R.push(cell(images['assets/reach_atlas.png'],k,3,512,512,48));
}
function cell(im,i,cols,w,h,inset){
 const cv=document.createElement('canvas');cv.width=w;cv.height=h;
 cv.getContext('2d').drawImage(im,(i%cols)*w+inset,Math.floor(i/cols)*h,w-inset,h,inset,0,w-inset,h);return cv;
}
function lens(c,z,x=540,y=1000,dx=0,dy=0){c.translate(dx,dy);A.camera(c,z,x,y);}
function background(c,t,shade=0){A.exterior(c,t);if(shade){c.fillStyle=`rgba(4,13,24,${shade})`;c.fillRect(0,0,W,H);}A.dust(c,t,12,.12);}
function actorPose(c,frames,k,p,x,y,scale,t){
 let im=frames[k];
 if(k>0&&p<1){
  const m=mix.getContext('2d');m.clearRect(0,0,512,512);m.globalCompositeOperation='source-over';m.globalAlpha=1-p;m.drawImage(frames[k-1],0,0);m.globalCompositeOperation='lighter';m.globalAlpha=p;m.drawImage(im,0,0);m.globalAlpha=1;m.globalCompositeOperation='source-over';im=mix;
 }
 const fw=frames[0].width,fh=frames[0].height;
 c.save();c.translate(x,y);c.scale(scale,scale);
 // Only the left trailing material has secondary wind; the hand/head stay put.
 const edge=fw===384?112:138;
 for(let sx=0;sx<edge;sx+=8){const ww=Math.min(8,edge-sx),q=Math.pow(1-sx/edge,1.4),dy=Math.sin(t*2.1+sx*.03)*1.7*q;c.drawImage(im,sx,0,ww,fh,sx,dy,ww,fh);}
 c.drawImage(im,edge,0,fw-edge,fh,edge,0,fw-edge,fh);c.restore();
}
function poseIndex(times,t){let k=0;for(let i=0;i<times.length;i++)if(t>=times[i])k=i;return k;}
function opening(c,lt,t){
 c.save();
 if(lt<1.35)lens(c,1.045+.075*S(0,1.35,lt),500,1000,-7*S(0,1.35,lt));
 else lens(c,1.78+.10*S(1.35,2.5,lt),510,995,35,-20);
 background(c,t);A.actor(c,t,IM);A.thread(c,t);c.restore();
}
function longing(c,lt,t){
 const p=S(0,3.25,lt);c.save();lens(c,1.40,470,995,lerp(25,-32,p),lerp(3,-8,p));background(c,t);A.actor(c,t,IM);A.thread(c,t);c.restore();
}
// Six irregular pieces. All joins share exact vertices and return to one photo.
const polygons=[[[0,0],[342,0],[330,140],[372,278],[195,300],[0,240]],[[342,0],[900,0],[900,216],[690,266],[372,278],[330,140]],[[0,240],[195,300],[372,278],[404,407],[256,453],[0,411]],[[372,278],[690,266],[900,216],[900,447],[654,429],[404,407]],[[0,411],[256,453],[404,407],[432,650],[0,650]],[[404,407],[654,429],[900,447],[900,650],[432,650]]];
const centers=[[185,134],[643,136],[190,353],[654,353],[215,531],[662,530]];
function fragment(c,i,x,y,ang,alpha=1){
 const pts=polygons[i],[cx,cy]=centers[i];c.save();c.translate(x+cx,y+cy);c.rotate(ang);c.translate(-cx,-cy);c.globalAlpha=alpha;c.beginPath();pts.forEach((p,k)=>k?c.lineTo(...p):c.moveTo(...p));c.closePath();c.shadowColor='rgba(0,0,0,.38)';c.shadowBlur=15;c.shadowOffsetY=8;c.fillStyle='#c8b99b';c.fill();c.shadowColor='transparent';c.save();c.clip();c.drawImage(A.photo,0,0);c.restore();c.strokeStyle='rgba(105,82,59,.55)';c.lineWidth=1.4;c.stroke();c.restore();
}
function pieces(c,t,lt,mode){
 const q=S(0,1.36,lt),ret=1-S(0,1.18,lt);
 c.save();c.translate(540,950);c.rotate(-.025+Math.sin(t*.5)*.004);c.scale(.83,.83);c.translate(-450,-325);
 for(let i=0;i<6;i++){
  const [cx,cy]=centers[i],sx=(cx-450)/260,sy=(cy-325)/210;
  let d=mode==='join'?(1-q):ret;
  let x=sx*(170*d+Math.sin(t*1.6+i)*1.8),y=sy*(135*d+Math.cos(t*1.3+i)*2.0),a=sx*.14*d;
  if(mode==='linger'&&i%2===0){x=sx*2;y=sy*2;a=Math.sin(t+i)*.002;}
  fragment(c,i,x,y,a);
 }c.restore();
}
function join(c,lt,t){c.save();lens(c,1.03+.13*S(0,2.25,lt),540,950,0,-6*S(0,2.25,lt));background(c,t,.40);pieces(c,t,lt,'join');c.restore();}
function empty(c,lt,t){
 c.save();
 if(lt<1.55)lens(c,1.015,540,1050,lerp(18,-16,S(0,1.55,lt)));
 else lens(c,1.29+.06*S(1.55,2.75,lt),565,1050,0,-4);
 A.room(c,t,lt);c.restore();
}
function escapedPhoto(c,t,lt,detail=false){
 const p=S(.28,2.38,lt);let x=lerp(867,1280,p),y=lerp(1090,715,p),sc=.255;
 if(detail){x=lerp(650,815,S(1.92,3,lt));y=lerp(960,820,S(1.92,3,lt));sc=.61;}
 c.save();c.translate(x,y);c.rotate(-.05+p*.30);c.scale(sc,sc);c.translate(-450,-325);
 c.shadowColor='rgba(0,0,0,.45)';c.shadowBlur=25;c.fillStyle='#c8b99b';c.fillRect(0,0,900,650);c.shadowColor='transparent';c.drawImage(A.photo,0,0);c.restore();
}
function reaching(c,lt,t){
 const times=[0,.32,.64,1.15,1.57],k=poseIndex(times,lt);
 c.save();
 if(lt<1.92){
  lens(c,1.035+.065*S(0,1.92,lt),540,1000,-10*S(0,1.92,lt));background(c,t,.12);
  actorPose(c,R,k,k?S(times[k],times[k]+1/30,lt):1,-570,320,3.2,t);
  escapedPhoto(c,t,lt);
 }else{
  // A motivated object insert follows the departing paper, not a body reset.
  lens(c,1.04+.08*S(1.92,3,lt),540,950);background(c,t,.34);escapedPhoto(c,t,lt,true);
 }c.restore();
}
function linger(c,lt,t){c.save();lens(c,1.13-.07*S(0,2.5,lt),540,950,lerp(-10,12,S(0,2.5,lt)));background(c,t,.40);pieces(c,t,lt,'linger');c.restore();}
function gesture(c,t){
 const lt=t-16.25,times=[0,.42,.66,.87,1.03,1.19,1.36,1.56],k=poseIndex(times,lt);
 // L07 and L08 share this analytic camera path and held pose: no seam reset.
 const z=1.025+.095*S(0,2.5,lt)-.095*S(2.5,5.110907,lt),dx=-12*S(0,2.5,lt)+12*S(2.5,5.110907,lt);
 c.save();lens(c,z,600,980,dx,0);background(c,t);
 actorPose(c,G,k,k?S(times[k],times[k]+1/30,lt):1,-212,296,3.2,t);
 c.restore();
}
const funcs=[opening,longing,join,empty,reaching,linger,(c,lt,t)=>gesture(c,t),(c,lt,t)=>gesture(c,t)];
const assets=A.assets.concat(['assets/gesture_atlas.png','assets/reach_atlas.png']);
ERAS.forEach((e,k)=>{e.assets=assets;SCENES[e.id]={init,draw(c,lt,t){funcs[k](c,Math.max(0,lt),t);}};});
window.MV_ACTION_COVERAGE={reach_generated:6,reach_used:5,gesture_used:8,video_model:false,walking:false};
})();
