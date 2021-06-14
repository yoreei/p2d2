#!/bin/env python3
import pandas as pd
import psycopg2
import time


def action(name):
    return None

start_clock = time.perf_counter()

conn = psycopg2.connect(CONNSTR)
joined = pd.read_sql_query("SELECT * FROM lineitem INNER JOIN orders ON l_orderkey = o_orderkey", conn)

#SHARED_DB_TIME is a memory shared variable
SHARED_DB_TIME.value = time.perf_counter() - start_clock


action(joined)
