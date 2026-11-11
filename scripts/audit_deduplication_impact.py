import duckdb
import json

con = duckdb.connect()
raw_path = "data/raw/*.csv"

print("--- 1. DUPLICATE BREAKDOWN BY EVENT_TYPE ---")
res_dup_types = con.execute(f"""
    WITH ranked AS (
        SELECT 
            event_type,
            price,
            product_id,
            user_id,
            user_session,
            event_time,
            ROW_NUMBER() OVER (
                PARTITION BY event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session
                ORDER BY event_time
            ) AS rn
        FROM read_csv('{raw_path}', auto_detect=true, header=true)
    )
    SELECT 
        event_type,
        COUNT(*) AS total_raw,
        COUNT(CASE WHEN rn = 1 THEN 1 END) AS clean_kept,
        COUNT(CASE WHEN rn > 1 THEN 1 END) AS duplicates_removed,
        ROUND(COUNT(CASE WHEN rn > 1 THEN 1 END) * 100.0 / COUNT(*), 4) AS dup_pct
    FROM ranked
    GROUP BY event_type
    ORDER BY duplicates_removed DESC
""").fetchall()

print(f"{'event_type':<20} | {'total_raw':<12} | {'clean_kept':<12} | {'duplicates':<12} | {'dup_pct':<8}")
print("-" * 75)
for r in res_dup_types:
    print(f"{r[0]:<20} | {r[1]:<12} | {r[2]:<12} | {r[3]:<12} | {r[4]:<8}%")

print("\n--- 2. DETAILED INSPECTION OF DUPLICATES ---")
# Check how many duplicates per duplicate cluster (max rn)
res_max_rn = con.execute(f"""
    WITH ranked AS (
        SELECT 
            event_type,
            ROW_NUMBER() OVER (
                PARTITION BY event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session
                ORDER BY event_time
            ) AS rn
        FROM read_csv('{raw_path}', auto_detect=true, header=true)
    )
    SELECT 
        event_type,
        MAX(rn) AS max_copies,
        COUNT(CASE WHEN rn = 2 THEN 1 END) AS copies_2,
        COUNT(CASE WHEN rn >= 3 THEN 1 END) AS copies_3_plus
    FROM ranked
    WHERE rn > 1
    GROUP BY event_type
""").fetchall()

print(f"{'event_type':<20} | {'max_copies':<12} | {'copies_2':<12} | {'copies_3_plus':<12}")
print("-" * 65)
for r in res_max_rn:
    print(f"{r[0]:<20} | {r[1]:<12} | {r[2]:<12} | {r[3]:<12}")

print("\n--- 3. IMPACT COMPARISON: KEEP ALL VS DROP DUP ON KEY METRICS ---")
# On Observation Window:
res_impact = con.execute(f"""
    WITH raw_obs AS (
        SELECT 
            *,
            ROW_NUMBER() OVER (
                PARTITION BY event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session
                ORDER BY event_time
            ) AS rn
        FROM read_csv('{raw_path}', auto_detect=true, header=true)
        WHERE event_time >= '2019-10-01 00:00:00 UTC' AND event_time < '2020-02-01 00:00:00 UTC'
    )
    SELECT 
        -- Policy KEEP ALL (rn >= 1)
        COUNT(*) AS raw_events,
        COUNT(DISTINCT user_id) AS raw_users,
        COUNT(DISTINCT CASE WHEN user_session IS NOT NULL THEN user_id || '_' || user_session END) AS raw_sessions,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS raw_purchases,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' AND user_session IS NOT NULL THEN user_id || '_' || user_session END) AS raw_purchase_sessions,
        SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS raw_purchase_monetary,
        COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS raw_views,
        COUNT(CASE WHEN event_type = 'cart' THEN 1 END) AS raw_carts,
        COUNT(CASE WHEN event_type = 'remove_from_cart' THEN 1 END) AS raw_removes,
        
        -- Policy DROP EXACT DUP (rn = 1)
        COUNT(CASE WHEN rn = 1 THEN 1 END) AS clean_events,
        COUNT(DISTINCT CASE WHEN rn = 1 THEN user_id END) AS clean_users,
        COUNT(DISTINCT CASE WHEN rn = 1 AND user_session IS NOT NULL THEN user_id || '_' || user_session END) AS clean_sessions,
        COUNT(CASE WHEN rn = 1 AND event_type = 'purchase' THEN 1 END) AS clean_purchases,
        COUNT(DISTINCT CASE WHEN rn = 1 AND event_type = 'purchase' AND user_session IS NOT NULL THEN user_id || '_' || user_session END) AS clean_purchase_sessions,
        SUM(CASE WHEN rn = 1 AND event_type = 'purchase' THEN price ELSE 0 END) AS clean_purchase_monetary,
        COUNT(CASE WHEN rn = 1 AND event_type = 'view' THEN 1 END) AS clean_views,
        COUNT(CASE WHEN rn = 1 AND event_type = 'cart' THEN 1 END) AS clean_carts,
        COUNT(CASE WHEN rn = 1 AND event_type = 'remove_from_cart' THEN 1 END) AS clean_removes
    FROM raw_obs
""").fetchone()

print(f"Observation Window Metrics Comparison:")
print(f"Total events: Raw = {res_impact[0]:,} | Clean = {res_impact[9]:,} | Diff = {res_impact[0] - res_impact[9]:,}")
print(f"Unique users: Raw = {res_impact[1]:,} | Clean = {res_impact[10]:,} | Diff = {res_impact[1] - res_impact[10]:,}")
print(f"Unique sessions: Raw = {res_impact[2]:,} | Clean = {res_impact[11]:,} | Diff = {res_impact[2] - res_impact[11]:,}")
print(f"Purchase events: Raw = {res_impact[3]:,} | Clean = {res_impact[12]:,} | Diff = {res_impact[3] - res_impact[12]:,}")
print(f"Purchase sessions: Raw = {res_impact[4]:,} | Clean = {res_impact[13]:,} | Diff = {res_impact[4] - res_impact[13]:,}")
print(f"Purchase Monetary (raw price): Raw = {res_impact[5]:,.2f} | Clean = {res_impact[14]:,.2f} | Diff = {res_impact[5] - res_impact[14]:,.2f}")
print(f"Views: Raw = {res_impact[6]:,} | Clean = {res_impact[15]:,} | Diff = {res_impact[6] - res_impact[15]:,}")
print(f"Carts: Raw = {res_impact[7]:,} | Clean = {res_impact[16]:,} | Diff = {res_impact[7] - res_impact[16]:,}")
print(f"Removes: Raw = {res_impact[8]:,} | Clean = {res_impact[17]:,} | Diff = {res_impact[8] - res_impact[17]:,}")

