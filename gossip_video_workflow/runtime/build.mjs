// Adapted from op7418/guizang-product-video-skill; see ../NOTICE.md.
import {build} from 'esbuild';
import {readFile,writeFile,mkdir,rm,cp} from 'node:fs/promises';
await rm('dist',{recursive:true,force:true}); await mkdir('dist',{recursive:true});
await build({entryPoints:['film.jsx'],bundle:true,platform:'browser',format:'iife',jsx:'automatic',outfile:'dist/client.js',minify:true,legalComments:'eof'});
await writeFile('dist/index.html',`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>中文热议视频</title><style>${await readFile('film.css','utf8')}</style><body><div id="film-root"></div><script src="client.js"></script></body></html>`);
await cp('public','dist',{recursive:true});
console.log('Built Chinese React / GSAP film');
