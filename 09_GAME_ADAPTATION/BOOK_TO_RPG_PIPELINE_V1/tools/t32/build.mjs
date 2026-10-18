import fs from 'node:fs/promises';import path from 'node:path';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),book=path.resolve(here,'../..');
const [root,baseline,out]=process.argv.slice(2).map(x=>path.resolve(x));
function run(cmd,args,cwd=root,env={}){const r=spawnSync(cmd,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('T32 preparation failed '+args[0])}
// Reuse shipped corresponding source, including all proven T18 input/reliability patches.
// Never regenerate map/story content as a side effect of an art build.
run('python3',['-c','from zipfile import ZipFile; import sys; ZipFile(sys.argv[1]).extractall(sys.argv[2])',path.join(baseline,'downloads/corresponding-source.zip'),root]);
run('python3',[path.join(here,'patch-renderer.py'),root]);
await fs.rm(path.join(root,'projects/book-pilot-cinematic'),{recursive:true,force:true});
await fs.cp(path.join(baseline,'chapter/game/projects/book-pilot-cinematic'),path.join(root,'projects/book-pilot-cinematic'),{recursive:true});
run(process.execPath,[path.join(root,'packages/editor/node_modules/vite/bin/vite.js'),'build','--base','./'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-pilot-cinematic'});
await fs.rm(out,{recursive:true,force:true});await fs.cp(baseline,out,{recursive:true,filter:s=>!s.split(path.sep).includes('.git')});
await fs.cp(path.join(root,'packages/reforge/dist'),path.join(out,'chapter/game'),{recursive:true});
await fs.mkdir(path.join(out,'chapter/game/t32-art'),{recursive:true});
for(const f of await fs.readdir(path.join(book,'art/t32')))if(f.endsWith('.webp'))await fs.copyFile(path.join(book,'art/t32',f),path.join(out,'chapter/game/t32-art',f));
for(const f of ['index.html','style.css','shell.js','config.js','journey-guide.js']){
 const a=await fs.readFile(path.join(baseline,'chapter',f)),b=await fs.readFile(path.join(out,'chapter',f));if(!a.equals(b))throw Error('Shell regression '+f);
}
// GPL corresponding source must match this display patch rather than stale T18-only source.
run('python3',[path.join(here,'package-source.py'),root,path.join(out,'downloads/corresponding-source.zip'),book]);
console.log('T32_BUILD_READY_WITH_EXACT_T22_SHELL_AND_T30_GAME_CONTENT');
