"""
Unit Tests for Phase 5: Model Evaluation & Business Segment Profiling
=====================================================================
Tests:
1. test_01_labels_mapping_exists_and_keys
2. test_02_manifest_exists_and_structure
3. test_03_customer_conservation
4. test_04_future_buyers_less_than_total
5. test_05_purchase_rate_monotonicity
6. test_06_spend_per_customer_monotonicity
7. test_07_wilson_ci_validity
8. test_08_non_buyers_benchmark
9. test_09_figures_exist_and_size
10. test_10_anti_leakage_preservation
"""

import os
import json
import unittest
import duckdb

class TestPhase5Evaluation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labels_path = "outputs/models/cluster_business_labels.json"
        cls.manifest_path = "outputs/experiments/phase5_holdout_evaluation.json"
        
        cls.labels_data = None
        if os.path.exists(cls.labels_path):
            with open(cls.labels_path, "r", encoding="utf-8") as f:
                cls.labels_data = json.load(f)
                
        cls.manifest_data = None
        if os.path.exists(cls.manifest_path):
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                cls.manifest_data = json.load(f)

    def test_01_labels_mapping_exists_and_keys(self):
        self.assertIsNotNone(self.labels_data, "Missing cluster_business_labels.json")
        self.assertIn("cluster_mapping", self.labels_data)
        mapping = self.labels_data["cluster_mapping"]
        self.assertEqual(len(mapping), 4)
        for c in range(4):
            self.assertIn(str(c), mapping)
            self.assertIn("name_en", mapping[str(c)])
            self.assertIn("name_vi", mapping[str(c)])

    def test_02_manifest_exists_and_structure(self):
        self.assertIsNotNone(self.manifest_data, "Missing phase5_holdout_evaluation.json")
        required_keys = ["model_freeze", "audit_findings", "holdout_evaluation_metrics", "non_buyers_benchmark", "figures"]
        for k in required_keys:
            self.assertIn(k, self.manifest_data, f"Missing key {k} in manifest")

    def test_03_customer_conservation(self):
        self.assertIsNotNone(self.manifest_data)
        metrics = self.manifest_data["holdout_evaluation_metrics"]
        total = sum(m["n_customers"] for m in metrics)
        self.assertEqual(total, 92652, "Total customer cohort must equal 92,652 exactly")

    def test_04_future_buyers_less_than_total(self):
        self.assertIsNotNone(self.manifest_data)
        metrics = self.manifest_data["holdout_evaluation_metrics"]
        for m in metrics:
            self.assertLessEqual(m["future_buyers"], m["n_customers"])
            self.assertLessEqual(m["future_active_users"], m["n_customers"])

    def test_05_purchase_rate_monotonicity(self):
        """Validates that Phase 5 evaluation manifest records the empirical historical separation: C0 < C2 < C3 < C1."""
        self.assertIsNotNone(self.manifest_data)
        m_dict = {m["cluster_id"]: m for m in self.manifest_data["holdout_evaluation_metrics"]}
        c0 = m_dict[0]["future_purchase_rate_pct"]
        c2 = m_dict[2]["future_purchase_rate_pct"]
        c3 = m_dict[3]["future_purchase_rate_pct"]
        c1 = m_dict[1]["future_purchase_rate_pct"]
        # Empirical historical observation on Feb 2020: C0 < C2 < C3 < C1
        self.assertLess(c0, c2, f"C0 ({c0}%) must be < C2 ({c2}%)")
        self.assertLess(c2, c3, f"C2 ({c2}%) must be < C3 ({c3}%)")
        self.assertLess(c3, c1, f"C3 ({c3}%) must be < C1 ({c1}%)")

    def test_06_spend_per_customer_monotonicity(self):
        self.assertIsNotNone(self.manifest_data)
        m_dict = {m["cluster_id"]: m for m in self.manifest_data["holdout_evaluation_metrics"]}
        s0 = m_dict[0]["future_spend_per_customer"]
        s2 = m_dict[2]["future_spend_per_customer"]
        s3 = m_dict[3]["future_spend_per_customer"]
        s1 = m_dict[1]["future_spend_per_customer"]
        self.assertLess(s0, s2, f"S0 ({s0}) must be < S2 ({s2})")
        self.assertLess(s2, s3, f"S2 ({s2}) must be < S3 ({s3})")
        self.assertLess(s3, s1, f"S3 ({s3}) must be < S1 ({s1})")

    def test_07_wilson_ci_validity(self):
        self.assertIsNotNone(self.manifest_data)
        metrics = self.manifest_data["holdout_evaluation_metrics"]
        for m in metrics:
            ci = m["future_purchase_rate_ci_95"]
            self.assertGreaterEqual(ci[0], 0.0)
            self.assertLessEqual(ci[1], 100.0)
            self.assertLess(ci[0], ci[1])
            self.assertGreaterEqual(m["future_purchase_rate_pct"], ci[0])
            self.assertLessEqual(m["future_purchase_rate_pct"], ci[1])

    def test_08_non_buyers_benchmark(self):
        self.assertIsNotNone(self.manifest_data)
        nb = self.manifest_data["non_buyers_benchmark"]
        self.assertEqual(nb["n_customers"], 1248847)
        m_dict = {m["cluster_id"]: m for m in self.manifest_data["holdout_evaluation_metrics"]}
        self.assertLess(nb["future_purchase_rate_pct"], m_dict[0]["future_purchase_rate_pct"])

    def test_09_figures_exist_and_size(self):
        figs = [
            "outputs/figures/fig17_future_purchase_rate.png",
            "outputs/figures/fig18_future_spend_per_customer.png",
            "outputs/figures/fig19_segment_transition_sankey.png",
            "outputs/figures/fig20_cluster_profiles_comprehensive.png"
        ]
        for f in figs:
            self.assertTrue(os.path.exists(f), f"Missing figure {f}")
            self.assertGreater(os.path.getsize(f), 30000, f"Figure too small: {f}")

    def test_10_anti_leakage_preservation(self):
        con = duckdb.connect()
        # Verify holdout table row count exactly 3,916,392
        holdout_count = con.execute("SELECT COUNT(*) FROM 'data/cleaned/holdout_events.parquet'").fetchone()[0]
        self.assertEqual(holdout_count, 3916392)
        # Verify customer features table exactly 1,341,499
        cust_count = con.execute("SELECT COUNT(*) FROM 'data/features/customer_features.parquet'").fetchone()[0]
        self.assertEqual(cust_count, 1341499)

if __name__ == '__main__':
    unittest.main()

