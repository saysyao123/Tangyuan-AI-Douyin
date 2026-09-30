"""Public same-track source acquisition for a labeled validation branch."""
import urllib.request,re,html,json,hashlib,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
URL='https://xiangxiang.bandcamp.com/track/-'
page=urllib.request.urlopen(URL,timeout=30).read().decode()
data=json.loads(html.unescape(re.search(r'data-tralbum="([^"]+)"',page).group(1)))
track=data['trackinfo'][0]
assert track['id']==985094992 and track['title']=='一个人在家'
audio=urllib.request.urlopen(track['file']['mp3-128'],timeout=60).read()
assert hashlib.sha256(audio[:1500000]).hexdigest()=='68760594212b2e55e25da334c543a0420a7cefc75709714a71ee1884d0db3ab6'
(R/'validation_full.mp3').write_bytes(audio)
lyrics=track.get('lyrics') or data.get('current',{}).get('lyrics') or ''
(R/'trusted_lyrics_private.txt').write_text(lyrics)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,bit_rate:stream=sample_rate,channels,codec_name','-of','json',str(R/'validation_full.mp3')]))
meta={'song_family':track['title'],'artist':'想想XiangXiang','source_url':URL,'track_id':track['id'],'coverage':'FULL_SOURCE_ACQUIRED','catalog_duration_seconds':track['duration'],'bytes':len(audio),'sha256':hashlib.sha256(audio).hexdigest(),'matches_previous_reference_prefix':True,'probe':probe,'purpose':'SUPPLEMENTAL_TEST_VALIDATION_ONLY_NOT_PRODUCTION_SELECTION','lyric_chars':len(re.sub(r'\s+','',lyrics)),'lyric_text_sha256':hashlib.sha256(lyrics.encode()).hexdigest(),'release_note':'2024-09-23 public artist publication verified earlier; not represented as a 2026 first release.'}
(R/'full_source_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
print(json.dumps(meta,ensure_ascii=False))
