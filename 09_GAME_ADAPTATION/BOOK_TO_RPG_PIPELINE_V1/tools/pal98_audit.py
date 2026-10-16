#!/usr/bin/env python3
"""Read-only MKF metadata audit. Never exports chunks, scripts, character text or game assets.
Usage: python3 tools/pal98_audit.py --sss Sss.mkf --data Data.mkf --msg M.msg --word Word.dat --out report.json
Only use source files you have permission to examine. No EXE is executed.
"""
import argparse, collections, hashlib, json, pathlib, struct, sys

def mkf(path):
    raw=pathlib.Path(path).read_bytes()
    if len(raw)<8: raise ValueError('MKF shorter than 8 bytes')
    first=struct.unpack_from('<I',raw,0)[0]
    if first%4 or first<8 or first>len(raw) or first>8000000:raise ValueError('invalid MKF table length')
    count=first//4-1
    offsets=struct.unpack_from('<'+'I'*(count+1),raw,0)
    if offsets[0]!=first or offsets[-1]!=len(raw) or any(a>b for a,b in zip(offsets,offsets[1:])):
        raise ValueError('invalid MKF index offsets')
    return {'raw':raw,'chunks':[raw[offsets[i]:offsets[i+1]] for i in range(count)],
            'sha256':hashlib.sha256(raw).hexdigest(),'count':count}

def inspect(sss,data,msg=None,word=None):
    ss=mkf(sss);dd=mkf(data)
    if ss['count']<5:raise ValueError('SSS must have at least five chunks')
    lengths=[len(c) for c in ss['chunks']]
    for idx,sz in ((0,32),(1,8),(2,14),(3,4),(4,8)):
        if len(ss['chunks'][idx])%sz:raise ValueError('invalid structure boundary SSS chunk '+str(idx))
    scripts=ss['chunks'][4]
    op=collections.Counter(struct.unpack_from('<H',scripts,i)[0] for i in range(0,len(scripts),8))
    result={'source':'user-supplied-local-game-files; read-only aggregate metadata only',
        'sss_sha256':ss['sha256'],'data_sha256':dd['sha256'],
        'sss_chunk_lengths':lengths,'data_chunk_lengths':[len(c) for c in dd['chunks']],
        'candidate_event_objects_32_byte':len(ss['chunks'][0])//32,'scene_records_8_byte':len(ss['chunks'][1])//8,
        'object_records_14_byte':len(ss['chunks'][2])//14,
        'script_records_8_byte':len(scripts)//8,'distinct_opcode_values':len(op),
        'special_value_0xFFFF':op[0xffff],
        'opcode_frequency':{'0x%04X'%k:v for k,v in sorted(op.items())},
        'message_offset_entries':len(ss['chunks'][3])//4,
        'data_chunk_count':dd['count']}
    offsets=struct.unpack('<'+'I'*(len(ss['chunks'][3])//4),ss['chunks'][3])
    result['message_offsets_monotonic']=all(a<=b for a,b in zip(offsets,offsets[1:]))
    result['message_last_offset']=offsets[-1] if offsets else None
    if msg:
        m=pathlib.Path(msg).read_bytes()
        result['msg_file_bytes']=len(m);result['message_index_matches_file_size']=bool(offsets and offsets[-1]==len(m))
        if not result['message_offsets_monotonic'] or not result['message_index_matches_file_size']:
            raise ValueError('message index is inconsistent with text length')
        result['nonempty_message_spans']=sum(b>a for a,b in zip(offsets,offsets[1:]))
    if word:
        w=pathlib.Path(word).read_bytes()
        result['word_file_bytes']=len(w);result['word_records_if_10byte']=len(w)//10 if len(w)%10==0 else None
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--sss',required=True);p.add_argument('--data',required=True)
    p.add_argument('--msg');p.add_argument('--word');p.add_argument('--out')
    a=p.parse_args();report=inspect(a.sss,a.data,a.msg,a.word)
    summary=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if a.out:pathlib.Path(a.out).write_text(summary,encoding='utf8')
    else:print(summary)
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,struct.error) as exc: print('AUDIT_FAIL:',exc,file=sys.stderr);sys.exit(1)
