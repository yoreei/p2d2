import modin.pandas as pd
import numpy as np

import psycopg2
import time

def udf_disc_price(extended, discount):
	return np.multiply(extended, np.subtract(1, discount))

def udf_charge(extended, discount, tax):
	return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))

start_clock = time.perf_counter()
    
conn = psycopg2.connect(CONN)
#conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
# variable CONN should be provided by the overseeing script. See benchmarker/main.py

region = pd.read_sql_query("SELECT * FROM region", con=conn)
nation = pd.read_sql_query("SELECT * FROM nation", con=conn)
supplier = pd.read_sql_query("SELECT * FROM supplier", con=conn)
customer = pd.read_sql_query("SELECT * FROM customer", con=conn)
orders = pd.read_sql_query("SELECT * FROM orders", parse_dates=['o_orderdate'], con=conn)
lineitem = pd.read_sql_query("SELECT * FROM lineitem", parse_dates = ['l_shipdate', 'l_commitdate', 'l_receiptdate'], con=conn)

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

orders = orders.astype({'o_orderstatus' : 'category', 'o_orderpriority' : 'category'})
customer = customer['c_mktsegment'].astype({'c_mktsegment': 'category'})

lineitem = lineitem.astype({'l_returnflag': 'category', 'l_linestatus': 'category'})

nr = nation.merge(region[region.r_name == "MIDDLE EAST"], left_on="n_regionkey", right_on="r_regionkey")[["n_nationkey", "n_name"]]
snr = supplier[["s_suppkey", "s_nationkey"]].merge(nr, left_on="s_nationkey", right_on="n_nationkey")[["s_suppkey", "s_nationkey", "n_name"]]
lsnr = lineitem[["l_suppkey", "l_orderkey", "l_extendedprice", "l_discount"]].merge(snr, left_on="l_suppkey", right_on="s_suppkey")
o = orders[["o_orderkey", "o_custkey", "o_orderdate"]][(orders.o_orderdate >= "1994-01-01") & (orders.o_orderdate < "1995-01-01")][["o_orderkey", "o_custkey"]]
oc = o.merge(customer[["c_custkey", "c_nationkey"]], left_on="o_custkey", right_on="c_custkey")[["o_orderkey", "c_nationkey"]]
lsnroc = lsnr.merge(oc, left_on=["l_orderkey", "s_nationkey"], right_on=["o_orderkey", "c_nationkey"])[["l_extendedprice", "l_discount", "n_name"]]
lsnroc["volume"] = lsnroc.l_extendedprice * (1 - lsnroc.l_discount)
result = lsnroc.groupby("n_name").agg({'volume' : sum}).reset_index().sort_values("volume", ascending=False)
