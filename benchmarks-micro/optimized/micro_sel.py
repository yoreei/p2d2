import time
start_clock = time.perf_counter()
import pandas as pd

a = pd.read_sql_query("SELECT * FROM lineitem WHERE l_linenumber <= 0.05", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock

