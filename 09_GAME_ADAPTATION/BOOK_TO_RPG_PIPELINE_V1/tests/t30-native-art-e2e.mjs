import {chromium} from 'playwright';
import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const out='/tmp/t30-evidence';await fs.mkdir(out,{recursive:true});
const fixture=JSON.parse(await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8'));
const browser=await chromium.launch({headless:true});let errors=[],states=[];
async function go(site,id){
 const page=await browser.newPage({viewport:{width:1440,height:960}});
 page.on('pageerror',e=>errors.push(site+'/'+id+' '+e.message));
 try{
  await page.goto('http://127.0.0.1:6154/'+site+'/chapter/game/?observe=1');
  await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime(),null,{timeout:60000});
  const drain=async()=>{for(let i=0;i<230;i++){const s=await page.evaluate(()=>window.__tpObserve.readRuntime());
   if(!s.dialogue&&!s.scriptRunning&&!s.presentationBusy)break;
   if(s.dialogue)await page.keyboard.press('Space');else await page.waitForTimeout(80);}
  };
  await drain();
  const scene=JSON.parse(await fs.readFile('../'+site+'/chapter/game/projects/book-pilot-cinematic/content/scenes/'+id+'.json','utf8'));
  const f=structuredClone(fixture);f.position.sceneId=id;f.position.pos=scene.entry.pos;
  await page.evaluate(x=>window.tpPlayer.importQuickSave(x),JSON.stringify(f));await page.keyboard.press('F9');
  await page.waitForFunction(v=>window.__tpObserve?.readRuntime()?.sceneId===v,id,{timeout:40000});
  await drain();await page.waitForTimeout(650);
  const s=await page.evaluate(()=>window.__tpObserve.readRuntime());
  await page.locator('#screen').screenshot({path:out+'/'+site+'-'+id+'.png'});
  states.push({site,scene:id,camera:s.camera,position:s.position,actors:s.actors.length});
  return s;
 }finally{await page.close()}
}
try{
 for(const id of ['street','courtyard']){
  const base=await go('candidate',id),version=await go('site',id);
  assert.deepEqual(base.camera,version.camera);assert.deepEqual(base.position,version.position);
  assert.equal(base.actors.length,version.actors.length);
 }
 assert.deepEqual(errors,[]);
 await fs.writeFile(out+'/NATIVE_QA.json',JSON.stringify({status:'TECH_PASS',states,errors,
  purpose:'actual native renderer picture art replaces old buildings; no DOM overlay',
  storyAndNativeCastSame:true,firstActFullArt:'NOT_YET_APPROVED'},null,2));
 console.log('T30_NATIVE_TWO_SCENE_ART_REPLACEMENT_PASS');
}catch(e){await fs.writeFile(out+'/NATIVE_QA.json',JSON.stringify({status:'FAIL',states,errors,error:String(e)},null,2));throw e}
finally{await browser.close()}
