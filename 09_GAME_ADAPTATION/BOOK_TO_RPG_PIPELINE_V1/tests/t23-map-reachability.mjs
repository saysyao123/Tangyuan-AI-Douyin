/* T23 static first-act map topology gate.
   Checks all existing authored story routes, not just sprite loading.
   It deliberately does NOT mutate world flags/scene events/SAVE12. */
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const root='../t23site/chapter/game/projects/book-pilot-cinematic/content';
const expectations={
 fair:['vendor','stage','backstage-gate','exit'],
 backstage:['return'],
 street:['stranger','home-road','fair-return'],
 courtyard:['neighbor','medicine','home','street-return']
};
const result={status:'PASS',scenes:[],limitations:[
 'Static free-tile reachability only; dynamic actor blocking, dialogue gates and precise native movement still require browser playthrough.',
 'Original event flag order and story not rewritten by this test.']};
for(const [id,targets] of Object.entries(expectations)){
 const scene=JSON.parse(await fs.readFile(root+'/scenes/'+id+'.json','utf8'));
 const map=JSON.parse(await fs.readFile(root+'/maps/'+id+'.json','utf8'));
 const blocked=new Set(scene.entities.filter(e=>e.collide&&!e.hidden).map(e=>e.pos.col+','+e.pos.row));
 const free=(c,r)=>{
  const b=c+r,k=(c-r-(b&1))/2;
  return Number.isInteger(k)&&b>=0&&b<map.height*2&&k>=0&&k<map.width&&map.collision[b]?.[k]===0&&!blocked.has(c+','+r);
 };
 const start=[scene.entry.pos.col,scene.entry.pos.row],key=p=>p.join(',');
 assert.ok(free(...start),id+' entry blocked');
 const visited=new Map([[key(start),0]]),queue=[start];
 for(let i=0;i<queue.length;i++){
  const [c,r]=queue[i],distance=visited.get(key(queue[i]));
  for(const [dc,dr] of [[1,0],[-1,0],[0,1],[0,-1]]){
   const next=[c+dc,r+dr],k=key(next);
   if(!visited.has(k)&&free(...next)){visited.set(k,distance+1);queue.push(next)}
  }
 }
 const findings=[];
 for(const target of targets){
  const e=scene.entities.find(x=>x.id===target);
  assert.ok(e,'missing story entity '+id+'/'+target);
  const {col,row}=e.pos,adjacent=[[col-1,row],[col+1,row],[col,row-1],[col,row+1]];
  const closest=adjacent.map(p=>({p,steps:visited.get(key(p))})).filter(x=>x.steps!==undefined)
    .sort((a,b)=>a.steps-b.steps)[0];
  assert.ok(closest,'unreachable first-act event '+id+'/'+target);
  findings.push({target,nearestAdjacent:closest.p,steps:closest.steps});
 }
 result.scenes.push({id,entry:start,walkableTiles:visited.size,targets:findings});
}
await fs.mkdir('/tmp/t23-evidence',{recursive:true});
await fs.writeFile('/tmp/t23-evidence/T23_ROUTE_TOPOLOGY.json',JSON.stringify(result,null,2));
console.log('T23_FIRST_ACT_MAP_TOPOLOGY_PASS',JSON.stringify(result.scenes.map(s=>({id:s.id,targets:s.targets.length}))));
