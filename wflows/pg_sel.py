#!/usr/bin/env python3
import pandas as pd
import psycopg2
import pgconn

#conn = psycopg2.connect("host=localhost dbname=tpch user=vagrant password=vagrant")

conn = pgconn.get() #gives us a connection to PostgreSQL. 
a = pd.read_sql_query('SELECT * FROM customer', conn)
p = a.loc[:,'c_custkey'] # probably a view but we take it as a copy
cop = a.loc[:,['c_custkey','c_name','c_acctbal']].copy()
s = a.loc[a.loc[:,'c_acctbal']<800]
a.loc[a['c_acctbal'] < 800, 'c_acctbal'] = 4
