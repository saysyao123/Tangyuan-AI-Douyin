/* T20 G0 only: recover a real street camera from the existing SAVE12 fixture.
   No art, story, entities or game code changed. */
import {chromium} from 'playwright'
import fs from 'node:fs/promises'
import assert from 'node:assert/strict'
const out='/tmp/t20-act1-street'
await fs.mkdir(out,{recursive:true})
const raw=await fs.readFile('book-rpg-tests/t15-street.native-save.json','utf8')
const fixture=JSON.parse(raw)
assert.equal(fixture.version,12)
assert.equal(fixture.position.sceneId,'street')
const browser=await chromium.launch({headless:true})
const page=await browser.newPage({viewport:{width:1440,height:960}})
const pageErrors=[]
page.on('pageerror',e=>pageErrors.push(e.message))
try{
 await page.goto('http://127.0.0.1:6154/chapter/game/?observe=1')
 await page.waitForFunction(()=>window.tpPlayer&&window.__tpObserve?.readRuntime(),null,{timeout:60000})
 await page.evaluate(text=>window.tpPlayer.importQuickSave(text),raw)
 await page.keyboard.press('F9')
 await page.waitForFunction(()=>window.__tpObserve?.readRuntime()?.sceneId==='street',null,{timeout:50000})
 await page.waitForFunction(()=>{const x=window.__tpObserve?.readRuntime();return x&&!x.scriptRunning&&!x.dialogue&&!x.presentationBusy},null,{timeout:30000})
 await page.waitForTimeout(300)
 const s=await page.evaluate(()=>window.__tpObserve.readRuntime())
 assert.equal(s.sceneId,'street')
 assert.ok(s.actors.some(x=>x.id==='entity:stranger'),'original stranger entity missing')
 assert.ok(s.actors.some(x=>x.id==='party:hero'),'original hero missing')
 const screen=page.locator('#screen')
 await screen.screenshot({path:out+'/01-street-native-screen.png'})
 await page.screenshot({path:out+'/02-street-browser-camera.png'})
 const anchors=s.actors.filter(a=>['entity:fair-return','entity:stranger','entity:home-road','party:hero','party:child'].includes(a.id)).map(a=>{
  const col=a.canonical?.col,row=a.canonical?.row
  return {id:a.id,col,row,screenPixel:Number.isFinite(col)&&Number.isFinite(row)?[16*(col-row)-s.camera.x,8*(col+row)-s.camera.y]:null}
 })
 const report={status:'PASS',task:'T20_FIRST_ACT_STREET_CAMERA_BASELINE',fixture:'t15-street.native-save.json',
  fixturePosition:fixture.position,sceneId:s.sceneId,position:s.position,camera:s.camera,
  storyFlags:s.story?.flags,actors:s.actors.length,anchors,pageErrors,visualQA:'NOT_YET_PERFORMED',nativeArtAssetsChanged:false}
 assert.deepEqual(pageErrors,[])
 await fs.writeFile(out+'/REPORT.json',JSON.stringify(report,null,2))
 console.log('T20_STREET_BASELINE_CAPTURED',JSON.stringify({camera:s.camera,anchors,pageErrors}))
}catch(e){await page.screenshot({path:out+'/FAIL.png'}).catch(()=>{});await fs.writeFile(out+'/FAIL.json',JSON.stringify({error:String(e),pageErrors}));throw e}
finally{await browser.close()}
