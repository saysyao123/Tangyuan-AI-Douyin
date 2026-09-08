import argparse
import os
import sys

import cv2
import numpy as np
import torch

sys.path.insert(0, os.path.abspath('Depth-Anything-V2'))
from depth_anything_v2.dpt import DepthAnythingV2


def normalize_with_ema(depth, state, alpha=0.10):
    lo = float(np.percentile(depth, 1.0))
    hi = float(np.percentile(depth, 99.0))
    if state['lo'] is None:
        state['lo'], state['hi'] = lo, hi
    else:
        state['lo'] = (1 - alpha) * state['lo'] + alpha * lo
        state['hi'] = (1 - alpha) * state['hi'] + alpha * hi
    denom = max(state['hi'] - state['lo'], 1e-6)
    return np.clip((depth - state['lo']) / denom, 0.0, 1.0).astype(np.float32)


def warp_previous(prev_depth, curr_gray, prev_gray):
    # Backward flow: for every current pixel, find where it came from in previous frame.
    small_w, small_h = 180, 320
    cg = cv2.resize(curr_gray, (small_w, small_h), interpolation=cv2.INTER_AREA)
    pg = cv2.resize(prev_gray, (small_w, small_h), interpolation=cv2.INTER_AREA)
    flow = cv2.calcOpticalFlowFarneback(cg, pg, None, 0.5, 3, 11, 3, 5, 1.1, 0)
    yy, xx = np.mgrid[0:small_h, 0:small_w].astype(np.float32)
    map_x = xx + flow[..., 0]
    map_y = yy + flow[..., 1]
    pd = cv2.resize(prev_depth, (small_w, small_h), interpolation=cv2.INTER_AREA)
    warped = cv2.remap(pd, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return warped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--checkpoint', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--input-size', type=int, default=518)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    device = 'cpu'
    torch.set_num_threads(max(1, os.cpu_count() or 2))

    cfg = {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]}
    model = DepthAnythingV2(**cfg)
    model.load_state_dict(torch.load(args.checkpoint, map_location='cpu'))
    model = model.to(device).eval()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise RuntimeError(f'Cannot open input: {args.input}')

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    raw_path = os.path.join(args.outdir, 'depth_anything_v2_raw.mp4')
    stable_path = os.path.join(args.outdir, 'depth_anything_v2_temporal.mp4')
    compare_path = os.path.join(args.outdir, 'original_vs_depth_temporal.mp4')
    raw_out = cv2.VideoWriter(raw_path, fourcc, fps, (w, h))
    stable_out = cv2.VideoWriter(stable_path, fourcc, fps, (w, h))
    compare_out = cv2.VideoWriter(compare_path, fourcc, fps, (w * 2, h))

    state = {'lo': None, 'hi': None}
    prev_gray = None
    prev_stable = None
    idx = 0

    with torch.inference_mode():
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            idx += 1
            depth = model.infer_image(frame, args.input_size).astype(np.float32)
            norm = normalize_with_ema(depth, state)

            # Fine-detail raw depth.
            raw_u8 = np.clip(norm * 255.0, 0, 255).astype(np.uint8)
            raw_bgr = cv2.cvtColor(raw_u8, cv2.COLOR_GRAY2BGR)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_stable is None:
                stable = norm
            else:
                warped_small = warp_previous(prev_stable, gray, prev_gray)
                warped = cv2.resize(warped_small, (w, h), interpolation=cv2.INTER_LINEAR)
                # Keep current-frame detail dominant; use flow-warped history only to suppress flicker.
                stable = 0.82 * norm + 0.18 * warped
                # Very light edge-preserving cleanup.
                stable = cv2.bilateralFilter(stable.astype(np.float32), 5, 0.04, 3)

            stable_u8 = np.clip(stable * 255.0, 0, 255).astype(np.uint8)
            stable_bgr = cv2.cvtColor(stable_u8, cv2.COLOR_GRAY2BGR)

            raw_out.write(raw_bgr)
            stable_out.write(stable_bgr)
            compare_out.write(cv2.hconcat([frame, stable_bgr]))

            prev_gray = gray
            prev_stable = stable

            if idx == 1 or idx % 30 == 0 or idx == total:
                print(f'processed {idx}/{total}', flush=True)

    cap.release()
    raw_out.release()
    stable_out.release()
    compare_out.release()
    print('DONE', raw_path, stable_path, compare_path, flush=True)


if __name__ == '__main__':
    main()
