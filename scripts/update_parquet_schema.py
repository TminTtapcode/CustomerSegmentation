import duckdb
import time
import os

con = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})
t0 = time.perf_counter()

print("Upgrading schema of observation_events.parquet...")
con.execute("""
    COPY (
        SELECT 
            event_time,
            event_date,
            event_type,
            user_id,
            session_id,
            user_session_id,
            product_id,
            category_id,
            category_code,
            brand,
            price,
            source_month,
            split_partition,
            quality_flag,
            is_valid_for_monetary,
            is_valid_for_engagement,
            is_valid_session,
            (brand = 'unknown') AS is_missing_brand,
            (category_code = 'unknown') AS is_missing_category_code,
            (price <= 0) AS is_invalid_price,
            (session_id IS NULL) AS is_missing_session
        FROM read_parquet('data/cleaned/observation_events.parquet')
    ) TO 'data/cleaned/observation_events_new.parquet' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
""")

print("Upgrading schema of holdout_events.parquet...")
con.execute("""
    COPY (
        SELECT 
            event_time,
            event_date,
            event_type,
            user_id,
            session_id,
            user_session_id,
            product_id,
            category_id,
            category_code,
            brand,
            price,
            source_month,
            split_partition,
            quality_flag,
            is_valid_for_monetary,
            is_valid_for_engagement,
            is_valid_session,
            (brand = 'unknown') AS is_missing_brand,
            (category_code = 'unknown') AS is_missing_category_code,
            (price <= 0) AS is_invalid_price,
            (session_id IS NULL) AS is_missing_session
        FROM read_parquet('data/cleaned/holdout_events.parquet')
    ) TO 'data/cleaned/holdout_events_new.parquet' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
""")

print("Upgrading schema of clean_events.parquet...")
con.execute("""
    COPY (
        SELECT 
            event_time,
            event_date,
            event_type,
            user_id,
            session_id,
            user_session_id,
            product_id,
            category_id,
            category_code,
            brand,
            price,
            source_month,
            split_partition,
            quality_flag,
            is_valid_for_monetary,
            is_valid_for_engagement,
            is_valid_session,
            (brand = 'unknown') AS is_missing_brand,
            (category_code = 'unknown') AS is_missing_category_code,
            (price <= 0) AS is_invalid_price,
            (session_id IS NULL) AS is_missing_session
        FROM read_parquet('data/cleaned/clean_events.parquet')
    ) TO 'data/cleaned/clean_events_new.parquet' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
""")

con.close()

# Atomically replace files
os.replace('data/cleaned/observation_events_new.parquet', 'data/cleaned/observation_events.parquet')
os.replace('data/cleaned/holdout_events_new.parquet', 'data/cleaned/holdout_events.parquet')
os.replace('data/cleaned/clean_events_new.parquet', 'data/cleaned/clean_events.parquet')

t1 = time.perf_counter()
print(f"All Parquet files updated with 4 independent flags in {t1 - t0:.2f}s!")

# Print new file sizes
for fname in ['clean_events.parquet', 'observation_events.parquet', 'holdout_events.parquet']:
    fpath = os.path.join('data/cleaned', fname)
    size_mb = os.path.getsize(fpath) / (1024 * 1024)
    print(f"  {fname}: {size_mb:.2f} MB")

