// @vitest-environment jsdom
import {expect,test} from 'vitest'
import {PresentationPosition} from './presentation-position.js'
import {RuntimeHealth} from './runtime-health.js'
import {welcomeRow} from './welcome-row.js'
test('adjacent restore explicitly resets display before the first sample',()=>{
 const p=new PresentationPosition(80),a={col:10,row:0,height:0},b={col:11,row:0,height:0}
 p.sample('inn',a,100);p.sample('inn',b,110);expect(p.sample('inn',b,120).pos.col).toBeLessThan(11)
 p.reset();expect(p.sample('inn',a,121)).toEqual({pos:a,moving:false})
})
test('engine counters are independent from observer reads and distinguish successful draw',()=>{
 const h=new RuntimeHealth();h.frame(100);h.draw();h.frame(120)
 expect(h.snapshot()).toMatchObject({frames:2,draws:1,lastFrameAt:120,p95FrameMs:20})
 for(let i=0;i<10;i++)h.snapshot()
 expect(h.snapshot().frames).toBe(2)
})
test('fatal frame recovery is visible once and preserves existing browser data',()=>{
 localStorage.setItem('saved-proof','unchanged');const h=new RuntimeHealth()
 h.fail(Error('frame failed'));h.fail(Error('second'));expect(h.failed).toBe(true)
 expect(document.querySelectorAll('#runtime-recovery')).toHaveLength(1)
 expect(document.querySelector('#runtime-recovery')?.textContent).toContain('已保存的进度仍在')
 expect(localStorage.getItem('saved-proof')).toBe('unchanged')
 document.querySelector('#runtime-recovery')?.remove();delete document.documentElement.dataset.runtimeError
})
test('welcome edit survives extra stages and outer branches and fails closed if ambiguous',()=>{
 const quest={kind:'branch',cond:{kind:'flag',flag:'quest_started'},else:[{kind:'dialog',cue:{identity:{kind:'actor',actor:'keeper'},rows:[{text:'hello'}]}}]}
 const flow={stages:[{body:[]},{body:[{kind:'branch',then:[quest]}]}]}
 expect(welcomeRow(flow).text).toBe('hello');welcomeRow(flow).text='changed';expect(quest.else[0]!.cue.rows[0]!.text).toBe('changed')
 expect(()=>welcomeRow({stages:[{body:[quest,quest]}]})).toThrow('唯一定位')
})

test('hidden and resumed gaps are excluded while visible stalls remain measured',()=>{
 Object.defineProperty(document,'hidden',{value:false,configurable:true});const h=new RuntimeHealth();h.frame(100);h.frame(120)
 Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));h.frame(5000)
 Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'));h.frame(10000);expect(h.snapshot().p99FrameMs).toBe(20)
 h.frame(12000);expect(h.snapshot().p99FrameMs).toBe(2000);delete (document as {hidden?:boolean}).hidden
})
