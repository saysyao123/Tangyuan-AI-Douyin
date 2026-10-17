import type { Facing, GridPos } from '@type-pal/content'

const STEPS: readonly [Facing, number, number][] = [
  ['right', 1, 0],
  ['down', 0, 1],
  ['left', -1, 0],
  ['up', 0, -1],
]
export interface NavigationStep {
  pos: GridPos
  direction: Facing
}

/** Bounded four-axis search. The caller supplies the SAME swept terrain/occupancy rule as walking. */
export function navigationPath(
  from: GridPos,
  goal: (pos: GridPos) => boolean,
  canStep: (from: GridPos, to: GridPos) => boolean,
  limit: number,
): NavigationStep[] | null {
  const queue = [{ pos: from, parent: -1, direction: 'down' as Facing }]
  const key = (p: GridPos) => `${p.col.toFixed(5)},${p.row.toFixed(5)}`
  const seen = new Set([key(from)])
  for (let i = 0; i < queue.length && i < limit; i++) {
    const current = queue[i]
    if (!current) break
    if (goal(current.pos)) {
      const result: NavigationStep[] = []
      let at = i
      while (at > 0) {
        const node = queue[at]
        if (!node) break
        result.push({ pos: node.pos, direction: node.direction })
        at = node.parent
      }
      return result.reverse()
    }
    for (const [direction, dc, dr] of STEPS) {
      const next = (value: number, direction: number) =>
        direction > 0 ? Math.floor(value + 1e-6) + 1 : Math.ceil(value - 1e-6) - 1
      const pos = {
        ...from,
        col: dc ? next(current.pos.col, dc) : current.pos.col,
        row: dr ? next(current.pos.row, dr) : current.pos.row,
      }
      const id = key(pos)
      if (seen.has(id) || !canStep(current.pos, pos)) continue
      seen.add(id)
      queue.push({ pos, parent: i, direction })
    }
  }
  return null
}

/** Content updates can put a real saved position inside new furniture. Never alter story data. */
export function nearestStandable(
  from: GridPos,
  free: (pos: GridPos) => boolean,
  canStep: (from: GridPos, to: GridPos) => boolean,
): GridPos | null {
  for (let radius = 0; radius <= 4; radius++) {
    const candidates: GridPos[] = []
    for (let dc = -radius; dc <= radius; dc++)
      for (let dr = -radius; dr <= radius; dr++) {
        if (Math.max(Math.abs(dc), Math.abs(dr)) !== radius) continue
        candidates.push({ ...from, col: Math.round(from.col) + dc, row: Math.round(from.row) + dr })
      }
    candidates.sort(
      (a, b) =>
        Math.hypot(a.col - from.col, a.row - from.row) -
        Math.hypot(b.col - from.col, b.row - from.row),
    )
    for (const pos of candidates)
      if (
        free(pos) &&
        STEPS.some(([, dc, dr]) => canStep(pos, { ...pos, col: pos.col + dc, row: pos.row + dr }))
      )
        return pos
  }
  return null
}
