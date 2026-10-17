import fs from 'node:fs/promises'
import path from 'node:path'
import {createHash}from'node:crypto'
import {createServer}from'vite'
const [root,project,pack]=process.argv.slice(2).map(p=>path.resolve(p)),read=async(p:string)=>JSON.parse(await fs.readFile(path.join(project,p),'utf8')),write=async(p:string,v:any)=>fs.writeFile(path.join(project,p),Buffer.isBuffer(v)?v:JSON.stringify(v,null,2)+'\n')
const vite=await createServer({root:path.join(root,'packages/editor'),configFile:path.join(root,'packages/editor/vite.config.ts'),server:{middlewareMode:true},appType:'custom'});let art:any
try{art=await(await vite.ssrLoadModule('/scripts/t18-art.mts')).environmentArt(pack,project)}finally{await vite.close()}
const catalog=await read('assets/index.json'),sprites=await read('content/sprites.json')
for(const[id,bytes]of Object.entries(art)as[string,Buffer][]){const tile=id==='night-tiles',asset=tile?'night.night-tiles':'environment.'+id,rel='assets/generated/'+(tile?'tilesets/':'sprites/')+id+'.rle';await write(rel,bytes);catalog.assets[asset]={kind:tile?'tileset':'sprite',path:rel,mediaType:'application/vnd.type-pal.rle',bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),origin:{kind:'generated'},label:id};if(!tile&&!sprites.some((s:any)=>s.id===id))sprites.push({id,label:id,asset,layout:{kind:'static'}})}
await write('assets/index.json',catalog);await write('content/sprites.json',sprites)
const placements:Record<string,[string,string,number,number,number,number][]>= {
 'home-room':[['kitchen-cupboard','cupboard',240,184,18,8],['moonlit-room-window','moon-window',352,168,0,0],['winter-coat-by-wall','coat-rack',560,168,12,8]],
 'night-road':[['road-west-winter-tree','winter-tree',352,224,12,8],['road-east-winter-tree','winter-tree',976,320,12,8],['store-firewood','snow-wood',912,320,20,8],['home-firewood','snow-wood',384,304,20,8],['road-warm-lantern','stone-lantern',448,320,11,8],['road-store-lantern','stone-lantern',800,320,11,8]],
 'courtyard':[['court-winter-tree','winter-tree',224,176,12,8],['court-firewood','snow-wood',832,256,20,8]],
 'snow-yard':[['yard-west-tree','winter-tree',288,208,12,8],['yard-east-tree','winter-tree',560,232,12,8],['yard-stone-lantern','stone-lantern',320,288,11,8],['yard-woodpile','snow-wood',544,304,20,8]],
 'night-shop-room':[['shop-stock-cupboard','cupboard',240,176,18,8],['shop-moon-window','moon-window',368,168,0,0]],
}
for(const [sceneId,entries]of Object.entries(placements)){
 const scene=await read('content/scenes/'+sceneId+'.json'),map=await read('content/maps/'+sceneId+'.json')
 for(const[id,sprite,x,y]of entries){const pos={col:(x/16+y/8)/2,row:(y/8-x/16)/2,height:0},entity={id,label:id,pos,sprite,facing:'right',collide:false};const at=scene.entities.findIndex((e:any)=>e.id===id);if(at<0)scene.entities.push(entity);else scene.entities[at]=entity}
 for(let b=0;b<map.height*2;b++)for(let k=0;k<map.width;k++){const x=(2*k+b%2)*16,y=b*8
  for(const[,,px,py,w,h]of entries)if(w&&Math.abs(x-px)<w&&y>=py-h&&y<=py)map.collision[b][k]=1
  // Low contrast variation keeps snow broad and readable, with a cleared walking strip.
  if(['night-road','snow-yard'].includes(sceneId)&&map.layers[0].tiles[b][k]===8)map.layers[0].tiles[b][k]=8+(k*7+b*3)%4
 }
 await write('content/scenes/'+sceneId+'.json',scene);await write('content/maps/'+sceneId+'.json',map)
}
console.log('T18_ENVIRONMENT_COMPOSITION_READY')
