#!/usr/bin/env python3
"""Auditable GIF postprocessor. No generation API, model weights or paid service.

Source samples live at cumulative GIF start times. The last GIF delay is a
natural hold, never an implicit loop. MP4 is CFR; GIF uses centisecond delays.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

import cv2
import numpy as np
from PIL import GifImagePlugin, Image, ImageColor, ImageDraw, __version__ as PIL_VERSION

VERSION = '1.1.0'
MAX_MEMORY = 768 * 1024**2  # conservative working-set estimate, not an OS guarantee


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def decode_gif(path, matte=(0, 0, 0), default_duration_ms=None):
    """Pillow sequential seek performs logical-screen/disposal reconstruction.

    Composite RGBA onto an explicit matte only after reconstruction. A .gif
    suffix is insufficient. Do not silently invent missing/zero frame delays.
    """
    frames, durations, disposals, rectangles, timing_overrides = [], [], [], [], []
    with Image.open(path) as im:
        if im.format != 'GIF':
            raise ValueError('Input must be a genuine GIF87a/GIF89a file')
        if im.n_frames < 2:
            raise ValueError('Source must contain at least two decoded frames')
        if im.width * im.height > 2_000_000 or im.n_frames > 512:
            raise ValueError('Input exceeds CPU profile: 2M pixels or 512 source frames')
        if im.width * im.height * im.n_frames * 12 > MAX_MEMORY:
            raise ValueError('Source working-set estimate exceeds 768 MiB CPU profile')
        loop, version = im.info.get('loop'), im.info.get('version', b'').decode('ascii')
        has_transparency = False
        for i in range(im.n_frames):
            im.seek(i)
            d = im.info.get('duration')
            if d is None or d <= 0:
                if default_duration_ms is None or default_duration_ms <= 0:
                    raise ValueError(f'Frame {i} has missing/zero duration; supply explicit --default-duration-ms')
                d = default_duration_ms
                timing_overrides.append(i)
            durations.append(int(d))
            disposals.append(int(getattr(im, 'disposal_method', 0)))
            rectangles.append(list(getattr(im, 'dispose_extent', (0, 0, im.width, im.height))))
            rgba = im.convert('RGBA')
            has_transparency |= rgba.getextrema()[3][0] < 255
            bg = Image.new('RGBA', rgba.size, (*matte, 255))
            frames.append(np.array(Image.alpha_composite(bg, rgba).convert('RGB')))
    if len(frames) < 2:
        raise ValueError('Source must contain at least two decoded frames')
    return frames, durations, {
        'loop': loop, 'version': version, 'durations_ms': durations,
        'disposal': disposals, 'local_rectangles': rectangles,
        'transparency_composited': has_transparency, 'matte_rgb': list(matte),
        'timing_override_frames': timing_overrides,
    }


def load_gif(path):
    """Compatibility reader returning frames, durations, loop."""
    f, d, m = decode_gif(path)
    return f, d, m['loop']


def timeline_map(durations, output_count):
    """Sample j*source_total/N; preserve variable delays, including final hold.

    No forced endpoint at t=duration: CFR sample 119 starts at 119/24 seconds.
    Source onset times may fall between output ticks; provenance counts actual
    endpoint samples, not a fictitious N - source_count formula.
    """
    if output_count < 2 or len(durations) < 2 or min(durations) <= 0:
        raise ValueError('Need >=2 output/source frames and positive durations')
    starts = np.r_[0., np.cumsum(durations, dtype=np.float64)]
    records = []
    for j in range(output_count):
        t = j * starts[-1] / output_count
        k = min(int(np.searchsorted(starts, t + 1e-9, side='right') - 1), len(durations) - 1)
        alpha = max(0., (t - starts[k]) / durations[k])
        kind = 'source_sample' if alpha < 1e-8 else ('terminal_hold' if k == len(durations) - 1 else 'interpolated')
        records.append({'output_frame': j, 'source_time_ms': round(float(t), 6),
                        'source_index': k, 'alpha': round(float(alpha), 10), 'kind': kind})
    return records


def pair_flow(a, b):
    ga, gb = [cv2.cvtColor(x, cv2.COLOR_RGB2GRAY) for x in (a, b)]
    fields = [cv2.calcOpticalFlowFarneback(x, y, None, .5, 3, 13, 3, 5, 1.2, 0)
              for x, y in ((ga, gb), (gb, ga))]
    return tuple(np.clip(cv2.medianBlur(f, 5), -24, 24) for f in fields)


def optical_between(a, b, t, method='flow', fields=None):
    """Retain V1 bidirectional approximate inverse warp. Not occlusion solving."""
    if t <= 0:
        return a.copy()
    if t >= 1:
        return b.copy()
    if method == 'blend':
        return cv2.addWeighted(a, 1-t, b, t, 0)
    ab, ba = pair_flow(a, b) if fields is None else fields
    h, w = a.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    aw = cv2.remap(a, gx-t*ab[:, :, 0], gy-t*ab[:, :, 1], cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT101)
    bw = cv2.remap(b, gx-(1-t)*ba[:, :, 0], gy-(1-t)*ba[:, :, 1], cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT101)
    return cv2.addWeighted(aw, 1-t, bw, t, 0)


def flow_pair_risk(a, b, fields):
    # Large connected disagreement of the two middle-time warps is a warning,
    # not an anatomical classifier. In the real sample it exposes the hand ghost.
    ab, ba = fields
    h, w = a.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    aw = cv2.remap(a, gx-.5*ab[:, :, 0], gy-.5*ab[:, :, 1], cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT101)
    bw = cv2.remap(b, gx-.5*ba[:, :, 0], gy-.5*ba[:, :, 1], cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_REFLECT101)
    disagreement = np.max(np.abs(aw.astype(np.int16)-bw.astype(np.int16)), axis=2)
    mask = (disagreement > 35).astype(np.uint8)
    _, _, stats, _ = cv2.connectedComponentsWithStats(mask)
    largest = int(max(stats[1:, cv2.CC_STAT_AREA], default=0))
    return {'flag': 'OCCLUSION_OR_GHOST_RISK' if largest > max(64, .008*h*w) else None,
            'largest_disagreement_component_pixels': largest,
            'fraction_pixels_rgb_difference_over_35': float(mask.mean()),
            'warning': 'Heuristic; inspect actual output. Does not prove good/bad anatomy.'}


def render_frames(source, output_count, durations=None, method='flow', risk_log=None):
    durations = [100] * len(source) if durations is None else durations
    if len(durations) != len(source):
        raise ValueError('One duration required per source frame')
    records = timeline_map(durations, output_count)
    frames, cached_index, fields, calls = [], None, None, 0
    for r in records:
        k, t = r['source_index'], r['alpha']
        if r['kind'] != 'interpolated':
            frames.append(source[k].copy())
            continue
        if method == 'flow' and cached_index != k:
            fields, cached_index = pair_flow(source[k], source[k+1]), k
            calls += 2
            if risk_log is not None:
                risk_log.append({'source_pair': [k, k+1], **flow_pair_risk(source[k], source[k+1], fields)})
        frames.append(optical_between(source[k], source[k+1], t, method, fields))
    return frames, records, calls


def diagnostics(frames):
    diffs = [float(np.mean(np.abs(a.astype(np.int16)-b.astype(np.int16))))
             for a, b in zip(frames, frames[1:])]
    med = float(np.median(diffs)) if diffs else 0.
    exact = sum(np.array_equal(a, b) for a, b in zip(frames, frames[1:]))
    return {'adjacent_mean_abs_rgb_diff': {'min': min(diffs, default=0.), 'median': med,
                                         'max': max(diffs, default=0.)},
            'exact_duplicate_transitions': exact,
            'near_duplicate_transitions_threshold_0_15': sum(x < .15 for x in diffs),
            'extreme_change_boundaries': [i+1 for i, d in enumerate(diffs) if d > 45. or (med > .2 and d > max(25., 12*med))],
            'warning': 'Signals only; cannot prove identity, hands, complete scenes or absence of grids.'}


def source_risks(frames):
    """Conservative fixed-camera guard. Tests cover known negatives, not all grids."""
    diag = diagnostics(frames)
    translations = []
    h, w = frames[0].shape[:2]
    mask = np.full((h, w), 255, np.uint8)
    mask[h//5:4*h//5, w//5:4*w//5] = 0
    for a, b in zip(frames, frames[1:]):
        ga, gb = [cv2.cvtColor(x, cv2.COLOR_RGB2GRAY) for x in (a, b)]
        pts = cv2.goodFeaturesToTrack(ga, maxCorners=120, qualityLevel=.02, minDistance=4, mask=mask)
        if pts is None or len(pts) < 8:
            translations.append(None)
            continue
        nxt, ok, _ = cv2.calcOpticalFlowPyrLK(ga, gb, pts, None)
        back, ok_back, _ = cv2.calcOpticalFlowPyrLK(gb, ga, nxt, None)
        valid = (ok[:, 0] > 0) & (ok_back[:, 0] > 0) & (np.linalg.norm(back[:, 0]-pts[:, 0], axis=1) < 1.)
        if valid.sum() < 8:
            translations.append(None)
            continue
        delta = nxt[valid, 0]-pts[valid, 0]
        center = np.median(delta, axis=0)
        support = float((np.linalg.norm(delta-center, axis=1) < .75).mean())
        translations.append([float(center[0]), float(center[1]), support])
    drift = [i+1 for i, v in enumerate(translations) if v is not None and np.linalg.norm(v[:2]) > 1.0 and v[2] > .7]
    flags = []
    if diag['exact_duplicate_transitions'] == len(frames)-1:
        flags.append('STATIC_SOURCE')
    if len(drift) >= max(2, math.ceil(.35*(len(frames)-1))):
        flags.append('GLOBAL_DRIFT_OR_SCROLL')
    if diag['extreme_change_boundaries']:
        flags.append('ABRUPT_CHANGE_OR_GRID_SLIP')
    return {'flags': flags, 'background_translation_xy_support': translations,
            'drift_boundaries': drift, 'diagnostics': diag,
            'coverage': 'Heuristic fixed-camera guard; subtle grids and anatomy still require actual review.'}


def visual_sheet(frames, out, cols=4, sample=16, index_offset=0, total=None):
    inds = np.linspace(0, len(frames)-1, min(sample, len(frames)), dtype=int)
    rows = math.ceil(len(inds)/cols)
    sheet = Image.new('RGB', (cols*176, rows*320), '#222222')
    for j, idx in enumerate(inds):
        im = Image.fromarray(frames[idx]); im.thumbnail((160, 284))
        x, y = (j % cols)*176, (j//cols)*320
        sheet.paste(im, (x+(176-im.width)//2, y+8))
        ImageDraw.Draw(sheet).text((x+8, y+299), f'Frame {idx+index_offset}/{(total or len(frames))-1}', fill='white')
    sheet.save(out, quality=92)


def review_pages(frames, directory, prefix):
    names = []
    for i in range(0, len(frames), 30):
        name = f'{prefix}_{i:03d}_{min(i+29, len(frames)-1):03d}.jpg'
        visual_sheet(frames[i:i+30], Path(directory)/name, cols=6, sample=30, index_offset=i, total=len(frames))
        names.append(name)
    return names


def shared_palette(frames):
    # Bounded, deterministic samples from ALL frames, no per-frame color pumping.
    samples = []
    for f in frames:
        im = Image.fromarray(f); im.thumbnail((64, 64))
        samples.append(np.array(im).reshape(-1, 3))
    pixels = np.concatenate(samples)
    if len(pixels) > 262144:
        pixels = pixels[np.linspace(0, len(pixels)-1, 262144, dtype=int)]
    return Image.fromarray(pixels.reshape(-1, 1, 3)).quantize(colors=256, method=Image.Quantize.MEDIANCUT)


def gif_delays(count, seconds):
    cs = round(seconds*100)
    if abs(seconds*100-cs) > 1e-7 or cs < count:
        raise ValueError('GIF needs representable centiseconds and >=10ms per frame')
    return [round((i+1)*cs/count)-round(i*cs/count) for i in range(count)]


def encode_gif(frames, out, duration_seconds, loop=False, palette_mode='global'):
    delays = gif_delays(len(frames), duration_seconds)
    palette = shared_palette(frames) if palette_mode == 'global' else None
    with Path(out).open('wb') as stream:
        for i, f in enumerate(frames):
            im = Image.fromarray(f)
            if palette is None:
                im = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
            else:
                im = im.quantize(palette=palette, dither=Image.Dither.NONE)
            # Public GIF block helpers preserve genuine holds without Pillow's
            # save_all identical-frame merging. Never perturb pixels to fake motion.
            if i == 0:
                header, _ = GifImagePlugin.getheader(im, info={'loop': 0} if loop else {})
                header[0] = b'GIF89a' + header[0][6:]
                for block in header:
                    stream.write(block)
            for block in GifImagePlugin.getdata(im, duration=delays[i]*10, disposal=1,
                                               include_color_table=palette is None):
                stream.write(block)
        stream.write(b';')
    return delays


def encode_mp4(frames, out, fps, audio=None):
    h, w = frames[0].shape[:2]
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
           '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', str(fps), '-i', '-']
    if audio:
        cmd += ['-i', str(audio), '-map', '0:v:0', '-map', '1:a:0', '-af', 'apad',
                '-c:a', 'aac', '-b:a', '160k', '-t', str(len(frames)/fps)]
    else:
        cmd += ['-an']
    cmd += ['-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:color=black,setsar=1',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-r', str(fps), '-frames:v', str(len(frames)), '-movflags', '+faststart', str(out)]
    with tempfile.TemporaryFile() as errors:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=errors)
        try:
            for f in frames:
                proc.stdin.write(np.ascontiguousarray(f).tobytes())
            proc.stdin.close()
            rc = proc.wait(timeout=180)
        except BaseException as exc:
            proc.kill(); proc.wait()
            errors.seek(0)
            raise RuntimeError(f'FFmpeg interrupted: {errors.read().decode(errors="replace")[-1500:]}') from exc
        errors.seek(0)
        if rc:
            raise RuntimeError(f'FFmpeg exit {rc}: {errors.read().decode(errors="replace")[-1500:]}')
    return cmd


def probe_mp4(path):
    cmd = ['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)]
    result = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180).stdout)
    return result


def decode_mp4_frames(path):
    meta = probe_mp4(path)
    video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    w, h, n = video['width'], video['height'], int(video['nb_read_frames'])
    if w*h*n*3 > MAX_MEMORY:
        raise ValueError('Decoded review frames exceed CPU profile')
    data = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                          capture_output=True, check=True, timeout=180).stdout
    if len(data) != w*h*n*3:
        raise RuntimeError('Decoded MP4 byte length mismatch')
    return list(np.frombuffer(data, dtype=np.uint8).reshape(n, h, w, 3))


def verify_outputs(gif, mp4, n, fps, seconds, gif_size, audio=False):
    frames, delays, meta = decode_gif(gif)
    if len(frames) != n or sum(delays) != round(seconds*1000) or list(frames[0].shape[1::-1]) != list(gif_size):
        raise RuntimeError('GIF frame count, dimensions or duration verification failed')
    if meta['version'] != 'GIF89a':
        raise RuntimeError('GIF89a verification failed')
    mp = probe_mp4(mp4)
    video = next(s for s in mp['streams'] if s['codec_type'] == 'video')
    if (int(video.get('nb_read_frames', -1)) != n or int(video.get('nb_frames', -1)) != n
        or Fraction(video['r_frame_rate']) != fps or Fraction(video['avg_frame_rate']) != fps
        or video['codec_name'] != 'h264' or video['pix_fmt'] != 'yuv420p'
        or abs(float(video['duration'])-seconds) > .001
        or video['width'] != gif_size[0]+gif_size[0] % 2
        or video['height'] != gif_size[1]+gif_size[1] % 2):
        raise RuntimeError('MP4 count/fps/codec/size/duration verification failed')
    timestamps = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_frames', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(mp4)],
        capture_output=True, text=True, check=True, timeout=180).stdout)['frames']
    if len(timestamps) != n or any(abs(float(x['best_effort_timestamp_time'])-i/fps) > 2e-6 for i, x in enumerate(timestamps)):
        raise RuntimeError('Decoded MP4 timestamp spacing is not requested CFR')
    # Decode all video AND audio packets, fail on actual decoder errors.
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-err_detect', 'explode', '-i', str(mp4),
                    '-f', 'null', '-'], capture_output=True, check=True, timeout=180)
    tracks = [s for s in mp['streams'] if s['codec_type'] == 'audio']
    if audio and (len(tracks) != 1 or abs(float(tracks[0]['duration'])-seconds) > .05):
        raise RuntimeError('Audio track missing or wrong duration')
    return {'gif_frames': len(frames), 'gif_duration_ms': sum(delays), 'gif_loop': meta['loop'],
            'gif_delays_ms': delays, 'mp4': video, 'audio_tracks': tracks,
            'full_decode': 'PASS', 'cfr_timestamps': 'PASS'}


def select_source_range(frames, durations, metadata, selection):
    total = len(frames)
    if selection is None:
        start, stop = 0, total
    else:
        try:
            start, stop = map(int, selection.split(':'))
        except (ValueError, AttributeError) as exc:
            raise ValueError('--source-range must be START:STOP (zero-based, stop excluded)') from exc
        if not 0 <= start < stop <= total or stop-start < 2:
            raise ValueError('--source-range needs at least 2 frames within original input')
    result = dict(metadata)
    for key in ('durations_ms', 'disposal', 'local_rectangles'):
        result[key] = metadata[key][start:stop]
    result['timing_override_frames'] = [i-start for i in metadata['timing_override_frames'] if start <= i < stop]
    result['input_total_frames'] = total
    result['selected_input_frame_indices'] = list(range(start, stop))
    return frames[start:stop], durations[start:stop], result


def run(args):
    started = time.perf_counter()
    if not math.isfinite(args.seconds) or args.seconds <= 0 or args.fps <= 0:
        raise ValueError('seconds and fps must be finite and positive')
    n = round(args.seconds*args.fps)
    if n < 2 or abs(n-args.seconds*args.fps) > 1e-7:
        raise ValueError('seconds*fps must be an integer >=2')
    gif_delays(n, args.seconds)
    for tool in ('ffmpeg', 'ffprobe'):
        if not args.inspect_only and not shutil.which(tool):
            raise RuntimeError(f'{tool} not installed')
    args.out.mkdir(parents=True, exist_ok=True)
    if list(args.out.iterdir()):
        raise ValueError('Output directory must be empty; use a new run directory to avoid stale evidence')
    frames, durations, source_meta = decode_gif(args.input, ImageColor.getrgb(args.matte), args.default_duration_ms)
    frames, durations, source_meta = select_source_range(frames, durations, source_meta, args.source_range)
    h, w = frames[0].shape[:2]
    estimated = w*h*(len(frames)+n*args.scale**2)*9
    if estimated > MAX_MEMORY:
        raise ValueError(f'Working-set estimate {estimated} exceeds 768 MiB CPU profile; reduce scale/source size')
    risks = source_risks(frames)
    source_pages = review_pages(frames, args.out, 'source_frames')
    source = {'filename': args.input.name, 'sha256': sha256(args.input), 'frames': len(frames),
              'width': w, 'height': h, 'duration_ms': sum(durations), **source_meta}
    report = {'version': VERSION, 'status': 'SOURCE_REVIEW_REQUIRED', 'source': source,
              'source_risks': risks, 'source_review_pages': source_pages,
              'source_origin': args.source_origin,
              'visual_qa': {'status': 'PENDING', 'note': 'Script never grants visual approval.'}}
    write_json(args.out/'source_report.json', report)
    if args.inspect_only:
        return report
    if risks['flags']:
        report['status'] = 'SOURCE_REJECTED'; write_json(args.out/'qa_report.json', report)
        raise ValueError('SOURCE_REJECTED: ' + ', '.join(risks['flags']))
    if not args.source_reviewed:
        raise ValueError('Source review required: inspect all source pages, then rerun in a new directory with --source-reviewed')
    flow_risks = []
    outframes, records, calls = render_frames(frames, n, durations, args.method, risk_log=flow_risks)
    if args.scale != 1:
        outframes = [cv2.resize(f, (w*args.scale, h*args.scale), interpolation=cv2.INTER_CUBIC) for f in outframes]
    dest_gif, dest_mp4 = args.out/'animation.gif', args.out/'animation.mp4'
    delays = encode_gif(outframes, dest_gif, args.seconds, args.loop, args.palette)
    command = encode_mp4(outframes, dest_mp4, args.fps, args.audio)
    verified = verify_outputs(dest_gif, dest_mp4, n, args.fps, args.seconds,
                              (w*args.scale, h*args.scale), bool(args.audio))
    decoded_output = decode_mp4_frames(dest_mp4)
    visual_sheet(decoded_output, args.out/'qa_contact_sheet.jpg')
    pages = review_pages(decoded_output, args.out, 'output_frames')
    counts = dict(Counter(r['kind'] for r in records))
    used = sorted(set(r['source_index'] for r in records if r['kind'] == 'source_sample'))
    report.update({
        'status': 'TECH_PASS_VISUAL_PENDING',
        'output': {'frames': n, 'fps': args.fps, 'seconds': args.seconds,
                   'gif_size': [w*args.scale, h*args.scale], 'verified': verified},
        'timeline': {'policy': 'cumulative-duration CFR ticks; terminal GIF delay is a hold',
                     'retime_factor': args.seconds/(sum(durations)/1000), 'mapping': records},
        'provenance': {'source_origin_asserted_not_inferred': args.source_origin,
                       'source_frame_count': len(frames), 'output_sample_kinds': counts,
                       'distinct_source_endpoints_sampled': used,
                       'upsampling_not_restoration': args.scale > 1,
                       'all_output_frames_are_postprocessed': True,
                       'no_external_paid_api': True},
        'processing': {'method': args.method, 'flow_calculations': calls, 'palette': args.palette,
                       'matte': args.matte, 'loop_requested': args.loop,
                       'ffmpeg_command': [str(x) for x in command], 'elapsed_seconds': time.perf_counter()-started,
                       'memory_estimate_bytes': estimated},
        'flow_pair_risks': flow_risks,
        'flow_flagged_source_pairs': [r['source_pair'] for r in flow_risks if r['flag']],
        'diagnostics': diagnostics(outframes), 'mp4_decoded_diagnostics': diagnostics(decoded_output),
        'output_review_pages': pages, 'review_pages_origin': 'actual decoded MP4 RGB frames',
        'runtime': {'python': platform.python_version(), 'platform': platform.platform(),
                    'numpy': np.__version__, 'opencv': cv2.__version__, 'pillow': PIL_VERSION,
                    'script_sha256': sha256(__file__),
                    'ffmpeg': subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]},
        'files': {p.name: {'sha256': sha256(p), 'bytes': p.stat().st_size}
                  for p in [dest_gif, dest_mp4, args.out/'qa_contact_sheet.jpg']},
    })
    if args.audio:
        report['audio_source'] = {'filename': args.audio.name, 'sha256': sha256(args.audio),
                                  'policy': 'trim/pad to video duration; no synthesis or lip-sync'}
    write_json(args.out/'qa_report.json', report)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--seconds', type=float, default=5.)
    p.add_argument('--fps', type=int, default=24)
    p.add_argument('--scale', type=int, choices=(1, 2, 3), default=1, help='Display resize, not detail restoration')
    p.add_argument('--method', choices=('flow', 'blend'), default='flow')
    p.add_argument('--palette', choices=('global', 'per-frame'), default='global')
    p.add_argument('--matte', default='#000000', help='Explicit transparent-source composite color')
    p.add_argument('--default-duration-ms', type=int)
    p.add_argument('--inspect-only', action='store_true')
    p.add_argument('--source-reviewed', action='store_true', help='Operator has actually inspected all source frames')
    p.add_argument('--source-range', help='Explicit START:STOP subclip; keeps original input hash and indices')
    p.add_argument('--source-origin', choices=('unknown', 'gpt-native', 'synthetic-fixture'), default='unknown')
    p.add_argument('--loop', action='store_true', help='Only request after separately reviewing end/start seam')
    p.add_argument('--audio', type=Path, help='Optional existing audio; trimmed/padded, no TTS generation')
    args = p.parse_args()
    try:
        report = run(args)
        print(json.dumps({'status': report['status'], 'out': str(args.out)}, ensure_ascii=False))
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'FAILED', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
