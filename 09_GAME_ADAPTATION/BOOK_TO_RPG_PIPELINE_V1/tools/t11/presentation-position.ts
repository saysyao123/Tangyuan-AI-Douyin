import type {GridPos} from '@type-pal/content'
/** Display-only interpolation. Never writes gameplay position, collisions or save payloads. */
export class PresentationPosition {
 private scene='';private target:GridPos|null=null;private from:GridPos|null=null;private began=0
 constructor(private readonly duration=80){}
 sample(scene:string,pos:GridPos,now:number,enabled=true):{pos:GridPos;moving:boolean}{
  const copy=()=>({...pos})
  if(!enabled||scene!==this.scene||!this.target||!this.from||Math.abs(pos.col-this.target.col)+Math.abs(pos.row-this.target.row)>1.01||pos.height!==this.target.height){this.scene=scene;this.target=copy();this.from=copy();this.began=now;return {pos:copy(),moving:false}}
  const current=()=>{const t=Math.max(0,Math.min(1,(now-this.began)/this.duration));const a=this.from!,b=this.target!;return {col:a.col+(b.col-a.col)*t,row:a.row+(b.row-a.row)*t,height:b.height}}
  if(pos.col!==this.target.col||pos.row!==this.target.row){this.from=current();this.target=copy();this.began=now}
  const visual=current();return {pos:visual,moving:Math.abs(visual.col-pos.col)+Math.abs(visual.row-pos.row)>.001}
 }
}
