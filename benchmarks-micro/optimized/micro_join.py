import time

start_clock = time.perf_counter()
import pandas as pd

joined = pd.read_sql_query(
    "SELECT * FROM lineitem INNER JOIN orders ON l_orderkey = o_orderkey", CONNSTR
)

# SHARED_DB_TIME is a memory shared variable
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
