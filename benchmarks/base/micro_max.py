#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2


def action(name):
    return None
conn = psycopg2.connect(CONNSTR)
# variable CONNSTR should be provided by the overseeing script. See benchmarker/main.py
# could also MAX(l_partkey), MAX(l_suppkey)
df = pd.read_sql_query("SELECT l_orderkey, l_linenumber FROM lineitem", conn)

# 8 > l_linenumber > 0 for tpch1
gmaxi = df.groupby(["l_linenumber"]).max()
# gmaxi =df.groupby(['l_linestatus']).max()
# gmaxi =df.groupby(['l_shipmode']).max()

action(gmaxi)
