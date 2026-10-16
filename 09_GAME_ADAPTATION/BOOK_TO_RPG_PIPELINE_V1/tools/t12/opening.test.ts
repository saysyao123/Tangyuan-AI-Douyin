// TEST-REFORGE-OPENING-IO-LIFECYCLE-1 — 标题读档 IO 与缩略图生命周期（GLM r2）。
// 排重：H2 flows 已证选定/空档 Esc 回退/跨页读档与完成时帧键收尾；observation 已证快照流；
// Q01 已证未处理键、环绕与单次进入逐槽恰读一次；host-lifecycle-1 已证标题读档端到端开局。
// r2 口径（Codex 一审 O-R1-01/02）：重复输入产生的双份 IO/解码与退出后继续解码属产品
// 缺陷面，只在隔离红反例（R4/R5b）中作诊断，不写成绿预期；O4 单次正常读档归
// existing-proof（flows H2 跨页读档），本文件不再为重复输入立绿合同。
// 本文件只保留合法残余合同：在途退出后迟到 IO 不复活退休菜单（O5）、重进消费
// 真实 store 更新后的新数据（O6）、有图/无图槽并存选档（O8）。
// IO 拒绝悬空（D-Q01-1）与位图不 close 同为缺陷面：隔离红反例交付，默认 suite 不留红/skip。
// @vitest-environment jsdom
import { buildWorld } from '@type-pal/content'
import { afterEach, expect, test } from 'vitest'
import { chromePng, installShellHost, type ShellHost } from './__tests__/runtime-shell/dom-host.js'
import { drain, key, until } from './__tests__/runtime-shell/driver.js'
import { shellProject } from './__tests__/runtime-shell/project.js'
import type { OpeningDecision, OpeningMenuObservation } from './opening-menu.js'
import { buildCurrentSavePayload } from './save/ops.js'
import { IndexedDbSaveStore, MemorySaveStore, type SaveStore } from './save/store.js'
import { type SaveMeta, type SlotId, slotKind } from './save/types.js'

let host: ShellHost | undefined
afterEach(() => {
  host?.close()
  host = undefined
})

function metaOf(slotId: SlotId, mapName: string, savedAt = 1000): SaveMeta {
  return {
    slotId,
    kind: slotKind(slotId),
    party: [{ name: 'Hero', level: 1 }],
    mapName,
    savedAt,
  }
}

/** 公开 SaveStore 边界的透明留痕层：真实读链路照跑，只记录调用序。 */
function tracedStore(real: SaveStore, reads: string[]): SaveStore {
  return {
    putSlot: (meta, payload, thumb) => real.putSlot(meta, payload, thumb),
    getPayload: (slotId) => real.getPayload(slotId),
    getThumb: async (slotId) => {
      reads.push(`thumb:${slotId}`)
      return real.getThumb(slotId)
    },
    listMeta: async () => {
      reads.push('meta')
      return real.listMeta()
    },
  }
}

/**
 * 卡内测试自用的公开边界注入（合法值/门控送达），底层读写全部落在真实 store：
 * 产品 SaveStore 合同本身允许 getThumb 返回 null（无缩略图槽）与任意 IO 延迟/拒绝。
 */
type Decorate = (real: SaveStore, reads: string[]) => SaveStore

async function opening(
  options: { metas?: SaveMeta[]; indexedDb?: boolean; decorate?: Decorate } = {},
) {
  host = await installShellHost()
  const fixture = await shellProject()
  const { loadMenuAssets } = await import('./menu/menu-box.js')
  const { projectItemsView } = await import('./runtime-project-view.js')
  const { loadGlyphs } = await import('./text/glyph.js')
  const { runOpeningMenu } = await import('./opening-menu.js')
  const menuAssets = await loadMenuAssets(
    projectItemsView(fixture.project.items),
    fixture.project.imageCache,
  )
  const real: SaveStore = options.indexedDb
    ? new IndexedDbSaveStore({ kind: 'project', projectId: 'shell-project' })
    : new MemorySaveStore({ kind: 'project', projectId: 'shell-project' })
  const entry = fixture.project.manifest.entryPoints[0]!
  const payload = buildCurrentSavePayload(
    buildWorld(entry.startWorld, fixture.project.actorsById),
    { sceneId: 'a', pos: { col: 2, row: 2, height: 0 }, facing: 'down' },
    'shell-project',
  )
  const seed = async (meta: SaveMeta): Promise<void> => {
    // 经产品写路径更新真实 store（同 payload 换 meta = 浏览界面可见快照更新）。
    await real.putSlot(meta, payload, new Blob([chromePng().slice().buffer], { type: 'image/png' }))
  }
  for (const meta of options.metas ?? []) await seed(meta)
  const reads: string[] = []
  const store = options.decorate ? options.decorate(real, reads) : tracedStore(real, reads)
  const canvas = document.querySelector('canvas')!
  const ctx = canvas.getContext('2d')!
  const bg = await createImageBitmap(new Blob([chromePng().slice().buffer]))
  const bitmapsBeforeMenu = host.bitmaps.length
  const snapshots: OpeningMenuObservation[] = []
  const done = runOpeningMenu({
    ctx,
    glyphs: await loadGlyphs(),
    bg,
    items: [
      { id: 'first', label: 'A' },
      { id: 'second', label: 'AA' },
    ],
    worldScale: 4,
    locale: {},
    menuAssets,
    saveStore: store,
    observe: (snapshot) => snapshots.push(snapshot),
  })
  const state: { value?: OpeningDecision } = {}
  const consumed = done.then((value) => {
    state.value = value
  })
  host.frame()
  return {
    h: host,
    state,
    done,
    consumed,
    reads,
    snapshots,
    seed,
    /** 宿主 createImageBitmap 记录中的缩略图位图（菜单启动后的增量）。 */
    thumbBitmaps: () => host!.bitmaps.slice(bitmapsBeforeMenu),
    async finish() {
      for (let i = 0; i < 3 && !state.value; i++) {
        await key(host!, 'Escape')
        await key(host!, 'ArrowDown')
        await key(host!, 'Enter')
      }
      if (!state.value) throw new Error('opening menu did not resolve during cleanup')
      await consumed
    },
  }
}

function spanTextsSince(host: ShellHost, mark: number): string[] {
  return host.text.mock.calls.slice(mark).flatMap((call) => call[1].map((span) => span.text))
}

test('T12 title storage failure is contained, retains selection and permits retry', async()=>{
 let fail=true
 const o=await opening({metas:[metaOf('m01','Map')],decorate:(real)=>({...real,putSlot:real.putSlot.bind(real),listMeta:real.listMeta.bind(real),getPayload:real.getPayload.bind(real),getThumb:async(id)=>{if(fail)throw Error('expected legal IO rejection');return real.getThumb(id)}})})
 await key(o.h,'ArrowUp');await key(o.h,'Enter');await drain()
 await o.h.frame();expect(o.snapshots.at(-1)?.phase).toBe('menu');expect(spanTextsSince(o.h,0)).toContain('存档读取失败，请重试')
 fail=false;await key(o.h,'Enter');await until(o.h,()=>o.snapshots.at(-1)?.phase==='load')
 await o.finish()
})

test('T12 repeated title selection does not duplicate in-flight IO',async()=>{
 let release:(value:SaveMeta[])=>void=()=>{};let calls=0
 const gate=new Promise<SaveMeta[]>(resolve=>{release=resolve})
 const o=await opening({decorate:(real)=>({putSlot:real.putSlot.bind(real),getPayload:real.getPayload.bind(real),getThumb:real.getThumb.bind(real),listMeta:()=>{calls++;return gate}})})
 await key(o.h,'ArrowUp');await key(o.h,'Enter');await key(o.h,'Enter');expect(calls).toBe(1)
 release([]);await until(o.h,()=>o.snapshots.at(-1)?.phase==='load');await o.finish()
})
