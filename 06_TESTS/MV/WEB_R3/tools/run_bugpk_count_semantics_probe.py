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
VARIANTS=[
 ('page_size_30', {'page':1,'page_size':30}),
 ('count_30', {'count':30}),
 ('count_36', {'count':36}),
 ('count_54', {'count':54}),
 ('count_72', {'count':72}),
]

def main():
    root=Path(__file__).resolve().parents[4]
    out=root/'06_TESTS/MV/WEB_R3/_count_semantics_probe'
    out.mkdir(parents=True,exist_ok=True)
    s=requests.Session(); s.headers.update({'User-Agent':'Mozilla/5.0','Accept':'application/json,text/plain,*/*'})
    report=[]
    for case,uid in TARGETS.items():
        for name,extra in VARIANTS:
            params={'id':uid,**extra}
            rec={'case_id':case,'variant':name,'params':params}
            try:
                r=s.get(BASE,params=params,timeout=60)
                rec['http_status']=r.status_code
                payload=r.json()
                rec['code']=payload.get('code') if isinstance(payload,dict) else None
                rec['msg']=payload.get('msg') if isinstance(payload,dict) else None
                data=(payload.get('data') or []) if isinstance(payload,dict) else []
                rec['items']=len(data) if isinstance(data,list) else None
                rec['pagination']=payload.get('pagination') if isinstance(payload,dict) else None
                if isinstance(data,list) and data:
                    rec['newest']=data[0].get('create_time')
                    rec['oldest']=data[-1].get('create_time')
                    rec['first_aweme']=data[0].get('aweme_id')
                    rec['last_aweme']=data[-1].get('aweme_id')
                (out/f'{case}_{name}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
            except Exception as e:
                rec['error']=str(e)[:500]
            report.append(rec)
            time.sleep(3)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__': main()
