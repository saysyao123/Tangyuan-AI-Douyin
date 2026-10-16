/** Resolve the welcome by its quest condition, independent of branch nesting. */
interface Row { text: string }
interface Command { kind: string; cond?: {kind?: string; flag?: string}; then?: Command[]; else?: Command[]; cue?: {identity?: {kind?: string; actor?: string}; rows?: Row[]} }
export function welcomeRow(flow: {stages: {body: Command[]}[]}): Row {
  const found: Row[] = []
  function visit(body: Command[]) {
    for (const command of body) {
      if (command.kind === 'branch' && command.cond?.kind === 'flag' && command.cond.flag === 'quest_started') {
        const dialog = command.else?.find(c => c.kind === 'dialog' && c.cue?.identity?.actor === 'keeper')
        if (dialog?.cue?.rows?.length === 1) found.push(dialog.cue.rows[0]!)
      }
      if (command.then) visit(command.then)
      if (command.else) visit(command.else)
    }
  }
  for (const stage of flow.stages) visit(stage.body)
  if (found.length !== 1) throw new Error('无法唯一定位初次对白，请使用完整剧本编辑器。')
  return found[0]!
}
