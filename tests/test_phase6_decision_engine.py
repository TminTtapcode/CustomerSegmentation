"""
Unit Tests for Phase 6: Marketing Decision Support Engine
=========================================================
Tests:
1. test_01_ruleset_structure: Config file has 7 goals, 8 tactics, guardrails, non_buyer_tiers
2. test_02_buyer_recommendations_count_and_schema: 92,652 buyers, required columns, cohort='BUYER'
3. test_03_non_buyer_recommendations_count_and_schema: 1,248,847 non-buyers, required columns
4. test_04_customer_population_conservation: 92,652 + 1,248,847 = 1,341,499 exactly
5. test_05_non_static_segment_diversity: Each buyer cluster receives >= 3 distinct tactics
6. test_06_non_buyer_tiering_coverage: All 4 non-buyer tiers present, no NULL tiers
7. test_07_guardrail_g1_consent_pending: 100% of rows have eligibility_status='PENDING_CONSENT'
8. test_08_guardrail_g3_budget_protection: Deep dormant buyers receive TAC_NO_ACTION
9. test_09_guardrail_g4_cart_precedence: Users with recent cart additions prioritized for TAC_CART_RECOVERY
10. test_10_guardrail_g5_non_buyer_fatigue: Inactive non-buyers receive TAC_NO_ACTION
11. test_11_explainability_contract_traceability: Valid reason_codes and primary_kpi
12. test_12_decision_rules_deterministic_and_reproducible: Rule evaluation is strictly deterministic
"""

import os
import json
import unittest
import duckdb
from src.decision_engine.rules import MarketingDecisionRules, load_marketing_rules

class TestPhase6DecisionEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules_path = "configs/marketing_rules.yaml"
        cls.buyer_rec_path = "outputs/recommendations/buyer_recommendations.parquet"
        cls.nb_rec_path = "outputs/recommendations/non_buyer_recommendations.parquet"
        cls.summary_path = "outputs/experiments/phase6_decision_support_summary.json"
        
        cls.con = duckdb.connect()
        cls.has_buyer_recs = os.path.exists(cls.buyer_rec_path)
        cls.has_nb_recs = os.path.exists(cls.nb_rec_path)
        cls.has_summary = os.path.exists(cls.summary_path)

    def test_01_ruleset_structure(self):
        rules = load_marketing_rules(self.rules_path)
        self.assertIn("marketing_goals", rules)
        self.assertIn("candidate_tactics", rules)
        self.assertIn("guardrails", rules)
        self.assertIn("non_buyer_tiering_rules", rules)
        
        self.assertEqual(len(rules["marketing_goals"]), 7, "Must contain exactly 7 marketing goals")
        self.assertEqual(len(rules["candidate_tactics"]), 8, "Must contain exactly 8 candidate tactics")
        self.assertEqual(len(rules["non_buyer_tiering_rules"]), 4, "Must contain exactly 4 non-buyer tiers")

    def test_02_buyer_recommendations_count_and_schema(self):
        self.assertTrue(self.has_buyer_recs, "Missing buyer recommendations parquet")
        count = self.con.execute(f"SELECT COUNT(*) FROM '{self.buyer_rec_path}'").fetchone()[0]
        self.assertEqual(count, 92652, f"Expected 92,652 buyers, got {count}")
        
        cols = [r[0] for r in self.con.execute(f"DESCRIBE SELECT * FROM '{self.buyer_rec_path}'").fetchall()]
        required = {'user_id', 'cohort', 'segment_id', 'marketing_goal', 'recommended_tactic', 'reason_codes', 'guardrails_applied', 'primary_kpi', 'eligibility_status'}
        self.assertTrue(required.issubset(set(cols)), f"Missing columns in buyer recommendations: {required - set(cols)}")
        
        null_user_count = self.con.execute(f"SELECT COUNT(*) FROM '{self.buyer_rec_path}' WHERE user_id IS NULL").fetchone()[0]
        self.assertEqual(null_user_count, 0, "Found null user_id in buyer recommendations")

    def test_03_non_buyer_recommendations_count_and_schema(self):
        self.assertTrue(self.has_nb_recs, "Missing non-buyer recommendations parquet")
        count = self.con.execute(f"SELECT COUNT(*) FROM '{self.nb_rec_path}'").fetchone()[0]
        self.assertEqual(count, 1248847, f"Expected 1,248,847 non-buyers, got {count}")
        
        cols = [r[0] for r in self.con.execute(f"DESCRIBE SELECT * FROM '{self.nb_rec_path}'").fetchall()]
        required = {'user_id', 'cohort', 'segment_id', 'engagement_tier', 'marketing_goal', 'recommended_tactic', 'reason_codes', 'guardrails_applied', 'primary_kpi'}
        self.assertTrue(required.issubset(set(cols)), f"Missing columns in non-buyer recommendations: {required - set(cols)}")

    def test_04_customer_population_conservation(self):
        self.assertTrue(self.has_buyer_recs and self.has_nb_recs)
        b_cnt = self.con.execute(f"SELECT COUNT(*) FROM '{self.buyer_rec_path}'").fetchone()[0]
        nb_cnt = self.con.execute(f"SELECT COUNT(*) FROM '{self.nb_rec_path}'").fetchone()[0]
        total = b_cnt + nb_cnt
        self.assertEqual(total, 1341499, f"Population mismatch: {total} != 1,341,499")

    def test_05_non_static_segment_diversity(self):
        """Validates that each buyer cluster receives >= 3 distinct tactics (proves non-static mapping)"""
        self.assertTrue(self.has_buyer_recs)
        tactic_counts_per_cluster = self.con.execute(f"""
            SELECT cluster_id, COUNT(DISTINCT recommended_tactic) as tactic_count
            FROM '{self.buyer_rec_path}'
            GROUP BY cluster_id
            ORDER BY cluster_id
        """).fetchall()
        
        self.assertEqual(len(tactic_counts_per_cluster), 4, "Must have exactly 4 buyer clusters")
        for cid, t_count in tactic_counts_per_cluster:
            self.assertGreaterEqual(t_count, 3, f"Cluster {cid} has only {t_count} tactics. Must be dynamic (>=3)")

    def test_06_non_buyer_tiering_coverage(self):
        self.assertTrue(self.has_nb_recs)
        tiers = self.con.execute(f"""
            SELECT engagement_tier, COUNT(*) 
            FROM '{self.nb_rec_path}' 
            GROUP BY 1 
            ORDER BY 2 DESC
        """).fetchall()
        
        tier_names = set(r[0] for r in tiers)
        expected_tiers = {'HIGH_INTENT', 'EXPLORING', 'LOW_ENGAGEMENT', 'INACTIVE'}
        self.assertEqual(tier_names, expected_tiers, f"Tier mismatch: {tier_names}")

    def test_07_guardrail_g1_consent_pending(self):
        self.assertTrue(self.has_buyer_recs and self.has_nb_recs)
        non_pending_buyers = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.buyer_rec_path}' WHERE eligibility_status != 'PENDING_CONSENT'
        """).fetchone()[0]
        non_pending_nb = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.nb_rec_path}' WHERE eligibility_status != 'PENDING_CONSENT'
        """).fetchone()[0]
        self.assertEqual(non_pending_buyers + non_pending_nb, 0, "All recommendations must be PENDING_CONSENT")

    def test_08_guardrail_g3_budget_protection(self):
        self.assertTrue(self.has_buyer_recs)
        # Deep dormant with monetary < 20 and recency > 90 must receive TAC_NO_ACTION
        check = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.buyer_rec_path}'
            WHERE recency_days > 90.0 AND monetary < 20.0 AND sessions_30d = 0
              AND recommended_tactic != 'TAC_NO_ACTION'
        """).fetchone()[0]
        self.assertEqual(check, 0, f"Found {check} deep dormant buyers who were not suppressed by G3")

    def test_09_guardrail_g4_cart_precedence(self):
        self.assertTrue(self.has_buyer_recs)
        # Non-VIP buyers with cart_sessions_30d >= 1 must receive TAC_CART_RECOVERY
        check = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.buyer_rec_path}'
            WHERE cluster_id IN (0, 2, 3) AND cart_sessions_30d >= 1
              AND recommended_tactic != 'TAC_CART_RECOVERY'
        """).fetchone()[0]
        self.assertEqual(check, 0, f"Found {check} cart buyers in C0/C2/C3 without TAC_CART_RECOVERY")

    def test_10_guardrail_g5_non_buyer_fatigue(self):
        self.assertTrue(self.has_nb_recs)
        # Inactive non-buyers (sessions_30d = 0) must receive TAC_NO_ACTION
        check = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.nb_rec_path}'
            WHERE sessions_30d = 0 AND recommended_tactic != 'TAC_NO_ACTION'
        """).fetchone()[0]
        self.assertEqual(check, 0, f"Found {check} inactive non-buyers without TAC_NO_ACTION")

    def test_11_explainability_contract_traceability(self):
        self.assertTrue(self.has_buyer_recs and self.has_nb_recs)
        # Check that primary_kpi and reason_codes are non-empty
        empty_reason_b = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.buyer_rec_path}' WHERE reason_codes IS NULL OR reason_codes = ''
        """).fetchone()[0]
        empty_kpi_b = self.con.execute(f"""
            SELECT COUNT(*) FROM '{self.buyer_rec_path}' WHERE primary_kpi IS NULL OR primary_kpi = ''
        """).fetchone()[0]
        self.assertEqual(empty_reason_b, 0, "Found empty reason_codes in buyers")
        self.assertEqual(empty_kpi_b, 0, "Found empty primary_kpi in buyers")

    def test_12_decision_rules_deterministic_and_reproducible(self):
        engine = MarketingDecisionRules(self.rules_path)
        sample_ev = {
            "user_id": "TEST_DETERMINISTIC_USER",
            "is_buyer": True,
            "cluster": 1,
            "recency_days": 15.0,
            "frequency": 3,
            "monetary": 115.0,
            "sessions_30d": 5,
            "views_30d": 20,
            "cart_sessions_30d": 1,
            "log_activity_ratio": 0.8
        }
        res1 = engine.evaluate_customer(sample_ev)
        res2 = engine.evaluate_customer(sample_ev)
        
        self.assertEqual(res1["recommended_tactic"], res2["recommended_tactic"])
        self.assertEqual(res1["marketing_goal"], res2["marketing_goal"])
        self.assertEqual(res1["reason_codes"], res2["reason_codes"])
        self.assertEqual(res1["guardrails_applied"], res2["guardrails_applied"])

if __name__ == "__main__":
    unittest.main()

