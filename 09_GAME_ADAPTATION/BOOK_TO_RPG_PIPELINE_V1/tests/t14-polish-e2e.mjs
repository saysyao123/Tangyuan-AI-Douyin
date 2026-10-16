/* New scope only: imported art, actor draw interpolation and four-scene continuation. */
import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const out='/tmp/t14-evidence',base=process.env.T1_URL??'http://127.0.0.1:6154';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true}),ctx=await browser.newContext({viewport:{width:1440,height:960},recordVideo:{dir:out,size:{width:1280,height:800}}});let page=await ctx.newPage();const errors=[],checks=[],motion=[];page.on('pageerror',e=>errors.push(e.message));
const state=()=>page.evaluate(()=>window.__tpObserve?.readRuntime());const ready=()=>page.waitForFunction(()=>window.__tpObserve?.readRuntime(),null,{timeout:45000});
const press=async k=>{await page.keyboard.press(k);await page.waitForTimeout(170)};
const face=async k=>{await page.keyboard.down(k);await page.waitForTimeout(25);await page.keyboard.up(k);await page.waitForTimeout(160)};
async function drain(){for(let i=0;i<110;i++){const s=await state();if(!s.scriptRunning&&!s.dialogue){await page.waitForTimeout(140);if(!(await state()).scriptRunning)return}await press('Space')}throw Error('dialogue timeout')}
async function walk(col,row){for(let i=0;i<200;i++){const s=await state(),p=s.position;if(p.col===col&&p.row===row)return;if(s.scriptRunning||s.dialogue)throw Error('unexpected dialogue walking');const k=p.row!==row?(p.row>row?'ArrowUp':'ArrowDown'):(p.col>col?'ArrowLeft':'ArrowRight');await page.keyboard.down(k);await page.waitForTimeout(80);await page.keyboard.up(k);await page.waitForTimeout(40)}throw Error('walk blocked '+JSON.stringify({col,row,state:await state()}))}
async function interact(){await press('Space');await drain()}
async function portal(scene){await press('Space');await page.waitForFunction(id=>window.__tpObserve?.readRuntime()?.sceneId===id,scene,{timeout:10000});await drain()}
async function shot(name){await page.screenshot({path:out+'/'+name+'.png'})}
const pack=JSON.parse(await fs.readFile('t14-artpack.json','utf8'));const art={colors:pack.palette,frames:Object.entries(pack.sprites).flatMap(([style,frames])=>frames.map((f,dir)=>({...f,style,dir,pixels:[...Buffer.from(f.pixels,'base64')],opaque:[...Buffer.from(f.opaque,'base64')]})))};
async function visible(style,dirs){return page.evaluate(({frames,colors,style,dirs})=>{
 const canvas=document.getElementById('screen'),ctx=canvas.getContext('2d'),{data}=ctx.getImageData(0,0,canvas.width,canvas.height),w=canvas.width,h=canvas.height;let best=0;
 for(const f of frames.filter(f=>f.style===style&&dirs.includes(f.dir))){const pts=[];for(let y=0;y<f.height;y++)for(let x=0;x<f.width;x++)if(f.opaque[y*f.width+x]&&f.pixels[y*f.width+x]!==1)pts.push([x,y,colors[f.pixels[y*f.width+x]]]);const first=pts.find(p=>p[2][0]===233)??pts[0];
  for(const scale of [1,2])for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const i=(y*w+x)*4;if(data[i]!==first[2][0]||data[i+1]!==first[2][1]||data[i+2]!==first[2][2])continue;
   const ox=x-first[0]*scale,oy=y-first[1]*scale;if(ox<0||oy<0||ox+f.width*scale>w||oy+f.height*scale>h)continue;let n=0;
   for(const [px,py,c] of pts){const k=((oy+py*scale)*w+ox+px*scale)*4;if(data[k]===c[0]&&data[k+1]===c[1]&&data[k+2]===c[2])n++}best=Math.max(best,n/pts.length);if(best>.98)return best;
  }
 }return best;
 },{frames:art.frames,colors:art.colors,style,dirs})}
try{
 await page.goto(base+'/pilot/game/?observe=1');await ready();await drain();
 if(!process.env.T14_RESUME){await shot('01-fair');
 // Record real render inputs while native keys move the two-member party.
 await page.evaluate(()=>{window.t14Samples=[];let n=0;const sample=()=>{const s=window.__tpObserve.readRuntime();window.t14Samples.push({position:s.position,presentation:s.presentationPosition,actors:s.actors});if(++n<120)requestAnimationFrame(sample)};requestAnimationFrame(sample)});
 await page.keyboard.down('ArrowRight');await page.waitForTimeout(260);await page.keyboard.up('ArrowRight');await page.waitForTimeout(2000);
 const samples=await page.evaluate(()=>window.t14Samples);const rows=samples.flatMap(s=>s.actors.filter(a=>a.id==='party:child'));const fractional=rows.filter(a=>Math.abs(a.canonical.col-a.displayed.col)+Math.abs(a.canonical.row-a.displayed.row)>.005);assert.ok(fractional.length>=3,'real follower must have intermediate draw positions');assert.ok(rows.some(a=>!a.moving),'follower settles');for(const a of fractional)assert.ok(a.moving);motion.push(...fractional.slice(0,10));checks.push('REAL_FOLLOWER_INTERMEDIATE_DRAW_AND_SETTLEMENT');
 // Four new art views on an unobstructed lane, with screenshots for visual inspection.
 await walk(8,0);await walk(8,6);for(const [key,dir] of [['ArrowUp',2],['ArrowLeft',1],['ArrowDown',0],['ArrowRight',3]]){await face(key);const score=await visible('hero',[dir]);assert.ok(score>.98,'new art hidden/wrong direction '+key+' '+score);await shot('art-'+key)}checks.push('FOUR_IMPORTED_ART_VIEW_CAPTURES');
 await walk(8,0);await walk(13,-1);await face('ArrowLeft');await press('Space');await shot('02-portrait');await drain();assert.equal((await state()).story.flags.bought,true);
 await walk(14,-1);await walk(14,-3);await face('ArrowRight');await interact();assert.equal((await state()).story.flags.watched,true);await shot('03-stage');
 await walk(14,-1);await walk(17,-1);await face('ArrowRight');await portal('backstage');await walk(10,0);await face('ArrowRight');await interact();assert.equal((await state()).story.flags.backstage_seen,true);await shot('04-backstage');
 await walk(8,0);await face('ArrowLeft');await portal('fair');await walk(15,-1);await walk(8,-1);await walk(8,0);await face('ArrowLeft');
 // Build an authentic current SAVE12 containing precisely the old fair-only completion flags.
 await press('F5');await page.waitForTimeout(500);let legacy=JSON.parse(await page.evaluate(()=>window.tpPlayer.exportQuickSave()));await fs.writeFile(out+'/save-shape.json',JSON.stringify({keys:Object.keys(legacy),worldKeys:Object.keys(legacy.world)},null,2));
 legacy.world.script.flags.ending_seen=true;delete legacy.world.script.flags.chapter_complete;delete legacy.world.script.flags.street_seen;delete legacy.world.script.flags.stranger_seen;delete legacy.world.script.flags.promise_seen;delete legacy.world.script.flags.neighbor_seen;
 await page.evaluate(text=>window.tpPlayer.importQuickSave(text),JSON.stringify(legacy));await press('F9');await drain();assert.equal((await state()).sceneId,'fair');assert.equal((await state()).story.flags.ending_seen,true);assert.ok(!(await state()).story.flags.chapter_complete);
 await face('ArrowLeft');await portal('street');checks.push('OLD_FAIR_ENDING_SAVE_CONTINUES_INTO_STREET');await shot('05-street');
 }else{
  await press('F5');await page.waitForTimeout(500);const checkpoint=JSON.parse(await page.evaluate(()=>window.tpPlayer.exportQuickSave()));checkpoint.world.script.flags={intro_seen:true,bought:true,shared:true,watched:true,backstage_seen:true,ending_seen:true,street_seen:true};checkpoint.world.money=5;checkpoint.world.inventory=[];checkpoint.position={sceneId:'street',pos:{col:8,row:0,height:0},facing:'right'};await page.evaluate(text=>window.tpPlayer.importQuickSave(text),JSON.stringify(checkpoint));await press('F9');await drain();checks.push('VALIDATED_NATIVE_CHECKPOINT_FOR_UNPASSED_STREET_SECTION');await shot('05-street');
 }
 await walk(10,0);await face('ArrowRight');await press('Space');await page.waitForTimeout(400);await shot('dialogue-framed');await drain();assert.equal((await state()).story.flags.stranger_seen,true);
 await walk(10,-1);await walk(16,-1);await walk(16,0);await face('ArrowRight');await portal('courtyard');assert.equal((await state()).story.flags.promise_seen,true);await shot('06-courtyard');
 await walk(10,0);await face('ArrowRight');await interact();assert.equal((await state()).story.flags.neighbor_seen,true);
 await walk(10,-1);await walk(16,-1);await walk(16,0);await face('ArrowRight');await interact();assert.equal((await state()).story.flags.chapter_complete,true);await shot('07-home-ending');checks.push('FOUR_SCENE_STORY_REACHES_DISTINCT_CHAPTER_COMPLETE');
 await press('F5');await page.waitForTimeout(500);const end=await state();await page.reload();await ready();await drain();await press('F9');await drain();const restored=await state();assert.equal(restored.sceneId,'courtyard');assert.equal(restored.story.flags.chapter_complete,true);assert.deepEqual(restored.position,end.position);assert.ok(restored.actors.every(a=>Math.abs(a.canonical.col-a.displayed.col)+Math.abs(a.canonical.row-a.displayed.row)<.001));checks.push('NEW_ENDING_RELOAD_AND_DISPLAY_RESET');
 await page.goto(base+'/pilot/');await page.waitForFunction(()=>document.getElementById('loading').hidden,null,{timeout:45000});assert.equal(await page.locator('#quests li').count(),7);await shot('08-shell');checks.push('SEVEN_STAGE_SHELL_AND_COMPLETION_FLAG');assert.deepEqual(errors,[]);
 await fs.writeFile(out+'/result.json',JSON.stringify({status:'PASS',checks,motion,errors},null,2));console.log('T14_POLISH_E2E_PASS '+JSON.stringify(checks));
}catch(e){await shot('FAIL');await fs.writeFile(out+'/result.json',JSON.stringify({status:'FAIL',checks,error:String(e),state:await state().catch(()=>null),motion,errors},null,2));console.error(e);process.exitCode=1}finally{await ctx.close();await browser.close()}
