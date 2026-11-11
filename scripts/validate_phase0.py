#!/usr/bin/env python3
"""Validate Phase 0 config and KPI contracts WITHOUT third-party packages.

Both *.yaml files use YAML 1.2's JSON-compatible subset; json.load is sufficient.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def time_utc(value):
    date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert date.utcoffset() is not None
    return date.astimezone(timezone.utc)


def main():
    project = json.loads((ROOT / "configs/project.yaml").read_text(encoding="utf-8"))
    dictionary = json.loads((ROOT / "configs/kpi_dictionary.yaml").read_text(encoding="utf-8"))
    t = project["time"]
    assert (time_utc(t["observation_start_inclusive"]) < time_utc(t["observation_end_exclusive"]) ==
            time_utc(t["future_start_inclusive"]) < time_utc(t["future_end_exclusive"]))
    assert project["dataset"]["order_id_present"] is False
    assert project["dataset"]["verified_local"] in (True, False)
    assert project["marketing"]["campaign_effect_data_present"] is False
    assert project["time"]["holdout_used_for_tuning"] is False
    metrics = dictionary["metrics"]
    ids = [m["id"] for m in metrics]
    assert len(ids) == len(set(ids)), "KPI ids must be unique"
    assert len(metrics) >= 12, "KPI dictionary incomplete"
    for m in metrics:
        assert all(k in m for k in ("id", "name", "grain", "time_window", "formula", "unit", "source_columns", "observability", "caveat")), m
        assert m["observability"] in ("measurable_after_p1", "measurable_after_p5", "not_observable_with_REES46"), m
        if "numerator" in m:
            assert "denominator" in m and m["unit"] == "ratio", m
    assert dictionary["common"]["window_convention"] == "[start_inclusive,end_exclusive)"
    assert "repeat_buyer_rate_proxy" in ids and "buyer_frequency_proxy" in ids
    assert "future_purchase_rate_by_segment" in ids
    for report in project["reports"]:
        assert (ROOT / report).is_file(), f"missing report {report}"
    print(f"PASS Phase 0 contract check: {len(metrics)} KPI definitions, half-open time windows, no fabricated verified dataset.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
