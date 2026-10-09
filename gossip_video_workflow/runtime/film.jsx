import React from 'react';
import {createRoot} from 'react-dom/client';
import {flushSync} from 'react-dom';
import gsap from 'gsap';
import timeline from './timeline.json';
const rows=timeline.rows;
function Highlight({text,quote}) {const i=quote?text.indexOf(quote):-1;return i<0?text:<>{text.slice(0,i)}<mark>{quote}</mark>{text.slice(i+quote.length)}</>;}
function Media({row}) {
 if(row.type==='cover') return row.cover?.length?<div className="cover-grid">{row.cover.map((v,i)=><React.Fragment key={i}><img className={['wang','liu','couple'][i]} src={v.file}/><div className={'cover-label '+['wang-label','liu-label','couple-label'][i]}>{v.label}</div></React.Fragment>)}</div>:<div className="end-ledger"><p className="big-question">{row.note||'云端流程检查'}</p><p className="ledger-row">技术样片 · 非新闻成片</p></div>;
 if(row.type==='end') return <div className="end-ledger"><p className="big-question">{row.question||'评论区，\n聊聊你的看法。'}</p>{(row.items||[]).map(v=><p className="ledger-row" key={v}>{v}</p>)}</div>;
 if(row.type==='tweet')return <div className="tweet-stage"><div className="tweet-author">{row.tweet.author}</div><div className="tweet-original"><Highlight text={row.tweet.original} quote={row.tweet.highlight}/></div><div className="translation">{row.tweet.translation}</div><div className="tweet-link">{row.tweet.url}</div></div>;
 if(row.type==='image')return <div className="screenshot-stage"><img src={row.image}/><div className="translation">{row.note}</div></div>;
 return <img className={'footage '+(row.fit==='cover'?'people':'landscape')} data-media={row.id} src={`frames/${row.id}/0001.jpg`}/>;
}
function Film(){return <main className="zh">{rows.map((row,index)=><section key={row.id} className={'shot '+(row.type==='cover'?'cover':'')} data-shot={row.id}>
 <div className="topbar"><span>{timeline.label}</span><span>{timeline.edition}</span></div>
 <div className="chapter">{row.chapter}{row.kind==='claim'?' / 未证实':''}</div><h1>{row.headline}</h1><div className="accent-rule" data-rule={row.id}/>
 <div className="media-well"><Media row={row}/></div>
 {row.note&&row.type==='video'&&<div className="note">{row.note}</div>}
 <div className="source"><div>{row.factSource}</div><div>{row.screenSource}</div></div>
 <div className="caption"><p>{row.text}</p></div>
 <div className="footer"><span>{timeline.footer||'有来源，再聊看法'}</span><span>{String(index+1).padStart(2,'0')} / {rows.length}</span></div><div className="progress"/>
 </section>)}</main>}
flushSync(()=>createRoot(document.getElementById('film-root')).render(<Film/>));
gsap.ticker.sleep();const master=gsap.timeline({paused:true});
for(const row of rows)if(row.type!=='cover')master.fromTo(`[data-rule="${row.id}"]`,{scaleX:0},{scaleX:1,duration:.28,ease:'power2.out'},row.start+.1);
const nodes=[...document.querySelectorAll('.shot')];let current=-1;
window.seek=async seconds=>{
 const t=Math.min(Math.max(Number(seconds)||0,0),timeline.duration-1/timeline.fps);
 const index=rows.findIndex(r=>r.start<=t&&r.end>t);const row=rows[index<0?rows.length-1:index];const selected=rows.indexOf(row);
 if(current!==selected){nodes.forEach((n,i)=>n.style.display=i===selected?'block':'none');current=selected;}
 const img=document.querySelector(`img[data-media="${row.id}"]`);
 if(img){const frame=Math.min(row.frames,1+Math.floor((t-row.start)/(row.end-row.start)*row.frames));const src=`frames/${row.id}/${String(frame).padStart(4,'0')}.jpg`;if(img.getAttribute('src')!==src){img.src=src;await img.decode();}}
 master.seek(t,true);nodes[selected].querySelector('.progress').style.transform=`scaleX(${Math.max(.01,t/timeline.duration)})`;
};
window.__filmReady=(async()=>{
 nodes.forEach(n=>n.style.display='block');await document.fonts.load('500 56px NewsMedium');await document.fonts.load('300 96px NewsLight');await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));
 const fitting=[];
 for(const n of nodes){const p=n.querySelector('.caption p');let size=56;p.style.fontSize=size+'px';while(p.scrollHeight>size*1.43*3+3&&size>40){size--;p.style.fontSize=size+'px';}fitting.push({id:n.dataset.shot,fontSize:size,lines:Math.round(p.scrollHeight/(size*1.43)),overflow:p.scrollWidth>p.clientWidth||p.scrollHeight>size*1.43*3+3});n.style.display='none';}
 window.CAPTION_QA=fitting;await window.seek(0);
})();
