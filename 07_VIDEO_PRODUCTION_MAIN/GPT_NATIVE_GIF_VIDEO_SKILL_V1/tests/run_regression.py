#!/usr/bin/env python3
"""Offline, text-fixture regression plus actual 5s/24fps media; stdlib runner."""
import argparse
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from fixtures import make_all


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
    if list(a.out.iterdir()):raise SystemExit('Use an empty evidence directory')
    started=time.perf_counter();log=io.StringIO()
    tests=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(tests)
    (a.out/'tests.log').write_text(log.getvalue(),encoding='utf-8')
    fixtures=make_all(a.out/'fixtures')
    command=[sys.executable,str(ROOT/'scripts/gif_to_video.py'),'--input',str(fixtures/'fixed.gif'),
             '--out',str(a.out/'fixture_video'),'--source-reviewed','--source-origin','synthetic-fixture']
    run=subprocess.run(command,capture_output=True,text=True)
    (a.out/'fixture_cli.log').write_text(run.stdout+run.stderr,encoding='utf-8')
    report={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'skipped':len(result.skipped),'test_exit_code':0 if result.wasSuccessful() else 1,
            'fixture_cli_exit_code':run.returncode,'elapsed_seconds':time.perf_counter()-started,
            'python':platform.python_version(),'command':command,
            'status':'ENGINEERING_PASS' if result.wasSuccessful() and run.returncode==0 else 'FAIL',
            'real_character_visual_qa':'NOT_PROVEN_BY_SYNTHETIC_FIXTURES'}
    (a.out/'summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return 0 if report['status']=='ENGINEERING_PASS' else 1


if __name__=='__main__':raise SystemExit(main())
