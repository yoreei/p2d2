#!/bin/env python3
import pandas as pd
import psycopg2
import time


def action(name):
    return None


start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
gmaxi = pd.read_sql_query("SELECT MAX(l_orderkey), l_linenumber FROM lineitem GROUP BY l_linenumber", conn)
SHARED_DB_TIME.value = time.perf_counter() - start_clock


action(gmaxi)
