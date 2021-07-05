import time
start_clock = time.perf_counter()
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

result = pd.read_sql_query(query, con=CONNSTR)
#SHARED_DB_TIME is multiprocessing.Value
SHARED_DB_TIME.value = time.perf_counter() - start_clock
SHARED_WALL_TIME.value = time.perf_counter() - start_clock
