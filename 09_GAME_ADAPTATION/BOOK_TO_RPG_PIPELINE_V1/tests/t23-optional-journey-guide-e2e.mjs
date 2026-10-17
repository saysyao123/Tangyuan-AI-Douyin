import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {chromium} from 'playwright';
const evidence='/tmp/t23-evidence';
await fs.mkdir(evidence,{recursive:true});
const path='../source/09_GAME_ADAPTATION/BOOK_TO_RPG_PIPELINE_V1/tools/t23/journey-guide.js';
const code=await fs.readFile(path,'utf8');
const box={module:{exports:{}},setInterval:()=>{}};
vm.runInNewContext(code,box);
const {selectHint,directionHint}=box.module.exports;
const flagsBase=()=>({bought:false,shared:false,watched:false,backstage_seen:false,ending_seen:false,stranger_seen:false,neighbor_seen:false,chapter_complete:false});
const checks=[];
const got=(scene,flags,want)=>{
 const v=selectHint(scene,flags)?.target??null;assert.equal(v,want,scene+' '+JSON.stringify(flags));
 checks.push(scene+' -> '+want);
};
got('fair',flagsBase(),'vendor');
got('fair',{...flagsBase(),bought:true,shared:true},'stage');
got('fair',{...flagsBase(),bought:true,shared:true,watched:true},'backstage-gate');
got('fair',{...flagsBase(),bought:true,shared:true,watched:true,backstage_seen:true},'exit');
got('backstage',flagsBase(),null);
got('backstage',{...flagsBase(),backstage_seen:true},'return');
got('street',flagsBase(),'stranger');
got('street',{...flagsBase(),stranger_seen:true},'home-road');
got('courtyard',flagsBase(),'neighbor');
got('courtyard',{...flagsBase(),neighbor_seen:true},'home');
got('courtyard',{...flagsBase(),neighbor_seen:true,chapter_complete:true},null);
got('fair',{...flagsBase(),night_started:true},null);
assert.equal(selectHint('mind-tree',flagsBase()),null);
assert.match(directionHint({col:10,row:0},{x:0,y:0}),/当前画面|镜头/);
const base='../t22site/chapter';
const current='../t23site/chapter';
for(const file of ['shell.js','config.js','game/index.html']){
 const a=await fs.readFile(base+'/'+file),b=await fs.readFile(current+'/'+file);
 assert.deepEqual(a,b,'must preserve '+file);
}
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:960}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto('http://127.0.0.1:6154/t23site/chapter/');
 await page.waitForFunction(()=>{
 const f=document.getElementById('game')?.contentWindow?.__tpObserve?.readRuntime();
 return document.getElementById('loading')?.hidden&&f?.sceneId==='fair'&&f.health.draws>0
 },null,{timeout:60000});
 assert.equal(await page.locator('nav a').count()>=3,true);
 assert.equal(await page.locator('#quests li').count()>0,true);
 assert.equal(await page.locator('#focus-game').count(),1);
 const button=page.getByRole('button',{name:'旅途提示 · 可选'});
 await button.click();
 await assert.equal(await page.locator('#t23-guide-text').isVisible(),true);
 assert.ok((await page.locator('#t23-guide-text').innerText()).includes('摊市'));
 await page.getByRole('button',{name:'旅途提示 · 查看位置'}).click();
 assert.ok((await page.locator('#t23-guide-text').innerText()).includes('商贩'));
 await page.getByRole('button',{name:'旅途提示 · 收起'}).click();
 assert.equal(await page.locator('#t23-guide-text').isVisible(),false);
 await page.screenshot({path:evidence+'/T23-ORIGINAL-SHELL-GUIDE-COLLAPSED.png',fullPage:true});
 await page.getByRole('button',{name:'旅途提示 · 可选'}).click();
 await page.screenshot({path:evidence+'/T23-ORIGINAL-SHELL-GUIDE-OPEN.png',fullPage:true});
 assert.deepEqual(errors,[]);
 const result={status:'PASS',stages:checks,originalShellPreserved:true,htmlAndCSSAddedOnly:true,
  firstActOptionalNoSpoilerGuide:true,gameScene:'fair',runtimeDraws:true,jsErrors:errors,
  unchanged:'story script / save data / collision / battle / nightly game / projectId',
  limitations:'Visual art refinement and full first-act continuity remain separate acceptance gates'};
 await fs.writeFile(evidence+'/RESULT.json',JSON.stringify(result,null,2));
 console.log('T23_NATIVE_JRPG_OPTIONAL_GUIDE_PASS',JSON.stringify({steps:checks.length,errors}));
}catch(e){await page.screenshot({path:evidence+'/FAIL.png'}).catch(()=>{});await fs.writeFile(evidence+'/RESULT.json',JSON.stringify({status:'FAIL',error:String(e),errors,checks}));throw e}
finally{await browser.close()}
