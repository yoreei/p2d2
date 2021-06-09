#!/bin/env python3
import pandas as pd
import psycopg2



def action(name):
    return None
conn = psycopg2.connect(CONNSTR)
# variable CONN should be provided by the overseeing script. See benchmarker/main.py
df1 = pd.read_sql_query("SELECT * FROM lineitem", conn)
df2 = pd.read_sql_query("SELECT * FROM orders", conn)

joined = df1.merge(
    right=df2,
    how="inner",
    left_on="l_orderkey",
    right_on="o_orderkey",
    suffixes=("_x", "_y"),
)

action(joined)
