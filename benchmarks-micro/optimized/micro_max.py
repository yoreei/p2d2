import time
start_clock = time.perf_counter()
import pandas as pd

gmaxi = pd.read_sql_query("SELECT MAX(l_orderkey), l_linenumber FROM lineitem GROUP BY l_linenumber", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
