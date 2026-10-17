import fs from 'node:fs/promises'
import assert from 'node:assert/strict'
import {chromium} from 'playwright'
const evidence='/tmp/t21-evidence'
await fs.mkdir(evidence,{recursive:true})
const project='projects/book-pilot-cinematic'
const fixture=JSON.parse(await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8'))
const manifest=JSON.parse(await fs.readFile(evidence+'/T21_ART_MANIFEST.json','utf8'))
const sceneIds=['fair','backstage','street','courtyard']
const browser=await chromium.launch({headless:true})
const page=await browser.newPage({viewport:{width:1440,height:960}})
const errors=[],states=[]
page.on('pageerror',e=>errors.push(e.message))
const read=()=>page.evaluate(()=>window.__tpObserve.readRuntime())
const key=async k=>{await page.keyboard.press(k);await page.waitForTimeout(65)}
async function drain(){
 for(let i=0;i<250;i++){
  const s=await read()
  if(!s.scriptRunning&&!s.dialogue&&!s.presentationBusy)return
  if(s.dialogue)await key('Space');else await page.waitForTimeout(80)
 }
 throw Error('T21 opening did not settle')
}
try{
 await page.goto('http://127.0.0.1:6154/game/?observe=1')
 await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime(),null,{timeout:60000})
 await drain()
 for(const id of sceneIds){
  const scene=JSON.parse(await fs.readFile(project+'/content/scenes/'+id+'.json'))
  const patched=structuredClone(fixture)
  patched.position.sceneId=id
  patched.position.pos=scene.entry.pos
  await page.evaluate(text=>window.tpPlayer.importQuickSave(text),JSON.stringify(patched))
  await key('F9')
  await page.waitForFunction(target=>window.__tpObserve.readRuntime()?.sceneId===target,id,{timeout:30000})
  await drain()
  const s=await read()
  assert.equal(s.sceneId,id)
  assert.ok(s.actors.length>=4,'expected native actors in '+id)
  const linked=manifest.entityReplacements.filter(x=>x.scene===id)
  assert.ok(linked.length>0)
  for(const entry of linked){
   assert.ok(scene.entities.some(e=>e.id===entry.entityId&&e.sprite===entry.sprite),
              'native '+id+' references adjusted sprite '+entry.entityId)
  }
  await page.locator('#screen').screenshot({path:evidence+'/ACT1-'+id+'.png'})
  states.push({id,actorCount:s.actors.length,camera:s.camera,position:s.position,
               artReplacements:linked.length,flagsUnchanged:s.story?.flags})
 }
 assert.equal(errors.length,0,'no browser script errors')
 const result={status:'PASS',scope:'Four first-act scene screens with actual new indexed assets and native SAVE12 restores',
  states,errors,artCount:Object.keys(manifest.newSprites).length,
  limitations:['Four direct scene restore screenshots; not proof of full first-act story end-to-end',
               'High reference-level aesthetic parity not assumed by technical test',
               'Public fixture only; no private book dialogues or deployed Site modifications']}
 await fs.writeFile(evidence+'/T21_BROWSER_QA.json',JSON.stringify(result,null,2))
 console.log('T21_FIRST_ACT_NATIVE_ART_SCENES_PASS',JSON.stringify(states.map(x=>({scene:x.id,replacements:x.artReplacements,actors:x.actorCount}))))
}catch(e){const result={status:'FAIL',error:String(e),errors,states,scene:(await read().catch(()=>({sceneId:'unknown'}))).sceneId};
 await fs.writeFile(evidence+'/T21_BROWSER_QA.json',JSON.stringify(result,null,2))
 await page.screenshot({path:evidence+'/FAIL.png'}).catch(()=>{})
 throw e
}finally{await browser.close()}
