import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const out='/tmp/t32-evidence';await fs.mkdir(out,{recursive:true});
const fixture=JSON.parse(await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8'));
const browser=await chromium.launch({headless:true});let errors=[],states=[];
async function sceneShot(site,id){
 const page=await browser.newPage({viewport:{width:1440,height:960}});page.on('pageerror',e=>errors.push(site+'/'+id+': '+e.message));
 await page.goto('http://127.0.0.1:6154/'+site+'/chapter/game/?observe=1');await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime(),null,{timeout:60000});
 const state=()=>page.evaluate(()=>window.__tpObserve.readRuntime());
 async function drain(){for(let i=0;i<250;i++){let s=await state();if(!s.dialogue&&!s.scriptRunning&&!s.presentationBusy)return;if(s.dialogue)await page.keyboard.press('Space');else await page.waitForTimeout(80)}throw Error('scene did not settle')}
 await drain();const scene=JSON.parse(await fs.readFile('../'+site+'/chapter/game/projects/book-pilot-cinematic/content/scenes/'+id+'.json','utf8'));
 const f=structuredClone(fixture);f.position.sceneId=id;f.position.pos=scene.entry.pos;
 await page.evaluate(x=>window.tpPlayer.importQuickSave(x),JSON.stringify(f));await page.keyboard.press('F9');await page.waitForFunction(id=>window.__tpObserve.readRuntime().sceneId===id,id,{timeout:30000});await drain();await page.waitForTimeout(1800);
 if(site==='site'){
  await page.waitForFunction(()=>document.documentElement.dataset.t32Art==='ready',null,{timeout:30000});
  const art=await page.evaluate(async()=>{const names=['house','stage','stall','backstage','wall','tree','stove','terrain-snow','terrain-stone','terrain-wood'];return Promise.all(names.map(n=>new Promise(resolve=>{let i=new Image();i.onload=()=>resolve({n,w:i.width,h:i.height});i.onerror=()=>resolve({n,error:true});i.src='./t32-art/'+n+'.webp'})))});
  assert.ok(art.every(a=>!a.error&&a.w>100));
 }
 const s=await state();await page.locator('#screen').screenshot({path:out+'/'+site+'-'+id+'.png'});
 const canvas=await page.locator('#screen').evaluate(c=>({width:c.width,height:c.height}));if(site==='site'){assert.equal(canvas.width,1280);assert.equal(canvas.height,800)}else{assert.ok([640,1280].includes(canvas.width));assert.equal(canvas.width/canvas.height,1.6)}
 if(site==='site'){
  if(id==='fair'){
   const motion=[];await page.keyboard.down('ArrowRight');
   for(let i=0;i<6;i++){await page.waitForTimeout(65);await page.locator('#screen').screenshot({path:out+'/motion-'+i+'.png'});const q=await state();motion.push({position:q.position,actors:q.actors.filter(a=>a.id.startsWith('party:'))})}
   await page.keyboard.up('ArrowRight');await fs.writeFile(out+'/MOTION_ACTUAL.json',JSON.stringify(motion,null,2));
  }
  const box=await page.locator('#screen').boundingBox();let p={...s.position};
  // Real pointer route toward a nearby visible legal cell, then keyboard takeover.
  await page.mouse.click(box.x+box.width*.6,box.y+box.height*.58);await page.waitForTimeout(30);await page.keyboard.press('ArrowDown');await page.waitForTimeout(150);
  assert.equal((await state()).navigation.active,false,'keyboard must cancel pointer navigation');
 }
 states.push({site,scene:id,camera:s.camera,position:s.position,actors:s.actors.length,canvas,p95:s.health.p95FrameMs});await page.close();return s;
}
try{
 // Unchanged T30 control was captured in successful Run39087660114; reuse its frozen values.
 const control={fair:{camera:{x:320,y:128},position:{col:30,row:0,height:0},actors:35},backstage:{camera:{x:256,y:96},position:{col:26,row:0,height:0},actors:7},street:{camera:{x:224,y:112},position:{col:26,row:2,height:0},actors:11},courtyard:{camera:{x:256,y:112},position:{col:27,row:1,height:0},actors:16}};
 for(const id of ['fair','backstage','street','courtyard']){const b=await sceneShot('site',id),a=control[id];assert.deepEqual(a.position,b.position);assert.deepEqual(a.camera,b.camera);assert.equal(a.actors,b.actors.length)}
 const page=await browser.newPage({viewport:{width:1440,height:960}});await page.goto('http://127.0.0.1:6154/site/chapter/');await page.waitForFunction(()=>document.getElementById('loading').hidden,null,{timeout:60000});assert.equal(await page.locator('#quests li').count(),7);await page.screenshot({path:out+'/WEB-full-page.png',fullPage:true});await page.close();
 assert.deepEqual(errors,[]);await fs.writeFile(out+'/ART_ENGINE_QA.json',JSON.stringify({status:'TECH_PASS_REQUIRES_VISUAL_REVIEW',states,errors,artGate:'PENDING_HUMAN_REVIEW'},null,2));
}catch(e){await fs.writeFile(out+'/ART_ENGINE_QA.json',JSON.stringify({status:'FAIL',states,errors,error:String(e)},null,2));throw e}finally{await browser.close()}
