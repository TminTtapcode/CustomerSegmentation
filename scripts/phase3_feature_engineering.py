#!/usr/bin/env python3
"""
Phase 3 — Customer Feature Engineering & Behavioral Analytics.
Extracts RFM and 30-day Clickstream Engagement features from observation_events.parquet.
Produces:
  - data/features/customer_features.parquet (All 1,341,499 observation users)
  - data/features/buyer_features.parquet (92,652 Buyers)
  - data/features/non_buyer_features.parquet (1,248,847 Non-Buyers)
  - outputs/experiments/phase3_feature_profiling.json
  - outputs/figures/fig9_rfm_distributions.png
  - outputs/figures/fig10_engagement_distributions.png
  - outputs/figures/fig11_rfm_correlation_matrix.png
  - outputs/figures/fig12_buyer_vs_non_buyer_engagement.png
"""
import os
import sys
import time
import json
import threading
from pathlib import Path
import duckdb
import psutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_CLEANED = ROOT / "data" / "cleaned"
DATA_FEATURES = ROOT / "data" / "features"
DATA_FEATURES.mkdir(parents=True, exist_ok=True)
OUTPUTS_EXP = ROOT / "outputs" / "experiments"
OUTPUTS_EXP.mkdir(parents=True, exist_ok=True)
FIGURES_DIR = ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

OBS_PARQUET = str(DATA_CLEANED / "observation_events.parquet").replace("\\", "/")
CUSTOMER_PARQUET = str(DATA_FEATURES / "customer_features.parquet").replace("\\", "/")
BUYER_PARQUET = str(DATA_FEATURES / "buyer_features.parquet").replace("\\", "/")
NON_BUYER_PARQUET = str(DATA_FEATURES / "non_buyer_features.parquet").replace("\\", "/")
MANIFEST_PATH = OUTPUTS_EXP / "phase3_feature_profiling.json"

# Track Peak RSS
process = psutil.Process(os.getpid())
baseline_rss = process.memory_info().rss / (1024 * 1024)
peak_rss = baseline_rss
stop_monitoring = False

def monitor_memory():
    global peak_rss, stop_monitoring
    while not stop_monitoring:
        try:
            current = process.memory_info().rss / (1024 * 1024)
            if current > peak_rss:
                peak_rss = current
        except Exception:
            pass
        time.sleep(0.1)

mem_thread = threading.Thread(target=monitor_memory, daemon=True)
mem_thread.start()

print("================================================================================")
print("PHASE 3 — CUSTOMER FEATURE ENGINEERING & BEHAVIORAL ANALYTICS")
print("================================================================================")
t0_total = time.perf_counter()

# Connect to DuckDB with constrained memory
con = duckdb.connect(config={"memory_limit": "2GB", "threads": "4"})

print("\n[Step 1] Aggregating Raw Clickstream to Customer-level Grain...")
t0_agg = time.perf_counter()

con.execute(f"""
CREATE OR REPLACE TABLE customer_features_staging AS
WITH user_aggregates AS (
    SELECT 
        user_id,
        
        -- RFM Base (Lifetime in Observation: Oct 2019 - Jan 2020)
        MAX(CASE WHEN is_valid_for_monetary = TRUE THEN event_time END) AS max_purchase_time,
        MIN(CASE WHEN is_valid_for_monetary = TRUE THEN event_time END) AS min_purchase_time,
        COUNT(DISTINCT CASE WHEN is_valid_for_monetary = TRUE THEN user_session_id END) AS frequency,
        COALESCE(SUM(CASE WHEN is_valid_for_monetary = TRUE THEN price ELSE 0.0 END), 0.0) AS monetary,
        COUNT(CASE WHEN is_valid_for_monetary = TRUE THEN 1 END) AS total_purchase_items,
        
        -- General Lifetime
        MAX(event_time) AS max_event_time,
        MIN(event_time) AS min_event_time,
        COUNT(*) AS lifetime_events,
        COUNT(DISTINCT user_session_id) AS lifetime_sessions,
        
        -- Recent 30 days: [2020-01-02 00:00:00, 2020-02-01 00:00:00)
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' 
            THEN user_session_id 
        END) AS sessions_30d,
        
        COUNT(CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'view'
            THEN 1 
        END) AS views_30d,
        
        COUNT(CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'cart'
            THEN 1 
        END) AS carts_30d,
        
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00'
            THEN product_id 
        END) AS unique_products_30d,
        
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'cart'
            THEN user_session_id 
        END) AS cart_sessions_30d,
        
        -- Previous 30 days: [2019-12-03 00:00:00, 2020-01-02 00:00:00)
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2019-12-03 00:00:00' AND event_time < '2020-01-02 00:00:00' 
            THEN user_session_id 
        END) AS sessions_previous_30d
        
    FROM read_parquet('{OBS_PARQUET}')
    GROUP BY user_id
)
SELECT 
    user_id,
    
    -- Cohort Identifiers
    CASE 
        WHEN frequency > 0 AND monetary > 0 THEN TRUE 
        ELSE FALSE 
    END AS is_buyer,
    
    CASE 
        WHEN frequency > 0 AND monetary > 0 THEN 'BUYER' 
        ELSE 'NON_BUYER' 
    END AS customer_cohort,
    
    CASE 
        WHEN frequency >= 2 THEN TRUE 
        ELSE FALSE 
    END AS is_repeat_buyer,
    
    -- Traditional RFM (for Buyers; NULL for Non-Buyers on Recency)
    CASE 
        WHEN max_purchase_time IS NOT NULL 
        THEN ROUND(EXTRACT(EPOCH FROM (TIMESTAMP '2020-02-01 00:00:00' - max_purchase_time)) / 86400.0, 2)
        ELSE NULL 
    END AS recency_days,
    
    frequency,
    ROUND(monetary, 2) AS monetary,
    
    CASE 
        WHEN frequency > 0 THEN ROUND(monetary / frequency, 2)
        ELSE 0.0 
    END AS monetary_per_session,
    
    CASE 
        WHEN frequency > 0 THEN ROUND(total_purchase_items * 1.0 / frequency, 2)
        ELSE 0.0 
    END AS items_per_purchase_session,
    
    CASE 
        WHEN min_purchase_time IS NOT NULL AND max_purchase_time IS NOT NULL 
        THEN ROUND(EXTRACT(EPOCH FROM (max_purchase_time - min_purchase_time)) / 86400.0, 2)
        ELSE 0.0 
    END AS purchase_span_days,
    
    -- Engagement Features
    ROUND(EXTRACT(EPOCH FROM (TIMESTAMP '2020-02-01 00:00:00' - max_event_time)) / 86400.0, 2) AS days_since_last_event,
    
    sessions_30d,
    views_30d,
    carts_30d,
    unique_products_30d,
    cart_sessions_30d,
    
    ROUND((carts_30d + 1.0) / (views_30d + 1.0), 4) AS cart_to_view_ratio_30d,
    
    sessions_previous_30d,
    sessions_30d AS sessions_recent_30d,
    (sessions_30d - sessions_previous_30d) AS activity_difference,
    ROUND(LN((sessions_30d + 1.0) / (sessions_previous_30d + 1.0)), 4) AS log_activity_ratio,
    
    lifetime_events,
    lifetime_sessions

FROM user_aggregates;
""")
t1_agg = time.perf_counter()
print(f"Customer table staging built in {t1_agg - t0_agg:.2f}s.")

# Check counts
total_customers = con.execute("SELECT COUNT(*) FROM customer_features_staging").fetchone()[0]
total_buyers = con.execute("SELECT COUNT(*) FROM customer_features_staging WHERE is_buyer = TRUE").fetchone()[0]
total_non_buyers = con.execute("SELECT COUNT(*) FROM customer_features_staging WHERE is_buyer = FALSE").fetchone()[0]

print(f"Total Unique Customers in Feature Table: {total_customers:,}")
print(f"  - Buyers:     {total_buyers:,} ({total_buyers / total_customers * 100:.2f}%)")
print(f"  - Non-Buyers: {total_non_buyers:,} ({total_non_buyers / total_customers * 100:.2f}%)")

# [Step 2] Export Parquet datasets
print("\n[Step 2] Exporting Parquet Feature Tables...")
t0_exp = time.perf_counter()

print("  Exporting customer_features.parquet (All Users)...")
con.execute(f"""
COPY customer_features_staging TO '{CUSTOMER_PARQUET}' (FORMAT PARQUET, COMPRESSION ZSTD);
""")

print("  Exporting buyer_features.parquet (Buyers only)...")
con.execute(f"""
COPY (SELECT * FROM customer_features_staging WHERE is_buyer = TRUE) 
TO '{BUYER_PARQUET}' (FORMAT PARQUET, COMPRESSION ZSTD);
""")

print("  Exporting non_buyer_features.parquet (Non-buyers only)...")
con.execute(f"""
COPY (SELECT * FROM customer_features_staging WHERE is_buyer = FALSE) 
TO '{NON_BUYER_PARQUET}' (FORMAT PARQUET, COMPRESSION ZSTD);
""")
t1_exp = time.perf_counter()
print(f"Parquet tables exported in {t1_exp - t0_exp:.2f}s.")

cust_size_mb = os.path.getsize(CUSTOMER_PARQUET) / (1024 * 1024)
buyer_size_mb = os.path.getsize(BUYER_PARQUET) / (1024 * 1024)
non_buyer_size_mb = os.path.getsize(NON_BUYER_PARQUET) / (1024 * 1024)
print(f"File sizes:")
print(f"  customer_features.parquet:  {cust_size_mb:.2f} MB")
print(f"  buyer_features.parquet:     {buyer_size_mb:.2f} MB")
print(f"  non_buyer_features.parquet: {non_buyer_size_mb:.2f} MB")

# [Step 3] Statistical Profiling of Features
print("\n[Step 3] Computing Feature Statistical Profiling & Correlations...")
buyer_df = con.execute(f"SELECT * FROM read_parquet('{BUYER_PARQUET}')").fetchdf()
non_buyer_df = con.execute(f"SELECT * FROM read_parquet('{NON_BUYER_PARQUET}')").fetchdf()

feature_cols_rfm = ['recency_days', 'frequency', 'monetary', 'monetary_per_session', 'items_per_purchase_session']
feature_cols_eng = ['sessions_30d', 'views_30d', 'carts_30d', 'unique_products_30d', 'cart_sessions_30d', 
                    'days_since_last_event', 'log_activity_ratio', 'lifetime_sessions', 'lifetime_events']

def compute_stats(df, cols):
    stats = {}
    for c in cols:
        s = df[c].dropna()
        stats[c] = {
            "count": int(len(s)),
            "missing_count": int(df[c].isna().sum()),
            "missing_pct": round(float(df[c].isna().mean() * 100), 2),
            "mean": round(float(s.mean()), 2),
            "std": round(float(s.std()), 2),
            "skewness": round(float(s.skew()), 2),
            "min": round(float(s.min()), 2),
            "p25": round(float(s.quantile(0.25)), 2),
            "median_p50": round(float(s.median()), 2),
            "p75": round(float(s.quantile(0.75)), 2),
            "p90": round(float(s.quantile(0.90)), 2),
            "p95": round(float(s.quantile(0.95)), 2),
            "p99": round(float(s.quantile(0.99)), 2),
            "max": round(float(s.max()), 2)
        }
    return stats

buyer_rfm_stats = compute_stats(buyer_df, feature_cols_rfm)
buyer_eng_stats = compute_stats(buyer_df, feature_cols_eng)
non_buyer_eng_stats = compute_stats(non_buyer_df, feature_cols_eng)

print("\n--- BUYER RFM METRICS PROFILE ---")
for k, v in buyer_rfm_stats.items():
    print(f"  {k:<28}: Median={v['median_p50']}, Mean={v['mean']}, Std={v['std']}, P90={v['p90']}, Max={v['max']}, Skew={v['skewness']}")

print("\n--- BUYER ENGAGEMENT PROFILE ---")
for k, v in buyer_eng_stats.items():
    print(f"  {k:<28}: Median={v['median_p50']}, Mean={v['mean']}, Std={v['std']}, P90={v['p90']}, Max={v['max']}, Skew={v['skewness']}")

print("\n--- NON-BUYER ENGAGEMENT PROFILE ---")
for k, v in non_buyer_eng_stats.items():
    print(f"  {k:<28}: Median={v['median_p50']}, Mean={v['mean']}, Std={v['std']}, P90={v['p90']}, Max={v['max']}, Skew={v['skewness']}")

# Correlation Matrix for Buyers
corr_cols = ['recency_days', 'frequency', 'monetary', 'sessions_30d', 'views_30d', 'cart_sessions_30d', 'days_since_last_event', 'log_activity_ratio']
corr_matrix = buyer_df[corr_cols].corr().round(4).to_dict()

# [Step 4] Generate Visualizations
print("\n[Step 4] Generating EDA Figures for Features...")

# Figure 9: RFM Distributions for Buyers
plt.figure(figsize=(15, 4.5))
plt.subplot(1, 3, 1)
plt.hist(buyer_df['recency_days'], bins=40, color='#1f77b4', edgecolor='black', alpha=0.8)
plt.axvline(buyer_df['recency_days'].median(), color='red', linestyle='--', label=f'Median: {buyer_df["recency_days"].median():.1f}d')
plt.title("Recency Distribution (Days to Cutoff)", fontsize=11, fontweight='bold')
plt.xlabel("Recency (days)")
plt.ylabel("Buyers Count")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
# Frequency with log scale
plt.hist(buyer_df['frequency'], bins=range(1, 15), color='#2ca02c', edgecolor='black', alpha=0.8, align='left')
plt.title("Frequency Distribution (Purchase Sessions)", fontsize=11, fontweight='bold')
plt.xlabel("Purchase Sessions")
plt.ylabel("Buyers Count")
plt.xticks(range(1, 15))
plt.yscale('log')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
# Monetary with 99th percentile cap for visualization
p99_monetary = buyer_df['monetary'].quantile(0.99)
plt.hist(buyer_df[buyer_df['monetary'] <= p99_monetary]['monetary'], bins=40, color='#ff7f0e', edgecolor='black', alpha=0.8)
plt.axvline(buyer_df['monetary'].median(), color='red', linestyle='--', label=f'Median: {buyer_df["monetary"].median():.2f}')
plt.title(f"Monetary Distribution (Cap 99th: {p99_monetary:.1f})", fontsize=11, fontweight='bold')
plt.xlabel("Monetary (currency units)")
plt.ylabel("Buyers Count")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
fig9_path = FIGURES_DIR / "fig9_rfm_distributions.png"
plt.savefig(fig9_path, dpi=200)
plt.close()
print(f"  Saved {fig9_path.name}")

# Figure 10: Engagement Distributions
plt.figure(figsize=(15, 4.5))
plt.subplot(1, 3, 1)
p99_sess = buyer_df['sessions_30d'].quantile(0.99)
plt.hist(buyer_df['sessions_30d'], bins=range(0, 15), color='#9467bd', edgecolor='black', alpha=0.8, align='left')
plt.title("Recent Sessions in 30 Days (sessions_30d)", fontsize=11, fontweight='bold')
plt.xlabel("Sessions Count")
plt.ylabel("Buyers Count")
plt.yscale('log')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
p99_views = buyer_df['views_30d'].quantile(0.98)
plt.hist(buyer_df[buyer_df['views_30d'] <= p99_views]['views_30d'], bins=35, color='#8c564b', edgecolor='black', alpha=0.8)
plt.axvline(buyer_df['views_30d'].median(), color='red', linestyle='--', label=f'Median: {buyer_df["views_30d"].median():.0f}')
plt.title(f"Recent Views in 30 Days (Cap 98th: {p99_views:.0f})", fontsize=11, fontweight='bold')
plt.xlabel("Views Count")
plt.ylabel("Buyers Count")
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.hist(buyer_df['log_activity_ratio'], bins=35, color='#e377c2', edgecolor='black', alpha=0.8)
plt.axvline(0, color='black', linestyle='-', alpha=0.7)
plt.axvline(buyer_df['log_activity_ratio'].median(), color='red', linestyle='--', label=f'Median: {buyer_df["log_activity_ratio"].median():.2f}')
plt.title("Log Activity Ratio (Momentum: Recent vs Previous)", fontsize=11, fontweight='bold')
plt.xlabel("log((recent + 1) / (previous + 1))")
plt.ylabel("Buyers Count")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
fig10_path = FIGURES_DIR / "fig10_engagement_distributions.png"
plt.savefig(fig10_path, dpi=200)
plt.close()
print(f"  Saved {fig10_path.name}")

# Figure 11: RFM Correlation Heatmap
fig, ax = plt.subplots(figsize=(8.5, 7))
corr_df = buyer_df[corr_cols].corr()
cax = ax.imshow(corr_df.values, cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax, ax=ax)
ax.set_xticks(range(len(corr_cols)))
ax.set_yticks(range(len(corr_cols)))
ax.set_xticklabels(corr_cols, rotation=45, ha='right', fontsize=9)
ax.set_yticklabels(corr_cols, fontsize=9)
for (i, j), val in np.ndenumerate(corr_df.values):
    ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black' if abs(val) < 0.6 else 'white', fontsize=8)
ax.set_title("Feature Correlation Matrix (Buyers Cohort)", fontsize=12, fontweight='bold', pad=15)
fig.tight_layout()
fig11_path = FIGURES_DIR / "fig11_rfm_correlation_matrix.png"
fig.savefig(fig11_path, dpi=200)
plt.close(fig)
print(f"  Saved {fig11_path.name}")

# Figure 12: Buyer vs Non-Buyer Engagement Comparison
fig12, axes = plt.subplots(1, 3, figsize=(14, 5))
box_data_events = [np.log1p(buyer_df['lifetime_events']), np.log1p(non_buyer_df['lifetime_events'])]
axes[0].boxplot(box_data_events, tick_labels=['Buyers', 'Non-Buyers'], patch_artist=True,
                boxprops=dict(facecolor='#1f77b4', alpha=0.6))
axes[0].set_title("Log(1 + Lifetime Events)", fontsize=11, fontweight='bold')
axes[0].set_ylabel("log(1 + events)")
axes[0].grid(True, alpha=0.3)

box_data_sess = [np.log1p(buyer_df['lifetime_sessions']), np.log1p(non_buyer_df['lifetime_sessions'])]
axes[1].boxplot(box_data_sess, tick_labels=['Buyers', 'Non-Buyers'], patch_artist=True,
                boxprops=dict(facecolor='#2ca02c', alpha=0.6))
axes[1].set_title("Log(1 + Lifetime Sessions)", fontsize=11, fontweight='bold')
axes[1].set_ylabel("log(1 + sessions)")
axes[1].grid(True, alpha=0.3)

box_data_rec = [buyer_df['days_since_last_event'], non_buyer_df['days_since_last_event']]
axes[2].boxplot(box_data_rec, tick_labels=['Buyers', 'Non-Buyers'], patch_artist=True,
                boxprops=dict(facecolor='#ff7f0e', alpha=0.6))
axes[2].set_title("Days Since Last Event", fontsize=11, fontweight='bold')
axes[2].set_ylabel("Days to Cutoff")
axes[2].grid(True, alpha=0.3)

fig12.tight_layout()
fig12_path = FIGURES_DIR / "fig12_buyer_vs_non_buyer_engagement.png"
fig12.savefig(fig12_path, dpi=200)
plt.close(fig12)
print(f"  Saved {fig12_path.name}")

# Stop memory monitoring
stop_monitoring = True
t1_total = time.perf_counter()
wall_time = t1_total - t0_total

# Export Manifest JSON
manifest = {
    "phase": "P3_FEATURE_ENGINEERING",
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "hardware": {
        "os": "Windows-11",
        "cpu_count": psutil.cpu_count(logical=True),
        "duckdb_version": duckdb.__version__,
        "duckdb_memory_limit": "2GB",
        "duckdb_threads": 4
    },
    "performance": {
        "wall_time_seconds": round(wall_time, 2),
        "aggregation_time_seconds": round(t1_agg - t0_agg, 2),
        "export_time_seconds": round(t1_exp - t0_exp, 2),
        "throughput_events_per_second": round(15667350 / wall_time, 1),
        "throughput_customers_per_second": round(total_customers / wall_time, 1),
        "baseline_rss_mb": round(baseline_rss, 2),
        "peak_rss_mb": round(peak_rss, 2),
        "rss_delta_mb": round(peak_rss - baseline_rss, 2)
    },
    "cohort_counts": {
        "total_observation_customers": total_customers,
        "buyers_count": total_buyers,
        "non_buyers_count": total_non_buyers,
        "repeat_buyers_count": int(buyer_df['is_repeat_buyer'].sum()),
        "one_time_buyers_count": int((buyer_df['frequency'] == 1).sum()),
        "repeat_buyer_rate_pct": round(float(buyer_df['is_repeat_buyer'].mean() * 100), 2)
    },
    "file_storage_mb": {
        "customer_features_parquet": round(cust_size_mb, 2),
        "buyer_features_parquet": round(buyer_size_mb, 2),
        "non_buyer_features_parquet": round(non_buyer_size_mb, 2),
        "total_feature_storage_mb": round(cust_size_mb + buyer_size_mb + non_buyer_size_mb, 2)
    },
    "buyer_rfm_statistics": buyer_rfm_stats,
    "buyer_engagement_statistics": buyer_eng_stats,
    "non_buyer_engagement_statistics": non_buyer_eng_stats,
    "buyer_correlation_matrix": corr_matrix,
    "proposed_feature_sets_for_phase4": {
        "F0_traditional_rfm": ["recency_days", "frequency", "monetary"],
        "F1_rfm_plus_engagement": ["recency_days", "frequency", "monetary", "sessions_30d", "views_30d", "cart_sessions_30d", "log_activity_ratio"],
        "F2_extended_behavioral": ["recency_days", "frequency", "monetary", "monetary_per_session", "items_per_purchase_session", "sessions_30d", "views_30d", "unique_products_30d", "cart_sessions_30d", "cart_to_view_ratio_30d", "days_since_last_event", "log_activity_ratio"]
    }
}

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest saved to {MANIFEST_PATH}")
print(f"Total Phase 3 Execution Time: {wall_time:.2f}s | Peak RSS: {peak_rss:.2f} MB")
print("================================================================================")
print("PHASE 3 FEATURE ENGINEERING COMPLETED SUCCESSFULLY!")
print("================================================================================")

