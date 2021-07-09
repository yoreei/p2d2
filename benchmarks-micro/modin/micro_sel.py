import time

start_clock = time.perf_counter()
import modin.pandas as pd

a = pd.read_sql("SELECT * FROM lineitem", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock

sel = a[a["l_linenumber"] <= 0.05]  # roughly in the middle

SHARED_DB_TIME.value = time.perf_counter() - start_clock
