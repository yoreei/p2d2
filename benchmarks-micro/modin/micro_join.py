#!/bin/env python3
import time

start_clock = time.perf_counter()
import modin.pandas as pd

df1 = pd.read_sql("SELECT * FROM lineitem", CONNSTR)
df2 = pd.read_sql("SELECT * FROM orders", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock

joined = df1.merge(
    right=df2,
    how="inner",
    left_on="l_orderkey",
    right_on="o_orderkey",
    suffixes=("_x", "_y"),
)

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
