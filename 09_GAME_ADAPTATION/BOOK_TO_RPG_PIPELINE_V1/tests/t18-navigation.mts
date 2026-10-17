import assert from 'node:assert/strict'
import {navigationPath,nearestStandable}from'../tools/t18/navigation.js'
import {motionTerrainSweepBlocked,motionSweepsConflict}from'../../packages/reforge/src/entity-motion.js'
const pos=(col:number,row:number)=>({col,row,height:0}),body=[{dcol:0,drow:0}]
const npc=pos(4,2),blocked=(p:{col:number;row:number})=>p.col<0||p.col>7||p.row<0||p.row>6||(p.col===2&&p.row<4)
const step=(a:ReturnType<typeof pos>,b:ReturnType<typeof pos>)=>!motionTerrainSweepBlocked(a,b,body,blocked)&&!motionSweepsConflict(a,b,body,npc,npc,body)
const goal=(p:ReturnType<typeof pos>)=>Math.max(Math.abs(p.col-npc.col),Math.abs(p.row-npc.row))<=1
const route=navigationPath(pos(.25,.25),goal,step,400)
assert.ok(route?.length,'fractional start must route around wall and approach NPC body')
let last=pos(.25,.25)
for(const next of route){assert.ok(step(last,next.pos),'every partial/full leg must satisfy native continuous sweep');assert.ok(next.pos.col===last.col||next.pos.row===last.row);last=next.pos}
assert.ok(goal(last));assert.ok(route.some(s=>s.pos.row>=4),'must detour through wall opening')
assert.equal(navigationPath(pos(0,0),p=>p.col===6,()=>false,100),null)
const safe=nearestStandable(pos(2,2),p=>!blocked(p)&&Math.max(Math.abs(p.col-npc.col),Math.abs(p.row-npc.row))>=1,step)
assert.ok(safe);assert.ok(!blocked(safe));assert.ok(Math.max(Math.abs(safe.col-2),Math.abs(safe.row-2))<=4)
console.log('T18_NATIVE_SWEEP_FRACTIONAL_DETOUR_AND_RECOVERY_PASS')
