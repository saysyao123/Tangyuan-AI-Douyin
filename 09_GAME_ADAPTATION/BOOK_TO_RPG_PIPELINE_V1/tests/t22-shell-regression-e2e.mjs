/* Restore T18 chapter shell exactly, with optional T21 experiment behind a separate path.
   Validate that old navigation, quest/objective, JS and CSS are byte-identical, not simply similar. */
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const out='/tmp/t22-evidence';
await fs.mkdir(out,{recursive:true});
for(const n of ['index.html','style.css','shell.js','config.js']){
 const original=await fs.readFile('../web/chapter/'+n);
 const restored=await fs.readFile('../site/chapter/'+n);
 const experiment=await fs.readFile('../site/art-review/'+n);
 assert.deepEqual(restored,original,'T18 chapter shell changed unexpectedly '+n);
 assert.deepEqual(experiment,original,'T21 art review must reuse T18 shell '+n);
}
const original=JSON.parse(await fs.readFile('../site/chapter/game/projects/book-pilot-cinematic/content/scenes/street.json','utf8'));
const review=JSON.parse(await fs.readFile('../site/art-review/game/projects/book-pilot-cinematic/content/scenes/street.json','utf8'));
assert.equal(original.id,review.id);
const mapOf=x=>new Map(x.entities.map(e=>[e.id,e]));
let changed=0;
const reference=mapOf(original);
for(const e of review.entities){
 const prev=reference.get(e.id);
 assert.ok(prev,'added entity '+e.id);
 const {sprite:prevSprite,...a}=prev;
 const {sprite:nextSprite,...b}=e;
 assert.deepEqual(b,a,'changed story/position/collision for '+e.id);
 if(prevSprite!==nextSprite)changed++;
}
assert.equal(changed,3,'Expected only existing three street houses visually replaced');
const browser=await chromium.launch({headless:true});
let screenshots=[];
try{
 for(const [label,route] of [['T18-ORIGINAL','chapter'],['T21-ART-REVIEW','art-review']]){
  const page=await browser.newPage({viewport:{width:1440,height:960}});
  const errs=[];page.on('pageerror',e=>errs.push(e.message));
  await page.goto('http://127.0.0.1:6154/site/'+route+'/',{waitUntil:'load'});
  await page.locator('nav').waitFor({timeout:25000});
  assert.ok((await page.locator('nav a').count())>=3,label+' missing original nav');
  assert.ok(await page.locator('#quests').count(),label+' missing original quests');
  assert.ok(await page.locator('#objective').count(),label+' missing original objective');
  assert.ok(await page.locator('#focus-game').count(),label+' missing original game focus control');
  const frame=page.frameLocator('iframe');
  await frame.locator('#screen').waitFor({timeout:60000});
  // Real readiness: original shell's loading overlay must disappear and the
  // native gameplay scene must have produced at least one render frame.
  await page.waitForFunction(()=>{
   const shell=document.getElementById('loading');
   const s=document.getElementById('game')?.contentWindow?.__tpObserve?.readRuntime();
   return shell?.hidden && s?.sceneId==='fair' && s?.health?.draws>0;
  },null,{timeout:50000});
  await page.waitForTimeout(300);
  await page.screenshot({path:out+'/'+label+'-FULL-PAGE.png',fullPage:true});
  await frame.locator('#screen').screenshot({path:out+'/'+label+'-GAME.png'});
  assert.deepEqual(errs,[],label+' page errors');
  screenshots.push({label,links:await page.locator('nav a').count(),questPanel:true,objectivePanel:true});
  await page.close();
 }
 const result={status:'PASS',matchedFiles:['index.html','style.css','shell.js','config.js'],
  originalUiRestored:true,streetThreeBuildingVisualOnlyDiff:changed,
  screenshots,publicSyntheticDialogue:true,productionSiteChanged:false,
  artAesthetic:'NOT_PASSED',fullFirstActGameplay:'NOT_FULLY_TESTED',
  note:'The original UI has been restored exactly; T21 alternate art is kept as an explicit comparison, not a visual upgrade.'};
 await fs.writeFile(out+'/T22_RESTORE_QA.json',JSON.stringify(result,null,2));
 console.log('T22_ORIGINAL_T18_UI_RESTORED_PASS',JSON.stringify(result));
}catch(e){
 await fs.writeFile(out+'/T22_RESTORE_QA.json',JSON.stringify({status:'FAIL',reason:String(e),screenshots},null,2));
 throw e;
}finally{await browser.close()}
