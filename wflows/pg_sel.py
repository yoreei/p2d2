#!/usr/bin/env python3
import pandas as pd
import psycopg2

conn = psycopg2.connect("host=localhost dbname=tpch user=vagrant password=vagrant")

df = pd.read_sql_query("SELECT * FROM CUSTOMER", conn)
#df = pd.read_sql_table("customer", conn)
#breakpoint()
df = df["c_name"]
asn = 3
ans2 = asn
ans3 = 3+5

print (df)
