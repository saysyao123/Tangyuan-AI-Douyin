/** Original-source-independent 2048 rule implementation (x-major board). */
export function step2048(input,direction,random=Math.random){
 const n=input.cells.length;
 if(!Number.isInteger(direction)||direction<0||direction>3)throw new RangeError("direction 0..3");
 const cells=input.cells.map(c=>[...c]);
 if(!n||cells.some(c=>c.length!==n))throw new TypeError("square board needed");
 const r={cells,score:input.score??0,over:!!input.over,won:!!input.won,keepPlaying:!!input.keepPlaying};
 if(r.over||(r.won&&!r.keepPlaying))return r;
 let changed=false;
 for(let line=0;line<n;line++){
  const coords=[];
  for(let t=0;t<n;t++){
   if(direction===0)coords.push([line,t]);
   if(direction===1)coords.push([n-1-t,line]);
   if(direction===2)coords.push([line,n-1-t]);
   if(direction===3)coords.push([t,line]);
  }
  const a=coords.map(([x,y])=>cells[x][y]).filter(Boolean),out=[];
  for(let i=0;i<a.length;i++){
   if(i+1<a.length&&a[i]===a[i+1]){
    const v=a[i]*2;out.push(v);r.score+=v;if(v===2048)r.won=true;i++;
   }else out.push(a[i]);
  }
  for(let i=0;i<n;i++){
   const [x,y]=coords[i],v=out[i]??0;
   if(cells[x][y]!==v)changed=true;
   cells[x][y]=v;
  }
 }
 if(!changed)return r;
 const empty=[];
 for(let x=0;x<n;x++)for(let y=0;y<n;y++)if(!cells[x][y])empty.push([x,y]);
 if(empty.length){
  const v=random()<0.9?2:4;
  const [x,y]=empty[Math.floor(random()*empty.length)];
  cells[x][y]=v;
 }
 let avail=false;
 for(let x=0;x<n;x++)for(let y=0;y<n;y++){
  const v=cells[x][y];
  if(!v||(x+1<n&&cells[x+1][y]===v)||(y+1<n&&cells[x][y+1]===v))avail=true;
 }
 r.over=!avail;
 return r;
}
