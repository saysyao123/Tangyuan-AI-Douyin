// Offline single-file HTML builder, with no npm/CDN dependencies.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
const engine=fs.readFileSync(path.join(dir,'../03_reconstruction/engine.mjs'),'utf8');
const combined=html.replace('<script type="module">','<script>')
 .replace("import {step2048} from '../03_reconstruction/engine.mjs';",engine.replace('export function step2048','function step2048'));
if(combined===html||combined.includes('import {step2048}'))throw new Error('Cannot embed independent engine');
const target=path.join(dir,'offline-2048.html');
fs.writeFileSync(target,combined);
console.log('OFFLINE_HTML_OK bytes='+Buffer.byteLength(combined));
