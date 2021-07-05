import time

start_clock = time.perf_counter()
import pandas as pd
import numpy as np


### DEBUG:
# CONNSTR='postgresql://root:root@localhost/tpch1'
# from types import SimpleNamespace
# SHARED_DB_TIME=SimpleNamespace()
### END DEBUG


def udf_disc_price(extended, discount):
    import numpy as np

    return np.multiply(extended, np.subtract(1, discount))


def udf_charge(extended, discount, tax):
    import numpy as np

    return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))


region = pd.read_sql("SELECT * FROM region", con=CONNSTR)
nation = pd.read_sql("SELECT * FROM nation", con=CONNSTR)
supplier = pd.read_sql("SELECT * FROM supplier", con=CONNSTR)
customer = pd.read_sql("SELECT * FROM customer", con=CONNSTR)
orders = pd.read_sql("SELECT * FROM orders", parse_dates=["o_orderdate"], con=CONNSTR)
lineitem = pd.read_sql(
    "SELECT * FROM lineitem",
    parse_dates=["l_shipdate", "l_commitdate", "l_receiptdate"],
    con=CONNSTR,
)

# SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

orders = orders.astype({"o_orderstatus": "category", "o_orderpriority": "category"})
customer = customer.astype({"c_mktsegment": "category"})

lineitem = lineitem.astype({"l_returnflag": "category", "l_linestatus": "category"})

nr = nation.merge(
    region[region.r_name == "MIDDLE EAST"],
    left_on="n_regionkey",
    right_on="r_regionkey",
)[["n_nationkey", "n_name"]]
snr = supplier[["s_suppkey", "s_nationkey"]].merge(
    nr, left_on="s_nationkey", right_on="n_nationkey"
)[["s_suppkey", "s_nationkey", "n_name"]]
lsnr = lineitem[["l_suppkey", "l_orderkey", "l_extendedprice", "l_discount"]].merge(
    snr, left_on="l_suppkey", right_on="s_suppkey"
)
o = orders[["o_orderkey", "o_custkey", "o_orderdate"]][
    (orders.o_orderdate >= "1994-01-01") & (orders.o_orderdate < "1995-01-01")
][["o_orderkey", "o_custkey"]]
oc = o.merge(
    customer[["c_custkey", "c_nationkey"]], left_on="o_custkey", right_on="c_custkey"
)[["o_orderkey", "c_nationkey"]]
lsnroc = lsnr.merge(
    oc, left_on=["l_orderkey", "s_nationkey"], right_on=["o_orderkey", "c_nationkey"]
)[["l_extendedprice", "l_discount", "n_name"]]
lsnroc["volume"] = lsnroc.l_extendedprice * (1 - lsnroc.l_discount)
result = (
    lsnroc.groupby("n_name")
    .agg({"volume": sum})
    .reset_index()
    .sort_values("volume", ascending=False)
)

SHARED_WALL_TIME.value = time.perf_counter() - start_clock
print(f"{result.columns=}, {len(result)=}")
