import duckdb

con = duckdb.connect()

print("--- VARIATION WITHIN CLUSTER 1 (VIP) ---")
q1 = """
SELECT 
    CASE 
        WHEN cart_sessions_30d >= 1 THEN 'HAS_CART'
        WHEN sessions_30d >= 2 THEN 'ACTIVE_BROWSING'
        WHEN recency_days <= 45 THEN 'RECENT_PURCHASE_LOW_ACTIVITY'
        ELSE 'INACTIVE_VIP'
    END as sub_pattern,
    COUNT(*) as cnt,
    ROUND(COUNT(*) * 100.0 / 8755, 2) as pct
FROM 'data/features/buyer_clusters.parquet'
WHERE cluster = 1
GROUP BY 1
"""
print(con.execute(q1).fetchall())

print("\n--- VARIATION WITHIN CLUSTER 2 (AT RISK) ---")
q2 = """
SELECT 
    CASE 
        WHEN cart_sessions_30d >= 1 THEN 'HAS_RECENT_CART'
        WHEN monetary >= 60.0 THEN 'HIGH_SPEND_DORMANT'
        WHEN monetary >= 30.0 THEN 'MODERATE_SPEND_DORMANT'
        ELSE 'LOWER_SPEND_DORMANT'
    END as sub_pattern,
    COUNT(*) as cnt,
    ROUND(COUNT(*) * 100.0 / 18608, 2) as pct
FROM 'data/features/buyer_clusters.parquet'
WHERE cluster = 2
GROUP BY 1
"""
print(con.execute(q2).fetchall())

print("\n--- VARIATION WITHIN CLUSTER 3 (RECENT ACTIVE) ---")
q3 = """
SELECT 
    CASE 
        WHEN cart_sessions_30d >= 1 THEN 'HAS_CART'
        WHEN views_30d >= 5 THEN 'HIGH_VIEWS_NO_CART'
        WHEN recency_days <= 14 THEN 'VERY_RECENT_PURCHASE'
        ELSE 'CASUAL_RECENT'
    END as sub_pattern,
    COUNT(*) as cnt,
    ROUND(COUNT(*) * 100.0 / 23144, 2) as pct
FROM 'data/features/buyer_clusters.parquet'
WHERE cluster = 3
GROUP BY 1
"""
print(con.execute(q3).fetchall())

print("\n--- VARIATION WITHIN CLUSTER 0 (DORMANT) ---")
q4 = """
SELECT 
    CASE 
        WHEN cart_sessions_30d >= 1 THEN 'HAS_NEW_CART'
        WHEN sessions_30d >= 1 THEN 'HAS_NEW_SESSION'
        WHEN recency_days > 90 AND monetary < 20.0 THEN 'DEEP_DORMANT_LOW_VALUE'
        ELSE 'STANDARD_DORMANT'
    END as sub_pattern,
    COUNT(*) as cnt,
    ROUND(COUNT(*) * 100.0 / 42145, 2) as pct
FROM 'data/features/buyer_clusters.parquet'
WHERE cluster = 0
GROUP BY 1
"""
print(con.execute(q4).fetchall())

