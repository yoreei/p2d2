query="""
select
	o_orderpriority,
	count(*) as order_count
from
	orders
where
	o_orderdate >= date '1997-07-01'
	and o_orderdate < date '1997-07-01' + interval '3' month
	and exists (
		select
			*
		from
			lineitem
		where
			l_orderkey = o_orderkey
			and l_commitdate < l_receiptdate
	)
group by
	o_orderpriority
order by
	o_orderpriority;
"""
import pandas as pd
import numpy as np

import psycopg2
import time

start_clock = time.perf_counter()
    
# conn = psycopg2.connect("host=localhost dbname=tpch10 user=root password=root")
conn = psycopg2.connect(CONN)
# variable CONN should be provided by the overseeing script. See benchmarker/main.py

result = pd.read_sql_query(query, con=conn)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
