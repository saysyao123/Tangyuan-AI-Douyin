import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const base=process.env.T1_URL??'http://127.0.0.1:6154',out='/tmp/t13-evidence';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});const ctx=await browser.newContext({viewport:{width:1440,height:960},recordVideo:{dir:out,size:{width:1280,height:800}}});
let page=await ctx.newPage();const errors=[],checks=[],directions=[];const wire=()=>page.on('pageerror',e=>errors.push(e.message));wire();
const state=()=>page.evaluate(()=>window.__tpObserve?.readRuntime());
const press=async k=>{await page.keyboard.press(k);await page.waitForTimeout(160)};
const face=async k=>{await page.keyboard.down(k);await page.waitForTimeout(25);await page.keyboard.up(k)};
const ready=()=>page.waitForFunction(()=>window.__tpObserve?.readRuntime(),null,{timeout:45000});
async function drain(){for(let i=0;i<100;i++){const s=await state();if(!s.scriptRunning&&!s.dialogue&&!s.battleActive){await page.waitForTimeout(140);const n=await state();if(!n.scriptRunning&&!n.dialogue)return}await press('Space')}throw Error('dialogue timeout')}
async function walk(col,row){for(let i=0;i<200;i++){const s=await state();if(s.scriptRunning||s.dialogue)throw Error('Unexpected trigger while walking');const p=s.position;if(Math.abs(p.col-col)<.05&&Math.abs(p.row-row)<.05)return;const k=Math.abs(p.row-row)>.05?(p.row>row?'ArrowUp':'ArrowDown'):(p.col>col?'ArrowLeft':'ArrowRight');await page.keyboard.down(k);await page.waitForTimeout(80);await page.keyboard.up(k);await page.waitForTimeout(40)}throw Error('walk blocked '+JSON.stringify({col,row,state:await state()}))}
async function interact(){await press('Space');await drain()}
async function flag(f){await page.waitForFunction(f=>window.__tpObserve?.readRuntime()?.story.flags[f]===true,f,{timeout:8000})}
try{
 await page.goto(base+'/pilot/game/?observe=1');await ready();await drain();assert.equal((await state()).story.party.length,2);checks.push('NATIVE_TWO_MEMBER_PARTY');
 for(const [key,facing,axis,sign] of [['ArrowUp','up','row',-1],['ArrowLeft','left','col',-1],['ArrowDown','down','row',1],['ArrowRight','right','col',1]]){
  const from=await state();await page.keyboard.down(key);await page.waitForTimeout(160);await page.screenshot({path:out+'/walk-'+facing+'.png'});await page.keyboard.up(key);await page.waitForTimeout(160);const to=await state();assert.equal(to.facing,facing);assert.ok((to.position[axis]-from.position[axis])*sign>0);directions.push({facing,from:from.position,to:to.position});await page.screenshot({path:out+'/idle-'+facing+'.png'});
 }
 checks.push('FOUR_REAL_KEY_DIRECTIONS_AND_IDLE_SCREENSHOTS');
 await walk(8,0);await face('ArrowLeft');await interact();assert.equal((await state()).story.flags.ending_seen,false);checks.push('EXIT_GATED_BEFORE_STORY');
 await walk(9,-1);await walk(14,-1);await walk(14,-3);await face('ArrowRight');await interact();assert.equal((await state()).story.flags.watched,false);checks.push('PERFORMANCE_GATED_BEFORE_PURCHASE');
 await walk(14,-1);await walk(13,-1);await face('ArrowLeft');await interact();await flag('bought');assert.equal((await state()).story.money,5);assert.equal((await state()).story.inventory.find(x=>x.itemId==='treat')?.count,1);await interact();assert.equal((await state()).story.money,5);checks.push('NATIVE_PURCHASE_NO_REPEAT_CHARGE');
 await page.screenshot({path:out+'/01-purchase.png'});
 await walk(14,-1);await walk(14,-3);await face('ArrowRight');await interact();await flag('watched');assert.equal((await state()).story.flags.shared,true);assert.equal((await state()).story.inventory.find(x=>x.itemId==='treat')?.count??0,0);checks.push('SHARE_CONSUMES_ITEM_AND_PERFORMANCE_COMPLETES');await page.screenshot({path:out+'/02-performance.png'});
 await walk(14,-1);await walk(17,-1);await face('ArrowRight');await press('Space');await page.waitForFunction(()=>window.__tpObserve?.readRuntime()?.sceneId==='backstage');await drain();
 await walk(10,0);await face('ArrowRight');await interact();await flag('backstage_seen');checks.push('NATIVE_PORTAL_AND_BACKSTAGE_DISCOVERY');await page.screenshot({path:out+'/03-backstage.png'});
 const saved=await state();await press('F5');await page.waitForTimeout(600);await page.close();page=await ctx.newPage();wire();await page.goto(base+'/pilot/game/?observe=1');await ready();await drain();await press('F9');await flag('backstage_seen');await drain();assert.equal((await state()).sceneId,'backstage');assert.deepEqual((await state()).position,saved.position);assert.equal((await state()).story.money,5);checks.push('PILOT_SAVE_REOPEN_RESTORES_NATIVE_STATE');
 await walk(8,0);await face('ArrowLeft');await press('Space');await page.waitForFunction(()=>window.__tpObserve?.readRuntime()?.sceneId==='fair');await drain();
 await walk(15,-1);await walk(8,-1);await walk(8,0);await face('ArrowLeft');await interact();await flag('ending_seen');await interact();assert.equal((await state()).story.money,5);checks.push('RETURN_EXIT_ENDING_NO_REPEAT_MUTATION');await page.screenshot({path:out+'/04-ending.png'});
 await press('F5');await page.waitForTimeout(600);await page.goto(base+'/game/?observe=1');await ready();await drain();await press('F9');await page.waitForTimeout(300);assert.equal((await state()).projectId,'book-lantern-inn');assert.equal((await state()).sceneId,'inn');assert.equal((await state()).story.flags.ending_seen,false);checks.push('SAVE_SCOPE_ISOLATED_FROM_ORIGINAL_GAME');
 await page.goto(base+'/pilot/');await page.waitForFunction(()=>document.getElementById('loading').hidden,null,{timeout:45000});assert.ok((await page.locator('#quests li').count())===5);await page.screenshot({path:out+'/05-pilot-shell.png'});checks.push('CONFIGURED_PILOT_SHELL_READY');assert.deepEqual(errors,[]);
 await fs.writeFile(out+'/result.json',JSON.stringify({status:'PASS',checks,directions,errors},null,2));console.log('T13_OPENING_E2E=PASS '+JSON.stringify(checks));
}catch(e){await page.screenshot({path:out+'/FAIL.png'});await fs.writeFile(out+'/result.json',JSON.stringify({status:'FAIL',checks,error:String(e),state:await state().catch(()=>null),errors},null,2));console.error(e);process.exitCode=1}finally{await ctx.close();await browser.close()}
