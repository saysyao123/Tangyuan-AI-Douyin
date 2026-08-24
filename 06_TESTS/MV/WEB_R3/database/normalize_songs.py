#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DATA_DIR = Path(__file__).resolve().parent

GENERIC_TAGS = {
    '音乐推荐','音乐分享','好听的音乐分享','音乐种草计划','音乐种草激励计划','创作者中心','创作灵感',
    '翻唱','翻唱歌曲分享','翻唱作品分享','经典歌曲翻唱','热歌榜翻唱','新歌推荐','原创音乐','原创歌曲推荐',
    '炙热计划','抖音热歌','汽水音乐app','歌手live','音乐现场','宝藏女歌手','失恋','emo','破碎感','暗黑系',
    '氛围感','治愈','治愈系','自由','夏天','夏日','星空','星轨','银河','冰岛','冰岛黑沙滩','海边','海',
    'inmyfeeling','inmyfeelings','旅行推荐官','一站式ai创作工作台','ai视频生产级时代','即梦ai','抖音ai创作大赛',
    '中式美学','中式意境','国风','古风','油画风格','极端天气','infp','情侣','异地恋','宝妈','宝爸带娃',
    '火乐烁','泡泡与茶','黑米与糖豆','佩佩治愈ai','xiangjishi','鱼子西','张宇宙','大溪地','天宫',
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

MUSIC_ROLE_PREFIXES = ('MUSIC_', 'EDIT_LYRIC_MUSIC')
MUSIC_CONTEXT_TAGS = {'音乐推荐','音乐分享','音乐种草计划','音乐种草激励计划','新歌推荐','原创音乐','原创歌曲推荐','翻唱','热歌榜翻唱','好听的音乐分享'}


def norm(text: str) -> str:
    return unicodedata.normalize('NFKC', str(text or '')).strip().lstrip('#').strip()


def compact(text: str) -> str:
    return re.sub(r'\s+', '', norm(text)).lower()


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


def clean_family(value: str) -> tuple[str, str | None]:
    value = norm(value)
    c = compact(value)
    if c in ALIASES:
        return ALIASES[c]
    if c.startswith('歌曲') and len(value) > 2:
        value = value[2:].strip()
        c = compact(value)
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
    value = value.strip(' -—_·')
    return value, version


def plausible_tag(tag: str) -> bool:
    t = compact(tag)
    if not t or t in {compact(x) for x in GENERIC_TAGS}:
        return False
    if len(t) < 2 or len(t) > 26:
        return False
    if t.startswith(('pavoai','ai','抖音','旅行','创作者','音乐种草','inmy','dj')):
        return False
    return True


def result(aweme_id, family, version, status, confidence, method, reviewed_at, notes=''):
    return {
        'aweme_id': aweme_id, 'song_family': family, 'audio_version': version,
        'normalization_status': status, 'confidence': confidence,
        'evidence_method': method, 'reviewed_at': reviewed_at, 'notes': notes,
    }


def normalize_row(row: dict[str, str], role_category: str, reviewed_at: str):
    aweme_id = row['aweme_id']
    caption = norm(row.get('caption', ''))
    body = caption.split('#', 1)[0].strip()
    raw_title = norm(row.get('music_title_raw', ''))
    raw_author = norm(row.get('music_author_raw', ''))
    hashtags = [norm(x) for x in str(row.get('hashtags', '')).split('|') if norm(x)]

    # 1. Explicit '#歌曲X' is strongest work-level evidence.
    for tag in hashtags:
        if compact(tag).startswith('歌曲') and len(norm(tag)) > 2:
            family, alias_version = clean_family(tag)
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version:
                version = f'{alias_version}+{version}'
            return result(aweme_id, family, version, 'AUTO_HIGH', 0.98, 'EXPLICIT_SONG_HASHTAG', reviewed_at, f'source_tag={tag}')

    # 2. Non-generic named audio metadata is strong evidence.
    if raw_title and raw_title != '模板音乐' and not raw_title.startswith('@'):
        family, title_version = clean_family(raw_title)
        if family:
            version = infer_version(raw_title, hashtags, raw_title, raw_author)
            if title_version and title_version not in version:
                version = f'{title_version}+{version}'
            return result(aweme_id, family, version, 'AUTO_HIGH', 0.95, 'NAMED_MUSIC_METADATA', reviewed_at, f'raw_title={raw_title}')

    plausible = []
    for tag in hashtags:
        if plausible_tag(tag):
            family, alias_version = clean_family(tag)
            if family:
                plausible.append((tag, family, alias_version))

    # 3. Caption BODY corroboration only. Hashtags appended to caption do NOT count as corroboration.
    for tag, family, alias_version in plausible:
        if body and (compact(tag) in compact(body) or compact(family) in compact(body)):
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version:
                version = f'{alias_version}+{version}'
            return result(aweme_id, family, version, 'AUTO_HIGH', 0.90, 'BODY_HASHTAG_CORROBORATION', reviewed_at, f'body_tag={tag}')

    # 4. Active music accounts often put the song name only in the first useful hashtag.
    # Require explicit music-post context; visual accounts do not get this shortcut.
    is_music_role = role_category.startswith(MUSIC_ROLE_PREFIXES) if isinstance(MUSIC_ROLE_PREFIXES, str) else (role_category.startswith('MUSIC_') or role_category == 'EDIT_LYRIC_MUSIC')
    has_music_context = any(compact(t) in {compact(x) for x in MUSIC_CONTEXT_TAGS} for t in hashtags)
    if is_music_role and has_music_context and plausible:
        tag, family, alias_version = plausible[0]
        version = infer_version(tag, hashtags, raw_title, raw_author)
        if alias_version and alias_version not in version:
            version = f'{alias_version}+{version}'
        return result(aweme_id, family, version, 'AUTO_HIGH', 0.87, 'MUSIC_ACCOUNT_CONTEXT_HASHTAG', reviewed_at, f'context_tag={tag}')

    # 5. Everything else is a review lead, not a primary trend fact.
    if plausible:
        tag, family, alias_version = plausible[0]
        version = infer_version(tag, hashtags, raw_title, raw_author)
        if alias_version and alias_version not in version:
            version = f'{alias_version}+{version}'
        return result(aweme_id, family, version, 'REVIEW_REQUIRED', 0.65, 'PLAUSIBLE_HASHTAG_ONLY', reviewed_at, f'candidate_tag={tag}')

    return result(aweme_id, '', infer_version('', hashtags, raw_title, raw_author), 'UNRESOLVED', 0.0, 'NO_RELIABLE_SONG_IDENTITY', reviewed_at)


def main() -> int:
    reviewed_at = datetime.now(ZoneInfo('Asia/Manila')).isoformat(timespec='seconds')
    with (DATA_DIR / 'works.csv').open('r', encoding='utf-8-sig', newline='') as f:
        works = list(csv.DictReader(f))
    with (DATA_DIR / 'accounts.csv').open('r', encoding='utf-8-sig', newline='') as f:
        accounts = {r['account_id']: r for r in csv.DictReader(f)}
    rows = [normalize_row(row, accounts.get(row['account_id'], {}).get('role_category',''), reviewed_at) for row in works]
    fields = ['aweme_id','song_family','audio_version','normalization_status','confidence','evidence_method','reviewed_at','notes']
    with (DATA_DIR / 'song_normalization.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    counts = {}
    for row in rows:
        counts[row['normalization_status']] = counts.get(row['normalization_status'], 0) + 1
    print({'works': len(rows), 'status_counts': counts})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
