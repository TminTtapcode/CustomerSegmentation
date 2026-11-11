import duckdb

con = duckdb.connect()
raw_path = "data/raw/*.csv"

res = con.execute(f"""
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
        -- Cart sessions:
        COUNT(DISTINCT CASE WHEN event_type = 'cart' AND user_session IS NOT NULL THEN user_id || '_' || user_session END) AS raw_cart_sessions,
        COUNT(DISTINCT CASE WHEN rn = 1 AND event_type = 'cart' AND user_session IS NOT NULL THEN user_id || '_' || user_session END) AS clean_cart_sessions,
        
        -- Users with cart:
        COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS raw_cart_users,
        COUNT(DISTINCT CASE WHEN rn = 1 AND event_type = 'cart' THEN user_id END) AS clean_cart_users,
        
        -- Users with purchase:
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS raw_buyers,
        COUNT(DISTINCT CASE WHEN rn = 1 AND event_type = 'purchase' THEN user_id END) AS clean_buyers
    FROM raw_obs
""").fetchone()

print(f"Cart sessions: Raw = {res[0]:,} | Clean = {res[1]:,} | Diff = {res[0] - res[1]:,}")
print(f"Users with cart: Raw = {res[2]:,} | Clean = {res[3]:,} | Diff = {res[2] - res[3]:,}")
print(f"Buyers (Users with purchase): Raw = {res[4]:,} | Clean = {res[5]:,} | Diff = {res[4] - res[5]:,}")
