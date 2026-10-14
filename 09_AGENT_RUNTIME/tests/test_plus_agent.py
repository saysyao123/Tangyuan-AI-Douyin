"""No network, no credentials, no paid model: deterministic contract tests."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plus_agent import GateError, verify, inspect


class PlusAgentTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        (self.root / "gossip_video_workflow" / "examples").mkdir(parents=True)
        self.episode = self.root / "gossip_video_workflow" / "examples" / "episode.json"
        self.task = self.root / "task.json"
        self.base_episode = {"id": "example", "language": "zh", "technical_demo": True,
                             "direction": "draw a demo", "rows": [{"type": "cover"}, {"type": "end"}], "assets": {}}
        self.base_task = {"schema_version": 1, "task_type": "gossip_video", "task_id": "t1",
                          "episode_path": "gossip_video_workflow/examples/episode.json", "intent": "technical_demo"}
        self.write(self.base_episode, self.base_task)

    def write(self, episode, task):
        self.episode.write_text(json.dumps(episode, ensure_ascii=False), encoding="utf-8")
        self.task.write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8")

    def validate(self):
        with patch("plus_agent.REPO", self.root):
            return verify(self.task)

    def test_technical_demo_success(self):
        status = self.validate()
        self.assertEqual(status["status"], "ready_to_render")
        self.assertEqual(status["rights_status"], "not_applicable_demo")
        self.assertFalse(status["model_api_used"])

    def test_path_traversal_blocked(self):
        task = dict(self.base_task, episode_path="../out.json")
        self.write(self.base_episode, task)
        with self.assertRaisesRegex(GateError, "escapes repository"):
            self.validate()

    def test_real_news_must_have_review_and_rights(self):
        episode = dict(self.base_episode, technical_demo=False, editorial_review_complete=True,
                       assets={"clip.mp4": {"url": "https://example.org/clip.mp4"}})
        task = dict(self.base_task, intent="editorial", source_rights_review_complete=True)
        self.write(episode, task)
        with self.assertRaisesRegex(GateError, "missing licensing evidence"):
            self.validate()
        episode["assets"]["clip.mp4"]["license_evidence_url"] = "https://example.org/license"
        self.write(episode, task)
        self.assertEqual(self.validate()["rights_status"], "evidence_declared_unverified")

    def test_wrong_intent_rejected(self):
        task = dict(self.base_task, intent="editorial")
        self.write(self.base_episode, task)
        with self.assertRaises(GateError):
            self.validate()

    def test_inspect_never_claims_render_from_preflight(self):
        with patch("plus_agent.REPO", self.root):
            checked = inspect(self.validate())
        self.assertEqual(checked["status"], "not_exported")


if __name__ == "__main__":
    unittest.main()
