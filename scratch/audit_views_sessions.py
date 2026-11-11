import duckdb

con = duckdb.connect()

query = """
SELECT 
    c.cluster as cluster_id,
    count(*) as count,
    -- Sessions 30d
    median(f.sessions_30d) as median_sessions_30d,
    avg(f.sessions_30d) as avg_sessions_30d,
    -- Views 30d
    median(f.views_30d) as median_views_30d,
    avg(f.views_30d) as avg_views_30d,
    -- Recency
    median(f.recency_days) as median_recency,
    avg(f.recency_days) as avg_recency,
    -- Frequency
    median(f.frequency) as median_frequency,
    avg(f.frequency) as avg_frequency,
    -- Monetary
    median(f.monetary) as median_monetary,
    avg(f.monetary) as avg_monetary
FROM read_parquet('data/features/buyer_features.parquet') f
JOIN read_parquet('data/features/buyer_clusters.parquet') c
  ON f.user_id = c.user_id
GROUP BY c.cluster
ORDER BY c.cluster
"""

results = con.execute(query).fetchall()
cols = [desc[0] for desc in con.description]

print(f"{'Cluster':<8} | {'Count':<8} | {'Med Sess':<10} | {'Avg Sess':<10} | {'Med View':<10} | {'Avg View':<10} | {'Med R':<8} | {'Avg R':<8} | {'Med F':<6} | {'Avg F':<6} | {'Med M':<10} | {'Avg M':<10}")
print("-" * 130)
for r in results:
    cid, cnt, m_s, a_s, m_v, a_v, m_r, a_r, m_f, a_f, m_m, a_m = r
    print(f"C{cid:<7} | {cnt:<8} | {m_s:<10.2f} | {a_s:<10.2f} | {m_v:<10.2f} | {a_v:<10.2f} | {m_r:<8.2f} | {a_r:<8.2f} | {m_f:<6.2f} | {a_f:<6.2f} | {m_m:<10.2f} | {a_m:<10.2f}")

