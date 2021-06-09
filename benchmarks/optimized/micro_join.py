#!/bin/env python3
import pandas as pd
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
joined = pd.read_sql_query("SELECT * FROM lineitem INNER JOIN orders ON l_orderkey = o_orderkey", conn)


action(joined)
