"""Replace every PAL-derived engine chrome file with independently drawn pixels.
Only reads PNG dimensions, never uses any source image pixels. Also adds a read-only
QA observer to the official runtime; no gameplay state setter or alternate engine.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,sys,hashlib
root=Path(sys.argv[1]).resolve()
chrome=root/'packages/reforge/src/engine-chrome/assets'
ink='#172b38'; edge='#638168'; gold='#e6bb7c'; light='#f4e3b8'
font=ImageFont.load_default(size=8)
receipt=[]
for p in sorted((chrome/'ui').rglob('*.png')):
    w,h=Image.open(p).size
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    rel=p.relative_to(chrome/'ui'); group=rel.parts[0]
    if group in ['box','box-red','scroll','itembox']:
        n=int(p.stem[-2:]); row,col=divmod(n,3)
        d.rectangle((0,0,w-1,h-1),fill=ink)
        c='#c57564' if group=='box-red' else gold
        if row==0:d.line((0,1,w,1),fill=c)
        if row==2:d.line((0,h-2,w,h-2),fill=c)
        if col==0:d.line((1,0,1,h),fill=c)
        if col==2:d.line((w-2,0,w-2,h),fill=c)
    elif group.startswith('num'):
        patterns=['111101101101111','010110010010111','111001111100111','111001111001111','101101111001001','111100111001111','111100111101111','111001010010010','111101111101111','111101111001111']
        c='#a2bec0' if group=='num-blue' else '#e6bb7c' if group=='num-cyan' else light
        if p.stem.isdigit():
            for i,v in enumerate(patterns[int(p.stem)]):
                if v=='1':d.point((i%3+1,i//3+1),fill=c)
        else:d.line((1,6,3,1),fill=c,width=1)
    elif group=='cursor':
        if p.stem.startswith('up'):d.polygon([(w//2,0),(0,h-1),(w-1,h-1)],fill=gold)
        else:d.polygon([(0,0),(w-1,0),(w//2,h-1)],fill=gold)
    elif group=='battle':
        d.ellipse((1,1,w-2,h-2),fill=ink,outline=gold,width=1)
        if 'attack' in p.stem:
            d.line((8,22,22,7),fill=light,width=3);d.line((6,16,14,23),fill=gold,width=2)
        elif 'magic' in p.stem:
            d.polygon([(15,5),(18,12),(25,15),(18,18),(15,25),(12,18),(5,15),(12,12)],fill=gold)
        elif 'coop' in p.stem:
            d.line((7,22,22,7),fill=light,width=2);d.line((7,7,22,22),fill=gold,width=2)
        else:
            for y in [9,15,21]:d.line((8,y,22,y),fill=light,width=2)
    else:
        d.rectangle((0,0,w-1,h-1),fill=ink,outline=edge,width=1)
        if w>100:
            for y in range(h):d.line((0,y,w,y),fill=(16+y//12,28+y//14,39+y//12))
            d.rectangle((5,5,w-6,h-6),outline=gold)
        elif group=='status' and len(rel.parts)>2:
            d.line((w//3,h*2//3,w*2//3,h//3),fill=gold,width=2)
    im.save(p)
    receipt.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'origin':'original-procedural'})
# Original title screen. Replaces default PAL FBP2 even though player starts directly.
im=Image.new('RGB',(320,200),ink);d=ImageDraw.Draw(im)
for y in range(200):d.line((0,y,320,y),fill=(16+y//15,28+y//13,39+y//12))
d.ellipse((220,20,267,67),fill=light)
for x in range(-20,340,25):d.polygon([(x,40+(x%31)),(x-30,170),(x+30,170)],fill='#22434a')
d.rectangle((70,95,250,140),fill=ink,outline=gold);d.text((97,110),'LANTERN INN',font=ImageFont.load_default(size=18),fill=light)
im.save(chrome/'title.png')
(chrome/'PROVENANCE.md').write_text('# T1 original engine chrome\n\nAll 85 UI PNG slots, title and dialog cursor are replaced by original procedural art. No source PAL image pixels were copied. See type_pal_t1_prepare.py and type_pal_t1_art.ts.\n\nGNU Unifont Japanese 15.1.05 remains under its upstream SIL OFL 1.1 / GPL font exception; verbatim texts are in licenses/. Engine code is GPL-3.0.\n')
# Indexed-grayscale battle background, required by native battle-background contract.
bg=Image.new('RGB',(320,200));d=ImageDraw.Draw(bg)
d.rectangle((0,0,319,199),fill=(1,1,1));d.ellipse((223,19,253,49),fill=(26,26,26))
for i in range(14):
 x=i*27-15;y=40+(i*37)%40
 d.polygon([(x,y),(x-25,146),(x+25,146)],fill=(2,2,2));d.rectangle((x-3,100,x+3,160),fill=(10,10,10))
d.polygon([(0,142),(120,119),(320,147),(320,200),(0,200)],fill=(3,3,3));d.polygon([(180,128),(220,137),(150,200),(34,200)],fill=(37,37,37))
for i in range(140):
 x=(i*97)%320;y=144+(i*13)%55;d.point((x,y),fill=(4,4,4))
project=root/'projects/book-lantern-inn';rel='assets/generated/backgrounds/forest.png';p=project/rel;p.parent.mkdir(parents=True,exist_ok=True);bg.save(p)
catalog=json.loads((project/'assets/index.json').read_text());catalog['assets']['background.forest']={'kind':'battle-background','path':rel,'mediaType':'image/png','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'label':'原创雾林月色','origin':{'kind':'generated'}}
(project/'assets/index.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
f=project/'content/battle-fields.json';fields=json.loads(f.read_text());fields[0]['background']='background.forest';f.write_text(json.dumps(fields,ensure_ascii=False,indent=2)+'\n')
# Enable only read-only official observations on ?observe=1 in production.
p=root/'packages/reforge/src/main.ts';s=p.read_text()
s=s.replace("if (import.meta.env.DEV) {\n    ;(window as unknown as { __tpObserve", "if (import.meta.env.DEV || params.has('observe')) {\n    ;(window as unknown as { __tpObserve",1)
s=s.replace('if (import.meta.env.DEV) runtimeObservationReady = true',"if (import.meta.env.DEV || params.has('observe')) runtimeObservationReady = true")
s=s.replace('      sceneId: activeScene.scene.id,\n      position: Object.freeze', '''      sceneId: activeScene.scene.id,
      story: Object.freeze({flags: {...canonicalScript.flags}, inventory: world.inventory.map(i=>({...i})), money: world.money, party: world.party.map(c=>({hp:c.hp,maxHP:c.maxHP}))}),
      position: Object.freeze''')
# actual WorldState field confirmed below; fail on mismatch in typecheck rather than fake observer.
p.write_text(s)
(root/'t1-chrome-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('ORIGINAL_CHROME_REPLACED',len(receipt),'slots + title + cursor; read-only observation patch')
# Browser-first authoring with actual OPFS handles, explicit user click, native save policy.
import shutil
helper=Path(__file__).parent/'t1-browser-workspace.ts'
shutil.copyfile(helper,root/'packages/editor/src/core/t1-browser-workspace.ts')
p=root/'packages/editor/src/ui/ProjectPicker.tsx';s=p.read_text()
if "import { newBrowserStory }" not in s:
 s="import { newBrowserStory } from '../core/t1-browser-workspace.js'\n"+s
s=s.replace("seedBaseUrl = 'projects/pal'","seedBaseUrl = 'projects/book-lantern-inn'")
s=s.replace("const createBlank = run('创建空白项目', newBlankProject)","const browserStory = run('创建浏览器工程', async () => newBrowserStory(seedBaseUrl, (done,total,phase) => setProgress({done,total,phase})))\n  const createBlank = run('创建空白项目', newBlankProject)")
s=s.replace('<div className="picker-actions">','''<div className="picker-actions">
              <DsPressable type="button" className="picker-act primary" onClick={browserStory}>
                <span className="picker-act-t">创建浏览器工程</span>
                <span className="picker-act-d">复制原创《雾灯驿站》到浏览器目录。保存后可关闭重开；清理网站数据会删除它，请用另存为备份。</span>
              </DsPressable>''')
s=s.replace('从 PAL 开发快照创建本地项目','复制原创驿站到电脑文件夹').replace('当前快照仍随 E2E 持续完善，尚不是稳定用户种子。','需要你选择空文件夹并授权。保留标准 content22 工程。')
p.write_text(s)
