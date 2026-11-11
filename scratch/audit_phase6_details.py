import duckdb
con = duckdb.connect()

print("--- Buyer recommendations schema ---")
for col in con.execute("DESCRIBE SELECT * FROM 'outputs/recommendations/buyer_recommendations.parquet' LIMIT 1").fetchall():
    print(col)

print("\n--- Non-buyer recommendations schema ---")
for col in con.execute("DESCRIBE SELECT * FROM 'outputs/recommendations/non_buyer_recommendations.parquet' LIMIT 1").fetchall():
    print(col)

print("\n--- Sample Buyer Recommendation (First row) ---")
print(con.execute("SELECT * FROM 'outputs/recommendations/buyer_recommendations.parquet' LIMIT 1").fetchone())

print("\n--- Sample Non-Buyer Recommendation (First row) ---")
print(con.execute("SELECT * FROM 'outputs/recommendations/non_buyer_recommendations.parquet' LIMIT 1").fetchone())

