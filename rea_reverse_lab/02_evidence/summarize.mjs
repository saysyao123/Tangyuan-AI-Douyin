import fs from 'node:fs';
const [input,output]=process.argv.slice(2);
const report={status:'BLOCKED',reason:'Unverified output',metrics:{},limitations:[]};
try{
 const doc=JSON.parse(fs.readFileSync(input,'utf8'));
 const r=doc.normalized_result??{},graph=r.graph??{},semantic=r.semantic_graph??{},stats=r.statistics??{};
 const modules=(graph.nodes??[]).filter(n=>n.kind==='javascript-module');
 const gm=modules.filter(n=>(n.identity?.key??'').includes('js/game_manager.js'));
 const functions=(semantic.nodes??[]).filter(n=>n.kind==='function'&&n.identity?.module_path==='js/game_manager.js');
 report.metrics={parsed_javascript_files:stats.parsed_javascript_files??0,visited_ast_nodes:stats.visited_ast_nodes??0,
 commonjs_esm_modules:stats.modules??0,source_module_nodes:modules.length,
 graph_nodes:(graph.nodes??[]).length,graph_edges:(graph.edges??[]).length,
 semantic_nodes:(semantic.nodes??[]).length,semantic_relations:(semantic.relations??[]).length,
 semantic_unknowns:(semantic.unknowns??[]).length,game_manager_function_nodes:functions.length,
 graph_coverage:graph.coverage?.status??'unknown',semantic_coverage:semantic.coverage?.status??'unknown',
 integrity_contradictions:(r.integrity_contradictions??[]).length,parse_failures:stats.parse_failures??'unknown'};
 report.limitations=[...(r.limitations??[])];
 const ok=doc.operation==='analyze_javascript_application'&&stats.parsed_javascript_files>=3&&gm.length>=1&&
 functions.length>=1&&graph.coverage?.truncated===false&&!(r.integrity_contradictions??[]).length;
 report.status=ok?'EVIDENCE_VERIFIED':'EVIDENCE_INCOMPLETE';
 report.reason=ok?'REA AST and semantic graph contain original game-manager evidence':'Missing full-chain verified evidence';
}catch(e){report.limitations.push(String(e.message))}
fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
if(report.status!=='EVIDENCE_VERIFIED')process.exitCode=1;
