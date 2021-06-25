import pandas as pd
import psycopg2
import time


def action(name):
    return None


start_clock = time.perf_counter()
conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT l_linenumber FROM lineitem", conn)
SHARED_DB_TIME.value = time.perf_counter() - start_clock
action(a)
