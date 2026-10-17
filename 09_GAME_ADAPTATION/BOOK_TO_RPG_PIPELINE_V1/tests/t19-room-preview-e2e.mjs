/* P2 single asset, isolated game render: no unrelated story / combat regression. */
import {chromium} from 'playwright'
import fs from 'node:fs/promises'
import assert from 'node:assert/strict'
const folder='/tmp/t19-p2-evidence';await fs.mkdir(folder,{recursive:true})
const browser=await chromium.launch({headless:true})
const failures=[],screens=[]
try{
 for(const [name,part] of [['T18','chapter/game'],['T19-preview','t19-preview']]){
  const page=await browser.newPage({viewport:{width:1440,height:960}})
  page.on('pageerror',e=>failures.push(name+': '+e.message))
  await page.goto('http://127.0.0.1:6154/'+part+'/?entry=second-night&observe=1')
  await page.waitForFunction(()=>window.__tpObserve?.readRuntime()?.sceneId==='home-room',{timeout:60000})
  await page.waitForFunction(()=>!window.__tpObserve?.readRuntime().scriptRunning,{timeout:45000})
  await page.waitForTimeout(120)
  const state=await page.evaluate(()=>window.__tpObserve.readRuntime())
  assert.equal(state.sceneId,'home-room')
  assert.ok(state.actors.some(a=>a.id==='entity:meal-table'),'canonical story meal-table entity must be present')
  await page.locator('#screen').screenshot({path:folder+'/'+name+'.png'})
  if(name==='T19-preview'){
   const table=state.actors.find(a=>a.id==='entity:meal-table')
   const x=16*(table.canonical.col-table.canonical.row)-state.camera.x
   const y=8*(table.canonical.col+table.canonical.row)-state.camera.y+5
   assert.ok(x>1&&x<319&&y>1&&y<199,'meal table click marker must be in real camera')
   const box=await page.locator('#screen').boundingBox()
   await page.mouse.click(box.x+x*box.width/320,box.y+y*box.height/200)
   await page.waitForFunction(()=>{
    const s=window.__tpObserve.readRuntime()
    return Boolean(s.dialogue||s.scriptRunning)
   },null,{timeout:12000})
   const hit=await page.evaluate(()=>window.__tpObserve.readRuntime())
   assert.equal(hit.sceneId,'home-room','clicking the table must not load a different scene')
   screens.push({name:'T19-table-pointer',clickPixel:[x,y],dialogue:!!hit.dialogue,scriptRunning:!!hit.scriptRunning})
   await page.locator('#screen').screenshot({path:folder+'/T19-table-interaction.png'})
  }
  screens.push({name,sceneId:state.sceneId,actors:state.actors.length,story:state.story})
  await page.close()
 }
 assert.equal(failures.length,0,'no pageerrors')
 const meta=JSON.parse(await fs.readFile('../web/t19-preview/T19_PREVIEW.json','utf8'))
 assert.equal(meta.storyCollisionSaveChanges,false)
 assert.equal(meta.assetId,'night.noodle-table')
 const report={status:'PASS',scope:'T18 base vs isolated T19 replacement single meal-table; PUBLIC fixture only',screens,failures,meta,
  limits:['No private book text, real user save or official Site deployment','No NPC/animation or visual aesthetic approval inferred']}
 await fs.writeFile(folder+'/RESULT.json',JSON.stringify(report,null,2))
 console.log('T19_SINGLE_ASSET_NATIVE_RENDER_PASS')
}catch(err){
 await fs.writeFile(folder+'/FAIL.json',JSON.stringify({status:'FAIL',error:String(err),screens,failures},null,2))
 throw err
}finally{await browser.close()}
