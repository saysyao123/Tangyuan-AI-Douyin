import fs from 'node:fs/promises'
import { compressGzip, encodeSpriteChunk } from '@type-pal/reforge'
export async function environmentArt(packFile:string){
 const pack=JSON.parse(await fs.readFile(packFile,'utf8')),result:Record<string,Buffer>={}
 for(const [name,f]of Object.entries(pack)as[string,any][]){const frame={...f,pixels:Uint8Array.from(Buffer.from(f.pixels,'base64')),opaque:Uint8Array.from(Buffer.from(f.opaque,'base64'))};result[name]=Buffer.from(await compressGzip(encodeSpriteChunk([frame])))}
 return result
}
