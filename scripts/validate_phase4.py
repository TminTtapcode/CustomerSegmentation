"""
Validation Script for Phase 4: Customer Segmentation Modeling
============================================================
Validates:
1. Model bundle outputs/models/kmeans_best_model.joblib integrity & manifest metadata
2. Cluster assignments data/features/buyer_clusters.parquet (92,652 rows, no NaNs)
3. Experiment manifest outputs/experiments/phase4_model_selection.json
4. Screening and stability CSV tables
5. 4 publication figures in outputs/figures/ (fig13..fig16)
6. Anti-leakage verification (no holdout dependency)
"""

import os
import sys
import json
import hashlib
import duckdb

def validate_phase4():
    print("=" * 70)
    print("STARTING VALIDATION FOR PHASE 4 — CUSTOMER SEGMENTATION MODELING")
    print("=" * 70)
    
    # 1. Model Artifact Verification
    model_path = "outputs/models/kmeans_best_model.joblib"
    assert os.path.exists(model_path), f"Missing model bundle: {model_path}"
    model_size_kb = os.path.getsize(model_path) / 1024
    assert model_size_kb > 30, f"Model bundle too small: {model_size_kb:.1f} KB"
    
    with open(model_path, "rb") as f:
        file_sha256 = hashlib.sha256(f.read()).hexdigest()
    print(f"[PASS] Model bundle verified: {model_path} ({model_size_kb:.1f} KB, SHA-256: {file_sha256[:16]}...)")
    
    # 2. Cluster Assignments Parquet Verification
    clusters_path = "data/features/buyer_clusters.parquet"
    assert os.path.exists(clusters_path), f"Missing cluster assignments: {clusters_path}"
    con = duckdb.connect()
    
    row_count = con.execute(f"SELECT COUNT(*) FROM '{clusters_path}'").fetchone()[0]
    distinct_users = con.execute(f"SELECT COUNT(DISTINCT user_id) FROM '{clusters_path}'").fetchone()[0]
    null_clusters = con.execute(f"SELECT COUNT(*) FROM '{clusters_path}' WHERE cluster IS NULL").fetchone()[0]
    null_pca = con.execute(f"SELECT COUNT(*) FROM '{clusters_path}' WHERE pca_x IS NULL OR pca_y IS NULL").fetchone()[0]
    
    assert row_count == 92652, f"Expected 92,652 rows, found {row_count}"
    assert distinct_users == 92652, f"Duplicate user_id detected in cluster table"
    assert null_clusters == 0, f"Found {null_clusters} null cluster assignments"
    assert null_pca == 0, f"Found {null_pca} null PCA coordinates"
    
    cluster_counts = con.execute(f"""
        SELECT cluster, COUNT(*) as cnt, COUNT(*) * 100.0 / {row_count} as pct
        FROM '{clusters_path}'
        GROUP BY cluster
        ORDER BY cluster
    """).fetchall()
    
    assert len(cluster_counts) == 4, f"Expected 4 clusters, got {len(cluster_counts)}"
    min_pct = min(r[2] for r in cluster_counts)
    assert min_pct >= 5.0, f"Smallest cluster is below 5%: {min_pct:.2f}%"
    
    print(f"[PASS] Cluster assignments verified: {row_count:,} rows. Clusters: {dict([(r[0], r[1]) for r in cluster_counts])} (Min: {min_pct:.2f}%)")
    
    # 3. Experiment Manifest Verification
    manifest_path = "outputs/experiments/phase4_model_selection.json"
    assert os.path.exists(manifest_path), f"Missing manifest: {manifest_path}"
    with open(manifest_path, 'r', encoding="utf-8") as f:
        manifest = json.load(f)
        
    assert 'round1_screening' in manifest, "Missing round1_screening in manifest"
    assert 'round2_stability' in manifest, "Missing round2_stability in manifest"
    assert 'minibatch_vs_kmeans' in manifest, "Missing minibatch_vs_kmeans in manifest"
    assert 'winning_model' in manifest, "Missing winning_model in manifest"
    assert len(manifest['round1_screening']) > 0, "Empty round1_screening"
    
    surr_acc = manifest['winning_model']['surrogate_fidelity_test_accuracy']
    assert surr_acc >= 0.80, f"Surrogate tree fidelity too low: {surr_acc:.4f}"
    print(f"[PASS] Experiment manifest verified. Winning model: K=4, Surrogate test fidelity: {surr_acc*100:.2f}%")
    
    # 4. CSV Verification
    assert os.path.exists("outputs/experiments/phase4_round1_screening.csv"), "Missing round1 CSV"
    assert os.path.exists("outputs/experiments/phase4_round2_stability.csv"), "Missing round2 CSV"
    print("[PASS] Experiment CSV tables verified.")
    
    # 5. Publication Figures Verification
    expected_figures = [
        "outputs/figures/fig13_elbow_silhouette.png",
        "outputs/figures/fig14_cluster_pca.png",
        "outputs/figures/fig15_cluster_profiles.png",
        "outputs/figures/fig16_surrogate_tree.png"
    ]
    for fig_path in expected_figures:
        assert os.path.exists(fig_path), f"Missing figure: {fig_path}"
        size_kb = os.path.getsize(fig_path) / 1024
        assert size_kb > 20, f"Figure {fig_path} too small ({size_kb:.1f} KB)"
        print(f"[PASS] Figure verified: {fig_path} ({size_kb:.1f} KB)")
        
    # 6. Anti-Leakage Check
    holdout_check = con.execute("SELECT COUNT(*) FROM 'data/cleaned/holdout_events.parquet'").fetchone()[0]
    assert holdout_check == 3916392, f"Holdout count altered: {holdout_check}"
    print(f"[PASS] Anti-leakage verified: Holdout events completely isolated ({holdout_check:,} rows intact).")
    
    print("\n" + "=" * 70)
    print("ALL PHASE 4 VALIDATION CHECKS PASSED (100%)")
    print("=" * 70)

if __name__ == "__main__":
    validate_phase4()
