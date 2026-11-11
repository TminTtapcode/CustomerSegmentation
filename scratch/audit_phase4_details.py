import duckdb
import pyarrow as pa
import numpy as np

con = duckdb.connect()

print("=== 1. AUDIT DUPLICATE PURCHASES: 905 vs 793 ===")
query_dup_raw = """
WITH ranked AS (
    SELECT 
        event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session,
        CASE WHEN event_time < '2020-02-01T00:00:00Z' THEN 'observation' ELSE 'holdout' END as partition_name,
        ROW_NUMBER() OVER (
            PARTITION BY event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session
            ORDER BY event_time
        ) as rn
    FROM read_csv_auto('data/raw/*.csv')
    WHERE event_type = 'purchase'
)
SELECT 
    partition_name,
    COUNT(*) as total_purchases,
    COUNT(CASE WHEN rn = 1 THEN 1 END) as unique_purchases,
    COUNT(CASE WHEN rn > 1 THEN 1 END) as duplicate_purchases
FROM ranked
GROUP BY partition_name
UNION ALL
SELECT 
    'TOTAL' as partition_name,
    COUNT(*) as total_purchases,
    COUNT(CASE WHEN rn = 1 THEN 1 END) as unique_purchases,
    COUNT(CASE WHEN rn > 1 THEN 1 END) as duplicate_purchases
FROM ranked
ORDER BY partition_name
"""
tbl = con.execute(query_dup_raw).to_arrow_table()
for i in range(tbl.num_rows):
    row = {col: tbl[col][i].as_py() for col in tbl.column_names}
    print(row)

print("\n=== 2. AUDIT CANDIDATE PROFILES: F1-Std-K3 vs F1-Std-K4 vs F1-Rob-K4 ===")
import joblib
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, RobustScaler

# Load buyers feature table using DuckDB into Arrow / NumPy
buyers_arrow = con.execute("SELECT * FROM 'data/features/buyer_features.parquet'").to_arrow_table()
print(f"Loaded {buyers_arrow.num_rows:,} buyers")

F1_COLS = ['recency_days', 'frequency', 'monetary', 'sessions_30d', 'views_30d', 'cart_sessions_30d', 'log_activity_ratio']
LOG1P_COLS = ['frequency', 'monetary', 'sessions_30d', 'views_30d', 'cart_sessions_30d']

# Extract columns as numpy arrays
X_raw = np.column_stack([buyers_arrow[col].to_numpy() for col in F1_COLS])
X_trans = X_raw.copy()
for idx, col in enumerate(F1_COLS):
    if col in LOG1P_COLS:
        X_trans[:, idx] = np.log1p(np.maximum(X_trans[:, idx], 0.0))

scaler_std = StandardScaler()
X_std = scaler_std.fit_transform(X_trans)

scaler_rob = RobustScaler()
X_rob = scaler_rob.fit_transform(X_trans)

km_std_k3 = KMeans(n_clusters=3, n_init=20, random_state=42).fit(X_std)
km_std_k4 = KMeans(n_clusters=4, n_init=20, random_state=42).fit(X_std)
km_rob_k4 = KMeans(n_clusters=4, n_init=20, random_state=42).fit(X_rob)

labels_std_k3 = km_std_k3.labels_
labels_std_k4 = km_std_k4.labels_
labels_rob_k4 = km_rob_k4.labels_

print("\n--- Contingency: K=3 vs K=4 (StandardScaler) ---")
# Count overlaps
for c3 in range(3):
    row_str = f"K3_Cluster_{c3}: "
    for c4 in range(4):
        cnt = np.sum((labels_std_k3 == c3) & (labels_std_k4 == c4))
        row_str += f"K4_C{c4}={cnt:,} ({cnt/np.sum(labels_std_k3 == c3)*100:.1f}%) | "
    print(row_str)

print("\n--- K=3 Physical Medians (F1 Standard) ---")
for c in range(3):
    mask = (labels_std_k3 == c)
    n = np.sum(mask)
    print(f"C{c} (N={n:,} - {n/len(labels_std_k3)*100:.1f}%): "
          f"RecMed={np.median(X_raw[mask, 0]):.1f}d, "
          f"FreqMed={np.median(X_raw[mask, 1]):.0f}, "
          f"MonMed={np.median(X_raw[mask, 2]):.2f}, "
          f"SessMed={np.median(X_raw[mask, 3]):.0f}, "
          f"ActMed={np.median(X_raw[mask, 6]):.2f}")

print("\n--- K=4 Physical Medians (F1 Standard) ---")
for c in range(4):
    mask = (labels_std_k4 == c)
    n = np.sum(mask)
    print(f"C{c} (N={n:,} - {n/len(labels_std_k4)*100:.1f}%): "
          f"RecMed={np.median(X_raw[mask, 0]):.1f}d, "
          f"FreqMed={np.median(X_raw[mask, 1]):.0f}, "
          f"MonMed={np.median(X_raw[mask, 2]):.2f}, "
          f"SessMed={np.median(X_raw[mask, 3]):.0f}, "
          f"ActMed={np.median(X_raw[mask, 6]):.2f}")

print("\n--- K=4 Physical Medians (F1 RobustScaler) ---")
for c in range(4):
    mask = (labels_rob_k4 == c)
    n = np.sum(mask)
    print(f"C{c} (N={n:,} - {n/len(labels_rob_k4)*100:.1f}%): "
          f"RecMed={np.median(X_raw[mask, 0]):.1f}d, "
          f"FreqMed={np.median(X_raw[mask, 1]):.0f}, "
          f"MonMed={np.median(X_raw[mask, 2]):.2f}, "
          f"SessMed={np.median(X_raw[mask, 3]):.0f}, "
          f"ActMed={np.median(X_raw[mask, 6]):.2f}")
