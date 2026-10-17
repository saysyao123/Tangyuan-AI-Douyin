import fs from 'node:fs/promises';import path from 'node:path';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
const tools=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]);
function run(args,cwd=root,env={}){const r=spawnSync(process.execPath,args,{cwd,stdio:'inherit',env:{...process.env,...env}});if(r.status!==0)throw Error('Failed: '+args.join(' '))}
await fs.copyFile(path.join(tools,'type_pal_t1_full.mts'),path.join(root,'packages/editor/scripts/type_pal_t1_full.mts'));
await fs.copyFile(path.join(tools,'type_pal_t1_art.ts'),path.join(root,'packages/editor/scripts/type_pal_t1_art.ts'));
run(['--import','tsx','packages/editor/scripts/type_pal_t1_full.mts','projects/book-lantern-inn']);
const py=spawnSync('python3',[path.join(tools,'type_pal_t1_prepare.py'),root],{stdio:'inherit'});if(py.status!==0)throw Error('prepare failed');
run(['--import','tsx','packages/editor/scripts/check-project.mts','projects/book-lantern-inn']);
if(process.env.T1_STABILITY!=='0'){const patched=spawnSync('python3',[path.join(tools,'t11/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('stability patch failed')}
if(process.env.T1_STABILITY!=='0'&&process.env.T1_FOUNDATION!=='0'){const patched=spawnSync('python3',[path.join(tools,'t12/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('foundation patch failed')}

if(process.env.T1_POLISH==='1'){const patched=spawnSync('python3',[path.join(tools,'t14/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('polish patch failed')}

if(process.env.T1_CINEMATIC==='1'){const patched=spawnSync('python3',[path.join(tools,'t15/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('cinematic theme patch failed')}

if(process.env.T1_NIGHT==='1'){const patched=spawnSync('python3',[path.join(tools,'t16/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('night observation patch failed')}

if(process.env.T1_NAVIGATION==='1'){const patched=spawnSync('python3',[path.join(tools,'t18/patch.py'),root],{stdio:'inherit'});if(patched.status!==0)throw Error('navigation patch failed')}

await fs.rm(output,{recursive:true,force:true});await fs.mkdir(output,{recursive:true});
const vite=path.join(root,'packages/editor/node_modules/vite/bin/vite.js');
for(const app of ['reforge','editor'])await fs.rm(path.join(root,'packages',app,'dist'),{recursive:true,force:true});
run([vite,'build','--base','./'],path.join(root,'packages/reforge'),{VITE_PROJECT_ID:'book-lantern-inn'});
// Editor built without default project for native directory workflow. Use ?inspect for read-only HTTP project.
run([vite,'build','--base','./'],path.join(root,'packages/editor'),{VITE_PROJECT_ID:''});
await fs.cp(path.join(root,'packages/reforge/dist'),path.join(output,'game'),{recursive:true});
await fs.cp(path.join(root,'packages/editor/dist'),path.join(output,'editor'),{recursive:true});
for(const base of ['game','editor'])await fs.cp(path.join(root,'projects/book-lantern-inn'),path.join(output,base,'projects/book-lantern-inn'),{recursive:true});
await fs.cp(path.join(tools,'../player'),output,{recursive:true});
await fs.copyFile(path.join(root,'LICENSE'),path.join(output,'LICENSE-TypePAL.txt'));
for(const f of ['spessasynth_processor.min.js','favicon.ico'])await fs.copyFile(path.join(root,'packages/reforge/public',f),path.join(output,f));
await fs.cp(path.join(root,'packages/reforge/src/engine-chrome/assets/licenses'),path.join(output,'licenses'),{recursive:true});
await fs.copyFile(path.join(root,'packages/editor/public/type-pal-editor-mark.svg'),path.join(output,'type-pal-editor-mark.svg'));
await fs.copyFile(path.join(root,'packages/reforge/public/soundfont-LICENSE.txt'),path.join(output,'licenses/TimGM6mb.txt'));
await fs.copyFile(path.join(root,'packages/reforge/src/engine-chrome/assets/PROVENANCE.md'),path.join(output,'ART_PROVENANCE.md'));
const packed=spawnSync('python3',[path.join(tools,'type_pal_t1_package.py'),root,output,path.join(tools,'..')],{stdio:'inherit'});if(packed.status!==0)throw Error('packaging failed');
const verified=spawnSync('python3',[path.join(tools,'release_inventory.py'),'check',output],{stdio:'inherit'});if(verified.status!==0)throw Error('release inventory failed');
console.log('STATIC_T1_BUILD_READY '+output);
