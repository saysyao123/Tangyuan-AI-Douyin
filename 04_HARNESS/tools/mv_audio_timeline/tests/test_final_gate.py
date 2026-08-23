import csv, json, math, subprocess, sys, tempfile, wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/'package_tool.py'; FINAL=ROOT/'final_gate.py'

def run(tool,*args,expect=0):
    p=subprocess.run([sys.executable,str(tool),*map(str,args)],text=True,capture_output=True)
    if p.returncode!=expect: raise AssertionError(f'rc={p.returncode} expected={expect}\n{p.stdout}\n{p.stderr}')
    return p

def wav(path,seconds=5,sr=8000):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(b''.join(int(5000*math.sin(2*math.pi*220*i/sr)).to_bytes(2,'little',signed=True) for i in range(int(seconds*sr))))

def write_csv(path,headers,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers);w.writeheader();w.writerows(rows)

def build(root:Path,complete=True,bad_anchor=False):
    audio=root/'a.wav';wav(audio);lyrics=root/'lyrics.txt';lyrics.write_text('第一句\n第二句\n',encoding='utf-8');pkg=root/'pkg'
    run(CORE,'init','--package',pkg,'--audio',audio,'--lyrics',lyrics,'--title','T','--artist','A','--version','V','--source-clip-start','10','--source-clip-end','15')
    raw=root/'align.csv';write_csv(raw,['line_id','lyric','clip_start_s','clip_end_s'],[
        {'line_id':'L01','lyric':'第一句','clip_start_s':'0.500','clip_end_s':'2.000'},
        {'line_id':'L02','lyric':'第二句','clip_start_s':'2.100','clip_end_s':'4.500'}])
    run(CORE,'import-alignment','--package',pkg,'--timeline',raw,'--evidence-class','ASR_FORCED_ALIGNMENT','--tool','fixture','--tool-version','1')
    run(CORE,'mark-qa','--package',pkg,'--pass-qa','--note','synthetic audited boundaries')
    run(CORE,'export-srt','--package',pkg)
    if complete:
        write_csv(pkg/'anchor_words.csv',['anchor_id','line_id','phrase','start_s','end_s','qa_status'],[
            {'anchor_id':'A01','line_id':'L01','phrase':'第一','start_s':'0.700','end_s':'1.000' if not bad_anchor else '3.000','qa_status':'PASS'}])
        write_csv(pkg/'music_events.csv',['event_id','time_s','type','description','qa_status'],[
            {'event_id':'M01','time_s':'0.000','type':'PICKUP','description':'start','qa_status':'PASS'},
            {'event_id':'M02','time_s':'4.800','type':'TAIL','description':'release','qa_status':'PASS'}])
        (pkg/'alignment_qa_report.md').write_text('# QA\n\nSynthetic fixture: every lyric boundary checked against fixture ground truth.\n',encoding='utf-8')
        run(FINAL,'seal-qa','--package',pkg)
    return audio,pkg

def test_incomplete_package_fails():
    with tempfile.TemporaryDirectory() as d:
        a,p=build(Path(d),complete=False);out=run(FINAL,'validate','--package',p,'--audio',a,expect=2)
        assert 'anchor_words.csv' in out.stdout

def test_bad_anchor_fails():
    with tempfile.TemporaryDirectory() as d:
        a,p=build(Path(d),bad_anchor=True);out=run(FINAL,'validate','--package',p,'--audio',a,expect=2)
        assert 'anchor outside lyric window' in out.stdout

def test_complete_package_passes_and_locks():
    with tempfile.TemporaryDirectory() as d:
        a,p=build(Path(d));out=run(FINAL,'validate','--package',p,'--audio',a,'--write-manifest')
        payload=json.loads(out.stdout);assert payload['pass'] is True
        m=json.loads((p/'package_manifest.json').read_text());assert m['AUDIO_TIMELINE_PACKAGE_LOCKED'] is True
        assert 'anchor_words.csv' in m['files'] and 'music_events.csv' in m['files'] and 'alignment_qa_report.md' in m['files']

if __name__=='__main__':
    ts=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    for t in ts:t();print('PASS',t.__name__)
    print(f'{len(ts)} tests passed')
