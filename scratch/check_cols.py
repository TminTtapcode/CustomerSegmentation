import duckdb
con = duckdb.connect()
print("BUYER_CLUSTERS:", [r[0] for r in con.execute("DESCRIBE SELECT * FROM 'data/features/buyer_clusters.parquet'").fetchall()])
print("NON_BUYERS:", [r[0] for r in con.execute("DESCRIBE SELECT * FROM 'data/features/non_buyer_features.parquet'").fetchall()])
print("BUYER_FEATURES:", [r[0] for r in con.execute("DESCRIBE SELECT * FROM 'data/features/buyer_features.parquet'").fetchall()])

