import duckdb

con = duckdb.connect()
raw_path = "data/raw/*.csv"

# 3-step Monetary Reconciliation on Observation Window (2019-10-01 to 2020-02-01)
res = con.execute(f"""
    WITH raw_purchases AS (
        SELECT 
            price,
            event_time,
            product_id,
            user_id,
            user_session,
            ROW_NUMBER() OVER (
                PARTITION BY event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session
                ORDER BY event_time
            ) AS rn
        FROM read_csv('{raw_path}', auto_detect=true, header=true)
        WHERE event_type = 'purchase'
          AND event_time >= '2019-10-01 00:00:00 UTC' 
          AND event_time < '2020-02-01 00:00:00 UTC'
    )
    SELECT 
        -- Step 1: Raw
        COUNT(*) AS step1_count,
        SUM(price) AS step1_val,
        
        -- Step 2: After exact dedup (rn = 1)
        COUNT(CASE WHEN rn = 1 THEN 1 END) AS step2_count,
        SUM(CASE WHEN rn = 1 THEN price ELSE 0 END) AS step2_val,
        
        -- Step 3: After excluding price <= 0 on deduped data
        COUNT(CASE WHEN rn = 1 AND price > 0 THEN 1 END) AS step3_count,
        SUM(CASE WHEN rn = 1 AND price > 0 THEN price ELSE 0 END) AS step3_val,
        
        -- Excluded invalid purchases in step 3
        COUNT(CASE WHEN rn = 1 AND price <= 0 THEN 1 END) AS excluded_count,
        SUM(CASE WHEN rn = 1 AND price <= 0 THEN price ELSE 0 END) AS excluded_val,
        COUNT(CASE WHEN rn = 1 AND price < 0 THEN 1 END) AS neg_count,
        SUM(CASE WHEN rn = 1 AND price < 0 THEN price ELSE 0 END) AS neg_val,
        COUNT(CASE WHEN rn = 1 AND price = 0 THEN 1 END) AS zero_count
    FROM raw_purchases
""").fetchone()

print("--- 3-STEP MONETARY RECONCILIATION (OBSERVATION WINDOW) ---")
print(f"Step 1 (Raw Purchase Events): {res[0]:,} events | Value = {res[1]:,.2f} currency units")
print(f"Step 2 (After Exact Dedup):   {res[2]:,} events | Value = {res[3]:,.2f} currency units | Delta = {res[3] - res[1]:,.2f}")
print(f"Step 3 (After Invalid Price Filter): {res[4]:,} events | Value = {res[5]:,.2f} currency units | Delta = {res[5] - res[3]:,.2f}")
print(f"\nExcluded details in Step 3:")
print(f"  Total excluded purchases: {res[6]} events | Net impact: {res[7]:,.2f} currency units")
print(f"  Negative price purchases: {res[8]} events | Sum negative price: {res[9]:,.2f} currency units")
print(f"  Zero price purchases:     {res[10]} events")

