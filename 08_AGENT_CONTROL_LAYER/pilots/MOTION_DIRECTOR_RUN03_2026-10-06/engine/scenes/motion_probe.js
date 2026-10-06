/* Director event probe: fixed camera reveals real pose changes.
 * 8 generated poses; no claim of continuous video-model performance. */
(() => {
const A=window.MV_ART,W=1080,H=1920,offset=16.25;
const sat=p=>Math.max(0,Math.min(1,p));
const smooth=(a,b,t)=>{let p=sat((t-a)/(b-a));return p*p*(3-2*p);};
const times=[0,.42,.66,.87,1.03,1.19,1.36,1.56];
let frames=[],IM;
const mix=document.createElement('canvas');mix.width=384;mix.height=512;
function makeFrame(atlas,k){
 const cv=document.createElement('canvas');cv.width=384;cv.height=512;
 cv.getContext('2d').drawImage(atlas,(k%4)*384,Math.floor(k/4)*512,384,512,0,0,384,512);
 return cv;
}
function init(images){
 A.init(images);IM=images;if(frames.length)return;
 const atlas=images['assets/gesture_atlas.png'];
 for(let i=0;i<8;i++)frames.push(makeFrame(atlas,i));
}
function poseAt(t){let k=0;for(let i=0;i<8;i++)if(t>=times[i])k=i;return k;}
function drawActor(c,lt){
 const k=poseAt(lt),scale=3.2,left=-212,top=296;
 // The torso stays fixed. All change comes from authored/generated poses.
 c.save();
 // Crossfade only 2 rendered frames at a pose change to soften the cel change.
 const p=k?smooth(times[k],times[k]+.055,lt):1;
 if(k>0&&p<1){
  // Add premultiplied layers so shared opaque torso remains opaque.
  const m=mix.getContext('2d');m.clearRect(0,0,384,512);m.globalCompositeOperation='source-over';m.globalAlpha=1-p;m.drawImage(frames[k-1],0,0);m.globalCompositeOperation='lighter';m.globalAlpha=p;m.drawImage(frames[k],0,0);m.globalAlpha=1;m.globalCompositeOperation='source-over';c.drawImage(mix,left,top,384*scale,512*scale);
 }else c.drawImage(frames[k],left,top,384*scale,512*scale);
 c.restore();
}
function event(c,lt,t){
 const gt=t+offset;
 c.save();A.camera(c,1.035,540,1000);A.exterior(c,gt);c.restore();
 // Keep the action readable in one shot; a new crop cannot repair missing poses.
 drawActor(c,lt);
 // A shallow foreground breath of haze, not an opaque character glow.
 c.save();c.globalCompositeOperation='screen';
 const g=c.createRadialGradient(45,1280,0,45,1280,200);g.addColorStop(0,`rgba(139,165,182,${.025+.01*Math.sin(t)})`);g.addColorStop(1,'rgba(139,165,182,0)');c.fillStyle=g;c.fillRect(0,1080,245,400);c.restore();
}
const assetList=A.assets.concat(['assets/gesture_atlas.png']);
ERAS.forEach(e=>e.assets=assetList);
SCENES.gesture={init,draw:event};
// Same shot and held pose across the lyric boundary; no arm reset at a wide cut.
SCENES.hold={init,draw(c,lt,t){event(c,lt+2.5,t);}};
window.PROBE_POSE_AT=poseAt;
})();
