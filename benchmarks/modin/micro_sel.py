# import pandas as pd
import modin.pandas as pd
import psycopg2


def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT * FROM lineitem", conn)

sel = a[a["l_linenumber"] <= 0.05] # roughly in the middle

action(sel)
