/* Independent minimal story-game kernel. NOT the full PAL98 battle formula. */
export const GameRules = (() => {
  const copy = value => JSON.parse(JSON.stringify(value));
  const scene = (game,id) => game.world.scenes.find(x => x.id === id);
  const inside = (s,x,y) => y >= 0 && y < s.terrain.length && x >= 0 && x < s.terrain[0].length && s.terrain[y][x] !== '#';
  const entities = (s,x,y) => s.entities.filter(e => e.x===x && e.y===y);
  const dirmap = {up:[0,-1],down:[0,1],left:[-1,0],right:[1,0]};
  const put = (s,t) => {s.message=t; s.history.push(t); s.history=s.history.slice(-20)};
  function initial(game){
    const result={version:1,gameId:game.id,sceneId:game.world.startScene,
      x:game.player.position[0],y:game.player.position[1], hp:game.player.maxHp,
      mp:game.player.maxMp,gold:0,experience:0,flags:{},inventory:{},cleared:{},
      battle:null,ending:null,message:'探索地图，靠近人物按 E 对话或调查。',history:[]};
    return result;
  }
  function met(s,req=[]){return req.every(r => r.type==='flag' ? !!s.flags[r.target]===!!r.value
    :r.type==='has_item'? (s.inventory[r.target]||0)>=r.value:false);}
  function doEffects(g,s,effects=[]){
    for(const e of effects){
      switch(e.type){
        case 'set_flag':s.flags[e.target]=e.value;break;
        case 'give_item':s.inventory[e.target]=(s.inventory[e.target]||0)+(e.value||1);break;
        case 'set_ending':s.ending=e.target;break;
        case 'give_gold':s.gold+=(e.value||0);break;
        default:throw Error('Unknown effect '+e.type);
      }
    }
  }
  function trigger(g,s,eventId){
    const e=g.events.find(x=>x.id===eventId);
    if(!e){put(s,'缺失事件：'+eventId);return;}
    if(!met(s,e.requires)){put(s,e.failureText||'条件尚未满足。');return}
    doEffects(g,s,e.effects);
    put(s,e.text);
    if(s.ending)put(s,'结局：'+g.ending.title);
  }
  function resolveWin(g,s){
    let def=g.encounters.find(e=>e.id===s.battle.id);
    s.flags[def.winFlag]=true;s.cleared[s.battle.source]=true;
    s.gold+=def.rewardGold;s.experience+=def.rewardExp;
    s.battle=null;put(s,'战斗胜利！获得经验 '+def.rewardExp+'、银钱 '+def.rewardGold+'。');
  }
  function act(game,state,action){
    const s=copy(state),a=typeof action==='string'?{type:action}:action;
    if(s.ending){if(a.type!=='RESET')return s;return initial(game)}
    if(s.battle){
      const enemy=game.encounters.find(e=>e.id===s.battle.id);
      if(a.type==='FLEE'){s.battle=null;put(s,'你从战斗中撤退，雾狼仍留在原地。');return s}
      if(!['ATTACK','MAGIC','DEFEND'].includes(a.type))return s;
      const cost=a.type==='MAGIC'?3:0;
      if(s.mp<cost){put(s,'灵力不足！');return s}
      s.mp-=cost;
      const damage=a.type==='ATTACK'?Math.max(1,game.player.attack-enemy.defense)
        :a.type==='MAGIC'?Math.max(1,game.player.attack+3-enemy.defense):0;
      s.battle.enemyHp=Math.max(0,s.battle.enemyHp-damage);
      if(!s.battle.enemyHp){resolveWin(game,s);return s}
      const harm=Math.max(1,enemy.attack-game.player.defense-(a.type==='DEFEND'?3:0));
      s.hp=Math.max(0,s.hp-harm);
      put(s,(a.type==='DEFEND'?'你采取防御姿态。':'你造成 '+damage+' 点伤害。')+' '+enemy.name+'反击造成 '+harm+' 点伤害。');
      if(s.hp===0){s.hp=game.player.maxHp;s.mp=game.player.maxMp;s.battle=null;s.sceneId=game.world.startScene;s.x=game.player.position[0];s.y=game.player.position[1];put(s,'力竭后被送回驿站，恢复了状态。')}
      return s;
    }
    const current=scene(game,s.sceneId);
    if(a.type==='MOVE'){
      const vec=dirmap[a.direction];if(!vec)return s;
      const x=s.x+vec[0],y=s.y+vec[1];
      if(!inside(current,x,y))return s;
      const obj=entities(current,x,y).find(e=>e.kind==='enemy'&&!s.cleared[e.id]);
      if(obj){const def=game.encounters.find(e=>e.id===obj.encounterId);
        s.battle={id:def.id,source:obj.id,enemyHp:def.hp};put(s,'遭遇 '+def.name+'！');return s;
      }
      if(entities(current,x,y).some(e=>e.kind==='npc'||e.kind==='item'))return s;
      s.x=x;s.y=y;
      const exit=current.exits.find(e=>e.x===x&&e.y===y);
      if(exit){s.sceneId=exit.to;s.x=exit.spawn[0];s.y=exit.spawn[1];put(s,'进入：'+scene(game,s.sceneId).name)}
      return s;
    }
    if(a.type==='INTERACT'){
      const near=current.entities.filter(e=>Math.abs(e.x-s.x)+Math.abs(e.y-s.y)<=1);
      const obj=near.find(e=>e.kind==='item'&&!s.cleared[e.id])||near.find(e=>e.kind==='npc');
      if(!obj){put(s,'附近没有可以调查的对象。');return s}
      if(obj.kind==='item'){s.cleared[obj.id]=true;s.inventory[obj.itemId]=(s.inventory[obj.itemId]||0)+1;put(s,'取得：'+game.items.find(i=>i.id===obj.itemId).name);return s}
      const eventId=obj.completionFlag&&s.flags[obj.completionFlag]?obj.completedEventId:obj.eventId;
      trigger(game,s,eventId);return s;
    }
    if(a.type==='RESET')return initial(game);
    return s;
  }
  function snapshot(g,s){if(s.gameId!==g.id)throw Error('wrong game');return JSON.stringify(s)}
  function restore(g,save){const s=JSON.parse(save);
    if(s.gameId!==g.id||s.version!==1||!scene(g,s.sceneId)||!Number.isInteger(s.x)||!Number.isInteger(s.y)||!inside(scene(g,s.sceneId),s.x,s.y))throw Error('invalid save');
    if(typeof s.flags!=='object'||typeof s.inventory!=='object'||typeof s.cleared!=='object')throw Error('invalid save state');
    return s;
  }
  return {initial,act,snapshot,restore};
})();