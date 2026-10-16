/* T1 authored full story -> canonical content22. Execute from pinned upstream editor/scripts. */
import fs from 'node:fs/promises'
import path from 'node:path'
import {createHash} from 'node:crypto'
import {fileURLToPath} from 'node:url'
import {createServer} from 'vite'
const editor=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..')
const vite=await createServer({root:editor,configFile:path.join(editor,'vite.config.ts'),server:{middlewareMode:true},appType:'custom'})
let project:any,art:any
try{const seed=await vite.ssrLoadModule('/src/core/seed.ts');project=await seed.buildBlankProject('book-lantern-inn');art=await (await vite.ssrLoadModule('/scripts/type_pal_t1_art.ts')).buildOriginalArt()}finally{await vite.close()}
const [out]=process.argv.slice(2);if(!out)throw Error('Usage: type_pal_t1_full.mts OUTPUT')
const pos=(col:number,row:number)=>({col,row,height:0})
const flow=(body:any[])=>({kind:'stages',initial:'main',stages:[{id:'main',body}]})
const d=(text:string,actor?:string)=>({kind:'dialog',cue:{identity:actor?{kind:'actor',actor:actor}:{kind:'narration'},rows:[{text}]}})
const flag=(name:string,value=true)=>({kind:'setFlag',flag:name,value})
const cond=(name:string,is=true)=>({kind:'flag',flag:name,is})
const branch=(cond:any,then:any[],otherwise:any[]=[])=>({kind:'branch',cond,then,else:otherwise})
function entity(id:string,col:number,row:number,sprite:string,body:any[],on='interact',range=2){return {id,label:id,pos:pos(col,row),sprite,facing:'down',collide:on==='interact',behaviors:{trigger:{main:{label:'交互',order:0,flow:flow(body)}}},pages:[{id:'default',label:'交互页',trigger:'main',triggerActivation:{on,range}}],initialPage:'default'}}
const addr=(scene:string,entity:string)=>({scene,entity})
const palettePath='assets/generated/colors/project-standard.json'
project[palettePath]=art.palette
const catalog=project['assets/index.json'].assets={}
function bytesOf(v:any){return v instanceof ArrayBuffer?Buffer.from(v):Buffer.from(JSON.stringify(v,null,2)+'\n')}
function addAsset(id:string,kind:string,rel:string,value:any,mediaType='application/vnd.type-pal.rle'){const bytes=bytesOf(value);project[rel]=value;catalog[id]={kind,path:rel,mediaType,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),label:id,origin:{kind:'generated'}}}
addAsset('color.project-standard','color-table',palettePath,art.palette,'application/json')
addAsset('tileset.original','tileset','assets/generated/tilesets/original.rle',art.tiles)
const sprites:any[]=[]
for(const id of ['hero','keeper','wolf','tree','house','lantern','core','sign']){
 addAsset('sprite.'+id,'sprite','assets/generated/sprites/'+id+'.rle',art[id])
 sprites.push({id,asset:'sprite.'+id,label:id,layout:['hero','keeper','wolf'].includes(id)?{kind:'directional',framesPerDir:3}:{kind:'static'}})
}
addAsset('battle.hero','battle-sprite','assets/generated/battle-sprites/hero.rle',art.fighter)
addAsset('battle.wolf','battle-sprite','assets/generated/battle-sprites/wolf.rle',art.enemy)
project['content/sprites.json']=sprites
project['content/tilesets.json']=[{id:'original',name:'雾夜石路与苔地',category:'outdoor',asset:'tileset.original'}]
project['content/battle-sprites.json'][0].asset='battle.hero'
project['content/battle-sprites.json'].push({id:'mist-wolf',label:'雾狼',asset:'battle.wolf',profile:{kind:'enemy',idle:{start:0,count:2},magic:{start:2,count:0},attack:{start:2,count:2},idleTicksPerFrame:5,actTicksPerFrame:3}})
const hero=project['content/actors.json'][0];hero.name='name.hero';hero.battler.baseStats={level:1,hp:120,maxHP:120,mp:12,maxMP:12,attack:60,defense:40,magicAttack:12,speed:15,luck:8}
project['content/actors.json'].push({id:'keeper',name:'name.keeper',spriteId:'keeper'})
project['content/locale.json']={'name.hero':'阿笙','name.keeper':'守灯人','name.wolf':'雾狼'}
project['content/world-variables.json']=Object.fromEntries(['quest_started','core_taken','wolf_defeated','ending_seen'].map(id=>[id,{kind:'flag',name:id,description:'原创驿站任务状态',initial:false}]))
project['content/items.json']=[{id:'lamp-core',name:'灯芯碎晶',desc:['雾林里拾到的微光。','交给守灯人，点亮归途。'],buyPrice:0,sellPrice:0,sellable:false},{id:'herb',name:'回春草',desc:['行囊里的药草。'],buyPrice:10,sellPrice:3,sellable:true,use:{target:'oneAlly',consuming:true,effects:[{kind:'healHp',amount:40}]}}]
const zero={wind:0,thunder:0,water:0,fire:0,earth:0}
project['content/enemies.json']=[{id:'mist-wolf',name:'name.wolf',battleSprite:'mist-wolf',yPosOffset:0,stats:{health:110,level:1,exp:12,cash:10,attackStrength:0,magicStrength:0,defense:0,dexterity:8,fleeRate:0,physicalResistance:1,poisonResistance:0,elemResistance:zero,dualMove:false,collectValue:0},ai:{resistanceToSorcery:0},sounds:{},onDefeated:[flag('wolf_defeated')]}]
project['content/enemy-teams.json']=[{id:'mist-pack',slots:['mist-wolf']}]
project['content/battle-fields.json']=[{id:0,name:'雾林月色',screenWave:0,magicEffect:zero}]
const m=project['manifest.json'];m.name='雾灯驿站 · 灯火重明';m.entryPoints[0].label='从雾夜出发';m.entryPoints[0].scene='inn';m.entryPoints[0].startWorld={party:['hero'],money:0,inventory:[{itemId:'herb',count:3}]}
Object.assign(m.content,{enemies:'content/enemies.json',enemyTeams:'content/enemy-teams.json',battleFields:'content/battle-fields.json'})
const welcome='山道的灯熄了。雾林里还有一枚灯芯，能替我找回来吗？'
const finish=[d('灯芯回来了，雾狼也退了。你听，山道上已经有人在往家走。','keeper'),{kind:'loseItem',itemId:'lamp-core',count:1},flag('ending_seen'),{kind:'giveMoney',delta:20},d('灯火重明'),d('阿笙把灯挂上檐角。雾还没有散，但晚归的人，终于看见了家的方向。'),d('第一章 · 完\n你已完成原创试玩。可继续探索，或按 F5 留下这段归途。')]
const keeperBody=[{kind:'faceEntityToParty',target:addr('inn','keeper')},branch(cond('ending_seen'),[d('灯还亮着。累了就在这里歇一会儿。','keeper'),{kind:'increaseHpMp',delta:999}], [branch({kind:'all',of:[cond('wolf_defeated'),{kind:'hasItem',itemId:'lamp-core',atLeast:1}]},finish,[branch(cond('quest_started'),[d('灯芯在蓝色碎晶旁；别忘了击退守在路口的雾狼。受伤就用回春草。','keeper'),{kind:'increaseHpMp',delta:999}],[d(welcome,'keeper'),d('往右上方的路牌走，按空格进入雾林。先存个档吧，F5 保存，F9 读取。','keeper'),flag('quest_started')])])])]
const keeper=entity('keeper',12,0,'keeper',keeperBody);delete (keeper as any).sprite;Object.assign(keeper,{actor:'keeper'})
const gate=entity('forest-gate',16,-3,'sign',[branch(cond('quest_started'),[{kind:'loadScene',scene:'forest',pos:pos(8,0),facing:'right'}],[d('雾林前路不明。先和檐下的守灯人说几句话。')])])
const inn={id:'inn',mapId:'inn',entry:{pos:pos(10,0),facing:'right'},entities:[keeper,gate,...decor('inn')],hooks:{onEnter:{initial:'main',variants:{main:{label:'初到驿站',order:0,flow:{kind:'stages',initial:'first',stages:[{id:'first',body:[d('雾灯驿站'),d('天黑以后，山路只剩最后一点灯火。\n方向键走动，靠近人物后按空格交谈。')],next:'quiet'},{id:'quiet',body:[]}]}}}}}}
const core=entity('core-shard',11,-2,'core',[branch(cond('core_taken'),[d('碎晶已收进了行囊。')],[d('石缝里透出一点蓝光。获得：灯芯碎晶。'),{kind:'giveItem',itemId:'lamp-core',count:1},flag('core_taken'),{kind:'removeEntity',target:addr('forest','core-shard')}])])
const wolf=entity('wolf',15,0,'wolf',[d('雾狼压低身体，堵住了回程。\n战斗中方向键选择指令，空格确认。'),{kind:'startBattle',enemyTeamId:'mist-pack',fieldId:0,boss:true,music:null,onLose:[d('阿笙跌回路边。守灯人把他扶回檐下。'),{kind:'revivePartyAll',tenths:10},{kind:'loadScene',scene:'inn',pos:pos(10,0)}],onFlee:[]},branch(cond('wolf_defeated'),[{kind:'removeEntity',target:addr('forest','wolf')},d('雾狼退入林中。带上灯芯，回驿站点灯吧。')])],'touch',1)
// Also allow visible monster to be challenged with the normal interaction key at range 1.
const forest={id:'forest',mapId:'forest',battleFieldId:0,entry:{pos:pos(8,0),facing:'right'},entities:[entity('inn-gate',6,0,'sign',[{kind:'loadScene',scene:'inn',pos:pos(15,-3),facing:'left'}]),core,wolf,...decor('forest')]}
function decor(scene:string){const items:any[]=[];let i=0
 const add=(sprite:string,col:number,row:number)=>items.push({id:'decor-'+i++,sprite,pos:pos(col,row),facing:'down',collide:true})
 if(scene==='inn'){add('house',10,-4);add('lantern',13,-3);add('lantern',10,3);add('tree',6,-3);add('tree',7,4);add('tree',18,-1)}
 else{for(const p of [[6,-3],[9,-5],[13,-5],[18,-2],[19,1],[13,4],[8,4],[17,4]])add('tree',p[0],p[1]);add('lantern',7,1)}return items}
project['content/scenes/index.json']={version:1,scenes:[{id:'inn',name:'雾灯驿站',path:'content/scenes/inn.json'},{id:'forest',name:'雾林小道',path:'content/scenes/forest.json'}]}
project['content/maps/index.json']={version:1,maps:[{id:'inn',name:'檐下归途',path:'content/maps/inn.json'},{id:'forest',name:'月色雾林',path:'content/maps/forest.json'}]}
for(const scene of [inn,forest]){
 project['content/scenes/'+scene.id+'.json']=scene
 const tiles=Array.from({length:24},(_,b)=>Array.from({length:12},(_,k)=>{
 const x=k*2+(b%2),col=(b+x)/2,row=(b-x)/2
 if(scene.id==='inn')return Math.abs(row)<3&&col>6&&col<19?3+(b+k)%2:(b*7+k)%3
 return Math.abs(row)<2?3:(b+k)%3
 }))
 project['content/maps/'+scene.id+'.json']={version:4,width:12,height:12,tilesetRefs:['original'],layers:[{id:'floor',name:'苔地与石径',tiles}],collision:Array.from({length:24},()=>Array(12).fill(0))}
}
delete project['content/scenes/start.json'];delete project['content/maps/start.json']
const output=path.resolve(out);await fs.rm(output,{recursive:true,force:true});await fs.mkdir(output,{recursive:true})
for(const [rel,value] of Object.entries(project)){const dest=path.join(output,rel);await fs.mkdir(path.dirname(dest),{recursive:true});await fs.writeFile(dest,bytesOf(value))}
await fs.writeFile(path.resolve(editor,'../reforge/src/engine-chrome/assets/dialog-icons-raw.json'),JSON.stringify(art.cursor,null,2)+'\n')
console.log('T1_FULL_CANONICAL_BUILT '+Object.keys(project).length+' files; two scenes, inventory, quest, battle, ending; UNTESTED')
