"""Check all authored interaction-side routes, not only the browser's chosen path."""
from pathlib import Path
import json,sys
root=Path(sys.argv[1]);count=0;routes=0
for scene_id,ids in [('fair',['vendor','stage']),('street',['stranger']),('courtyard',['neighbor'])]:
 s=json.loads((root/'content/scenes'/f'{scene_id}.json').read_text());entities={e['id']:e for e in s['entities']};blocked={(e['pos']['col'],e['pos']['row']) for e in s['entities'] if e.get('collide') and not e.get('hidden')}
 for entity_id in ids:
  body=entities[entity_id]['behaviors']['trigger']['main']['flow']['stages'][0]['body'];node=body[1]
  while node.get('cond',{}).get('kind')=='entitiesNear':
   zone=entities[node['cond']['to']['entity']];at=(zone['pos']['col'],zone['pos']['row'])
   for cmd in node['then']:
    assert cmd['kind']=='moveParty';end=(cmd['to']['col'],cmd['to']['row']);assert abs(end[0]-at[0])+abs(end[1]-at[1])==1,(scene_id,entity_id,at,end);assert end not in blocked,(scene_id,entity_id,'crosses actor',end);at=end;count+=1
   routes+=1;node=node['else'][0] if node['else'] else {}
print(json.dumps({'status':'PASS','interactionSideRoutes':routes,'unitSegments':count,'claim':'Every compiled local approach is axis-aligned and avoids all colliding actor feet'}))
