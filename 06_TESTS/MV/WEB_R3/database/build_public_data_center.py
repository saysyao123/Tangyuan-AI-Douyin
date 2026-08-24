#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Manila")
DB_DIR = Path(__file__).resolve().parent
R3_DIR = DB_DIR.parent
SNAP_DIR = DB_DIR / "public_observed_30d"
CENTER = DB_DIR / "data_center"

GENERIC_TAGS = {
    '音乐推荐','音乐分享','好听的音乐分享','音乐种草计划','音乐种草激励计划','创作者中心','创作灵感',
    '翻唱','翻唱歌曲分享','翻唱作品分享','经典歌曲翻唱','热歌榜翻唱','新歌推荐','原创音乐','原创歌曲推荐',
    '炙热计划','抖音热歌','汽水音乐app','歌手live','音乐现场','宝藏女歌手','失恋','emo','破碎感','暗黑系',
    '氛围感','治愈','治愈系','自由','夏天','夏日','星空','星轨','银河','冰岛','冰岛黑沙滩','海边','海',
    'inmyfeeling','inmyfeelings','旅行推荐官','一站式ai创作工作台','ai视频生产级时代','即梦ai','抖音ai创作大赛',
    '中式美学','中式意境','国风','古风','油画风格','极端天气','infp','情侣','异地恋','宝妈','宝爸带娃',
    '火乐烁','泡泡与茶','黑米与糖豆','佩佩治愈ai','xiangjishi','鱼子西','张宇宙','大溪地','天宫',
}
MUSIC_CONTEXT_TAGS = {
    '音乐推荐','音乐分享','音乐种草计划','音乐种草激励计划','新歌推荐','原创音乐','原创歌曲推荐',
    '翻唱','热歌榜翻唱','好听的音乐分享'
}
ALIASES = {
    '如果风会替我说话林叙': ('如果风会替我说话', None),
    '有几次想你了林叙': ('有几次想你了', None),
    '爱让人脑袋空空电音版': ('爱让人脑袋空空', 'ELECTRONIC'),
    '沈园外电音remix': ('沈园外', 'ELECTRONIC_REMIX'),
    '大眼仔版做她的大地别做她的天': ('做她的大地别做她的天', 'R&B'),
    '杀破狼rnb氛围版': ('杀破狼', 'R&B'),
    '歌曲summerlove爱在盛夏': ('Summer Love 爱在盛夏', None),
    'summerlove爱在盛夏': ('Summer Love 爱在盛夏', None),
    'icantlove我无法去爱': ('我无法去爱', None),
    '离人赋电音版赵兮月版离人赋': ('离人赋', 'ELECTRONIC'),
    '锁电音版': ('锁', 'ELECTRONIC'),
    '张颜齐姚晓棠忘了吗忘了吧': ('忘了吗忘了吧', None),
    'almostalmost差一点心动': ('差一点心动', None),
}
VERSION_PATTERNS = [
    ('电音', 'ELECTRONIC'), ('remix', 'REMIX'), ('r&b', 'R&B'), ('rnb', 'R&B'),
    ('古筝', 'INSTRUMENTAL_GUZHENG'), ('剪辑版', 'EDIT_EXCERPT'), ('片段', 'EDIT_EXCERPT'),
    ('翻唱', 'COVER'), ('粤语', 'CANTONESE'),
]

WORK_FIELDS = [
    'aweme_id','account_id','case_id','nickname','create_time','work_url','caption',
    'music_title_raw','music_author_raw','hashtags','first_observed_at','last_observed_at'
]
METRIC_FIELDS = [
    'aweme_id','observed_at','digg_count','comment_count','share_count','collect_count','play_count'
]
NORM_FIELDS = [
    'aweme_id','song_family','audio_version','normalization_status','confidence','evidence_method','reviewed_at','notes'
]
CANDIDATE_FIELDS = [
    'song_family','distinct_accounts_30d','distinct_accounts_last15d','weighted_repeat_30d','weighted_repeat_last15d',
    'best_72h_distinct_accounts','visual_overlap_accounts','audio_version_count','work_count',
    'first_observed_work_time','latest_observed_work_time','evidence_grade'
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, '') for k in fields})


def parse_dt(value: Any) -> datetime | None:
    text = str(value or '').strip()
    for fmt in ('%Y-%m-%d %H:%M:%S','%Y-%m-%dT%H:%M:%S%z','%Y-%m-%dT%H:%M:%S'):
        try:
            dt = datetime.strptime(text, fmt)
            return dt.astimezone(TZ) if dt.tzinfo else dt.replace(tzinfo=TZ)
        except ValueError:
            pass
    return None


def norm(text: str) -> str:
    return unicodedata.normalize('NFKC', str(text or '')).strip().lstrip('#').strip()


def compact(text: str) -> str:
    return re.sub(r'\s+', '', norm(text)).lower()


def clean_family(value: str) -> tuple[str, str | None]:
    value = norm(value)
    c = compact(value)
    if c in ALIASES:
        return ALIASES[c]
    if c.startswith('歌曲') and len(value) > 2:
        value = value[2:].strip(); c = compact(value)
        if c in ALIASES:
            return ALIASES[c]
    version = None
    low = value.lower()
    for needle, label in VERSION_PATTERNS:
        if needle in low:
            version = label if version is None else f'{version}+{label}'
    value = re.sub(r'[（(](?:剪辑版\d*|片段|副歌|氛围片段|r&b|rnb|电音版|古筝版)[）)]', '', value, flags=re.I)
    value = re.sub(r'[（(](?:电音版)[）)].*$', '', value, flags=re.I)
    value = re.sub(r'[-—_](?:副歌|片段).*$', '', value, flags=re.I)
    value = re.sub(r'(?:电音版|电音remix|rnb氛围版)$', '', value, flags=re.I)
    return value.strip(' -—_·'), version


def plausible_tag(tag: str) -> bool:
    t = compact(tag)
    generic = {compact(x) for x in GENERIC_TAGS}
    if not t or t in generic or len(t) < 2 or len(t) > 26:
        return False
    if t.startswith(('pavoai','ai','抖音','旅行','创作者','音乐种草','inmy','dj')):
        return False
    return True


def infer_version(text: str, hashtags: list[str], raw_title: str, raw_author: str) -> str:
    joined = ' '.join([text, raw_title, *hashtags]).lower()
    labels = []
    for needle, label in VERSION_PATTERNS:
        if needle in joined and label not in labels:
            labels.append(label)
    if raw_title.startswith('@') and raw_author:
        labels.append(f'DOUYIN_ORIGINAL_SOUND:{raw_author}')
    elif raw_title and raw_title != '模板音乐':
        labels.append('NAMED_AUDIO')
    return '+'.join(labels) if labels else 'UNKNOWN_VERSION'


def normalize_work(row: dict[str, str], role_category: str, reviewed_at: str) -> dict[str, Any]:
    aid = row['aweme_id']
    caption = norm(row.get('caption',''))
    body = caption.split('#',1)[0].strip()
    raw_title = norm(row.get('music_title_raw',''))
    raw_author = norm(row.get('music_author_raw',''))
    hashtags = [norm(x) for x in str(row.get('hashtags','')).split('|') if norm(x)]

    def result(family='', version='', status='UNRESOLVED', confidence=0.0, method='NO_RELIABLE_SONG_IDENTITY', notes=''):
        return {'aweme_id':aid,'song_family':family,'audio_version':version,'normalization_status':status,
                'confidence':confidence,'evidence_method':method,'reviewed_at':reviewed_at,'notes':notes}

    for tag in hashtags:
        if compact(tag).startswith('歌曲') and len(norm(tag)) > 2:
            family, alias_version = clean_family(tag)
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version: version = f'{alias_version}+{version}'
            return result(family, version, 'AUTO_HIGH', 0.98, 'EXPLICIT_SONG_HASHTAG', f'source_tag={tag}')

    if raw_title and raw_title != '模板音乐' and not raw_title.startswith('@'):
        family, title_version = clean_family(raw_title)
        if family:
            version = infer_version(raw_title, hashtags, raw_title, raw_author)
            if title_version and title_version not in version: version = f'{title_version}+{version}'
            return result(family, version, 'AUTO_HIGH', 0.95, 'NAMED_MUSIC_METADATA', f'raw_title={raw_title}')

    plausible = []
    for tag in hashtags:
        if plausible_tag(tag):
            family, alias_version = clean_family(tag)
            if family: plausible.append((tag,family,alias_version))

    for tag, family, alias_version in plausible:
        if body and (compact(tag) in compact(body) or compact(family) in compact(body)):
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version: version = f'{alias_version}+{version}'
            return result(family, version, 'AUTO_HIGH', 0.90, 'BODY_HASHTAG_CORROBORATION', f'body_tag={tag}')

    is_music_role = role_category.startswith('MUSIC_') or role_category == 'EDIT_LYRIC_MUSIC'
    context = {compact(x) for x in MUSIC_CONTEXT_TAGS}
    if is_music_role and any(compact(t) in context for t in hashtags) and plausible:
        tag, family, alias_version = plausible[0]
        version = infer_version(tag, hashtags, raw_title, raw_author)
        if alias_version and alias_version not in version: version = f'{alias_version}+{version}'
        return result(family, version, 'AUTO_HIGH', 0.87, 'MUSIC_ACCOUNT_CONTEXT_HASHTAG', f'context_tag={tag}')

    if plausible:
        tag, family, alias_version = plausible[0]
        version = infer_version(tag, hashtags, raw_title, raw_author)
        if alias_version and alias_version not in version: version = f'{alias_version}+{version}'
        return result(family, version, 'REVIEW_REQUIRED', 0.65, 'PLAUSIBLE_HASHTAG_ONLY', f'candidate_tag={tag}')

    return result(version=infer_version('', hashtags, raw_title, raw_author))


def best_72h(rows: list[dict[str, Any]]) -> int:
    events = sorted((row['dt'], row['account_id']) for row in rows)
    best = 0
    for i, (start, _) in enumerate(events):
        end = start + timedelta(hours=72)
        best = max(best, len({acc for dt,acc in events[i:] if dt <= end}))
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot-dir', default=str(SNAP_DIR))
    args = parser.parse_args()
    snap = Path(args.snapshot_dir)
    summary = json.loads((snap / 'summary.json').read_text(encoding='utf-8'))
    fresh = read_csv(snap / 'works_observed_30d.csv')
    coverage = read_csv(snap / 'coverage.csv')
    accounts = read_csv(DB_DIR / 'accounts.csv')
    account_by_id = {a['account_id']:a for a in accounts}

    CENTER.mkdir(parents=True, exist_ok=True)
    observed_at = datetime.now(TZ).isoformat(timespec='seconds')
    anchor = parse_dt(summary['anchor_latest_observed'])
    window_start = parse_dt(summary['window_start'])
    window_end = parse_dt(summary['window_end_exclusive'])
    if not anchor or not window_start or not window_end:
        raise RuntimeError('snapshot summary contains invalid dates')

    previous = read_csv(CENTER / 'observed_works.csv')
    by_id = {r['aweme_id']:r for r in previous if r.get('aweme_id')}
    for row in fresh:
        aid = row['aweme_id']
        existing = by_id.get(aid, {})
        by_id[aid] = {
            'aweme_id':aid,'account_id':row['account_id'],'case_id':row.get('case_id',''),
            'nickname':row.get('nickname',''),'create_time':row.get('create_time',''),
            'work_url':row.get('work_url','') or f'https://www.douyin.com/video/{aid}',
            'caption':row.get('caption',''),'music_title_raw':row.get('music_title_raw',''),
            'music_author_raw':row.get('music_author_raw',''),'hashtags':row.get('hashtags',''),
            'first_observed_at':existing.get('first_observed_at') or observed_at,
            'last_observed_at':observed_at,
        }
    all_works = sorted(by_id.values(), key=lambda r:(r.get('create_time',''),r.get('account_id','')), reverse=True)
    write_csv(CENTER / 'observed_works.csv', all_works, WORK_FIELDS)

    existing_metrics = read_csv(CENTER / 'observed_metrics.csv')
    metric_keys = {(r.get('aweme_id',''),r.get('observed_at','')) for r in existing_metrics}
    new_metrics = []
    for row in fresh:
        key=(row['aweme_id'],observed_at)
        if key in metric_keys: continue
        new_metrics.append({
            'aweme_id':row['aweme_id'],'observed_at':observed_at,'digg_count':row.get('digg_count',0),
            'comment_count':row.get('comment_count',0),'share_count':row.get('share_count',0),
            'collect_count':row.get('collect_count',0),'play_count':row.get('play_count',0),
        })
    write_csv(CENTER / 'observed_metrics.csv', existing_metrics + new_metrics, METRIC_FIELDS)

    snapshots = read_csv(CENTER / 'snapshots.csv')
    snapshot_id = f"OBS_{datetime.now(TZ).strftime('%Y%m%d_%H%M%S')}"
    snapshots.append({
        'snapshot_id':snapshot_id,'observed_at':observed_at,'anchor_latest_observed':summary['anchor_latest_observed'],
        'window_start':summary['window_start'],'window_end_exclusive':summary['window_end_exclusive'],
        'observable_rows':len(fresh),'cumulative_unique_works':len(all_works),'source':summary.get('source',''),
        'mode':'PUBLIC_OBSERVED_30D','semantics':'POSITIVE_EVIDENCE_ONLY'
    })
    snapshot_fields=['snapshot_id','observed_at','anchor_latest_observed','window_start','window_end_exclusive','observable_rows','cumulative_unique_works','source','mode','semantics']
    write_csv(CENTER / 'snapshots.csv', snapshots, snapshot_fields)
    write_csv(CENTER / 'coverage_latest.csv', coverage, ['case_id','account_id','nickname','returned','newest','oldest','has_more','error'])

    reviewed_at = observed_at
    norms = [normalize_work(r, account_by_id.get(r['account_id'],{}).get('role_category',''), reviewed_at) for r in all_works]
    write_csv(CENTER / 'song_normalization.csv', norms, NORM_FIELDS)
    norm_by_id = {n['aweme_id']:n for n in norms}

    # Analysis uses the current rolling 30-day anchor window. Older cumulative observations remain stored but do not affect ranking.
    current = []
    for row in all_works:
        dt = parse_dt(row.get('create_time'))
        n = norm_by_id.get(row['aweme_id'])
        if not dt or not n or not (window_start <= dt < window_end): continue
        if n['normalization_status'] != 'AUTO_HIGH' or float(n['confidence'] or 0) < 0.85 or not n['song_family']: continue
        current.append({**row,'dt':dt,'song_family':n['song_family'],'audio_version':n['audio_version']})

    by_family: dict[str,list[dict[str,Any]]] = defaultdict(list)
    for row in current: by_family[row['song_family']].append(row)
    last15 = window_end - timedelta(days=15)
    candidates=[]; evidence=[]
    for family, rows in by_family.items():
        acc30=sorted({r['account_id'] for r in rows})
        if len(acc30)<2: continue
        rows15=[r for r in rows if r['dt']>=last15]
        acc15=sorted({r['account_id'] for r in rows15})
        weighted30=sum(float(account_by_id[a].get('trend_weight') or 0) for a in acc30)
        weighted15=sum(float(account_by_id[a].get('trend_weight') or 0) for a in acc15)
        visual=sum(1 for a in acc30 if float(account_by_id[a].get('visual_weight') or 0)>=0.8)
        versions=sorted({r['audio_version'] for r in rows if r.get('audio_version')})
        first=min(r['dt'] for r in rows); latest=max(r['dt'] for r in rows)
        grade='STRONG' if len(acc30)>=3 else 'CONFIRMED_REPEAT'
        candidates.append({
            'song_family':family,'distinct_accounts_30d':len(acc30),'distinct_accounts_last15d':len(acc15),
            'weighted_repeat_30d':round(weighted30,3),'weighted_repeat_last15d':round(weighted15,3),
            'best_72h_distinct_accounts':best_72h(rows),'visual_overlap_accounts':visual,
            'audio_version_count':len(versions),'work_count':len(rows),
            'first_observed_work_time':first.strftime('%Y-%m-%d %H:%M:%S'),
            'latest_observed_work_time':latest.strftime('%Y-%m-%d %H:%M:%S'),'evidence_grade':grade,
        })
        works_ev=[]
        for r in sorted(rows,key=lambda x:x['dt'],reverse=True):
            a=account_by_id[r['account_id']]
            works_ev.append({
                'account_id':r['account_id'],'nickname':a.get('current_nickname',''),'douyin_id':a.get('douyin_id',''),
                'create_time':r['create_time'],'aweme_id':r['aweme_id'],'work_url':r['work_url'],
                'caption':r['caption'],'audio_version':r.get('audio_version','')
            })
        evidence.append({'song_family':family,'evidence_grade':grade,'distinct_accounts':len(acc30),'works':works_ev})
    candidates.sort(key=lambda r:(r['distinct_accounts_last15d'],r['weighted_repeat_last15d'],r['distinct_accounts_30d'],r['best_72h_distinct_accounts'],r['weighted_repeat_30d']),reverse=True)
    write_csv(CENTER / 'song_repeat_candidates.csv', candidates, CANDIDATE_FIELDS)
    (CENTER / 'direct_douyin_evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    counts=defaultdict(int)
    for n in norms: counts[n['normalization_status']]+=1
    manifest={
        'version':'DATA_CENTER_v1','mode':'PUBLIC_OBSERVED_30D','semantics':'POSITIVE_EVIDENCE_ONLY',
        'observed_at':observed_at,'anchor_latest_observed':summary['anchor_latest_observed'],
        'rolling_window_start':summary['window_start'],'rolling_window_end_exclusive':summary['window_end_exclusive'],
        'locked_core_accounts':9,'fresh_snapshot_rows':len(fresh),'cumulative_unique_works':len(all_works),
        'current_window_auto_high_works':len(current),'repeated_song_families':len(candidates),
        'normalization_status_counts':dict(counts),'refresh_cadence_days':15,
        'next_refresh_due_approx':(datetime.now(TZ)+timedelta(days=15)).date().isoformat(),
        'absence_semantics':'UNKNOWN_NOT_NEGATIVE','hg01_evidence_ready':len(candidates)>0,
    }
    (CENTER / 'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    lines=[
        '# WEB R3｜Douyin Data Center v1','',
        f"- Mode: `PUBLIC_OBSERVED_30D / POSITIVE_EVIDENCE_ONLY`",
        f"- Anchor: `{manifest['anchor_latest_observed']}`",
        f"- Rolling window: `{manifest['rolling_window_start']}` → `{manifest['rolling_window_end_exclusive']}`",
        f"- Core accounts: `{manifest['locked_core_accounts']}`",
        f"- Fresh snapshot rows: `{manifest['fresh_snapshot_rows']}`",
        f"- Cumulative unique observed works: `{manifest['cumulative_unique_works']}`",
        f"- AUTO_HIGH works in current window: `{manifest['current_window_auto_high_works']}`",
        f"- Repeated SONG_FAMILY: `{manifest['repeated_song_families']}`",
        f"- Refresh cadence: every `{manifest['refresh_cadence_days']}` days",'',
        '## Evidence semantics','',
        '- Observed same-song use across independent core accounts is valid positive evidence.',
        '- Missing works/accounts are UNKNOWN, never interpreted as a negative signal.',
        '- Current ranking is an observed-repeat ranking, not a complete-platform popularity ranking.','',
        '## Top observed repeats','',
        '| SONG_FAMILY | acc/15d | acc/30d | weighted/15d | best72h | visual overlap | grade |',
        '|---|---:|---:|---:|---:|---:|---|'
    ]
    for r in candidates[:20]:
        lines.append(f"| {r['song_family']} | {r['distinct_accounts_last15d']} | {r['distinct_accounts_30d']} | {r['weighted_repeat_last15d']} | {r['best_72h_distinct_accounts']} | {r['visual_overlap_accounts']} | {r['evidence_grade']} |")
    lines += ['', '## Canonical files','',
              '- `observed_works.csv` — cumulative observed work facts',
              '- `observed_metrics.csv` — engagement snapshots',
              '- `snapshots.csv` — every refresh receipt',
              '- `coverage_latest.csv` — latest public page coverage per account',
              '- `song_normalization.csv` — work-level SONG_FAMILY mapping',
              '- `song_repeat_candidates.csv` — positive cross-account repeat ranking',
              '- `direct_douyin_evidence.json` — exact account/work links for HG01',
              '- `manifest.json` — machine-readable state','']
    (CENTER / 'DATA_CENTER_STATUS.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
