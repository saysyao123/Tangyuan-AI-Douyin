"""Regression checks for false progress and mode forks, using private in-memory copies."""
import json
import unittest
from pathlib import Path

from check_project import validate_state

ROOT = Path(__file__).resolve().parents[1]


class ContinuityChecks(unittest.TestCase):
    def setUp(self):
        self.state = json.loads((ROOT / "PROJECT_STATE.json").read_text())

    def test_current_state_is_valid(self):
        self.assertEqual(validate_state(ROOT, self.state), [])

    def test_mode_fork_is_rejected(self):
        self.state["project_root"] = "10_DIGITAL_ASSET_FACTORY/work_only/"
        self.assertTrue(any("project_root" in e for e in validate_state(ROOT, self.state)))

    def test_unknown_ai_admission_cannot_pass_production(self):
        p = self.state["platform_candidates"][0]
        p["decision"] = "approved_for_full_production"
        self.assertTrue(any("skips" in e for e in validate_state(ROOT, self.state)))

    def test_income_without_transaction_verification_is_rejected(self):
        self.state["verified_net_revenue"]["CNY"] = 9.9
        self.assertTrue(any("positive verified revenue" in e for e in validate_state(ROOT, self.state)))

    def test_evidence_outside_project_is_rejected(self):
        self.state["stages"]["R0"]["evidence"][0]["path"] = "../private_receipt.md"
        self.assertTrue(any("unsafe evidence" in e for e in validate_state(ROOT, self.state)))

    def test_clear_content_rules_alone_do_not_prove_buyer_demand(self):
        p = self.state["platform_candidates"][0]
        for field in ("public_ai_admission", "public_nonexclusive_sales_mechanism",
                      "personal_paid_upload_permission", "buyer_intended_use_license",
                      "final_personal_payout"):
            p[field] = "PASS"
        p["decision"] = "approved_for_full_production"
        self.assertTrue(any("platform and demand" in e for e in validate_state(ROOT, self.state)))


if __name__ == "__main__":
    unittest.main()
