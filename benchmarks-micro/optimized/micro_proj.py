import time

start_clock = time.perf_counter()
import pandas as pd

a = pd.read_sql_query("SELECT l_linenumber FROM lineitem", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
