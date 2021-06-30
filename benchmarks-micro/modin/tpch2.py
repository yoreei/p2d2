import modin.pandas as pd
import numpy as np

import psycopg2
import time

def udf_disc_price(extended, discount):
	return np.multiply(extended, np.subtract(1, discount))

def udf_charge(extended, discount, tax):
	return np.multiply(extended, np.multiply(np.subtract(1, discount), np.add(1, tax)))

start_clock = time.perf_counter()
    
# conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
conn = psycopg2.connect(CONN)
# variable CONN should be provided by the overseeing script. See benchmarker/main.py

region = pd.read_sql_query("SELECT * FROM region", con=conn)
nation = pd.read_sql_query("SELECT * FROM nation", con=conn)
supplier = pd.read_sql_query("SELECT * FROM supplier", con=conn)
part = pd.read_sql_query("SELECT * FROM part", con=conn)
partsupp = pd.read_sql_query("SELECT * FROM partsupp", con=conn)

#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock

part = part.astype({'p_container' : 'category'})

ps = partsupp[["ps_partkey", "ps_suppkey", "ps_supplycost"]]
p = part[["p_partkey", "p_mfgr", "p_size", "p_type"]][(part.p_size == 38) & (part.p_type.str.match(".*TIN$"))][["p_partkey", "p_mfgr"]]
psp = ps.merge(p, left_on="ps_partkey", right_on="p_partkey")
s = supplier[["s_suppkey", "s_nationkey", "s_acctbal", "s_name", "s_address", "s_phone", "s_comment"]]
psps = psp.merge(s, left_on="ps_suppkey", right_on="s_suppkey")[["ps_partkey", "ps_supplycost", "p_mfgr", "s_nationkey",         "s_acctbal", "s_name", "s_address", "s_phone", "s_comment"]]
nr = nation.merge(region[region.r_name == "MIDDLE EAST"], left_on="n_regionkey", right_on="r_regionkey")[["n_nationkey", "n_name"]]
pspsnr = psps.merge(nr, left_on="s_nationkey", right_on="n_nationkey")[["ps_partkey", "ps_supplycost", "p_mfgr", "n_name", "s_acctbal", "s_name", "s_address", "s_phone", "s_comment"]]
aggr = pspsnr.groupby("ps_partkey").agg({'ps_supplycost' : min}).reset_index()
sj = pspsnr.merge(aggr, left_on=["ps_partkey", "ps_supplycost"], right_on=["ps_partkey", "ps_supplycost"])
result = sj[["s_acctbal", "s_name", "n_name", "ps_partkey", "p_mfgr", "s_address", "s_phone", "s_comment"]].sort_values(["s_acctbal", "n_name", "s_name", "ps_partkey"], ascending=[False, True, True, True]).head(100)
