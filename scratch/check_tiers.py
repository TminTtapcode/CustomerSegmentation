import duckdb

con = duckdb.connect()

print("--- NON-BUYER RECOMMENDATIONS ---")
for r in con.execute("SELECT recommended_tactic, count(*) FROM read_parquet('outputs/recommendations/non_buyer_recommendations.parquet') GROUP BY 1 ORDER BY 2 DESC").fetchall():
    print(r)

print("--- BUYER RECOMMENDATIONS ---")
for r in con.execute("SELECT recommended_tactic, count(*) FROM read_parquet('outputs/recommendations/buyer_recommendations.parquet') GROUP BY 1 ORDER BY 2 DESC").fetchall():
    print(r)

print("--- NON-BUYER ENGAGEMENT LOGIC IN PHASE 6 ---")
# Let's inspect columns of non_buyer_recommendations
cols = [c[0] for c in con.execute("DESCRIBE SELECT * FROM read_parquet('outputs/recommendations/non_buyer_recommendations.parquet')").fetchall()]
print("Cols:", cols)
for r in con.execute("SELECT engagement_tier, count(*) FROM read_parquet('outputs/recommendations/non_buyer_recommendations.parquet') GROUP BY 1 ORDER BY 2 DESC").fetchall():
    print(r)