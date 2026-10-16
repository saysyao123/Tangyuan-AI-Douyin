import fs from 'node:fs/promises'
import path from 'node:path'
import os from 'node:os'
import {spawnSync} from 'node:child_process'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url)),book=path.resolve(here,'../..'),root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3])
let cfgFile=process.env.T16_CONFIG??path.join(book,'night-config.json');try{await fs.access(cfgFile)}catch{cfgFile=path.join(book,'examples/night-awakening/config.json')}cfgFile=path.resolve(cfgFile)
function run(cmd,args,cwd=root,env={}){const r=spawnSync(cmd,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('T16 command failed '+args[0])}
run(process.execPath,[path.join(book,'tools/t15/build.mjs'),root,out],root,{T1_NIGHT:'1'})
run('python3',[path.join(book,'tools/t14/prepare_art.py'),path.join(book,'art/t16'),path.join(root,'t16-artpack.json')])
for(const n of ['opening.mts','art.mts'])await fs.copyFile(path.join(here,n),path.join(root,'packages/editor/scripts/t16-'+n))
run(process.execPath,['--import','tsx','packages/editor/scripts/t16-opening.mts',root,path.join(root,'projects/book-pilot-cinematic'),cfgFile,path.join(root,'t16-artpack.json')])
run(process.execPath,['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-pilot-cinematic'])
const clean=await fs.mkdtemp(path.join(os.tmpdir(),'t16-runtime-'))
run(process.execPath,[path.join(root,'packages/reforge/node_modules/vite/bin/vite.js'),'build','--base','./','--outDir',clean,'--emptyOutDir'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-pilot-cinematic'})
await fs.rm(path.join(out,'chapter/game'),{recursive:true,force:true});await fs.cp(clean,path.join(out,'chapter/game'),{recursive:true});await fs.rm(clean,{recursive:true,force:true});await fs.rm(path.join(out,'chapter/game/soundfont.sf3'),{force:true})
for(const dir of ['chapter/game','editor']){const dst=path.join(out,dir,'projects/book-pilot-cinematic');await fs.rm(dst,{recursive:true,force:true});await fs.cp(path.join(root,'projects/book-pilot-cinematic'),dst,{recursive:true})}
const cfg=JSON.parse(await fs.readFile(cfgFile,'utf8')),priorJS=await fs.readFile(path.join(out,'chapter/config.js'),'utf8'),prior=JSON.parse(priorJS.slice(priorJS.indexOf('=')+1).trim().replace(/;$/,''))
const firstObjectives=[['shared','先到糖葫芦摊买一串，和同伴分着吃。'],['watched','走到观众区的路牌旁，按空格观看表演。'],['backstage_seen','沿舞台右侧路牌进入后台。'],['stranger_seen','从庙会出口走上旧街，和路边青年交谈。'],['neighbor_seen','进入小院，和药锅旁的邻居说话。'],['chapter_complete','到家门路牌前，完成归家。'],['night_started','第一幕完成。再次在家门按空格，继续第二幕。']].map(([until,text])=>({until,text}))
const nightObjectives=[['errand_started','向右下走，和屋里的同伴商量晚饭。'],['collision_seen','从左下方门牌出门，沿雪路往右边的便利店走。'],['noodles_bought','到亮灯便利店的柜台前，花五元买两包面。'],['returned_home','带着面沿雪路原路返回家里。'],['tree_seen','到房间右侧水盆边洗净血污，看看手心。'],['income_seen','意识空间左上是“收入记录”，先查看来源。'],['shop_seen','右上光标是商店，查看唯一亮起的果实。'],['fruit_won','右下转盘每次扣100；按方向键选“是”确认。共七次剧情抽取。'],['fruit_used','按 Esc → 物品 → 使用，选择洗髓果实并确认。'],['noodles_eaten','离开意识空间，走到桌边和她一起吃面。'],['night_complete','从屋内右侧门牌进小院，在两个雪堆旁分别按空格。']].map(([until,text])=>({until,text}))
const config={...prior,scenes:{...prior.scenes,...cfg.scenes},night:{...cfg.shell,scenes:{...prior.scenes,...cfg.scenes}},firstObjectives,nightObjectives}
await fs.writeFile(path.join(out,'chapter/config.js'),'window.PILOT_CONFIG='+JSON.stringify(config)+';\n');await fs.copyFile(path.join(here,'shell.js'),path.join(out,'chapter/shell.js'))
let html=await fs.readFile(path.join(out,'chapter/index.html'),'utf8');html=html.replace('<nav>','<nav><a href="../night/">第二幕 · 新开局</a>').replace('<ol id="quests">','<section class="next-step"><strong>当前目标</strong><p id="objective" aria-live="polite">正在核对剧情进度…</p><button id="focus-game">回到游戏</button></section><ol id="quests">');await fs.writeFile(path.join(out,'chapter/index.html'),html)
const extra='\n.next-step{margin:20px 0;padding:14px;border:1px solid #665d48;background:#15232b}.next-step strong{color:#d9c28e}.next-step p{font-size:14px;line-height:1.7;color:#d5dddf}.next-step button{border:1px solid #69756d;background:transparent;color:#d5dddf;padding:7px 12px;cursor:pointer}\n';await fs.appendFile(path.join(out,'chapter/style.css'),extra)
await fs.mkdir(path.join(out,'night'),{recursive:true});for(const n of ['style.css','shell.js'])await fs.copyFile(path.join(out,'chapter',n),path.join(out,'night',n))
let night=html.replace(/<title>.*?<\/title>/,'<title>'+cfg.title+'</title>').replace('src="game/?observe=1"','src="../chapter/game/?entry=second-night&observe=1"').replace('href="../night/">第二幕 · 新开局','href="../chapter/">第一幕 / 读取原进度').replace('<script src="config.js">','<script>window.NIGHT_ENTRY=true;</script><script src="config.js">');await fs.writeFile(path.join(out,'night/index.html'),night);await fs.writeFile(path.join(out,'night/config.js'),'window.PILOT_CONFIG='+JSON.stringify({...config,...cfg.shell})+';\n')
let landing=await fs.readFile(path.join(out,'index.html'),'utf8');await fs.writeFile(path.join(out,'index.html'),landing.replace('<nav>','<nav><a href="night/">雪夜觉醒 · 第二幕 ↗</a>'))
let oldCfg=process.env.T14_CONFIG??path.join(book,'pilot-config.json');try{await fs.access(oldCfg)}catch{oldCfg=path.join(book,'examples/complete-opening/config.json')}
let firstCfg=process.env.T15_CONFIG??path.join(book,'cinematic-config.json');try{await fs.access(firstCfg)}catch{firstCfg=path.join(book,'examples/cinematic-opening/config.json')}
run('python3',[path.join(book,'tools/type_pal_t1_package.py'),root,out,book],root,{T13_CONFIG:path.resolve(oldCfg),T14_BUILD:'1',T15_CONFIG:path.resolve(firstCfg),T16_CONFIG:cfgFile})
run('python3',[path.join(book,'tools/release_inventory.py'),'check',out])
console.log('T16_NIGHT_ACT_PLAYABLE_READY',out)
