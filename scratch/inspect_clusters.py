import duckdb

con = duckdb.connect()
print("Columns in buyer_clusters.parquet:")
for row in con.execute("DESCRIBE SELECT * FROM 'data/features/buyer_clusters.parquet'").fetchall():
    print(" ", row[0], row[1])

print("\nTotal rows in buyer_clusters.parquet:", con.execute("SELECT COUNT(*) FROM 'data/features/buyer_clusters.parquet'").fetchone()[0])

print("\nCluster Distribution:")
dist = con.execute("""
    SELECT cluster, cluster_name, COUNT(*) as n, ROUND(COUNT(*)*100.0/92652, 2) as pct 
    FROM 'data/features/buyer_clusters.parquet' 
    GROUP BY cluster, cluster_name 
    ORDER BY cluster
""").fetchall()
for r in dist:
    print(f"  Cluster {r[0]} ({r[1]}): {r[2]:,} customers ({r[3]}%)")

