/* T29 real picture-based high detail houses, not procedural tiles.
 * Native Type PAL still owns scene/camera/actors/story/SAVE12 and all pointer input.
 * This is an opt-in art prototype on the unchanged T27 site, not an art-complete game.
 */
(()=>{
  'use strict';
  const screen=document.getElementById('screen');if(!screen)return;
  const houses={
    street:[{col:23,row:-1,width:360},{col:30,row:-8,width:360},{col:37,row:-15,width:360}],
    courtyard:[{col:25,row:-5,width:310},{col:32,row:-12,width:335},{col:40,row:-16,width:345},
      {col:28,row:-2,width:310},{col:35,row:-9,width:320},{col:43,row:-13,width:345}]
  };
  const art=new Image();art.decoding='async';art.src='./hd-house.png';
  const layer=document.createElement('canvas');layer.id='t29-hd-architecture';
  layer.width=1280;layer.height=800;
  layer.style.cssText='position:fixed;pointer-events:none;z-index:5;image-rendering:auto;';
  document.body.append(layer);
  const ctx=layer.getContext('2d',{alpha:true});let enabled=true,painted=0,errors=0,scene='',visible=0;
  const toggle=document.createElement('button');
  toggle.type='button';toggle.textContent='高清建筑：开 · 点击对比';
  toggle.style.cssText='position:fixed;right:10px;top:10px;z-index:8;cursor:pointer;background:#15202ce8;border:1px solid #c6a06e;border-radius:4px;color:#f4d6a5;padding:7px 12px;font:12px sans-serif;';
  toggle.onclick=()=>{enabled=!enabled;toggle.textContent=enabled?'高清建筑：开 · 点击对比':'高清建筑：关 · 点击恢复';};
  document.body.append(toggle);
  const pixel=(p,c)=>({x:4*(16*(p.col-p.row)-c.x),y:4*(8*(p.col+p.row)-c.y)});
  const align=()=>{const r=screen.getBoundingClientRect();Object.assign(layer.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});};
  function paint(s){
    ctx.clearRect(0,0,1280,800);visible=0;scene=s.sceneId||'';
    if(!enabled||!art.complete||!art.naturalWidth||!s.camera||!houses[scene])return;
    for(const h of houses[scene]){
      const p=pixel(h,s.camera),w=h.width,hei=art.naturalHeight*w/art.naturalWidth;
      const x=p.x-w*.53,y=p.y-hei*.86;
      if(x+w<0||x>1280||y+hei<0||y>800)continue;
      ctx.drawImage(art,x,y,w,hei);visible++;
    }
    // Keep all active actor hit targets visible and native; this is only a
    // conservative render mask, never a second movement/collision engine.
    ctx.globalCompositeOperation='destination-out';
    for(const a of s.actors||[]){
      if(!a.canonical||!(/^party:/.test(a.id)||/^entity:(stranger|neighbor|vendor|performer|audience-)/.test(a.id)))continue;
      const p=pixel(a.canonical,s.camera);
      if(p.x>-70&&p.x<1350&&p.y>-40&&p.y<850)ctx.fillRect(p.x-37,p.y-139,74,155);
    }
    ctx.globalCompositeOperation='source-over';
    if(s.dialogue||s.presentationBusy||s.battleActive||s.menuActive)ctx.clearRect(0,575,1280,225);
    painted++;
  }
  let last=0;const tick=t=>{try{
    align();if(t-last>65){last=t;const s=window.__tpObserve?.readRuntime?.();if(s)paint(s);}
  }catch(e){errors++;if(errors===1)console.warn('[T29 high detail]',e);}
  requestAnimationFrame(tick);};
  window.__t29Art=Object.freeze({read:()=>({scene,loaded:art.complete&&!!art.naturalWidth,enabled,painted,visible,errors,
      screenSize:[layer.width,layer.height],pointerTransparent:layer.style.pointerEvents==='none'})});
  requestAnimationFrame(tick);
})();