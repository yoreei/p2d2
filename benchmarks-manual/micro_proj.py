#!/bin/env python3
import pandas as pd
import psycopg2
import time


CONNSTR = f"host=localhost dbname=tpch1 user=root password=root"

start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT * FROM orders", conn)
#SHARED_DB_TIME is multiprocessing.Value
print(time.perf_counter() - start_clock)
