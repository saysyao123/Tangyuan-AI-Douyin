// CDP capture and GSAP seek adapted from the validated 2026-10-08 film.
import {chromium} from 'playwright';import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';import {spawn} from 'node:child_process';import {existsSync} from 'node:fs';import path from 'node:path';import {serve} from './server.mjs';
const t=JSON.parse(await readFile('timeline.json','utf8'));const out=t.output;const fps=t.fps;
const hash=x=>createHash('sha256').update(x).digest('hex');
const provenance=hash(Buffer.concat([await readFile('timeline.json'),await readFile('dist/client.js'),await readFile('dist/index.html'),await readFile(t.master)]));
const frames=path.join(t.cache,'render-'+provenance);await mkdir(frames,{recursive:true});await mkdir(out,{recursive:true});await mkdir(path.join(out,'keyframes'),{recursive:true});
const {server,url}=await serve();const browser=await chromium.launch({headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
// Auto-height CJK headings use geometric boundaries; font scroll metrics include non-ink ascenders.
const failures=[];const layouts=[];
function ff(args){return new Promise((res,rej)=>{const p=spawn('ffmpeg',['-v','error','-y','-threads','2','-filter_threads','2',...args],{stdio:'inherit'});p.on('error',rej);p.on('close',c=>c===0?res():rej(Error('ffmpeg '+c)));});}
async function openPage(){const p=await browser.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});p.on('pageerror',e=>failures.push(e.message));p.on('requestfailed',r=>failures.push(r.url()));p.on('response',r=>{if(r.status()>=400)failures.push(`${r.status()} ${r.url()}`)});await p.goto(url,{waitUntil:'networkidle'});await p.evaluate(()=>window.__filmReady);return p;}
try{
 const p=await openPage();
 for(const row of t.rows){await p.evaluate(v=>window.seek(v),row.start+(row.end-row.start)/2);await p.screenshot({path:path.join(out,'keyframes',row.id+'.png')});
 layouts.push(await p.evaluate(()=>{const n=[...document.querySelectorAll('.shot')].find(x=>x.style.display==='block');const blocks=['h1','.chapter','.caption','.source','.note','.footer','.tweet-stage'];return {id:n.dataset.shot,bounds:blocks.map(role=>{const e=n.querySelector(role);if(!e)return null;const r=e.getBoundingClientRect();return {role,x:r.x,y:r.y,width:r.width,height:r.height,overflow:e.scrollWidth>e.clientWidth+1||(role!=='h1'&&e.scrollHeight>e.clientHeight+4),outside:r.x<0||r.y<0||r.right>1080||r.bottom>1920,headlineTooTall:role==='h1'&&r.bottom>442,sourceTooTall:role==='.source'&&r.bottom>1490,captionTooTall:role==='.caption'&&r.bottom>1790};}).filter(Boolean)};}));}
 await p.evaluate(()=>window.seek(0));await p.screenshot({path:path.join(out,'cover.png')});
 const captions=await p.evaluate(()=>window.CAPTION_QA);const bad=layouts.flatMap(x=>x.bounds.filter(b=>b.overflow||b.outside||b.headlineTooTall||b.sourceTooTall||b.captionTooTall));
 await writeFile(path.join(out,'layout-qa.json'),JSON.stringify({provenance,layouts,captions,failures},null,2));
 if(bad.length||captions.some(x=>x.overflow||x.lines>3)||failures.length)throw Error('Layout or media QA failed; inspect layout-qa.json');
 const total=Math.ceil(t.duration*fps);let done=0;
 await Promise.all(Array.from({length:Math.min(3,total)},async(_,w)=>{const page=w===0?p:await openPage();const session=await page.context().newCDPSession(page);for(let f=w;f<total;f+=3){const file=path.join(frames,String(f).padStart(6,'0')+'.jpg');if(!existsSync(file)){await page.evaluate(s=>window.seek(s),f/fps);const cap=await session.send('Page.captureScreenshot',{format:'jpeg',quality:90,fromSurface:true,captureBeyondViewport:false});await writeFile(file,Buffer.from(cap.data,'base64'));}done++;if(done%300===0)console.log(`Frames ${done}/${total}`);}if(w)await page.close();}));
 if(failures.length)throw Error(failures.join('\n'));
 const video=path.join(out,'final_1080p.mp4');
 await ff(['-framerate',String(fps),'-i',path.join(frames,'%06d.jpg'),'-i',t.master,'-map','0:v:0','-map','1:a:0','-t',String(t.duration),'-c:v','libx264','-preset','fast','-threads','2','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',video]);
 await ff(['-i',video,'-vf','scale=720:1280','-c:v','libx264','-preset','fast','-threads','2','-crf','24','-c:a','aac','-b:a','128k','-movflags','+faststart',path.join(out,'preview_720p.mp4')]);
 // Covers and shared keyframes are taken from the encoded movie, not just the browser.
 await ff(['-i',video,'-frames:v','1',path.join(out,'cover.png')]);
 for(const row of t.rows)await ff(['-ss',String((row.start+row.end)/2),'-i',video,'-frames:v','1',path.join(out,'keyframes',row.id+'.png')]);
 console.log('Exported Chinese 1080p, 720p, cover and keyframes',provenance);
}finally{await browser.close();await new Promise(r=>server.close(r));}
