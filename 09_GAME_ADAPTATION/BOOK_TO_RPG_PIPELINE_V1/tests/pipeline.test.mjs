import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {GameRules} from '../src/rules.mjs';
import {validateGame,buildHtml} from '../tools/pipeline.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const game=JSON.parse(fs.readFileSync(path.join(root,'examples/lantern-inn/game.json'),'utf8'));
const dup=obj=>JSON.parse(JSON.stringify(obj));
const move=(s,d)=>GameRules.act(game,s,{type:'MOVE',direction:d});
const interact=s=>GameRules.act(game,s,{type:'INTERACT'});
const walk=(s,dir,n=1)=>{for(let i=0;i<n;i++)s=move(s,dir);return s};

test('original sample validates with full referential and map checks',()=>{
 const v=validateGame(game);assert.equal(v.ok,true,v.errors.join('\n'));assert.equal(v.counts.scenes,2);
});
test('source rights are mandatory',()=>{
 const c=dup(game);c.rights.source_kind='unknown';assert.equal(validateGame(c).ok,false);
});
test('stable IDs must be unique',()=>{
 const c=dup(game);c.world.scenes.push(dup(c.world.scenes[0]));assert.ok(validateGame(c).errors.some(e=>e.includes('duplicate id')));
});
test('bad portal destination/spawn is rejected',()=>{
 const c=dup(game);c.world.scenes[0].exits[0].to='missing';assert.equal(validateGame(c).ok,false);
 const d=dup(game);d.world.scenes[0].exits[0].spawn=[-1,0];assert.equal(validateGame(d).ok,false);
});
test('unreachable scene/ending and bad event references are rejected',()=>{
 const c=dup(game);c.world.scenes[0].exits=[];assert.equal(validateGame(c).ok,false);
 const d=dup(game);d.world.scenes[0].entities[0].completedEventId='bad';assert.equal(validateGame(d).ok,false);
});
test('event original provenance must be present',()=>{
 const c=dup(game);c.events[0].sourceRefs=[];assert.equal(validateGame(c).ok,false);
});
test('player collides with boundaries and NPC, then learns mission',()=>{
 let s=GameRules.initial(game);assert.deepEqual([s.x,s.y],[2,3]);
 s=walk(s,'up',3);assert.deepEqual([s.x,s.y],[2,1]);s=walk(s,'up');assert.deepEqual([s.x,s.y],[2,1]);
 s=walk(s,'down',2);s=walk(s,'right');assert.deepEqual([s.x,s.y],[3,3]);
 s=walk(s,'right');assert.deepEqual([s.x,s.y],[3,3]);
 s=interact(s);assert.equal(s.flags.quest_started,true);
});
test('map gate reaches forest and unique collectible is taken once',()=>{
 let s=GameRules.initial(game);s=walk(s,'down');s=walk(s,'right',7);s=walk(s,'up');
 assert.equal(s.sceneId,'forest');assert.deepEqual([s.x,s.y],[1,3]);
 s=walk(s,'up');s=walk(s,'right');s=interact(s);
 assert.equal(s.inventory.lamp_core,1);s=interact(s);assert.equal(s.inventory.lamp_core,1);
});
test('visible enemy triggers battle, with victory changing world flags',()=>{
 let s=GameRules.initial(game);s=walk(s,'down');s=walk(s,'right',7);s=walk(s,'up');
 s=walk(s,'right',3);assert.equal(s.x,4);s=walk(s,'right');assert.equal(s.x,4);
 assert.equal(s.battle.id,'mist_wolf');for(let i=0;i<3;i++)s=GameRules.act(game,s,{type:'ATTACK'});
 assert.equal(s.battle,null);assert.equal(s.flags.wolf_defeated,true);assert.equal(s.cleared.wolf,true);
 assert.equal(s.experience,12);assert.equal(s.gold,10);
});
test('magic costs MP and guard reduces damage; fleeing does not clear enemy',()=>{
 let s=GameRules.initial(game);s=walk(s,'down');s=walk(s,'right',7);s=walk(s,'up');s=walk(s,'right',4);
 assert.ok(s.battle);
 s=GameRules.act(game,s,{type:'MAGIC'});assert.equal(s.mp,9);assert.ok(s.battle.enemyHp<15);
 const hp=s.hp;s=GameRules.act(game,s,{type:'DEFEND'});assert.ok(s.hp<=hp);
 s=GameRules.act(game,s,{type:'FLEE'});assert.equal(s.battle,null);assert.equal(!!s.flags.wolf_defeated,false);
});
test('complete scripted journey reaches ending only with item and victory',()=>{
 let s=GameRules.initial(game);
 s=move(s,'right');s=interact(s);assert.equal(s.flags.quest_started,true);
 s=move(s,'down');s=walk(s,'right',6);s=move(s,'up');
 assert.equal(s.sceneId,'forest');
 s=move(s,'up');s=move(s,'right');s=interact(s);assert.equal(s.inventory.lamp_core,1);
 s=move(s,'down');s=walk(s,'right',2);s=move(s,'right');assert.ok(s.battle);
 while(s.battle)s=GameRules.act(game,s,{type:'ATTACK'});
 assert.equal(s.flags.wolf_defeated,true);
 s=walk(s,'left',3);assert.equal(s.sceneId,'inn');assert.deepEqual([s.x,s.y],[8,3]);
 s=walk(s,'left',3);s=interact(s);assert.equal(s.ending,'lights_return');
 assert.ok(s.message.includes('结局'));
});
test('save/restore retains exact world and rejects wrong game and corrupt location',()=>{
 let s=GameRules.initial(game);s=move(s,'right');s=interact(s);
 const snap=GameRules.snapshot(game,s);assert.deepEqual(GameRules.restore(game,snap),s);
 const other=dup(game);other.id='second-book';assert.throws(()=>GameRules.restore(other,snap),/invalid save/);
 const corrupted=dup(s);corrupted.x=-100;assert.throws(()=>GameRules.restore(game,JSON.stringify(corrupted)),/invalid save/);
});
test('a second original story can reuse unchanged engine (content ID/name swap)',()=>{
 const g=dup(game);g.id='second-book';g.title='另一段原创旅程';
 assert.equal(validateGame(g).ok,true);
 const st=GameRules.initial(g);assert.equal(st.gameId,'second-book');
});
test('offline build includes inline engine, unique game data, Chinese font',()=>{
 const html=buildHtml(game);
 assert.ok(html.includes('const GameRules'));
 assert.ok(html.includes('"lantern-inn"'));
 assert.ok(html.includes('书籍RPG制作线'));
 assert.ok(!html.includes('/*__ENGINE__*/'));
 assert.ok(!html.includes('/*__DATA__*/'));
 assert.ok(!html.includes('type="module"'));
});
