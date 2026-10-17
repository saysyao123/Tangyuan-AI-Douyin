/* T23 — opt-in, progressive classic-JRPG hints for the existing first act.
   No plot events, save serialization, native movement or combat are changed.
   The old T18 shell remains the source of truth for objectives and UI.
*/
(function () {
  'use strict';
  const hintSteps = [
    {scene:'fair', key:'bought', target:'vendor', clue:'摊市人声鼎沸。先看看有什么适合带给同伴的小吃。', detail:'先找摆摊的商贩交谈；走到人物旁可按空格，也可点击人物。'},
    {scene:'fair', key:'shared', target:'vendor', clue:'买到了点心，别忘记同行的人。', detail:'回到卖点心的位置附近，完成与同伴的分享。'},
    {scene:'fair', key:'watched', target:'stage', clue:'人群正在往戏台聚集。跟着热闹往台前看看。', detail:'找到戏台前的演出触发位置。演出前需要先完成买点心与分享。'},
    {scene:'fair', key:'backstage_seen', target:'backstage-gate', clue:'台前的热闹暂歇，戏台侧面还留有通往后台的路。', detail:'从戏台一侧的后台入口进入。路口有剧情条件，先看完演出。'},
    {scene:'fair', key:'ending_seen', target:'exit', clue:'该从庙会回去了。沿原来的人行道寻找出口。', detail:'和庙会离开处的出口互动，继续旧街归途。'},
    {scene:'backstage', key:'backstage_seen', target:null, clue:'这里发生的事还没结束，先留在原地观察。', detail:'等待当前演出和人物对白结束；不要反复点击正在演出的角色。'},
    {scene:'backstage', key:'never', target:'return', clue:'后台已经安静下来。可以沿原路返回庙会。', detail:'找到返回庙会的出口，接着走上归家的旧街。'},
    {scene:'street', key:'stranger_seen', target:'stranger', clue:'旧街上有人似乎在等你。不妨先听听他说些什么。', detail:'沿街道找到那名陌生人，靠近并交谈。'},
    {scene:'street', key:'never', target:'home-road', clue:'事情说清楚了，沿旧街继续向住处走吧。', detail:'找到通往小院的道路出口；回头去庙会并不是本次归家的方向。'},
    {scene:'courtyard', key:'neighbor_seen', target:'neighbor', clue:'院里还有人守着日常杂事。先和邻居打个招呼。', detail:'走到小院里的邻居旁交谈，留意一旁的药锅。'},
    {scene:'courtyard', key:'chapter_complete', target:'home', clue:'院子已走过一圈，家门就在不远处。', detail:'找到自己家门口，完成第一幕的归家段落。'}
  ];
  function selectHint(sceneId, flags) {
    if (!flags || !['fair','backstage','street','courtyard'].includes(sceneId)) return null;
    if (flags.night_started || flags.chapter_complete) return null;
    const steps=hintSteps.filter(s=>s.scene===sceneId);
    return steps.find(s=>s.key==='never'||!flags[s.key])||null;
  }
  function directionHint(position, camera) {
    if(!position||!camera)return '';
    const x=16*(position.col-position.row)-camera.x, y=8*(position.col+position.row)-camera.y;
    if(x<16)return '目标在当前镜头左侧，可以沿通道继续探索。';
    if(x>304)return '目标在当前镜头右侧，可以沿通道继续探索。';
    if(y<14)return '目标在当前镜头上方，留意建筑旁的入口。';
    if(y>188)return '目标在当前镜头下方，留意前景道路。';
    return '目标已在当前画面中，留意闪烁的金色位置提示。';
  }
  if (typeof module!=='undefined' && module.exports) module.exports={selectHint,directionHint,hintSteps};
  if (typeof document==='undefined') return;
  const obj=document.getElementById('objective');
  const frame=document.getElementById('game');
  if(!obj||!frame) return;
  const host=obj.parentElement;
  const panel=document.createElement('div');
  panel.className='t23-guide';
  const button=document.createElement('button');
  button.type='button'; button.className='t23-guide-button';
  button.textContent='旅途提示 · 可选';
  button.setAttribute('aria-controls','t23-guide-text');button.setAttribute('aria-expanded','false');
  const text=document.createElement('p');text.id='t23-guide-text';text.hidden=true;
  text.setAttribute('aria-live','polite');
  const marker=document.createElement('div');
  marker.className='t23-guide-marker';marker.hidden=true;marker.setAttribute('aria-hidden','true');
  document.body.appendChild(marker);
  panel.append(button,text);host.appendChild(panel);
  let level=0,sceneKey='',targetId=null;
  const safeState=()=>{try{return frame.contentWindow?.__tpObserve?.readRuntime()||null}catch{return null}};
  const settle=()=>{
    const s=safeState();
    const step=s?selectHint(s.sceneId,s.story?.flags):null;
    if(!step){level=0;sceneKey='';text.hidden=true;button.hidden=!!s&&!!s.story?.flags?.chapter_complete;marker.hidden=true;button.setAttribute('aria-expanded','false');return}
    button.hidden=false;
    const key=s.sceneId+'|'+step.target+'|'+step.key;
    if(sceneKey!==key){sceneKey=key;level=0;text.hidden=true;marker.hidden=true;button.setAttribute('aria-expanded','false')}
    if(level) {
      button.textContent=level===1?'旅途提示 · 查看位置':'旅途提示 · 收起';
      text.textContent=level===1?step.clue:step.detail;
      text.hidden=false;button.setAttribute('aria-expanded','true');
    }else{button.textContent='旅途提示 · 可选';text.hidden=true;button.setAttribute('aria-expanded','false')}
    marker.hidden=true;
    if(level!==2||!step.target)return;
    const actor=s.actors?.find(a=>a.id==='entity:'+step.target);
    const pos=actor?.canonical;targetId=step.target;
    if(!pos||!s.camera){text.textContent=step.detail;return}
    text.textContent=step.detail+' '+directionHint(pos,s.camera);
    const x=16*(pos.col-pos.row)-s.camera.x,y=8*(pos.col+pos.row)-s.camera.y+4;
    if(x<10||x>310||y<12||y>189)return;
    try{
      const canvas=frame.contentWindow.document.getElementById('screen');
      if(!canvas)return;
      const f=frame.getBoundingClientRect(),c=canvas.getBoundingClientRect();
      marker.style.left=Math.round(f.left+c.left+x*c.width/320)+'px';
      marker.style.top=Math.round(f.top+c.top+y*c.height/200)+'px';
      marker.hidden=false;
    }catch{marker.hidden=true}
  };
  button.addEventListener('click',()=>{
    const s=safeState();
    if(!s)return;
    level=(level+1)%3;settle();
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)marker.hidden=true});
  setInterval(settle,400);
  settle();
})();