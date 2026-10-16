const frame=document.getElementById('game'),loading=document.getElementById('loading'),hint=document.getElementById('load-hint'),retry=document.getElementById('retry');
const held=new Map();let started=performance.now(),lastState='',ready=false;
function key(k,type){try{frame.contentWindow.dispatchEvent(new KeyboardEvent(type,{key:k,bubbles:true,cancelable:true}))}catch{}}
function releaseAll(){for(const k of new Set(held.values()))key(k,'keyup');held.clear();try{frame.contentWindow.dispatchEvent(new Event('blur'))}catch{}}
for(const b of document.querySelectorAll('[data-key]')){
 b.addEventListener('pointerdown',e=>{e.preventDefault();if(!ready)return;frame.contentWindow.focus();held.set(e.pointerId,b.dataset.key);key(b.dataset.key,'keydown');b.setPointerCapture(e.pointerId)});
 const release=e=>{const k=held.get(e.pointerId);if(!k)return;held.delete(e.pointerId);if(![...held.values()].includes(k))key(k,'keyup')};
 for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,release);
 b.addEventListener('click',e=>{if(e.detail!==0||!ready)return;frame.contentWindow.focus();key(b.dataset.key,'keydown');setTimeout(()=>key(b.dataset.key,'keyup'),70)});
}
window.addEventListener('blur',releaseAll);window.addEventListener('pagehide',releaseAll);document.addEventListener('visibilitychange',()=>{if(document.hidden)releaseAll()});
document.getElementById('fullscreen').onclick=()=>{releaseAll();frame.requestFullscreen().then(()=>frame.contentWindow.focus()).catch(()=>{hint.textContent='当前浏览器不支持全屏，可直接在页面内继续。'})};
retry.onclick=()=>{releaseAll();ready=false;lastState='';started=performance.now();retry.hidden=true;hint.textContent='正在重新载入…';frame.src=frame.src};
frame.onload=()=>{releaseAll();if(!document.hidden)frame.contentWindow.focus()};
function update(){
 try{
  const win=frame.contentWindow,error=win.document.documentElement.dataset.bootError;
  if(error){ready=false;loading.hidden=false;hint.textContent='载入未完成，请重试。'+error;retry.hidden=false;return}
  const s=win.__tpObserve?.readRuntime();if(!s){if(performance.now()-started>15000){hint.textContent='载入时间较长，你可以继续等待或重试。';retry.hidden=false}return}
  ready=true;loading.hidden=true;
  const f=s.story.flags,stamp=JSON.stringify([s.sceneId,s.battleActive,f,s.story.party]);if(stamp===lastState)return;lastState=stamp;
  document.getElementById('place').textContent=s.battleActive?'雾林 · 回合战斗':s.sceneId==='inn'?'雾灯驿站':'雾林小道';
  const done=[f.quest_started,s.sceneId==='forest'||f.core_taken||f.wolf_defeated,f.core_taken,f.wolf_defeated,f.ending_seen];document.querySelectorAll('#quests li').forEach((li,i)=>li.classList.toggle('done',!!done[i]));
  document.getElementById('health').textContent='体力 '+s.story.party[0].hp+'/'+s.story.party[0].maxHP;
  document.querySelector('h1').innerHTML=f.ending_seen?'灯火<em><br>重明。</em>':'把灯火<br><em>带回家。</em>';
 }catch{hint.textContent='暂时无法连接游戏画面，请重新载入。';retry.hidden=false}
}
setInterval(update,250);update();
