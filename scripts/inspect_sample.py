import duckdb

con = duckdb.connect()
print("Reading first 5 rows of 2019-Oct.csv:")
df = con.execute("SELECT * FROM read_csv('data/raw/2019-Oct.csv', header=True, auto_detect=True) LIMIT 5").fetchdf()
print("Columns:", df.columns.tolist())
print(df)
print("\nSchema:")
schema = con.execute("DESCRIBE SELECT * FROM read_csv('data/raw/2019-Oct.csv', header=True, auto_detect=True) LIMIT 5").fetchall()
for col in schema:
    print(col)
