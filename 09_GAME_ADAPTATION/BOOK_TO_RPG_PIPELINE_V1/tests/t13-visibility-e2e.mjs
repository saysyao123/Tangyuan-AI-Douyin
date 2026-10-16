/* New regression: state-facing can pass while the actor is hidden behind a roof. */
import {chromium} from 'playwright';import fs from 'node:fs/promises';import assert from 'node:assert/strict';
const out='/tmp/t13-evidence',art=JSON.parse(await fs.readFile(out+'/art.json','utf8')),browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1440,height:960}});const evidence=[];
const state=()=>page.evaluate(()=>window.__tpObserve?.readRuntime());
async function drain(){for(let i=0;i<100;i++){const s=await state();if(!s.scriptRunning&&!s.dialogue){await page.waitForTimeout(160);if(!(await state()).scriptRunning)return}await page.keyboard.press('Space');await page.waitForTimeout(160)}throw Error('drain')}
async function walk(col,row){for(let i=0;i<160;i++){const p=(await state()).position;if(p.col===col&&p.row===row)return;const k=p.row!==row?(p.row>row?'ArrowUp':'ArrowDown'):(p.col>col?'ArrowLeft':'ArrowRight');await page.keyboard.down(k);await page.waitForTimeout(80);await page.keyboard.up(k);await page.waitForTimeout(40)}throw Error('walk')}
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
 await page.goto('http://127.0.0.1:6154/pilot/game/?observe=1');await page.waitForFunction(()=>window.__tpObserve?.readRuntime(),null,{timeout:45000});await drain();
 for(const [key,dir,facing] of [['ArrowUp',2,'up'],['ArrowLeft',1,'left'],['ArrowDown',0,'down'],['ArrowRight',3,'right']]){
  await walk(8,-1);await page.keyboard.down(key);await page.waitForTimeout(80);await page.keyboard.up(key);await page.waitForTimeout(220);assert.equal((await state()).facing,facing);
  const hero=await visible('hero',[dir]),child=await visible('child',[0,1,2,3]);evidence.push({facing,position:(await state()).position,heroMatch:hero,childMatch:child});await page.screenshot({path:out+'/visible-'+facing+'.png'});assert.ok(hero>.98,'Rendered '+facing+' hero is hidden or wrong frame: '+hero);assert.ok(child>.98,'Rendered companion missing: '+child);
 }
 await walk(13,1);await page.keyboard.down('ArrowRight');await page.waitForTimeout(25);await page.keyboard.up('ArrowRight');await page.waitForTimeout(220);const score=await visible('hero',[3]);assert.ok(score>.98,'Roof occludes right-facing hero: '+score);evidence.push({case:'previous-roof-occlusion',score});await page.screenshot({path:out+'/visible-former-roof.png'});
 // Counterfactual project input: restore the old roof without mutating live engine state.
 await page.route('**/content/scenes/fair.json',async route=>{const response=await route.fetch(),scene=await response.json();scene.entities=scene.entities.map(e=>e.id==='stall2'?{id:'roof',pos:{col:16,row:4,height:0},sprite:'house',facing:'down',collide:true}:e);await route.fulfill({response,json:scene})});
 await page.reload();await page.waitForFunction(()=>window.__tpObserve?.readRuntime(),null,{timeout:45000});await drain();await walk(13,1);await page.keyboard.down('ArrowRight');await page.waitForTimeout(25);await page.keyboard.up('ArrowRight');await page.waitForTimeout(220);const hidden=await visible('hero',[3]);evidence.push({case:'old-roof-counterexample',score:hidden});await page.screenshot({path:out+'/old-roof-counterexample.png'});assert.ok(hidden<.95,'Counterexample must distinguish old roof from fixed scene');
 await fs.writeFile(out+'/visibility.json',JSON.stringify({status:'PASS',evidence},null,2));console.log('T13_NATIVE_VISIBLE_DIRECTION_AND_COMPANION=PASS');
}catch(e){await page.screenshot({path:out+'/FAIL-visibility.png'});await fs.writeFile(out+'/visibility.json',JSON.stringify({status:'FAIL',error:String(e),evidence},null,2));console.error(e);process.exitCode=1}finally{await browser.close()}
