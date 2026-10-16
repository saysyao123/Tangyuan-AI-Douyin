/* Type PAL canonical content22 adapter P0.
   Executes only inside pinned official Type PAL checkout.
   All palette/tileset/sprite bytes are produced by upstream buildBlankProject.
   Scope: first scene, 1 NPC interaction, movement. Other features are NOT claimed.
*/
import fs from 'node:fs/promises'
import path from 'node:path'
import { createServer } from 'vite'
import { fileURLToPath } from 'node:url'

const editorRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..')
const vite=await createServer({root:editorRoot,configFile:path.join(editorRoot,'vite.config.ts'),server:{middlewareMode:true},appType:'custom'})
const { buildBlankProject }=await vite.ssrLoadModule('/src/core/seed.ts')

const [input,output] = process.argv.slice(2)
if (!input || !output) throw new Error('Usage: tsx scripts/book_rpg_original_seed.mts GAME_JSON OUTPUT_DIR')
const story=JSON.parse(await fs.readFile(input,'utf8'))
if (story.format!=='book-rpg-game-v1'||story.rights?.source_kind!=='original') {
  throw new Error('Only fully original content is supported')
}
if (!Array.isArray(story.world?.scenes)||story.world.scenes.length===0||!Array.isArray(story.events)) {
  throw new Error('missing source scenes/events')
}
const pkgId='book-'+story.id
if (!/^[a-z0-9-]+$/.test(pkgId)) throw new Error('invalid id')
const project=await buildBlankProject(pkgId)
await vite.close()
const manifest=project['manifest.json'] as any
manifest.id=pkgId
manifest.name=story.title
const scene=project['content/scenes/start.json'] as any
const index=project['content/scenes/index.json'] as any
const actors=project['content/actors.json'] as any[]
const locale=project['content/locale.json'] as Record<string,string>
const first=story.world.scenes[0]
const npc=story.characters.find((c:any)=>c.id!==story.player.id)
if (!npc)throw new Error('story needs a nonplayer character')
const initial=story.events.find((e:any)=>e.kind==='dialogue')
if (!initial)throw new Error('story needs a dialogue event')
actors[0].name='name.story-hero'
actors[0].battler.baseStats.hp=story.player.maxHp
actors[0].battler.baseStats.maxHP=story.player.maxHp
actors[0].battler.baseStats.mp=story.player.maxMp
actors[0].battler.baseStats.maxMP=story.player.maxMp
actors[0].battler.baseStats.attack=story.player.attack
actors[0].battler.baseStats.defense=story.player.defense
locale['name.story-hero']=story.player.name
locale['name.story-npc']=npc.name
actors.push({id:'story-npc',name:'name.story-npc',spriteId:'hero'})
index.scenes[0].name=first.name
scene.entities.push({
 id:'npc-welcome',pos:{col:14,row:0,height:0},actor:'story-npc',facing:'down',collide:true,
 behaviors:{trigger:{default:{
  label:'与'+npc.name+'交谈',order:0,
  flow:{kind:'stages',initial:'main',
   stages:[{id:'main',body:[{kind:'dialog',
      cue:{identity:{kind:'narration'},rows:[{text:initial.text}]}}]}]}
 }}},
 pages:[{id:'default',label:'默认交互',trigger:'default',triggerActivation:{on:'interact'}}],
 initialPage:'default'
})
const dir=path.resolve(output)
try {await fs.access(dir);throw new Error('Output exists; refusing overwrite '+dir)}
catch(error:any){if(error.code!=='ENOENT')throw error}
await fs.mkdir(dir,{recursive:true})
const report:any={status:'BUILT_UNTESTED',engine:'type-pal/reforge',contentVersion:22,minimumSaveVersion:12,
 projectId:pkgId,origin:'upstream generated original assets',source:story.id,files:[],
 supported:['one scene','map movement','one NPC dialogue','original generated assets'],
 unsupported:['second scene','quest state effects','items','combat encounter','ending','browser directory save/reopen']}
for (const [rel,value] of Object.entries(project)){
 const dest=path.resolve(dir,rel)
 if(!dest.startsWith(dir+path.sep))throw new Error('Unsafe file path '+rel)
 await fs.mkdir(path.dirname(dest),{recursive:true})
 const bytes=value instanceof ArrayBuffer?Buffer.from(value):
   typeof value==='string'?Buffer.from(value,'utf8'):Buffer.from(JSON.stringify(value,null,2)+'\n')
 await fs.writeFile(dest,bytes)
 report.files.push({path:rel,bytes:bytes.length})
}
const reportPath=path.resolve(dir,'../../book-t1-reports/'+pkgId+'.json')
await fs.mkdir(path.dirname(reportPath),{recursive:true})
await fs.writeFile(reportPath,JSON.stringify(report,null,2)+'\n')
console.log(JSON.stringify({PROJECT_GENERATED:true,id:pkgId,files:report.files.length,
 assets:report.files.filter((v:any)=>v.path.startsWith('assets/generated')).length,status:report.status}))
