#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")

df = pd.read_sql_query('SELECT * FROM lineitem', conn)
proj1 = df.loc[:,['l_orderkey', 'l_linenumber', 'l_discount']]

maxi = proj1.max().to_frame().T
print(maxi)
