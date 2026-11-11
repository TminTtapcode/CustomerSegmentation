import duckdb

con = duckdb.connect()
raw_path = "data/raw/*.csv"

res = con.execute(f"""
    SELECT 
        COUNT(DISTINCT user_id) AS users_with_null_session,
        COUNT(*) AS rows_with_null_session
    FROM read_csv('{raw_path}', auto_detect=true, header=true)
    WHERE user_session IS NULL
""").fetchone()

print(f"Users with NULL session: {res[0]}")
print(f"Rows with NULL session: {res[1]}")

# Now check distinct non-null composite sessions in raw vs clean
raw_non_null = con.execute(f"""
    SELECT COUNT(DISTINCT (user_id || '_' || user_session))
    FROM read_csv('{raw_path}', auto_detect=true, header=true)
    WHERE user_session IS NOT NULL
""").fetchone()[0]

clean_non_null = con.execute(f"""
    SELECT COUNT(DISTINCT user_session_id)
    FROM read_parquet('data/cleaned/clean_events.parquet')
    WHERE user_session_id IS NOT NULL
""").fetchone()[0]

print(f"Raw non-null composite sessions: {raw_non_null}")
print(f"Clean non-null composite sessions: {clean_non_null}")
print(f"Difference: {raw_non_null - clean_non_null}")

# Also check distinct session_id (raw vs clean)
raw_sess_uuid = con.execute(f"""
    SELECT COUNT(DISTINCT user_session)
    FROM read_csv('{raw_path}', auto_detect=true, header=true)
    WHERE user_session IS NOT NULL
""").fetchone()[0]

clean_sess_uuid = con.execute(f"""
    SELECT COUNT(DISTINCT session_id)
    FROM read_parquet('data/cleaned/clean_events.parquet')
    WHERE session_id IS NOT NULL
""").fetchone()[0]

print(f"Raw distinct session UUIDs: {raw_sess_uuid}")
print(f"Clean distinct session UUIDs: {clean_sess_uuid}")
print(f"Difference: {raw_sess_uuid - clean_sess_uuid}")
