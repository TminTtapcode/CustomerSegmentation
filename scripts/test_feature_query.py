import duckdb
import time

con = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})
t0 = time.perf_counter()

obs_parquet = "data/cleaned/observation_events.parquet"

print("Testing DuckDB Feature Extraction Query...")
sample_df = con.execute(f"""
WITH user_aggregates AS (
    SELECT 
        user_id,
        -- RFM Base (Lifetime in Observation: Oct 2019 - Jan 2020)
        MAX(CASE WHEN is_valid_for_monetary = TRUE THEN event_time END) AS max_purchase_time,
        COUNT(DISTINCT CASE WHEN is_valid_for_monetary = TRUE THEN user_session_id END) AS frequency,
        COALESCE(SUM(CASE WHEN is_valid_for_monetary = TRUE THEN price ELSE 0.0 END), 0.0) AS monetary,
        COUNT(CASE WHEN is_valid_for_monetary = TRUE THEN 1 END) AS total_purchase_items,
        
        -- General Lifetime
        MAX(event_time) AS max_event_time,
        MIN(event_time) AS min_event_time,
        COUNT(*) AS lifetime_events,
        COUNT(DISTINCT user_session_id) AS lifetime_sessions,
        
        -- Recent 30 days: [2020-01-02 00:00:00, 2020-02-01 00:00:00)
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' 
            THEN user_session_id 
        END) AS sessions_30d,
        
        COUNT(CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'view'
            THEN 1 
        END) AS views_30d,
        
        COUNT(CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'cart'
            THEN 1 
        END) AS carts_30d,
        
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00'
            THEN product_id 
        END) AS unique_products_30d,
        
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2020-01-02 00:00:00' AND event_time < '2020-02-01 00:00:00' AND event_type = 'cart'
            THEN user_session_id 
        END) AS cart_sessions_30d,
        
        -- Previous 30 days: [2019-12-03 00:00:00, 2020-01-02 00:00:00)
        COUNT(DISTINCT CASE 
            WHEN event_time >= '2019-12-03 00:00:00' AND event_time < '2020-01-02 00:00:00' 
            THEN user_session_id 
        END) AS sessions_previous_30d
        
    FROM read_parquet('{obs_parquet}')
    GROUP BY user_id
)
SELECT 
    user_id,
    -- Recency in days relative to cutoff 2020-02-01 00:00:00 UTC
    CASE 
        WHEN max_purchase_time IS NOT NULL 
        THEN ROUND(EXTRACT(EPOCH FROM (TIMESTAMP '2020-02-01 00:00:00' - max_purchase_time)) / 86400.0, 2)
        ELSE NULL 
    END AS recency_days,
    
    frequency,
    ROUND(monetary, 2) AS monetary,
    
    CASE 
        WHEN frequency > 0 THEN ROUND(monetary / frequency, 2)
        ELSE 0.0 
    END AS monetary_per_session,
    
    CASE 
        WHEN frequency > 0 THEN ROUND(total_purchase_items * 1.0 / frequency, 2)
        ELSE 0.0 
    END AS items_per_purchase_session,
    
    ROUND(EXTRACT(EPOCH FROM (TIMESTAMP '2020-02-01 00:00:00' - max_event_time)) / 86400.0, 2) AS days_since_last_event,
    
    sessions_30d,
    views_30d,
    carts_30d,
    unique_products_30d,
    cart_sessions_30d,
    sessions_previous_30d,
    sessions_30d AS sessions_recent_30d,
    
    (sessions_30d - sessions_previous_30d) AS activity_difference,
    ROUND(LN((sessions_30d + 1.0) / (sessions_previous_30d + 1.0)), 4) AS log_activity_ratio,
    
    lifetime_events,
    lifetime_sessions,
    
    CASE 
        WHEN frequency > 0 AND monetary > 0 THEN TRUE 
        ELSE FALSE 
    END AS is_buyer
FROM user_aggregates
LIMIT 10
""").fetchdf()

t1 = time.perf_counter()
print(f"Sample 10 users extracted in {t1 - t0:.2f}s:")
print(sample_df)
