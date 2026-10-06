// Original scenes. Huashu time -> frame engine and easing are reused.
// All random geometry is seeded once; rendering never depends on the last frame.
(() => {
const W=1080,H=1920, C=U.clamp, L=U.lerp, S=U.ss;
const palettes={
 ink:{sky:'#e7e2d4',low:'#a7afb0',water:'#c4c9c3',hill:'#6d7c7b',far:'#a3aba4',bridge:'#777c70',edge:'#424f4b',person:'#273b3c',light:'#e5ddc4',red:'#a8453e',leaf:'#6b7d70',white:'#f5eedc'},
 paper:{sky:'#e3c88f',low:'#819e96',water:'#2c686d',hill:'#41717a',far:'#83a19a',bridge:'#c19163',edge:'#725950',person:'#233f4a',light:'#f8dc9c',red:'#ba5345',leaf:'#2e6770',white:'#f0dfba'},
 night:{sky:'#121d37',low:'#455d73',water:'#213e56',hill:'#314e61',far:'#4c6976',bridge:'#68787c',edge:'#243d4a',person:'#0e2737',light:'#eed2a0',red:'#df8078',leaf:'#3b6265',white:'#f0ddbd'}
};
const P=palettes[window.MV_STYLE||'night'];
const r=U.rng(1062026), stars=Array.from({length:160},()=>[r()*W,r()*760,0.6+r()*1.7,r()*6.28]);
const motes=Array.from({length:35},()=>[r()*W,r()*1550,4+r()*5,r()*6.28]);
const twigs=Array.from({length:45},(_,i)=>[30+i*12,165+r()*190,r()*6.28]);
const texture=document.createElement('canvas');texture.width=W;texture.height=H;
const tx=texture.getContext('2d'), nr=U.rng(90);
for(let i=0;i<90000;i++){tx.fillStyle=nr()>.5?'rgba(255,242,218,.055)':'rgba(5,20,25,.08)';tx.fillRect(nr()*W,nr()*H,1+nr()*2,1+nr()*2);}
const oval=(c,x,y,rx,ry,fill)=>{c.fillStyle=fill;c.beginPath();c.ellipse(x,y,rx,ry,0,0,Math.PI*2);c.fill();};
const path=(c,pts,fill,stroke,lw=2)=>{c.beginPath();pts.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));if(fill){c.closePath();c.fillStyle=fill;c.fill();}if(stroke){c.strokeStyle=stroke;c.lineWidth=lw;c.stroke();}};
function fog(c,x,y,rad,a){c.save();let g=c.createRadialGradient(x,y,0,x,y,rad);g.addColorStop(0,`rgba(223,219,193,${a})`);g.addColorStop(1,'rgba(223,219,193,0)');c.fillStyle=g;c.fillRect(x-rad,y-rad,rad*2,rad*2);c.restore();}
function sky(c,t){let g=c.createLinearGradient(0,0,0,1350);g.addColorStop(0,P.sky);g.addColorStop(.66,P.low);g.addColorStop(1,P.water);c.fillStyle=g;c.fillRect(0,0,W,H);
 if(window.MV_STYLE==='night'){for(const [x,y,z,ph] of stars){c.globalAlpha=.25+.25*Math.sin(t*.7+ph);oval(c,x,y,z,z,P.light);}c.globalAlpha=1;}
 fog(c,770,405,240,window.MV_STYLE==='night'?.08:.2);
 const mx=760,my=400;oval(c,mx,my,76,76,P.light);c.save();c.globalAlpha=.12;
 for(let i=0;i<12;i++)oval(c,mx+Math.sin(i*9)*50,my+Math.cos(i*13)*48,8+i,3+i,P.hill);c.restore();
 for(let j=0;j<4;j++){let y=730+j*78; c.beginPath();c.moveTo(-30,1300);
  for(let x=-30;x<=W+30;x+=12)c.lineTo(x,y-90*Math.sin(x*.006+j*1.7)-35*Math.sin(x*.012+j));
  c.lineTo(W+30,1300);c.fillStyle=j<2?P.far:P.hill;c.globalAlpha=.18+j*.12;c.fill();}
 c.globalAlpha=1;
 for(let j=0;j<4;j++)fog(c,180+j*300+Math.sin(t*.1+j)*22,790+j*67,270,.08);
}
function river(c,t){const g=c.createLinearGradient(0,1000,0,H);g.addColorStop(0,P.water);g.addColorStop(1,P.sky);c.fillStyle=g;c.fillRect(0,1080,W,H-1080);
 for(let i=0;i<95;i++){const y=1110+i*7.7, a=(y-1100)/750;let x=760+Math.sin(i*.3+t*1.4)*36;let w=8+a*160+(Math.sin(i*2.71)+1)*25;
  c.strokeStyle=P.light;c.globalAlpha=(1-a)*.19+.05;c.lineWidth=1+a*2;c.beginPath();c.moveTo(x-w,y);c.lineTo(x+w,y);c.stroke();}
 for(let i=0;i<42;i++){c.strokeStyle=P.far;c.globalAlpha=.12;c.lineWidth=1.5;const y=1160+i*16;let x=150+Math.sin(i*8.7)*110+Math.sin(t*.3+i)*12;c.beginPath();c.moveTo(x,y);c.bezierCurveTo(x+100,y-6,x+180,y+8,x+310,y);c.stroke();}c.globalAlpha=1;
}
function bridge(c){c.save();c.beginPath();c.moveTo(-30,1205);c.bezierCurveTo(245,1120,725,1035,1120,1105);c.lineTo(1120,1375);c.bezierCurveTo(850,1260,825,1190,708,1213);c.bezierCurveTo(555,1230,546,1390,310,1430);c.lineTo(-30,1480);c.closePath();c.fillStyle=P.bridge;c.fill();
 c.strokeStyle=P.edge;c.lineWidth=6;c.stroke();
 c.save();c.clip();c.globalAlpha=.18;const rr=U.rng(311);
 for(let i=0;i<500;i++){let x=rr()*W,y=1120+rr()*380;c.strokeStyle=rr()>.5?P.edge:P.light;c.lineWidth=1;c.strokeRect(x,y,20+rr()*50,13+rr()*12);}c.restore();
 c.beginPath();c.moveTo(-20,1135);c.bezierCurveTo(345,1035,735,999,1100,1060);c.strokeStyle=P.edge;c.lineWidth=14;c.stroke();
 c.strokeStyle=P.bridge;c.lineWidth=8;c.stroke();
 for(let x=0;x<1120;x+=76){let y=1100-75*Math.sin((x/W)*Math.PI*.85);c.beginPath();c.moveTo(x,y+55);c.lineTo(x,y-25);c.strokeStyle=P.edge;c.lineWidth=9;c.stroke();oval(c,x,y-26,8,8,P.bridge);}
 c.restore();}
function leaves(c,t,amount=1){c.save();
 for(let i=0;i<motes.length;i++){let [x,y,z,p]=motes[i];x=(x+t*(28+i%5)*amount)%1180-50;y=y+25*Math.sin(t*.5+p);c.save();c.translate(x,y);c.rotate(p+Math.sin(t*.4+p)*.6);c.globalAlpha=.25+(i%3)*.15;c.fillStyle=P.leaf;c.beginPath();c.moveTo(-z*3,0);c.quadraticCurveTo(0,-z*2,z*3,0);c.quadraticCurveTo(0,z*2,-z*3,0);c.fill();c.restore();}c.restore();}
function willow(c,t){c.save();c.strokeStyle=P.edge;c.lineWidth=23;c.lineCap='round';c.beginPath();c.moveTo(-20,90);c.bezierCurveTo(180,190,380,145,660,250);c.stroke();
 for(let [x,len,ph] of twigs){let top=180+x*.09, sway=32*Math.sin(t*1.2+ph);c.strokeStyle=P.leaf;c.lineWidth=2;c.beginPath();c.moveTo(x,top);c.bezierCurveTo(x+15+sway,top+80,x-15+sway,top+len-50,x+sway,top+len);c.stroke();
  for(let i=1;i<9;i++){let y=top+i*len/9; c.save();c.translate(x+sway*Math.sin(i/9*Math.PI),y);c.rotate(i%2?-.5:.5);oval(c,0,0,4,12,P.leaf);c.restore();}}
 c.restore();}
// Stylized geometric silhouette. Walk displacement and both foot contacts are
// derived from the same gait phase. During stance the world-space toe is fixed.
function person(c,x,y,scale,t,walk=false,alpha=1,turn=1){c.save();c.translate(x,y);c.scale(scale*turn,scale);c.globalAlpha=alpha;
 const phase=t/0.72, cyc=Math.floor(phase), u=phase-cyc;
 const trajectory=z=>715+146*S(0,2.55,z);
 const bob=walk?-Math.sin(u*Math.PI*2)*2:Math.sin(t*.6)*.5;
 c.translate(0,bob);c.strokeStyle=P.person;c.lineWidth=11;c.lineCap='round';
 if(walk){for(let k=0;k<2;k++){let v=phase+k*.5,q=v-Math.floor(v),st=(Math.floor(v)-k*.5)*.72,anchor=trajectory(st)+14*.78,endToe=14+(trajectory(st)-trajectory(st+.36))/.78, nextToe=14+(trajectory(st+.72)-trajectory(t))/.78,toe=q<.5?14+(trajectory(st)-trajectory(t))/.78:L(endToe,nextToe,MO.smooth((q-.5)*2)),lift=q<.5?0:11*Math.sin((q-.5)*Math.PI*2);c.beginPath();c.moveTo(k?6:-6,-55);c.lineTo(toe*.5,-27-lift*.3);c.lineTo(toe,-lift-bob);c.stroke();c.beginPath();c.moveTo(toe-3,-lift-bob);c.lineTo(toe+10,-lift-bob);c.stroke();}}
 else{c.beginPath();c.moveTo(-7,-55);c.lineTo(-8,0);c.moveTo(8,-55);c.lineTo(10,0);c.stroke();}
 c.fillStyle=P.person;c.beginPath();c.moveTo(-15,-151);c.quadraticCurveTo(-35,-106,-28,-48);c.quadraticCurveTo(0,-39,29,-48);c.lineTo(17,-149);c.closePath();c.fill();
 oval(c,0,-169,19,23,P.person);c.beginPath();c.moveTo(-20,-170);c.quadraticCurveTo(-31,-134,-10,-139);c.quadraticCurveTo(18,-142,18,-172);c.closePath();c.fill();
 const hold=S(16.25,18.5,t);c.strokeStyle=P.person;c.lineWidth=10;c.beginPath();c.moveTo(-15,-144);c.quadraticCurveTo(-35,-125,L(-10,2,hold),L(-110,-138,hold));c.moveTo(16,-145);c.quadraticCurveTo(30,-125,L(8,2,hold),L(-115,-138,hold));c.stroke();
 c.strokeStyle=P.red;c.lineWidth=5;c.beginPath();c.moveTo(-17,-144);c.quadraticCurveTo(22,-131,18,-144);c.stroke();
 c.beginPath();c.moveTo(14,-139);c.bezierCurveTo(30,-127,29+Math.sin(t*1.8)*7,-107,52+Math.sin(t*1.2)*10,-112);c.stroke();
 c.strokeStyle=P.light;c.globalAlpha=alpha*.16;c.lineWidth=2;c.beginPath();c.moveTo(-17,-147);c.quadraticCurveTo(-31,-115,-25,-65);c.stroke();c.restore();}
function ribbon(c,t,p=1,broken=true){c.save();c.strokeStyle=P.red;c.lineWidth=7;c.lineCap='round';c.shadowColor=P.red;c.shadowBlur=window.MV_STYLE==='night'?6:0;
 const separation=95*S(.3,2.1,t);c.beginPath();c.moveTo(409,997);c.bezierCurveTo(460,900+Math.sin(t)*10,500,950,560-separation/2,967);if(!broken)c.bezierCurveTo(590,960,620,900,695,982);c.stroke();
 if(broken){c.beginPath();c.moveTo(560+separation/2,967+Math.sin(t*1.1)*8*S(.3,2.1,t));c.bezierCurveTo(615,960,650,928,695,982);c.stroke();}
 if(t>2.5&&t<5.75){let q=(t-2.5)/3.25;c.globalAlpha=.75;c.beginPath();c.ellipse(540,960,40+q*120,20+q*60,Math.sin(t)*.1,0,Math.PI*2);c.lineWidth=2;c.stroke();}
 c.restore();}
function wide(c,t,local,mode=0){sky(c,t);river(c,t);bridge(c);willow(c,t);leaves(c,t);
 if(mode===4){let p=S(10.85,13.4,t);person(c,715+p*146,1090,.78,t-10.85,true,1,1);person(c,395,1127,1.12,t,false);ribbon(c,t,1,true);}
 else{person(c,395,1127,1.12,t);person(c,700,1085,.88,t,false,mode===7?0:.13,-1);ribbon(c,t,1,true);}
}
function memoryCard(c,x,y,rot,s,t,empty=false){c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s);c.shadowColor='rgba(0,0,0,.3)';c.shadowBlur=25;c.shadowOffsetY=14;c.fillStyle=P.white;c.fillRect(-145,-190,290,380);c.shadowBlur=0;c.shadowOffsetY=0;c.fillStyle=P.water;c.fillRect(-124,-166,248,276);
 c.save();c.beginPath();c.rect(-124,-166,248,276);c.clip();c.globalAlpha=.4;oval(c,60,-104,32,32,P.light);c.globalAlpha=1;
 c.fillStyle=P.hill;c.beginPath();c.moveTo(-150,60);c.bezierCurveTo(-25,-60,10,-20,140,50);c.lineTo(140,160);c.lineTo(-150,160);c.fill();
 person(c,-48,95,.65,t,false,1);if(!empty)person(c,51,81,.52,t,false,.75,-1);c.restore();c.strokeStyle=P.red;c.lineWidth=2;c.beginPath();c.moveTo(-78,144);c.quadraticCurveTo(0,133,78,144);c.stroke();c.restore();}
function puzzle(c,t,lt){sky(c,t);river(c,t);willow(c,t);let p=MO.anim(lt,.15,1.5,MO.smooth),gap=L(150,1.5,p);
 const pieces=[[-1,-1],[-1,1],[1,-1],[1,1]];
 for(let [a,b] of pieces){c.save();c.translate(a*gap,b*gap*.7);c.beginPath();c.rect(a<0?380:540,b<0?680:890,160,210);c.clip();memoryCard(c,540,890,0,1.05,t,false);c.restore();}
 leaves(c,t);}
function room(c,t,lt,photos=false){let g=c.createLinearGradient(0,0,1080,1920);g.addColorStop(0,P.sky);g.addColorStop(1,P.person);c.fillStyle=g;c.fillRect(0,0,W,H);
 const light=c.createLinearGradient(270,400,700,1400);light.addColorStop(0,P.light);light.addColorStop(1,'rgba(229,208,158,0)');
 c.save();c.globalAlpha=.1;c.fillStyle=light;path(c,[[210,350],[850,350],[1120,1700],[100,1700]],light);c.restore();
 c.fillStyle=P.edge;c.fillRect(205,215,675,690);c.fillStyle=P.water;c.fillRect(228,238,630,645);
 c.save();c.beginPath();c.rect(228,238,630,645);c.clip();c.translate(0,160);sky(c,t);willow(c,t);c.restore();
 c.strokeStyle=P.edge;c.lineWidth=15;c.strokeRect(225,235,635,645);c.beginPath();c.moveTo(542,238);c.lineTo(542,885);c.moveTo(228,680);c.lineTo(858,680);c.stroke();
 for(let side of [0,1]){let x=side?858:225;c.fillStyle=P.far;c.globalAlpha=.25;c.beginPath();c.moveTo(x,215);c.bezierCurveTo(x+(side?-80:80),400,x+(side?-65:65)+Math.sin(t*1.8)*45,600,x+(side?-140:140),915);c.lineTo(x,915);c.closePath();c.fill();c.globalAlpha=1;}
 c.fillStyle=P.bridge;c.beginPath();c.ellipse(536,1125,340,58,0,0,Math.PI*2);c.fill();c.strokeStyle=P.edge;c.lineWidth=18;c.beginPath();c.moveTo(312,1140);c.lineTo(270,1500);c.moveTo(767,1140);c.lineTo(809,1500);c.stroke();
 for(let k=0;k<2;k++){let x=390+k*292;oval(c,x,1090,44,15,P.light);c.fillStyle=P.light;c.fillRect(x-40,1060,80,32);c.strokeStyle=P.light;c.lineWidth=8;c.beginPath();c.arc(x+47,1070,15,-1.4,1.4);c.stroke();c.strokeStyle=P.white;c.globalAlpha=k?.07:.6;c.lineWidth=5;c.beginPath();c.moveTo(x,1039);c.bezierCurveTo(x-14+Math.sin(t)*8,1015,x+14,990,x,964);c.stroke();c.globalAlpha=1;}
 for(let k=0;k<2;k++){let x=260+k*580;c.fillStyle=P.person;let shift=k===1?38*MO.anim(lt,.1,2.4,MO.smooth):0;c.save();c.translate(shift,0);c.fillRect(x-65,1230,130,22);c.fillRect(x-59,1190,12,210);c.fillRect(x+46,1190,12,210);c.fillRect(x-65,1200,130,18);c.restore();}
 if(photos){for(let i=0;i<3;i++){let x=310+i*244,y=760+Math.sin(t*.6+i)*16;memoryCard(c,x,y,(i-1)*.16+Math.sin(t*.5+i)*.03,.55,t,i===2);}}
 else{person(c,242,1300,1.22,t,false,1);}
 leaves(c,t,.3);}
function echo(c,t,lt){sky(c,t);river(c,t);let p=S(.1,2.4,lt);c.save();c.translate(0,-80);memoryCard(c,540+Math.sin(lt*1.1)*32,900,-.08+Math.sin(lt*1.3)*.18,1.1,t);c.restore();
 for(let i=0;i<3;i++){let q=(t*.2+i/3)%1;c.save();c.strokeStyle=P.red;c.globalAlpha=(1-q)*.2;c.lineWidth=2;c.beginPath();c.ellipse(540,1310,130+q*270,20+q*50,0,0,Math.PI*2);c.stroke();c.restore();}leaves(c,t);}
function clasp(c,t,lt){wide(c,t,lt,7);c.save();let z=1+MO.anim(lt,0,2.5,MO.smooth)*.28;c.translate(400,1070);c.scale(z,z);c.translate(-400,-1070);c.clearRect(0,0,0,0);c.restore();
 let g=c.createRadialGradient(407,964,0,407,964,100);g.addColorStop(0,'rgba(233,130,105,.13)');g.addColorStop(1,'rgba(233,130,105,0)');c.fillStyle=g;c.fillRect(300,860,220,220);}
function frame(c,i,lt,t){c.save();c.resetTransform();c.clearRect(0,0,W,H);
 // A gentle single-direction push within a shot; no oscillating camera zoom.
 const p=C(lt/2.8), z=i===0?1+.14*p:i===1?1.42+.18*MO.smooth(p):i===6?1.38+.18*MO.smooth(p):i===7?1.45-.36*MO.smooth(p):1+.07*p;
 const ax=i===6?410:540,ay=(i===1||i===6)?1010:H*.52;c.translate(ax,ay);c.scale(z,z);c.translate(-ax,-ay);
 if(i===2)puzzle(c,t,lt);else if(i===3)room(c,t,lt);else if(i===5)echo(c,t,lt);else if(i===6)clasp(c,t,lt);else wide(c,t,lt,i);
 c.restore();c.save();c.globalAlpha=window.MV_STYLE==='paper'?.9:.7;c.drawImage(texture,0,0);c.restore();
 // Bottom is a calm, independent subtitle layer; scenery never cuts text.
 let g=c.createLinearGradient(0,1490,0,H);g.addColorStop(0,'rgba(4,15,27,0)');g.addColorStop(1,window.MV_STYLE==='ink'?'rgba(28,41,42,.40)':'rgba(5,18,31,.85)');c.fillStyle=g;c.fillRect(0,1490,W,430);
}
for(let i=0;i<8;i++)SCENES[`l${String(i+1).padStart(2,'0')}`]={init(){U.assertGlyphs('LXGWWenKai-500','若爱有尽头如果爱有尽头怎么想念没有我该如何拼凑没有你的以后你随时光远走回忆却总逗留怪我太过念旧迟迟不肯退后','歌词');},draw(c,lt,t){frame(c,i,lt,t);}};
const lyrics=['如果爱有尽头','怎么想念没有','我该如何拼凑','没有你的以后','你随时光远走','回忆却总逗留','怪我太过念旧','迟迟不肯退后'], bounds=[0,2.5,5.75,8,10.75,13.75,16.25,18.75,21.360907];
window.GLOBAL_OVERLAY=(c,t)=>{let i=0;for(let j=0;j<8;j++)if(t>=bounds[j])i=j;c.save();c.fillStyle=P.white;c.textAlign='center';c.textBaseline='middle';c.font='52px "LXGWWenKai-500"';c.shadowColor='rgba(0,0,0,.5)';c.shadowBlur=8;c.fillText(lyrics[i],W/2,1660);c.shadowBlur=0;
 c.globalAlpha=.55;c.font='22px "NotoSansSC-500"';c.fillText('若爱有尽头',W/2,1750);c.restore();};
})();
