import time
start_clock = time.perf_counter()
import pandas as pd

# variable CONNSTR should be provided by the overseeing script. See benchmarker/main.py
df1 = pd.read_sql_query("SELECT * FROM lineitem", CONNSTR)
df2 = pd.read_sql_query("SELECT * FROM orders", CONNSTR)

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

joined = df1.merge(
    right=df2,
    how="inner",
    left_on="l_orderkey",
    right_on="o_orderkey",
    suffixes=("_x", "_y"),
)

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
