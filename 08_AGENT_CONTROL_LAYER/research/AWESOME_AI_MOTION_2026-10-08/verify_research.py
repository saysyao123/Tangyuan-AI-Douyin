#!/usr/bin/env python3
"""验证归档无目录遗漏；不把覆盖检查当成视频质量检查。仅用 Python 标准库。"""
import argparse, collections, hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent

def lines(name):
    return [json.loads(s) for s in (ROOT / name).read_text().splitlines() if s.strip()]

def load(name):
    return json.loads((ROOT / name).read_text())

def verify(upstream=None):
    cases = lines('CASE_STUDY_INDEX.jsonl')
    files = lines('FILE_INVENTORY.jsonl')
    prompts = lines('PROMPT_STUDY_INDEX.jsonl')
    resources = lines('RESOURCE_STUDY_INDEX.jsonl')
    snapshot = load('SOURCE_SNAPSHOT.json')
    status = load('RESEARCH_STATUS.json')
    ids = {c['id'] for c in cases}
    checks = {}

    def require(name, condition):
        checks[name] = bool(condition)
        if not condition:
            raise AssertionError(name)

    require('581 unique case records', len(cases) == len(ids) == 581)
    require('category counts', dict(collections.Counter(c['category'] for c in cases)) == snapshot['stats']['categories'])
    require('83 original 118 brief 380 unknown', collections.Counter(c['prompt_status'] for c in cases) == {'original': 83, 'brief': 118, 'unknown': 380})
    require('201 nonunknown prompt records', len(prompts) == 201 and {p['id'] for p in prompts} == {c['id'] for c in cases if c['prompt_status'] != 'unknown'})
    require('128 inline prompt records', sum(c['prompt_text_read'] for c in cases) == 128 and sum(p['inline_read'] for p in prompts) == 128)
    require('73 source_link records', sum(c['prompt_display'] == 'source_link' for c in cases) == 73)
    require('1943 unique tracked files', len(files) == len({f['path'] for f in files}) == 1943)
    require('all file hashes valid', all(re.fullmatch(r'[0-9a-f]{64}', f['sha256']) and f['bytes'] >= 0 and f['review_level'] for f in files))
    require('581 covers match case IDs', {pathlib.PurePosixPath(f['path']).stem for f in files if f['path'].startswith('assets/covers/')} == ids)
    require('1162 bilingual generated case files', sum(f['path'].startswith('cases/') for f in files) == 1162)
    require('128 generated prompt files', sum(f['path'].startswith('prompts/') for f in files) == 128)
    require('90 resource associations 84 URLs 70 cases', len(resources) == 90 and len({r['url'] for r in resources}) == 84 and len({r['case_id'] for r in resources}) == 70)
    require('resource kinds', collections.Counter(r['kind'] for r in resources) == {'code': 27, 'demo': 41, 'tool': 22})
    require('resource associations map to exact cases', all(r['case_id'] in ids and r['url'] in next(c['resource_urls'] for c in cases if c['id'] == r['case_id']) for r in resources))
    require('39 README records', len(load('evidence/README_SOURCES.json')) == 39)
    require('14 focused source files', len(load('evidence/KEY_SOURCE_FILES.json')) == 14)
    require('no false full review or reproduction', all(not c['full_video_review_completed'] and not c['independently_reproduced'] for c in cases) and status['full_video_review']['completed'] == 0)
    require('601 attachments and 16 multi-video records', sum(c['attachment_count'] for c in cases) == 601 and sum(c['attachment_count'] > 1 for c in cases) == 16)
    for case in cases:
        path, anchor = case['note_path'].split('#')
        content = (ROOT / path).read_text()
        require('case note ' + case['id'], f'id="{anchor}"' in content and case['source_url'] in content and case['title'] in content)
    media = load('evidence/MEDIA_HEADER_CHECK.json')
    require('media check complete', len(media['results']) == 581 and {r['id'] for r in media['results']} == ids)
    require('575 header passes 6 failures', sum(r['ok'] for r in media['results']) == media['passed'] == 575 and media['failed'] == 6)
    pages = load('evidence/PAGE_RETRIEVAL.json')
    require('581 work pages attempted', sum(r['kind'] == 'work_post' for r in pages) == 581)
    require('157 resource and prompt pages attempted', sum(r['kind'] != 'work_post' for r in pages) == 157)
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^\s)]+)\)', path.read_text()):
            if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            file_part, _, anchor = target.partition('#')
            dest = (path.parent / file_part).resolve() if file_part else path
            require('relative link ' + path.name + ' ' + target, dest.exists())
            if anchor.startswith('case-'):
                require('case anchor ' + anchor, f'id="{anchor}"' in dest.read_text())
    require('no media or raw external copies', not any(p.suffix.lower() in {'.mp4','.mp3','.wav','.jpg','.png','.html'} for p in ROOT.rglob('*') if p.is_file()))
    if upstream:
        source = pathlib.Path(upstream)
        payload = (source / 'data/cases.json').read_bytes()
        require('upstream data hash', hashlib.sha256(payload).hexdigest() == snapshot['data_sha256'])
        authoritative = json.loads(payload)['cases']
        require('exact upstream IDs', {c['id'] for c in authoritative} == ids)
        for record in files:
            file = source / record['path']
            require('frozen file ' + record['path'], file.is_file() and hashlib.sha256(file.read_bytes()).hexdigest() == record['sha256'])
    report = {'status':'PASS','checks_passed':len(checks),'cases':len(cases),'files':len(files),'prompt_records':len(prompts),'resource_associations':len(resources),'upstream_hashes_rechecked':bool(upstream),'full_video_review_proven':False,'external_reproduction_proven':False}
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', help='可选：冻结提交的 awesome-ai-motion 工作树路径')
    parser.add_argument('--receipt', action='store_true', help='保存本次覆盖收据')
    args = parser.parse_args()
    try:
        result = verify(args.upstream)
        if args.receipt:
            (ROOT / 'evidence/ARCHIVE_VERIFICATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(result, ensure_ascii=False))
    except (AssertionError, ValueError, KeyError, FileNotFoundError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
