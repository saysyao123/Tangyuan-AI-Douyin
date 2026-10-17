/* Scoped author repair. Preserve real SAVE12 identifiers, never rewrite runtime save data. */
import fs from 'node:fs/promises'
import path from 'node:path'
import {createHash} from 'node:crypto'
import {createServer} from 'vite'
const [root,project]=process.argv.slice(2).map(p=>path.resolve(p)),read=async(p:string)=>JSON.parse(await fs.readFile(path.join(project,p),'utf8')),write=async(p:string,v:any)=>fs.writeFile(path.join(project,p),Buffer.isBuffer(v)?v:JSON.stringify(v,null,2)+'\n')
const vite=await createServer({root:path.join(root,'packages/editor'),configFile:path.join(root,'packages/editor/vite.config.ts'),server:{middlewareMode:true},appType:'custom'});let art:any
try{art=await(await vite.ssrLoadModule('/scripts/t17-art.mts')).buildDisplayArt(project)}finally{await vite.close()}
const catalog=await read('assets/index.json'),sprites=await read('content/sprites.json')
for(const [id,bytes]of Object.entries(art)as[string,Buffer][]){const tile=id==='night-tiles',asset=tile?'night.night-tiles':'display.'+id,rel='assets/generated/'+(tile?'tilesets/':'sprites/')+id+'.rle';await write(rel,bytes);catalog.assets[asset]={kind:tile?'tileset':'sprite',path:rel,mediaType:'application/vnd.type-pal.rle',bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),origin:{kind:'generated'},label:id};if(!tile&&!sprites.some((s:any)=>s.id===id))sprites.push({id,label:id,asset,layout:{kind:'static'}})}
await write('assets/index.json',catalog);await write('content/sprites.json',sprites)
const pos=(col:number,row:number)=>({col,row,height:0}),load={kind:'loadScene',scene:'home-room'}
const scenes=Object.fromEntries(await Promise.all(['courtyard','home-room','night-road','night-shop-room'].map(async id=>[id,await read('content/scenes/'+id+'.json')])))
function replaceDecoration(scene:string,oldId:string,id:string,col:number,row:number,sprite?:string){const s=scenes[scene],old=s.entities.find((e:any)=>e.id===oldId);if(!old)throw Error('Missing old decoration '+oldId);old.hidden=true;old.collide=false;const e={id,label:id,pos:pos(col,row),sprite:sprite??old.sprite,facing:'right',collide:false};const at=s.entities.findIndex((x:any)=>x.id===id);if(at<0)s.entities.push(e);else s.entities[at]=e}
replaceDecoration('night-road','road-house-0','west-street-cottage',30,-2,'street-cottage');replaceDecoration('night-road','road-house-1','east-street-cottage',38,-10,'street-cottage');replaceDecoration('night-road','shop-facade','lit-storefront',46,-12,'street-store')
replaceDecoration('home-room','bed','room-bedside',26,-1);replaceDecoration('home-room','tv','room-television',28,-4)
replaceDecoration('night-shop-room','shelf-1','store-back-shelf',27,-3);replaceDecoration('night-shop-room','shelf-2','store-side-shelf',31,-3)
for(const [i,c,r]of [[0,28,-2],[1,35,-9],[2,43,-13]])replaceDecoration('courtyard','courtyard-rental-'+i,['west-courtyard-house','middle-courtyard-house','home-courtyard-house'][i],c,r,'street-cottage')
// Same native interaction reaches the next scene after all first-act dialogue and camera reset.
const home=scenes.courtyard.entities.find((e:any)=>e.id==='home'),branch=home.behaviors.trigger.main.flow.stages[0].body[0];if(branch.cond?.flag!=='chapter_complete')throw Error('home completion anchor');branch.then=[load];const success=branch.else[0].then;if(!success.some((x:any)=>x.kind==='setFlag'&&x.flag==='chapter_complete'))throw Error('first-act successful completion anchor');if(!success.some((x:any)=>x.kind==='loadScene'&&x.scene==='home-room'))success.push(load)
function softenEnding(v:any){if(Array.isArray(v))v.forEach(softenEnding);else if(v&&typeof v==='object'){for(const [k,x]of Object.entries(v)){if(k==='text'&&typeof x==='string')v[k]=x.replace(/(?:开篇演出版|开篇短阶段|本段|短阶段|第一幕|小阶段)(?:已)?完成[。！]?$/,'推开家门，屋里的灯还亮着。');else softenEnding(x)}}}softenEnding(home)
for(const [id,scene]of Object.entries(scenes))await write('content/scenes/'+id+'.json',scene)
const footprints:Record<string,[number,number,number,number][]>= {
 'home-room':[[432,200,43,16],[512,192,23,10]],
 'night-shop-room':[[480,192,37,9],[544,224,37,9]],
 'night-road':[[512,224,65,16],[768,224,65,16],[928,272,56,10]],
 'courtyard':[[480,208,65,16],[704,208,65,16],[896,240,65,16]],
}
for(const id of ['home-room','night-shop-room','night-road','mind-tree','snow-yard','courtyard']){const m=await read('content/maps/'+id+'.json'),scene=scenes[id];for(let b=0;b<m.height*2;b++)for(let k=0;k<m.width;k++){const x=(2*k+b%2)*16,y=b*8;if(id!=='courtyard'){let tile=id==='mind-tree'?12:id==='home-room'||id==='night-shop-room'?b<16?16:b<=18?28+b-16:4:8;if(id==='night-road'){const i=[29,30,38,39].indexOf(b);tile=i>=0?24+i:b>=31&&b<=37?0:8}m.layers[0].tiles[b][k]=tile}
 let solid=x<192||x>m.width*32-192||y<128||y>m.height*16-112;if(id==='night-road'&&x>=640&&x<=776&&y>=208&&y<=256)solid=true
 for(const [px,py,w,h]of footprints[id]??[])if(Math.abs(x-px)<w&&y>=py-h&&y<=py)solid=true
 if(id==='courtyard')for(const e of scene.entities.filter((e:any)=>!e.hidden&&['wall','crate'].includes(e.sprite))){const px=16*(e.pos.col-e.pos.row),py=8*(e.pos.col+e.pos.row);if(Math.abs(x-px)<(e.sprite==='wall'?44:12)&&y>=py-8&&y<=py)solid=true}
 m.collision[b][k]=solid?1:0}await write('content/maps/'+id+'.json',m)}
console.log('T17_DISPLAY_AND_NATIVE_CONTINUITY_READY; old decoration IDs retained hidden for actual SAVE12 inputs')
