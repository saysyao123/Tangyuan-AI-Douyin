import fs from 'node:fs/promises'
import path from 'node:path'
import {pathToFileURL} from 'node:url'
import {gunzipSync} from 'node:zlib'
import {createHash} from 'node:crypto'
import assert from 'node:assert/strict'
const root=path.resolve(process.argv[2]),project=path.join(root,'projects/book-pilot-opening')
const {parseSpriteChunk}=await import(pathToFileURL(path.join(root,'packages/shared/src/index.ts')).href)
const results=[]
for(const [id,w,h,count] of [['hero',36,56,12],['child',32,44,12],['merchant',36,56,1],['stage',128,100,1],['house',128,112,1],['tree',72,88,1]]){
 const frames=parseSpriteChunk(new Uint8Array(gunzipSync(await fs.readFile(path.join(project,'assets/generated/sprites/'+id+'.rle')))))
 assert.equal(frames.length,count)
 const hashes=frames.map(f=>{assert.equal(f.width,w);assert.equal(f.height,h);assert.ok(f.opaque.some(x=>x===1));return createHash('sha256').update(f.pixels).update(f.opaque).digest('hex')})
 if(count===12)for(let dir=0;dir<4;dir++)assert.equal(new Set(hashes.slice(dir*3,dir*3+3)).size,3,'three poses must differ in each native direction')
 results.push({id,width:w,height:h,frames:count,uniqueFrames:new Set(hashes).size})
}
console.log(JSON.stringify({status:'PASS',nativeRLE:results,source:'Official shared parseSpriteChunk on final compressed project assets'},null,2))
