import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const base=process.env.T1_URL??'http://127.0.0.1:6154',out=process.env.T1_EVIDENCE??'/tmp/t1-evidence';await fs.mkdir(out,{recursive:true});
const b=await chromium.launch({headless:true,channel:'chromium',args:['--disable-dev-shm-usage']});const c=await b.newContext({viewport:{width:1600,height:1000}});let p=await c.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('crash',()=>console.log('EDITOR_PAGE_CRASH'));p.on('close',()=>console.log('EDITOR_PAGE_CLOSE'));b.on('disconnected',()=>console.log('EDITOR_BROWSER_DISCONNECTED'));
try{
 await p.goto(base+'/editor/');await p.getByText('创建浏览器工程',{exact:true}).click();
 await p.waitForFunction(()=>document.body.innerText.includes('雾灯驿站')&&!document.body.innerText.includes('创建浏览器工程'),null,{timeout:45000});
 await p.screenshot({path:out+'/06-editor-open.png'});console.log('EDITOR_OPEN_BODY='+ (await p.locator('body').innerText()).slice(0,10000).replaceAll('\n',' | '));
 // Locate and modify NPC dialogue through the official script UI. Inspect output guides bounded fixes.
 await fs.writeFile(out+'/editor-dom.txt',await p.locator('body').innerText());
 await fs.writeFile(out+'/editor-inputs.json',JSON.stringify(await p.locator('input,textarea,button,[role=tab]').evaluateAll(es=>es.map(e=>({tag:e.tagName,role:e.getAttribute('role'),text:e.innerText,label:e.getAttribute('aria-label'),title:e.getAttribute('title'),value:e.value}))),null,2));
 console.log('T1_EDITOR_DIRECTORY_CREATE=PASS');
 await fs.writeFile(out+'/editor.json',JSON.stringify({status:'DIRECTORY_CREATED_EDIT_REOPEN_PENDING',errors},null,2));
}catch(e){console.error('EDITOR_ORIGINAL_ERROR '+String(e));await p.screenshot({path:out+'/FAIL-editor.png'}).catch(()=>{});console.error('T1_EDITOR=FAIL '+e+' BODY='+ (await p.locator('body').innerText().catch(()=>'' )).slice(0,5000));await fs.writeFile(out+'/editor.json',JSON.stringify({status:'FAIL',error:String(e),errors},null,2));process.exitCode=1}finally{await c.close();await b.close()}
