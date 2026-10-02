import unittest

from s0_stage import evaluate_s0


def candidate(name="甲", **changes):
    item = {
        "song_family": name,
        "artist_or_account": "账号",
        "source_lane": "PRIMARY_CORE",
        "language_evidence": "CHINESE",
        "history_policy": "ELIGIBLE",
        "semantic_direction": "可视化方向",
        "reference_review": {"identity_tied": True, "user_reviewable": True, "access": "PLAYABLE_PUBLIC_REFERENCE", "current_freshness": "CURRENT"},
    }
    item.update(changes)
    return item


def payload(items, confirmation=None, **changes):
    result = {"candidates": items, "supplemental_enabled": False, "test_mode": False,
              "human_confirmation": confirmation or {"status": "PENDING", "actor": "USER", "mode": "PRODUCTION", "song_family": None}}
    result.update(changes)
    return result


class S0Tests(unittest.TestCase):
    def test_ready_core(self): self.assertEqual(evaluate_s0(payload([candidate()]))["stage_route"], "READY_FOR_HG01")
    def test_title_only_not_chinese_evidence(self): self.assertEqual(evaluate_s0(payload([candidate(language_evidence="TITLE_ONLY")]))["stage_route"], "SONG_POOL_REFRESH_REQUIRED")
    def test_used_or_rejected_excluded(self): self.assertEqual(evaluate_s0(payload([candidate(history_policy="REJECTED")]))["direction_candidates"], [])
    def test_supplemental_never_production_core(self): self.assertEqual(evaluate_s0(payload([candidate(source_lane="SUPPLEMENTAL_TEST")], supplemental_enabled=True))["direction_candidates"], [])
    def test_html_shell_not_reviewable(self):
        ref={"identity_tied":True,"user_reviewable":False,"access":"HTML_SHELL_ONLY","http_status":200,"current_freshness":"NOT_REFRESHED"}
        self.assertEqual(evaluate_s0(payload([candidate(reference_review=ref)]))["stage_route"], "REFERENCE_REFRESH_REQUIRED")
    def test_http_200_alone_not_reviewable(self):
        ref={"identity_tied":True,"user_reviewable":False,"access":"UNKNOWN","http_status":200}
        self.assertEqual(evaluate_s0(payload([candidate(reference_review=ref)]))["hg01_ready_candidates"], [])
    def test_boundary_leakage_invalid(self): self.assertEqual(evaluate_s0(payload([candidate()], production_segment={"start":1}))["stage_route"], "INVALID")
    def test_family_dedupe(self): self.assertEqual(evaluate_s0(payload([candidate(),candidate()]))["direction_candidates"], ["甲"])
    def test_max_three(self): self.assertEqual(len(evaluate_s0(payload([candidate(str(i)) for i in range(5)]))["direction_candidates"]), 3)
    def test_zero_valid(self): self.assertEqual(evaluate_s0(payload([]))["stage_route"], "SONG_POOL_REFRESH_REQUIRED")
    def test_pending_human_does_not_seal(self): self.assertFalse(evaluate_s0(payload([candidate()]))["s0_sealed"])
    def test_test_auto_cannot_seal(self):
        c={"status":"PASS","actor":"AUTO","mode":"TEST","song_family":"甲"}
        self.assertFalse(evaluate_s0(payload([candidate()], c))["s0_sealed"])
    def test_real_production_human_pass_seals(self):
        c={"status":"PASS","actor":"USER","mode":"PRODUCTION","song_family":"甲"}
        self.assertTrue(evaluate_s0(payload([candidate()], c))["s1_entry_allowed"])


if __name__ == "__main__": unittest.main()

