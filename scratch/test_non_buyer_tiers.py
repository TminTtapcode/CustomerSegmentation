import duckdb

con = duckdb.connect()

query = """
SELECT 
    CASE 
        WHEN (cart_sessions_30d >= 1 OR carts_30d >= 1) AND (sessions_30d >= 2 OR views_30d >= 5) THEN 'HIGH_INTENT'
        WHEN (sessions_30d >= 2 OR views_30d >= 5) THEN 'EXPLORING'
        WHEN sessions_30d >= 1 THEN 'LOW_ENGAGEMENT'
        ELSE 'INACTIVE'
    END AS engagement_tier,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / 1248847, 2) as pct
FROM 'data/features/non_buyer_features.parquet'
GROUP BY 1
ORDER BY customer_count DESC
"""

print(con.execute(query).fetchall())

