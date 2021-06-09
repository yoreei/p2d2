#!/bin/env python3
# import pandas as pd
import modin.pandas as pd
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
df = pd.read_sql_query("SELECT l_linenumber, l_orderkey FROM lineitem", conn)

gmaxi = df.groupby(["l_linenumber"]).max()
# gmaxi =df.groupby(['l_linestatus']).max()
# gmaxi =df.groupby(['l_shipmode']).max()

action(gmaxi)
