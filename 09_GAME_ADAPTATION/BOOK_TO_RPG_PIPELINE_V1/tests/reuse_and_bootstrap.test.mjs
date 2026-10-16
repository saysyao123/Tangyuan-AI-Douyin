import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRun} from '../tools/new_book_run.mjs';
import {validateGame,buildHtml} from '../tools/pipeline.mjs';
import {GameRules} from '../src/rules.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const stories=['lantern-inn','river-ledger'];
test('two distinct original content packs pass without changing engine code',()=>{
 for(const slug of stories){
  const g=JSON.parse(fs.readFileSync(path.join(root,'examples',slug,'game.json'),'utf8'));
  assert.equal(validateGame(g).ok,true,slug);
  const h=buildHtml(g);assert.ok(h.includes(g.title));assert.ok(h.includes(g.introHint));
  assert.equal(GameRules.initial(g).gameId,g.id);
 }
});
test('second story battle/reward and intro do not mention first story',()=>{
 const g=JSON.parse(fs.readFileSync(path.join(root,'examples/river-ledger/game.json'),'utf8'));
 let s=GameRules.initial(g);assert.ok(!s.message.includes('守灯人'));
 for(const dir of ['down',...Array(7).fill('right'),'up',...Array(4).fill('right')]){
  s=GameRules.act(g,s,{type:'MOVE',direction:dir});
 }
 assert.equal(s.battle.id,'river_beast');
 s=GameRules.act(g,s,{type:'ATTACK'});
 assert.ok(s.message.includes('河泽野兽')&&!s.message.includes('雾狼'));
});
test('new-book scaffolder creates 8 stages, no unsupported PASS claim',()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'bookrpg-'));
 try{
  const x=createRun('test-novel','测试小说',temp);
  assert.equal(x.stages,8);
  const state=JSON.parse(fs.readFileSync(path.join(x.dest,'STATUS.json'),'utf8'));
  assert.equal(state.nextStage,'S0');
  assert.equal(state.stages.S7,'NOT_STARTED');
  const rights=JSON.parse(fs.readFileSync(path.join(x.dest,'S0_INPUT_AND_RIGHTS/source_manifest.json'),'utf8'));
  assert.equal(rights.rights_status,'NOT_VERIFIED');assert.deepEqual(rights.source_files,[]);
  assert.throws(()=>createRun('test-novel','标题',temp),/Refusing to overwrite/);
  assert.throws(()=>createRun('../danger','坏',temp),/slug/);
 }finally{fs.rmSync(temp,{recursive:true,force:true})}
});
