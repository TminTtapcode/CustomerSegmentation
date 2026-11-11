"""Phase 2 ETL Pipeline: Data Preparation, Cleaning, Flagging, and Parquet Export.

Pipeline:
Raw CSVs -> Schema Validation -> Deduplication -> Cleaning & Flagging -> Temporal Split -> Parquet Export
-> Data Quality Audit -> Empirical Benchmark (CSV vs Parquet)
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
import psutil

# Directories
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_CLEANED = ROOT / "data" / "cleaned"
OUTPUTS_EXP = ROOT / "outputs" / "experiments"
DATA_CLEANED.mkdir(parents=True, exist_ok=True)
OUTPUTS_EXP.mkdir(parents=True, exist_ok=True)


class MemoryMonitor:
    def __init__(self, interval: float = 0.2):
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


def run_phase2_etl():
    print("=" * 70)
    print("STARTING PHASE 2 — DATA PREPARATION & CLEANING ETL")
    print("=" * 70)

    # Monitor memory and time
    monitor = MemoryMonitor(interval=0.2)
    monitor.start()
    t_pipeline_start = time.perf_counter()

    con = duckdb.connect(database=":memory:")
    con.execute("SET memory_limit = '2GB'")
    con.execute("SET threads = 4")
    con.execute("SET preserve_insertion_order = false")

    all_raw_glob = str(DATA_RAW / "20*.csv").replace("\\", "/")
    raw_files = sorted(list(DATA_RAW.glob("20*.csv")))
    raw_bytes = sum(f.stat().st_size for f in raw_files)
    print(f"Input Raw Data: {len(raw_files)} files, {raw_bytes / (1024*1024):.2f} MB")

    # -------------------------------------------------------------
    # STEP 1: Schema Validation & Raw Count
    # -------------------------------------------------------------
    t_step1_start = time.perf_counter()
    print("\n[Step 1] Validating Raw Schema and Counting Rows...")
    raw_count = int(con.execute(f"SELECT COUNT(*) FROM read_csv('{all_raw_glob}', header=True, auto_detect=True)").fetchone()[0])
    t_step1 = time.perf_counter() - t_step1_start
    print(f"  Raw Rows: {raw_count:,} (Validated in {t_step1:.2f}s)")

    # -------------------------------------------------------------
    # STEP 2: Create Clean & Flagged View (Deduplication + Rules)
    # -------------------------------------------------------------
    t_step2_start = time.perf_counter()
    print("\n[Step 2] Applying Cleaning Rules, Deduplication, and Quality Flags...")

    # We use ROW_NUMBER() to identify and remove exact duplicate events (same second, same user, same session, same product, same event_type, same price)
    # And we construct composite session key: user_id || '_' || user_session to avoid the 331 session ID collisions across users.
    con.execute(f"""
    CREATE TABLE clean_events_staging AS
    WITH ranked_events AS (
        SELECT 
            event_time,
            CAST(event_time AS DATE) AS event_date,
            event_type,
            user_id,
            user_session AS session_id,
            CASE 
                WHEN user_session IS NOT NULL THEN CAST(user_id AS VARCHAR) || '_' || user_session 
                ELSE NULL 
            END AS user_session_id,
            product_id,
            category_id,
            COALESCE(category_code, 'unknown') AS category_code,
            COALESCE(brand, 'unknown') AS brand,
            price,
            SUBSTRING(CAST(CAST(event_time AS DATE) AS VARCHAR), 1, 7) AS source_month,
            CASE 
                WHEN event_time < '2020-02-01 00:00:00' THEN 'observation'
                ELSE 'holdout'
            END AS split_partition,
            -- Quality flags
            CASE 
                WHEN user_session IS NULL THEN 'MISSING_SESSION'
                WHEN price < 0 THEN 'PRICE_NEGATIVE'
                WHEN price = 0 THEN 'PRICE_ZERO'
                WHEN brand IS NULL AND category_code IS NULL THEN 'MISSING_BRAND_AND_CATEGORY'
                WHEN brand IS NULL THEN 'MISSING_BRAND'
                WHEN category_code IS NULL THEN 'MISSING_CATEGORY'
                ELSE 'VALID'
            END AS quality_flag,
            -- Monetary eligibility: purchase event with price > 0 and user_id present
            CASE 
                WHEN event_type = 'purchase' AND price > 0 AND user_id IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS is_valid_for_monetary,
            -- Engagement eligibility: all user interactions
            CASE 
                WHEN user_id IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS is_valid_for_engagement,
            -- Session validity: both user and session present
            CASE 
                WHEN user_id IS NOT NULL AND user_session IS NOT NULL THEN TRUE
                ELSE FALSE
            END AS is_valid_session,
            -- Independent quality flags
            CASE WHEN brand IS NULL THEN TRUE ELSE FALSE END AS is_missing_brand,
            CASE WHEN category_code IS NULL THEN TRUE ELSE FALSE END AS is_missing_category_code,
            CASE WHEN price <= 0 THEN TRUE ELSE FALSE END AS is_invalid_price,
            CASE WHEN user_session IS NULL THEN TRUE ELSE FALSE END AS is_missing_session,
            -- Deduplication rank
            ROW_NUMBER() OVER (
                PARTITION BY event_time, event_type, product_id, category_id, user_id, user_session, price
                ORDER BY event_time
            ) AS dup_rank
        FROM read_csv('{all_raw_glob}', header=True, auto_detect=True)
    )
    SELECT 
        event_time,
        event_date,
        event_type,
        user_id,
        session_id,
        user_session_id,
        product_id,
        category_id,
        category_code,
        brand,
        price,
        source_month,
        split_partition,
        quality_flag,
        is_valid_for_monetary,
        is_valid_for_engagement,
        is_valid_session,
        is_missing_brand,
        is_missing_category_code,
        is_invalid_price,
        is_missing_session
    FROM ranked_events
    WHERE dup_rank = 1;
    """)
    t_step2 = time.perf_counter() - t_step2_start

    clean_count = int(con.execute("SELECT COUNT(*) FROM clean_events_staging").fetchone()[0])
    dedup_removed = raw_count - clean_count
    print(f"  Clean Staging Rows: {clean_count:,}")
    print(f"  Deduplicated Exact Duplicates Removed: {dedup_removed:,} ({dedup_removed / raw_count * 100:.3f}%)")
    print(f"  Staging created in {t_step2:.2f}s")

    # -------------------------------------------------------------
    # STEP 3: Export to Parquet (ZSTD compressed)
    # -------------------------------------------------------------
    t_step3_start = time.perf_counter()
    print("\n[Step 3] Exporting Clean Parquet Datasets...")

    obs_parquet = str(DATA_CLEANED / "observation_events.parquet").replace("\\", "/")
    holdout_parquet = str(DATA_CLEANED / "holdout_events.parquet").replace("\\", "/")
    all_clean_parquet = str(DATA_CLEANED / "clean_events.parquet").replace("\\", "/")

    # Export Observation Dataset
    print("  Exporting observation_events.parquet (Oct 2019 - Jan 2020)...")
    con.execute(f"""
    COPY (
        SELECT * FROM clean_events_staging WHERE split_partition = 'observation'
        ORDER BY event_time
    ) TO '{obs_parquet}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
    """)

    # Export Holdout Dataset
    print("  Exporting holdout_events.parquet (Feb 2020)...")
    con.execute(f"""
    COPY (
        SELECT * FROM clean_events_staging WHERE split_partition = 'holdout'
        ORDER BY event_time
    ) TO '{holdout_parquet}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
    """)

    # Export Full Combined Clean Parquet
    print("  Exporting clean_events.parquet (Full clean dataset)...")
    con.execute(f"""
    COPY (
        SELECT * FROM clean_events_staging
        ORDER BY event_time
    ) TO '{all_clean_parquet}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
    """)
    t_step3 = time.perf_counter() - t_step3_start
    print(f"  Parquet exports completed in {t_step3:.2f}s")

    # Measure output file sizes
    obs_size = (DATA_CLEANED / "observation_events.parquet").stat().st_size
    holdout_size = (DATA_CLEANED / "holdout_events.parquet").stat().st_size
    all_clean_size = (DATA_CLEANED / "clean_events.parquet").stat().st_size
    print(f"  observation_events.parquet size: {obs_size / (1024*1024):.2f} MB")
    print(f"  holdout_events.parquet size: {holdout_size / (1024*1024):.2f} MB")
    print(f"  clean_events.parquet size: {all_clean_size / (1024*1024):.2f} MB")
    print(f"  Raw CSV Total: {raw_bytes / (1024*1024):.2f} MB -> Clean Parquet: {all_clean_size / (1024*1024):.2f} MB "
          f"(Compression ratio: {raw_bytes / all_clean_size:.2f}x)")

    # -------------------------------------------------------------
    # STEP 4: Reconciliation and Quality Audit
    # -------------------------------------------------------------
    t_step4_start = time.perf_counter()
    print("\n[Step 4] Running Full Data Quality Audit & Reconciliation...")

    # Counts by split_partition
    split_counts = con.execute("""
    SELECT 
        split_partition,
        COUNT(*) AS rows,
        COUNT(DISTINCT user_id) AS distinct_users,
        COUNT(DISTINCT user_session_id) AS distinct_sessions,
        COUNT(*) FILTER (WHERE event_type = 'view') AS views,
        COUNT(*) FILTER (WHERE event_type = 'cart') AS carts,
        COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS removes,
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases,
        COUNT(*) FILTER (WHERE is_valid_for_monetary) AS valid_monetary_purchases,
        SUM(price) FILTER (WHERE is_valid_for_monetary) AS valid_monetary_sum,
        COUNT(*) FILTER (WHERE price <= 0) AS price_le_zero_count,
        COUNT(*) FILTER (WHERE session_id IS NULL) AS missing_session_count
    FROM clean_events_staging
    GROUP BY split_partition
    """).fetchdf()
    print("\nReconciliation by Partition:")
    print(split_counts.to_string(index=False))

    # Flag breakdown
    flag_counts = con.execute("""
    SELECT quality_flag, COUNT(*) AS count, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 3) AS pct
    FROM clean_events_staging
    GROUP BY quality_flag
    ORDER BY count DESC;
    """).fetchdf()
    print("\nQuality Flags Distribution:")
    print(flag_counts.to_string(index=False))

    # Monetary comparison: Raw vs Clean Valid
    monetary_reconciliation = con.execute("""
    SELECT 
        COUNT(*) FILTER (WHERE event_type = 'purchase') AS raw_purchases,
        COUNT(*) FILTER (WHERE is_valid_for_monetary) AS valid_purchases,
        COUNT(*) FILTER (WHERE event_type = 'purchase' AND NOT is_valid_for_monetary) AS excluded_purchases_count,
        SUM(price) FILTER (WHERE event_type = 'purchase') AS raw_purchase_price_sum,
        SUM(price) FILTER (WHERE is_valid_for_monetary) AS clean_valid_monetary_sum,
        SUM(price) FILTER (WHERE event_type = 'purchase' AND price <= 0) AS excluded_price_sum
    FROM clean_events_staging
    WHERE split_partition = 'observation';
    """).fetchdf().iloc[0].to_dict()
    print("\nMonetary Reconciliation (Observation Window):")
    print(f"  Raw Purchases: {monetary_reconciliation['raw_purchases']:,}")
    print(f"  Valid Monetary Purchases (price > 0): {monetary_reconciliation['valid_purchases']:,}")
    print(f"  Excluded Purchases (price <= 0): {monetary_reconciliation['excluded_purchases_count']}")
    print(f"  Raw Sum Price: {monetary_reconciliation['raw_purchase_price_sum']:,.2f}")
    print(f"  Clean Valid Monetary: {monetary_reconciliation['clean_valid_monetary_sum']:,.2f}")
    print(f"  Excluded Price (Negative/Zero): {monetary_reconciliation['excluded_price_sum']}")

    t_step4 = time.perf_counter() - t_step4_start

    # -------------------------------------------------------------
    # STEP 5: Empirical Benchmark (Raw CSV vs Clean Parquet)
    # -------------------------------------------------------------
    print("\n[Step 5] Running Empirical Performance Benchmark: Raw CSV vs Clean Parquet...")
    test_query_csv = f"""
    SELECT event_type, COUNT(*), COUNT(DISTINCT user_id), SUM(price) FILTER (WHERE price > 0)
    FROM read_csv('{all_raw_glob}', header=True, auto_detect=True)
    GROUP BY event_type;
    """
    test_query_parquet = f"""
    SELECT event_type, COUNT(*), COUNT(DISTINCT user_id), SUM(price) FILTER (WHERE price > 0)
    FROM read_parquet('{all_clean_parquet}')
    GROUP BY event_type;
    """

    # Benchmark CSV
    t_csv_start = time.perf_counter()
    con.execute(test_query_csv).fetchall()
    t_csv = time.perf_counter() - t_csv_start

    # Benchmark Parquet
    t_pq_start = time.perf_counter()
    con.execute(test_query_parquet).fetchall()
    t_pq = time.perf_counter() - t_pq_start

    speedup = round(t_csv / t_pq, 2) if t_pq > 0 else 0
    print(f"  Benchmark Query on Raw CSV: {t_csv:.2f} s")
    print(f"  Benchmark Query on Clean Parquet: {t_pq:.2f} s")
    print(f"  Measured Speedup: {speedup}x faster on Clean Parquet!")

    # -------------------------------------------------------------
    # STEP 6: Pipeline Total Runtime & Memory Recording
    # -------------------------------------------------------------
    t_pipeline_end = time.perf_counter()
    monitor.stop()

    wall_time = round(t_pipeline_end - t_pipeline_start, 2)
    throughput = round(raw_count / wall_time, 1)
    baseline_rss_mb = round(monitor.baseline_rss / (1024 * 1024), 2)
    peak_rss_mb = round(monitor.peak_rss / (1024 * 1024), 2)
    rss_delta_mb = round(peak_rss_mb - baseline_rss_mb, 2)

    print("\n" + "=" * 70)
    print("PHASE 2 ETL EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Total Pipeline Wall Time: {wall_time} seconds")
    print(f"Throughput: {throughput:,.1f} rows/second")
    print(f"Memory: Baseline = {baseline_rss_mb} MB | Peak RSS = {peak_rss_mb} MB (Delta: +{rss_delta_mb} MB)")
    print(f"Input: {raw_bytes / (1024*1024):.2f} MB CSV -> Output: {all_clean_size / (1024*1024):.2f} MB Parquet")

    # -------------------------------------------------------------
    # STEP 7: Export Manifest & Metadata JSON
    # -------------------------------------------------------------
    manifest = {
        "phase": "P2_DATA_PREPARATION",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hardware": {
            "os": platform.platform(),
            "cpu_count": os.cpu_count(),
            "duckdb_version": duckdb.__version__,
            "duckdb_memory_limit": "2GB",
            "duckdb_threads": 4,
        },
        "performance": {
            "wall_time_seconds": wall_time,
            "throughput_rows_per_second": throughput,
            "baseline_rss_mb": baseline_rss_mb,
            "peak_rss_mb": peak_rss_mb,
            "rss_delta_mb": rss_delta_mb,
            "step_timings_seconds": {
                "step1_validation": round(t_step1, 2),
                "step2_cleaning_staging": round(t_step2, 2),
                "step3_parquet_export": round(t_step3, 2),
                "step4_audit_reconciliation": round(t_step4, 2),
                "step5_benchmark_csv": round(t_csv, 2),
                "step5_benchmark_parquet": round(t_pq, 2),
            },
            "empirical_speedup_parquet_vs_csv": speedup,
        },
        "reconciliation": {
            "raw_rows_total": raw_count,
            "exact_duplicates_removed": dedup_removed,
            "clean_distinct_rows": clean_count,
            "deduplication_rate_pct": round(dedup_removed / raw_count * 100, 3),
            "clean_observation_rows": int(split_counts[split_counts["split_partition"] == "observation"]["rows"].iloc[0]),
            "clean_holdout_rows": int(split_counts[split_counts["split_partition"] == "holdout"]["rows"].iloc[0]),
            "raw_input_mb": round(raw_bytes / (1024 * 1024), 2),
            "clean_parquet_mb": round(all_clean_size / (1024 * 1024), 2),
            "observation_parquet_mb": round(obs_size / (1024 * 1024), 2),
            "holdout_parquet_mb": round(holdout_size / (1024 * 1024), 2),
            "compression_ratio": round(raw_bytes / all_clean_size, 2),
        },
        "quality_flags_summary": {r["quality_flag"]: int(r["count"]) for _, r in flag_counts.iterrows()},
        "monetary_reconciliation": {k: round(float(v), 2) for k, v in monetary_reconciliation.items()},
    }

    manifest_path = OUTPUTS_EXP / "phase2_data_cleaning.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Saved Phase 2 cleaning manifest to: {manifest_path}")


if __name__ == "__main__":
    run_phase2_etl()

