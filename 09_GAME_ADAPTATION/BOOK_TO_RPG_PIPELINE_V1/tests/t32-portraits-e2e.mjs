/* New cinematic scope only. Native keys, real Canvas and read-only runtime observations. */
import {chromium,firefox,webkit} from 'playwright';import fs from 'node:fs/promises';import path from 'node:path';import assert from 'node:assert/strict';
const base=process.env.T1_URL??'http://127.0.0.1:6154',out='/tmp/t32-evidence/portraits/'+(process.env.T32_BROWSER??'chromium'),project=path.resolve('projects/book-pilot-cinematic');await fs.mkdir(out,{recursive:true});
const scenes={},maps={};for(const id of ['fair','backstage','street','courtyard']){scenes[id]=JSON.parse(await fs.readFile(path.join(project,'content/scenes/'+id+'.json')));maps[id]=JSON.parse(await fs.readFile(path.join(project,'content/maps/'+id+'.json')))}
const browserType={chromium,firefox,webkit}[process.env.T32_BROWSER??'chromium'];const browser=await browserType.launch({headless:true}),ctx=await browser.newContext({viewport:{width:1440,height:960},recordVideo:{dir:out,size:{width:1280,height:800}}}),page=await ctx.newPage(),errors=[],checks=[],screens=new Set(),coverage=[];let completedTrace=[];page.on('pageerror',e=>errors.push(e.message));
const state=()=>page.evaluate(()=>window.__tpObserve?.readRuntime());const ready=()=>page.waitForFunction(()=>window.__tpObserve?.readRuntime(),null,{timeout:45000});const press=async key=>{await page.keyboard.press(key);await page.waitForTimeout(100)};
async function shot(name){if(screens.has(name))return;screens.add(name);await page.screenshot({path:out+'/'+name+'.png'})}
async function oldSampleShots(s){const has=id=>s.actors.some(a=>a.id==='entity:'+id);if(s.story.flags.fire_ignited&&!s.story.flags.fire_recalled&&has('body-fire'))await shot('fire-ignited');if(s.story.flags.fire_cast&&!s.story.flags.fire_dissolved&&s.actors.some(a=>a.id==='entity:fireball'&&a.canonical.col<39))await shot('fire-in-flight');if(s.story.flags.performer_down&&has('performer'))await shot('backstage-collapse');if(has('carriers'))await shot('backstage-departure');if(s.dialogue?.pageText?.includes('一点点')&&!screens.has('medicine-crouch')){await page.waitForTimeout(300);await shot('medicine-crouch')}}
async function drain(){for(let i=0;i<1200;i++){const s=await state();await sampleShots(s);
 if(!s.scriptRunning&&!s.dialogue&&!s.presentationBusy){await page.waitForTimeout(140);const t=await state();if(!t.scriptRunning&&!t.dialogue&&!t.presentationBusy)return}if(s.dialogue)await press('Space');else await page.waitForTimeout(60)}throw Error('cutscene did not settle')}
async function blackCoverage(label){const value=await page.evaluate(()=>{const c=document.getElementById('screen'),d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let black=0;for(let i=0;i<d.length;i+=4)if(d[i]===0&&d[i+1]===0&&d[i+2]===0)black++;return black/(d.length/4)});coverage.push({label,blackFraction:value});assert.ok(value<.035,label+' exposes map edge/black field '+value)}
function route(s,to){const map=maps[s.sceneId],def=scenes[s.sceneId],visible=new Set(s.actors.map(a=>a.id)),blocked=new Set();for(const e of def.entities)if(e.collide&&visible.has('entity:'+e.id)){const runtime=s.actors.find(a=>a.id==='entity:'+e.id)?.canonical??e.pos;blocked.add(Math.round(runtime.col)+','+Math.round(runtime.row))}
 const free=(c,r)=>{const b=c+r,x=c-r,k=(x-(b&1))/2;return Number.isInteger(k)&&b>=0&&b<map.height*2&&k>=0&&k<map.width&&map.collision[b][k]===0&&!blocked.has(c+','+r)};
 const start=[Math.round(s.position.col),Math.round(s.position.row)],key=p=>p.join(','),queue=[start],prev=new Map([[key(start),null]]),dirs=[[1,0,'ArrowRight'],[-1,0,'ArrowLeft'],[0,1,'ArrowDown'],[0,-1,'ArrowUp']];for(let i=0;i<queue.length;i++){const cur=queue[i];if(cur[0]===to[0]&&cur[1]===to[1]){const result=[];let at=key(cur);while(prev.get(at)){const [from,keyName]=prev.get(at);result.push(keyName);at=from}return result.reverse()}for(const [dc,dr,k]of dirs){const n=[cur[0]+dc,cur[1]+dr],id=key(n);if(!prev.has(id)&&free(...n)){prev.set(id,[key(cur),k]);queue.push(n)}}}return null}
async function walk(c,r){for(let i=0;i<350;i++){const s=await state();assert.ok(!s.scriptRunning&&!s.dialogue,'unexpected script while navigating');if(s.position.col===c&&s.position.row===r){await page.waitForTimeout(150);return}const keys=route(s,[c,r]);if(!keys?.length)throw Error('no legal path '+JSON.stringify({scene:s.sceneId,to:[c,r],from:s.position}));await page.keyboard.down(keys[0]);await page.waitForTimeout(85);await page.keyboard.up(keys[0]);await page.waitForTimeout(55)}throw Error('walk timeout')}
async function approach(id){const s=await state(),e=scenes[s.sceneId].entities.find(e=>e.id===id);assert.ok(e,id);const candidates=[[e.pos.col-1,e.pos.row,'ArrowRight'],[e.pos.col+1,e.pos.row,'ArrowLeft'],[e.pos.col,e.pos.row-1,'ArrowDown'],[e.pos.col,e.pos.row+1,'ArrowUp']].map(p=>({p,route:route(s,p)})).filter(x=>x.route!==null&&scenes[s.sceneId].entities.filter(q=>q.behaviors?.trigger&&!q.hidden).map(q=>({id:q.id,d:Math.max(Math.abs(q.pos.col-x.p[0]),Math.abs(q.pos.row-x.p[1]))})).filter(q=>q.d<=2).sort((a,b)=>a.d-b.d)[0]?.id===id).sort((a,b)=>a.route.length-b.route.length);assert.ok(candidates.length,'unreachable interactive '+id);const [c,r,k]=candidates[0].p;await walk(c,r);await page.keyboard.down(k);await page.waitForTimeout(20);await page.keyboard.up(k);await page.waitForTimeout(120)}
async function checkpoint(name){const raw=await page.evaluate(()=>window.tpPlayer.exportQuickSave());await fs.writeFile(out+'/checkpoint-'+name+'.json',raw);await fs.writeFile(out+'/partial-checks.json',JSON.stringify(checks))}
async function interact(id){await approach(id);await press('Space');await drain()}
const seen=new Set(),dialogues=[];
async function sampleShots(s){
 for(const slot of s.dialogueSlots??[]){
  const asset=slot.portraitAsset;if(!asset||!slot.active||seen.has(asset))continue;
  if(slot.phase==='typing')await page.keyboard.press('Space');
  await page.waitForTimeout(100);
  const draw=await page.evaluate(asset=>window.__t32PortraitDraws?.[asset.replace('portrait.','portrait-')],asset);
  assert.ok(draw,'actual HD canvas draw missing for '+asset);assert.equal(draw.width,64);assert.equal(draw.height,72);assert.equal(draw.sourceWidth,256);assert.equal(draw.sourceHeight,288);
  assert.ok(draw.x>=0&&draw.y>=0&&draw.x+64<=320&&draw.y+72<=200,'portrait outside native screen');
  seen.add(asset);dialogues.push({asset,scene:s.sceneId,slot:slot.slot,draw});await shot(asset.replace('.','-'));
 }
}
async function importScene(id,flags={}){
 const f=JSON.parse(await fs.readFile('../source/09_GAME_ADAPTATION/BOOK_TO_RPG_PIPELINE_V1/tests/fixtures/t15-street.native-save.json','utf8'));f.position.sceneId=id;f.position.pos=scenes[id].entry.pos;Object.assign(f.world.script.flags,flags);
 await page.evaluate(x=>window.tpPlayer.importQuickSave(x),JSON.stringify(f));await press('F9');await drain();await page.waitForFunction(()=>document.documentElement.dataset.t32Art==='ready');
}
try{
 await page.addInitScript(()=>{
  window.__t32PortraitDraws={};const original=CanvasRenderingContext2D.prototype.drawImage;
  CanvasRenderingContext2D.prototype.drawImage=function(source,...args){
   if(source instanceof HTMLImageElement&&source.src.includes('/t32-art/portrait-')){
    const key=source.src.split('/').pop().replace('.webp','');
    window.__t32PortraitDraws[key]={x:args[0],y:args[1],width:args[2],height:args[3],sourceWidth:source.naturalWidth,sourceHeight:source.naturalHeight};
   }
   return original.call(this,source,...args);
  };
 });
 await page.goto(base+'/chapter/game/?observe=1');await ready();await page.waitForFunction(()=>document.documentElement.dataset.t32Art==='ready',null,{timeout:60000});await drain();
 const decoded=await page.evaluate(async()=>Promise.all(['hero','child','merchant','neighbor','stranger','visitor','officer','performer'].map(async role=>{const im=new Image();im.src='./t32-art/portrait-'+role+'.webp';await im.decode();return {role,w:im.naturalWidth,h:im.naturalHeight}})));
 assert.ok(decoded.every(i=>i.w===256&&i.h===288));checks.push('EIGHT_ORIGINAL_PORTRAITS_DECODED');
 await approach('vendor');await press('Space');await drain();assert.ok(seen.has('portrait.hero')&&seen.has('portrait.child')&&seen.has('portrait.merchant'));checks.push('ACTUAL_VENDOR_AND_LEADS_FIXED_FOOTPRINT');
 const stage=await fs.readFile('../validated/t32-evidence/story/checkpoint-stage.json','utf8');await page.evaluate(x=>window.tpPlayer.importQuickSave(x),stage);await press('F9');await drain();await interact('backstage-gate');assert.ok(seen.has('portrait.officer'));await page.locator('#screen').screenshot({path:out+'/backstage-native.png'});checks.push('ACTUAL_GUARD_DIALOGUE_AND_REVISED_INTERIOR');
 await importScene('street',{stranger_seen:false});await interact('stranger');assert.ok(seen.has('portrait.stranger'));checks.push('ACTUAL_STRANGER_DIALOGUE');
 await importScene('courtyard',{neighbor_seen:false});await interact('neighbor');assert.ok(seen.has('portrait.neighbor'));checks.push('ACTUAL_NEIGHBOR_DIALOGUE');
 await importScene('backstage',{backstage_seen:true,officers_departed:true});await page.locator('#screen').screenshot({path:out+'/backstage-entry.png'});
 assert.equal(seen.size,6);assert.deepEqual(errors,[]);
 await fs.writeFile(out+'/result.json',JSON.stringify({status:'PASS',browser:process.env.T32_BROWSER??'chromium',checks,decoded,dialogues,errors,scope:'Only newly changed portraits and backstage dressing. Actual first-act six speaking identities tested via native interactions. Visitor and performer assets decoded, no new dialogue invented. Prior full-story acceptance reused.'},null,2));
}catch(e){await page.screenshot({path:out+'/FAIL.png'});await fs.writeFile(out+'/result.json',JSON.stringify({status:'FAIL',checks,dialogues,error:String(e),state:await state().catch(()=>null),errors},null,2));throw e}finally{await ctx.close();await browser.close()}
