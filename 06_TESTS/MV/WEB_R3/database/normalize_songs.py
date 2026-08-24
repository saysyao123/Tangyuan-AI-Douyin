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
}

# Explicit variants we have already observed in the nine-account R3 sample.
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
    # Common audio-title suffixes: keep the song family, move variant to audio_version.
    version = None
    low = value.lower()
    for needle, label in VERSION_PATTERNS:
        if needle in low:
            version = label if version is None else f'{version}+{label}'
    value = re.sub(r'[（(](?:剪辑版\d*|片段|副歌|氛围片段|r&b|rnb|电音版)[）)]', '', value, flags=re.I)
    value = re.sub(r'[-—_](?:副歌|片段).*$', '', value, flags=re.I)
    value = re.sub(r'(?:电音版|电音remix|rnb氛围版)$', '', value, flags=re.I)
    value = value.strip(' -—_·')
    return value, version


def plausible_tag(tag: str) -> bool:
    t = compact(tag)
    if not t or t in GENERIC_TAGS:
        return False
    if len(t) < 2 or len(t) > 26:
        return False
    if t.startswith(('pavoai','ai','抖音','旅行','创作者','音乐种草','inmy','dj')):
        return False
    return True


def normalize_row(row: dict[str, str], reviewed_at: str) -> dict[str, str | float]:
    aweme_id = row['aweme_id']
    caption = norm(row.get('caption', ''))
    raw_title = norm(row.get('music_title_raw', ''))
    raw_author = norm(row.get('music_author_raw', ''))
    hashtags = [norm(x) for x in str(row.get('hashtags', '')).split('|') if norm(x)]

    # 1. Explicit '#歌曲X' is the strongest Douyin-visible song identity evidence.
    for tag in hashtags:
        if compact(tag).startswith('歌曲') and len(norm(tag)) > 2:
            family, alias_version = clean_family(tag)
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version:
                version = f'{alias_version}+{version}'
            return {
                'aweme_id': aweme_id, 'song_family': family, 'audio_version': version,
                'normalization_status': 'AUTO_HIGH', 'confidence': 0.98,
                'evidence_method': 'EXPLICIT_SONG_HASHTAG', 'reviewed_at': reviewed_at,
                'notes': f'source_tag={tag}'
            }

    # 2. A real named music title is normally much stronger than generic original-sound labels.
    if raw_title and raw_title != '模板音乐' and not raw_title.startswith('@'):
        family, title_version = clean_family(raw_title)
        if family:
            version = infer_version(raw_title, hashtags, raw_title, raw_author)
            if title_version and title_version not in version:
                version = f'{title_version}+{version}'
            return {
                'aweme_id': aweme_id, 'song_family': family, 'audio_version': version,
                'normalization_status': 'AUTO_HIGH', 'confidence': 0.95,
                'evidence_method': 'NAMED_MUSIC_METADATA', 'reviewed_at': reviewed_at,
                'notes': f'raw_title={raw_title}'
            }

    # 3. For creator-original-sound labels, accept a song-like hashtag only when caption also corroborates it.
    for tag in hashtags:
        if not plausible_tag(tag):
            continue
        family, alias_version = clean_family(tag)
        if not family:
            continue
        if compact(tag) in compact(caption) or compact(family) in compact(caption):
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version:
                version = f'{alias_version}+{version}'
            return {
                'aweme_id': aweme_id, 'song_family': family, 'audio_version': version,
                'normalization_status': 'AUTO_HIGH', 'confidence': 0.89,
                'evidence_method': 'CAPTION_HASHTAG_CORROBORATION', 'reviewed_at': reviewed_at,
                'notes': f'corroborated_tag={tag}'
            }

    # 4. Keep a plausible hashtag as a review lead, but do not let it enter primary trend counts yet.
    for tag in hashtags:
        if plausible_tag(tag):
            family, alias_version = clean_family(tag)
            version = infer_version(tag, hashtags, raw_title, raw_author)
            if alias_version and alias_version not in version:
                version = f'{alias_version}+{version}'
            return {
                'aweme_id': aweme_id, 'song_family': family, 'audio_version': version,
                'normalization_status': 'REVIEW_REQUIRED', 'confidence': 0.65,
                'evidence_method': 'PLAUSIBLE_HASHTAG_ONLY', 'reviewed_at': reviewed_at,
                'notes': f'candidate_tag={tag}'
            }

    return {
        'aweme_id': aweme_id, 'song_family': '', 'audio_version': infer_version('', hashtags, raw_title, raw_author),
        'normalization_status': 'UNRESOLVED', 'confidence': 0.0,
        'evidence_method': 'NO_RELIABLE_SONG_IDENTITY', 'reviewed_at': reviewed_at,
        'notes': ''
    }


def main() -> int:
    reviewed_at = datetime.now(ZoneInfo('Asia/Manila')).isoformat(timespec='seconds')
    with (DATA_DIR / 'works.csv').open('r', encoding='utf-8-sig', newline='') as f:
        works = list(csv.DictReader(f))
    rows = [normalize_row(row, reviewed_at) for row in works]
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
