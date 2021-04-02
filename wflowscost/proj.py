import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")
def action(name):
    return None

a = pd.read_sql_query('SELECT * FROM lineitem', conn)
b = a.loc[:,['l_linenumber','l_orderkey','l_comment']]
action(b)
