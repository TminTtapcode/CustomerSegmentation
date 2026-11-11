"""Unit and Integration Tests for Phase 3 — Customer Feature Engineering & Behavioral Analytics."""
import json
import unittest
from pathlib import Path
import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_FEATURES = ROOT / "data" / "features"
CUSTOMER_PARQUET = str(DATA_FEATURES / "customer_features.parquet").replace("\\", "/")
BUYER_PARQUET = str(DATA_FEATURES / "buyer_features.parquet").replace("\\", "/")
NON_BUYER_PARQUET = str(DATA_FEATURES / "non_buyer_features.parquet").replace("\\", "/")
MANIFEST_JSON = ROOT / "outputs" / "experiments" / "phase3_feature_profiling.json"
FIGURES_DIR = ROOT / "outputs" / "figures"


class TestPhase3FeatureEngineering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = duckdb.connect(database=":memory:")
        cls.con.execute("SET threads = 4")
        with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_feature_tables_exist_and_sizes(self):
        for fname in ["customer_features.parquet", "buyer_features.parquet", "non_buyer_features.parquet"]:
            fpath = DATA_FEATURES / fname
            self.assertTrue(fpath.is_file(), f"Missing feature Parquet: {fname}")
            self.assertGreater(fpath.stat().st_size, 1024 * 1024, f"File {fname} is unexpectedly small (<1MB)")

    def test_cohort_separation_and_counts(self):
        cohorts = self.manifest["cohort_counts"]
        total = cohorts["total_observation_customers"]
        buyers = cohorts["buyers_count"]
        non_buyers = cohorts["non_buyers_count"]

        self.assertEqual(total, 1341499)
        self.assertEqual(buyers, 92652)
        self.assertEqual(non_buyers, 1248847)
        self.assertEqual(buyers + non_buyers, total)

        # In database:
        db_cust = self.con.execute(f"SELECT COUNT(*) FROM read_parquet('{CUSTOMER_PARQUET}')").fetchone()[0]
        db_buyers = self.con.execute(f"SELECT COUNT(*) FROM read_parquet('{BUYER_PARQUET}')").fetchone()[0]
        db_non_buyers = self.con.execute(f"SELECT COUNT(*) FROM read_parquet('{NON_BUYER_PARQUET}')").fetchone()[0]
        self.assertEqual(db_cust, 1341499)
        self.assertEqual(db_buyers, 92652)
        self.assertEqual(db_non_buyers, 1248847)

    def test_non_buyer_recency_policy_is_null(self):
        # Non-buyers must NEVER have artificial Recency = 0, 999 or infinite. It must be strictly NULL.
        non_null_rec = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{NON_BUYER_PARQUET}')
        WHERE recency_days IS NOT NULL
        """).fetchone()[0]
        self.assertEqual(non_null_rec, 0, "Non-buyers must have NULL recency_days")

        # Non-buyers must have frequency = 0 and monetary = 0
        invalid_non_buyers = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{NON_BUYER_PARQUET}')
        WHERE frequency != 0 OR monetary != 0.0
        """).fetchone()[0]
        self.assertEqual(invalid_non_buyers, 0, "Non-buyers must have frequency=0 and monetary=0")

    def test_buyer_rfm_ranges_and_constraints(self):
        # Buyers must have recency in [0, 123] days (since observation window is 123 days)
        rfm_check = self.con.execute(f"""
        SELECT 
            MIN(recency_days) AS min_r,
            MAX(recency_days) AS max_r,
            MIN(frequency) AS min_f,
            MIN(monetary) AS min_m,
            COUNT(CASE WHEN recency_days IS NULL THEN 1 END) AS null_r_count
        FROM read_parquet('{BUYER_PARQUET}')
        """).fetchone()

        self.assertGreaterEqual(rfm_check[0], 0.0)
        self.assertLessEqual(rfm_check[1], 123.0)
        self.assertGreaterEqual(rfm_check[2], 1)
        self.assertGreater(rfm_check[3], 0.0)
        self.assertEqual(rfm_check[4], 0, "Buyers must have 0 null recency")

    def test_laplace_smoothing_log_activity_ratio(self):
        # log_activity_ratio = ln((sessions_recent_30d + 1) / (sessions_previous_30d + 1))
        sample = self.con.execute(f"""
        SELECT 
            sessions_recent_30d,
            sessions_previous_30d,
            log_activity_ratio,
            ROUND(LN((sessions_recent_30d + 1.0) / (sessions_previous_30d + 1.0)), 4) AS expected_ratio
        FROM read_parquet('{CUSTOMER_PARQUET}')
        WHERE sessions_recent_30d > 0 OR sessions_previous_30d > 0
        LIMIT 50
        """).fetchall()

        for row in sample:
            self.assertAlmostEqual(row[2], row[3], places=3, msg=f"Laplace smoothed ratio mismatch for row {row}")

    def test_activity_difference_semantics(self):
        # activity_difference = sessions_recent_30d - sessions_previous_30d
        mismatches = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{CUSTOMER_PARQUET}')
        WHERE activity_difference != (sessions_recent_30d - sessions_previous_30d)
        """).fetchone()[0]
        self.assertEqual(mismatches, 0, "activity_difference must match (recent - previous)")

    def test_days_since_last_event_bounds(self):
        # days_since_last_event must be >= 0 and <= 123 days
        row = self.con.execute(f"""
        SELECT 
            MIN(days_since_last_event), 
            MAX(days_since_last_event),
            COUNT(CASE WHEN days_since_last_event IS NULL THEN 1 END)
        FROM read_parquet('{CUSTOMER_PARQUET}')
        """).fetchone()
        self.assertGreaterEqual(row[0], 0.0)
        self.assertLessEqual(row[1], 123.0)
        self.assertEqual(row[2], 0, "Every customer must have non-null days_since_last_event")

    def test_monetary_per_session_consistency(self):
        # For buyers: monetary_per_session = monetary / frequency
        inconsistencies = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{BUYER_PARQUET}')
        WHERE ABS(monetary_per_session - ROUND(monetary / frequency, 2)) > 0.05
        """).fetchone()[0]
        self.assertEqual(inconsistencies, 0, "monetary_per_session must match monetary / frequency")

    def test_four_figures_generated(self):
        for fig_name in [
            "fig9_rfm_distributions.png",
            "fig10_engagement_distributions.png",
            "fig11_rfm_correlation_matrix.png",
            "fig12_buyer_vs_non_buyer_engagement.png"
        ]:
            fig_path = FIGURES_DIR / fig_name
            self.assertTrue(fig_path.is_file(), f"Missing figure: {fig_name}")
            self.assertGreater(fig_path.stat().st_size, 10000, f"Figure {fig_name} is too small (<10KB)")

    def test_feature_sets_f0_f1_f2_contract(self):
        proposed = self.manifest["proposed_feature_sets_for_phase4"]
        f0 = proposed["F0_traditional_rfm"]
        f1 = proposed["F1_rfm_plus_engagement"]
        f2 = proposed["F2_extended_behavioral"]

        self.assertEqual(f0, ["recency_days", "frequency", "monetary"])
        self.assertTrue(set(f0).issubset(set(f1)), "F1 must contain all F0 features")
        self.assertTrue(set(f1).issubset(set(f2)), "F2 must contain all F1 features")


if __name__ == "__main__":
    unittest.main()

