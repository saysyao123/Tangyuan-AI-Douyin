/** Small authored-story shortcut over the official ScriptEditSession and native save. */
import {useState,useRef} from 'react'
import {type ScriptEditSession,UpdateEntityBehaviorCommand} from '../core/script-editor.js'
export function T1WelcomeEditor({session,onSave,onPlay}:{session:ScriptEditSession;onSave:()=>Promise<unknown>;onPlay:()=>void}){
 const saving=useRef(false);const [busy,setBusy]=useState(false)
 const [open,setOpen]=useState(false),[text,setText]=useState(''),[status,setStatus]=useState('')
 const behavior=()=>session.getState().scenes.find(s=>s.id==='inn')?.entities.find(e=>e.id==='keeper')?.behaviors?.trigger?.main
 function row(flow:any){return flow.stages[0].body[1].else[0].else[0].else[0].cue.rows[0]}
 function edit(){try{const b=behavior();if(!b)throw Error('未找到守灯人');setText(row(b.flow).text);setStatus('');setOpen(true)}catch{setStatus('剧情结构已改变，请使用完整剧本编辑器。');setOpen(true)}}
 async function apply(){if(saving.current)return;saving.current=true;setBusy(true);try{const b=behavior();if(!b||!text.trim())throw Error('对白不能为空');const flow=structuredClone(b.flow);row(flow).text=text;session.dispatch(new UpdateEntityBehaviorCommand({scene:'inn',entity:'keeper'},'trigger','main',{flow}));await onSave();setStatus(session.isDirty()?'保存尚未完成，请查看编辑器的错误提示。':'已保存，可以试玩。')}catch(e){setStatus(String(e))}finally{saving.current=false;setBusy(false)}}
 return <div style={{position:'fixed',right:18,bottom:18,zIndex:9000,fontFamily:'sans-serif'}}>
  <button type="button" onClick={edit} style={{background:'#172b38',color:'#e6bb7c',border:'1px solid #638168',padding:'10px 16px',borderRadius:6}}>守灯人对白</button>
  {open?<section role="dialog" aria-label="编辑守灯人对白" style={{position:'fixed',inset:'20% auto auto 50%',transform:'translateX(-50%)',width:'min(580px,90vw)',padding:24,background:'#172b38',color:'#f4e3b8',border:'1px solid #638168',borderRadius:8,boxShadow:'0 20px 100px #000b'}}>
   <h2 style={{fontSize:18,margin:'0 0 10px'}}>守灯人 · 初次见面</h2><p style={{fontSize:12,color:'#a2bec0'}}>修改第一次见面时的台词，保存后可在试玩中查看。</p>
   <textarea aria-label="守灯人初次对白" value={text} onChange={e=>setText(e.target.value)} disabled={busy} rows={5} style={{width:'100%',boxSizing:'border-box',padding:12,fontSize:15,background:'#101c27',color:'#f4e3b8',border:'1px solid #638168',borderRadius:4}}/>
   <div style={{display:'flex',gap:12,marginTop:12}}><button type="button" disabled={busy} onClick={()=>void apply()}>{busy?'正在保存…':'应用对白并保存'}</button><button type="button" disabled={busy} onClick={onPlay}>试玩保存后的故事</button><button type="button" onClick={()=>setOpen(false)}>关闭</button></div><p role="status" style={{fontSize:12}}>{status}</p>
  </section>:null}
 </div>
}
