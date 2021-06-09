# import pandas as pd
import modin.pandas as pd
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT * FROM lineitem", conn)
b = a[["l_linenumber", "l_orderkey", "l_comment"]]
action(b)
