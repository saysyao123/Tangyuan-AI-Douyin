import {describe,it,expect} from 'vitest'
import {ActorPresentation} from './actor-presentation.js'
const p=(col:number,row=0)=>Object.freeze({col,row,height:0})
describe('display-only actor tracks',()=>{
 it('interpolates unchanged frozen canonical endpoints and settles; retains walk phase until settlement',()=>{
  const a=new ActorPresentation(80),start=p(4),end=p(5)
  a.begin();a.sample('party:child',start,0);a.phase('party:child',2,true);a.end()
  a.begin();expect(a.sample('party:child',end,100).pos.col).toBe(4);expect(a.phase('party:child',undefined,true)).toBe(2);a.end()
  for(const [t,col] of [[120,4.25],[140,4.5],[180,5]]){a.begin();expect(a.sample('party:child',end,t).pos.col).toBe(col);a.end()}
  expect(a.sample('party:child',end,200).moving).toBe(false);expect(a.phase('party:child',undefined,false)).toBeUndefined();expect(end).toEqual(p(5))
 })
 it('snaps teleports, explicit scene/restore resets and hidden/reappearing actors independently',()=>{
  const a=new ActorPresentation();a.begin();a.sample('entity:guard',p(0),0);a.sample('party:child',p(8),0);a.end()
  a.begin();expect(a.sample('entity:guard',p(10),10).pos.col).toBe(10);a.sample('party:child',p(9),10);a.end()
  a.begin();a.sample('party:child',p(9),20);a.end();a.begin();expect(a.sample('entity:guard',p(10.5),30).pos.col).toBe(10.5);a.end()
  a.reset();a.begin();expect(a.sample('party:child',p(8),40).pos.col).toBe(8);a.end()
 })
 it('explicit NPC placement snaps even within a single grid cell',()=>{const a=new ActorPresentation();a.begin();a.sample('entity:officer',p(1),0,false);a.end();a.begin();expect(a.sample('entity:officer',p(1.5),20,false).pos.col).toBe(1.5);a.end()})
 it('exposes immutable copies of the actual draw inputs',()=>{
  const a=new ActorPresentation();a.begin();a.sample('party:child',p(1),0);a.record('party:child',p(1),p(.75),true,7);const s=a.snapshot();expect(Object.isFrozen(s[0]?.displayed)).toBe(true);expect(s[0]?.frame).toBe(7);expect(()=>{(s[0]!.canonical as {col:number}).col=99}).toThrow()
 })
})
