"""Unit and Data Validation Tests for Phase 1 — Data Understanding & Profiling."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
PROFILE_JSON = ROOT / "outputs" / "experiments" / "phase1_data_profile.json"
FIGURES_DIR = ROOT / "outputs" / "figures"


class TestPhase1DataStructure(unittest.TestCase):
    """Test structural presence, schemas, and file existence."""

    def test_raw_files_exist(self):
        expected_files = [
            "2019-Oct.csv",
            "2019-Nov.csv",
            "2019-Dec.csv",
            "2020-Jan.csv",
            "2020-Feb.csv",
        ]
        for fname in expected_files:
            fpath = DATA_RAW / fname
            self.assertTrue(fpath.is_file(), f"Missing required raw CSV: {fname}")
            self.assertGreater(fpath.stat().st_size, 100 * 1024 * 1024, f"File {fname} is too small (<100MB)")

    def test_profile_json_valid(self):
        self.assertTrue(PROFILE_JSON.is_file(), "phase1_data_profile.json does not exist")
        with open(PROFILE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["phase"], "P1_DATA_UNDERSTANDING")
        self.assertEqual(data["global_statistics"]["total_rows"], 20692840)

    def test_eight_eda_figures_generated(self):
        expected_figures = [
            "fig1_event_type_distribution.png",
            "fig2_daily_monthly_volume.png",
            "fig3_unique_users_sessions_over_time.png",
            "fig4_user_activity_distribution.png",
            "fig5_purchase_behavior_distribution.png",
            "fig6_session_funnel.png",
            "fig7_missing_values_by_month.png",
            "fig8_price_distribution.png",
        ]
        for fig_name in expected_figures:
            fig_path = FIGURES_DIR / fig_name
            self.assertTrue(fig_path.is_file(), f"Missing EDA figure: {fig_name}")
            self.assertGreater(fig_path.stat().st_size, 5000, f"Figure {fig_name} is corrupted/empty")


class TestPhase1DataQualityAssumptions(unittest.TestCase):
    """Verify assumptions made in Phase 0 against actual REES46 experimental profile."""

    @classmethod
    def setUpClass(cls):
        with open(PROFILE_JSON, "r", encoding="utf-8") as f:
            cls.profile = json.load(f)

    def test_zero_missing_user_id(self):
        # Assumption: user_id is well tracked
        self.assertEqual(self.profile["global_statistics"]["missing_user_id_count"], 0)

    def test_purchase_session_proxy_validity(self):
        # Critical assumption from Phase 0: purchase events have sessions so proxy works
        missing_pur_session = self.profile["global_statistics"]["purchase_missing_session_count"]
        self.assertEqual(missing_pur_session, 0, "No purchase events should miss session ID")
        # Ratio of purchase items per session should be significantly > 1
        ratio = self.profile["global_statistics"]["items_per_purchase_session"]
        self.assertGreater(ratio, 5.0, "Items per purchase session should reflect basket-level transactions")

    def test_temporal_split_integrity(self):
        # Anti-leakage: observation + holdout must equal total rows
        split = self.profile["temporal_split"]
        total = self.profile["global_statistics"]["total_rows"]
        self.assertEqual(split["before_observation"], 0)
        self.assertEqual(split["after_holdout"], 0)
        self.assertEqual(split["observation_events"] + split["holdout_events"], total)

    def test_cohort_volumes_sufficient_for_modeling(self):
        # Buyer cohort must have sufficient volume (>50k) for robust K-Means
        buyers = self.profile["observation_cohort"]["buyers_count"]
        non_buyers = self.profile["observation_cohort"]["non_buyers_count"]
        self.assertGreater(buyers, 50000, "Buyers count should be substantial for K-Means")
        self.assertGreater(non_buyers, 500000, "Non-buyers count should be large for engagement stratification")

    def test_price_anomalies_flagged(self):
        # Confirm that negative and zero prices are detected and flagged for Phase 2
        p_neg = self.profile["global_statistics"]["price_negative_count"]
        p_zero = self.profile["global_statistics"]["price_zero_count"]
        self.assertGreater(p_neg, 0, "Negative prices exist and must be cleaned in Phase 2")
        self.assertGreater(p_zero, 0, "Zero prices exist and must be cleaned in Phase 2")


class TestPhase1Performance(unittest.TestCase):
    """Verify performance metrics against machine capacities."""

    @classmethod
    def setUpClass(cls):
        with open(PROFILE_JSON, "r", encoding="utf-8") as f:
            cls.perf = json.load(f)["performance"]

    def test_profiling_runtime_and_throughput(self):
        # Wall clock should be under 180s for 20.7M rows on DuckDB
        self.assertLess(self.perf["wall_time_seconds"], 180.0)
        self.assertGreater(self.perf["throughput_rows_per_second"], 100000.0)

    def test_peak_memory_within_safe_limits(self):
        # Peak RSS should remain within 2.5 GB to prevent OOM
        self.assertLess(self.perf["peak_rss_mb"], 2500.0)


if __name__ == "__main__":
    unittest.main()
