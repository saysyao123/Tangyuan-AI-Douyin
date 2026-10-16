import type { GridPos } from '@type-pal/content'
interface Track { from: GridPos; target: GridPos; began: number; phase?: number }
interface DrawObservation { id: string; canonical: GridPos; displayed: GridPos; moving: boolean; frame: number }
/** Display-only tracks. Stable actor keys; canonical positions are never modified. */
export class ActorPresentation {
  private tracks = new Map<string, Track>()
  private live = new Set<string>()
  private observations: DrawObservation[] = []
  constructor(private readonly duration = 80) {}
  reset(): void { this.tracks.clear(); this.live.clear(); this.observations = [] }
  begin(): void { this.live.clear(); this.observations = [] }
  end(): void { for (const id of this.tracks.keys()) if (!this.live.has(id)) this.tracks.delete(id) }
  sample(id: string, canonical: GridPos, now: number, interpolate = true): { pos: GridPos; moving: boolean } {
    this.live.add(id)
    let track = this.tracks.get(id)
    const distance = track ? Math.abs(canonical.col - track.target.col) + Math.abs(canonical.row - track.target.row) : Infinity
    if (!track || (!interpolate && distance > .001) || distance > 1.01 || canonical.height !== track.target.height) {
      track = { from: { ...canonical }, target: { ...canonical }, began: now }
      this.tracks.set(id, track)
    }
    const at = (): GridPos => {
      const t = Math.max(0, Math.min(1, (now - track.began) / this.duration))
      return { col: track.from.col + (track.target.col - track.from.col) * t, row: track.from.row + (track.target.row - track.from.row) * t, height: track.target.height }
    }
    if (canonical.col !== track.target.col || canonical.row !== track.target.row) {
      track.from = at(); track.target = { ...canonical }; track.began = now
    }
    const pos = at()
    return { pos, moving: Math.abs(pos.col - canonical.col) + Math.abs(pos.row - canonical.row) > .001 }
  }
  phase(id: string, current: number | undefined, moving: boolean): number | undefined {
    const track = this.tracks.get(id)
    if (track && current !== undefined) track.phase = current
    return current ?? (moving ? track?.phase : undefined)
  }
  record(id: string, canonical: GridPos, displayed: GridPos, moving: boolean, frame: number): void {
    this.observations.push({ id, canonical: { ...canonical }, displayed: { ...displayed }, moving, frame })
  }
  snapshot(): readonly Readonly<DrawObservation>[] {
    return Object.freeze(this.observations.map(row => Object.freeze({ ...row, canonical: Object.freeze({ ...row.canonical }), displayed: Object.freeze({ ...row.displayed }) })))
  }
}
