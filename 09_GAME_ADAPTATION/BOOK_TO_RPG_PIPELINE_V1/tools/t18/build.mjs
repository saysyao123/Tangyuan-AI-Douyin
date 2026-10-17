import fs from'node:fs/promises';import path from'node:path';import{spawnSync}from'node:child_process';import{fileURLToPath}from'node:url'
const here=path.dirname(fileURLToPath(import.meta.url)),book=path.resolve(here,'../..'),root=path.resolve(process.argv[2]),out=path.resolve(process.argv[3])
function run(cmd,args,cwd=root,env={}){const r=spawnSync(cmd,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('T18 failed '+args[0])}
// Apply before any runtime bundle is built. Earlier idempotent patches retain this addition.
if(process.env.T18_CONTENT_ONLY==='1'){
 run('python3',[path.join(here,'patch.py'),root])
 for(const n of['art.mts','opening.mts'])await fs.copyFile(path.join(book,'tools/t17',n),path.join(root,'packages/editor/scripts/t17-'+n))
 run(process.execPath,['--import','tsx','packages/editor/scripts/t17-opening.mts',root,path.join(root,'projects/book-pilot-cinematic')])
}
else run(process.execPath,[path.join(book,'tools/t17/build.mjs'),root,out],root,{T1_NAVIGATION:'1'})
run('python3',[path.join(here,'prepare_art.py'),book,path.join(root,'projects/book-pilot-cinematic'),path.join(root,'t18-artpack.json')])
for(const n of['opening.mts','art.mts'])await fs.copyFile(path.join(here,n),path.join(root,'packages/editor/scripts/t18-'+n))
run(process.execPath,['--import','tsx','packages/editor/scripts/t18-opening.mts',root,path.join(root,'projects/book-pilot-cinematic'),path.join(root,'t18-artpack.json')])
run(process.execPath,['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-pilot-cinematic'])
for(const sub of['chapter/game','editor']){const p=path.join(out,sub,'projects/book-pilot-cinematic');await fs.rm(p,{recursive:true,force:true});await fs.cp(path.join(root,'projects/book-pilot-cinematic'),p,{recursive:true})}
for(const sub of['chapter','night']){const p=path.join(out,sub,'index.html');let s=await fs.readFile(p,'utf8');if(!s.includes('点击地面 <b>绕路</b>'))s=s.replace('方向键 <b>走动</b>','点击地面 <b>绕路</b> · 点击物件 <b>交互</b>　方向键 <b>走动</b>');await fs.writeFile(p,s)}
const configs={T13_CONFIG:process.env.T14_CONFIG??path.join(book,'pilot-config.json'),T15_CONFIG:process.env.T15_CONFIG??path.join(book,'cinematic-config.json'),T16_CONFIG:process.env.T16_CONFIG??path.join(book,'night-config.json')}
for(const[k,v]of Object.entries(configs))try{await fs.access(v)}catch{configs[k]=path.join(book,'examples',k==='T13_CONFIG'?'complete-opening':k==='T15_CONFIG'?'cinematic-opening':'night-awakening','config.json')}
run('python3',[path.join(book,'tools/type_pal_t1_package.py'),root,out,book],root,{...configs,T14_BUILD:'1',T17_BUILD:'1',T18_BUILD:'1'})
run('python3',[path.join(book,'tools/release_inventory.py'),'check',out])
console.log('T18_NAVIGATION_ENVIRONMENT_READY')
