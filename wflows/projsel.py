import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_acctbal','c_nationkey']] # we assume a projection is always a copy
mask=b.loc[:,'c_custkey']<=5
sel = b.loc[mask]

print(sel)
print("the end")
