const frame=document.getElementById('game'),loading=document.getElementById('loading'),hint=document.getElementById('load-hint'),retry=document.getElementById('retry'),status=document.getElementById('save-status');
const held=new Map();let started=performance.now(),lastState='',ready=false,lastFrames=-1,lastDraws=-1,lastProgress=performance.now(),notice=-1;
function key(k,type){try{frame.contentWindow.dispatchEvent(new KeyboardEvent(type,{key:k,bubbles:true,cancelable:true}))}catch{}}
function releaseAll(){for(const k of new Set(held.values()))key(k,'keyup');held.clear();try{frame.contentWindow.dispatchEvent(new Event('blur'))}catch{}}
function showRecovery(message){ready=false;releaseAll();loading.hidden=false;hint.textContent=message;retry.hidden=false}
for(const b of document.querySelectorAll('[data-key]')){
 b.addEventListener('pointerdown',e=>{e.preventDefault();if(!ready)return;frame.contentWindow.focus();held.set(e.pointerId,b.dataset.key);key(b.dataset.key,'keydown');b.setPointerCapture(e.pointerId)});
 const release=e=>{const k=held.get(e.pointerId);if(!k)return;held.delete(e.pointerId);if(![...held.values()].includes(k))key(k,'keyup')};
 for(const event of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(event,release);
 b.addEventListener('click',e=>{if(e.detail!==0||!ready)return;frame.contentWindow.focus();key(b.dataset.key,'keydown');setTimeout(()=>key(b.dataset.key,'keyup'),70)});
}
window.addEventListener('blur',releaseAll);window.addEventListener('pagehide',releaseAll);document.addEventListener('visibilitychange',()=>{releaseAll();lastProgress=performance.now()});
document.getElementById('fullscreen').onclick=()=>{releaseAll();frame.requestFullscreen().then(()=>frame.contentWindow.focus()).catch(()=>{status.textContent='当前浏览器不支持全屏，可直接在页面内继续。'})};
retry.onclick=()=>{releaseAll();ready=false;lastState='';lastFrames=-1;lastDraws=-1;notice=-1;started=lastProgress=performance.now();loading.hidden=false;retry.hidden=true;hint.textContent='正在重新载入…已保存的进度可在载入后读取。';frame.src=frame.src};
frame.onload=()=>{releaseAll();lastProgress=performance.now();if(!document.hidden)frame.contentWindow.focus()};
document.getElementById('backup').onclick=async()=>{
 try{if(!ready)throw Error('请等待游戏载入。');const text=await frame.contentWindow.tpPlayer.exportQuickSave();const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='lantern-inn-save.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='已导出上次保存的进度；当前未保存的操作不在备份中。'}catch(e){status.textContent='备份失败：'+e.message}
};
document.getElementById('restore').onchange=async e=>{
 const file=e.target.files[0];e.target.value='';if(!file)return;
 try{if(!ready)throw Error('请等待游戏载入。');if(file.size>5000000)throw Error('备份文件过大。');if(!confirm('将用所选备份覆盖快速存档；当前画面暂不改变。确认后可按“读取进度”恢复。'))return;await frame.contentWindow.tpPlayer.importQuickSave(await file.text());status.textContent='备份已导入快速存档。请按“读取进度”恢复。'}catch(error){status.textContent='导入失败，原存档保留：'+error.message}
};
function update(){
 try{
  const win=frame.contentWindow,doc=win.document.documentElement;
  if(doc.dataset.bootError||doc.dataset.runtimeError){showRecovery('游戏暂时未能继续。重新载入后可读取已保存的进度，未保存的操作会丢失。');return}
  const s=win.__tpObserve?.readRuntime();if(!s){if(performance.now()-started>15000){hint.textContent='载入时间较长，可以继续等待或重试。';retry.hidden=false}return}
  const now=performance.now();if(s.health.frames!==lastFrames&&s.health.draws!==lastDraws){lastFrames=s.health.frames;lastDraws=s.health.draws;lastProgress=now}
  if(!document.hidden&&now-lastProgress>8000){showRecovery('游戏画面已较长时间未更新。可重新载入后读取已保存的进度，未保存的操作会丢失。');return}
  ready=true;loading.hidden=true;retry.hidden=true;
  if(s.health.storage.sequence!==notice){notice=s.health.storage.sequence;if(s.health.storage.message)status.textContent=s.health.storage.message}
  const f=s.story.flags,stamp=JSON.stringify([s.sceneId,s.battleActive,f,s.story.party]);if(stamp===lastState)return;lastState=stamp;
  document.getElementById('place').textContent=s.battleActive?'雾林 · 回合战斗':s.sceneId==='inn'?'雾灯驿站':'雾林小道';
  const done=[f.quest_started,s.sceneId==='forest'||f.core_taken||f.wolf_defeated,f.core_taken,f.wolf_defeated,f.ending_seen];document.querySelectorAll('#quests li').forEach((li,i)=>li.classList.toggle('done',!!done[i]));
  document.getElementById('health').textContent='体力 '+s.story.party[0].hp+'/'+s.story.party[0].maxHP;
  document.querySelector('h1').innerHTML=f.ending_seen?'灯火<em><br>重明。</em>':'把灯火<br><em>带回家。</em>';
 }catch{showRecovery('暂时无法连接游戏。可重新载入后读取已保存的进度，未保存的操作会丢失。')}
}
setInterval(update,250);update();
