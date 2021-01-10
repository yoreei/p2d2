#!/bin/env python3
import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

df1 = pd.read_sql_query('SELECT * FROM orders', conn)
df2 = pd.read_sql_query('SELECT * FROM customer', conn)
df1 = df1.loc[:,['o_orderstatus','o_custkey']]
df2 = df2.loc[:,['c_custkey','c_acctbal']]

joined = df1.merge(right=df2, how='inner', left_on='o_custkey', right_on='c_custkey', suffixes=('_x','_y'))

print(joined)
print("the end")

# .join does not correstpond to SQL JOIN
#joined = df1.join(other = df2.set_index('c_custkey'), on='o_custkey', how = "inner")
