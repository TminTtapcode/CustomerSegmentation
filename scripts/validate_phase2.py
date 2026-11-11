#!/usr/bin/env python3
"""Validate Phase 2 Data Preparation deliverables, parity, and Parquet integrity."""
import json
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATA_CLEANED = ROOT / "data" / "cleaned"
OBS_PARQUET = str(DATA_CLEANED / "observation_events.parquet").replace("\\", "/")
HOLDOUT_PARQUET = str(DATA_CLEANED / "holdout_events.parquet").replace("\\", "/")
CLEAN_PARQUET = str(DATA_CLEANED / "clean_events.parquet").replace("\\", "/")
MANIFEST_JSON = ROOT / "outputs" / "experiments" / "phase2_data_cleaning.json"


def main():
    assert MANIFEST_JSON.is_file(), "phase2_data_cleaning.json missing"
    with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["phase"] == "P2_DATA_PREPARATION"
    rec = manifest["reconciliation"]
    assert rec["raw_rows_total"] == 20692840
    assert rec["exact_duplicates_removed"] == 1109098
    assert rec["clean_distinct_rows"] == 19583742
    assert rec["clean_observation_rows"] == 15667350
    assert rec["clean_holdout_rows"] == 3916392
    assert rec["clean_parquet_mb"] < 500.0, f"Expected clean Parquet <500MB, got {rec['clean_parquet_mb']}"

    # Audited assertions: Session reconciliation & fair benchmark
    assert manifest["session_reconciliation"]["session_uuid_delta"] == 0, "Session UUIDs must be 100% preserved"
    assert manifest["session_reconciliation"]["composite_session_delta"] == 0, "Composite sessions must be 100% preserved"
    assert manifest["fair_benchmark"]["fair_speedup_median"] > 5.0, "Fair benchmark median speedup must exceed 5.0x"
    assert manifest["monetary_3step_reconciliation"]["step3_valid_monetary_events"] == 1044133

    con = duckdb.connect(database=":memory:")
    # Check that reading Parquet works and row counts match
    obs_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{OBS_PARQUET}')").fetchone()[0]
    holdout_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{HOLDOUT_PARQUET}')").fetchone()[0]
    total_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{CLEAN_PARQUET}')").fetchone()[0]
    assert obs_cnt == 15667350
    assert holdout_cnt == 3916392
    assert total_cnt == 19583742
    con.close()

    print(f"PASS Phase 2 validation: 19,583,742 clean rows (15.67M observation, 3.92M holdout), Parquet size: {rec['clean_parquet_mb']} MB (compression: {rec['compression_ratio']}x), speedup: {manifest['performance']['empirical_speedup_parquet_vs_csv']}x.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

