import importlib.util
import json
import tempfile
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'run_alignment.py'
spec = importlib.util.spec_from_file_location('run_alignment', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_timeline_duration_has_highest_priority():
    identity = {
        'timeline_duration_s': 15.386083,
        'content_duration_s': 15.386083,
        'container_duration_s': 15.412245,
        'rendered_duration_s': 99.0,
    }
    assert mod.timeline_duration(identity) == 15.386083


def test_content_duration_is_current_schema_fallback():
    identity = {'content_duration_s': 12.25, 'container_duration_s': 12.31}
    assert mod.timeline_duration(identity) == 12.25


def test_string_encoded_duration_is_accepted():
    identity = {'timeline_duration_s': '15.386083', 'container_duration_s': '15.412245'}
    assert mod.timeline_duration(identity) == 15.386083


def test_legacy_rendered_duration_remains_supported():
    assert mod.timeline_duration({'rendered_duration_s': 8.5}) == 8.5


def test_container_duration_is_last_compatibility_fallback():
    assert mod.timeline_duration({'container_duration_s': 6.75}) == 6.75


def test_missing_duration_fields_blocks():
    try:
        mod.timeline_duration({})
    except KeyError as exc:
        assert 'timeline duration' in str(exc)
    else:
        raise AssertionError('missing duration schema must block')


def test_xingyu_json_preserves_explicit_final_line_end():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / 'alignment.json'
        path.write_text(json.dumps({
            'lines': [
                {'text': '第一句', 'start': 0.3, 'end': 1.8, 'status': 'aligned'},
                {'text': '最后一句', 'start': 2.0, 'end': 3.25, 'status': 'aligned'},
            ]
        }, ensure_ascii=False), encoding='utf-8')
        rows = mod.xingyu_rows_from_alignment(path, ['第一句', '最后一句'])
        assert rows[0]['clip_start_s'] == '0.300'
        assert rows[0]['clip_end_s'] == '1.800'
        assert rows[1]['clip_start_s'] == '2.000'
        assert rows[1]['clip_end_s'] == '3.250'


def test_xingyu_json_changed_trusted_lyric_blocks():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / 'alignment.json'
        path.write_text(json.dumps({'lines': [
            {'text': '被改写的歌词', 'start': 0.1, 'end': 1.0, 'status': 'aligned'}
        ]}, ensure_ascii=False), encoding='utf-8')
        try:
            mod.xingyu_rows_from_alignment(path, ['正确歌词'])
        except ValueError as exc:
            assert 'changed/mismatched trusted lyric' in str(exc)
        else:
            raise AssertionError('changed trusted lyric must block')


def test_xingyu_json_missing_end_blocks():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / 'alignment.json'
        path.write_text(json.dumps({'lines': [
            {'text': '第一句', 'start': 0.1, 'status': 'aligned'}
        ]}, ensure_ascii=False), encoding='utf-8')
        try:
            mod.xingyu_rows_from_alignment(path, ['第一句'])
        except ValueError as exc:
            assert 'missing/invalid line boundary' in str(exc)
        else:
            raise AssertionError('missing end boundary must block')


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for test in tests:
        test()
        print('PASS', test.__name__)
    print(f'{len(tests)} tests passed')
