"""Unit and Integration Tests for Phase 2 — Data Preparation & Cleaning."""
import json
import unittest
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATA_CLEANED = ROOT / "data" / "cleaned"
OBS_PARQUET = str(DATA_CLEANED / "observation_events.parquet").replace("\\", "/")
HOLDOUT_PARQUET = str(DATA_CLEANED / "holdout_events.parquet").replace("\\", "/")
CLEAN_PARQUET = str(DATA_CLEANED / "clean_events.parquet").replace("\\", "/")
MANIFEST_JSON = ROOT / "outputs" / "experiments" / "phase2_data_cleaning.json"


class TestPhase2DataPreparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = duckdb.connect(database=":memory:")
        cls.con.execute("SET threads = 4")
        with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_parquet_files_exist(self):
        for fname in ["clean_events.parquet", "observation_events.parquet", "holdout_events.parquet"]:
            fpath = DATA_CLEANED / fname
            self.assertTrue(fpath.is_file(), f"Missing clean Parquet: {fname}")
            self.assertGreater(fpath.stat().st_size, 50 * 1024 * 1024, f"File {fname} is unexpectedly small")

    def test_reconciliation_counts(self):
        rec = self.manifest["reconciliation"]
        raw_total = rec["raw_rows_total"]
        dedup_removed = rec["exact_duplicates_removed"]
        clean_total = rec["clean_distinct_rows"]
        obs_rows = rec["clean_observation_rows"]
        holdout_rows = rec["clean_holdout_rows"]

        self.assertEqual(raw_total, 20692840)
        self.assertEqual(dedup_removed, 1109098)
        self.assertEqual(clean_total, 19583742)
        self.assertEqual(raw_total - dedup_removed, clean_total)
        self.assertEqual(obs_rows + holdout_rows, clean_total)
        self.assertEqual(obs_rows, 15667350)
        self.assertEqual(holdout_rows, 3916392)

    def test_strict_temporal_split_anti_leakage(self):
        obs_max = self.con.execute(f"SELECT MAX(event_time) FROM read_parquet('{OBS_PARQUET}')").fetchone()[0]
        holdout_min = self.con.execute(f"SELECT MIN(event_time) FROM read_parquet('{HOLDOUT_PARQUET}')").fetchone()[0]

        # Observation must strictly end before 2020-02-01 00:00:00
        self.assertLess(str(obs_max), "2020-02-01 00:00:00")
        # Holdout must strictly start on or after 2020-02-01 00:00:00
        self.assertGreaterEqual(str(holdout_min), "2020-02-01 00:00:00")

        # Zero purchase events in observation on or after cutoff
        future_purchases_in_obs = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{OBS_PARQUET}')
        WHERE event_time >= '2020-02-01 00:00:00' AND event_type = 'purchase'
        """).fetchone()[0]
        self.assertEqual(future_purchases_in_obs, 0)

    def test_composite_session_key_uniqueness(self):
        # Composite key user_session_id must resolve all 331 collisions across different users
        collisions = self.con.execute(f"""
        SELECT COUNT(*) FROM (
            SELECT user_session_id
            FROM read_parquet('{CLEAN_PARQUET}')
            WHERE user_session_id IS NOT NULL
            GROUP BY user_session_id
            HAVING COUNT(DISTINCT user_id) > 1
        )
        """).fetchone()[0]
        self.assertEqual(collisions, 0, "user_session_id composite key must have 0 user collisions")

    def test_monetary_exclusion_policy(self):
        # Events with is_valid_for_monetary = TRUE must be purchase AND price > 0
        invalid_flagged_as_valid = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}')
        WHERE is_valid_for_monetary = TRUE AND (event_type != 'purchase' OR price <= 0)
        """).fetchone()[0]
        self.assertEqual(invalid_flagged_as_valid, 0, "No non-purchase or zero/negative price should be valid for monetary")

        # All purchase events with price <= 0 must have is_valid_for_monetary = FALSE
        non_monetary_purchases = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}')
        WHERE event_type = 'purchase' AND price <= 0 AND is_valid_for_monetary = TRUE
        """).fetchone()[0]
        self.assertEqual(non_monetary_purchases, 0)

    def test_engagement_preservation_policy(self):
        # Views with price = 0 must be preserved and flagged is_valid_for_engagement = TRUE
        preserved_zero_views = self.con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}')
        WHERE event_type = 'view' AND price = 0 AND is_valid_for_engagement = TRUE
        """).fetchone()[0]
        self.assertGreater(preserved_zero_views, 25000, "Zero-price views must be preserved for engagement")

    def test_brand_and_category_fallbacks(self):
        # brand and category_code must not contain NULL in clean Parquet (replaced with 'unknown')
        null_brands = self.con.execute(f"SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}') WHERE brand IS NULL").fetchone()[0]
        null_categories = self.con.execute(f"SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}') WHERE category_code IS NULL").fetchone()[0]
        self.assertEqual(null_brands, 0)
        self.assertEqual(null_categories, 0)

    def test_empirical_speedup_recorded(self):
        speedup = self.manifest["performance"]["empirical_speedup_parquet_vs_csv"]
        self.assertGreater(speedup, 2.0, "Parquet must demonstrate measurable empirical query speedup over CSV")

    def test_independent_quality_flags_present(self):
        # Clean Parquet must have 4 independent boolean flags
        row = self.con.execute(f"""
        SELECT 
            COUNT(CASE WHEN is_missing_brand THEN 1 END) AS missing_brand_cnt,
            COUNT(CASE WHEN is_missing_category_code THEN 1 END) AS missing_cat_cnt,
            COUNT(CASE WHEN is_invalid_price THEN 1 END) AS invalid_price_cnt,
            COUNT(CASE WHEN is_missing_session THEN 1 END) AS missing_session_cnt
        FROM read_parquet('{CLEAN_PARQUET}')
        """).fetchone()
        self.assertGreater(row[0], 8000000, "Missing brand flag must identify >8M rows")
        self.assertGreater(row[1], 19000000, "Missing category flag must identify >19M rows")
        self.assertGreater(row[2], 86000, "Invalid price flag must identify >86k rows")
        self.assertEqual(row[3], 4085, "Missing session flag must identify exactly 4085 clean rows")

    def test_zero_session_loss_reconciliation(self):
        s_rec = self.manifest["session_reconciliation"]
        self.assertEqual(s_rec["session_uuid_delta"], 0, "Zero session UUIDs lost after deduplication")
        self.assertEqual(s_rec["composite_session_delta"], 0, "Zero composite sessions lost after deduplication")
        self.assertEqual(s_rec["distinct_session_uuids_clean"], 4535941)
        self.assertEqual(s_rec["distinct_composite_sessions_clean_non_null"], 4536272)
        self.assertEqual(s_rec["users_with_null_session_raw"], 1533)

    def test_monetary_three_step_reconciliation(self):
        m_rec = self.manifest["monetary_3step_reconciliation"]
        self.assertEqual(m_rec["step1_raw_purchase_events"], 1045014)
        self.assertEqual(m_rec["step2_dedup_purchase_events"], 1044221)
        self.assertEqual(m_rec["step3_valid_monetary_events"], 1044133)
        self.assertAlmostEqual(m_rec["step2_dedup_delta"], -3091.64, places=2)
        self.assertAlmostEqual(m_rec["step3_invalid_price_delta"], 2642.88, places=2)
        self.assertEqual(m_rec["step3_invalid_purchases_excluded"], 88)

    def test_fair_benchmark_recorded(self):
        fb = self.manifest["fair_benchmark"]
        self.assertGreater(fb["fair_speedup_median"], 5.0, "Fair benchmark median speedup must be > 5.0x")
        self.assertGreater(fb["fair_speedup_cold"], 4.0, "Fair benchmark cold speedup must be > 4.0x")
        self.assertEqual(fb["comparison_record_set"], "EXACT SAME 19,583,742 clean rows on both CSV and Parquet")


if __name__ == "__main__":
    unittest.main()

