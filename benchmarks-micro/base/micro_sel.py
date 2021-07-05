import time
start_clock = time.perf_counter()
import pandas as pd


a = pd.read_sql_query("SELECT * FROM lineitem", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
b = a[a['l_linenumber'] <= 0.05]     

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
