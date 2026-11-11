import duckdb, time

con = duckdb.connect()

t0 = time.perf_counter()
res = con.execute("""
    SELECT 
        b.cluster,
        CASE
            WHEN b.recency_days > 90.0 AND b.monetary < 20.0 AND b.sessions_30d = 0 THEN 'TAC_NO_ACTION'
            WHEN b.cart_sessions_30d >= 1 THEN 'TAC_CART_RECOVERY'
            WHEN b.cluster = 1 AND b.sessions_30d >= 2 THEN 'TAC_LOYALTY_VIP'
            WHEN b.cluster = 1 AND b.recency_days <= 45 THEN 'TAC_POST_PURCHASE_CARE'
            WHEN b.cluster = 1 THEN 'TAC_WINBACK_SURVEY'
            WHEN b.cluster = 2 AND b.monetary >= 40.0 THEN 'TAC_WINBACK_SURVEY'
            WHEN b.cluster = 2 THEN 'TAC_LOW_COST_NURTURE'
            WHEN b.cluster = 3 AND b.recency_days <= 14.0 AND b.sessions_30d <= 2 THEN 'TAC_POST_PURCHASE_CARE'
            WHEN b.cluster = 3 AND b.views_30d >= 5 THEN 'TAC_CROSS_SELL'
            WHEN b.cluster = 3 THEN 'TAC_PRODUCT_EDU'
            WHEN b.cluster = 0 AND (b.sessions_30d >= 1 OR b.views_30d >= 3) THEN 'TAC_PRODUCT_EDU'
            ELSE 'TAC_LOW_COST_NURTURE'
        END as tactic,
        COUNT(*) as cnt
    FROM 'data/features/buyer_clusters.parquet' b
    GROUP BY 1, 2
    ORDER BY 1, 3 DESC
""").fetchall()

t1 = time.perf_counter()
print(f"Processed 92,652 buyers in {t1 - t0:.3f} seconds!")
for r in res:
    print(f"Cluster {r[0]} -> {r[1]}: {r[2]:,} buyers")

