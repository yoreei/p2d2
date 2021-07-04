import pandas as pd
import numpy as np

import psycopg2
import time

start_clock = time.perf_counter()
    
### DEBUG:
CONNSTR='postgresql://root:root@localhost/tpch1'
from types import SimpleNamespace
SHARED_DB_TIME=SimpleNamespace()
### END DEBUG

# conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
#conn = psycopg2.connect(CONNSTR)
# variable CONNSTR should be provided by the overseeing script. See benchmarker/main.py


customer = pd.read_sql("SELECT * FROM customer", con=CONNSTR)
orders = pd.read_sql("SELECT * FROM orders", parse_dates=['o_orderdate'], con=CONNSTR)
lineitem = pd.read_sql("SELECT * FROM lineitem", parse_dates = ['l_shipdate', 'l_commitdate', 'l_receiptdate'], con=CONNSTR)
print("finished downloading")
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

customer = customer.astype({'c_mktsegment': 'category'})
orders = orders.astype({'o_orderstatus' : 'category', 'o_orderpriority' : 'category'})
lineitem = lineitem.astype({'l_returnflag': 'category', 'l_linestatus': 'category'})


def udf_disc_price(extended, discount):
	return np.multiply(extended, np.subtract(1, discount))

def udf_charge(extended, discount, tax):
	return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))

o  = orders[["o_orderkey", "o_custkey", "o_orderdate", "o_shippriority"]][orders.o_orderdate < "1995-03-29"][["o_orderkey", "o_custkey", "o_orderdate", "o_shippriority"]]
c  = customer[["c_custkey", "c_mktsegment"]][customer.c_mktsegment == "FURNITURE"][["c_custkey", "c_mktsegment"]]
oc = o.merge(c, left_on="o_custkey", right_on="c_custkey")[["o_orderkey", "o_orderdate", "o_shippriority"]]
l = lineitem[["l_orderkey", "l_extendedprice", "l_discount", "l_shipdate"]][lineitem.l_shipdate > "1995-03-29"][["l_orderkey", "l_extendedprice", "l_discount"]]
loc = l.merge(oc, left_on="l_orderkey", right_on="o_orderkey")
loc["volume"] = loc.l_extendedprice * (1 - loc.l_discount)
result = loc.groupby(["l_orderkey", "o_orderdate", "o_shippriority"]).agg({'volume' : sum}).reset_index()[["l_orderkey", "volume", "o_orderdate", "o_shippriority"]].sort_values(["volume", "o_orderdate"], ascending=[False, True]).head(10)
