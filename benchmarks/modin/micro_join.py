#!/bin/env python3
# import pandas as pd
import modin.pandas as pd
import psycopg2
import time


def action(name):
    return None


start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
df1 = pd.read_sql_query("SELECT * FROM lineitem", conn)
df2 = pd.read_sql_query("SELECT * FROM orders", conn)
SHARED_DB_TIME.value = time.perf_counter() - start_clock

joined = df1.merge(
    right=df2,
    how="inner",
    left_on="l_orderkey",
    right_on="o_orderkey",
    suffixes=("_x", "_y"),
)

action(joined)
