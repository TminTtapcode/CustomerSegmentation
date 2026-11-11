import json
from pathlib import Path
import os

manifest_path = Path("outputs/experiments/phase2_data_cleaning.json")
with open(manifest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Update with audited findings
data["session_reconciliation"] = {
    "distinct_session_uuids_raw": 4535941,
    "distinct_session_uuids_clean": 4535941,
    "session_uuid_delta": 0,
    "distinct_composite_sessions_raw_non_null": 4536272,
    "distinct_composite_sessions_clean_non_null": 4536272,
    "composite_session_delta": 0,
    "session_collisions_raw_uuids_with_multiple_users": 331,
    "session_collisions_clean_user_session_id": 0,
    "users_with_null_session_raw": 1533,
    "rows_with_null_session_raw": 4598,
    "rows_with_null_session_clean": 4085,
    "explanation": "No sessions were lost due to deduplication. The difference of 1,533 between raw composite-with-null (4,537,805) and clean non-null (4,536,272) was entirely due to NULL session handling: 1,533 users had NULL session_id which COUNT(DISTINCT user_session_id) excludes in SQL."
}

data["monetary_3step_reconciliation"] = {
    "currency_unit": "currency_units (unspecified source currency)",
    "step1_raw_purchase_events": 1045014,
    "step1_raw_purchase_sum": 5141715.66,
    "step2_dedup_purchase_events": 1044221,
    "step2_dedup_purchase_sum": 5138624.02,
    "step2_dedup_delta": -3091.64,
    "step2_duplicate_events_removed": 793,
    "step3_valid_monetary_events": 1044133,
    "step3_valid_monetary_sum": 5141266.90,
    "step3_invalid_price_delta": 2642.88,
    "step3_invalid_purchases_excluded": 88,
    "step3_negative_purchases_count": 87,
    "step3_negative_purchases_sum": -2642.88,
    "step3_zero_purchases_count": 1,
    "net_change_step1_to_step3": -448.76
}

data["storage_reconciliation"] = {
    "clean_events_parquet_mb": round(os.path.getsize("data/cleaned/clean_events.parquet") / (1024 * 1024), 2),
    "observation_events_parquet_mb": round(os.path.getsize("data/cleaned/observation_events.parquet") / (1024 * 1024), 2),
    "holdout_events_parquet_mb": round(os.path.getsize("data/cleaned/holdout_events.parquet") / (1024 * 1024), 2),
    "total_physical_storage_on_disk_mb": round((os.path.getsize("data/cleaned/clean_events.parquet") + os.path.getsize("data/cleaned/observation_events.parquet") + os.path.getsize("data/cleaned/holdout_events.parquet")) / (1024 * 1024), 2),
    "minimal_deployment_storage_mb": round((os.path.getsize("data/cleaned/observation_events.parquet") + os.path.getsize("data/cleaned/holdout_events.parquet")) / (1024 * 1024), 2),
    "redundancy_explanation": "clean_events.parquet is an exact concatenation of observation + holdout, retained during Phase 2 for cross-dataset audit. In production, observation + holdout (474.69 MB) is sufficient."
}

# Add fair benchmark results
with open("outputs/experiments/fair_benchmark_results.json", "r", encoding="utf-8") as f_bench:
    bench_data = json.load(f_bench)

data["fair_benchmark"] = {
    "comparison_record_set": "EXACT SAME 19,583,742 clean rows on both CSV and Parquet",
    "csv_median_seconds": bench_data["csv_bench"]["median"],
    "csv_cold_seconds": bench_data["csv_bench"]["cold"],
    "csv_mean_seconds": bench_data["csv_bench"]["mean"],
    "csv_stdev_seconds": bench_data["csv_bench"]["stdev"],
    "parquet_median_seconds": bench_data["parquet_bench"]["median"],
    "parquet_cold_seconds": bench_data["parquet_bench"]["cold"],
    "parquet_mean_seconds": bench_data["parquet_bench"]["mean"],
    "parquet_stdev_seconds": bench_data["parquet_bench"]["stdev"],
    "fair_speedup_median": bench_data["speedup_median"],
    "fair_speedup_cold": bench_data["speedup_cold"],
    "note": "Speedup on identical 19.58M rows is 8.09x on median runtime (6.57x on cold cache). Speedup on arbitrary Phase 3 queries will vary based on projection pushdown and query complexity."
}

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Updated outputs/experiments/phase2_data_cleaning.json successfully!")
