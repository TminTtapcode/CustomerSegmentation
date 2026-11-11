import os, sys, hashlib, time
import numpy as np
import duckdb
import joblib.numpy_pickle as jnp

sys.path.insert(0, os.path.abspath("."))
from scripts.smoke_test_model_inference import SafeNumpyUnpickler

model_path = "outputs/models/kmeans_best_model.joblib"
with open(model_path, "rb") as f:
    with jnp._validate_fileobject_and_memmap(f, model_path, None) as (fobj, val_mmap):
        unpickler = SafeNumpyUnpickler(model_path, fobj, True, mmap_mode=val_mmap)
        bundle = unpickler.load()

print("Feature names in bundle:", bundle["feature_names"])
print("Log1p candidates in bundle:", bundle["log1p_candidates"])
print("Scaler mean:", bundle["scaler"].mean_)
print("Scaler scale:", bundle["scaler"].scale_)
print("Cluster centers shape:", bundle["model"].cluster_centers_.shape)

# Now let's test across ALL 92,652 buyers
t0 = time.perf_counter()
con = duckdb.connect()
feat_names = bundle["feature_names"]
log1p_feats = bundle["log1p_candidates"]
centers = bundle["model"].cluster_centers_
mean = bundle["scaler"].mean_
scale = bundle["scaler"].scale_

all_data = con.execute('''
    SELECT f.user_id, f.recency_days, f.frequency, f.monetary, 
           f.sessions_30d, f.views_30d, f.cart_sessions_30d, f.log_activity_ratio,
           c.cluster as expected_cluster
    FROM 'data/features/buyer_features.parquet' f
    JOIN 'data/features/buyer_clusters.parquet' c ON f.user_id = c.user_id
    ORDER BY f.user_id
''').fetchall()

print(f"Loaded {len(all_data):,} buyers in {time.perf_counter() - t0:.2f}s")
X_raw = np.array([[r[1], r[2], r[3], r[4], r[5], r[6], r[7]] for r in all_data], dtype=np.float64)
expected_clusters = np.array([r[8] for r in all_data], dtype=np.int32)

# Transform
X_tf = X_raw.copy()
for i, name in enumerate(feat_names):
    if name in log1p_feats:
        X_tf[:, i] = np.log1p(np.maximum(X_tf[:, i], 0.0))

X_scaled = (X_tf - mean) / scale

# Distance calculation
dists = np.sum((X_scaled[:, None, :] - centers[None, :, :]) ** 2, axis=2)
predicted_clusters = np.argmin(dists, axis=1)

matches = np.sum(predicted_clusters == expected_clusters)
print(f"Total buyers: {len(expected_clusters)}")
print(f"Matches: {matches} ({matches / len(expected_clusters) * 100:.4f}%)")
assert matches == len(expected_clusters), f"Mismatch: {matches} != {len(expected_clusters)}"
print("ALL 92,652 BUYERS MATCH PERFECTLY!")

