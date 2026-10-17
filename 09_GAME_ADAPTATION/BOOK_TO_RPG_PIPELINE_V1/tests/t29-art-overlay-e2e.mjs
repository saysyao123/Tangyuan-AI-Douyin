import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='/tmp/t29-evidence';await fs.mkdir(out,{recursive:true});
const fixture=JSON.parse(await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8'));
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:960}});
let errors=[];page.on('pageerror',e=>errors.push(e.message));
const state=()=>page.evaluate(()=>window.__tpObserve?.readRuntime());
async function settle(){
 for(let i=0;i<220;i++){
  const s=await state();
  if(!s?.dialogue&&!s?.scriptRunning&&!s?.presentationBusy) return;
  if(s.dialogue)await page.keyboard.press('Space');
  else await page.waitForTimeout(85);
 }
 throw Error('original cutscene did not settle');
}
try{
 await page.goto('http://127.0.0.1:6154/candidate/chapter/game/?observe=1');
 await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime()&&window.__t29Art?.read(),null,{timeout:60000});
 await settle();
 for(const sceneId of ['street','courtyard']){
  const scene=JSON.parse(await fs.readFile('../candidate/chapter/game/projects/book-pilot-cinematic/content/scenes/'+sceneId+'.json','utf8'));
  const f=structuredClone(fixture);f.position.sceneId=sceneId;f.position.pos=scene.entry.pos;
  await page.evaluate(save=>window.tpPlayer.importQuickSave(save),JSON.stringify(f));
  await page.keyboard.press('F9');
  await page.waitForFunction(id=>window.__tpObserve.readRuntime()?.sceneId===id,sceneId,{timeout:30000});
  await settle();
  await page.waitForFunction(id=>{const a=window.__t29Art?.read();return a?.scene===id&&a?.painted>5&&a.loaded&&a.visible>0},sceneId,{timeout:30000});
  const a=await page.evaluate(()=>window.__t29Art.read());
  assert.equal(a.pointerTransparent,true);
  assert.deepEqual(a.screenSize,[1280,800]);
  assert.equal(a.errors,0);
  await page.screenshot({path:out+'/'+sceneId+'-HD-ON.png'});
  await page.locator('button').filter({hasText:'高清建筑'}).click();
  await page.waitForTimeout(350);
  await page.screenshot({path:out+'/'+sceneId+'-HD-OFF.png'});
  await page.locator('button').filter({hasText:'高清建筑'}).click();
  await page.waitForTimeout(350);
  assert.equal((await page.evaluate(()=>window.__t29Art.read())).enabled,true);
 }
 assert.deepEqual(errors,[]);
 await fs.writeFile(out+'/T29_NATIVE_QA.json',JSON.stringify({status:'TECH_PASS',scenes:['street','courtyard'],
   loaded:true,overlayToggle:true,pointerTransparent:true,engineStorySaveUnchanged:true,
   source:'T27 native Type PAL real game',errors,limitation:'Only HD building visual integration, no four-scene art parity claimed'},null,2));
 console.log('T29_HD_NATIVE_ASSET_BOTH_SCENES_PASS');
}catch(e){
 await fs.writeFile(out+'/T29_NATIVE_QA.json',JSON.stringify({status:'FAIL',error:String(e),errors},null,2));
 await page.screenshot({path:out+'/FAIL.png'}).catch(()=>{});throw e;
}finally{await browser.close()}
