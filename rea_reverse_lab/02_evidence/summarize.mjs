import fs from 'node:fs';
const input=process.argv[2],output=process.argv[3];
let report={status:'BLOCKED',gameManagerObserved:false,analyzedModuleCount:null,limitations:[]};
try{
 const obj=JSON.parse(fs.readFileSync(input,'utf8'));
 report.gameManagerObserved=JSON.stringify(obj).includes('game_manager.js');
 let max=0;
 function walk(v,depth=0){
  if(depth>25||v===null||typeof v!=='object')return;
  if(Array.isArray(v)){for(const c of v)walk(c,depth+1);return}
  if(Array.isArray(v.modules))max=Math.max(max,v.modules.length);
  for(const [k,x] of Object.entries(v))if(k!=='modules')walk(x,depth+1);
 }
 walk(obj);report.analyzedModuleCount=max||null;
 report.status=report.gameManagerObserved?'EVIDENCE_FOUND':'UNCONFIRMED';
 if(!report.gameManagerObserved)report.limitations.push('game_manager.js not referenced in actual REA Evidence');
}catch(e){report.limitations.push(String(e.message))}
fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
if(report.status!=='EVIDENCE_FOUND')process.exitCode=1;
