import fs from 'node:fs/promises'
import path from 'node:path'
import {spawnSync} from 'node:child_process'
import {fileURLToPath} from 'node:url'
const tools=path.dirname(fileURLToPath(import.meta.url)),book=path.resolve(tools,'../..'),root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3])
let config=process.env.T15_CONFIG;if(!config){try{await fs.access(path.join(book,'cinematic-config.json'));config=path.join(book,'cinematic-config.json')}catch{config=path.join(book,'examples/cinematic-opening/config.json')}}config=path.resolve(config)
function run(args,cwd=root,env={}){const r=spawnSync(process.execPath,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('Command failed: '+args[0])}
run([path.join(book,'tools/t14/build.mjs'),root,out],root,{T1_CINEMATIC:'1'})
const prep=spawnSync('python3',[path.join(book,'tools/t14/prepare_art.py'),path.join(book,'art/t15'),path.join(root,'t15-artpack.json')],{stdio:'inherit'});if(prep.status!==0)throw Error('Cinematic art import failed')
for(const [src,dst]of[['art.ts','t15-art.ts'],['opening.mts','t15-opening.mts']])await fs.copyFile(path.join(tools,src),path.join(root,'packages/editor/scripts',dst))
run(['--import','tsx','packages/editor/scripts/t15-opening.mts',root,path.join(root,'projects/book-pilot-cinematic'),config,path.join(root,'t14-artpack.json'),path.join(root,'t15-artpack.json')])
run(['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-pilot-cinematic'])
await fs.rm(path.join(root,'packages/reforge/dist'),{recursive:true,force:true})
run([path.join(root,'packages/reforge/node_modules/vite/bin/vite.js'),'build','--base','./'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-pilot-cinematic'})
await fs.cp(path.join(root,'packages/reforge/dist'),path.join(out,'chapter/game'),{recursive:true});await fs.rm(path.join(out,'chapter/game/soundfont.sf3'),{force:true})
for(const dst of ['chapter/game','editor'])await fs.cp(path.join(root,'projects/book-pilot-cinematic'),path.join(out,dst,'projects/book-pilot-cinematic'),{recursive:true})
for(const name of ['index.html','style.css','shell.js'])await fs.copyFile(path.join(out,'pilot',name),path.join(out,'chapter',name))
const cfg=JSON.parse(await fs.readFile(config,'utf8'));let html=await fs.readFile(path.join(out,'chapter/index.html'),'utf8');html=html.replace(/<title>.*?<\/title>/,'<title>'+cfg.title+'</title>').replace(/<small>.*?<\/small>/,'<small>'+cfg.title+'</small>').replaceAll('projects/book-pilot-opening','projects/book-pilot-cinematic').replace('开篇试玩','剧情演出').replace('<nav>','<nav><a href="../pilot/">上一版对照</a>');await fs.writeFile(path.join(out,'chapter/index.html'),html)
await fs.writeFile(path.join(out,'chapter/config.js'),'window.PILOT_CONFIG='+JSON.stringify({title:cfg.title,scenes:cfg.scenes,...cfg.shell})+';\n')
let main=await fs.readFile(path.join(out,'index.html'),'utf8');main=main.replace('<nav>','<nav><a href="chapter/">剧情演出版 ↗</a>');await fs.writeFile(path.join(out,'index.html'),main)
let previous=await fs.readFile(path.join(out,'pilot/index.html'),'utf8');previous=previous.replace('<nav>','<nav><a href="../chapter/">新版剧情演出 ↗</a>');await fs.writeFile(path.join(out,'pilot/index.html'),previous)
const oldConfig=process.env.T14_CONFIG??path.join(book,'pilot-config.json');let effectiveOld=oldConfig;try{await fs.access(effectiveOld)}catch{effectiveOld=path.join(book,'examples/complete-opening/config.json')}
const env={...process.env,T13_CONFIG:path.resolve(effectiveOld),T14_BUILD:'1',T15_CONFIG:config};const py=spawnSync('python3',[path.join(book,'tools/type_pal_t1_package.py'),root,out,book],{stdio:'inherit',env});if(py.status!==0)throw Error('Cinematic packaging failed')
const check=spawnSync('python3',[path.join(book,'tools/release_inventory.py'),'check',out],{stdio:'inherit'});if(check.status!==0)throw Error('Cinematic release inventory failed')
console.log('T15_PLAYABLE_CINEMATIC_READY '+out)
