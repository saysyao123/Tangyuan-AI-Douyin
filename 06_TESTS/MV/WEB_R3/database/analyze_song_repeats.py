#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

DATA_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = DATA_DIR / 'analysis'
TZ = ZoneInfo('Asia/Manila')


def read_csv(name: str):
    with (DATA_DIR / name).open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def parse_dt(v: str):
    try:
        return datetime.strptime(v, '%Y-%m-%d %H:%M:%S').replace(tzinfo=TZ)
    except Exception:
        return None


def main() -> int:
    now = datetime.now(TZ)
    accounts = {r['account_id']: r for r in read_csv('accounts.csv')}
    works = {r['aweme_id']: r for r in read_csv('works.csv')}
    norms = {r['aweme_id']: r for r in read_csv('song_normalization.csv')}

    # Coverage / freshness gate. A trend database cannot call missing newest-edge data "zero".
    by_account_times = defaultdict(list)
    for w in works.values():
        dt = parse_dt(w.get('create_time', ''))
        if dt:
            by_account_times[w['account_id']].append(dt)

    coverage = []
    freshness_fail = []
    for account_id, a in accounts.items():
        times = by_account_times.get(account_id, [])
        newest = max(times) if times else None
        age_hours = (now - newest).total_seconds() / 3600 if newest else None
        trend_weight = float(a.get('trend_weight') or 0)
        threshold_hours = 72 if trend_weight >= 0.65 else 168
        fresh = bool(newest and age_hours <= threshold_hours)
        row = {
            'account_id': account_id,
            'nickname': a.get('current_nickname',''),
            'trend_weight': trend_weight,
            'window_15d_complete': int(a.get('window_15d_complete') or 0),
            'newest_work': newest.isoformat(timespec='seconds') if newest else '',
            'newest_age_hours': round(age_hours, 1) if age_hours is not None else None,
            'freshness_threshold_hours': threshold_hours,
            'latest_edge_fresh': fresh,
        }
        coverage.append(row)
        if trend_weight >= 0.65 and not fresh:
            freshness_fail.append(account_id)

    eligible = []
    for aweme_id, n in norms.items():
        try:
            conf = float(n.get('confidence') or 0)
        except ValueError:
            conf = 0
        if n.get('normalization_status') != 'AUTO_HIGH' or conf < 0.85 or not n.get('song_family'):
            continue
        w = works.get(aweme_id)
        if not w:
            continue
        eligible.append((w, n))

    families = defaultdict(list)
    for w, n in eligible:
        families[n['song_family']].append((w, n))

    rows = []
    anchor_7d = now - timedelta(days=7)
    anchor_72h = now - timedelta(hours=72)
    for family, items in families.items():
        account_ids = sorted({w['account_id'] for w, _ in items})
        dts = [parse_dt(w['create_time']) for w, _ in items if parse_dt(w['create_time'])]
        versions = sorted({n.get('audio_version','') for _, n in items if n.get('audio_version')})
        radar_weight = sum(float(accounts[a].get('trend_weight') or 0) for a in account_ids)
        visual_count = sum(1 for a in account_ids if 'VISUAL' in accounts[a].get('role_category',''))
        current_7d_accounts = {w['account_id'] for w, _ in items if (dt := parse_dt(w['create_time'])) and dt >= anchor_7d}
        current_72h_accounts = {w['account_id'] for w, _ in items if (dt := parse_dt(w['create_time'])) and dt >= anchor_72h}
        latest = max(dts) if dts else None
        earliest = min(dts) if dts else None
        # Concentration around the song's latest observed appearance; useful only as an exploratory lower-bound metric.
        local72 = {w['account_id'] for w, _ in items if latest and (dt := parse_dt(w['create_time'])) and dt >= latest - timedelta(hours=72)}
        rows.append({
            'song_family': family,
            'distinct_account_repeat_15d_lower_bound': len(account_ids),
            'distinct_account_repeat_7d_current': len(current_7d_accounts),
            'distinct_account_repeat_72h_current': len(current_72h_accounts),
            'music_radar_weighted_repeat': round(radar_weight, 2),
            'visual_account_repeat': visual_count,
            'local_72h_account_concentration': len(local72),
            'audio_version_count': len(versions),
            'audio_versions': ' || '.join(versions),
            'first_observed_work_time': earliest.isoformat(timespec='seconds') if earliest else '',
            'latest_observed_work_time': latest.isoformat(timespec='seconds') if latest else '',
            'account_ids': '|'.join(account_ids),
            'work_count': len(items),
        })
    rows.sort(key=lambda r: (-r['distinct_account_repeat_15d_lower_bound'], -r['music_radar_weighted_repeat'], r['song_family']))

    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else [
        'song_family','distinct_account_repeat_15d_lower_bound','distinct_account_repeat_7d_current',
        'distinct_account_repeat_72h_current','music_radar_weighted_repeat','visual_account_repeat',
        'local_72h_account_concentration','audio_version_count','audio_versions','first_observed_work_time',
        'latest_observed_work_time','account_ids','work_count'
    ]
    with (ANALYSIS_DIR / 'song_repeat_analysis.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(rows)
    (ANALYSIS_DIR / 'coverage.json').write_text(json.dumps({
        'observed_at': now.isoformat(timespec='seconds'),
        'coverage': coverage,
        'high_trend_latest_edge_fail_accounts': freshness_fail,
        'latest_edge_gate_pass': len(freshness_fail) == 0,
        'note': 'Current repeats are lower bounds until latest-edge freshness and all requested 15d windows are closed.'
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    repeated = [r for r in rows if r['distinct_account_repeat_15d_lower_bound'] >= 2]
    md = [
        '# WEB R3｜Database Song Analysis v1', '',
        f'- observed_at: `{now.isoformat(timespec="seconds")}`',
        f'- eligible normalized works: `{len(eligible)}` / `{len(works)}`',
        f'- repeated SONG_FAMILY (2+ accounts): `{len(repeated)}`',
        f'- latest-edge gate: `{"PASS" if not freshness_fail else "FAIL"}`',
        f'- stale/high-trend accounts: `{", ".join(freshness_fail) if freshness_fail else "none"}`', '',
        '## Interpretation', '',
        'This report is database-only. 15-day repeat values are lower bounds while any account is incomplete, and no current 7-day/72h trend conclusion is allowed while the latest-edge gate fails.', '',
        '## Repeated song families｜lower bound', '',
        '| SONG_FAMILY | accounts/15d | weighted radar | visual overlap | local72h | versions | latest observed |',
        '|---|---:|---:|---:|---:|---:|---|',
    ]
    for r in repeated:
        md.append(f"| {r['song_family']} | {r['distinct_account_repeat_15d_lower_bound']} | {r['music_radar_weighted_repeat']} | {r['visual_account_repeat']} | {r['local_72h_account_concentration']} | {r['audio_version_count']} | {r['latest_observed_work_time']} |")
    md += ['', '## Gate', '', 'HG01 remains blocked if either:', '- any required 15-day core window is not closed;', '- high-trend account latest-edge freshness is not verified.', '']
    (ANALYSIS_DIR / 'R3_DATABASE_SONG_ANALYSIS_v1.md').write_text('\n'.join(md), encoding='utf-8')

    print({
        'works': len(works), 'eligible_normalized_works': len(eligible),
        'repeated_families': len(repeated), 'latest_edge_gate_pass': not freshness_fail,
        'freshness_fail_accounts': freshness_fail,
    })
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
