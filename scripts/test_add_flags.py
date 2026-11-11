import duckdb
import time

con = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})
t0 = time.perf_counter()

print("Testing transformation from clean_events.parquet to updated schema...")
res = con.execute("""
    SELECT 
        *,
        (brand = 'unknown') AS is_missing_brand,
        (category_code = 'unknown') AS is_missing_category_code,
        (price <= 0) AS is_invalid_price,
        (session_id IS NULL) AS is_missing_session
    FROM read_parquet('data/cleaned/clean_events.parquet')
    LIMIT 10
""").fetchdf()

t1 = time.perf_counter()
print(f"Sample queried in {t1 - t0:.2f}s:")
print(res[['event_type', 'is_missing_brand', 'is_missing_category_code', 'is_invalid_price', 'is_missing_session']])
