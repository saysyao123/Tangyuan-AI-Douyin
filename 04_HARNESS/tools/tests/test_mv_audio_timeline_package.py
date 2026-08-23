import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "mv_audio_timeline_package.py"


class AudioTimelinePackageTests(unittest.TestCase):
    def run_cmd(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
        )

    def make_common(self, root: Path, clip_start=83.8, duration=12.0):
        config = {
            "title": "Test Song",
            "artist": "Test Artist",
            "exact_version": "studio-master",
            "source_clip_start_sec": clip_start,
            "source_clip_end_sec": clip_start + duration,
            "rendered_duration_sec": duration,
            "locked_bgm_sha256": "a" * 64,
            "speed": 1.0,
        }
        (root / "audio_identity.json").write_text(json.dumps(config), encoding="utf-8")
        (root / "lyrics.txt").write_text("第一句歌词\n第二句歌词\n第三句歌词\n", encoding="utf-8")

    def test_same_version_lrc_transforms_monotonically_but_stays_unlocked_until_qa(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_common(root)
            (root / "raw.lrc").write_text(
                "[01:24.20]第一句歌词\n"
                "[01:28.00]第二句歌词\n"
                "[01:32.40]第三句歌词\n",
                encoding="utf-8",
            )
            out = root / "pkg"
            p = self.run_cmd(
                "from-lrc",
                "--config", root / "audio_identity.json",
                "--lyrics", root / "lyrics.txt",
                "--lrc", root / "raw.lrc",
                "--out-dir", out,
                "--source-platform", "fixture",
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            timeline = (out / "line_timeline.csv").read_text(encoding="utf-8-sig")
            self.assertIn("0.4", timeline)
            self.assertIn("4.2", timeline)
            self.assertIn("8.6", timeline)
            manifest = json.loads((out / "package_manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["AUDIO_TIMELINE_PACKAGE_LOCKED"])

            v = self.run_cmd("validate", "--package-dir", out)
            self.assertEqual(v.returncode, 3)
            self.assertIn("remains BLOCKED", v.stderr)

    def test_wrong_version_lrc_with_first_line_far_before_clip_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_common(root, clip_start=139.93, duration=37.12)
            # Mirrors the R2 failure class: matching title/lyrics but wrong chorus timing.
            (root / "raw.lrc").write_text(
                "[02:14.00]第一句歌词\n"
                "[02:20.00]第二句歌词\n"
                "[02:23.00]第三句歌词\n",
                encoding="utf-8",
            )
            out = root / "pkg"
            p = self.run_cmd(
                "from-lrc",
                "--config", root / "audio_identity.json",
                "--lyrics", root / "lyrics.txt",
                "--lrc", root / "raw.lrc",
                "--out-dir", out,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("before clip", p.stderr)

    def test_speed_change_forbids_simple_offset_transform(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_common(root)
            cfg = json.loads((root / "audio_identity.json").read_text(encoding="utf-8"))
            cfg["speed"] = 1.1
            (root / "audio_identity.json").write_text(json.dumps(cfg), encoding="utf-8")
            (root / "raw.lrc").write_text("[01:24.20]第一句歌词\n[01:28.00]第二句歌词\n[01:32.40]第三句歌词\n", encoding="utf-8")
            p = self.run_cmd(
                "from-lrc",
                "--config", root / "audio_identity.json",
                "--lyrics", root / "lyrics.txt",
                "--lrc", root / "raw.lrc",
                "--out-dir", root / "pkg",
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("time-stretch", p.stderr)

    def test_repeated_lyrics_consume_distinct_occurrences(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            config = {
                "title": "Repeat Song",
                "artist": "Artist",
                "exact_version": "studio",
                "source_clip_start_sec": 60.0,
                "source_clip_end_sec": 75.0,
                "rendered_duration_sec": 15.0,
                "locked_bgm_sha256": "b" * 64,
                "speed": 1.0,
            }
            (root / "audio_identity.json").write_text(json.dumps(config), encoding="utf-8")
            (root / "lyrics.txt").write_text("副歌\n中间句\n副歌\n", encoding="utf-8")
            (root / "raw.lrc").write_text(
                "[01:00.20]副歌\n[01:05.00]中间句\n[01:10.00]副歌\n",
                encoding="utf-8",
            )
            out = root / "pkg"
            p = self.run_cmd(
                "from-lrc",
                "--config", root / "audio_identity.json",
                "--lyrics", root / "lyrics.txt",
                "--lrc", root / "raw.lrc",
                "--out-dir", out,
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            text = (out / "line_timeline.csv").read_text(encoding="utf-8-sig")
            self.assertIn("0.2", text)
            self.assertIn("10.0", text)


if __name__ == "__main__":
    unittest.main()
