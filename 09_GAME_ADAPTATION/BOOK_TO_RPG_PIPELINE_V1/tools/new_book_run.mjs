import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const root=path.resolve(path.dirname(url.fileURLToPath(import.meta.url)),'..');
const stages=[
['S0','INPUT_AND_RIGHTS',['source_manifest.json','chapter_index.json','rights.md']],
['S1','ORIGINAL_FACTS',['fact_ledger.json','timeline.json','character_relations.json','locations.json']],
['S2','GAME_DIRECTOR',['game_bible.md','beat_graph.json','character_cards.json','quest_graph.json']],
['S3','ASSETS',['assets_manifest.json','character_style_guide.md','scene_style_guide.md']],
['S4','CONTENT',['game.json','content_gate.json']],
['S5','ENGINE_BUILD',['build_log.txt','html_or_engine_adapter_output.txt']],
['S6','PLAYTHROUGH_QA',['qa_report.json','issues.md']],
['S7','RELEASE',['release_manifest.json','changelog.md']]
];
export function createRun(slug,title,rootDir=path.join(root,'runs')){
 if(!/^[a-z][a-z0-9-]{2,55}$/.test(slug))throw Error('slug should be lower-case letters/digits/hyphens, length 3-56');
 if(!title||title.length>150)throw Error('nonempty title up to 150 chars needed');
 const dest=path.join(rootDir,slug);if(fs.existsSync(dest))throw Error('Refusing to overwrite existing run '+slug);
 fs.mkdirSync(dest,{recursive:true});
 const status={project:slug,title,contract:'BOOK_TO_RPG_PIPELINE_V1',mechanics:'PAL98_FREEZE_V0_1',
  firstStage:'S0',nextStage:'S0',stages:Object.fromEntries(stages.map(([id])=>[id,'NOT_STARTED'])),
  notes:['Created from skeleton. No source book has been read or validated yet.','No phase is marked PASS.']};
 fs.writeFileSync(path.join(dest,'STATUS.json'),JSON.stringify(status,null,2)+'\n');
 const manifest={work_id:slug,book_title:title,source_kind:'unknown',rights_status:'NOT_VERIFIED',
  source_files:[],chapters_checked:0,chapters_expected:null,public_distribution_allowed:false};
 for(const [id,label,required] of stages){
   const folder=path.join(dest,id+'_'+label);fs.mkdirSync(folder);
   fs.writeFileSync(path.join(folder,'_REQUIRED_OUTPUTS.md'),
    '# '+id+' '+label+'\n\nRequired outputs after source review:\n'+required.map(x=>'- '+x).join('\n')+
    '\n\nGate: see docs/STAGES.md. Do not mark PASS without real evidence.\n');
   if(id==='S0')fs.writeFileSync(path.join(folder,'source_manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 }
 fs.writeFileSync(path.join(dest,'READ_ME_FIRST.md'),
  '# '+title+'\n\nThis is a NEW EMPTY work folder, not a generated game. Read ../START_WEB.md, STAGES.md and STATUS.json.'+
  '\nSource book files stay private; avoid adding copyrighted originals to public git.\n');
 return {dest,stages:stages.length,status:'NEW_UNVERIFIED_RUN'};
}
if(process.argv[1]&&path.resolve(process.argv[1])===url.fileURLToPath(import.meta.url)){
 try{
  const [slug,title]=process.argv.slice(2);
  if(!slug||!title)throw Error('Usage: node tools/new_book_run.mjs book-slug "书籍标题"');
  console.log(JSON.stringify(createRun(slug,title),null,2));
 }catch(e){console.error(e.message);process.exitCode=1}
}