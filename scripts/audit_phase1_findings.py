"""Audit Phase 1 findings: November daily purchases, cart session rate, price anomalies, and session collisions."""
import json
import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = str(ROOT / "data" / "raw" / "20*.csv").replace("\\", "/")

con = duckdb.connect(database=":memory:")
con.execute("SET memory_limit = '2GB'")
con.execute("SET threads = 4")

print("=== 1. AUDITING NOVEMBER 2019 DAILY PURCHASES AND EVENTS ===")
nov_query = """
SELECT 
    CAST(event_time AS DATE) AS dt,
    COUNT(*) AS total_events,
    COUNT(*) FILTER (WHERE event_type = 'view') AS views,
    COUNT(*) FILTER (WHERE event_type = 'cart') AS carts,
    COUNT(*) FILTER (WHERE event_type = 'remove_from_cart') AS removes,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS purchases,
    COUNT(DISTINCT (user_id, user_session)) FILTER (WHERE event_type = 'purchase') AS purchase_sessions
FROM read_csv('data/raw/2019-Nov.csv', header=True, auto_detect=True)
GROUP BY CAST(event_time AS DATE)
ORDER BY purchases DESC
LIMIT 10;
"""
df_nov = con.execute(nov_query).fetchdf()
print("Top 10 purchase days in November 2019:")
print(df_nov.to_string(index=False))

print("\nNovember 2019 Monthly Total Check:")
nov_tot = con.execute("""
SELECT 
    COUNT(*) AS total_events,
    COUNT(*) FILTER (WHERE event_type = 'purchase') AS total_purchases,
    COUNT(DISTINCT (user_id, user_session)) FILTER (WHERE event_type = 'purchase') AS total_purchase_sessions
FROM read_csv('data/raw/2019-Nov.csv', header=True, auto_detect=True)
""").fetchdf()
print(nov_tot.to_string(index=False))

print("\n=== 2. AUDITING PRICE <= 0 BREAKDOWN BY EVENT TYPE ===")
price_audit = con.execute(f"""
SELECT 
    event_type,
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE price < 0) AS price_negative,
    COUNT(*) FILTER (WHERE price = 0) AS price_zero,
    COUNT(*) FILTER (WHERE price <= 0) AS price_le_zero,
    ROUND(COUNT(*) FILTER (WHERE price <= 0) * 100.0 / COUNT(*), 4) AS pct_le_zero,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM read_csv('{DATA_RAW}', header=True, auto_detect=True)
GROUP BY event_type
ORDER BY price_le_zero DESC;
""").fetchdf()
print("Breakdown of price <= 0 by event_type:")
print(price_audit.to_string(index=False))

print("\n=== 3. AUDITING SESSION ID COLLISIONS ACROSS USERS ===")
session_collision = con.execute(f"""
SELECT 
    COUNT(DISTINCT user_session) AS distinct_session_ids,
    COUNT(DISTINCT (user_id, user_session)) AS distinct_user_session_pairs,
    COUNT(DISTINCT (user_id, user_session)) - COUNT(DISTINCT user_session) AS collision_count
FROM read_csv('{DATA_RAW}', header=True, auto_detect=True)
WHERE user_session IS NOT NULL AND user_id IS NOT NULL;
""").fetchdf()
print("Session ID collision audit:")
print(session_collision.to_string(index=False))

print("\nSample of collided sessions (if any):")
collided_samples = con.execute(f"""
SELECT user_session, COUNT(DISTINCT user_id) AS user_count, LIST(DISTINCT user_id) AS users
FROM read_csv('{DATA_RAW}', header=True, auto_detect=True)
WHERE user_session IS NOT NULL AND user_id IS NOT NULL
GROUP BY user_session
HAVING COUNT(DISTINCT user_id) > 1
LIMIT 5;
""").fetchdf()
print(collided_samples.to_string(index=False))

print("\n=== 4. AUDITING CART SESSION NO-PURCHASE RATE ===")
cart_audit = con.execute(f"""
WITH session_summary AS (
    SELECT 
        user_id,
        user_session,
        BOOL_OR(event_type = 'cart') AS has_cart,
        BOOL_OR(event_type = 'purchase') AS has_purchase,
        MIN(event_time) FILTER (WHERE event_type = 'cart') AS first_cart_time,
        MAX(event_time) FILTER (WHERE event_type = 'purchase') AS last_purchase_time
    FROM read_csv('{DATA_RAW}', header=True, auto_detect=True)
    WHERE event_time >= '2019-10-01 00:00:00' AND event_time < '2020-02-01 00:00:00'
      AND user_id IS NOT NULL AND user_session IS NOT NULL
    GROUP BY user_id, user_session
)
SELECT 
    COUNT(*) AS total_valid_sessions,
    COUNT(*) FILTER (WHERE has_cart) AS cart_sessions,
    COUNT(*) FILTER (WHERE has_purchase) AS purchase_sessions,
    COUNT(*) FILTER (WHERE has_cart AND has_purchase) AS cart_and_purchase_sessions,
    COUNT(*) FILTER (WHERE has_cart AND has_purchase AND last_purchase_time > first_cart_time) AS cart_then_purchase_sessions,
    COUNT(*) FILTER (WHERE has_cart AND NOT has_purchase) AS cart_session_no_purchase
FROM session_summary;
""").fetchdf()
print("Cart session audit:")
print(cart_audit.to_string(index=False))

