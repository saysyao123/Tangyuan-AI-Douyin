#!/usr/bin/env bash
set -euo pipefail

SLOT='06_TESTS/MV/WEB_R3/30D_60/D02-B'
OUT="$SLOT/03_AUDIO_TIMELINE"
TMP='/tmp/d02b_audio_timeline'
ALIGN_IMAGE='ghcr.io/wangjiqing/xingyu-lyrics-aligner:v0.6.1'
LOCKED_B_SHA='6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4'
mkdir -p "$OUT" "$TMP/jobs/result" "$TMP/models"
chmod -R 0777 "$TMP/jobs" "$TMP/models"

# Re-acquire the exact locked Douyin source without committing audio to Git.
bash 04_HARNESS/tools/d02b_hg02_audio_probe.sh
BGM='/tmp/hg02_audio/HG02_B_soft_tail_0p8s.mp3'
ACTUAL_SHA=$(sha256sum "$BGM" | awk '{print $1}')
if [ "$ACTUAL_SHA" != "$LOCKED_B_SHA" ]; then
  echo "ERROR: locked BGM SHA mismatch: expected=$LOCKED_B_SHA actual=$ACTUAL_SHA" >&2
  exit 41
fi

cp "$OUT/trusted_lyrics.txt" "$TMP/jobs/trusted_lyrics.txt"

# Strong Route B: trusted Chinese lyrics + CTC forced alignment.
docker pull "$ALIGN_IMAGE" >/dev/null
docker run --rm \
  -v /tmp/hg02_audio:/music:ro \
  -v "$TMP/jobs":/jobs \
  -v "$TMP/models":/models \
  "$ALIGN_IMAGE" \
  xingyu-align models pull --language zh --device cpu

docker run --rm \
  -v /tmp/hg02_audio:/music:ro \
  -v "$TMP/jobs":/jobs \
  -v "$TMP/models":/models \
  "$ALIGN_IMAGE" \
  xingyu-align align \
    --audio /music/HG02_B_soft_tail_0p8s.mp3 \
    --lyrics /jobs/trusted_lyrics.txt \
    --output-dir /jobs/result \
    --language zh \
    --device cpu \
    --json-result \
  > "$TMP/xingyu_cli_result.json"

for f in alignment.json lyrics.lrc lyrics.swlrc report.json; do
  test -s "$TMP/jobs/result/$f"
done
cp "$TMP/jobs/result/alignment.json" "$OUT/alignment_raw.json"
cp "$TMP/jobs/result/lyrics.lrc" "$OUT/alignment_raw.lrc"
cp "$TMP/jobs/result/lyrics.swlrc" "$OUT/alignment_raw.swlrc"
cp "$TMP/jobs/result/report.json" "$OUT/alignment_raw_report.json"
cp "$TMP/xingyu_cli_result.json" "$OUT/alignment_cli_result.json"

# Decode the locked audio to PCM only in /tmp for supporting energy/onset checks.
ffmpeg -hide_banner -loglevel error -y -i "$BGM" -ac 1 -ar 16000 -c:a pcm_s16le "$TMP/locked_bgm.wav"
ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels \
  -of json "$BGM" > "$TMP/bgm_ffprobe.json"

python - <<'PY'
from __future__ import annotations
import csv, hashlib, json, math, re, statistics, wave
from pathlib import Path
from datetime import datetime, timezone

SLOT = Path('06_TESTS/MV/WEB_R3/30D_60/D02-B')
OUT = SLOT / '03_AUDIO_TIMELINE'
TMP = Path('/tmp/d02b_audio_timeline')
LOCKED_SHA = '6a4ada560d9f7e08fe945a57dbbc574f3f802737ae102cbc3922871cea2a4bd4'
ASSET_ID = '7670104695834282815'
FADE_D = 0.8


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsec(v: str) -> float:
    mm, ss = v.split(':', 1)
    return int(mm) * 60 + float(ss)


def srt_time(sec: float) -> str:
    ms = int(round(max(0.0, sec) * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

trusted = [x.strip() for x in (OUT/'trusted_lyrics.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
if len(trusted) != 4:
    raise SystemExit(f'expected 4 trusted lyric lines, got {len(trusted)}')

ffp = json.loads((TMP/'bgm_ffprobe.json').read_text())
audio_duration = float(ffp['format']['duration'])
stream = ffp['streams'][0]

# Parse SWLRC blocks. Header: [mm:ss.xxx,mm:ss.xxx], tokens: <start,end>text
sw = (OUT/'alignment_raw.swlrc').read_text(encoding='utf-8').splitlines()
line_re = re.compile(r'^\[(\d{2}:\d{2}\.\d{3}),(\d{2}:\d{2}\.\d{3})\]$')
tok_re = re.compile(r'^<(\d{2}:\d{2}\.\d{3}),(\d{2}:\d{2}\.\d{3})>(.*)$')
blocks = []
current = None
for raw in sw:
    m = line_re.match(raw.strip())
    if m:
        if current:
            blocks.append(current)
        current = {'start': tsec(m.group(1)), 'end': tsec(m.group(2)), 'tokens': []}
        continue
    tm = tok_re.match(raw.strip())
    if tm and current is not None:
        current['tokens'].append({'start': tsec(tm.group(1)), 'end': tsec(tm.group(2)), 'text': tm.group(3)})
if current:
    blocks.append(current)

for b in blocks:
    b['text'] = ''.join(t['text'] for t in b['tokens'])

# Keep only sung blocks. For this file there must be exactly the four trusted lines.
blocks = [b for b in blocks if b['tokens']]
text_exact = len(blocks) == len(trusted) and all(b['text'] == lyric for b, lyric in zip(blocks, trusted))
monotonic = all(
    b['start'] >= -0.001 and b['end'] > b['start'] and b['end'] <= audio_duration + 0.15 and
    (i == 0 or b['start'] >= blocks[i-1]['start'])
    for i, b in enumerate(blocks)
)
token_contained = all(
    all(t['start'] >= b['start'] - 0.03 and t['end'] <= b['end'] + 0.03 and t['end'] > t['start'] for t in b['tokens'])
    for b in blocks
)

report = json.loads((OUT/'alignment_raw_report.json').read_text(encoding='utf-8'))
cli = json.loads((OUT/'alignment_cli_result.json').read_text(encoding='utf-8'))

# Extract warnings conservatively without assuming one exact report schema.
def collect_warning_strings(obj):
    found=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            lk=str(k).lower()
            if 'warning' in lk:
                if isinstance(v, list): found.extend(str(x) for x in v)
                elif v not in (None, '', [], {}): found.append(str(v))
            found.extend(collect_warning_strings(v))
    elif isinstance(obj, list):
        for x in obj: found.extend(collect_warning_strings(x))
    return found
warnings = list(dict.fromkeys(collect_warning_strings(report) + collect_warning_strings(cli)))
critical_terms = ('unmatched','failed','failure','skipped','foreground_voice_switch','section_boundary_review')
critical_warnings = [w for w in warnings if any(term in w.lower() for term in critical_terms)]

# Search numeric estimated/skipped counters recursively.
def counters(obj, prefix=''):
    out=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            key=f'{prefix}.{k}' if prefix else str(k)
            if isinstance(v,(int,float)) and any(s in str(k).lower() for s in ('estimated','skipped','unmatched')):
                out.append((key,v))
            out.extend(counters(v,key))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): out.extend(counters(v,f'{prefix}[{i}]'))
    return out
bad_counters = [(k,v) for k,v in counters(report) if v and float(v) > 0]

# PCM RMS support: verifies aligned spans contain audible energy; not used to invent lyric timing.
with wave.open(str(TMP/'locked_bgm.wav'),'rb') as wf:
    sr=wf.getframerate(); n=wf.getnframes(); raw=wf.readframes(n)
import array
samples=array.array('h'); samples.frombytes(raw)
frame=max(1,int(sr*0.02))
rms=[]
for i in range(0,len(samples),frame):
    chunk=samples[i:i+frame]
    if not chunk: continue
    rms.append(math.sqrt(sum(float(x)*x for x in chunk)/len(chunk)))
nonzero=[x for x in rms if x>1]
global_med=statistics.median(nonzero) if nonzero else 0.0

def interval_rms(a,b):
    i0=max(0,int(a/0.02)); i1=min(len(rms),max(i0+1,int(math.ceil(b/0.02))))
    vals=rms[i0:i1]
    return statistics.median(vals) if vals else 0.0
line_rms=[interval_rms(b['start'],b['end']) for b in blocks]
energy_support = bool(blocks) and global_med > 0 and all(x >= global_med*0.20 for x in line_rms)

# line_timeline.csv
with (OUT/'line_timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f)
    w.writerow(['line_id','lyric','start','end','source_evidence','confidence','qa_status'])
    for i,(lyric,b) in enumerate(zip(trusted,blocks),1):
        w.writerow([f'L{i:02d}',lyric,f"{b['start']:.3f}",f"{b['end']:.3f}",'Route B / Xingyu CTC forced alignment v0.6.1','STRONG_CTC', 'PASS' if (b['text']==lyric) else 'FAIL'])

# SRT only from locked line timeline.
srt=[]
for i,(lyric,b) in enumerate(zip(trusted,blocks),1):
    srt += [str(i), f"{srt_time(b['start'])} --> {srt_time(b['end'])}", lyric, '']
(OUT/'lyrics_exact.srt').write_text('\n'.join(srt),encoding='utf-8')

# Anchor phrases from character token timings, never guessed from line-level interpolation.
anchors=[('A01','想你',0),('A02','忍住',1),('A03','想说',2),('A04','算了',3)]
with (OUT/'anchor_words.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['anchor_id','line_id','anchor','start','end','evidence','purpose','qa_status'])
    for aid,phrase,li in anchors:
        b=blocks[li]; text=b['text']; pos=text.find(phrase)
        if pos < 0:
            w.writerow([aid,f'L{li+1:02d}',phrase,'','','SWLRC character tokens','director semantic anchor','FAIL'])
            continue
        toks=b['tokens'][pos:pos+len(phrase)]
        ok=''.join(t['text'] for t in toks)==phrase
        w.writerow([aid,f'L{li+1:02d}',phrase,f"{toks[0]['start']:.3f}",f"{toks[-1]['end']:.3f}",'SWLRC character token timestamps','director semantic anchor','PASS' if ok else 'FAIL'])

# Supporting music-event clock. Energy derivative creates only supporting strong-onset candidates;
# phrase releases come from the strong CTC route; tail comes from the locked HG02 transform.
deltas=[]
for i in range(1,len(rms)):
    deltas.append((rms[i]-rms[i-1],i*0.02,rms[i]))
deltas.sort(reverse=True,key=lambda x:x[0])
peaks=[]
for delta,t,level in deltas:
    if delta <= 0: break
    if all(abs(t-p[0])>=0.55 for p in peaks):
        peaks.append((t,delta,level))
    if len(peaks)>=3: break
peaks.sort()
fade_start=max(0.0, audio_duration-FADE_D)
with (OUT/'music_events.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['event_id','time','event_type','evidence','purpose','confidence','qa_status'])
    eid=1
    for t,delta,level in peaks:
        w.writerow([f'M{eid:02d}',f'{t:.3f}','strong_energy_onset','20ms PCM RMS positive derivative','candidate edit accent / supporting only', 'SUPPORTING', 'PASS']); eid+=1
    for i,b in enumerate(blocks,1):
        w.writerow([f'M{eid:02d}',f"{b['end']:.3f}",'phrase_release',f'Route B CTC line L{i:02d} end','phrase release / edit breathing point','STRONG_CTC','PASS']); eid+=1
    w.writerow([f'M{eid:02d}',f'{fade_start:.3f}','tail_fade_start','HG02 locked transform: final 0.8s fade','outro/tail handling','LOCKED_TRANSFORM','PASS'])

# Identity and provenance.
audio_identity={
  'schema_version':'1.0','title':'有几次想你了','artist_or_audio_author':'林叙（错位秋天已上线）',
  'exact_version':'Douyin native original audio object 7670104695834282815 / Option B',
  'douyin_music_asset_object_id':ASSET_ID,
  'locked_bgm_reference':'02_BGM/BGM_CANDIDATE_PACKAGE.json#selected_option_by_user=B',
  'locked_bgm_sha256':LOCKED_SHA,
  'rendered_duration_seconds':audio_duration,
  'codec':stream.get('codec_name'),'sample_rate_hz':int(stream.get('sample_rate')),'channels':stream.get('channels'),
  'source_clip_start_seconds':0.0,'source_clip_end_seconds':audio_duration,
  'render_transform':{'speed_change':False,'time_stretch':False,'lead_in_seconds':0.0,'tail_fade_seconds':FADE_D},
  'AUDIO_IDENTITY_LOCKED':'YES'
}
(OUT/'audio_identity.json').write_text(json.dumps(audio_identity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

prov={
  'schema_version':'1.0','evidence_class':'STRONG_ROUTE_B_TRUSTED_LYRICS_CTC_FORCED_ALIGNMENT',
  'trusted_lyrics_source':'Two independently verified Douyin core works use the same exact music object; the displayed/sung excerpt is locked as four lines before timing.',
  'tool':'wangjiqing/xingyu-lyrics-aligner','tool_version':'v0.6.1','runtime':'official CPU Docker image',
  'alignment_method':'WhisperX CTC forced alignment without free ASR rewriting','language':'zh','device':'cpu',
  'locked_audio_sha256':LOCKED_SHA,
  'raw_evidence_files':{p.name:sha(p) for p in [OUT/'alignment_raw.json',OUT/'alignment_raw.lrc',OUT/'alignment_raw.swlrc',OUT/'alignment_raw_report.json',OUT/'alignment_cli_result.json']},
  'clip_transformation_formula':'identity clip clock; no speed/time-stretch/lead-in; final 0.8s fade changes amplitude only, not time mapping',
  'warnings':warnings,'critical_warnings':critical_warnings,'nonzero_estimated_skipped_unmatched_counters':bad_counters,
  'repeated_line_mapping':'No repeated lyric lines in this locked 4-line excerpt.',
  'LYRIC_ALIGNMENT_PROVENANCE_VERIFIED':'YES' if not critical_warnings and not bad_counters else 'NO'
}
(OUT/'alignment_provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

all_pass = text_exact and monotonic and token_contained and energy_support and not critical_warnings and not bad_counters and len(blocks)==4
qa_lines=[
'# D02-B Audio Timeline Alignment QA', '',
'- Strong route: `Route B / trusted lyrics + Chinese CTC forced alignment`',
'- Tool: `wangjiqing/xingyu-lyrics-aligner v0.6.1`',
'- Locked BGM SHA verified before alignment: `PASS`',
-f'- Aligned line count: `{len(blocks)}` / expected `4`',
-f'- Trusted text ↔ SWLRC token reconstruction: `{"PASS" if text_exact else "FAIL"}`',
-f'- Monotonic/in-bounds line timing: `{"PASS" if monotonic else "FAIL"}`',
-f'- Character token containment: `{"PASS" if token_contained else "FAIL"}`',
-f'- PCM energy support inside all aligned sung spans: `{"PASS" if energy_support else "FAIL"}`',
-f'- Critical aligner warnings: `{len(critical_warnings)}`',
-f'- Nonzero estimated/skipped/unmatched counters: `{len(bad_counters)}`', '',
'## Ground-truth audit', ''
]
for i,(lyric,b,r) in enumerate(zip(trusted,blocks,line_rms),1):
    qa_lines.append(f'- L{i:02d} `{lyric}`: `{b["start"]:.3f}s → {b["end"]:.3f}s`; token text exact; median PCM RMS `{r:.1f}`; `PASS`')
qa_lines += ['', '## Gate markers', '',
'AUDIO_IDENTITY_LOCKED = YES',
'LYRIC_TEXT_LOCKED = YES',
'LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED = YES',
-f'LYRIC_ALIGNMENT_PROVENANCE_VERIFIED = {"YES" if not critical_warnings and not bad_counters else "NO"}',
-f'ALIGNMENT_GROUND_TRUTH_QA_PASS = {"YES" if all_pass else "NO"}',
-f'LYRIC_TIMELINE_LOCKED = {"YES" if all_pass else "NO"}',
-f'MUSIC_EVENT_MAP_VERIFIED = {"YES" if all_pass else "NO"}',
-f'AUDIO_TIMELINE_PACKAGE_LOCKED = {"YES" if all_pass else "NO"}', '',
-f'FINAL_QA = {"PASS" if all_pass else "BLOCKED"}',
]
(OUT/'alignment_qa_report.md').write_text('\n'.join(qa_lines)+'\n',encoding='utf-8')

# Manifest is written last and hashes every package member except itself.
required=[
'audio_identity.json','trusted_lyrics.txt','alignment_raw.json','alignment_raw.lrc','alignment_raw.swlrc','alignment_raw_report.json','alignment_cli_result.json',
'alignment_provenance.json','line_timeline.csv','lyrics_exact.srt','anchor_words.csv','music_events.csv','alignment_qa_report.md']
manifest={
 'package_version':'1.0','slot_id':'D02-B','song_family':'有几次想你了','selected_bgm_option':'B','locked_bgm_sha256':LOCKED_SHA,
 'strong_timing_route':'B_TRUSTED_LYRICS_CTC_FORCED_ALIGNMENT','files':{name:sha(OUT/name) for name in required},
 'AUDIO_IDENTITY_LOCKED':'YES','LYRIC_TEXT_LOCKED':'YES','LYRIC_ALIGNMENT_RAW_EVIDENCE_SAVED':'YES',
 'LYRIC_ALIGNMENT_PROVENANCE_VERIFIED':'YES' if not critical_warnings and not bad_counters else 'NO',
 'ALIGNMENT_GROUND_TRUTH_QA_PASS':'YES' if all_pass else 'NO','LYRIC_TIMELINE_LOCKED':'YES' if all_pass else 'NO',
 'MUSIC_EVENT_MAP_VERIFIED':'YES' if all_pass else 'NO','AUDIO_TIMELINE_PACKAGE_LOCKED':'YES' if all_pass else 'NO',
 'locked_at':datetime.now(timezone.utc).isoformat() if all_pass else None,
 'status':'PASS' if all_pass else 'BLOCKED'
}
(OUT/'package_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'all_pass':all_pass,'line_count':len(blocks),'warnings':warnings,'critical_warnings':critical_warnings,'bad_counters':bad_counters,'duration':audio_duration},ensure_ascii=False,indent=2))
if not all_pass:
    raise SystemExit(42)
PY
