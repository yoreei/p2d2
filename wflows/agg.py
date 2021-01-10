#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

df1 = pd.read_sql_query('SELECT * FROM orders', conn)
df2 = pd.read_sql_query('SELECT * FROM customer', conn)
proj1 = df1.loc[:,['o_orderstatus','o_custkey']]
proj2 = df2.loc[:,['c_custkey', 'c_nationkey', 'c_acctbal']]
single2 = df2.loc[:,['c_acctbal']]

m2 = df2.max()
gagg = df2.groupby("c_nationkey").agg({'c_nationkey': np.sum, 'c_acctbal': np.max})
nogroup1 = df2.agg({'c_nationkey': np.sum, 'c_acctbal': np.max})
nogroup2 = df2.agg({'c_nationkey': [np.sum], 'c_acctbal': [np.max]})

breakpoint()

print(gagg)
print("the end")

# .join does not correstpond to SQL JOIN
#joined = df1.join(other = df2.set_index('c_custkey'), on='o_custkey', how = "inner")
