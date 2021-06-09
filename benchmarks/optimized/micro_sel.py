import pandas as pd
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT * FROM lineitem WHERE l_linenumber <= 0.05", conn)

action(a)
