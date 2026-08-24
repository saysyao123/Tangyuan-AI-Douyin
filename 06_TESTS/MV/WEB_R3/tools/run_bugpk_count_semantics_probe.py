#!/usr/bin/env python3
from __future__ import annotations
import json, time
from pathlib import Path
import requests

BASE='https://api.bugpk.com/api/dyzy'
TARGETS={
 'P04':'MS4wLjABAAAA_TyjlQm1QDz9oQlS4x7f3MzHvuL-V9IYMQ2Qsc2xWg4',
 'P07':'MS4wLjABAAAAtxmz8hjhGyax79DGnNe5KojkphdWs1GOojeMcq3H-y4',
}

def summarize(payload):
    data=(payload.get('data') or []) if isinstance(payload,dict) else []
    rec={
        'code': payload.get('code') if isinstance(payload,dict) else None,
        'msg': payload.get('msg') if isinstance(payload,dict) else None,
        'items': len(data) if isinstance(data,list) else None,
        'pagination': payload.get('pagination') if isinstance(payload,dict) else None,
    }
    if isinstance(data,list) and data:
        rec.update({
            'newest':data[0].get('create_time'),
            'oldest':data[-1].get('create_time'),
            'first_aweme':data[0].get('aweme_id'),
            'last_aweme':data[-1].get('aweme_id'),
        })
    return rec

def call(s, params):
    r=s.get(BASE,params=params,timeout=60)
    payload=r.json()
    return r.status_code,payload

def main():
    root=Path(__file__).resolve().parents[4]
    out=root/'06_TESTS/MV/WEB_R3/_count_semantics_probe'
    out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(); s.headers.update({'User-Agent':'Mozilla/5.0','Accept':'application/json,text/plain,*/*'})
    report=[]
    for case,uid in TARGETS.items():
        # First page is the control and gives the real cursor.
        control_params={'id':uid,'page':1,'page_size':30}
        http,payload=call(s,control_params)
        control={'case_id':case,'variant':'page_size_30','params':control_params,'http_status':http,**summarize(payload)}
        report.append(control)
        (out/f'{case}_page_size_30.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
        cursor=str(((payload.get('pagination') or {}).get('next_cursor') or ''))
        time.sleep(3)

        variants=[
            ('page_2', {'page':2,'page_size':30}),
            ('max_cursor', {'max_cursor':cursor,'page_size':30}),
            ('cursor', {'cursor':cursor,'page_size':30}),
            ('next_cursor', {'next_cursor':cursor,'page_size':30}),
            ('page2_max_cursor', {'page':2,'max_cursor':cursor,'page_size':30}),
            ('page2_cursor', {'page':2,'cursor':cursor,'page_size':30}),
        ]
        for name,extra in variants:
            params={'id':uid,**extra}
            rec={'case_id':case,'variant':name,'params':params}
            try:
                http,payload=call(s,params)
                rec.update({'http_status':http,**summarize(payload)})
                (out/f'{case}_{name}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
            except Exception as e:
                rec['error']=str(e)[:500]
            report.append(rec)
            time.sleep(3)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__': main()
