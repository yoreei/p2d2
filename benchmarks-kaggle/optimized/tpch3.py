query = """
select
	l_orderkey,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	o_orderdate,
	o_shippriority
from
	customer,
	orders,
	lineitem
where
	c_mktsegment = ':1'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date ':2'
	and l_shipdate > date ':2'
group by
	l_orderkey,
	o_orderdate,
	o_shippriority
order by
	revenue desc,
	o_orderdate;
"""
import pandas as pd
import numpy as np

import psycopg2
import time

start_clock = time.perf_counter()
    
conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
# variable CONN should be provided by the overseeing script. See benchmarker/main.py

result = pd.read_sql_query(query, con=conn)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
