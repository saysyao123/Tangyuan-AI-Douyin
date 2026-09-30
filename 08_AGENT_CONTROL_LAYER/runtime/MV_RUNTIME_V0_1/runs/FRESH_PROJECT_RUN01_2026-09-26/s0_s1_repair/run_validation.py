"""Verify real local media and exercise a declared supplemental test lane."""
import argparse
import hashlib
import json
from pathlib import Path
from candidate_intake import rank_directions, screen_source

ROOT = Path(__file__).resolve().parent
REJECTED = ['6463db1a27b6d3ebdd1541205796f42888cadc281fa2c45e14c07c4fcfaf4a43']


def inspect_media(path, meta, scan):
    exists = path.is_file()
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if exists else None
    media_verified = bool(exists and digest == meta.get('sha256') and path.stat().st_size == meta.get('bytes'))
    scan_bound = bool(media_verified and scan.get('source_sha256') == digest)
    rows = scan.get('rows', [])
    # Do not count duplicated/overlapping windows as independent support.
    coverage_valid = bool(rows)
    end = 0.0
    for row in rows:
        start = row.get('start_seconds', -1)
        new_end = row.get('end_seconds', -1)
        if abs(start - end) > .01 or new_end <= start or new_end - start > 30.01:
            coverage_valid = False
        end = new_end
    coverage_valid = coverage_valid and abs(end - scan.get('decoded_duration_seconds', -100)) < .01
    coverage_valid = coverage_valid and abs(end - meta.get('catalog_duration_seconds', -100)) < 1
    valid_scan = scan_bound and coverage_valid and scan.get('lyric_prompt_supplied_to_recognizer') is False
    support = sum(row.get('trusted_contiguous_match_chars', 0) >= 6 for row in rows) if valid_scan else 0
    best = max((row.get('trusted_contiguous_match_chars', 0) for row in rows), default=0) if valid_scan else 0
    identity = media_verified and meta.get('track_id') == 985094992 and meta.get('song_family') == '一个人在家' and meta.get('matches_previous_reference_prefix') is True
    evidence = dict(actual_media_exists=media_verified, identity_verified=bool(identity), sha256=digest,
                    rejected_source_hashes=REJECTED, supporting_windows=support,
                    best_contiguous_match_chars=best, human_audio_review='PENDING')
    return {'media_hash_verified': media_verified, 'full_scan_bound_to_media': valid_scan,
            'source_evidence': evidence, 'screen': screen_source(evidence)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--media', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'REAL_VALIDATION_RESULT.json')
    args = parser.parse_args()
    candidates = json.loads((ROOT / 'DIRECTION_INPUT.json').read_text())
    meta = json.loads((ROOT / 'full_source_meta.json').read_text())
    scan = json.loads((ROOT / 'full_scan_summary.json').read_text())
    result = {
        'execution_mode': 'LOCAL_MEDIA_HASH_VERIFIED' if args.media.is_file() else 'MISSING_MEDIA_NOT_A_REAL_RUN',
        'direction_shortlist': rank_directions(candidates),
        'validation_branch': {
            'purpose': 'VALIDATION_ONLY_NOT_PRODUCTION_LOCK',
            'song_family': meta['song_family'], 'source_group': 'SUPPLEMENTAL_TEST',
            **inspect_media(args.media, meta, scan)},
        'production_selected_song_family': None, 'formal_s1_seal': False, 'allow_s2': False
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'direction_count': len(result['direction_shortlist']),
                      'validation_branch': result['validation_branch'],
                      'formal_s1_seal': False}, ensure_ascii=False, indent=2))
    return 0 if result['validation_branch']['screen']['allow_full_analysis'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
