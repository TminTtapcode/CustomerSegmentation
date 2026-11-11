import duckdb
import json
from pathlib import Path

con = duckdb.connect()

def print_query(title, query):
    print(f"\n=== {title} ===")
    res = con.execute(query)
    cols = [desc[0] for desc in res.description]
    print("\t".join(cols))
    for row in res.fetchall():
        print("\t".join(str(v) for v in row))

print_query("1. BUYER RECOMMENDATIONS PARQUET", "SELECT recommended_tactic, count(*) as cnt FROM 'outputs/recommendations/buyer_recommendations.parquet' GROUP BY recommended_tactic ORDER BY cnt DESC")

print_query("2. NON-BUYER RECOMMENDATIONS PARQUET", "SELECT recommended_tactic, count(*) as cnt FROM 'outputs/recommendations/non_buyer_recommendations.parquet' GROUP BY recommended_tactic ORDER BY cnt DESC")

print_query("3. NON-BUYER TIERS PARQUET", "SELECT engagement_tier, count(*) as cnt FROM 'outputs/recommendations/non_buyer_recommendations.parquet' GROUP BY engagement_tier ORDER BY cnt DESC")

print_query("4. TOTAL BY TACTIC (BUYERS + NON-BUYERS)", """
    SELECT recommended_tactic, sum(cnt) as total_customers
    FROM (
        SELECT recommended_tactic, count(*) as cnt FROM 'outputs/recommendations/buyer_recommendations.parquet' GROUP BY recommended_tactic
        UNION ALL
        SELECT recommended_tactic, count(*) as cnt FROM 'outputs/recommendations/non_buyer_recommendations.parquet' GROUP BY recommended_tactic
    )
    GROUP BY recommended_tactic
    ORDER BY total_customers DESC
""")

print("\n=== 5. PHASE 6 SUMMARY JSON ===")
p6_path = Path("outputs/experiments/phase6_decision_support_summary.json")
if p6_path.exists():
    with open(p6_path, "r", encoding="utf-8") as f:
        p6_summary = json.load(f)
    print("Keys in P6 summary:", list(p6_summary.keys()))
    print("P6 summary content:\n", json.dumps(p6_summary, indent=2))

print("\n=== 6. SNAPSHOT JSON ===")
snap_path = Path("outputs/dashboard/ivre_dashboard_snapshot.json")
if snap_path.exists():
    with open(snap_path, "r", encoding="utf-8") as f:
        snap = json.load(f)
    print("Tactics in snapshot:")
    for t in snap.get("candidate_tactics", []):
        print(f"  {t.get('tactic_id')}: {t.get('allocated_customers')} ({t.get('pct_of_population')}%)")
    print("\nNon-buyer tiers in snapshot:")
    for tier in snap.get("non_buyer_tiers", []):
        print(f"  {tier.get('tier_id')}: {tier.get('n_customers')} ({tier.get('pct_of_non_buyers')}%)")

print_query("7. CLUSTERS SUMMARY IN BUYER_CLUSTERS.PARQUET", """
    SELECT 
        cluster_id, 
        count(*) as n_customers,
        round(median(recency_days), 2) as median_recency,
        round(mean(recency_days), 2) as mean_recency,
        round(median(frequency), 2) as median_frequency,
        round(mean(frequency), 2) as mean_frequency,
        round(median(monetary), 2) as median_monetary,
        round(mean(monetary), 2) as mean_monetary,
        round(median(sessions_30d), 2) as median_sessions_30d,
        round(mean(sessions_30d), 2) as mean_sessions_30d
    FROM 'data/features/buyer_clusters.parquet'
    GROUP BY cluster_id
    ORDER BY cluster_id
""")