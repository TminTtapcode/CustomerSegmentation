"""Phase 1: Full Data Profiling and EDA on REES46 Cosmetics Dataset using DuckDB.

Measures wall-clock time and process RSS using psutil.
Exports structured profiling metrics to outputs/experiments/phase1_data_profile.json
and generates 8 figures in outputs/figures/.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import sys
import threading
import time
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil

# Base directory
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
OUTPUTS_EXP = ROOT / "outputs" / "experiments"
OUTPUTS_FIG = ROOT / "outputs" / "figures"
OUTPUTS_EXP.mkdir(parents=True, exist_ok=True)
OUTPUTS_FIG.mkdir(parents=True, exist_ok=True)

# Set matplotlib style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "sans-serif"]
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8


class MemoryMonitor:
    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self.peak_rss = self.process.memory_info().rss
        self.baseline_rss = self.peak_rss
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._monitor, daemon=True)

    def _monitor(self):
        while not self._stop_event.is_set():
            try:
                rss = self.process.memory_info().rss
                if rss > self.peak_rss:
                    self.peak_rss = rss
            except Exception:
                pass
            time.sleep(self.interval)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join(timeout=2.0)
        final_rss = self.process.memory_info().rss
        if final_rss > self.peak_rss:
            self.peak_rss = final_rss


def run_profiling():
    print("=" * 70)
    print("STARTING PHASE 1 DATA PROFILING ON REES46 DATASET")
    print("=" * 70)

    # 1. Environment & Hardware Survey
    mem_info = psutil.virtual_memory()
    disk_info = shutil.disk_usage(str(ROOT))
    hardware_meta = {
        "python_version": sys.version,
        "os_platform": platform.platform(),
        "cpu_count_logical": os.cpu_count(),
        "total_ram_gb": round(mem_info.total / (1024**3), 2),
        "available_ram_gb": round(mem_info.available / (1024**3), 2),
        "free_disk_gb": round(disk_info.free / (1024**3), 2),
        "duckdb_version": duckdb.__version__,
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
    }
    print(f"Hardware: {hardware_meta['cpu_count_logical']} CPUs | "
          f"{hardware_meta['total_ram_gb']} GB RAM ({hardware_meta['available_ram_gb']} GB available) | "
          f"{hardware_meta['free_disk_gb']} GB Disk Free")

    # Start memory monitoring
    monitor = MemoryMonitor(interval=0.2)
    monitor.start()
    t_start = time.perf_counter()

    # 2. DuckDB Connection with Memory Limit
    con = duckdb.connect(database=":memory:")
    # Set conservative memory limit so we don't exceed available RAM
    con.execute("SET memory_limit = '2GB'")
    con.execute("SET threads = 4")
    con.execute("SET preserve_insertion_order = false")

    files = sorted(list(DATA_RAW.glob("*.csv")))
    csv_files = [f for f in files if f.name != ".gitkeep"]
    print(f"Found {len(csv_files)} CSV files in data/raw/:")
    for f in csv_files:
        print(f"  - {f.name}: {f.stat().st_size / (1024*1024):.2f} MB")

    # 3. Monthly Profiling
    monthly_profiles = {}
    total_raw_bytes = sum(f.stat().st_size for f in csv_files)

    for f in csv_files:
        month_name = f.stem
        f_size_mb = round(f.stat().st_size / (1024 * 1024), 2)
        print(f"\n--- Profiling {f.name} ({f_size_mb} MB) ---")
        f_path = str(f).replace("\\", "/")

        # File query
        query = f"""
        SELECT
            COUNT(*) AS row_count,
            MIN(event_time) AS min_time,
            MAX(event_time) AS max_time,
            COUNT(DISTINCT user_id) AS distinct_users,
            COUNT(DISTINCT user_session) AS distinct_sessions,
            COUNT(DISTINCT (user_id, user_session)) AS distinct_user_sessions,
            COUNT(*) FILTER (WHERE event_type = 'view') AS views,
            COUNT(*) FILTER (WHERE event_type = 'cart') AS carts,
            COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS removes,
            COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases,
            COUNT(*) FILTER (WHERE user_id IS NULL) AS missing_user_id,
            COUNT(*) FILTER (WHERE user_session IS NULL) AS missing_user_session,
            COUNT(*) FILTER (WHERE category_code IS NULL) AS missing_category_code,
            COUNT(*) FILTER (WHERE brand IS NULL) AS missing_brand,
            COUNT(*) FILTER (WHERE price IS NULL) AS missing_price,
            COUNT(*) FILTER (WHERE price <= 0) AS price_le_zero,
            COUNT(*) FILTER (WHERE event_type = 'purchase' AND user_session IS NULL) AS purchase_missing_session
        FROM read_csv('{f_path}', header=True, auto_detect=True)
        """
        res = con.execute(query).fetchdf().iloc[0].to_dict()

        # Distinct purchase sessions proxy for this file
        ps_query = f"""
        SELECT COUNT(DISTINCT (user_id, user_session)) AS purchase_sessions_proxy
        FROM read_csv('{f_path}', header=True, auto_detect=True)
        WHERE event_type = 'purchase' AND user_id IS NOT NULL AND user_session IS NOT NULL
        """
        ps_proxy = int(con.execute(ps_query).fetchone()[0])
        res["purchase_sessions_proxy"] = ps_proxy

        # Convert types for JSON serialization
        clean_res = {
            "filename": f.name,
            "size_mb": f_size_mb,
            "row_count": int(res["row_count"]),
            "min_time": str(res["min_time"]),
            "max_time": str(res["max_time"]),
            "distinct_users": int(res["distinct_users"]),
            "distinct_sessions": int(res["distinct_sessions"]),
            "distinct_user_sessions": int(res["distinct_user_sessions"]),
            "views": int(res["views"]),
            "carts": int(res["carts"]),
            "removes": int(res["removes"]),
            "purchases": int(res["purchases"]),
            "purchase_sessions_proxy": ps_proxy,
            "missing_user_id": int(res["missing_user_id"]),
            "missing_user_session": int(res["missing_user_session"]),
            "missing_category_code": int(res["missing_category_code"]),
            "missing_brand": int(res["missing_brand"]),
            "missing_price": int(res["missing_price"]),
            "price_le_zero": int(res["price_le_zero"]),
            "purchase_missing_session": int(res["purchase_missing_session"]),
            "missing_session_pct": round(res["missing_user_session"] / res["row_count"] * 100, 3) if res["row_count"] else 0,
            "missing_brand_pct": round(res["missing_brand"] / res["row_count"] * 100, 2) if res["row_count"] else 0,
            "missing_category_code_pct": round(res["missing_category_code"] / res["row_count"] * 100, 2) if res["row_count"] else 0,
        }
        monthly_profiles[month_name] = clean_res
        print(f"  Rows: {clean_res['row_count']:,} | Users: {clean_res['distinct_users']:,} | "
              f"Sessions: {clean_res['distinct_user_sessions']:,}")
        print(f"  Views: {clean_res['views']:,} | Carts: {clean_res['carts']:,} | "
              f"Purchases: {clean_res['purchases']:,} | Purchase Sessions Proxy: {clean_res['purchase_sessions_proxy']:,}")
        print(f"  Missing Session: {clean_res['missing_user_session']:,} ({clean_res['missing_session_pct']}%) | "
              f"Missing Brand: {clean_res['missing_brand_pct']}% | Missing Category: {clean_res['missing_category_code_pct']}%")

    # 4. Global Profiling across All 5 Months
    print("\n" + "=" * 70)
    print("PROFILING ENTIRE DATASET (OCT 2019 - FEB 2020)")
    print("=" * 70)
    all_raw_glob = str(DATA_RAW / "20*.csv").replace("\\", "/")

    # Create a unified view
    con.execute(f"""
    CREATE VIEW raw_events AS
    SELECT * FROM read_csv('{all_raw_glob}', header=True, auto_detect=True)
    """)

    global_stats = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        MIN(event_time) AS global_min_time,
        MAX(event_time) AS global_max_time,
        COUNT(DISTINCT user_id) AS total_unique_users,
        COUNT(DISTINCT (user_id, user_session)) AS total_unique_sessions,
        COUNT(*) FILTER (WHERE event_type = 'view') AS total_views,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS total_carts,
        COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS total_removes,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS total_purchases,
        COUNT(*) FILTER (WHERE user_id IS NULL) AS total_missing_user,
        COUNT(*) FILTER (WHERE user_session IS NULL) AS total_missing_session,
        COUNT(*) FILTER (WHERE brand IS NULL) AS total_missing_brand,
        COUNT(*) FILTER (WHERE category_code IS NULL) AS total_missing_category,
        COUNT(*) FILTER (WHERE price IS NULL) AS total_missing_price,
        COUNT(*) FILTER (WHERE price <= 0) AS total_price_le_zero,
        COUNT(*) FILTER (WHERE price < 0) AS total_price_negative,
        COUNT(*) FILTER (WHERE price = 0) AS total_price_zero,
        COUNT(*) FILTER (WHERE event_type = 'purchase' AND user_session IS NULL) AS total_purchase_missing_session
    FROM raw_events
    """).fetchdf().iloc[0].to_dict()

    # Total distinct purchase sessions proxy
    total_purchase_sessions = int(con.execute("""
    SELECT COUNT(DISTINCT (user_id, user_session))
    FROM raw_events
    WHERE event_type = 'purchase' AND user_id IS NOT NULL AND user_session IS NOT NULL
    """).fetchone()[0])
    global_stats["total_purchase_sessions_proxy"] = total_purchase_sessions

    # Convert to standard types
    total_rows = int(global_stats["total_rows"])
    print(f"Total Rows: {total_rows:,}")
    print(f"Global Time Range: {global_stats['global_min_time']} to {global_stats['global_max_time']}")
    print(f"Total Unique Users: {int(global_stats['total_unique_users']):,}")
    print(f"Total Unique Sessions: {int(global_stats['total_unique_sessions']):,}")
    print(f"Total Purchase Events: {int(global_stats['total_purchases']):,}")
    print(f"Total Purchase Sessions Proxy: {total_purchase_sessions:,}")
    print(f"Ratio Purchases/Purchase Sessions: {int(global_stats['total_purchases']) / total_purchase_sessions:.2f} items/session")

    # 5. Price Distribution Metrics
    print("\n--- Price Statistics ---")
    price_stats_df = con.execute("""
    SELECT
        MIN(price) AS min_price,
        QUANTILE_CONT(price, 0.25) AS q25,
        QUANTILE_CONT(price, 0.50) AS median_price,
        QUANTILE_CONT(price, 0.75) AS q75,
        QUANTILE_CONT(price, 0.90) AS q90,
        QUANTILE_CONT(price, 0.95) AS q95,
        QUANTILE_CONT(price, 0.99) AS q99,
        QUANTILE_CONT(price, 0.999) AS q999,
        MAX(price) AS max_price,
        AVG(price) AS mean_price,
        STDDEV(price) AS std_price
    FROM raw_events
    WHERE price IS NOT NULL
    """).fetchdf().iloc[0].to_dict()
    price_stats = {k: round(float(v), 2) for k, v in price_stats_df.items()}
    print(f"Price Quantiles: Min={price_stats['min_price']} | 25%={price_stats['q25']} | "
          f"Median={price_stats['median_price']} | Mean={price_stats['mean_price']} | "
          f"75%={price_stats['q75']} | 99%={price_stats['q99']} | Max={price_stats['max_price']}")

    # 6. Temporal Split Audit: Observation [2019-10-01, 2020-02-01) vs Holdout [2020-02-01, 2020-03-01)
    print("\n--- Temporal Split & Data Leakage Audit ---")
    temporal_split = con.execute("""
    SELECT
        COUNT(*) FILTER (WHERE event_time < '2019-10-01 00:00:00') AS before_observation,
        COUNT(*) FILTER (WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-02-01 00:00:00') AS observation_events,
        COUNT(*) FILTER (WHERE event_time >= '2020-02-01 00:00:00' AND event_time < '2020-03-01 00:00:00') AS holdout_events,
        COUNT(*) FILTER (WHERE event_time >= '2020-03-01 00:00:00') AS after_holdout
    FROM raw_events
    """).fetchdf().iloc[0].to_dict()
    temporal_stats = {k: int(v) for k, v in temporal_split.items()}
    print(f"Events before 2019-10-01: {temporal_stats['before_observation']:,}")
    print(f"Observation Events [2019-10-01, 2020-02-01): {temporal_stats['observation_events']:,} "
          f"({temporal_stats['observation_events'] / total_rows * 100:.2f}%)")
    print(f"Holdout Events [2020-02-01, 2020-03-01): {temporal_stats['holdout_events']:,} "
          f"({temporal_stats['holdout_events'] / total_rows * 100:.2f}%)")
    print(f"Events after 2020-03-01: {temporal_stats['after_holdout']:,}")

    # Check for sessions spanning across cutoff
    print("Checking sessions spanning across 2020-02-01 cutoff...")
    spanning_sessions_count = int(con.execute("""
    SELECT COUNT(*) FROM (
        SELECT user_id, user_session
        FROM raw_events
        WHERE user_id IS NOT NULL AND user_session IS NOT NULL
        GROUP BY user_id, user_session
        HAVING MIN(event_time) < '2020-02-01 00:00:00' AND MAX(event_time) >= '2020-02-01 00:00:00'
    )
    """).fetchone()[0])
    print(f"Sessions spanning across cutoff: {spanning_sessions_count:,}")

    # 7. Buyers vs Observed Non-Buyers in Observation Window
    print("\n--- Buyers vs Observed Non-Buyers (Observation Window) ---")
    user_cohort_stats = con.execute("""
    WITH user_obs AS (
        SELECT
            user_id,
            COUNT(*) AS event_count,
            COUNT(DISTINCT user_session) AS session_count,
            COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchase_events,
            COUNT(DISTINCT user_session) FILTER (WHERE event_type = 'purchase') AS purchase_sessions,
            SUM(price) FILTER (WHERE event_type = 'purchase' AND price > 0) AS total_monetary
        FROM raw_events
        WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-02-01 00:00:00'
          AND user_id IS NOT NULL
        GROUP BY user_id
    )
    SELECT
        COUNT(*) AS total_obs_users,
        COUNT(*) FILTER (WHERE purchase_events > 0) AS buyers_count,
        COUNT(*) FILTER (WHERE purchase_events = 0) AS non_buyers_count,
        COUNT(*) FILTER (WHERE purchase_sessions = 1) AS single_purchase_buyers,
        COUNT(*) FILTER (WHERE purchase_sessions >= 2) AS repeat_buyers,
        AVG(session_count) AS avg_sessions_per_user,
        MEDIAN(session_count) AS median_sessions_per_user,
        AVG(event_count) AS avg_events_per_user,
        MEDIAN(event_count) AS median_events_per_user,
        AVG(total_monetary) FILTER (WHERE purchase_events > 0) AS avg_buyer_monetary,
        MEDIAN(total_monetary) FILTER (WHERE purchase_events > 0) AS median_buyer_monetary
    FROM user_obs
    """).fetchdf().iloc[0].to_dict()

    obs_users = int(user_cohort_stats["total_obs_users"])
    obs_buyers = int(user_cohort_stats["buyers_count"])
    obs_non_buyers = int(user_cohort_stats["non_buyers_count"])
    single_buyers = int(user_cohort_stats["single_purchase_buyers"])
    repeat_buyers = int(user_cohort_stats["repeat_buyers"])
    repeat_buyer_rate = round(repeat_buyers / obs_buyers, 4) if obs_buyers else 0
    buyer_conversion_rate = round(obs_buyers / obs_users, 4) if obs_users else 0

    print(f"Total Observation Users: {obs_users:,}")
    print(f"Buyers (>=1 purchase in obs): {obs_buyers:,} ({buyer_conversion_rate*100:.2f}%)")
    print(f"Observed Non-Buyers: {obs_non_buyers:,} ({round(obs_non_buyers/obs_users*100, 2)}%)")
    print(f"Single-Purchase Buyers (Freq=1): {single_buyers:,} ({round(single_buyers/obs_buyers*100, 2)}%)")
    print(f"Repeat Buyers (Freq>=2): {repeat_buyers:,} ({repeat_buyer_rate*100:.2f}%)")
    print(f"Buyer Monetary Median: {round(float(user_cohort_stats['median_buyer_monetary']), 2)} | "
          f"Mean: {round(float(user_cohort_stats['avg_buyer_monetary']), 2)}")

    # 8. Session-Level Funnel Analysis (Observation Window)
    print("\n--- Session-Level Funnel Analysis ---")
    session_funnel = con.execute("""
    WITH session_flags AS (
        SELECT
            user_id,
            user_session,
            BOOL_OR(event_type = 'view') AS has_view,
            BOOL_OR(event_type = 'cart') AS has_cart,
            BOOL_OR(event_type = 'remove_from_cart') AS has_remove,
            BOOL_OR(event_type = 'purchase') AS has_purchase,
            MIN(event_time) FILTER (WHERE event_type = 'cart') AS first_cart_time,
            MAX(event_time) FILTER (WHERE event_type = 'purchase') AS last_purchase_time
        FROM raw_events
        WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-02-01 00:00:00'
          AND user_id IS NOT NULL AND user_session IS NOT NULL
        GROUP BY user_id, user_session
    )
    SELECT
        COUNT(*) AS total_valid_sessions,
        COUNT(*) FILTER (WHERE has_view) AS view_sessions,
        COUNT(*) FILTER (WHERE has_cart) AS cart_sessions,
        COUNT(*) FILTER (WHERE has_purchase) AS purchase_sessions,
        COUNT(*) FILTER (WHERE has_cart AND has_purchase AND last_purchase_time > first_cart_time) AS cart_then_purchase_sessions,
        COUNT(*) FILTER (WHERE has_cart AND NOT has_purchase) AS cart_abandoned_sessions,
        COUNT(*) FILTER (WHERE has_view AND NOT has_cart AND NOT has_purchase) AS view_only_sessions
    FROM session_flags
    """).fetchdf().iloc[0].to_dict()

    tot_sess = int(session_funnel["total_valid_sessions"])
    view_sess = int(session_funnel["view_sessions"])
    cart_sess = int(session_funnel["cart_sessions"])
    pur_sess = int(session_funnel["purchase_sessions"])
    cart_then_pur = int(session_funnel["cart_then_purchase_sessions"])
    cart_abandoned = int(session_funnel["cart_abandoned_sessions"])
    view_only = int(session_funnel["view_only_sessions"])

    funnel_metrics = {
        "total_valid_sessions": tot_sess,
        "view_sessions": view_sess,
        "cart_sessions": cart_sess,
        "purchase_sessions": pur_sess,
        "cart_then_purchase_sessions": cart_then_pur,
        "cart_abandoned_sessions": cart_abandoned,
        "view_only_sessions": view_only,
        "session_cart_rate": round(cart_sess / tot_sess, 4) if tot_sess else 0,
        "session_purchase_rate": round(pur_sess / tot_sess, 4) if tot_sess else 0,
        "cart_to_purchase_rate": round(cart_then_pur / cart_sess, 4) if cart_sess else 0,
        "cart_abandonment_rate": round(cart_abandoned / cart_sess, 4) if cart_sess else 0,
    }
    print(f"Total Valid Sessions: {tot_sess:,}")
    print(f"View Sessions: {view_sess:,} ({view_sess/tot_sess*100:.2f}%)")
    print(f"Cart Sessions: {cart_sess:,} ({funnel_metrics['session_cart_rate']*100:.2f}%)")
    print(f"Purchase Sessions: {pur_sess:,} ({funnel_metrics['session_purchase_rate']*100:.2f}%)")
    print(f"Cart-then-Purchase Sessions: {cart_then_pur:,} ({funnel_metrics['cart_to_purchase_rate']*100:.2f}% of cart sessions)")
    print(f"Cart Abandoned Sessions: {cart_abandoned:,} ({funnel_metrics['cart_abandonment_rate']*100:.2f}% of cart sessions)")

    # 9. Daily Volume Aggregation for Visualization
    print("\n--- Daily Aggregations for Charts ---")
    daily_df = con.execute("""
    SELECT
        CAST(event_time AS DATE) AS event_date,
        COUNT(*) AS total_events,
        COUNT(*) FILTER (WHERE event_type = 'view') AS views,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS carts,
        COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS removes,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases,
        COUNT(DISTINCT user_id) AS dau,
        COUNT(DISTINCT (user_id, user_session)) AS daily_sessions
    FROM raw_events
    WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-03-01 00:00:00'
    GROUP BY CAST(event_time AS DATE)
    ORDER BY event_date
    """).fetchdf()
    print(f"Aggregated daily time series across {len(daily_df)} days.")

    # 10. User Activity Quantiles
    user_activity_dist = con.execute("""
    WITH user_counts AS (
        SELECT user_id, COUNT(*) AS event_count, COUNT(DISTINCT user_session) AS session_count
        FROM raw_events
        WHERE user_id IS NOT NULL
        GROUP BY user_id
    )
    SELECT
        QUANTILE_CONT(event_count, 0.25) AS events_p25,
        QUANTILE_CONT(event_count, 0.50) AS events_median,
        QUANTILE_CONT(event_count, 0.75) AS events_p75,
        QUANTILE_CONT(event_count, 0.90) AS events_p90,
        QUANTILE_CONT(event_count, 0.95) AS events_p95,
        QUANTILE_CONT(event_count, 0.99) AS events_p99,
        QUANTILE_CONT(session_count, 0.25) AS sessions_p25,
        QUANTILE_CONT(session_count, 0.50) AS sessions_median,
        QUANTILE_CONT(session_count, 0.75) AS sessions_p75,
        QUANTILE_CONT(session_count, 0.90) AS sessions_p90,
        QUANTILE_CONT(session_count, 0.95) AS sessions_p95,
        QUANTILE_CONT(session_count, 0.99) AS sessions_p99
    FROM user_counts
    """).fetchdf().iloc[0].to_dict()

    # 11. Stop Monitoring & Record Performance
    t_end = time.perf_counter()
    monitor.stop()

    wall_time = round(t_end - t_start, 2)
    rows_per_sec = round(total_rows / wall_time, 1) if wall_time else 0
    peak_rss_mb = round(monitor.peak_rss / (1024 * 1024), 2)
    baseline_rss_mb = round(monitor.baseline_rss / (1024 * 1024), 2)
    rss_delta_mb = round(peak_rss_mb - baseline_rss_mb, 2)

    perf_benchmark = {
        "wall_time_seconds": wall_time,
        "rows_processed": total_rows,
        "throughput_rows_per_second": rows_per_sec,
        "total_input_bytes": total_raw_bytes,
        "total_input_mb": round(total_raw_bytes / (1024 * 1024), 2),
        "baseline_rss_mb": baseline_rss_mb,
        "peak_rss_mb": peak_rss_mb,
        "rss_delta_mb": rss_delta_mb,
        "duckdb_memory_limit": "2GB",
        "duckdb_threads": 4,
    }
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Wall-Clock Time: {wall_time:.2f} s | Throughput: {rows_per_sec:,.1f} rows/s")
    print(f"Total Input: {perf_benchmark['total_input_mb']:.2f} MB across 5 CSVs")
    print(f"Process RSS: Baseline = {baseline_rss_mb} MB | Peak = {peak_rss_mb} MB (Delta: +{rss_delta_mb} MB)")

    # 12. Save Results to JSON
    profile_summary = {
        "phase": "P1_DATA_UNDERSTANDING",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hardware": hardware_meta,
        "performance": perf_benchmark,
        "global_statistics": {
            "total_rows": total_rows,
            "total_unique_users": int(global_stats["total_unique_users"]),
            "total_unique_sessions": int(global_stats["total_unique_sessions"]),
            "total_views": int(global_stats["total_views"]),
            "total_carts": int(global_stats["total_carts"]),
            "total_removes": int(global_stats["total_removes"]),
            "total_purchases": int(global_stats["total_purchases"]),
            "total_purchase_sessions_proxy": total_purchase_sessions,
            "items_per_purchase_session": round(int(global_stats["total_purchases"]) / total_purchase_sessions, 2),
            "missing_user_id_count": int(global_stats["total_missing_user"]),
            "missing_session_count": int(global_stats["total_missing_session"]),
            "missing_session_pct": round(int(global_stats["total_missing_session"]) / total_rows * 100, 3),
            "missing_brand_count": int(global_stats["total_missing_brand"]),
            "missing_brand_pct": round(int(global_stats["total_missing_brand"]) / total_rows * 100, 2),
            "missing_category_code_count": int(global_stats["total_missing_category"]),
            "missing_category_code_pct": round(int(global_stats["total_missing_category"]) / total_rows * 100, 2),
            "missing_price_count": int(global_stats["total_missing_price"]),
            "price_le_zero_count": int(global_stats["total_price_le_zero"]),
            "price_negative_count": int(global_stats["total_price_negative"]),
            "price_zero_count": int(global_stats["total_price_zero"]),
            "purchase_missing_session_count": int(global_stats["total_purchase_missing_session"]),
            "purchase_missing_session_pct": round(int(global_stats["total_purchase_missing_session"]) / int(global_stats["total_purchases"]) * 100, 3),
        },
        "monthly_breakdown": monthly_profiles,
        "price_distribution": price_stats,
        "temporal_split": temporal_stats,
        "sessions_spanning_cutoff": spanning_sessions_count,
        "observation_cohort": {
            "users_count": obs_users,
            "buyers_count": obs_buyers,
            "non_buyers_count": obs_non_buyers,
            "buyer_conversion_rate": buyer_conversion_rate,
            "single_purchase_buyers": single_buyers,
            "repeat_buyers": repeat_buyers,
            "repeat_buyer_rate_proxy": repeat_buyer_rate,
            "median_buyer_monetary": round(float(user_cohort_stats["median_buyer_monetary"]), 2),
            "avg_buyer_monetary": round(float(user_cohort_stats["avg_buyer_monetary"]), 2),
        },
        "session_funnel": funnel_metrics,
        "user_activity_quantiles": {k: round(float(v), 2) for k, v in user_activity_dist.items()},
    }

    json_path = OUTPUTS_EXP / "phase1_data_profile.json"
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(profile_summary, fp, indent=2, ensure_ascii=False)
    print(f"\nSaved profile JSON to: {json_path}")

    # 13. GENERATE 8 EDA FIGURES
    print("\n" + "=" * 70)
    print("GENERATING 8 PUBLICATION-QUALITY EDA FIGURES")
    print("=" * 70)

    # Figure 1: Event Type Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    ev_labels = ["View", "Cart", "Remove from Cart", "Purchase"]
    ev_counts = [
        int(global_stats["total_views"]),
        int(global_stats["total_carts"]),
        int(global_stats["total_removes"]),
        int(global_stats["total_purchases"]),
    ]
    ev_colors = ["#3498db", "#f39c12", "#e74c3c", "#2ecc71"]
    bars = ax.bar(ev_labels, [c / 1e6 for c in ev_counts], color=ev_colors, width=0.55, edgecolor="#333333", linewidth=1)
    for bar, count in zip(bars, ev_counts):
        pct = count / total_rows * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{count/1e6:.2f}M\n({pct:.1f}%)", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title("REES46: Event Type Distribution (Oct 2019 – Feb 2020)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Event Count (Millions)", fontsize=11)
    ax.set_ylim(0, max(ev_counts) / 1e6 * 1.25)
    plt.tight_layout()
    fig1_path = OUTPUTS_FIG / "fig1_event_type_distribution.png"
    plt.savefig(fig1_path, dpi=200)
    plt.close()
    print(f"Generated: {fig1_path.name}")

    # Figure 2: Daily Event Volume by Type
    fig, ax = plt.subplots(figsize=(12, 5))
    dates = pd.to_datetime(daily_df["event_date"])
    ax.plot(dates, daily_df["views"] / 1000, label="Views", color="#3498db", linewidth=1.5)
    ax.plot(dates, daily_df["carts"] / 1000, label="Carts", color="#f39c12", linewidth=1.5)
    ax.plot(dates, daily_df["removes"] / 1000, label="Remove from Cart", color="#e74c3c", linewidth=1.2, linestyle="--")
    ax.plot(dates, daily_df["purchases"] / 1000, label="Purchases", color="#2ecc71", linewidth=1.8)
    # Cutoff line
    ax.axvline(pd.to_datetime("2020-02-01"), color="#e74c3c", linestyle=":", linewidth=2, label="Cutoff (Holdout Start)")
    # Black Friday / November peak annotation
    nov_peak_idx = daily_df["total_events"].idxmax()
    nov_peak_date = pd.to_datetime(daily_df.loc[nov_peak_idx, "event_date"])
    nov_peak_val = daily_df.loc[nov_peak_idx, "views"] / 1000
    ax.annotate(f"Peak: {nov_peak_date.strftime('%Y-%m-%d')}\n({daily_df.loc[nov_peak_idx, 'total_events']/1000:.1f}k events)",
                xy=(nov_peak_date, nov_peak_val), xytext=(nov_peak_date - pd.Timedelta(days=25), nov_peak_val + 20),
                arrowprops=dict(facecolor="#2c3e50", shrink=0.08, width=1, headwidth=6),
                fontsize=9, fontweight="bold", bbox=dict(boxstyle="round,pad=0.3", fc="#ecf0f1", ec="#bdc3c7"))
    ax.set_title("Daily Event Volume by Event Type (Oct 2019 – Feb 2020)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Daily Events (Thousands)", fontsize=11)
    ax.set_xlabel("Date", fontsize=11)
    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    fig2_path = OUTPUTS_FIG / "fig2_daily_monthly_volume.png"
    plt.savefig(fig2_path, dpi=200)
    plt.close()
    print(f"Generated: {fig2_path.name}")

    # Figure 3: Unique Users (DAU) and Unique Sessions Over Time
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()
    ax1.plot(dates, daily_df["dau"] / 1000, label="Daily Active Users (DAU)", color="#2980b9", linewidth=1.8)
    ax2.plot(dates, daily_df["daily_sessions"] / 1000, label="Daily Sessions", color="#8e44ad", linewidth=1.8, linestyle="-.")
    ax1.axvline(pd.to_datetime("2020-02-01"), color="#e74c3c", linestyle=":", linewidth=2, label="Cutoff (2020-02-01)")
    ax1.set_title("Daily Active Users (DAU) and Active Sessions Trend", fontsize=13, fontweight="bold", pad=15)
    ax1.set_xlabel("Date", fontsize=11)
    ax1.set_ylabel("DAU (Thousands)", color="#2980b9", fontsize=11)
    ax2.set_ylabel("Sessions (Thousands)", color="#8e44ad", fontsize=11)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", frameon=True)
    plt.tight_layout()
    fig3_path = OUTPUTS_FIG / "fig3_unique_users_sessions_over_time.png"
    plt.savefig(fig3_path, dpi=200)
    plt.close()
    print(f"Generated: {fig3_path.name}")

    # Figure 4: User Activity Distribution (Log Scale Histograms)
    print("Querying user activity sample for Fig 4...")
    user_sample = con.execute("""
    SELECT event_count, session_count
    FROM (
        SELECT user_id, COUNT(*) AS event_count, COUNT(DISTINCT user_session) AS session_count
        FROM raw_events
        WHERE user_id IS NOT NULL
        GROUP BY user_id
    )
    USING SAMPLE 100000
    """).fetchdf()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.hist(user_sample["event_count"], bins=np.logspace(0, 4, 40), color="#3498db", edgecolor="#2c3e50", alpha=0.8)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_title("Distribution of Events per User (Sample 100k)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Events per User (log scale)", fontsize=10)
    ax1.set_ylabel("User Count (log scale)", fontsize=10)
    ax1.axvline(user_activity_dist["events_median"], color="#e74c3c", linestyle="--", label=f"Median = {user_activity_dist['events_median']:.0f}")
    ax1.axvline(user_activity_dist["events_p90"], color="#f39c12", linestyle=":", label=f"90th Pct = {user_activity_dist['events_p90']:.0f}")
    ax1.legend(loc="upper right")

    ax2.hist(user_sample["session_count"], bins=np.logspace(0, 3, 30), color="#9b59b6", edgecolor="#2c3e50", alpha=0.8)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Distribution of Sessions per User (Sample 100k)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Sessions per User (log scale)", fontsize=10)
    ax2.set_ylabel("User Count (log scale)", fontsize=10)
    ax2.axvline(user_activity_dist["sessions_median"], color="#e74c3c", linestyle="--", label=f"Median = {user_activity_dist['sessions_median']:.0f}")
    ax2.axvline(user_activity_dist["sessions_p90"], color="#f39c12", linestyle=":", label=f"90th Pct = {user_activity_dist['sessions_p90']:.0f}")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    fig4_path = OUTPUTS_FIG / "fig4_user_activity_distribution.png"
    plt.savefig(fig4_path, dpi=200)
    plt.close()
    print(f"Generated: {fig4_path.name}")

    # Figure 5: Purchase Behavior Distribution (Frequency & Monetary)
    print("Querying buyer behavior for Fig 5...")
    buyer_sample = con.execute("""
    SELECT purchase_sessions, total_monetary
    FROM (
        SELECT
            user_id,
            COUNT(DISTINCT user_session) FILTER (WHERE event_type = 'purchase') AS purchase_sessions,
            SUM(price) FILTER (WHERE event_type = 'purchase' AND price > 0) AS total_monetary
        FROM raw_events
        WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-02-01 00:00:00'
          AND user_id IS NOT NULL
        GROUP BY user_id
        HAVING COUNT(*) FILTER (WHERE event_type = 'purchase') > 0
    )
    """).fetchdf()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    # Frequency bar chart
    freq_counts = buyer_sample["purchase_sessions"].value_counts().sort_index()
    # Group >= 5
    freq_binned = {}
    for k, v in freq_counts.items():
        key = str(k) if k < 5 else "5+"
        freq_binned[key] = freq_binned.get(key, 0) + v
    ax1.bar(list(freq_binned.keys()), [v / 1000 for v in freq_binned.values()], color="#2ecc71", edgecolor="#27ae60", width=0.6)
    for i, (k, v) in enumerate(freq_binned.items()):
        pct = v / len(buyer_sample) * 100
        ax1.text(i, v / 1000 + 1, f"{v/1000:.1f}k\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax1.set_title("Buyer Frequency Proxy Distribution (Observation)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Number of Purchase Sessions", fontsize=10)
    ax1.set_ylabel("Buyer Count (Thousands)", fontsize=10)
    ax1.set_ylim(0, max(freq_binned.values()) / 1000 * 1.25)

    # Monetary distribution
    ax2.hist(buyer_sample["total_monetary"], bins=np.logspace(0, 4, 40), color="#1abc9c", edgecolor="#16a085", alpha=0.8)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Buyer Total Monetary Distribution (Log Scale)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Monetary Observed (log scale)", fontsize=10)
    ax2.set_ylabel("Buyer Count (log scale)", fontsize=10)
    ax2.axvline(user_cohort_stats["median_buyer_monetary"], color="#e74c3c", linestyle="--",
                label=f"Median = {user_cohort_stats['median_buyer_monetary']:.1f}")
    ax2.axvline(user_cohort_stats["avg_buyer_monetary"], color="#f39c12", linestyle=":",
                label=f"Mean = {user_cohort_stats['avg_buyer_monetary']:.1f}")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    fig5_path = OUTPUTS_FIG / "fig5_purchase_behavior_distribution.png"
    plt.savefig(fig5_path, dpi=200)
    plt.close()
    print(f"Generated: {fig5_path.name}")

    # Figure 6: Session-Level View-Cart-Purchase Funnel
    fig, ax = plt.subplots(figsize=(9, 5))
    stages = ["All Sessions", "View Sessions", "Cart Sessions", "Purchase Sessions"]
    counts = [tot_sess, view_sess, cart_sess, pur_sess]
    pcts = [100.0, view_sess / tot_sess * 100, cart_sess / tot_sess * 100, pur_sess / tot_sess * 100]
    colors = ["#34495e", "#3498db", "#f39c12", "#2ecc71"]

    y_pos = np.arange(len(stages))
    bars = ax.barh(y_pos, [c / 1e6 for c in counts], color=colors, height=0.55, edgecolor="#2c3e50")
    for i, (bar, count, pct) in enumerate(zip(bars, counts, pcts)):
        step_drop = ""
        if i > 0:
            step_conv = count / counts[i-1] * 100
            step_drop = f" (Step conv: {step_conv:.1f}%)"
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{count/1e6:.2f}M ({pct:.2f}% of total){step_drop}",
                ha="left", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=10, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Number of Sessions (Millions)", fontsize=11)
    ax.set_xlim(0, max(counts) / 1e6 * 1.55)
    ax.set_title("Session-Level Conversion Funnel (Observation Window: Oct 2019 – Jan 2020)", fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    fig6_path = OUTPUTS_FIG / "fig6_session_funnel.png"
    plt.savefig(fig6_path, dpi=200)
    plt.close()
    print(f"Generated: {fig6_path.name}")

    # Figure 7: Missing Value Rates by Month
    fig, ax = plt.subplots(figsize=(10, 5))
    month_keys = list(monthly_profiles.keys())
    cat_missing = [monthly_profiles[m]["missing_category_code_pct"] for m in month_keys]
    brand_missing = [monthly_profiles[m]["missing_brand_pct"] for m in month_keys]
    sess_missing = [monthly_profiles[m]["missing_session_pct"] for m in month_keys]

    x = np.arange(len(month_keys))
    w = 0.25
    ax.bar(x - w, cat_missing, width=w, label="Missing category_code (%)", color="#e74c3c", edgecolor="#333")
    ax.bar(x, brand_missing, width=w, label="Missing brand (%)", color="#f39c12", edgecolor="#333")
    ax.bar(x + w, sess_missing, width=w, label="Missing user_session (%)", color="#9b59b6", edgecolor="#333")

    for i in range(len(month_keys)):
        ax.text(x[i] - w, cat_missing[i] + 1, f"{cat_missing[i]:.1f}%", ha="center", va="bottom", fontsize=8)
        ax.text(x[i], brand_missing[i] + 1, f"{brand_missing[i]:.1f}%", ha="center", va="bottom", fontsize=8)
        ax.text(x[i] + w, sess_missing[i] + 1, f"{sess_missing[i]:.2f}%", ha="center", va="bottom", fontsize=8, color="#8e44ad", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(month_keys, fontsize=10, fontweight="bold")
    ax.set_ylabel("Missing Percentage (%)", fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_title("Missing Value Rates across Monthly CSV Files", fontsize=12, fontweight="bold", pad=15)
    ax.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    fig7_path = OUTPUTS_FIG / "fig7_missing_values_by_month.png"
    plt.savefig(fig7_path, dpi=200)
    plt.close()
    print(f"Generated: {fig7_path.name}")

    # Figure 8: Price Distribution (Sample 100k)
    print("Querying price sample for Fig 8...")
    price_sample = con.execute("""
    SELECT price
    FROM raw_events
    WHERE price IS NOT NULL AND price > 0
    USING SAMPLE 100000
    """).fetchdf()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.hist(price_sample["price"], bins=50, range=(0, 100), color="#3498db", edgecolor="#2980b9", alpha=0.85)
    ax1.set_title("Price Distribution (Zoomed to 0 – 100 units)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Price", fontsize=10)
    ax1.set_ylabel("Frequency", fontsize=10)
    ax1.axvline(price_stats["median_price"], color="#e74c3c", linestyle="--", label=f"Median = {price_stats['median_price']:.2f}")
    ax1.axvline(price_stats["mean_price"], color="#f39c12", linestyle=":", label=f"Mean = {price_stats['mean_price']:.2f}")
    ax1.legend(loc="upper right")

    ax2.hist(price_sample["price"], bins=np.logspace(-1, 3, 50), color="#e67e22", edgecolor="#d35400", alpha=0.85)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Price Distribution (Full Range on Log-Log Scale)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Price (log scale)", fontsize=10)
    ax2.set_ylabel("Frequency (log scale)", fontsize=10)
    ax2.axvline(price_stats["q99"], color="#c0392b", linestyle="--", label=f"99th Pct = {price_stats['q99']:.2f}")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    fig8_path = OUTPUTS_FIG / "fig8_price_distribution.png"
    plt.savefig(fig8_path, dpi=200)
    plt.close()
    print(f"Generated: {fig8_path.name}")

    print("\n" + "=" * 70)
    print("PHASE 1 DATA PROFILING AND FIGURE GENERATION COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    run_profiling()

