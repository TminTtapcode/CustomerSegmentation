import duckdb

con = duckdb.connect()
con.execute("SET memory_limit = '2GB'; SET threads = 4;")

print("Checking duplicate events in raw CSVs...")
# Check exact duplicates across all 9 columns
exact_dup_query = """
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (event_time, event_type, product_id, category_id, category_code, brand, price, user_id, user_session)) AS distinct_rows
FROM read_csv('data/raw/20*.csv', header=True, auto_detect=True);
"""
res = con.execute(exact_dup_query).fetchdf()
total = int(res["total_rows"][0])
distinct = int(res["distinct_rows"][0])
duplicates = total - distinct
print(f"Total rows: {total:,}")
print(f"Distinct full rows: {distinct:,}")
print(f"Exact identical duplicate rows: {duplicates:,} ({duplicates / total * 100:.3f}%)")

# Check breakdown of duplicate rows by event_type
dup_by_type = con.execute("""
WITH ranked AS (
    SELECT 
        event_type,
        ROW_NUMBER() OVER (
            PARTITION BY event_time, event_type, product_id, category_id, user_id, user_session 
            ORDER BY price
        ) AS rn
    FROM read_csv('data/raw/20*.csv', header=True, auto_detect=True)
)
SELECT event_type, COUNT(*) AS duplicate_count
FROM ranked
WHERE rn > 1
GROUP BY event_type
ORDER BY duplicate_count DESC;
""").fetchdf()
print("\nDuplicates by event_type (same second, same user, same session, same product, same event_type):")
print(dup_by_type.to_string(index=False))

