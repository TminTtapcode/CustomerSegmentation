import duckdb
import time

con = duckdb.connect(config={'memory_limit': '2GB', 'threads': '4'})

obs_parquet = "data/cleaned/observation_events.parquet"

print("--- TESTING OBSERVATION DATASET USER COUNTS ---")
res = con.execute(f"""
    SELECT 
        COUNT(*) AS total_obs_events,
        COUNT(DISTINCT user_id) AS total_obs_users,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' AND is_valid_for_monetary = TRUE THEN user_id END) AS buyers_count,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS all_purchase_users,
        COUNT(DISTINCT user_session_id) AS total_obs_sessions
    FROM read_parquet('{obs_parquet}')
""").fetchone()

print(f"Total Observation Events: {res[0]:,}")
print(f"Total Observation Users:  {res[1]:,}")
print(f"Buyers (valid monetary):  {res[2]:,}")
print(f"All Purchase Users:       {res[3]:,}")
print(f"Total Obs Sessions:       {res[4]:,}")
print(f"Non-Buyers:               {res[1] - res[2]:,}")

