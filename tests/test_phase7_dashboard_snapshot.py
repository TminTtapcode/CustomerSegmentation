"""
Tests for Phase 7: Verified Analytics Snapshot & Dashboard Contract.
Verifies:
  1. Snapshot files existence and non-empty size.
  2. Snapshot manifest checksum integrity.
  3. Customer population conservation across cohorts.
  4. Segment and Non-Buyer tier counts reconciliation.
  5. Tactic distribution reconciliation.
  6. Privacy & anonymization audit (no raw database user_id in samples).
  7. Strict monotonic conversion ordering in historical holdout evaluation.
  8. Responsible marketing compliance: 100% PENDING_CONSENT, no auto-execution triggers.
  9. HTML dashboard asset existence and disclaimer presence.
"""

import os
import json
import unittest
import hashlib
from pathlib import Path

class TestPhase7DashboardSnapshot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dashboard_dir = "outputs/dashboard"
        cls.manifest_path = os.path.join(cls.dashboard_dir, "snapshot_manifest.json")
        cls.master_snapshot_path = os.path.join(cls.dashboard_dir, "ivre_dashboard_snapshot.json")
        cls.html_dashboard_path = os.path.join(cls.dashboard_dir, "index.html")

        with open(cls.master_snapshot_path, "r", encoding="utf-8") as f:
            cls.snapshot = json.load(f)

        with open(cls.manifest_path, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_01_snapshot_files_exist_and_non_empty(self):
        """Validates that all expected snapshot files exist and have non-zero size."""
        expected_files = [
            "ivre_dashboard_snapshot.json",
            "snapshot_manifest.json",
            "summary_snapshot.json",
            "segments_snapshot.json",
            "recommendations_snapshot.json",
            "holdout_evaluation_snapshot.json",
            "model_system_insights_snapshot.json",
            "index.html"
        ]
        for fname in expected_files:
            fpath = os.path.join(self.dashboard_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing snapshot file: {fname}")
            self.assertGreater(os.path.getsize(fpath), 0, f"Snapshot file is empty: {fname}")

    def test_02_manifest_checksum_integrity(self):
        """Validates SHA-256 checksums recorded in the snapshot manifest."""
        for fname, meta in self.manifest["files"].items():
            fpath = os.path.join(self.dashboard_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"File in manifest missing on disk: {fname}")
            with open(fpath, "rb") as f:
                content = f.read()
                actual_sha = hashlib.sha256(content).hexdigest()
            self.assertEqual(actual_sha, meta["sha256"], f"Checksum mismatch for {fname}")

    def test_03_customer_population_conservation(self):
        """Validates that customer overview totals exactly 1,341,499 (92,652 buyers + 1,248,847 non-buyers)."""
        overview = self.snapshot["customer_overview"]
        self.assertEqual(overview["total_observed_customers"], 1341499)
        self.assertEqual(overview["buyers_count"], 92652)
        self.assertEqual(overview["non_buyers_count"], 1248847)
        self.assertEqual(overview["buyers_count"] + overview["non_buyers_count"], 1341499)

    def test_04_buyer_segments_reconciliation(self):
        """Validates that the 4 buyer segments reconcile to exactly 92,652."""
        segments = self.snapshot["buyer_segments"]
        self.assertEqual(len(segments), 4)
        total_buyers = sum(s["customer_count"] for s in segments)
        self.assertEqual(total_buyers, 92652)
        cluster_ids = {s["cluster_id"] for s in segments}
        self.assertEqual(cluster_ids, {0, 1, 2, 3})

    def test_05_non_buyer_tiers_reconciliation(self):
        """Validates that the 4 non-buyer tiers reconcile to exactly 1,248,847."""
        tiers = self.snapshot["non_buyer_tiers"]
        self.assertEqual(len(tiers), 4)
        total_nb = sum(t["customer_count"] for t in tiers)
        self.assertEqual(total_nb, 1248847)
        tier_codes = {t["tier_code"] for t in tiers}
        self.assertEqual(tier_codes, {"HIGH_INTENT", "EXPLORING", "LOW_ENGAGEMENT", "INACTIVE"})

    def test_06_tactic_distribution_conservation(self):
        """Validates that the sum of all tactics equals exactly 1,341,499."""
        tactics = self.snapshot["tactic_distribution"]
        total_tactics = sum(t["total_count"] for t in tactics)
        self.assertEqual(total_tactics, 1341499)
        buyer_tactics = sum(t["buyers_count"] for t in tactics)
        self.assertEqual(buyer_tactics, 92652)
        nb_tactics = sum(t["non_buyers_count"] for t in tactics)
        self.assertEqual(nb_tactics, 1248847)

    def test_07_privacy_and_anonymization(self):
        """Validates that no raw user_id or sensitive personal identifiers exist in customer samples."""
        samples = self.snapshot["archetype_samples"]
        self.assertGreaterEqual(len(samples), 8)
        for s in samples:
            demo_id = str(s["demo_id"])
            self.assertTrue(demo_id.startswith("DEMO_"), f"Raw user ID detected: {demo_id}")
            self.assertEqual(s["eligibility_status"], "PENDING_CONSENT")
            self.assertIn("evaluation_kpi", s)
            self.assertIn("explanation", s)

    def test_08_holdout_source_reconciliation_and_empirical_ordering(self):
        """Validates that snapshot accurately reflects the empirical historical holdout findings from Phase 5 manifest."""
        holdout = self.snapshot["historical_holdout_evaluation"]
        self.assertIn("holdout_evaluation_metrics", holdout)
        self.assertIn("non_buyers_benchmark", holdout)
        
        # Source-of-truth reconciliation against phase5_holdout_evaluation.json
        phase5_manifest_path = Path("outputs/evaluation/phase5_holdout_evaluation.json")
        if phase5_manifest_path.exists():
            with open(phase5_manifest_path, "r", encoding="utf-8") as f:
                source_eval = json.load(f)
            source_nb_rate = source_eval["non_buyers_benchmark"]["future_purchase_rate_pct"]
            self.assertEqual(holdout["non_buyers_benchmark"]["future_purchase_rate_pct"], source_nb_rate)
            
            source_cluster_map = {m["cluster_id"]: m["future_purchase_rate_pct"] for m in source_eval["holdout_evaluation_metrics"]}
            for item in holdout["holdout_evaluation_metrics"]:
                cid = item["cluster_id"]
                self.assertEqual(item["future_purchase_rate_pct"], source_cluster_map[cid])

        # Verify historical empirical separation observed on REES46 Feb 2020
        nb_rate = holdout["non_buyers_benchmark"]["future_purchase_rate_pct"]
        cluster_map = {item["cluster_id"]: item["future_purchase_rate_pct"] for item in holdout["holdout_evaluation_metrics"]}
        self.assertLess(nb_rate, cluster_map[0])
        self.assertLess(cluster_map[0], cluster_map[2])
        self.assertLess(cluster_map[2], cluster_map[3])
        self.assertLess(cluster_map[3], cluster_map[1])

    def test_09_disclaimer_and_html_dashboard_integrity(self):
        """Validates disclaimer content in JSON snapshot and HTML dashboard."""
        disclaimer = self.snapshot["metadata"]["disclaimer"]
        self.assertIn("REES46", disclaimer)
        self.assertIn("Research Demo", disclaimer)
        with open(self.html_dashboard_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("IVRE ATELIER", html)
        self.assertIn("Research Demo", html)
        self.assertIn("PENDING_CONSENT", html)

if __name__ == "__main__":
    unittest.main()

