import {test,expect} from 'vitest'
import {Keyboard} from './input.js'
import {PresentationPosition} from './presentation-position.js'
function key(target:EventTarget,type:string,k:string){const e=new Event(type);Object.defineProperty(e,'key',{value:k});target.dispatchEvent(e)}
test.each(['blur','pagehide'])('lost keyup on %s releases held and pending input',event=>{
 const t=new EventTarget(),kb=new Keyboard(t as unknown as Window);key(t,'keydown','ArrowRight');key(t,'keydown',' ');t.dispatchEvent(new Event(event));expect(kb.isDown('ArrowRight')).toBe(false);expect(kb.consumePressed().size).toBe(0)
})
test('visibility loss releases keys without needing keyup',()=>{const t=new EventTarget() as EventTarget & {document:EventTarget & {hidden:boolean}};t.document=Object.assign(new EventTarget(),{hidden:false});const kb=new Keyboard(t as unknown as Window);key(t,'keydown','ArrowUp');t.document.hidden=true;t.document.dispatchEvent(new Event('visibilitychange'));expect(kb.isDown('ArrowUp')).toBe(false)})
test('display interpolation stays within committed segment and leaves gameplay object intact',()=>{const p=new PresentationPosition(80),a={col:10,row:0,height:0},b={col:11,row:0,height:0};p.sample('inn',a,100);p.sample('inn',b,110);expect(p.sample('inn',b,150).pos.col).toBe(10.5);expect(p.sample('inn',b,190).pos).toEqual(b);expect(b).toEqual({col:11,row:0,height:0})})
test('scene transitions, teleport/load and interaction snap immediately',()=>{const p=new PresentationPosition(),a={col:10,row:0,height:0};p.sample('inn',a,1);expect(p.sample('forest',{col:8,row:0,height:0},2).pos.col).toBe(8);expect(p.sample('forest',{col:15,row:0,height:0},3).pos.col).toBe(15);expect(p.sample('forest',{col:16,row:0,height:0},4,false).pos.col).toBe(16)})
