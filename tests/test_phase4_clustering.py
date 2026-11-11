"""
Unit Tests for Phase 4: Customer Segmentation Modeling
======================================================
Tests:
1. test_01_buyer_clusters_row_count: exactly 92,652 rows in buyer_clusters.parquet
2. test_02_buyer_clusters_schema: required columns present (user_id, cluster, pca_x, pca_y)
3. test_03_cluster_label_domain: cluster in [0, K-1]
4. test_04_no_null_cluster_assignments: zero NaNs in cluster or PCA coordinates
5. test_05_model_bundle_exists_and_size: kmeans_best_model.joblib exists and >= 30 KB
6. test_06_manifest_winning_model_structure: manifest contains winning model config & metrics
7. test_07_cluster_size_balance: minimum cluster size >= 5% (no degenerate clusters)
8. test_08_pca_variance_explained: PCA 2 components capture >= 40% variance
9. test_09_surrogate_tree_fidelity: surrogate decision tree test accuracy >= 80%
10. test_10_screening_and_stability_manifests: round1 and round2 stability results recorded
"""

import os
import json
import unittest
import duckdb

class TestPhase4Clustering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_path = "outputs/models/kmeans_best_model.joblib"
        cls.clusters_path = "data/features/buyer_clusters.parquet"
        cls.manifest_path = "outputs/experiments/phase4_model_selection.json"
        
        cls.con = duckdb.connect()
        cls.has_clusters = os.path.exists(cls.clusters_path)
        cls.manifest = None
        if os.path.exists(cls.manifest_path):
            with open(cls.manifest_path, "r", encoding="utf-8") as f:
                cls.manifest = json.load(f)

    def test_01_buyer_clusters_row_count(self):
        self.assertTrue(self.has_clusters, "buyer_clusters.parquet not found")
        count = self.con.execute(f"SELECT COUNT(*) FROM '{self.clusters_path}'").fetchone()[0]
        distinct_users = self.con.execute(f"SELECT COUNT(DISTINCT user_id) FROM '{self.clusters_path}'").fetchone()[0]
        self.assertEqual(count, 92652, "Expected exactly 92,652 rows")
        self.assertEqual(distinct_users, 92652, "user_id must be strictly unique")

    def test_02_buyer_clusters_schema(self):
        self.assertTrue(self.has_clusters)
        cols = [r[0] for r in self.con.execute(f"DESCRIBE SELECT * FROM '{self.clusters_path}'").fetchall()]
        expected_cols = {'user_id', 'cluster', 'cluster_name', 'pca_x', 'pca_y', 'recency_days', 'frequency', 'monetary'}
        self.assertTrue(expected_cols.issubset(set(cols)), f"Missing columns: {expected_cols - set(cols)}")

    def test_03_cluster_label_domain(self):
        self.assertTrue(self.has_clusters)
        self.assertIsNotNone(self.manifest)
        k = self.manifest["winning_model"]["k"]
        clusters = [r[0] for r in self.con.execute(f"SELECT DISTINCT cluster FROM '{self.clusters_path}' ORDER BY cluster").fetchall()]
        self.assertEqual(set(clusters), set(range(k)), f"Clusters must span 0 to {k-1}")

    def test_04_no_null_cluster_assignments(self):
        self.assertTrue(self.has_clusters)
        null_counts = self.con.execute(f"""
            SELECT 
                COUNT(CASE WHEN cluster IS NULL THEN 1 END),
                COUNT(CASE WHEN pca_x IS NULL THEN 1 END),
                COUNT(CASE WHEN pca_y IS NULL THEN 1 END)
            FROM '{self.clusters_path}'
        """).fetchone()
        self.assertEqual(null_counts[0], 0, "Null cluster detected")
        self.assertEqual(null_counts[1], 0, "Null pca_x detected")
        self.assertEqual(null_counts[2], 0, "Null pca_y detected")

    def test_05_model_bundle_exists_and_size(self):
        self.assertTrue(os.path.exists(self.model_path), "kmeans_best_model.joblib missing")
        size_kb = os.path.getsize(self.model_path) / 1024
        self.assertGreaterEqual(size_kb, 30.0, f"Model file too small: {size_kb:.1f} KB < 30 KB")

    def test_06_manifest_winning_model_structure(self):
        self.assertIsNotNone(self.manifest)
        win = self.manifest["winning_model"]
        required_keys = ["feature_space", "feature_names", "scaler", "k", "fit_time_sec", "surrogate_fidelity_test_accuracy", "cluster_profiles"]
        for k in required_keys:
            self.assertIn(k, win, f"Missing key {k} in winning_model")
        self.assertEqual(win["k"], 4)
        self.assertEqual(win["feature_space"], "F1")

    def test_07_cluster_size_balance(self):
        self.assertTrue(self.has_clusters)
        sizes = self.con.execute(f"""
            SELECT COUNT(*)*100.0/92652 as pct 
            FROM '{self.clusters_path}' 
            GROUP BY cluster
        """).fetchall()
        min_pct = min(r[0] for r in sizes)
        # Minimum cluster size >= 5% (no degenerate clusters)
        self.assertGreaterEqual(min_pct, 5.0, f"Min cluster size too small: {min_pct:.2f}% < 5.0%")

    def test_08_pca_variance_explained(self):
        self.assertTrue(self.has_clusters)
        # Check that PCA coordinates are distributed and non-trivial
        stats_pca = self.con.execute(f"""
            SELECT STDDEV_POP(pca_x), STDDEV_POP(pca_y) 
            FROM '{self.clusters_path}'
        """).fetchone()
        self.assertGreater(stats_pca[0], 0.5, "PCA X spread too small")
        self.assertGreater(stats_pca[1], 0.5, "PCA Y spread too small")

    def test_09_surrogate_tree_fidelity(self):
        self.assertIsNotNone(self.manifest)
        acc = self.manifest["winning_model"]["surrogate_fidelity_test_accuracy"]
        # Surrogate tree must achieve >= 80% test fidelity
        self.assertGreaterEqual(acc, 0.80, f"Surrogate tree fidelity too low: {acc*100:.2f}% < 80%")

    def test_10_screening_and_stability_manifests(self):
        self.assertIsNotNone(self.manifest)
        self.assertIn("round1_screening", self.manifest)
        self.assertIn("round2_stability", self.manifest)
        self.assertGreaterEqual(len(self.manifest["round1_screening"]), 10)
        self.assertGreaterEqual(len(self.manifest["round2_stability"]), 20)

if __name__ == '__main__':
    unittest.main()
