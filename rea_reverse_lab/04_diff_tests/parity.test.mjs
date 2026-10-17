import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {step2048} from '../03_reconstruction/engine.mjs';

const root=process.env.UPSTREAM_2048||'rea_reverse_lab/upstream';
const original=['tile.js','grid.js','game_manager.js'].map(f=>fs.readFileSync(path.join(root,'js',f),'utf8')).join('\n');
function prng(seed){let s=seed>>>0;return {reset(n){s=n>>>0},next(){s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296}}}
const refRandom=prng(1);
const math=Object.create(Math);math.random=()=>refRandom.next();
const context={Math:math};vm.createContext(context);
vm.runInContext(original,context,{filename:'pinned-original-2048.js',timeout:5000});
class Input{on(){}}
class Actuator{actuate(){}continueGame(){}}
class Store{getGameState(){return null}getBestScore(){return 0}setBestScore(){}setGameState(){}clearGameState(){}}
function originalStep(state,dir,seed){
 refRandom.reset(33);
 const g=new context.GameManager(4,Input,Actuator,Store);
 g.grid=new context.Grid(4);
 for(let x=0;x<4;x++)for(let y=0;y<4;y++){
  const v=state.cells[x][y];if(v)g.grid.insertTile(new context.Tile({x,y},v));
 }
 g.score=state.score;g.over=state.over;g.won=state.won;g.keepPlaying=state.keepPlaying;
 refRandom.reset(seed);
 g.move(dir);
 return {cells:Array.from({length:4},(_,x)=>Array.from({length:4},(_,y)=>g.grid.cells[x][y]?.value??0)),
 score:g.score,over:g.over,won:g.won,keepPlaying:g.keepPlaying};
}
function board(...rows){return Array.from({length:4},(_,x)=>Array.from({length:4},(_,y)=>rows[y][x]));}
function state(cells,o={}){return {cells,score:o.score??0,over:o.over??false,won:o.won??false,keepPlaying:o.keepPlaying??false};}
const cases=[
 state(board([2,2,2,2],[0,0,0,0],[0,0,0,0],[0,0,0,0])),
 state(board([2,2,4,4],[2,0,2,0],[0,0,0,0],[0,0,0,0])),
 state(board([1024,1024,0,0],[2,4,8,16],[0,0,0,0],[0,0,0,0])),
 state(board([2,4,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,2])),
 state(board([4,0,0,0],[0,8,0,0],[0,0,16,0],[0,0,0,32])),
 state(board([2,2,2,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]),{score:20}),
 state(board([2048,2,4,8],[0,0,0,0],[0,0,0,0],[0,0,0,0]),{won:true}),
 state(board([2048,2,4,8],[0,0,0,0],[0,0,0,0],[0,0,0,0]),{won:true,keepPlaying:true}),
 state(board([2,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]),{over:true}),
 state(board([0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]))
];
const gen=prng(48239);
for(let i=0;i<300;i++){
 const p=gen.next();
 const cells=Array.from({length:4},()=>Array.from({length:4},()=>gen.next()<p?0:2**(1+Math.floor(gen.next()*10))));
 cases.push(state(cells,{score:Math.floor(gen.next()*1000)}));
}
test('pinned original 2048 vs independent reconstruction, 1240 differential pairs',()=>{
 let count=0;
 cases.forEach((s,i)=>{
  for(let direction=0;direction<4;direction++){
   const seed=(i*1315423911+direction*7907+17)>>>0;
   const rng=prng(seed);
   const actual=step2048(s,direction,()=>rng.next());
   const expected=originalStep(s,direction,seed);
   assert.deepStrictEqual(actual,expected,'case '+i+' direction '+direction+' seed '+seed);
   count++;
  }
 });
 assert.equal(count,1240);
 console.log('PARITY_OK cases='+count);
});
