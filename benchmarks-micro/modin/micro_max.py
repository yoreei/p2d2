#!/bin/env python3
# import pandas as pd
import time
start_clock = time.perf_counter()
import modin.pandas as pd


df = pd.read_sql_query("SELECT l_linenumber, l_orderkey FROM lineitem", CONNSTR)
SHARED_DB_TIME.value = time.perf_counter() - start_clock

gmaxi = df.groupby(["l_linenumber"]).max()
# gmaxi =df.groupby(['l_linestatus']).max()
# gmaxi =df.groupby(['l_shipmode']).max()
SHARED_WALL_TIME.value = time.perf_counter() - start_clock

