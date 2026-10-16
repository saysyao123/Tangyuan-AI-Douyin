/* Fixed small-stage template; text/data supplied separately. Not a general book compiler. */
import fs from 'node:fs/promises'
import path from 'node:path'
import {createHash} from 'node:crypto'
import {createServer} from 'vite'
const [upstream,output,configFile,artFile]=process.argv.slice(2).map(x=>path.resolve(x))
const cfg=JSON.parse(await fs.readFile(configFile,'utf8'))
const editor=path.join(upstream,'packages/editor')
const vite=await createServer({root:editor,configFile:path.join(editor,'vite.config.ts'),server:{middlewareMode:true},appType:'custom'})
let p:any,art:any
try{p=await (await vite.ssrLoadModule('/src/core/seed.ts')).buildBlankProject('book-pilot-opening');art=await (await vite.ssrLoadModule('/scripts/t14-art.ts')).buildPolishedArt(artFile)}finally{await vite.close()}
const pos=(col:number,row:number)=>({col,row,height:0})
const d=(key:string,actor?:string)=>({kind:'dialog',cue:{slot:'bottom',identity:actor?{kind:'actor',actor,portrait:{kind:'default',side:'right'}}:{kind:'narration'},rows:[{text:cfg.text[key]}]}})
const flag=(name:string)=>({kind:'setFlag',flag:name,value:true})
const is=(name:string)=>({kind:'flag',flag:name,is:true})
const branch=(name:string,yes:any[],no:any[]=[])=>({kind:'branch',cond:is(name),then:yes,else:no})
const flow=(body:any[])=>({kind:'stages',initial:'main',stages:[{id:'main',body}]})
const entity=(id:string,col:number,row:number,sprite:string,body:any[],actor?:string)=>({id,label:cfg.labels[id]??id,pos:pos(col,row),...(actor?{actor}:{sprite}),facing:['vendor','guard','stranger','neighbor','rumor'].includes(id)?'right':'down',collide:true,behaviors:{trigger:{main:{label:'交互',order:0,flow:flow(body)}}},pages:[{id:'default',label:'交互',trigger:'main',triggerActivation:{on:'interact',range:2}}],initialPage:'default'})
const bytes=(v:any)=>v instanceof ArrayBuffer?Buffer.from(v):ArrayBuffer.isView(v)?Buffer.from(v.buffer,v.byteOffset,v.byteLength):Buffer.from(JSON.stringify(v,null,2)+'\n')
const assets=p['assets/index.json'].assets
function add(id:string,kind:string,rel:string,value:any,mediaType='application/vnd.type-pal.rle'){const data=bytes(value);p[rel]=value;assets[id]={kind,path:rel,mediaType,bytes:data.length,sha256:createHash('sha256').update(data).digest('hex'),origin:{kind:'generated'},label:id}}
add('color.project-standard','color-table','assets/generated/colors/project-standard.json',art.palette,'application/json')
add('tileset.original','tileset','assets/generated/tilesets/original.rle',art.tiles)
p['content/tilesets.json']=[{id:'original',name:cfg.title,category:'outdoor',asset:'tileset.original'}]
p['content/sprites.json']=[]
for(const id of ['hero','keeper','child','guard','merchant','officer','stranger','neighbor','performer','visitor','house','gate','pot','lantern','sign','stall','stage','flame','tree']){add('sprite.'+id,'sprite','assets/generated/sprites/'+id+'.rle',art[id]);p['content/sprites.json'].push({id,label:id,asset:'sprite.'+id,layout:['hero','child','keeper','guard'].includes(id)?{kind:'directional',framesPerDir:3}:{kind:'static'}})}
p['content/sprites.json'].find((s:any)=>s.id==='flame').poses={flicker:{label:'火光',steps:[0,1,2].map(frame=>({frame,durationMs:180})),loopFrom:0}}
for(const [role,data] of Object.entries(art.portraits))add('portrait.'+role,'portrait','assets/generated/portraits/'+role+'.png',data,'image/png')
const hero={...p['content/actors.json'][0],portraits:{default:'portrait.hero'}}
p['content/actors.json']=[hero,{...structuredClone(hero),id:'child',name:'name.child',spriteId:'child',portraits:{default:'portrait.child'}},...Object.entries({vendor:'merchant',guard:'officer',stranger:'stranger',neighbor:'neighbor'}).map(([id,spriteId])=>({id,name:'name.'+id,spriteId,portraits:{default:'portrait.'+spriteId}}))]
p['content/locale.json']=Object.fromEntries(Object.entries(cfg.names).map(([id,name])=>['name.'+id,name]))
p['content/items.json']=[{id:'treat',name:cfg.item,desc:[cfg.itemDescription],buyPrice:5,sellPrice:0,sellable:false}]
const flags=['intro_seen','bought','shared','watched','backstage_seen','rumor_seen','ending_seen','street_seen','stranger_seen','promise_seen','neighbor_seen','chapter_complete']
p['content/world-variables.json']=Object.fromEntries(flags.map(id=>[id,{kind:'flag',name:id,description:'开篇短阶段进度',initial:false}]))
const m=p['manifest.json'];m.name=cfg.title;m.entryPoints[0].label=cfg.entryLabel;m.entryPoints[0].scene='fair';m.entryPoints[0].startWorld={party:['hero','child'],money:10,inventory:[]}
const vendor=entity('vendor',12,0,'merchant',[{kind:'faceEntityToParty',target:{scene:'fair',entity:'vendor'}},branch('bought',[d('vendorAgain','vendor')],[d('vendor','vendor'),{kind:'giveMoney',delta:-5},{kind:'giveItem',itemId:'treat',count:1},flag('bought'),d('bought')])],'vendor')
const performance=[branch('shared',[],[{kind:'loseItem',itemId:'treat',count:1},flag('shared'),d('share','child')]),d('performance'),{kind:'shakeScreen',frames:5,level:1},d('reaction','hero'),flag('watched'),d('afterPerformance','child')]
const stage=entity('stage',15,-3,'sign',[branch('watched',[d('stageAgain')],[branch('bought',performance,[d('needTreat','child')])])])
const gate=entity('backstage-gate',18,0,'sign',[branch('watched',[{kind:'loadScene',scene:'backstage',pos:pos(8,0),facing:'right'}],[d('gateLocked')])])
const exit=entity('exit',6,0,'sign',[branch('backstage_seen',[branch('ending_seen',[],[d('leave','hero'),d('reply','child'),flag('ending_seen')]),{kind:'loadScene',scene:'street',pos:pos(8,0),facing:'right'}],[d('exitLocked','child')])])
const rumor=entity('rumor',10,3,'visitor',[d('rumor'),flag('rumor_seen')])
const guard=entity('guard',12,0,'officer',[{kind:'faceEntityToParty',target:{scene:'backstage',entity:'guard'}},branch('backstage_seen',[d('guardAgain','guard')],[d('discovery'),d('protest','child'),d('guard','guard'),d('doubt','hero'),flag('backstage_seen'),d('goBack')])],'guard')
const deco=(id:string,col:number,row:number,sprite:string)=>({id,pos:pos(col,row),sprite,facing:'down',collide:true,...(sprite==='flame'?{pages:[{id:'default',label:'火光',animation:{sprite:'flame',action:'flicker',loop:true}}],initialPage:'default'}:{})})
const fair={id:'fair',mapId:'fair',entry:{pos:pos(10,0),facing:'right'},entities:[vendor,stage,gate,exit,rumor,deco('theater',18,-5,'stage'),deco('lamp1',8,-3,'lantern'),deco('lamp2',18,-3,'lantern'),deco('stall',12,-6,'stall'),deco('winter-tree',19,-7,'tree'),deco('stage-fire',16,-5,'flame')],hooks:{onEnter:{initial:'main',variants:{main:{label:'开场',order:0,flow:flow([branch('intro_seen',[],[d('intro'),d('wish','child'),flag('intro_seen')])])}}}}}
const backstage={id:'backstage',mapId:'backstage',entry:{pos:pos(8,0),facing:'right'},entities:[entity('return',6,0,'sign',[{kind:'loadScene',scene:'fair',pos:pos(16,0),facing:'left'}]),guard,deco('performer',14,-3,'performer'),deco('guard2',15,-2,'officer'),deco('curtain',16,-7,'gate'),deco('lamp3',7,-3,'lantern')]}
const enter=(body:any[])=>({onEnter:{initial:'main',variants:{main:{label:'抵达',order:0,flow:flow(body)}}}})
const street={id:'street',mapId:'street',entry:{pos:pos(8,0),facing:'right'},entities:[
 entity('fair-return',6,0,'sign',[{kind:'loadScene',scene:'fair',pos:pos(8,0),facing:'right'}]),
 entity('stranger',12,0,'stranger',[branch('stranger_seen',[d('strangerAgain','stranger')],[d('strangerQuestion','stranger'),d('strangerAnswer','hero'),d('strangerReply','stranger'),flag('stranger_seen')])],'stranger'),
 entity('home-road',18,0,'sign',[branch('stranger_seen',[branch('promise_seen',[],[d('promiseChild','child'),d('promiseHero','hero'),flag('promise_seen')]),{kind:'loadScene',scene:'courtyard',pos:pos(8,0),facing:'right'}],[d('streetLocked','child')])]),
 deco('street-house',15,-5,'house'),deco('street-gate',21,-5,'gate'),deco('street-tree',7,-7,'tree'),deco('street-lamp',12,-4,'lantern')],hooks:enter([branch('street_seen',[],[d('streetIntro'),flag('street_seen')])])}
const courtyard={id:'courtyard',mapId:'courtyard',entry:{pos:pos(8,0),facing:'right'},entities:[
 entity('street-return',6,0,'sign',[{kind:'loadScene',scene:'street',pos:pos(16,0),facing:'left'}]),
 entity('neighbor',12,0,'neighbor',[branch('neighbor_seen',[d('neighborAgain','neighbor')],[d('neighborIntro','neighbor'),d('medicineChild','child'),d('medicineHero','hero'),d('neighborReply','neighbor'),flag('neighbor_seen')])],'neighbor'),
 entity('medicine',13,-2,'pot',[d('medicineInspect')]),
 entity('home',18,0,'sign',[branch('chapter_complete',[d('homeAgain','child')],[branch('neighbor_seen',[d('homeChild','child'),d('homeHero','hero'),flag('chapter_complete'),d('chapterEnding')],[d('homeLocked','hero')])])]),
 deco('home-house',18,-5,'house'),deco('courtyard-tree',8,-7,'tree'),deco('courtyard-gate',21,4,'gate'),deco('home-lamp',17,-4,'lantern')],hooks:enter([d('courtyardIntro')])}
const scenes=[fair,backstage,street,courtyard]
p['content/scenes/index.json']={version:1,scenes:scenes.map(s=>({id:s.id,name:cfg.scenes[s.id],path:'content/scenes/'+s.id+'.json'}))}
p['content/maps/index.json']={version:1,maps:scenes.map(s=>({id:s.id,name:cfg.scenes[s.id],path:'content/maps/'+s.id+'.json'}))}
for(const scene of scenes){p['content/scenes/'+scene.id+'.json']=scene;p['content/maps/'+scene.id+'.json']={version:4,width:12,height:12,tilesetRefs:['original'],layers:[{id:'floor',name:cfg.scenes[scene.id],tiles:Array.from({length:24},(_,b)=>Array.from({length:12},(_,k)=>{const x=k*2+b%2,row=(b-x)/2;return Math.abs(row)<3?(scene.id==='courtyard'?12:0)+(b*3+k)%10:22+(b+k)%10}))}],collision:Array.from({length:24},()=>Array(12).fill(0))}}
delete p['content/maps/start.json'];delete p['content/scenes/start.json']
await fs.rm(output,{recursive:true,force:true});await fs.mkdir(output,{recursive:true})
for(const [rel,value] of Object.entries(p)){const file=path.join(output,rel);await fs.mkdir(path.dirname(file),{recursive:true});await fs.writeFile(file,bytes(value))}
console.log('T14_OPENING_BUILT '+Object.keys(p).length+' files; 4 scenes; shared palette; portraits; native party')
