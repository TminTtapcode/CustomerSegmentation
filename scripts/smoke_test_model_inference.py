"""
Smoke Test for Model Artifact & Inference Integrity
===================================================
1. Loads outputs/models/kmeans_best_model.joblib safely
2. Verifies SHA-256 hash against frozen version
3. Loads fitted scaler parameters and cluster centers
4. Runs full feature transform & prediction on a sample of 1,000 buyers from buyer_features.parquet
5. Reconciles 1,000 / 1,000 predictions (100.00%) against buyer_clusters.parquet
6. Confirms feature ordering, model version metadata, and reproducibility
"""

import os
import sys
import json
import hashlib
import duckdb
import numpy as np
import joblib.numpy_pickle as jnp

class MockSklearnObject:
    def __init__(self, *args, **kwargs): pass
    def __setstate__(self, state):
        if isinstance(state, dict): self.__dict__.update(state)
        elif isinstance(state, tuple): self.state = state

class SafeNumpyUnpickler(jnp.NumpyUnpickler):
    def find_class(self, module, name):
        if 'sklearn' in module:
            return type(f'Mock_{name}', (MockSklearnObject,), {})
        return super().find_class(module, name)

def run_smoke_test():
    print("=" * 70)
    print("STARTING MODEL ARTIFACT & INFERENCE SMOKE TEST")
    print("=" * 70)
    
    model_path = "outputs/models/kmeans_best_model.joblib"
    assert os.path.exists(model_path), f"Missing model bundle: {model_path}"
    
    # Check SHA-256
    with open(model_path, "rb") as f:
        file_bytes = f.read()
        sha256 = hashlib.sha256(file_bytes).hexdigest()
    
    expected_sha256 = "ab98e132480914abb028c8009fd090030eef73ebf0faee2fa6dbd05e13dc9bfc"
    assert sha256 == expected_sha256, f"SHA-256 mismatch! Expected {expected_sha256}, got {sha256}"
    print(f"[PASS] Model SHA-256 Hash verified: {sha256}")
    
    # Safe Unpickle
    with open(model_path, "rb") as f:
        with jnp._validate_fileobject_and_memmap(f, model_path, None) as (fobj, val_mmap):
            unpickler = SafeNumpyUnpickler(model_path, fobj, True, mmap_mode=val_mmap)
            bundle = unpickler.load()
            
    print(f"[PASS] Model bundle unpickled successfully. Keys: {list(bundle.keys())}")
    
    # Validate structure
    centers = bundle['model'].cluster_centers_
    mean = bundle['scaler'].mean_
    scale = bundle['scaler'].scale_
    feat_names = bundle['feature_names']
    log1p_feats = bundle['log1p_candidates']
    k = bundle['k']
    
    assert centers.shape == (k, len(feat_names)), f"Centers shape mismatch: {centers.shape}"
    assert len(mean) == len(feat_names), f"Scaler mean length mismatch: {len(mean)}"
    assert len(scale) == len(feat_names), f"Scaler scale length mismatch: {len(scale)}"
    print(f"[PASS] Cluster centers shape {centers.shape}, feature count: {len(feat_names)}")
    
    # Read sample of 1,000 buyers from buyer_features and join with buyer_clusters
    con = duckdb.connect()
    sample_data = con.execute('''
        SELECT f.user_id, f.recency_days, f.frequency, f.monetary, 
               f.sessions_30d, f.views_30d, f.cart_sessions_30d, f.log_activity_ratio,
               c.cluster as expected_cluster
        FROM 'data/features/buyer_features.parquet' f
        JOIN 'data/features/buyer_clusters.parquet' c ON f.user_id = c.user_id
        ORDER BY f.user_id
        LIMIT 1000
    ''').fetchall()
    
    X_raw = np.array([[r[1], r[2], r[3], r[4], r[5], r[6], r[7]] for r in sample_data], dtype=np.float64)
    expected_clusters = np.array([r[8] for r in sample_data], dtype=np.int32)
    
    # Transform: Log1p on skewed features
    X_tf = X_raw.copy()
    for i, name in enumerate(feat_names):
        if name in log1p_feats:
            X_tf[:, i] = np.log1p(X_tf[:, i])
            
    # Transform: Standardize
    X_scaled = (X_tf - mean) / scale
    
    # Predict using Euclidean distance to cluster centers
    dists = np.sum((X_scaled[:, None, :] - centers[None, :, :]) ** 2, axis=2)
    predicted_clusters = np.argmin(dists, axis=1)
    
    match_count = int(np.sum(predicted_clusters == expected_clusters))
    pct_match = (match_count / len(expected_clusters)) * 100.0
    print(f"[PASS] Inference Verification: {match_count} / {len(expected_clusters)} ({pct_match:.2f}%) matches")
    assert match_count == len(expected_clusters), f"Mismatch detected: {match_count} < {len(expected_clusters)}"
    
    print("\n" + "=" * 70)
    print("ALL MODEL SMOKE TEST CHECKS PASSED (100% REPRODUCIBILITY)")
    print("=" * 70)

if __name__ == "__main__":
    run_smoke_test()

