import fs from 'node:fs/promises';import path from 'node:path';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const tools=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]);
function run(args,cwd=root,env={}){const r=spawnSync(process.execPath,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('Failed: '+args.join(' '))}
await fs.copyFile(path.join(tools,'type_pal_t1_full.mts'),path.join(root,'packages/editor/scripts/type_pal_t1_full.mts'));
await fs.copyFile(path.join(tools,'type_pal_t1_art.ts'),path.join(root,'packages/editor/scripts/type_pal_t1_art.ts'));
run(['--import','tsx','packages/editor/scripts/type_pal_t1_full.mts','projects/book-lantern-inn']);
const py=spawnSync('python3',[path.join(tools,'type_pal_t1_prepare.py'),root],{stdio:'inherit'});if(py.status!==0)throw Error('prepare failed');
run(['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-lantern-inn']);
await fs.rm(output,{recursive:true,force:true});await fs.mkdir(output,{recursive:true});
const vite=path.join(root,'packages/editor/node_modules/vite/bin/vite.js');
run([vite,'build','--base','./'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-lantern-inn'});
// Editor built without default project for native directory workflow. Use ?inspect for read-only HTTP project.
run([vite,'build','--base','./'],path.join(root,'packages/editor'),{VITE_PROJECT_ID:''});
await fs.cp(path.join(root,'packages/reforge/dist'),path.join(output,'game'),{recursive:true});
await fs.cp(path.join(root,'packages/editor/dist'),path.join(output,'editor'),{recursive:true});
for(const base of ['game','editor'])await fs.cp(path.join(root,'projects/book-lantern-inn'),path.join(output,base,'projects/book-lantern-inn'),{recursive:true});
await fs.cp(path.join(tools,'../player'),output,{recursive:true});
await fs.copyFile(path.join(root,'LICENSE'),path.join(output,'LICENSE-TypePAL.txt'));
await fs.cp(path.join(root,'packages/reforge/src/engine-chrome/assets/licenses'),path.join(output,'licenses'),{recursive:true});
await fs.copyFile(path.join(root,'packages/reforge/src/engine-chrome/assets/PROVENANCE.md'),path.join(output,'ART_PROVENANCE.md'));
const packed=spawnSync('python3',[path.join(tools,'type_pal_t1_package.py'),root,output,path.join(tools,'..')],{stdio:'inherit'});if(packed.status!==0)throw Error('packaging failed');
console.log('STATIC_T1_BUILD_READY '+output);
