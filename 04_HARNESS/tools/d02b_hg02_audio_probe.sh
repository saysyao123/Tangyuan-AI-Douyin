#!/usr/bin/env bash
set -euo pipefail

OUT='06_TESTS/MV/WEB_R3/30D_60/D02-B/02_BGM/BGM_DISCOVERY'
ASSET_REPORT="$OUT/asset_probe_report.json"
AUDIO_REPORT="$OUT/audio_probe_report.json"
TMP='/tmp/hg02_audio'
WORK_URL='https://www.douyin.com/video/7674212223707078833'
mkdir -p "$OUT" "$TMP"

if [ ! -f "$ASSET_REPORT" ]; then
  echo "ERROR: missing $ASSET_REPORT" >&2
  exit 1
fi

python - <<'PY' > /tmp/d02b_music_urls.txt
import json
from pathlib import Path
p=Path('06_TESTS/MV/WEB_R3/30D_60/D02-B/02_BGM/BGM_DISCOVERY/asset_probe_report.json')
d=json.loads(p.read_text(encoding='utf-8'))
for s in d['samples']:
    print(s['music_url'])
PY
mapfile -t MUSIC_URLS < /tmp/d02b_music_urls.txt

UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36'
SOURCE_MODE=''
SOURCE_NOTE=''
MASTER="$TMP/master_source.mp3"

try_music_asset() {
  local u="$1"
  local dest="$2"
  curl --http1.1 -fL \
    --connect-timeout 10 --max-time 45 \
    --retry 2 --retry-delay 1 --retry-all-errors \
    -A "$UA" -H 'Referer: https://www.douyin.com/' \
    "$u" -o "$dest"
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$dest" >/dev/null
}

for u in "${MUSIC_URLS[@]}"; do
  rm -f "$TMP/direct_asset.mp3"
  if try_music_asset "$u" "$TMP/direct_asset.mp3"; then
    cp "$TMP/direct_asset.mp3" "$MASTER"
    SOURCE_MODE='P1_EXACT_DOUYIN_MUSIC_ASSET'
    SOURCE_NOTE='Direct download of exact Douyin ies-music object 7670104695834282815.'
    break
  fi
done

if [ -z "$SOURCE_MODE" ]; then
  echo 'Direct music CDN unavailable from runner; falling back to audio actually heard in verified core work.'
  curl -fsSL --retry 2 --retry-delay 2 \
    -H 'Referer: https://api.bugpk.com/doc-douyin.html' \
    -H 'X-Requested-With: XMLHttpRequest' \
    --get 'https://api.bugpk.com/api/douyin' \
    --data-urlencode "url=$WORK_URL" \
    > /tmp/d02b_fire_parser.json

  VIDEO_URL=$(python - <<'PY'
import json
from pathlib import Path
d=json.loads(Path('/tmp/d02b_fire_parser.json').read_text(encoding='utf-8'))
print((d.get('data') or {}).get('url') or '')
PY
)

  if [ -n "$VIDEO_URL" ]; then
    set +e
    curl --http1.1 -fL \
      --connect-timeout 10 --max-time 90 \
      --retry 2 --retry-delay 1 --retry-all-errors \
      -A "$UA" -H 'Referer: https://www.douyin.com/' \
      "$VIDEO_URL" -o "$TMP/core_work.mp4"
    VIDEO_CODE=$?
    set -e
  else
    VIDEO_CODE=1
  fi

  if [ "$VIDEO_CODE" -ne 0 ] || ! ffprobe -v error "$TMP/core_work.mp4" >/dev/null 2>&1; then
    echo 'BugPk returned video CDN was unavailable; trying douyin.wtf proxy.'
    curl -fL \
      --connect-timeout 10 --max-time 120 \
      --retry 2 --retry-delay 1 --retry-all-errors \
      -A "$UA" \
      --get 'https://douyin.wtf/api/download' \
      --data-urlencode "url=$WORK_URL" \
      --data-urlencode 'prefix=false' \
      --data-urlencode 'watermark=false' \
      -o "$TMP/core_work.mp4"
  fi

  ffprobe -v error "$TMP/core_work.mp4" >/dev/null
  ffmpeg -hide_banner -loglevel error -y -i "$TMP/core_work.mp4" -vn \
    -codec:a libmp3lame -q:a 2 "$MASTER"
  SOURCE_MODE='P2_VERIFIED_CORE_WORK_AUDIO_AS_HEARD'
  SOURCE_NOTE='Audio extracted from the verified 火乐烁 core MV; both core works independently resolve to Douyin music object 7670104695834282815.'
fi

ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels \
  -of json "$MASTER" > /tmp/master_probe.json
cp "$MASTER" "$TMP/HG02_A_native.mp3"
DURATION=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$MASTER")
FADE_START=$(python -c "print(max(0.0, float('$DURATION') - 0.8))")
ffmpeg -hide_banner -loglevel error -y -i "$MASTER" \
  -af "afade=t=out:st=${FADE_START}:d=0.8" \
  -codec:a libmp3lame -q:a 2 "$TMP/HG02_B_soft_tail_0p8s.mp3"

SOURCE_MODE="$SOURCE_MODE" SOURCE_NOTE="$SOURCE_NOTE" python - <<'PY'
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

root=Path('/tmp/hg02_audio')
probe=json.loads(Path('/tmp/master_probe.json').read_text())
report={
  'schema_version':'1.1',
  'song_family':'有几次想你了',
  'checked_at':datetime.now(timezone.utc).isoformat(),
  'douyin_music_asset_object_id':'7670104695834282815',
  'version_identity_evidence':{
    'core_work_count':2,
    'same_music_object_id':True,
    'same_music_title':True,
    'same_music_author':True,
    'music_title':'@林叙（错位秋天已上线）创作的原声',
    'music_author':'林叙（错位秋天已上线）'
  },
  'listening_source_mode':os.environ['SOURCE_MODE'],
  'listening_source_note':os.environ['SOURCE_NOTE'],
  'master_ffprobe':probe,
  'candidate_A':{
    'name':'HG02_A_native.mp3',
    'transform':'native listening source; no tail fade',
    'sha256':sha(root/'HG02_A_native.mp3')
  },
  'candidate_B':{
    'name':'HG02_B_soft_tail_0p8s.mp3',
    'transform':'same listening source; final 0.8s fade-out only',
    'sha256':sha(root/'HG02_B_soft_tail_0p8s.mp3')
  },
  'decision':'HG02_LISTENING_ASSETS_READY'
}
Path('06_TESTS/MV/WEB_R3/30D_60/D02-B/02_BGM/BGM_DISCOVERY/audio_probe_report.json').write_text(
    json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
PY
