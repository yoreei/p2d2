import pandas as pd
import psycopg2

def action(name):
    return None


conn = psycopg2.connect(CONNSTR)
a = pd.read_sql_query("SELECT * FROM lineitem", conn)
b = a[a['l_linenumber'] <= 0.05]     

action(b)
