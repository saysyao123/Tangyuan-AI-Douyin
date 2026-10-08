#!/usr/bin/env python3
"""Distinctly WATERMARKED synthetic image fixtures for Chrome/Canvas ENGINE QA ONLY.
Never use this output to pass GPT-asset production gates. Does not use old user imagery.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parents[1]
DEST=ROOT/'08_AGENT_CONTROL_LAYER/pilots/CODE_MOTION_MV_RUN01_2026-10-06/engine/assets/gpt'
DEST.mkdir(parents=True,exist_ok=True)
W,H=941,1672
names=['L01_clean.png','L04_hero.png','L07_clean.png','L08_hero.png']
for n,name in enumerate(names):
    im=Image.new('RGB',(W,H))
    px=im.load()
    for y in range(H):
        r=round(18+19*y/H)+n*2;g=round(33+12*y/H)+n*3;b=round(57+22*y/H)+n*4
        for x in range(W):px[x,y]=(r,g,b)
    d=ImageDraw.Draw(im)
    for x in range(-300,1300,140):
        d.line((x,200,x+450,1420),fill=(47,67,93),width=3)
    d.rectangle((40,700,900,1060),fill=(9,17,31),outline=(220,98,80),width=7)
    d.text((74,758),name,fill=(240,230,214),font=ImageFont.load_default())
    d.text((74,809),'SYNTHETIC ENGINE FIXTURE',fill=(255,177,156),font=ImageFont.load_default())
    d.text((74,864),'NOT A GPT IMAGE | NOT ART APPROVED',fill=(255,177,156),font=ImageFont.load_default())
    im.save(DEST/name,optimize=True)
photo=Image.new('RGBA',(145,169),(208,188,161,230))
d=ImageDraw.Draw(photo);d.rectangle((5,5,140,164),outline=(93,60,52,255),width=5)
d.text((15,72),'FIXTURE',fill=(80,51,51,255),font=ImageFont.load_default())
photo.save(DEST/'L07_photo.png',optimize=True)
(DEST/'.SYNTHETIC_FIXTURE_ONLY').write_text('Synthetic QA input only, not real GPT art.\n',encoding='utf-8')
print('SYNTHETIC_ENGINE_FIXTURE_CREATED',DEST,flush=True)
