/* Native gameplay/multi-scene visual parity on both baseline and new renderer. */
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const evidence='/tmp/t25-evidence';
await fs.mkdir(evidence,{recursive:true});
const fixture=JSON.parse(await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8'));
const sceneIds=['fair','backstage','street','courtyard'];
const browser=await chromium.launch({headless:true});
const errors=[],checks=[];
async function closeOpening(page){
 for(let i=0;i<160;i++){
  const state=await page.evaluate(()=>window.__tpObserve?.readRuntime());
  if(state&&!state.scriptRunning&&!state.dialogue&&!state.presentationBusy)return;
  if(state?.dialogue)await page.keyboard.press('Space');
  else await page.waitForTimeout(120);
 }
 throw Error('opening dialogue did not settle');
}
async function run(which,id){
 const page=await browser.newPage({viewport:{width:1400,height:950}});
 page.on('pageerror',e=>errors.push(which+'/'+id+': '+e.message));
 try{
  await page.goto('http://127.0.0.1:6154/web-'+which+'/chapter/game/?observe=1');
  await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime(),null,{timeout:60000});
  await closeOpening(page);
  const scene=JSON.parse(await fs.readFile('../web-'+which+'/chapter/game/projects/book-pilot-cinematic/content/scenes/'+id+'.json','utf8'));
  const save=structuredClone(fixture);
  save.position.sceneId=id;
  save.position.pos=scene.entry.pos;
  await page.evaluate(text=>window.tpPlayer.importQuickSave(text),JSON.stringify(save));
  await page.keyboard.press('F9');
  await page.waitForFunction(x=>window.__tpObserve?.readRuntime()?.sceneId===x,id,{timeout:40000});
  await closeOpening(page);
  await page.waitForTimeout(500);
  const state=await page.evaluate(()=>window.__tpObserve.readRuntime());
  assert.equal(state.sceneId,id);
  assert.ok(state.actors.length>=4,id+' missing actors');
  const canvas=page.locator('#screen');
  assert.equal(await canvas.count(),1);
  const screenshot=evidence+'/'+which+'-'+id+'.png';
  await canvas.screenshot({path:screenshot});
  checks.push({version:which,scene:id,actors:state.actors.length,position:state.position,camera:state.camera});
  return state;
 }finally{await page.close()}
}
try{
 for(const id of sceneIds){
  const original=await run('t18',id);
  const detailed=await run('t25',id);
  assert.equal(original.sceneId,detailed.sceneId);
  assert.equal(original.actors.length,detailed.actors.length);
  assert.deepEqual(original.position,detailed.position);
 }
 assert.deepEqual(errors,[]);
 await fs.writeFile(evidence+'/GAME_QA.json',JSON.stringify({
  status:'PASS',scope:'Four actually restored Type PAL first-act scenes; unchanged identities, actor count and SAVE12 checkpoint',
  screenshots:checks,errors,artQuality:'REQUIRES_HUMAN_VISUAL_APPROVAL',continuousFirstAct:'NOT_CLAIMED'
 },null,2));
 console.log('T25_FOUR_SCENE_NATIVE_RENDER_PASS',checks.length);
}catch(e){await fs.writeFile(evidence+'/GAME_QA.json',JSON.stringify({status:'FAIL',error:String(e),checks,errors},null,2));throw e}
finally{await browser.close()}
