import duckdb
import pandas as pd
import numpy as np
from scipy import stats

con = duckdb.connect()

print("--- 1. Schema of observation_events.parquet ---")
cols = con.execute("DESCRIBE SELECT * FROM 'data/cleaned/observation_events.parquet'").df()
print(cols[['column_name', 'column_type']])

print("\n--- 2. Purchase User Stats & 3 Monetary Cases ---")
# Check 3 cases:
# Case 1: Customers with valid purchase events and positive monetary
# Case 2: Customers with purchase events but ALL monetary invalid (price <= 0 or is_valid_for_monetary = false)
# Case 3: Customers with no purchase events in Observation

query_cases = """
WITH user_purchases AS (
    SELECT 
        user_id,
        COUNT(*) as total_purchase_events,
        COUNT(CASE WHEN is_valid_for_monetary = true AND price > 0 THEN 1 END) as valid_purchases,
        COUNT(CASE WHEN is_valid_for_monetary = false OR price <= 0 THEN 1 END) as invalid_purchases,
        SUM(CASE WHEN is_valid_for_monetary = true AND price > 0 THEN price ELSE 0 END) as valid_monetary_sum
    FROM 'data/cleaned/observation_events.parquet'
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
all_users AS (
    SELECT DISTINCT user_id FROM 'data/cleaned/observation_events.parquet'
)
SELECT 
    COUNT(a.user_id) as total_observation_users,
    COUNT(u.user_id) as users_with_any_purchase_event,
    COUNT(CASE WHEN u.valid_purchases > 0 AND u.valid_monetary_sum > 0 THEN 1 END) as case1_valid_purchase_positive_monetary,
    COUNT(CASE WHEN u.user_id IS NOT NULL AND u.valid_purchases = 0 THEN 1 END) as case2_all_purchase_events_invalid,
    COUNT(CASE WHEN u.valid_purchases > 0 AND u.valid_monetary_sum = 0 THEN 1 END) as case2b_valid_purchase_zero_monetary,
    COUNT(CASE WHEN u.user_id IS NULL THEN 1 END) as case3_no_purchase_events
FROM all_users a
LEFT JOIN user_purchases u ON a.user_id = u.user_id
"""
df_cases = con.execute(query_cases).df()
print(df_cases.to_string())

print("\n--- 3. Are there any users in case 2? Let's check them ---")
query_invalid_users = """
SELECT 
    user_id,
    COUNT(*) as num_purchases,
    list(price) as prices
FROM 'data/cleaned/observation_events.parquet'
WHERE event_type = 'purchase'
GROUP BY user_id
HAVING COUNT(CASE WHEN is_valid_for_monetary = true AND price > 0 THEN 1 END) = 0
"""
df_inv = con.execute(query_invalid_users).df()
print("Number of users with ONLY invalid purchase events:", len(df_inv))
if len(df_inv) > 0:
    print(df_inv.head())

print("\n--- 4. Feature normality check on log_activity_ratio ---")
df_feat = con.execute("SELECT log_activity_ratio FROM 'data/features/customer_features.parquet'").df()
ratio = df_feat['log_activity_ratio'].values
print("log_activity_ratio descriptive stats:")
print(f"Count: {len(ratio):,}")
print(f"Mean: {np.mean(ratio):.4f}, Std: {np.std(ratio):.4f}, Median: {np.median(ratio):.4f}")
print(f"Min: {np.min(ratio):.4f}, Max: {np.max(ratio):.4f}")
print(f"Skewness: {stats.skew(ratio):.4f}")
print(f"Kurtosis (excess): {stats.kurtosis(ratio):.4f}")
# Shapiro-Wilk on sample of 5000 (since 1.34M exceeds Shapiro limit 5000)
np.random.seed(42)
sample_ratio = np.random.choice(ratio, size=5000, replace=False)
shapiro_stat, shapiro_p = stats.shapiro(sample_ratio)
print(f"Shapiro-Wilk test on 5k sample: stat={shapiro_stat:.4f}, p-value={shapiro_p:.4e}")
# Value counts of exact values (checking discreteness)
unique_vals = pd.Series(ratio).value_counts()
print(f"Top 5 frequent values:\n{unique_vals.head(5)}")

print("\n--- 5. Correlation & Multicollinearity between Frequency & Monetary ---")
df_buyers = con.execute("SELECT frequency, monetary, recency_days FROM 'data/features/buyer_features.parquet'").df()
r_fm, p_fm = stats.pearsonr(df_buyers['frequency'], df_buyers['monetary'])
r_fm_spearman, _ = stats.spearmanr(df_buyers['frequency'], df_buyers['monetary'])
print(f"Pearson r(F, M): {r_fm:.4f}")
print(f"Spearman rho(F, M): {r_fm_spearman:.4f}")

# Log-transformed correlation
r_log_fm, _ = stats.pearsonr(np.log1p(df_buyers['frequency']), np.log1p(df_buyers['monetary']))
print(f"Pearson r(log1p(F), log1p(M)): {r_log_fm:.4f}")

print("\n--- 6. Engagement check: Buyers vs Non-Buyers (41x interactions reconciliation) ---")
cols_feat = con.execute("DESCRIBE SELECT * FROM 'data/features/customer_features.parquet'").df()
print("Columns in customer_features.parquet:")
print(cols_feat['column_name'].tolist())

df_eng = con.execute("""
    SELECT 
        is_buyer,
        COUNT(*) as customer_count,
        AVG(lifetime_events) as mean_lifetime_events,
        MEDIAN(lifetime_events) as median_lifetime_events,
        AVG(lifetime_sessions) as mean_lifetime_sessions,
        MEDIAN(lifetime_sessions) as median_lifetime_sessions,
        AVG(views_30d) as mean_views_30d,
        MEDIAN(views_30d) as median_views_30d,
        AVG(sessions_30d) as mean_sessions_30d,
        MEDIAN(sessions_30d) as median_sessions_30d,
        AVG(carts_30d) as mean_carts_30d,
        MEDIAN(carts_30d) as median_carts_30d
    FROM 'data/features/customer_features.parquet'
    GROUP BY is_buyer
""").df()
print(df_eng.to_string())

mean_ratio_events = df_eng.loc[df_eng['is_buyer'] == True, 'mean_lifetime_events'].values[0] / df_eng.loc[df_eng['is_buyer'] == False, 'mean_lifetime_events'].values[0]
median_ratio_events = df_eng.loc[df_eng['is_buyer'] == True, 'median_lifetime_events'].values[0] / df_eng.loc[df_eng['is_buyer'] == False, 'median_lifetime_events'].values[0]
mean_ratio_sessions = df_eng.loc[df_eng['is_buyer'] == True, 'mean_lifetime_sessions'].values[0] / df_eng.loc[df_eng['is_buyer'] == False, 'mean_lifetime_sessions'].values[0]
median_ratio_sessions = df_eng.loc[df_eng['is_buyer'] == True, 'median_lifetime_sessions'].values[0] / df_eng.loc[df_eng['is_buyer'] == False, 'median_lifetime_sessions'].values[0]

print(f"\nRatio Buyers/Non-Buyers mean lifetime events: {mean_ratio_events:.2f}x")
print(f"Ratio Buyers/Non-Buyers median lifetime events: {median_ratio_events:.2f}x")
print(f"Ratio Buyers/Non-Buyers mean lifetime sessions: {mean_ratio_sessions:.2f}x")
print(f"Ratio Buyers/Non-Buyers median lifetime sessions: {median_ratio_sessions:.2f}x")

# Check 30d ratios
mean_ratio_views_30d = df_eng.loc[df_eng['is_buyer'] == True, 'mean_views_30d'].values[0] / df_eng.loc[df_eng['is_buyer'] == False, 'mean_views_30d'].values[0]
median_ratio_views_30d = (df_eng.loc[df_eng['is_buyer'] == True, 'median_views_30d'].values[0] + 1e-5) / (df_eng.loc[df_eng['is_buyer'] == False, 'median_views_30d'].values[0] + 1e-5)
print(f"Ratio Buyers/Non-Buyers mean views 30d: {mean_ratio_views_30d:.2f}x")


