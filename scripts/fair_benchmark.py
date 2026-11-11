import duckdb
import time
import os
import psutil
import json
import statistics

con = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})

print("--- EXPORTING CLEAN CSV FOR FAIR BENCHMARK ---")
t0_export = time.perf_counter()
csv_bench_path = "data/cleaned/clean_events_benchmark.csv"
parquet_bench_path = "data/cleaned/clean_events.parquet"

if not os.path.exists(csv_bench_path):
    print("Exporting clean_events to CSV...")
    con.execute(f"""
        COPY (SELECT * FROM read_parquet('{parquet_bench_path}'))
        TO '{csv_bench_path}' (HEADER, DELIMITER ',')
    """)
    t1_export = time.perf_counter()
    print(f"Exported in {t1_export - t0_export:.2f}s")
else:
    print("CSV benchmark file already exists.")

csv_size_mb = os.path.getsize(csv_bench_path) / (1024 * 1024)
parquet_size_mb = os.path.getsize(parquet_bench_path) / (1024 * 1024)
print(f"File sizes: Clean CSV = {csv_size_mb:.2f} MB | Clean Parquet = {parquet_size_mb:.2f} MB")

# Benchmark query
query_template = """
    SELECT 
        event_type, 
        COUNT(*) AS event_count, 
        COUNT(DISTINCT user_id) AS unique_users, 
        SUM(price) AS total_val
    FROM {table}
    GROUP BY event_type
"""

process = psutil.Process(os.getpid())

def run_benchmark(source_type, table_expr, runs=5):
    times = []
    peak_rss = 0
    print(f"\n--- BENCHMARKING {source_type} ({runs} runs) ---")
    for i in range(runs):
        con_fresh = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})
        t0 = time.perf_counter()
        res = con_fresh.execute(query_template.format(table=table_expr)).fetchall()
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        current_rss = process.memory_info().rss / (1024 * 1024)
        peak_rss = max(peak_rss, current_rss)
        run_type = "Cold" if i == 0 else f"Warm #{i}"
        print(f"Run {i+1} ({run_type}): {elapsed:.4f}s | Result rows: {len(res)} | RSS: {current_rss:.2f} MB")
        con_fresh.close()
    
    return {
        "runs": times,
        "cold": times[0],
        "warm_runs": times[1:],
        "median": statistics.median(times),
        "mean": statistics.mean(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "peak_rss_mb": peak_rss
    }

bench_csv = run_benchmark("Clean CSV (19.58M rows)", f"read_csv('{csv_bench_path}', auto_detect=true, header=true)")
bench_parquet = run_benchmark("Clean Parquet (19.58M rows)", f"read_parquet('{parquet_bench_path}')")

speedup_median = bench_csv["median"] / bench_parquet["median"]
speedup_cold = bench_csv["cold"] / bench_parquet["cold"]

print("\n================ BENCHMARK SUMMARY (FAIR COMPARISON) ================")
print(f"Record set: EXACT SAME 19,583,742 clean rows on both formats")
print(f"CSV Size: {csv_size_mb:.2f} MB | Parquet Size: {parquet_size_mb:.2f} MB | Compression: {csv_size_mb / parquet_size_mb:.2f}x")
print(f"CSV Runtime: Median = {bench_csv['median']:.4f}s (Cold: {bench_csv['cold']:.4f}s, Mean: {bench_csv['mean']:.4f}s ± {bench_csv['stdev']:.4f}s)")
print(f"Parquet Runtime: Median = {bench_parquet['median']:.4f}s (Cold: {bench_parquet['cold']:.4f}s, Mean: {bench_parquet['mean']:.4f}s ± {bench_parquet['stdev']:.4f}s)")
print(f"FAIR SPEEDUP (Median): {speedup_median:.2f}x")
print(f"FAIR SPEEDUP (Cold): {speedup_cold:.2f}x")

results = {
    "fair_comparison": True,
    "row_count": 19583742,
    "csv_size_mb": csv_size_mb,
    "parquet_size_mb": parquet_size_mb,
    "compression_ratio": csv_size_mb / parquet_size_mb,
    "csv_bench": bench_csv,
    "parquet_bench": bench_parquet,
    "speedup_median": speedup_median,
    "speedup_cold": speedup_cold
}

with open("outputs/experiments/fair_benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

# Remove temporary CSV after benchmark to save disk space
print("\nCleaning up temporary CSV benchmark file...")
if os.path.exists(csv_bench_path):
    os.remove(csv_bench_path)
    print("Removed temporary clean_events_benchmark.csv successfully.")

