// Project scenes for real GPT-native illustration assets, plugged into Huashu's original SCENES API.
// No generated human animation is claimed: L07/L08 actor is a static GPT frame pending motion keyframes.
(() => {
const W=1080,H=1920;
const shots={
l01:{img:'assets/gpt/L01_clean.png',caption:'如果爱有尽头'},
l04:{img:'assets/gpt/L04_hero.png',caption:'没有你的以后'},
l07:{img:'assets/gpt/L07_clean.png',photo:'assets/gpt/L07_photo.png',caption:'怪我太过念旧'},
l08:{img:'assets/gpt/L08_hero.png',caption:'迟迟不肯退后'}
};
function ease(a,b,t){let p=Math.max(0,Math.min(1,(t-a)/(b-a)));return p*p*(3-2*p)}
function weather(c,t,quiet=false){
  c.save();c.lineWidth=.8;
  for(let i=0;i<58;i++){
    const x=((i*179.7+Math.sin(i*93.2)*113+t*(24+i%7*7))%1150+1150)%1150-35;
    const y=((i*267.9+t*(165+i%9*19))%2100+2100)%2100-90;
    c.strokeStyle=quiet?'rgba(186,198,211,.075)':'rgba(185,199,212,.12)';
    c.beginPath();c.moveTo(x,y);c.lineTo(x-4,y+16+(i%5)*3);c.stroke();
  }c.restore();
}
function ambient(c,t,id) {
  if(id==='l04'){
    const xy=[[255,1110],[766,1040]];
    for(const [cx,cy] of xy){
      c.save();c.lineWidth=2;c.strokeStyle='rgba(224,205,179,.15)';
      for(let j=0;j<2;j++) {
        c.beginPath();
        for(let i=0;i<=25;i++){
          const u=i/25,x=cx+(j-.5)*10+u*11*Math.sin(t*1.2+u*4+j);
          const y=cy-u*87-t%1*4;
          if(i===0)c.moveTo(x,y);else c.lineTo(x,y);
        }c.stroke();
      }c.restore();
    }
    const breath=.045+.014*Math.sin(t*1.7);
    const g=c.createRadialGradient(130,1004,0,130,1004,310);
    g.addColorStop(0,'rgba(250,163,85,'+breath+')');g.addColorStop(1,'rgba(250,163,85,0)');
    c.fillStyle=g;c.fillRect(0,650,500,650);
  }
}
function thread(c,t) {
  const sx=747*W/941,sy=859*H/1672;
  const ex=941*W/941,ey=818*H/1672,peak=1.03;
  c.save();c.lineWidth=2.3;c.strokeStyle='rgba(191,78,62,.93)';
  c.shadowColor='rgba(250,107,82,.38)';c.shadowBlur=4;
  if(t<peak){
    c.beginPath();c.moveTo(sx,sy);
    c.quadraticCurveTo((sx+ex)/2,(sy+ey)/2+Math.sin(t*7)*2,ex,ey);
    c.stroke();
  } else {
    const dt=t-peak,k=ease(0,.72,dt);
    c.beginPath();c.moveTo(sx,sy);
    c.quadraticCurveTo(sx+9,sy+13*k,sx+19,sy+9+7*k);c.stroke();
    c.beginPath();c.moveTo(sx+37+k*90,sy-9-k*6);
    c.quadraticCurveTo(ex+k*62-50,ey+Math.sin(t*2)*3,ex+k*180,ey-16*k);c.stroke();
    const gl=(1-ease(0,.22,dt));
    if(gl>0){c.globalAlpha=gl*.8;c.fillStyle='rgba(253,190,125,.7)';c.beginPath();c.arc(sx+25,sy-2,2+gl*4,0,2*Math.PI);c.fill();}
  }
  c.restore();
}
function loosePhoto(c,t,im) {
  // Object-only movement using a transparent cutout and a repaired source still.
  const k=ease(.33,1.78,t),q=ease(1.82,2.42,t);
  let x=785*W/941,y=327*H/1672,w=145*W/941,h=169*H/1672;
  x+=33*k-12*q+3*Math.sin(t*1.6)*k;
  y-=36*k+8*q+2*Math.sin(t*2.3)*k;
  c.save();c.translate(x+w/2,y+h/2);c.rotate((-.08*k+.027*Math.sin(t*2))*k);
  c.drawImage(im,-w/2,-h/2,w,h);c.restore();
}
function footer(c,caption){
 const grad=c.createLinearGradient(0,1480,0,H);
 grad.addColorStop(0,'rgba(4,11,19,0)');grad.addColorStop(1,'rgba(4,11,19,.74)');
 c.fillStyle=grad;c.fillRect(0,1480,W,440);
 c.save();c.textAlign='center';c.textBaseline='middle';
 c.shadowColor='rgba(0,0,0,.55)';c.shadowBlur=12;
 c.fillStyle='#f5eade';c.font='52px "LXGWWenKai-500"';
 c.fillText(caption,W/2,1660);c.shadowBlur=0;
 c.globalAlpha=.52;c.font='23px "NotoSansSC-500"';c.fillText('若爱有尽头',W/2,1745);c.restore();
}
function draw(id,c,t,IMG) {
 c.clearRect(0,0,W,H);c.drawImage(IMG[shots[id].img],0,0,W,H);
 if(id==='l01')thread(c,t);
 if(id==='l07')loosePhoto(c,t,IMG[shots[id].photo]);
 ambient(c,t,id);weather(c,t,id==='l04');
 footer(c,shots[id].caption);
}
for(const id of Object.keys(shots)){
 SCENES[id]={
  init(){U.assertGlyphs('LXGWWenKai-500',shots[id].caption,'GPT 镜头歌词')},
  draw(c,lt,t,IMG){draw(id,c,lt,IMG)}
 };
}
})();
