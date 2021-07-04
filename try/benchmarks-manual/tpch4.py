import pandas as pd
import numpy as np

import psycopg2
import time

def udf_disc_price(extended, discount):
	return np.multiply(extended, np.subtract(1, discount))

def udf_charge(extended, discount, tax):
	return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))

start_clock = time.perf_counter()
    
conn = psycopg2.connect(CONNSTR)
# conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
# variable CONNSTR should be provided by the overseeing script. See benchmarker/main.py


orders = pd.read_sql_query("SELECT * FROM orders", parse_dates=['o_orderdate'], con=conn)

lineitem = pd.read_sql_query("SELECT * FROM lineitem", parse_dates = ['l_shipdate', 'l_commitdate', 'l_receiptdate'], con=conn)

orders = orders.astype({'o_orderstatus' : 'category', 'o_orderpriority' : 'category'})
lineitem = lineitem.astype({'l_returnflag': 'category', 'l_linestatus': 'category'})

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock


l = lineitem[["l_orderkey", "l_commitdate"]][lineitem.l_commitdate < lineitem.l_receiptdate][["l_orderkey"]]
o = orders[["o_orderkey", "o_orderpriority", "o_orderdate"]][(orders.o_orderdate >= "1997-07-01") & (orders.o_orderdate < "1997-10-01")][["o_orderkey", "o_orderpriority"]]
lo = l.merge(o, left_on="l_orderkey", right_on="o_orderkey").drop_duplicates()[["o_orderpriority"]]
result = lo.groupby("o_orderpriority").size().reset_index(name='counts').sort_values('o_orderpriority')
