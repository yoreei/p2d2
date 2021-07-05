import time
start_clock = time.perf_counter()
import modin.pandas as pd

a = pd.read_sql_query("SELECT * FROM lineitem", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
b = a[["l_linenumber", "l_orderkey", "l_comment"]]
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
