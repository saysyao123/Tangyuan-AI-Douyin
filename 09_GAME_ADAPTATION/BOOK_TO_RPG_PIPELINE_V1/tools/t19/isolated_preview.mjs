/* T19 P2 isolated preview overlay. Preserve all T18 scene logic, collision and SAVE12.
   This writes only to a copy of the PUBLIC fixture web runtime, never production Site. */
import fs from 'node:fs/promises'
import path from 'node:path'
import {createHash} from 'node:crypto'
import {spawnSync} from 'node:child_process'
import {fileURLToPath} from 'node:url'
const book=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..')
const web=path.resolve(process.argv[2]??'web')
const source=path.join(web,'chapter/game'),target=path.join(web,'t19-preview')
const project='projects/book-pilot-cinematic'
await fs.access(path.join(source,project,'assets/index.json'))
const art=path.join(web,'t19-generated')
const generated=spawnSync('python3',[path.join(book,'tools/t19/generate_table.py'),art],{stdio:'inherit'})
if(generated.status!==0)throw Error('Failed to generate T19 table candidate')
await fs.rm(target,{recursive:true,force:true})
await fs.cp(source,target,{recursive:true})
const catalogPath=path.join(target,project,'assets/index.json')
const cat=JSON.parse(await fs.readFile(catalogPath,'utf8'))
const matches=Object.entries(cat.assets).filter(([id,a])=>id==='night.noodle-table'||(a.path??'').endsWith('/noodle-table.rle'))
if(matches.length!==1)throw Error('No unique original noodle-table sprite asset: '+matches.map(x=>x[0]))
const [id,asset]=matches[0]
if(asset.kind!=='sprite')throw Error('expected native sprite asset kind')
const newFile=await fs.readFile(path.join(art,'noodle-table-preview.rle'))
const native=path.join(target,project,asset.path)
await fs.access(native)
const before=await fs.readFile(native)
await fs.writeFile(native,newFile)
const sha=data=>createHash('sha256').update(data).digest('hex')
cat.assets[id]={...asset,bytes:newFile.length,sha256:sha(newFile)}
await fs.writeFile(catalogPath,JSON.stringify(cat,null,2)+'\n')
const after=JSON.parse(await fs.readFile(catalogPath,'utf8'))
if(after.assets[id].sha256!==sha(await fs.readFile(native)))throw Error('Asset catalog digest mismatch')
const status={phase:'T19_P2_ISOLATED_PREVIEW',source:'T18 public fixture, unchanged',role:'single room meal-table draft',
 assetId:id,path:asset.path,beforeSHA256:sha(before),afterSHA256:sha(newFile),otherAssetsChanged:false,
 siteDeployment:'none',storyCollisionSaveChanges:false,visualQA:'PENDING',enginePlaybackQA:'PENDING'}
await fs.writeFile(path.join(target,'T19_PREVIEW.json'),JSON.stringify(status,null,2)+'\n')
console.log('T19_ISOLATED_ROOM_PREVIEW_READY',JSON.stringify(status))
