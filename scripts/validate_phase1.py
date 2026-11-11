#!/usr/bin/env python3
"""Validate Phase 1 Data Understanding outputs, benchmarks, and data contracts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
PROFILE_JSON = ROOT / "outputs" / "experiments" / "phase1_data_profile.json"
FIG_DIR = ROOT / "outputs" / "figures"


def main():
    # 1. Project config check
    project = json.loads((ROOT / "configs/project.yaml").read_text(encoding="utf-8"))
    assert project["dataset"]["verified_local"] is True, "Dataset must be verified local for Phase 1"
    assert project["dataset"]["order_id_present"] is False

    # 2. Raw files check
    raw_files = ["2019-Oct.csv", "2019-Nov.csv", "2019-Dec.csv", "2020-Jan.csv", "2020-Feb.csv"]
    for rf in raw_files:
        assert (DATA_RAW / rf).is_file(), f"Missing raw file: {rf}"

    # 3. Profile JSON check
    assert PROFILE_JSON.is_file(), "phase1_data_profile.json missing"
    with open(PROFILE_JSON, "r", encoding="utf-8") as f:
        profile = json.load(f)
    assert profile["phase"] == "P1_DATA_UNDERSTANDING"
    assert profile["global_statistics"]["total_rows"] == 20692840
    assert profile["global_statistics"]["total_unique_users"] == 1639358
    assert profile["global_statistics"]["total_unique_sessions"] == 4537805
    assert profile["global_statistics"]["missing_user_id_count"] == 0
    assert profile["global_statistics"]["purchase_missing_session_count"] == 0

    # 4. Check all 8 figures
    expected_figures = [
        "fig1_event_type_distribution.png",
        "fig2_daily_monthly_volume.png",
        "fig3_unique_users_sessions_over_time.png",
        "fig4_user_activity_distribution.png",
        "fig5_purchase_behavior_distribution.png",
        "fig6_session_funnel.png",
        "fig7_missing_values_by_month.png",
        "fig8_price_distribution.png",
    ]
    for fig in expected_figures:
        assert (FIG_DIR / fig).is_file(), f"Missing figure: {fig}"

    print(f"PASS Phase 1 validation: 20,692,840 rows profiled across 5 CSVs, 8 figures verified, purchase session proxy 100% valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
