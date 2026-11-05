"""Run controlled baseline/retimed/palette comparisons; never score face identity."""
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'tests')]
import gif_to_video as g
from fixtures import motion_frames


def load_module(path):
    spec=importlib.util.spec_from_file_location('baseline',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def benchmark(legacy_script, source, out):
    out.mkdir(parents=True,exist_ok=True)
    old=load_module(legacy_script)
    src,ds,_=g.decode_gif(source)
    # Warm up OpenCV; repeat three times, report median not a best run.
    old.render_frames(src[:3],8);g.render_frames(src[:3],8,ds[:3])
    times={}
    for label,fn in [('legacy',lambda:old.render_frames(src,120)),
                     ('v11',lambda:g.render_frames(src,120,ds)[0])]:
        durations=[]
        for _ in range(3):
            t=time.perf_counter();result=fn();durations.append(time.perf_counter()-t)
        times[label]={'runs_seconds':durations,'median_seconds':float(np.median(durations))}
    output,records,calls=g.render_frames(src,120,ds)
    # Static-region temporal color pumping after GIF quantization.
    fixed=motion_frames()
    palette={}
    for mode in ['global','per-frame']:
        path=out/f'palette_{mode}.gif';g.encode_gif(fixed,path,5.,palette_mode=mode)
        decoded,_,_=g.decode_gif(path)
        roi=[f[:40].astype(float) for f in decoded]
        temporal=float(np.mean([np.abs(a-b).mean() for a,b in zip(roi,roi[1:])]))
        palette[mode]={'fixed_background_temporal_mae':temporal}
    # Timing correctness independent of image estimator: known source start times.
    durations=[100,700,200];n=120
    mapping=g.timeline_map(durations,n)
    expected=np.searchsorted([0,100,800,1000],np.arange(n)*1000/n+1e-9,side='right')-1
    old_indices=np.floor(np.arange(n)*2/(n-1)).astype(int)
    timing={'fixture_durations_ms':durations,
            'old_wrong_source_intervals':int(np.count_nonzero(expected!=old_indices)),
            'v11_wrong_source_intervals':int(np.count_nonzero(expected!=[r['source_index'] for r in mapping]))}
    # Cache is a pure optimization: pixel equality at the same t is mandatory.
    max_error=0
    for k in range(len(src)-1):
        fields=g.pair_flow(src[k],src[k+1])
        for t in [.25,.5,.75]:
            a=old.optical_between(src[k],src[k+1],t)
            b=g.optical_between(src[k],src[k+1],t,fields=fields)
            max_error=max(max_error,int(np.abs(a.astype(int)-b.astype(int)).max()))
    result={'source_sha256':g.sha256(source),'baseline_script_sha256':g.sha256(legacy_script),
            'current_script_sha256':g.sha256(ROOT/'scripts/gif_to_video.py'),
            'runtime_median':times,'render_speedup_ratio':times['legacy']['median_seconds']/times['v11']['median_seconds'],
            'flow_calls':{'legacy':236,'v11':calls},'same_time_warp_max_pixel_error':max_error,
            'timing':timing,'palette':palette,
            'scope':'Engineering correctness, timing and palette stability only. No claim of recovered detail or human anatomy.'}
    g.write_json(out/'benchmark.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--legacy-script',required=True,type=Path)
    p.add_argument('--real-source',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();benchmark(a.legacy_script,a.real_source,a.out)
