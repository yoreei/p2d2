#!/bin/env python3
import pandas as pd
import numpy as np
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")
def action(name):
    return None

df = pd.read_sql_query('SELECT * FROM lineitem', conn)

gmaxi =df.groupby(['l_partkey']).max()
action(gmaxi)
