#!/bin/env python3
# import pandas as pd
import modin.pandas as pd
import psycopg2
import time


def action(name):
    return None


start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
df = pd.read_sql_query("SELECT l_linenumber, l_orderkey FROM lineitem", conn)
SHARED_DB_TIME.value = time.perf_counter() - start_clock

gmaxi = df.groupby(["l_linenumber"]).max()
# gmaxi =df.groupby(['l_linestatus']).max()
# gmaxi =df.groupby(['l_shipmode']).max()

action(gmaxi)
