import duckdb

con = duckdb.connect()

print("--- 1. Check holdout_events.parquet ---")
print("Total holdout rows:", con.execute("SELECT COUNT(*) FROM 'data/cleaned/holdout_events.parquet'").fetchone()[0])
print("Holdout event types:")
print(con.execute("SELECT event_type, COUNT(*) as n FROM 'data/cleaned/holdout_events.parquet' GROUP BY event_type").fetchall())

print("\n--- 2. Future Behavior of the 92,652 Buyers by Cluster ---")
query_future_buyers = """
WITH holdout_user_summary AS (
    SELECT 
        user_id,
        COUNT(*) as holdout_total_events,
        COUNT(DISTINCT user_session_id) as holdout_total_sessions,
        COUNT(CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = true AND price > 0 THEN 1 END) as holdout_valid_purchases,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = true AND price > 0 THEN user_session_id END) as holdout_purchase_sessions,
        SUM(CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = true AND price > 0 THEN price ELSE 0 END) as holdout_monetary
    FROM 'data/cleaned/holdout_events.parquet'
    GROUP BY user_id
)
SELECT 
    b.cluster,
    COUNT(b.user_id) as n_customers,
    COUNT(CASE WHEN h.holdout_total_events > 0 THEN 1 END) as future_active_users,
    ROUND(COUNT(CASE WHEN h.holdout_total_events > 0 THEN 1 END) * 100.0 / COUNT(b.user_id), 2) as future_activity_rate_pct,
    COUNT(CASE WHEN h.holdout_purchase_sessions > 0 THEN 1 END) as future_buyers,
    ROUND(COUNT(CASE WHEN h.holdout_purchase_sessions > 0 THEN 1 END) * 100.0 / COUNT(b.user_id), 2) as future_purchase_rate_pct,
    SUM(COALESCE(h.holdout_purchase_sessions, 0)) as future_total_purchase_sessions,
    ROUND(SUM(COALESCE(h.holdout_monetary, 0)), 2) as future_total_spend,
    ROUND(SUM(COALESCE(h.holdout_monetary, 0)) / COUNT(b.user_id), 2) as future_spend_per_customer,
    ROUND(SUM(COALESCE(h.holdout_monetary, 0)) / NULLIF(COUNT(CASE WHEN h.holdout_purchase_sessions > 0 THEN 1 END), 0), 2) as future_spend_per_buyer
FROM 'data/features/buyer_clusters.parquet' b
LEFT JOIN holdout_user_summary h ON b.user_id = h.user_id
GROUP BY b.cluster
ORDER BY b.cluster
"""
print(con.execute(query_future_buyers).fetchall())

print("\n--- 3. Check Future Behavior of Non-Buyers (Benchmark Cohort) ---")
query_future_non_buyers = """
WITH holdout_user_summary AS (
    SELECT 
        user_id,
        COUNT(*) as holdout_total_events,
        COUNT(DISTINCT user_session_id) as holdout_total_sessions,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = true AND price > 0 THEN user_session_id END) as holdout_purchase_sessions,
        SUM(CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = true AND price > 0 THEN price ELSE 0 END) as holdout_monetary
    FROM 'data/cleaned/holdout_events.parquet'
    GROUP BY user_id
)
SELECT 
    'Non-Buyers' as cohort,
    COUNT(nb.user_id) as n_customers,
    COUNT(CASE WHEN h.holdout_total_events > 0 THEN 1 END) as future_active_users,
    ROUND(COUNT(CASE WHEN h.holdout_total_events > 0 THEN 1 END) * 100.0 / COUNT(nb.user_id), 2) as future_activity_rate_pct,
    COUNT(CASE WHEN h.holdout_purchase_sessions > 0 THEN 1 END) as future_buyers,
    ROUND(COUNT(CASE WHEN h.holdout_purchase_sessions > 0 THEN 1 END) * 100.0 / COUNT(nb.user_id), 2) as future_purchase_rate_pct,
    ROUND(SUM(COALESCE(h.holdout_monetary, 0)) / COUNT(nb.user_id), 2) as future_spend_per_customer
FROM 'data/features/non_buyer_features.parquet' nb
LEFT JOIN holdout_user_summary h ON nb.user_id = h.user_id
"""
print(con.execute(query_future_non_buyers).fetchall())

