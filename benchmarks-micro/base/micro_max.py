#!/bin/env python3
import pandas as pd
import psycopg2
import time


def action(name):
    return None
start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
# variable CONNSTR should be provided by the overseeing script. See benchmarker/main.py
# could also MAX(l_partkey), MAX(l_suppkey)
df = pd.read_sql_query("SELECT l_orderkey, l_linenumber FROM lineitem", conn)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

# 8 > l_linenumber > 0 for tpch1
gmaxi = df.groupby(["l_linenumber"]).max()
# gmaxi =df.groupby(['l_linestatus']).max()
# gmaxi =df.groupby(['l_shipmode']).max()

action(gmaxi)