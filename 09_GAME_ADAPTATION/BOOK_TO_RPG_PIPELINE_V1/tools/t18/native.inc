  // T18_NATIVE_NAVIGATION: opt-in author project; native motion remains the only walking writer.
  const pointNavigationEnabled = project.manifest.id === 'book-pilot-cinematic'
  let pointGoal: { scene: string; session: string; pos: GridPos; entityId?: string } | null = null
  let pointRoute: NavigationStep[] = []
  let pointHover: string | undefined
  let pointLastPlan = -Infinity
  let pointLastPosition = ''
  let pointLastProgress = 0
  let pointDirection: Facing | null = null
  const cancelPointNavigation = () => { pointGoal = null; pointRoute = []; pointDirection = null }
  const pointCanStep = (from: GridPos, to: GridPos) =>
    !isBlocked(to) && !motionTerrainSweepBlocked(from, to, [{ dcol: 0, drow: 0 }], pos => isBlockedAt(activeScene.map, pos)) &&
    !activeScene.scene.entities.some(e => entityLifecycleGates(e).collidable && motionSweepsConflict(from,to,[{dcol:0,drow:0}],e.pos,e.pos,[{dcol:0,drow:0}]))
  const pointEntity = (id: string) => activeScene.scene.entities.find(e => e.id === id)
  function pointInteractable(e: EntityDef): boolean {
    return e.pages?.[0]?.trigger?.on === 'interact' && entityLifecycleGates(e, {hasTrigger:true,triggerKind:'manual'}).manualInteractable
  }
  function nextPointDirection(): Facing | null {
    const goal = pointGoal
    if (!goal) return null
    if (goal.scene !== activeScene.scene.id || goal.session !== currentMotionSceneSessionId()) { cancelPointNavigation(); return null }
    const entity = goal.entityId ? pointEntity(goal.entityId) : undefined
    if (goal.entityId && (!entity || !pointInteractable(entity))) { cancelPointNavigation(); return null }
    const target = entity?.pos ?? goal.pos
    const range = entity ? Math.max(entity.pages?.[0]?.trigger?.range ?? 0, 1) : 0.55
    const arrived = (pos: GridPos) => gridDist(pos, target) <= range
    if (arrived(player.pos)) {
      cancelPointNavigation()
      if (entity && !worldTriggerDeliveryBusy() && pointInteractable(entity)) {
        facing = interactionFacingToward(player.pos, entity.pos)
        fireTrigger(entity)
      }
      return null
    }
    const now = performance.now(), position = `${player.pos.col},${player.pos.row}`
    if (position !== pointLastPosition) { pointLastPosition = position; pointLastProgress = now }
    if (now - pointLastProgress > 1200) { cancelPointNavigation(); showToast('前方暂时被挡住了，请换个落脚点。'); return null }
    if (now - pointLastPlan < 90) return pointDirection
    pointLastPlan = now
    const route = navigationPath(player.pos, arrived, pointCanStep, activeScene.map.width * activeScene.map.height * 4)
    if (!route?.length) { cancelPointNavigation(); showToast('这里暂时走不到，请点击道路或物件旁的空地。'); return null }
    pointRoute = route
    pointDirection = route[0]?.direction ?? null
    return pointDirection
  }
  function pointHit(x: number, y: number): EntityDef | undefined {
    const entities = activeScene.scene.entities.filter(pointInteractable)
    // Explicit foot markers remain selectable even when the authored sprite has transparent feet.
    const marker = entities.find(e => { const p=gridToPixel(e.pos); return Math.abs(x-p.x)<=5 && Math.abs(y-p.y-5)<=4 })
    if (marker) return marker
    return entities.filter(e => {
      const pixel = gridToPixel(e.pos), definition = activeScene.entitySpriteDefs.get(e.id)
      const frame = definition ? spriteCache.get(project.assetResolver, definition.asset)?.frames[worldPresentation.renderedEntityFrame(e.id) ?? 0] : undefined
      if (!frame) return false
      const localX=Math.floor(x-pixel.x+Math.floor(frame.width/2)),localY=Math.floor(y-pixel.y+frame.height-7)
      return localX>=0 && localY>=0 && localX<frame.width && localY<frame.height && frame.opaque[localY*frame.width+localX]!==0
    }).sort((a,b) => gridToPixel(b.pos).y-gridToPixel(a.pos).y)[0]
  }
  if (pointNavigationEnabled) {
    canvas.style.touchAction = 'none'
    const at = (event: PointerEvent) => {
      const rect = canvas.getBoundingClientRect()
      return {x:(event.clientX-rect.left)*320/rect.width+camera.x,y:(event.clientY-rect.top)*200/rect.height+camera.y}
    }
    canvas.addEventListener('pointermove', event => {
      const p = at(event); pointHover = pointHit(p.x,p.y)?.id
      canvas.style.cursor = pointHover ? 'pointer' : 'crosshair'
    })
    canvas.addEventListener('pointerleave', () => {pointHover = undefined})
    canvas.addEventListener('pointerdown', event => {
      if (event.button !== 0 || !event.isPrimary) return
      event.preventDefault(); window.focus()
      cancelPointNavigation()
      if (dialogBox.active && !scriptConfirmModal.active) { inputPorts.dialogue.advance(performance.now()); return }
      if (worldTriggerDeliveryBusy() || pendingTouchTrigger.pending) return
      const p = at(event), entity = pointHit(p.x,p.y)
      pointGoal = {scene:activeScene.scene.id,session:currentMotionSceneSessionId(),pos:{...pixelToGrid(p.x,p.y),height:0},...(entity ? {entityId:entity.id} : {})}
      pointLastPlan = -Infinity; pointLastProgress = performance.now(); pointLastPosition = ''
    })
    window.addEventListener('keydown', cancelPointNavigation)
    window.addEventListener('blur', cancelPointNavigation)
    document.addEventListener('visibilitychange', cancelPointNavigation)
  }
  function drawPointNavigation(): void {
    if (!pointNavigationEnabled || worldTriggerDeliveryBusy()) return
    ctx.save(); ctx.scale(WORLD_SCALE,WORLD_SCALE)
    ctx.font = '8px sans-serif'; ctx.textAlign = 'center'
    for (const e of activeScene.scene.entities.filter(pointInteractable)) {
      const p = gridToPixel(e.pos), x=p.x-camera.x, y=p.y-camera.y+5
      if (x<5 || x>315 || y<7 || y>194) continue
      ctx.fillStyle = '#e7bd79'; ctx.fillRect(Math.round(x)-1,Math.round(y)-1,3,3)
      if (e.id===pointHover || e.id===pointGoal?.entityId || gridDist(player.pos,e.pos)<=1) {
        const label = e.label ?? e.id, width=ctx.measureText(label).width+8
        ctx.fillStyle = '#15232be8';ctx.fillRect(x-width/2,y+4,width,12)
        ctx.fillStyle = '#f0d7a7';ctx.fillText(label,x,y+13)
      }
    }
    if (pointGoal) {
      for (const step of pointRoute.slice(0,12)) {
        const p=gridToPixel(step.pos);ctx.fillStyle='#e7bd7970';ctx.fillRect(Math.round(p.x-camera.x),Math.round(p.y-camera.y),2,1)
      }
      const p=gridToPixel(pointGoal.entityId ? pointEntity(pointGoal.entityId)?.pos ?? pointGoal.pos : pointGoal.pos)
      ctx.strokeStyle='#efca86';ctx.beginPath();ctx.ellipse(p.x-camera.x,p.y-camera.y,5,2.5,0,0,Math.PI*2);ctx.stroke()
    }
    ctx.restore()
  }
