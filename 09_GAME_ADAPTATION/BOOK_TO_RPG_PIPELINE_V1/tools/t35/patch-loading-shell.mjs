// Only the parent loading hint changes. The tested game engine and artwork stay byte-identical.
import fs from 'node:fs/promises';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawnSync} from 'node:child_process';
const root=path.resolve(process.argv[2]),file=path.join(root,'chapter/shell.js');let s=await fs.readFile(file,'utf8');
function patch(a,b){if(s.split(a).length!==2)throw Error('Unexpected shell source: '+a);s=s.replace(a,b)}
patch('function update(){',`function showBootWaiting(){ready=false;loading.hidden=false;const slow=performance.now()-started>15000;hint.textContent=slow?'载入时间较长，可以继续等待或重试。':'正在载入场景与人物素材，请稍候。';retry.hidden=!slow}
function update(){`);
patch('if(doc.dataset.bootError||doc.dataset.runtimeError)', 'if(doc?.dataset.bootError||doc?.dataset.runtimeError)');
patch("const s=win.__tpObserve?.readRuntime();if(!s){if(performance.now()-started>15000){hint.textContent='载入时间较长，可以继续等待或重试。';retry.hidden=false}return}","const s=win.__tpObserve?.readRuntime();if(!s){showBootWaiting();return}");
patch("}catch{showRecovery('暂时无法连接游戏。可重新载入后读取已保存的进度，未保存的操作会丢失。')}","}catch{if(!ready&&performance.now()-started<15000)showBootWaiting();else showRecovery('暂时无法连接游戏。可重新载入后读取已保存的进度，未保存的操作会丢失。')}");
await fs.writeFile(file,s);
// Retain complete corresponding engine source; append this exact reproducible parent-shell patch.
const here=path.dirname(fileURLToPath(import.meta.url));const result=spawnSync('python3',['-c',"from zipfile import ZipFile; import sys; z=ZipFile(sys.argv[1],'a'); z.write(sys.argv[2],'t35-tools/patch-loading-shell.mjs'); z.write(sys.argv[3],'t35-shell/chapter-shell.js'); z.close()",path.join(root,'downloads/corresponding-source.zip'),fileURLToPath(import.meta.url),file],{stdio:'inherit'});if(result.status)throw Error('Source package append failed');
console.log('T35_PARENT_LOADING_HINT_PATCHED_ENGINE_UNCHANGED');
