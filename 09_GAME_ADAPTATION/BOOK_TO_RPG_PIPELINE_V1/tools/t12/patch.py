"""Exact, checked adapters for the pinned upstream + T1.1. No silent substitutions."""
from pathlib import Path
import shutil, sys

root = Path(sys.argv[1]); here = Path(__file__).parent
path = root / 'packages/reforge/src/main.ts'
source = path.read_text()
marker = '// T12_FOUNDATION'
def once(text, old, new):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'Patch anchor mismatch: expected 1, got {count}: {old[:95]}')
    return text.replace(old, new, 1)

if marker not in source:
    source = "import { RuntimeHealth } from './runtime-health.js'\nimport { assertCurrentSaveStructure } from './save/current-structure.js'\n" + source
    source = once(source, '  const displayPosition = new PresentationPosition(80)', '''  // T12_FOUNDATION
  const runtimeHealth = new RuntimeHealth()
  const displayPosition = new PresentationPosition(80)''')
    source = once(source, '    player.pos = plan.spawn.pos', '''    player.pos = plan.spawn.pos
    displayPosition.reset()
    renderedPlayerPos = { ...player.pos }''')
    source = once(source, '      player.pos = { ...pos }', '''      player.pos = { ...pos }
      displayPosition.reset()
      renderedPlayerPos = { ...player.pos }''')
    source = once(source, '      applyAmbienceTint()\n      return true', '      applyAmbienceTint()\n      runtimeHealth.draw()\n      return true')
    source = once(source, '      runWithPresentationFinalizer(render, abortScript)', '      runWithPresentationFinalizer(render, abortScript)\n      runtimeHealth.draw()')
    source = once(source, '''    await frames.tick(t, framePorts)
    requestAnimationFrame(tick)''', '''    if (runtimeHealth.failed) return
    try {
      await frames.tick(t, framePorts)
      runtimeHealth.frame(performance.now())
      requestAnimationFrame(tick)
    } catch (error) {
      runtimeHealth.fail(error)
      console.error('[runtime] 帧执行失败:', error)
    }''')
    source = once(source, '      projectId: inputProject.manifest.id,\n      sceneId:', '      projectId: inputProject.manifest.id,\n      health: runtimeHealth.snapshot(),\n      sceneId:')
    source = once(source, "    await doSave('quick', captureThumbnail(canvas))", "    runtimeHealth.notice('saving', '正在保存进度…')\n    await doSave('quick', captureThumbnail(canvas))\n    runtimeHealth.notice('saved', '进度已保存到当前浏览器。')")
    source = once(source, "    showToast('存档失败')", "    runtimeHealth.notice('error', '保存失败：请检查浏览器存储空间与权限，原存档不会因失败而删除。')\n    showToast('存档失败')")

    source = once(source, "    if (outcome === 'loaded') showToast('已读取快速存档')\n    else if (outcome === 'absent') showToast('无快速存档')", "    if (outcome === 'loaded') { showToast('已读取快速存档'); runtimeHealth.notice('loaded', '已读取快速存档。') }\n    else if (outcome === 'absent') { showToast('无快速存档'); runtimeHealth.notice('absent', '还没有快速存档，请先保存进度。') }")
    source = once(source, "    else if (outcome === 'absent') { showToast('无快速存档'); runtimeHealth.notice('absent', '还没有快速存档，请先保存进度。') }", "    else if (outcome === 'absent') { showToast('无快速存档'); runtimeHealth.notice('absent', '还没有快速存档，请先保存进度。') }\n    else runtimeHealth.notice('error', '读取未完成：存档校验或场景准备失败，当前进度未被替换。')")
    source = once(source, "  type LoadOutcome = 'loaded' | 'absent' | 'rejected'", "  type LoadOutcome = 'loaded' | 'absent' | 'rejected' | 'superseded'")
    source = once(source, "    let outcome: 'loaded' | 'absent' | 'rejected'", "    let outcome: LoadOutcome")
    start = source.index('  async function doLoad(')
    end = source.index('  async function quickSave()', start)
    part = source[start:end].replace("if (!loadIntent.isCurrent(token)) return 'rejected'", "if (!loadIntent.isCurrent(token)) return 'superseded'")
    part = once(part, "      showToast(`存档槽 ${slotId} 读取失败`)", "      runtimeHealth.notice('error', '读取失败：浏览器存储暂不可用，可重试；请勿清理网站数据。')\n      showToast(`存档槽 ${slotId} 读取失败`)")
    part = once(part, "    return (await restorePayload(p, token, where, signal)) ? 'loaded' : 'rejected'", "    const restored = await restorePayload(p, token, where, signal)\n    if (!loadIntent.isCurrent(token)) return 'superseded'\n    return restored ? 'loaded' : 'rejected'")
    source = source[:start] + part + source[end:]
    source = once(source, "    const outcome = await doLoad('quick')", "    const outcome = await doLoad('quick')\n    if (outcome === 'superseded') return")
    source = once(source, "    where: string,\n    signal?: AbortSignal,\n  ): Promise<boolean> {", "    where: string,\n    signal?: AbortSignal,\n    validateOnly = false,\n  ): Promise<boolean> {")
    source = once(source, '    // 从这里开始没有 await：强停旧演出、world 与 scene 在同一个任务中同步提交。', '    if (validateOnly) return true // Native preflight only: no world/scene/save mutation.\n    // 从这里开始没有 await：强停旧演出、world 与 scene 在同一个任务中同步提交。')
    source = once(source, '  function captureRuntimeObservation() {', '''  // Explicit player backup API; only current SAVE12, same project, native validation/write queue.
  let backupBusy = false
  ;(window as unknown as { tpPlayer?: unknown }).tpPlayer = Object.freeze({
    exportQuickSave: async () => {
      await saveWriteQueue
      const payload = await saveStore.getPayload('quick')
      if (!payload) throw new Error('还没有快速存档，请先保存进度。')
      return JSON.stringify(payload, null, 2)
    },
    importQuickSave: async (text: string) => {
      if (backupBusy) throw new Error('正在导入，请稍候。')
      backupBusy = true
      try {
        if (text.length > 5_000_000) throw new Error('备份文件过大。')
        const raw: unknown = JSON.parse(text)
        assertCurrentSaveStructure(raw)
        const payload = await normalizeStoredPayload(raw, '导入备份')
        if (!await restorePayload(payload, loadIntent.begin(), '导入备份', undefined, true)) throw new Error('备份无法恢复，未覆盖原存档。')
        const thumbnail = document.createElement('canvas')
        thumbnail.width = 64; thumbnail.height = 40
        const thumb = await captureThumbnail(thumbnail)
        const scheduled = saveWriteQueue.then(async () => {
          await saveMetasReady
          const metas = await saveStore.listMeta()
          const count = Math.max(committedSavedTimes, ...metas.map(m => m.savedTimes ?? 0)) + 1
          const meta = buildMeta('quick', payload.world, '导入备份', c => lookupText(`name.${c.template}`, project.locale), Date.now(), count)
          await saveStore.putSlot(meta, payload, thumb)
          committedSavedTimes = count
        })
        saveWriteQueue = scheduled.catch(() => undefined)
        await scheduled
        runtimeHealth.notice('saved', '备份已导入快速存档。按 F9 或“读取进度”恢复。')
      } finally { backupBusy = false }
    },
  })
  function captureRuntimeObservation() {''')
    path.write_text(source)
else:
    for expected in ['runtimeHealth.frame(performance.now())', 'runtimeHealth.draw()', 'displayPosition.reset()', 'assertCurrentSaveStructure(raw)', 'tpPlayer']:
        if expected not in source: raise RuntimeError('Incomplete T12 patch: ' + expected)

shutil.copyfile(here / 'runtime-health.ts', root / 'packages/reforge/src/runtime-health.ts')
# The revised display helper is shared with T1.1 callers.
shutil.copyfile(here.parent / 't11/presentation-position.ts', root / 'packages/reforge/src/presentation-position.ts')

path = root / 'packages/reforge/src/opening-menu.ts'
source = path.read_text()
if '// T12_OPENING_IO' not in source:
    source = once(source, '    let now = 0', "    let now = 0\n    // T12_OPENING_IO\n    let disposed = false\n    let loading = false\n    let loadError = ''")
    source = once(source, '      cancelAnimationFrame(raf)', '      disposed = true\n      for (const bitmap of thumbs.values()) bitmap.close()\n      thumbs.clear()\n      cancelAnimationFrame(raf)')
    a = source.index('    const enterLoad = async (): Promise<void> => {')
    b = source.index('\n\n    const onKey', a)
    source = source[:a] + '''    const enterLoad = async (): Promise<void> => {
      if (loading || disposed) return
      loading = true
      loadError = ''
      const staged = new Map<SlotId, ImageBitmap>()
      try {
        const metas = await saveStore.listMeta()
        if (disposed) return
        for (const meta of metas) {
          const blob = await saveStore.getThumb(meta.slotId)
          if (disposed) return
          if (blob) {
            const bitmap = await createImageBitmap(blob)
            if (disposed) { bitmap.close(); return }
            staged.set(meta.slotId, bitmap)
          }
        }
        for (const bitmap of thumbs.values()) bitmap.close()
        thumbs.clear()
        for (const [id, bitmap] of staged) thumbs.set(id, bitmap)
        staged.clear()
        browser = openSaveBrowser('load', metas)
        phase = 'load'
      } catch (error) {
        if (!disposed) {
          loadError = '存档读取失败，请重试'
          console.warn('[opening] 存档读取失败:', error)
        }
      } finally {
        for (const bitmap of staged.values()) bitmap.close()
        loading = false
      }
    }''' + source[b:]
    source = once(source, '      ctx.restore()\n      deps.observe?', '''      if (loadError || loading) renderSpans(ctx, [{ text: loadError || '正在读取存档…' }], 48, 170, { glyphs, shadow: true })
      ctx.restore()
      deps.observe?''')
    path.write_text(source)
elif 'staged.values()' not in source:
    raise RuntimeError('Incomplete opening IO patch')
print('T12_CHECKED_FOUNDATION_PATCH_APPLIED')
