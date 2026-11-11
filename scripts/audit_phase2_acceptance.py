import duckdb
import os
import json

con = duckdb.connect()

print("--- 1. AUDIT RAW SESSIONS GRAIN ---")
raw_path = "data/raw/*.csv"

# Query raw counts
res = con.execute(f"""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(DISTINCT user_session) AS distinct_session_uuid,
        COUNT(DISTINCT user_id) AS distinct_users,
        COUNT(CASE WHEN user_session IS NULL THEN 1 END) AS null_sessions,
        COUNT(DISTINCT (user_id || '_' || COALESCE(user_session, 'NULL'))) AS distinct_user_session_pairs_with_null,
        COUNT(DISTINCT (user_id || '_' || user_session)) AS distinct_user_session_pairs_non_null
    FROM read_csv('{raw_path}', auto_detect=true, header=true)
""").fetchone()

print(f"Total rows: {res[0]}")
print(f"Distinct user_session (non-null UUIDs): {res[1]}")
print(f"Distinct user_id: {res[2]}")
print(f"Null sessions: {res[3]}")
print(f"Distinct user_session composite with null: {res[4]}")
print(f"Distinct user_session composite non-null: {res[5]}")

# Where did 4,537,805 come from? Let's check!
print("\n--- Checking raw CSV session counts per month ---")
res_m = con.execute(f"""
    SELECT 
        _file,
        COUNT(*) AS rows,
        COUNT(DISTINCT user_session) AS distinct_sessions,
        COUNT(DISTINCT (user_id || '_' || user_session)) AS distinct_composite
    FROM read_csv('{raw_path}', auto_detect=true, header=true, filename=true)
    GROUP BY _file
    ORDER BY _file
""").fetchall()
sum_dist_sess = sum(r[2] for r in res_m)
sum_dist_comp = sum(r[3] for r in res_m)
print(f"Sum of monthly distinct user_session: {sum_dist_sess}")
print(f"Sum of monthly distinct composite: {sum_dist_comp}")

print("\n--- 2. AUDIT CLEAN SESSIONS GRAIN ---")
clean_path = "data/cleaned/clean_events.parquet"
res_clean = con.execute(f"""
    SELECT 
        COUNT(*) AS total_rows,
        COUNT(DISTINCT session_id) AS distinct_session_uuid,
        COUNT(DISTINCT user_id) AS distinct_users,
        COUNT(CASE WHEN session_id IS NULL THEN 1 END) AS null_sessions,
        COUNT(DISTINCT user_session_id) AS distinct_user_session_id
    FROM read_parquet('{clean_path}')
""").fetchone()

print(f"Total clean rows: {res_clean[0]}")
print(f"Distinct clean session_id: {res_clean[1]}")
print(f"Distinct clean users: {res_clean[2]}")
print(f"Null clean sessions: {res_clean[3]}")
print(f"Distinct clean user_session_id: {res_clean[4]}")

