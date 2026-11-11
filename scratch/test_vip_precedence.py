import duckdb

con = duckdb.connect()

q = """
SELECT 
    b.cluster,
    CASE
        -- Deep dormant guardrail
        WHEN b.recency_days > 90.0 AND b.monetary < 20.0 AND b.sessions_30d = 0 THEN 'TAC_NO_ACTION'
        
        -- Active VIP gets Loyalty VIP as primary, unless they haven't bought in >30d with active cart
        WHEN b.cluster = 1 AND b.sessions_30d >= 2 AND b.recency_days <= 30 THEN 'TAC_LOYALTY_VIP'
        
        -- High urgency: Active cart in last 30d across any cluster
        WHEN b.cart_sessions_30d >= 1 THEN 'TAC_CART_RECOVERY'
        
        -- Other VIP cases
        WHEN b.cluster = 1 AND b.recency_days <= 45 THEN 'TAC_POST_PURCHASE_CARE'
        WHEN b.cluster = 1 THEN 'TAC_WINBACK_SURVEY'
        
        -- Cluster 2 (At-Risk Spenders)
        WHEN b.cluster = 2 AND b.monetary >= 40.0 THEN 'TAC_WINBACK_SURVEY'
        WHEN b.cluster = 2 THEN 'TAC_LOW_COST_NURTURE'
        
        -- Cluster 3 (Recent Active Prospects)
        WHEN b.cluster = 3 AND b.recency_days <= 14.0 AND b.sessions_30d <= 2 THEN 'TAC_POST_PURCHASE_CARE'
        WHEN b.cluster = 3 AND b.views_30d >= 5 THEN 'TAC_CROSS_SELL'
        WHEN b.cluster = 3 THEN 'TAC_PRODUCT_EDU'
        
        -- Cluster 0 (Dormant Low-Value)
        WHEN b.cluster = 0 AND (b.sessions_30d >= 1 OR b.views_30d >= 3) THEN 'TAC_PRODUCT_EDU'
        ELSE 'TAC_LOW_COST_NURTURE'
    END as tactic,
    COUNT(*) as cnt
FROM 'data/features/buyer_clusters.parquet' b
GROUP BY 1, 2
ORDER BY 1, 3 DESC
"""

res = con.execute(q).fetchall()
for r in res:
    print(f"Cluster {r[0]} -> {r[1]}: {r[2]:,} buyers")

