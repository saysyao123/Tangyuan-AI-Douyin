import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const dir=path.dirname(url.fileURLToPath(import.meta.url));
const root=path.resolve(dir,'..');
const safeId=/^[a-z][a-z0-9_-]{1,63}$/;
const allowedEffects=new Set(['set_flag','give_item','set_ending','give_gold']);
const errors=[];
export function validateGame(g){
  const err=[];
  const fail=msg=>err.push(msg);
  if(!g||g.format!=='book-rpg-game-v1')return {ok:false,errors:['format must be book-rpg-game-v1']};
  if(!safeId.test(g.id||''))fail('invalid game id');
  if(!g.title||!g.rights||!['original','public_domain','licensed'].includes(g.rights.source_kind)||!g.rights.status)fail('source rights missing/unsupported');
  if(g.baseline!=='PAL98_FREEZE_V0_1')fail('baseline mismatch');
  const lists=['characters','items','encounters','events'];
  for(const k of lists)if(!Array.isArray(g[k]))fail('array required: '+k);
  if(!g.world||!Array.isArray(g.world.scenes))fail('world.scenes required');
  if(err.length)return {ok:false,errors:err};
  const uniq=(list,k)=>{const seen=new Set();for(const x of list){if(!safeId.test(x?.id||''))fail(k+' invalid ID');if(seen.has(x.id))fail(k+' duplicate id '+x.id);seen.add(x.id)}return seen};
  const characters=uniq(g.characters,'characters'), items=uniq(g.items,'items'), en=uniq(g.encounters,'encounters'), events=uniq(g.events,'events'), scenes=uniq(g.world.scenes,'scenes');
  if(!characters.has(g.player?.id))fail('player not in characters');
  for(const k of ['maxHp','maxMp','attack','defense'])if(!Number.isInteger(g.player?.[k])||g.player[k]<0|| (k==='maxHp'&&!g.player[k]))fail('player invalid '+k);
  const byScene=new Map(g.world.scenes.map(x=>[x.id,x]));
  const byEvent=new Map(g.events.map(x=>[x.id,x]));
  const pass=(s,x,y)=>Number.isInteger(x)&&Number.isInteger(y)&&y>=0&&y<s.terrain?.length&&x>=0&&x<(s.terrain?.[0]?.length||0)&&s.terrain[y][x]!=='#';
  if(!scenes.has(g.world.startScene))fail('startScene missing');
  const ss=byScene.get(g.world.startScene);
  if(ss&&(!Array.isArray(g.player.position)||!pass(ss,...g.player.position)))fail('bad start position');
  let portals=0;
  for(const s of g.world.scenes){
    if(!Array.isArray(s.terrain)||s.terrain.length<3||typeof s.terrain[0]!=='string'||s.terrain[0].length<3) {fail('bad terrain '+s.id);continue}
    if(s.terrain.some(row=>typeof row!=='string'||row.length!==s.terrain[0].length||/[^.#]/.test(row)))fail('non-rectangular/invalid terrain '+s.id);
    if(!Array.isArray(s.exits)||!Array.isArray(s.entities)) {fail('exits/entities required '+s.id);continue}
    const positions=new Set();
    for(const obj of s.entities){
      if(!safeId.test(obj.id||''))fail('bad entity id in '+s.id);
      if(!pass(s,obj.x,obj.y))fail('entity '+obj.id+' out of bounds/blocked');
      const p=obj.x+','+obj.y;if(positions.has(p))fail('entity overlap '+s.id+':'+p);positions.add(p);
      if(obj.kind==='npc'){if(!events.has(obj.eventId))fail('npc missing event '+obj.id);if(obj.completedEventId&&!events.has(obj.completedEventId))fail('npc completion missing event '+obj.id);}
      else if(obj.kind==='item'){if(!items.has(obj.itemId))fail('item entity invalid '+obj.id);}
      else if(obj.kind==='enemy'){if(!en.has(obj.encounterId))fail('enemy entity invalid '+obj.id);}
      else fail('unknown entity kind '+obj.kind);
    }
    for(const e of s.exits){
      portals++;
      if(!scenes.has(e.to))fail('exit target missing '+s.id+'->'+e.to);
      if(!pass(s,e.x,e.y))fail('exit point blocked '+s.id);
      const target=byScene.get(e.to);
      if(target&&(!Array.isArray(e.spawn)||!pass(target,...e.spawn)))fail('exit spawn invalid '+s.id+'->'+e.to);
    }
  }
  if(!portals)fail('no world transitions');
  const reached=new Set(),pending=[g.world.startScene];
  while(pending.length){const id=pending.pop();if(reached.has(id)||!byScene.has(id))continue;reached.add(id);pending.push(...(byScene.get(id).exits||[]).map(e=>e.to))}
  for(const s of g.world.scenes)if(!reached.has(s.id))fail('unreachable scene '+s.id);
  for(const e of g.events){
    if(!e.text||!Array.isArray(e.effects))fail('event text/effects missing '+e.id);
    if(!Array.isArray(e.sourceRefs)||!e.sourceRefs.length)fail('event sourceRefs missing '+e.id);
    for(const ef of e.effects||[]){
      if(!allowedEffects.has(ef.type))fail('unsupported effect '+ef.type);
      if(ef.type==='give_item'&&!items.has(ef.target))fail('event gives unknown item '+ef.target);
      if(ef.type==='set_ending'&&ef.target!==g.ending?.id)fail('wrong ending target '+ef.target);
      if(ef.type==='give_gold'&&(!Number.isInteger(ef.value)||ef.value<0))fail('bad gold reward');
    }
    for(const r of e.requires||[]){
      if(r.type==='has_item'&&!items.has(r.target))fail('condition item missing '+r.target);
      if(!['has_item','flag'].includes(r.type))fail('unsupported condition '+r.type);
    }
  }
  if(!g.events.some(e=>(e.effects||[]).some(x=>x.type==='set_ending')))fail('no ending event');
  const endNpcs=g.world.scenes.flatMap(s=>s.entities.filter(e=>e.kind==='npc'&&[e.eventId,e.completedEventId].some(k=>byEvent.get(k)?.effects?.some(x=>x.type==='set_ending'))).map(e=>s.id));
  if(!endNpcs.some(id=>reached.has(id)))fail('no reachable ending NPC (coarse structural)');
  for(const e of g.encounters)if(![e.hp,e.attack,e.defense].every(v=>Number.isInteger(v)&&v>=0)||!e.hp)fail('invalid encounter '+e.id);
  if(!g.ending?.id||!g.ending?.title)fail('ending not defined');
  return {ok:err.length===0,errors:err,counts:{scenes:g.world.scenes.length,characters:g.characters.length,events:g.events.length,encounters:g.encounters.length,items:g.items.length}};
}
export function buildHtml(g){
  const check=validateGame(g);if(!check.ok)throw Error(check.errors.join('\n'));
  let tmpl=fs.readFileSync(path.join(root,'runtime','template.html'),'utf8');
  let engine=fs.readFileSync(path.join(root,'src','rules.mjs'),'utf8').replace(/^export const GameRules/m,'const GameRules');
  if(!tmpl.includes('/*__ENGINE__*/')||!tmpl.includes('/*__DATA__*/'))throw Error('template placeholder missing');
  return tmpl.replace('/*__ENGINE__*/',engine)
    .replace('/*__DATA__*/',JSON.stringify(g).replace(/</g,'\\u003c'));
}
function main(){
  const [cmd,input,out]=process.argv.slice(2);
  if(!['validate','build'].includes(cmd)||!input){console.error('Usage: node tools/pipeline.mjs validate|build game.json [output.html]');process.exitCode=2;return}
  try{
    const g=JSON.parse(fs.readFileSync(input,'utf8')),r=validateGame(g);
    if(!r.ok){console.error(JSON.stringify({status:'FAIL',...r},null,2));process.exitCode=1;return}
    if(cmd==='build'){
      if(!out)throw Error('output path required');
      const html=buildHtml(g);fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,html);
      console.log(JSON.stringify({status:'PASS',artifact:path.resolve(out),bytes:Buffer.byteLength(html),...r},null,2));
    }else console.log(JSON.stringify({status:'PASS',...r},null,2));
  }catch(e){console.error(JSON.stringify({status:'FAIL',error:e.message}));process.exitCode=1}
}
if(process.argv[1]&&path.resolve(process.argv[1])===url.fileURLToPath(import.meta.url))main();