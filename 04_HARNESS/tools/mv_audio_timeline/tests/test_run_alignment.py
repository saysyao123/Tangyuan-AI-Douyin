import importlib.util
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


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for test in tests:
        test()
        print('PASS', test.__name__)
    print(f'{len(tests)} tests passed')
