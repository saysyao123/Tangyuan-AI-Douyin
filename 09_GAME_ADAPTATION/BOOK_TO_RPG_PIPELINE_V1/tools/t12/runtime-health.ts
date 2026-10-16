/** Read-only runtime health. Counters advance only at real engine call sites. */
export class RuntimeHealth {
  private frames = 0
  private draws = 0
  private lastFrameAt = 0
  private intervals: number[] = []
  private sampleAt = 0
  constructor() { document.addEventListener('visibilitychange', () => { this.sampleAt = 0 }) }
  private fatalMessage: string | null = null
  private storage = { sequence: 0, state: 'idle', message: '' }
  get failed(): boolean { return this.fatalMessage !== null }
  frame(now: number): void {
    if (!document.hidden && this.sampleAt > 0 && now > this.sampleAt) {
      this.intervals.push(now - this.sampleAt)
      if (this.intervals.length > 240) this.intervals.shift()
    }
    this.sampleAt = document.hidden ? 0 : now
    this.frames += 1
    this.lastFrameAt = now
  }
  draw(): void { this.draws += 1 }
  notice(state: string, message: string): void {
    this.storage = { sequence: this.storage.sequence + 1, state, message }
  }
  fail(error: unknown): void {
    if (this.failed) return
    this.fatalMessage = error instanceof Error ? error.message : String(error)
    document.documentElement.dataset.runtimeError = this.fatalMessage
    const panel = document.createElement('section')
    panel.id = 'runtime-recovery'
    panel.setAttribute('role', 'alert')
    panel.style.cssText = 'position:fixed;inset:15%;z-index:99999;background:#172b38;color:#f4e3b8;padding:24px;font:16px sans-serif'
    const message = document.createElement('p')
    message.textContent = '游戏暂时停止。已保存的进度仍在；重新载入后可读取，未保存的进度会丢失。'
    const retry = document.createElement('button')
    retry.textContent = '重新载入游戏'
    retry.onclick = () => location.reload()
    panel.append(message, retry)
    document.body.append(panel)
  }
  snapshot() {
    const ordered = [...this.intervals].sort((a, b) => a - b)
    const percentile = (p: number) => ordered[Math.min(ordered.length - 1, Math.floor(ordered.length * p))] ?? 0
    return Object.freeze({ frames: this.frames, draws: this.draws, lastFrameAt: this.lastFrameAt,
      p95FrameMs: percentile(.95), p99FrameMs: percentile(.99), error: this.fatalMessage,
      storage: Object.freeze({ ...this.storage }) })
  }
}
