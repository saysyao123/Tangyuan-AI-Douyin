import fs from 'node:fs/promises'
import path from 'node:path'
import {spawnSync} from 'node:child_process'
import {fileURLToPath} from 'node:url'
const tools=path.dirname(fileURLToPath(import.meta.url)),book=path.resolve(tools,'../..'),root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3])
let config=process.env.T14_CONFIG
if(!config){try{await fs.access(path.join(book,'pilot-config.json'));config=path.join(book,'pilot-config.json')}catch{config=path.join(book,'examples/complete-opening/config.json')}}
config=path.resolve(config)
function run(args,cwd=root,env={}){const r=spawnSync(process.execPath,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('Command failed: '+args[0])}
run([path.join(book,'tools/type_pal_t1_build.mjs'),root,out],root,{T1_POLISH:'1'})
const prep=spawnSync('python3',[path.join(tools,'prepare_art.py'),path.join(book,'art/t14'),path.join(root,'t14-artpack.json')],{stdio:'inherit'});if(prep.status!==0)throw Error('Art import failed')
await fs.copyFile(path.join(tools,'art.ts'),path.join(root,'packages/editor/scripts/t14-art.ts'))
await fs.copyFile(path.join(tools,'opening.mts'),path.join(root,'packages/editor/scripts/t14-opening.mts'))
run(['--import','tsx','packages/editor/scripts/t14-opening.mts',root,path.join(root,'projects/book-pilot-opening'),config,path.join(root,'t14-artpack.json')])
run(['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-pilot-opening'])
await fs.rm(path.join(root,'packages/reforge/dist'),{recursive:true,force:true})
run([path.join(root,'packages/editor/node_modules/vite/bin/vite.js'),'build','--base','./'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-pilot-opening'})
await fs.cp(path.join(root,'packages/reforge/dist'),path.join(out,'pilot/game'),{recursive:true})
// Opening has no MIDI/soundfont catalog entries; remove the unused public fallback copy.
await fs.rm(path.join(out,'pilot/game/soundfont.sf3'),{force:true})
await fs.cp(path.join(root,'projects/book-pilot-opening'),path.join(out,'pilot/game/projects/book-pilot-opening'),{recursive:true})
await fs.cp(path.join(root,'projects/book-pilot-opening'),path.join(out,'editor/projects/book-pilot-opening'),{recursive:true})
for(const name of ['index.html','style.css','shell.js'])await fs.copyFile(path.join(out,name),path.join(out,'pilot',name))
const cfg=JSON.parse(await fs.readFile(config,'utf8'))
let html=await fs.readFile(path.join(out,'pilot/index.html'),'utf8')
html=html.replace('<script src="shell.js">','<script src="config.js"></script><script src="shell.js">').replace('href="editor/"','href="../editor/?inspect=projects/book-pilot-opening"').replace('href="downloads/lantern-inn-project.zip"','href="../downloads/lantern-inn-project.zip"').replaceAll('href="help.html"','href="../help.html"')
html=html.replace('<title>雾灯驿站 · 原创像素 RPG</title>','<title>'+cfg.title+'</title>').replace('雾灯驿站 <small>第一章 · 灯火重明</small>','开篇试玩 <small>'+cfg.title+'</small>').replace('正在点亮驿站…','正在进入开篇…').replace('原创故事 · TYPE PAL','完整开篇 · TYPE PAL').replace('原创像素画面与界面 · 免费试玩','独立像素素材 · 内部短阶段测试').replace('雾灯驿站 · T1 原创可玩原型','开篇短阶段 · 内部测试').replace('旅人阿笙的第一段归途','庙会、归途与一盏家灯').replace('href="./"','href="../"').replace('title="雾灯驿站可玩游戏"','title="开篇短阶段可玩游戏"')
await fs.writeFile(path.join(out,'pilot/index.html'),html)
await fs.writeFile(path.join(out,'pilot/config.js'),'window.PILOT_CONFIG='+JSON.stringify({title:cfg.title,scenes:cfg.scenes,...cfg.shell})+';\n')
// A visible entry from the established prototype; existing save scope is preserved.
let main=await fs.readFile(path.join(out,'index.html'),'utf8');main=main.replace('<nav>','<nav><a href="pilot/">开篇试玩 ↗</a>');await fs.writeFile(path.join(out,'index.html'),main)
const py=spawnSync('python3',[path.join(book,'tools/type_pal_t1_package.py'),root,out,book],{stdio:'inherit',env:{...process.env,T13_CONFIG:config,T14_BUILD:'1'}});if(py.status!==0)throw Error('Pilot packaging failed')
const check=spawnSync('python3',[path.join(book,'tools/release_inventory.py'),'check',out],{stdio:'inherit'});if(check.status!==0)throw Error('Pilot release check failed')
console.log('T14_PLAYABLE_BUILD_READY '+out)
