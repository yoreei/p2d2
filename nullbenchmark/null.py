import pandas as pd
import psycopg2

conn = psycopg2.connect(f"host=localhost dbname=tpch user=p2d2 password=p2d2")


def action(name):
    return None


a = pd.read_sql_query("SELECT * FROM lineitem", conn)
mask = a.loc[:, "l_discount"] <= 0.05  # roughly in the middle
sel = a.loc[mask]

action(sel)
