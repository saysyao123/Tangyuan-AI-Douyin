from pathlib import Path
import json,shutil,sys,hashlib,subprocess
# Usage: update-r2-site.py TESTED_RUNTIME RUNTIME_SHA SITE_DIST
base=Path(sys.argv[3]); runtime=Path(sys.argv[1]); sha=sys.argv[2]; review=base/'review'; evidence=runtime/'t32-evidence'; r=evidence/'portraits/chromium'
# Runtime is the exact successfully tested GitHub candidate, not a second local rebuild.
shutil.rmtree(base/'chapter/game');shutil.copytree(runtime/'chapter/game',base/'chapter/game')
for role in ['hero','child','merchant','neighbor','stranger','officer']:shutil.copy2(r/('portrait-'+role+'.png'),review/('portrait-'+role+'.png'))
shutil.copy2(evidence/'portraits/webkit/backstage-entry.png',review/'backstage.png')
for engine in ['chromium','firefox','webkit']:shutil.copy2(evidence/('portraits/'+engine+'/result.json'),review/('portraits-'+engine+'-qa.json'))
shutil.copy2(evidence/'story/result.json',review/'backstage-qa.json')
video=next((evidence/'story').glob('*.webm'))
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(video),'-vf','scale=1280:-2','-an','-c:v','libx264','-crf','23','-movflags','+faststart',str(review/'backstage.mp4')],check=True)
q=json.loads((review/'QA.json').read_text());q['runtimeGitHubCommit']=sha;q['sourceCommit']='7826619a61d978c73c7a26d0288d9c335c371953';q['r2AffectedScope']={'runs':{'chromium':39093310372,'firefox':39093310372,'webkit':39093766720},'engines':['Chromium','Firefox','WebKit'],'portraitsAuthored':8,'actualSpeakingIdentitiesTested':6,'nativePortraitSource':'256x288','logicalPortraitRect':'64x72','checksPerEngine':5,'scope':'actual vendor/leads/guard/stranger/neighbor dialogue and revised backstage; prior complete fresh story reused'};q['finalAffectedBackstage']={'run':39093766720,'status':'PASS','checks':2};q['limits']=[x for x in q['limits'] if 'portrait' not in x.lower() and 'phone' not in x.lower()];q['limits'].append('Three headless browser engines tested; WebKit uses a normal persistent session. Private WebKit IDB Blob storage remains unsupported; no physical phone or Safari application test.');q['screenEvidence']={'backstage':'Current R2 WebKit same-entry capture (normal persistent context)','portraitDialogue':'Current R2 actual native dialogue screenshots','fairStreetCourtyard':'Previous accepted internal captures reused; world assets and projection unchanged','walkingStageMedicine':'Previous actual playthrough captures reused; corresponding behavior unchanged'};q['artGate']='Internal review of revised portraits and backstage completed; final user acceptance pending';(review/'QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
old='e4e667dee5c24647c4125c8864e52a39dec91415'
for f in [review/'index.html',base/'help.html']:
 s=f.read_text().replace(old,sha)
 if f.parent==review:
  s=s.replace('<section><h2>验收边界</h2>', '<section><h2>对白人物 · 本轮实际运行</h2><p>头像保持原对白框大小，与世界人物的发型、冬装和身份一致。以下六张均出自实际对白。</p><div class="pair">'+''.join('<figure><img loading="lazy" src="portrait-'+role+'.png"><figcaption>'+label+'</figcaption></figure>' for role,label in [('hero','主角'),('child','孩子'),('merchant','摊主'),('officer','看守'),('stranger','问路青年'),('neighbor','邻居')])+'</div><p>新增头像与后台的定向验证：<a href="portraits-chromium-qa.json">Chromium</a> · <a href="portraits-firefox-qa.json">Firefox</a> · <a href="portraits-webkit-qa.json">WebKit</a>。WebKit 使用正常持久会话；引擎测试不等同真实 Safari 或手机测试，隐私会话的存档限制仍存在。</p></section><section><h2>验收边界</h2>')
  s=s.replace('后台最后一轮仅修改画面墙体投影，另外进行了倒地、抬走和读档的定向复测。','本轮统一对白头像、补齐后台门窗梁柱并移除室内箱子积雪，定向验证真实对白、倒地、抬走和读档。')
 f.write_text(s)
# The two large archives remain external to avoid the hosting Git object limit.
downloads=json.loads((base/'download-checksums.json').read_text())
for d in downloads:
 if d.get('external'):d['url']=d['url'].replace(old,sha)
(base/'download-checksums.json').write_text(json.dumps(downloads,indent=2)+'\n')
(base/'PLAY_README.txt').write_text('雾灯驿站 · 第一幕 T32 R2 美术验收版\n在线试玩：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/\n实机画面与记录：review/index.html\n本地请通过 HTTP 服务打开 chapter/，避免 file:// 的资源限制。可使用现有 PLAY_WINDOWS.cmd；此脚本未在真实 Windows 机器复测。\n原生 SAVE12、剧情、地图与碰撞保持。新增统一头像与后台门窗、室内道具。最终用户审美尚待验收。\n合成示例对白，不含原书私有文本。WebKit 需正常会话存档，隐私会话存在数据库 Blob 限制。\n对应源码：https://github.com/saysyao123/Tangyuan-AI-Douyin/raw/'+sha+'/downloads/corresponding-source.zip\n')
excluded={'runtime-manifest.json','download-checksums.json'}
files={p.relative_to(base).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*')) if p.is_file() and p.relative_to(base).parts[0]!='downloads' and p.relative_to(base).as_posix() not in excluded}
(base/'runtime-manifest.json').write_text(json.dumps({'version':1,'files':files},indent=2)+'\n')
print('UPDATED_SITE_FROM_TESTED_RUNTIME',sha,len(files))
