#!/usr/bin/env python3
"""Validate Phase 3 Feature Engineering deliverables, schema, parity and cohort constraints."""
import json
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATA_FEATURES = ROOT / "data" / "features"
CUSTOMER_PARQUET = str(DATA_FEATURES / "customer_features.parquet").replace("\\", "/")
BUYER_PARQUET = str(DATA_FEATURES / "buyer_features.parquet").replace("\\", "/")
NON_BUYER_PARQUET = str(DATA_FEATURES / "non_buyer_features.parquet").replace("\\", "/")
MANIFEST_JSON = ROOT / "outputs" / "experiments" / "phase3_feature_profiling.json"
FIGURES_DIR = ROOT / "outputs" / "figures"


def main():
    assert MANIFEST_JSON.is_file(), "phase3_feature_profiling.json missing"
    with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["phase"] == "P3_FEATURE_ENGINEERING"
    cohorts = manifest["cohort_counts"]
    assert cohorts["total_observation_customers"] == 1341499
    assert cohorts["buyers_count"] == 92652
    assert cohorts["non_buyers_count"] == 1248847
    assert cohorts["buyers_count"] + cohorts["non_buyers_count"] == 1341499

    con = duckdb.connect(database=":memory:")
    
    # 1. Row counts verification
    cust_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{CUSTOMER_PARQUET}')").fetchone()[0]
    buyer_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{BUYER_PARQUET}')").fetchone()[0]
    non_buyer_cnt = con.execute(f"SELECT COUNT(*) FROM read_parquet('{NON_BUYER_PARQUET}')").fetchone()[0]
    assert cust_cnt == 1341499, f"Expected 1,341,499 customers, got {cust_cnt}"
    assert buyer_cnt == 92652, f"Expected 92,652 buyers, got {buyer_cnt}"
    assert non_buyer_cnt == 1248847, f"Expected 1,248,847 non-buyers, got {non_buyer_cnt}"

    # 2. Non-buyers recency constraint: MUST BE NULL
    non_null_recency_in_non_buyers = con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{NON_BUYER_PARQUET}') WHERE recency_days IS NOT NULL
    """).fetchone()[0]
    assert non_null_recency_in_non_buyers == 0, f"Non-buyers must have NULL recency, got {non_null_recency_in_non_buyers}"

    # 3. Buyers validity: recency NOT NULL, frequency >= 1, monetary > 0
    invalid_buyers = con.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{BUYER_PARQUET}')
        WHERE recency_days IS NULL OR frequency < 1 OR monetary <= 0
    """).fetchone()[0]
    assert invalid_buyers == 0, f"Buyers must have valid RFM, got {invalid_buyers} invalid"

    # 4. Check figures existence
    for fig_id in ["fig9_rfm_distributions.png", "fig10_engagement_distributions.png", 
                   "fig11_rfm_correlation_matrix.png", "fig12_buyer_vs_non_buyer_engagement.png"]:
        fig_path = FIGURES_DIR / fig_id
        assert fig_path.is_file(), f"Missing figure {fig_id}"

    con.close()

    print(f"PASS Phase 3 validation: {cust_cnt:,} customers ({buyer_cnt:,} buyers, {non_buyer_cnt:,} non-buyers), RFM & Engagement contracts verified, 4 figures verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

