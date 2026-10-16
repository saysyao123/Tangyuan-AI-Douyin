/** Explicit browser-storage workspace. Uses real OPFS directory handles and the
 * same official clone, save journal, workspace policy and finishOpen as local FSA.
 * Does not intercept showDirectoryPicker or grant access to user filesystem.
 */
import type {CurrentManifest} from '@type-pal/content'
import {httpSource} from '@type-pal/reforge'
import {cloneFromPal,type CloneProgress} from './clone.js'
import {finishOpen,type Opened} from './open-actions.js'
import {createLocalWorkspaceContext} from './workspace-context.js'
import {preflightFirstSaveTarget,authorizeFirstSaveTarget,withAuthorizedWorkspaceMutation,registerAuthorizedWorkspaceMutation} from './workspace-persistence.js'
export async function newBrowserStory(seedBaseUrl:string,onProgress:CloneProgress):Promise<Opened>{
 if(!isSecureContext||!navigator.storage?.getDirectory)throw Error('浏览器工程需要 HTTPS 和支持 OPFS 的浏览器。请下载工程并用 Chrome/Edge 打开本地项目。')
 const root=await navigator.storage.getDirectory()
 const dir=await root.getDirectoryHandle('lantern-'+crypto.randomUUID(),{create:true})
 const source=httpSource(seedBaseUrl)
 const manifest=await source.readJson<CurrentManifest>('manifest.json')
 const workspace=createLocalWorkspaceContext(manifest.id,'local-directory')
 await preflightFirstSaveTarget(workspace,dir)
 const target=await authorizeFirstSaveTarget(workspace,dir)
 return withAuthorizedWorkspaceMutation(target,async mutation=>{
  await registerAuthorizedWorkspaceMutation(mutation,workspace,dir.name)
  const saved=await cloneFromPal(source,mutation,onProgress)
  const opened=await finishOpen(dir,{workspaceHint:workspace,registrationMutation:mutation})
  return saved.cleanupWarning?{...opened,recoveryWarning:saved.cleanupWarning}:opened
 })
}
