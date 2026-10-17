import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {chromium} from 'playwright';
const base='http://127.0.0.1:6154/t24site/chapter/';
const out='/tmp/t24-evidence';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:960}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base);
 await page.waitForFunction(()=>{
  const f=document.getElementById('game')?.contentWindow;
  return document.getElementById('loading')?.hidden && f?.__tpObserve?.readRuntime()?.health?.draws>0&&f?.__t24ArtProbe?.read()?.frame>8
 },null,{timeout:60000});
 // A modal original opening dialogue intentionally suppresses environmental
 // treatment. Advance native dialogue before checking the visual layer.
 await page.locator('#game').focus();
 for(let i=0;i<180;i++){
  const state=await page.evaluate(()=>document.getElementById('game').contentWindow.__tpObserve.readRuntime());
  if(!state.dialogue&&!state.scriptRunning&&!state.presentationBusy)break;
  if(state.dialogue)await page.keyboard.press('Space');
  else await page.waitForTimeout(110);
 }
 await page.waitForFunction(()=>{
  const f=document.getElementById('game')?.contentWindow;
  return !!f?.__t24ArtProbe?.read()?.paintCount
 },null,{timeout:30000});
 const overlay=page.frameLocator('#game').locator('#t24-atmosphere');
 assert.equal(await overlay.count(),1);
 const state=await page.evaluate(()=>document.getElementById('game').contentWindow.__t24ArtProbe.read());
 assert.equal(state.canvas[0],1280);
 assert.equal(state.canvas[1],800);
 assert.equal(state.errors,0);
 assert.equal(state.scene,'fair');
 assert.equal(state.isPointerTransparent,true);
 const html=page.frameLocator('#game');
 await page.screenshot({path:out+'/T24-FAIR-RENDER-PROBE.png',fullPage:true});
 // Pixel evidence must include original game exactly and be immediately reversible.
 await overlay.evaluate(x=>x.hidden=true);
 await html.locator('#screen').screenshot({path:out+'/T23-ORIGINAL-FAIR.png'});
 await overlay.evaluate(x=>x.hidden=false);
 await page.waitForTimeout(200);
 await html.locator('#screen').screenshot({path:out+'/T24-NATIVE-FAIR-UNCHANGED.png'});
 const original=await fs.readFile('../t23site/chapter/game/projects/book-pilot-cinematic/content/scenes/fair.json');
 const updated=await fs.readFile('../t24site/chapter/game/projects/book-pilot-cinematic/content/scenes/fair.json');
 assert.deepEqual(original,updated);
 assert.deepEqual(errors,[]);
 const result={status:'PASS',scope:'High-DPI layered rendering technical probe, not approved game art',
  scene:'fair',paintCount:state.paintCount,errors,canvas:state.canvas,
  preserved:'T23 original full page and native scene/interaction resources',
  aesthetic:'NOT_APPROVED',firstActFullArt:'NOT_COMPLETE'};
 await fs.writeFile(out+'/RESULT.json',JSON.stringify(result,null,2));
 console.log('T24_ISOLATED_HIGH_DPI_LAYER_TECHNICAL_PASS');
}catch(e){await page.screenshot({path:out+'/FAIL.png'}).catch(()=>{});await fs.writeFile(out+'/RESULT.json',JSON.stringify({status:'FAIL',error:String(e),errors}));throw e}
finally{await browser.close()}
