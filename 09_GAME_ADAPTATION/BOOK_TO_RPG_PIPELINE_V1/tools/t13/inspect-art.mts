import fs from 'node:fs/promises'
import path from 'node:path'
import {createServer} from 'vite'
const root=path.resolve(process.argv[2],'packages/editor')
const vite=await createServer({root,configFile:path.join(root,'vite.config.ts'),server:{middlewareMode:true},appType:'custom'})
try{const m=await vite.ssrLoadModule('/scripts/type_pal_t1_art.ts');await fs.writeFile(process.argv[3],JSON.stringify({colors:m.colors,frames:m.previewFrames().map((f:any)=>({...f,pixels:[...f.pixels],opaque:[...f.opaque]}))}))}finally{await vite.close()}
