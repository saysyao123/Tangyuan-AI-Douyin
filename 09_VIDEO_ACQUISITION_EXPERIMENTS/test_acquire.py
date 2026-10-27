#!/usr/bin/env python3
"""Offline deterministic checks for the acquisition wrapper."""
import os
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from acquire import classify_error, safe_source_url, platform_of, execute

class AcquireTests(unittest.TestCase):
    def test_douyin_session(self):
        self.assertEqual(classify_error("Fresh cookies (not necessarily logged in) are needed"), "SESSION_NEEDED")
    def test_bilibili_access(self):
        self.assertEqual(classify_error("HTTP Error 412: Precondition Failed"), "HTTP_412")
    def test_youtube_bot(self):
        self.assertEqual(classify_error("Sign in to confirm you're not a bot"), "SESSION_NEEDED")
    def test_drm(self):
        self.assertEqual(classify_error("This content is protected by DRM"), "DRM_PROTECTED")
    def test_sanitization_keeps_youtube_id(self):
        self.assertEqual(safe_source_url("https://youtube.com/watch?v=abc123&token=secret"),
                         "https://youtube.com/watch?v=abc123")
    def test_signed_media_url_redaction(self):
        self.assertEqual(safe_source_url("https://example.com/video.mp4?auth=secret#fragment"),
                         "https://example.com/video.mp4")
    def test_platform(self):
        self.assertEqual(platform_of("https://www.bilibili.com/video/BV1234"), "bilibili")
        self.assertEqual(platform_of("https://hongguoduanju.com/player/123"), "hongguo_related_web")
    def test_full_requires_rights(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "rights-basis"):
                execute("https://media.w3.org/test.mp4", "full", Path(temp), 3, 10, None, "unspecified")
    def test_browser_rejected_in_ci(self):
        with tempfile.TemporaryDirectory() as temp:
            prior = os.environ.get("GITHUB_ACTIONS")
            try:
                os.environ["GITHUB_ACTIONS"] = "true"
                with self.assertRaisesRegex(ValueError, "forbidden in hosted CI"):
                    execute("https://media.w3.org/test.mp4", "probe", Path(temp), 3, 10, "chrome", "unspecified")
            finally:
                if prior is None:
                    os.environ.pop("GITHUB_ACTIONS", None)
                else:
                    os.environ["GITHUB_ACTIONS"] = prior

if __name__ == "__main__":
    unittest.main()
