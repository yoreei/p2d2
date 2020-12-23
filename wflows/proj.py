import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=vagrant password=vagrant")

a = pd.read_sql_query('SELECT * FROM customer', conn)
b = a.loc[:,['c_custkey','c_nationkey','c_acctbal']] # we assume a projection is always a copy
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
b = b.loc[:,['c_acctbal']]
print(b)
print(a)
print(b)
print("the end")
