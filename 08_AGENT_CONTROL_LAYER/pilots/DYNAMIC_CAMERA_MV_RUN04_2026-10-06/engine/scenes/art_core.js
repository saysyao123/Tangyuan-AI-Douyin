/* GPT-painted assets + deterministic limited animation. No video model.
 * The shoe anchor stays fixed. Paper translations are paper motion,
 * not walking. Canvas consumes source pixels without editing source files. */
(() => {
const W=1080,H=1920,PI=Math.PI,plates={};
const clamp=x=>Math.max(0,Math.min(1,x));
const S=(a,b,t)=>{let p=clamp((t-a)/(b-a));return p*p*(3-2*p);};
const assets=['bridge','woman','memory','room','close'].map(k=>'assets/'+k+'.png');
const photo=document.createElement('canvas');photo.width=900;photo.height=650;
const lyric=['如果爱有尽头','怎么想念没有','我该如何拼凑','没有你的以后','你随时光远走','回忆却总逗留','怪我太过念旧','迟迟不肯退后'];
const bounds=[0,2.5,5.75,8,10.75,13.75,16.25,18.75,21.360907];
function seed(n){let x=(n*1103515245+12345)>>>0;return(x&0x7fffffff)/2147483648;}
function init(IM){
 if(plates.bridge)return;
 U.assertGlyphs('LXGWWenKai-500',lyric.join('')+'若爱有尽头','MV歌词');
 for(const k of ['bridge','room','close']){let cv=document.createElement('canvas');cv.width=W;cv.height=H;cv.getContext('2d').drawImage(IM['assets/'+k+'.png'],0,0,W,H);plates[k]=cv;}
 const p=photo.getContext('2d');p.fillStyle='#c7b697';p.fillRect(0,0,900,650);
 p.drawImage(IM['assets/memory.png'],280,200,790,570,13,13,874,624);
 p.strokeStyle='rgba(72,53,34,.45)';p.lineWidth=2;p.strokeRect(7,7,886,636);
}
function camera(c,z,x=540,y=1050){c.translate(x,y);c.scale(z,z);c.translate(-x,-y);}
function water(c,plate,t,rects){
 for(const r of rects){c.save();c.beginPath();c.rect(...r);c.clip();
  for(let y=r[1];y<r[1]+r[3];y+=5){let dep=(y-r[1])/r[3],dx=Math.sin(y*.042-t*2.5)*(1.2+dep*5.0)+Math.sin(y*.011+t*1.3)*2.5;c.drawImage(plate,0,y,W,6,dx,y,W,6);}c.restore();}
}
function veil(c,t,x,y,w,h,alpha){c.save();c.globalCompositeOperation='screen';const g=c.createRadialGradient(x+Math.sin(t*.22)*35,y,0,x,y,w*.55);g.addColorStop(0,`rgba(137,166,183,${alpha})`);g.addColorStop(1,'rgba(98,134,156,0)');c.fillStyle=g;c.fillRect(x-w/2,y-h/2,w,h);c.restore();}
function dust(c,t,n=14,alpha=.15){
 c.save();c.fillStyle='#dfc5a0';for(let i=0;i<n;i++){const x=70+seed(i+22)*940+Math.sin(t*.32+i)*11,y=650+((seed(i+56)*680-t*(4+seed(i+4)*5))%720+720)%720;c.globalAlpha=alpha*(.4+.6*Math.pow(Math.sin(t*.6+i),2));c.beginPath();c.arc(x,y,.8+seed(i+7)*1.5,0,PI*2);c.fill();}c.restore();
}
function willow(c,plate,t){
 const l=400;c.save();c.beginPath();c.moveTo(0,0);c.lineTo(l,0);c.lineTo(310,760);c.lineTo(0,920);c.closePath();c.clip();
 for(let x=0;x<l;x+=12){const dx=Math.sin(t*1.9+x*.018)*9*(1-x/l);c.drawImage(plate,x,0,13,920,x+dx,0,13,920);}c.restore();
}
function exterior(c,t){
 const b=plates.bridge;c.drawImage(b,0,0);water(c,b,t,[[0,935,1080,90],[515,1390,560,350]]);willow(c,b,t);veil(c,t,630,830,850,330,.035+.012*Math.sin(t*.55));
 c.save();c.globalCompositeOperation='screen';for(const[x,y]of[[1010,868],[793,887],[692,865],[115,840]]){let g=c.createRadialGradient(x,y,1,x,y,17);g.addColorStop(0,`rgba(221,148,71,${.07+.03*Math.sin(t*1.4+x)})`);g.addColorStop(1,'rgba(221,148,71,0)');c.fillStyle=g;c.fillRect(x-17,y-17,34,34);}c.restore();
}
function actor(c,t,IM){
 const im=IM['assets/woman.png'],sc=.414,dx=388-561*sc,dy=1215-1571*sc;
 c.save();c.translate(dx,dy);c.scale(sc,sc);
 for(let x=0;x<420;x+=10){const w=Math.min(11,420-x),q=Math.pow(1-x/420,1.5),yy=(Math.sin(t*2.4+x*.009)*68+Math.sin(t*3.1+x*.02)*13)*q;c.drawImage(im,x,0,w,im.height,x,yy,w,im.height);}
 c.drawImage(im,420,0,im.width-420,im.height,420,0,im.width-420,im.height);c.restore();
}
function thread(c,t){
 const hx=493,hy=951,end=S(.65,1.65,t);c.save();c.strokeStyle='rgba(176,70,54,.94)';c.lineWidth=2.3;c.lineCap='round';c.beginPath();c.moveTo(hx,hy);c.bezierCurveTo(502,1010,510+Math.sin(t*1.7)*8,1031,550-end*19,1042+end*35);c.stroke();c.beginPath();c.moveTo(550+end*21,1042+end*45);c.bezierCurveTo(617,1012+Math.sin(t*1.1)*9,721,1055,884,1089);c.stroke();c.restore();
}
function bridge(c,t,IM,which){
 const local=which===0?t:which===1?t-2.5:t-18.75,z=which===0?1.055+.035*S(0,2.5,local):which===1?1.15+.045*S(0,3.25,local):1.085-.04*S(0,2.6,local);
 c.save();camera(c,z,which===1?450:540,1000);exterior(c,t);actor(c,t,IM);thread(c,t);dust(c,t,12,.13);c.restore();
}
function room(c,t,local){
 const b=plates.room;c.save();camera(c,1.035+.035*S(0,2.75,local),600,1050);c.drawImage(b,0,0);water(c,b,t,[[242,673,450,96]]);
 c.save();c.beginPath();c.moveTo(0,90);c.lineTo(135,90);c.lineTo(240,985);c.lineTo(0,985);c.closePath();c.clip();for(let y=90;y<985;y+=6){const dx=Math.sin(t*2.3+y*.007)*20*S(130,830,y);c.drawImage(b,0,y,250,7,dx,y,250,7);}c.restore();
 let g=c.createRadialGradient(354,914,1,354,914,130);g.addColorStop(0,`rgba(233,160,82,${.08+.025*Math.sin(t*5.1)+.01*Math.sin(t*9.7)})`);g.addColorStop(1,'rgba(233,160,82,0)');c.save();c.globalCompositeOperation='screen';c.fillStyle=g;c.fillRect(224,784,260,260);c.restore();
 U.steam(c,t,{x:384,y:1030,h:95,w:2,n:2,color:'rgba(188,202,204,.32)',wobble:7,spread:8,speed:.45});dust(c,t,11,.16);c.restore();
}
const seams=[[[0,0],[402,0],[406,168],[398,325],[0,325]],[[402,0],[900,0],[900,325],[398,325],[406,168]],[[0,325],[398,325],[410,480],[402,650],[0,650]],[[398,325],[900,325],[900,650],[402,650],[410,480]]];
function piece(c,index,ox,oy,ang,alpha){
 const pts=seams[index],cx=index%2?650:205,cy=index<2?165:490;c.save();c.translate(ox,oy);c.translate(cx,cy);c.rotate(ang);c.translate(-cx,-cy);c.globalAlpha=alpha;c.beginPath();pts.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.closePath();c.shadowColor='rgba(0,0,0,.36)';c.shadowBlur=20;c.shadowOffsetY=10;c.fillStyle='#c7b697';c.fill();c.shadowColor='transparent';c.save();c.clip();c.drawImage(photo,0,0);c.restore();c.strokeStyle='rgba(167,146,118,.65)';c.lineWidth=1.8;c.stroke();c.restore();
}
function memory(c,t,local,mode){
 if(mode==='depart')room(c,t,local);else{c.save();camera(c,1.035,540,950);exterior(c,t);c.restore();}c.fillStyle=mode==='depart'?'rgba(5,12,20,.23)':'rgba(4,16,27,.40)';c.fillRect(0,0,W,H);
 const join=S(0,1.45,local),gone=S(.25,2.55,local);c.save();c.translate(540,960);c.rotate((-2.3+Math.sin(t*.55)*.5)*PI/180);c.translate(-450,-325);
 for(let i=0;i<4;i++){const side=i%2?1:-1,down=i<2?-1:1;let x=0,y=0,a=0,opacity=1;
  if(mode==='join'){x=side*(128*(1-join)+2.5*Math.sin(t*2.1));y=down*(120*(1-join)+3.5*Math.sin(t*1.7));a=side*.1*(1-join)+Math.sin(t*1.5+i)*.004;}
  if(mode==='depart'&&side===1){x=gone*510;y=-gone*230;a=gone*.28;opacity=1-.75*gone;}
  if(mode==='linger'){const ret=1-S(0,.7,local);x=side*(ret*95+3.5+Math.sin(t*2.4)*5);y=down*Math.sin(t*2.2)*6;a=Math.sin(t*2.1+i)*.008;}piece(c,i,x,y,a,opacity);
 }c.restore();c.save();c.strokeStyle='rgba(158,67,53,.62)';c.lineWidth=2;c.beginPath();c.moveTo(155,1440);c.bezierCurveTo(310,1320+Math.sin(t)*11,485,1440,585,1350);c.bezierCurveTo(655,1300,830,1315,900,1400+Math.sin(t*.8)*12);c.stroke();c.restore();dust(c,t,15,.2);
}
function close(c,t,local){
 const b=plates.close;c.save();camera(c,1.035+.035*S(0,2.5,local),660,1000);c.drawImage(b,0,0);
 c.save();c.beginPath();c.moveTo(0,780);c.lineTo(290,820);c.lineTo(315,1340);c.lineTo(105,1790);c.lineTo(0,1790);c.closePath();c.clip();for(let y=780;y<1790;y+=6){const dx=Math.sin(t*2.7+y*.009)*16*S(830,1300,y);c.drawImage(b,0,y,350,7,dx,y,350,7);}c.restore();water(c,b,t,[[4,1080,145,350],[935,850,145,440]]);dust(c,t,9,.12);c.restore();
}
window.GLOBAL_OVERLAY=(c,t)=>{
 let k=0;for(let i=0;i<8;i++)if(t>=bounds[i])k=i;c.save();let g=c.createLinearGradient(0,1450,0,1920);g.addColorStop(0,'rgba(4,11,19,0)');g.addColorStop(.54,'rgba(4,11,19,.59)');g.addColorStop(1,'rgba(4,11,19,.76)');c.fillStyle=g;c.fillRect(0,1450,W,470);
 const edge=Math.min(S(0,.14,t-bounds[k]),1-S(bounds[k+1]-.10,bounds[k+1],t));c.globalAlpha=.75+.25*edge;c.fillStyle='#eee7d8';c.font='52px "LXGWWenKai-500"';c.textAlign='center';c.textBaseline='middle';c.shadowColor='rgba(0,0,0,.7)';c.shadowBlur=12;c.letterSpacing='3px';c.fillText(lyric[k],540,1645);c.shadowBlur=0;c.globalAlpha=.43;c.font='23px "NotoSansSC-500"';c.letterSpacing='6px';c.fillText('若爱有尽头',540,1735);c.restore();
};
window.MV_ART={init,bridge,exterior,close,room,camera,plates,assets,photo,actor,thread,dust,water};
})();
