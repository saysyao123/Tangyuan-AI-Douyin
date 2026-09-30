import hashlib
import tempfile
import unittest
from pathlib import Path
from run_validation import inspect_media


class MediaEvidenceTests(unittest.TestCase):
    def fixtures(self, p):
        p.write_bytes(b'actual media')
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        meta = dict(sha256=sha, bytes=p.stat().st_size, track_id=985094992,
                    song_family='一个人在家', matches_previous_reference_prefix=True,
                    catalog_duration_seconds=60)
        scan = dict(source_sha256=sha, decoded_duration_seconds=60,
                    lyric_prompt_supplied_to_recognizer=False,
                    rows=[dict(start_seconds=0, end_seconds=30, trusted_contiguous_match_chars=8),
                          dict(start_seconds=30, end_seconds=60, trusted_contiguous_match_chars=8)])
        return meta, scan

    def test_real_matching_file_supports_analysis_only(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'media'; m, s = self.fixtures(p)
            result = inspect_media(p, m, s)
            self.assertTrue(result['screen']['allow_full_analysis'])
            self.assertFalse(result['screen']['allow_s1_seal'])

    def test_changed_or_missing_file_cannot_replay_pass(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'media'; m, s = self.fixtures(p)
            p.write_bytes(b'changed')
            self.assertFalse(inspect_media(p, m, s)['screen']['allow_full_analysis'])
            p.unlink()
            self.assertFalse(inspect_media(p, m, s)['screen']['allow_full_analysis'])

    def test_foreign_scan_hash_cannot_support_media(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'media'; m, s = self.fixtures(p)
            s['source_sha256'] = 'other source'
            self.assertFalse(inspect_media(p, m, s)['screen']['allow_full_analysis'])

    def test_duplicated_windows_cannot_supply_two_supports(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'media'; m, s = self.fixtures(p)
            s['rows'][1] = s['rows'][0]
            self.assertFalse(inspect_media(p, m, s)['screen']['allow_full_analysis'])


if __name__ == '__main__':
    unittest.main()
